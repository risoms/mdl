#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pipreqs - Generate pip requirements.txt file based on imports.
"""
from pdb import set_trace as breakpoint
from contextlib import contextmanager
import os
import sys
import re
import logging
import codecs
import ast
import traceback
from docopt import docopt
import requests
from yarg import json2package
from yarg.exceptions import HTTPError
import argparse

__version__ = '0.4.8'

REGEXP = [
	re.compile(r'^import (.+)$'),
	re.compile(r'^from ((?!\.+).*?) import (?:.*)$')
]

if sys.version_info[0] > 2:
	open_func = open
	py2 = False
else:
	open_func = codecs.open
	py2 = True
	py2_exclude = ["concurrent", "concurrent.futures"]


@contextmanager
def _open(filename=None, mode='r'):
	"""Open a file or ``sys.stdout`` depending on the provided filename.

	Parameters
	----------
	filename : :obj:`str`
		The path to the file that should be opened. If ``None`` or ``'-'``, ``sys.stdout`` or ``sys.stdin`` is
		returned depending on the desired mode. Defaults to ``None``.
	mode : :obj:`str`
		The mode that should be used to open the file.

	Yields
	------
	file :
		A file handle.

	"""
	if not filename or filename == '-':
		if not mode or 'r' in mode:
			file = sys.stdin
		elif 'w' in mode:
			file = sys.stdout
		else:
			raise ValueError('Invalid mode for file: {}'.format(mode))
	else:
		file = open(filename, mode)

	try:
		yield file
	finally:
		if file not in (sys.stdin, sys.stdout):
			file.close()

def get_all_imports(path, encoding=None, extra_ignore_dirs=None, follow_links=True):
	"""[summary]

	Parameters
	----------
	path : [type]
		[description]
	encoding : [type], optional
		[description], by default None
	extra_ignore_dirs : [type], optional
		[description], by default None
	follow_links : bool, optional
		[description], by default True

	Returns
	-------
	[type]
		[description]

	Raises
	------
	exc
		[description]
	"""
	imports = set()
	raw_imports = set()
	candidates = []
	ignore_errors = False
	ignore_dirs = [".hg", ".svn", ".git", ".tox", "__pycache__", "env", "venv"]

	if extra_ignore_dirs:
		ignore_dirs_parsed = []
		for e in extra_ignore_dirs:
			ignore_dirs_parsed.append(os.path.basename(os.path.realpath(e)))
		ignore_dirs.extend(ignore_dirs_parsed)

	walk = os.walk(path, followlinks=follow_links)
	for root, dirs, files in walk:
		dirs[:] = [d for d in dirs if d not in ignore_dirs]

		candidates.append(os.path.basename(root))
		files = [fn for fn in files if os.path.splitext(fn)[1] == ".py"]

		candidates += [os.path.splitext(fn)[0] for fn in files]
		for file in files:
			filename = os.path.join(root, file)
			with open_func(filename, "r", encoding=encoding) as f:
				print(filename)
				contents = f.read()
			try:
				tree = ast.parse(contents)
				for node in ast.walk(tree):
					if isinstance(node, ast.Import):
						for subnode in node.names:
							raw_imports.add(subnode.name)
					elif isinstance(node, ast.ImportFrom):
						raw_imports.add(node.module)
			except Exception as error:
				if ignore_errors:
					traceback.print_exc(error)
					logging.warn("Failed on file: %s"%(filename))
					continue
				else:
					logging.error("Failed on file: %s"%(filename))
					raise error

	# Clean up imports
	for name in [n for n in raw_imports if n]:
		# Sanity check: Name could have been None if the import
		# statement was as ``from . import X``
		# Cleanup: We only want to first part of the import.
		# Ex: from django.conf --> django.conf. But we only want django
		# as an import.
		cleaned_name, _, _ = name.partition('.')
		imports.add(cleaned_name)

	packages = imports - (set(candidates) & imports)
	logging.debug('Found packages: {0}'.format(packages))

	with open(join("stdlib"), "r") as f:
		data = {x.strip() for x in f}

	data = {x for x in data if x not in py2_exclude} if py2 else data
	return list(packages - data)

def filter_line(l):
	"""[summary]

	Parameters
	----------
	l : [type]
		[description]

	Returns
	-------
	[type]
		[description]
	"""
	return len(l) > 0 and l[0] != "#"

def generate_requirements_file(path, imports, versioning):
	"""[summary]

	Parameters
	----------
	path : [type]
		[description]
	imports : [type]
		[description]
	versioning : [type]
		[description]
	"""
	with open(path, "w") as out_file:
		logging.debug('Writing {num} requirements: {imports} to {file}'.format(
			num=len(imports),
			file=path,
			imports=", ".join([x['name'] for x in imports])
		))
		# if excluding version
		if versioning == "logging":
			pass
		elif versioning == None:
			fmt = '{name}\n'
			out_file.write(''.join(fmt.format(**item) for item in imports))
		elif versioning == "exact":
			fmt = '{name}=={version}\n'
			out_file.write(''.join(fmt.format(**item) if item['version'] else '{name}'.format(**item) for item in imports))
		else:
			fmt = '{name}>={version}\n'
			out_file.write(''.join(fmt.format(**item) if item['version'] else '{name}'.format(**item) for item in imports))

def get_imports_info(imports, pypi_server="https://pypi.python.org/pypi/", proxy=None):
	"""[summary]

	Parameters
	----------
	imports : [type]
		[description]
	pypi_server : str, optional
		[description], by default "https://pypi.python.org/pypi/"
	proxy : [type], optional
		[description], by default None

	Returns
	-------
	[type]
		[description]

	Raises
	------
	HTTPError
		[description]
	"""
	result = []

	for item in imports:
		try:
			response = requests.get(
				"{0}{1}/json".format(pypi_server, item), proxies=proxy)
			if response.status_code == 200:
				if hasattr(response.content, 'decode'):
					data = json2package(response.content.decode())
				else:
					data = json2package(response.content)
			elif response.status_code >= 300:
				raise HTTPError(status_code=response.status_code,
								reason=response.reason)
		except HTTPError:
			logging.debug(
				'Package %s does not exist or network problems', item)
			continue
		result.append({'name': item, 'version': data.latest_release_id})
	return result

def get_locally_installed_packages(encoding=None):
	"""[summary]

	Parameters
	----------
	encoding : [type], optional
		[description], by default None

	Returns
	-------
	[type]
		[description]
	"""
	packages = {}
	ignore = ["tests", "_tests", "egg", "EGG", "info"]
	for path in sys.path:
		for root, dirs, files in os.walk(path):
			for item in files:
				if "top_level" in item:
					item = os.path.join(root, item)
					with open_func(item, "r", encoding=encoding) as f:
						package = root.split(os.sep)[-1].split("-")
						try:
							package_import = f.read().strip().split("\n")
						except:  # NOQA
							# TODO: What errors do we intend to suppress here?
							continue
						for i_item in package_import:
							if ((i_item not in ignore) and
									(package[0] not in ignore)):
								version = None
								if len(package) > 1:
									version = package[1].replace(
										".dist", "").replace(".egg", "")

								packages[i_item] = {
									'version': version,
									'name': package[0]
								}
	return packages

def get_import_local(imports, encoding=None):
	"""[summary]

	Parameters
	----------
	imports : [type]
		[description]
	encoding : [type], optional
		[description], by default None

	Returns
	-------
	[type]
		[description]
	"""
	local = get_locally_installed_packages()
	result = []
	for item in imports:
		if item.lower() in local:
			result.append(local[item.lower()])

	# removing duplicates of package/version
	result_unique = [
		dict(t)
		for t in set([
			tuple(d.items()) for d in result
		])
	]

	return result_unique

def get_pkg_names(pkgs):
	"""Get PyPI package names from a list of imports.

	Parameters
	----------
	pkgs: :obj:`list` of :obj:`str`
		List of import names.

	Returns
	-------
	results: :obj:`list` of :obj:`str`
		The corresponding PyPI package names.
	"""
	_result = set()
	with open(join("mapping"), "r") as f:
		data = dict(x.strip().split(":") for x in f)
	for pkg in pkgs:
		# Look up the mapped requirement. If a mapping isn't found,
		# simply use the package name.
		_result.add(data.get(pkg, pkg))
	# Return a sorted list for backward compatibility.
	results = sorted(_result)
	return results

def get_name_without_alias(name):
	"""[summary]

	Parameters
	----------
	name : [type]
		[description]

	Returns
	-------
	[type]
		[description]
	"""
	if "import " in name:
		match = REGEXP[0].match(name.strip())
		if match:
			name = match.groups(0)[0]
	return name.partition(' as ')[0].partition('.')[0].strip()

def join(f):
	"""[summary]

	Parameters
	----------
	f : [type]
		[description]

	Returns
	-------
	[type]
		[description]
	"""
	return os.path.join(os.path.dirname(__file__), f)

def parse_requirements(file_):
	"""Parse a requirements formatted file.

	Traverse a string until a delimiter is detected, then split at said
	delimiter, get module name by element index, create a dict consisting of
	module:version, and add dict to list of parsed modules.

	Parameters
	----------
	file_ : [type]
		File to parse.

	Raises
	------
	OSerror
		If there's any issues accessing the file.

	Returns
	-------
	[type]
		The contents of the file, excluding comments.
	"""
	modules = []
	# For the dependency identifier specification, see
	# https://www.python.org/dev/peps/pep-0508/#complete-grammar
	delim = ["<", ">", "=", "!", "~"]

	try:
		f = open_func(file_, "r")
	except OSError:
		logging.error("Failed on file: {}".format(file_))
		raise
	else:
		data = [x.strip() for x in f.readlines() if x != "\n"]
	finally:
		f.close()

	data = [x for x in data if x[0].isalpha()]

	for x in data:
		# Check for modules w/o a specifier.
		if not any([y in x for y in delim]):
			modules.append({"name": x, "version": None})
		for y in x:
			if y in delim:
				module = x.split(y)
				module_name = module[0]
				module_version = module[-1].replace("=", "")
				module = {"name": module_name, "version": module_version}

				if module not in modules:
					modules.append(module)

				break

	return modules

def compare_modules(file_, imports):
	"""Compare modules in a file to imported modules in a project.

	Parameters
	----------
	file_ : :obj:`str`
		File to parse for modules to be compared.
	imports : :obj:`tuple`
		Modules being imported in the project.

	Returns
	-------
	modules_not_imported : :obj:`list`
		The modules not imported in the project, but do exist in the specified file.
	"""
	modules = parse_requirements(file_)

	imports = [imports[i]["name"] for i in range(len(imports))]
	modules = [modules[i]["name"] for i in range(len(modules))]
	modules_not_imported = set(modules) - set(imports)

	return modules_not_imported

def diff(file_, imports):
	"""Display the difference between modules in a file and imported modules.

	Parameters
	----------
	file_ : [type]
		[description]
	imports : [type]
		[description]
	"""
	modules_not_imported = compare_modules(file_, imports)

	logging.info(
		"The following modules are in {} but do not seem to be imported: "
		"{}".format(file_, ", ".join(x for x in modules_not_imported)))

def clean(file_, imports):
	"""Remove modules that aren't imported in project from file.

	Parameters
	----------
	file_ : [type]
		[description]
	imports : [type]
		[description]
	"""
	modules_not_imported = compare_modules(file_, imports)
	re_remove = re.compile("|".join(modules_not_imported))
	to_write = []

	try:
		f = open_func(file_, "r+")
	except OSError:
		logging.error("Failed on file: {}".format(file_))
		raise
	else:
		for i in f.readlines():
			if re_remove.match(i) is None:
				to_write.append(i)
		f.seek(0)
		f.truncate()

		for i in to_write:
			f.write(i)
	finally:
		f.close()

	logging.info("Successfully cleaned up requirements in " + file_)

def init(args):
	"""[summary]

	Parameters
	----------
	args : [type]
		[description]
	"""
	# arguments
	encoding = args['encoding']
	extra_ignore_dirs = args['ignore']
	follow_links = not args['no_follow_links']

	# path
	input_path = args['path'][0]
	if input_path is None:
		input_path = os.path.abspath(os.curdir)

	# path
	path = (args["savepath"] if args["savepath"] else os.path.join(input_path, "requirements.txt"))

	# ignored
	if args['ignore']:
		extra_ignore_dirs = args['ignore']
		logging.debug("ignored: %s"%(extra_ignore_dirs))
	else:
		extra_ignore_dirs = None

	# get list of candidates
	candidates = get_all_imports(input_path, encoding=encoding, extra_ignore_dirs=extra_ignore_dirs, follow_links=follow_links)
	candidates = get_pkg_names(candidates)
	logging.debug("found imports: %s"%(candidates))
	pypi_server = "https://pypi.python.org/pypi/"
	proxy = None

	# include
	if args["include"]:
		include = args["include"].split(',')
		logging.debug("include: %s"%(include))
		candidates = candidates + include

	# exclude
	if args["exclude"]:
		exclude = args["exclude"].split(',')
		logging.debug("exclude: %s"%(exclude))
		candidates = [item for item in candidates if item not in exclude]

	# PyPi
	if args["pypi_server"]:
		pypi_server = args["pypi-server"]

	# proxy
	if args["proxy"]:
		proxy = {'http': args["proxy"], 'https': args["proxy"]}

	# use_local
	if args["use_local"]:
		logging.debug("getting package information ONLY from local installation")
		imports = get_import_local(candidates, encoding=encoding)
	else:
		logging.debug("fetting packages information from pypi")
		local = get_import_local(candidates, encoding=encoding)
		# Get packages that were not found locally
		difference = [x for x in candidates if x.lower() not in [z['name'].lower() for z in local]]
		imports = local + get_imports_info(difference, proxy=proxy, pypi_server=pypi_server)

	# differences
	if args["diff"]:
		diff(args["diff"], imports)
		return

	# clean
	if args["clean"]:
		clean(args["clean"], imports)
		return

	# force
	if (not args["print"] and not args["savepath"] and not args["force"] and os.path.exists(path)):
		logging.warning("requirements.txt already exists, use --force to overwrite it")
		return

	# versioning
	if args["version"] == "greater":
		versioning = "greater"
	elif args["version"] == "exact":
		versioning = "exact"
	elif ((args["version"] == "None") or (args["version"] is None)):
		versioning = None

	# finish
	if args["print"]:
		generate_requirements_file('-', imports, 'logging')
		logging.info("Successfully created requirements.txt")
	else:
		generate_requirements_file(path, imports, versioning)
		logging.info("Successfully saved requirements file in " + path)

def run(args):
	"""[summary]

	Parameters
	----------
	args : [type]
		[description]
	"""
	_args = vars(args)
	log_level = logging.DEBUG if _args['debug'] else logging.INFO
	logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
	try:
		init(_args)
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	# https://docs.python.org/3.7/library/argparse.html
	sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
	parser = argparse.ArgumentParser(
		prog = sys.argv[0],
		usage = "Generate pip requirements.txt file based on imports."
	)
	# Arguments
	parser.add_argument("path", nargs='+', help="The path to the directory containing the application \
		files for which a requirements file should be generated (defaults to the current working directory).")
	# options
	parser.add_argument("--use-local", help="Use ONLY local package info instead of querying PyPI.", default=None)
	parser.add_argument("--pypi-server", help="Use custom PyPi server.", default=None)
	parser.add_argument("--proxy", help='Use Proxy, parameter will be passed to requests\n\
		library. You can also just set the environments parameter in your terminal: $ export HTTPS_PROXY="https://10.10.1.10:1080"', default=None)
	parser.add_argument("--debug", help="Print debug information.", nargs='?', const=True, default=None)
	parser.add_argument("--include", help="Include modules.", nargs='?', const=True, default=None)
	parser.add_argument("--exclude", help="Exclude modules.", nargs='?', const=True, default=None)
	parser.add_argument("--ignore", help="Ignore extra directories, each separated by a comma.", default=None)
	parser.add_argument("--no-follow-links", help="Do not follow symbolic links in the project", nargs='?', const=True, default=None)
	parser.add_argument("--encoding", help="Use encoding parameter for file open.", default=None)
	parser.add_argument("--savepath", help="Save the list of requirements in the given file.", default=None)
	parser.add_argument("--print", help="Output the list of requirements in the standard output.", default=None)
	parser.add_argument("--force", help="Overwrite existing requirements.txt", nargs='?', const=True, default=None)
	parser.add_argument("--diff", help="Compare modules in requirements.txt to project imports.")
	parser.add_argument("--clean", help="Clean up requirements.txt.")
	parser.add_argument("--version", help="Control package version from requirements file. \
		Either: `None`, `exact`, `greater`. Default `greater`.", nargs='?', const=True, default="greater")
	args = parser.parse_args()
	sys.exit(run(args))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Generate doctree for a package or directory.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""
# import
from pdb import set_trace as breakpoint
from pathlib import Path
import re, sys, argparse, textwrap

class DisplayablePath():
	"""[summary]

	Returns
	-------
	[type]
		[description]
	"""
	display_filename_prefix_middle = '├──'
	display_filename_prefix_last = '└──'
	display_parent_prefix_middle = '    '
	display_parent_prefix_last = '│   '

	def __init__(self, path, parent_path, is_last, param):
		"""[summary]

		Parameters
		----------
		path : [type]
			[description]
		parent_path : [type]
			[description]
		is_last : bool
			[description]
		param : dict
			[description]
		"""
		self.path = Path(str(path))
		self.parent = parent_path
		self.is_last = is_last
		if self.parent:
			print(path)
			self.depth = self.parent.depth + 1
		else:
			self.depth = 0

	@classmethod
	def exclude(cls, param):
		"""[summary]

		Parameters
		----------
		param : [type]
			[description]

		Returns
		-------
		[type]
			[description]
		"""
		# exclude_extension
		if param['exclude_extension'] is not None:
			# find file extensions
			if Path(child).suffix in exclude_extension:
				return None
		# exclude_files
		if param['exclude_files'] is not None:
			if str(child.name) in exclude_files:
				return None

		# exclude_folders
		if param['exclude_folders'] is not None:
			if str(child.name) in exclude_folders:
				return None

		# exclude_all_files
		if param['exclude_all_files'] is True:
			if not child.is_dir():
				return None

		return child

	@classmethod
	def make_tree(cls, root, parent=None, is_last=False, criteria=None, exclude_extension=None, exclude_files=None, exclude_folders=None, exclude_all_files=False):
		"""[summary]

		Parameters
		----------
		root : [type]
			[description]
		parent : [type], optional
			[description], by default None
		is_last : bool, optional
			[description], by default False
		criteria : [type], optional
			[description], by default None
		exclude_extension : [type], optional
			[description], by default None
		exclude_files : [type], optional
			[description], by default None
		exclude_folders : [type], optional
			[description], by default None
		exclude_all_files : [type], optional
			[description], by default False
		"""
		# path
		root = Path(str(root))

		# parameters
		param = dict(
			child = root, 
			exclude_extension = exclude_extension, 
			exclude_files = exclude_files, 
			exclude_folders = exclude_files, 
			exclude_all_files = exclude_files
		)
		criteria = criteria or cls._default_criteria

		displayable_root = cls(root, parent, is_last, param)
		yield displayable_root
		# get list of files
		children = sorted(list(path for path in root.iterdir() if criteria(path)), key=lambda s: str(s).lower())
		count = 1
		for path in children:
			param = dict(
				child = path, 
				exclude_extension = exclude_extension, 
				exclude_files = exclude_files, 
				exclude_folders = exclude_files, 
				exclude_all_files = exclude_files
			)
			path = cls.exclude(param)
			if path is None:
				continue
			is_last = count == len(children)
			if path.is_dir():
				yield from cls.make_tree(path, parent=displayable_root, is_last=is_last, criteria=criteria)
			else:
				yield cls(path, displayable_root, is_last)
			count += 1

	@classmethod
	def _default_criteria(cls, path):
		return True

	@property
	def displayname(self):
		if self.path.is_dir():
			#print(self.path.name)
			return self.path.name + '/'
		return self.path.name

	def displayable(self):
		if self.parent is None:
			return self.displayname

		_filename_prefix = (self.display_filename_prefix_last if self.is_last else self.display_filename_prefix_middle)
		parts = ['{!s} {!s}'.format(_filename_prefix, self.displayname)]

		parent = self.parent
		while parent and parent.parent is not None:
			parts.append(self.display_parent_prefix_middle if parent.is_last else self.display_parent_prefix_last)
			parent = parent.parent

		return ''.join(reversed(parts))

def run(args):
	"""[summary]

	Parameters
	----------
	args : [type]
		[description]
	"""
	# start
	try:
		# arguments
		_args = vars(args)
		directory_p = str(Path(_args['path'][0]))
		output_p = _args['output'] if _args['output'] else directory_p
		extensions = _args['extensions'][0].split(",") if _args['extensions'] else None
		files = _args['files'][0].split(",") if _args['files'] else None
		folders = _args['folders'][0].split(",") if _args['folders'] else None
		allf = True if (_args['all'] is True) else False

		# start
		doctree = DisplayablePath.make_tree(root=directory_p, exclude_extension=extensions, exclude_files=files, exclude_folders=folders, exclude_all_files=allf)
		## for each branch
		export = []
		for branch_ in doctree:
			branch = branch_.displayable()
			export.append(branch)
		## save
		output = '\n'.join(export)
		with open("%s/doctree.txt"%(output_p), "w") as file_:
			file_.write(output)

	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	# https://docs.python.org/3.7/library/argparse.html
	sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
	example = '''example: 
	
	macos: python doctree.py /Users/mdl-admin/Desktop/mdl/ --files=.DS_Store
	github: python doctree.py /Users/mdl-admin/Desktop/mdl/ --files=.git,.gitignore,.gitattributes,.nojekyll,.gitmodules
	'''
	parser = argparse.ArgumentParser(
		description = "Generate package doctrees.",
		epilog=example,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		prog = sys.argv[0]
	)
	# Arguments
	parser.add_argument("path", nargs='+', help="The path to the directory to generate doctree.")
	# options
	parser.add_argument("--output", help="Output path. Default will be same location as directory path.", default=None, type=str)
	parser.add_argument("--extensions", help="List of file extensions to exclude (i.e. .csv, .pyc).", default=None, type=str, nargs='+')
	parser.add_argument("--files", help="List of files to exclude (i.e. TODO.md, passkey.pem). Default None.", default=None, type=str, nargs='+')
	parser.add_argument("--folders", help="List of folders to exclude (i.e. src, dist, .git). Default None.", default=None, type=str, nargs='+')
	parser.add_argument("--all", help="(Bool) Exclude all files from doctree. Default False.", default=False, type=bool)
	args = parser.parse_args()
	sys.exit(run(args))

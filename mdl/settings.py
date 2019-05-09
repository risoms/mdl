#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Default settings for processing.py
| @date: Created on Sat May 1 15:12:38 2019
| @author: Semeon Risom
| @email: semeon.risom@gmail.com
| @url: https://semeon.io/d/mdl  
"""

from pdb import set_trace as breakpoint
from datetime import datetime
import os
import re
import sys

# available functions
__all__ = ['console','link','popover','stn','library','path']

# path
path = {
	'home': os.path.dirname(os.path.abspath(__file__))
}

def copyInherit(fromfunc, sep="\n"):
	"""Copy the docstring of inherited functions and classes.

	Parameters
	----------
	fromfunc : [type]
		[description]
	sep : str, optional
		[description], by default "\n"

	Returns
	-------
	[type]
		[description]
	"""
	#breakpoint()
	def _decorator(func):
		sourcedoc = fromfunc.__doc__
		if func.__doc__ == None:
			func.__doc__ = sourcedoc
		return func

	return _decorator

def time():
	"""
	Get local time in ISO-8601 format.

	Returns
	-------
	iso : :class:`str`
		ISO-8601 datetime format, with timezone.

	Example
	-------
	>>> __time__()
	'2019-04-23 11:29:44-05:00'
	"""

	iso = datetime.now().astimezone().replace(microsecond=0).isoformat()

	return iso

def console(message, color='blue'):
	"""
	Allows user-friend console logging using ANSI escape codes.

	Parameters
	----------
	message : :class:`str`
		Message to send to console.
	color : :class:`str`
		Name of color or ANSI escape event to use.

	Returns
	-------
	result : :class:`str`
		ANSI escape code.

	Examples
	--------
	>>> console(self, message, color='blue)

	Notes
	-----
	Colors are produced using ASCII Oct format. For example: '`\033[40m`. See http://jafrog.com/2013/11/23/colors-in-terminal.html
	for more.
	"""

	_c = dict(
		black='40m',
		red='41m',
		green='42m',
		orange='43m',
		purple='45m',
		blue='46m',
		grey='47m'
	)

	# result will be in this format: [<PREFIX>];[<COLOR>];[<TEXT DECORATION>][<MESSAGE>][<FINISHING SYMBOL>]
	result = '\033[' + _c[color] + message + '\033[0m'

	return print(result)

def link(name, url):
	"""
	Create popover of variable in html.

	Parameters
	----------
	name : :class:`str`
		Name of variable.
	url : :class:`str`
		URL to link to.

	Returns
	-------
	link : :class:`str`
		HTML <a> element.

	Examples
	--------
	>>> link(name=roi, url="#boxplot")

	.. code-block:: html

		<a href="#boxplot" class="anchor">roi</a>
	"""

	_link = '<a href="%s" class="anchor">%s</a>' % (url, name)

	return _link

def popover(name, title, description, url=None, **kwargs):
	"""
	Create popover of variable in html.

	Parameters
	----------
	name : :class:`str`
		Local name of variable.
	title : :class:`str`
		Title of variable in popover.
	description : :class:`str`
		Description of variable in popover.
	url : :class:`str` or :obj:`str`
		URL to include. Default `None`.
	**kwargs : :obj:`str` or :obj:`None`, optional
		Additional properties, relevent for specific content types. Here's a list of available properties:

		.. list-table::
			:class: kwargs
			:widths: 25 50
			:header-rows: 1
			
			* - Property
			  - Description
			* - img : :obj:`dict` {'src': :obj:`str`,'className': :obj:`str`}
			  - Create an image to be included in the popover

	Returns
	-------
	link : :class:`str`
		HTML <a> element.

	Examples
	--------
	>>> description = "Chambers, J., Hastie, T. (1992). Statistical Models in S. Wadsworth & Brooks/Cole."
	>>> popover(name="anova", title="Statistical Models in S", description=description)

	.. code-block:: html 
		
		<a tabindex="0" class="popover-anchor" link-id="anova" data-toggle="popover" data-content="Chambers, J., Hastie, T. (1992). \
		Statistical Models in S. Wadsworth & Brooks/Cole." title="" data-original-title="Statistical Models in S">Chambers, Hastie, 1992</a>
	"""
	# img
	img = kwargs['img'] if 'img' in kwargs else None

	# if image
	if img is not None:
		_img = '<img class="%s" src="%s"></img>'%(img['class'], img['src'])
	else:
		_img = ''

	# if not url
	if url is not None:
		url = '<a class="anchor" href="%s">%s</a>' %(url, url)
		description = '%s<br>%s' % (description, url)
	else:
		description = ''

	# create link
	_link = '<a tabindex="0" class="popover-anchor" link-id="%s" data-toggle="popover" data-content="%s" title="" data-original-title="%s">%s</a>%s'\
		%(name, description, title, title, _img)
		
	# format
	_link = re.sub(r'\s+', ' ', link).strip()

	return _link

def stn(source):
	"""
	Convert to scientific notation.

	Parameters
	----------
	source : :class:`float`
		Original number.

	Returns
	-------
	output : :class:`str`
		Number in scientific notation, if (number < 0.0001) or (if number > 9999).
	"""
	# convert to float
	source = float(source)

	# if less than 0.0001, use scientific notation
	if (source < 0.0001):
		output = '%.2E' % source
	# else if greater than 9999, use scientific notation
	elif (source > 9999):
		output = '%.2E' % source
	# else round number to 4th digit
	else:
		output = '%s' % (round(source, 4))

	return output

def library(required=None):
	"""
	Check if required libraries are available.

	Parameters
	----------
	required : :class:`list`
		List of required libraries.
	"""

	import platform
	import importlib
	import pkg_resources
	import pip
	from distutils.version import StrictVersion
	from pip._internal import main as _main
	
	# start
	console('settings.library()', 'green')

	# for timestamp
	_t0 = datetime.now()
	_f = debug(message='t', source="timestamp")

	# if required is string
	if isinstance(required, str):
		required = [required]

	# packages to download from outside of pypi
	not_pypi = {
		'nslr': "https://gitlab.com/risoms/nslr"
	}

	# try installing and/or importing packages
	try:
		import subprocess, sys
		pipv = pkg_resources.get_distribution("pip").version
		if StrictVersion(pipv) > StrictVersion('10.0.0'):
			# for required packages check if package exists on device
			for package in required:
					# if missing, install
					if importlib.util.find_spec(package) is None:
						# if package is not in PyPi
						if package in not_pypi:
							_package = 'git+%s'%(not_pypi[package])
							#_main(['install', _path])
							subprocess.check_call([sys.executable, '-m', 'pip', 'install', _package])
						# if package is cv2
						elif package == 'cv2':
							#_main(['install', 'opencv-python'])
							subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-python'])
						# install from PyPi
						else:
							#_main(['install', package])
							subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
	except Exception as error:
		return error

	# ----finished
	console('%s finished in %s msec' % (_f, ((datetime.now()-_t0).total_seconds()*1000)), 'blue')

def debug(message, source='debug'):
	"""
	Get function or class for console print.

	Parameters
	----------
	message : :class:`str`
		Log message.
	source : :class:`str`
		Origin of call. Either debug or timestamp.

	"""
	import inspect

	#start
	if source == 'debug':
		caller = inspect.getframeinfo(inspect.stack()[1][0])
		event = "%s, line %d, in processing.%s(), %s" % (caller.filename, caller.lineno, caller.function, message)
		print(event)
	elif source == 'timestamp':
		caller = inspect.getframeinfo(inspect.stack()[1][0])
		event = "processing.%s()" % (caller.function)

	return event

def pydoc(path=None, source=None, build=None, copy=False):
	"""
	Generate pydoc docmentation.

	Parameters
	----------
	source : : class: `str`, optional
		pydoc source path, by default None
	build : : class: `str`, optional
	pydoc source path,, by default None
	copy : : class: `str` or bool, optional
		[description], by default False

	Attributes
	----------
	path: : class: `str`
		Location to save the pydoc to.
	"""

	import subprocess

	# for timestamp
	_t0 = datetime.now()
	_f = debug(message='t', source="timestamp")

	# create pydoc
	# if osx
	if sys.platform == "darwin":
		print(source); print(build)
		subprocess.call(['sphinx-build "%s" "%s"' % (source, build)],stdout=subprocess.PIPE, shell=True)
	# if windows
	else:
		# set location of makefile
		# sys.path.append('/Users/mdl-admin/Desktop/R33-analysis-master/output/docs/')

		_file = path + 'make.bat'
		p = subprocess.Popen([_file], cwd=path, shell=False)
		p.communicate()
		os.system("C:\\Windows\\System32\\cmd.exe /c %s" % (path))

	print('created pydoc at ' + build)
	print(console('%s finished in %s msec' %(_f, ((datetime.now()-_t0).total_seconds()*1000))))

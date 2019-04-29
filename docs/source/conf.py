# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
# This file does only contain a selection of the most common options. For a full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import re
import os
import sys
import time
import datetime

# Sphinx toctree include functions -------------------------------------------------------------------------------------
from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary import get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr

class AutoAutoSummary(Autosummary):
	option_spec = {
		'methods': directives.unchanged,
    	'attributes': directives.unchanged
	}
	required_arguments = 1
	@staticmethod
	def get_members(obj, typ, include_public=None):
		if not include_public:
			include_public = []
		items = []
		for name in dir(obj):
			try:
				documenter = get_documenter(safe_getattr(obj, name), obj)
			except AttributeError:
				continue
			if documenter.objtype == typ:
				items.append(name)
		public = [x for x in items if x in include_public or not x.startswith('_')]
		return public, items

	def run(self):
		class_ = str(self.arguments[0])
		try:
			(module_name, class_name) = class_.rsplit('.', 1)
			m = __import__(module_name, globals(), locals(), [class_name])
			c = getattr(m, class_name)
			if 'methods' in self.options:
				_, methods = self.get_members(c, 'method', ['__init__'])
				self.content = ["~%s.%s" % (class_, method) for method in methods if not method.startswith('_')]
			if 'attributes' in self.options:
				_, attribs = self.get_members(c, 'attribute')
				self.content = ["~%s.%s" % (class_, attrib) for attrib in attribs if not attrib.startswith('_')]
		finally:
			return super(AutoAutoSummary, self).run()

# Exclude modules ------------------------------------------------------------------------------------------------------
# http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-process-docstring
def remove_module_docstring(app, what, name, obj, options, lines):
	#if what == "module" and name == "hpclogging.logger" and 'members' in options:
	if what == "module" and name == "yourmodule":
		del lines[:]

# date -----------------------------------------------------------------------------------------------------------------
def iso():
	"""
	Get local time in ISO-8601 format.

	Returns
	-------
	iso : :class:`str`
		ISO-8601 datetime format, with timezone.

	Examples
	--------
	>>> __time__()
	'2019-04-23 11:29:44-05:00'
	"""

	isoname = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

	return isoname

# apidoc ---------------------------------------------------------------------------------------------------------------
def run_apidoc(app):
    """Generate API documentation"""
    import better_apidoc
    better_apidoc.APP = app
    better_apidoc.main([
        'better-apidoc',
        '--templates', os.path.abspath(os.path.join('.', 'source/_templates/')), #Custom template directory
        '--force', #Overwrite existing files'
        '--separate', #Put documentation for each module on its own page
        '--output-dir',
        os.path.abspath(os.path.join('.', 'source/api/')), # output path
        os.path.abspath(path) #module path
    ])

# allows inclusion or exclusion of __init__ ----------------------------------------------------------------------------
#http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-skip-member
autoclass_content = 'init'
def skip(app, what, name, obj, skip, options):
	if name == "__init__":
		return False
	return skip

# Path setup -----------------------------------------------------------------------------------------------------------
path = os.path.abspath(os.getcwd()+ '../../../') 
print('path %s'%(path))
# module directory
sys.path.append(path)
sys.path.append('/anaconda3/lib/python3.6/site-packages/')

# Path setup -----------------------------------------------------------------------------------------------------------
autodoc_mock_imports = ["numpy", "pandas", "scipy", "PIL", 'pylink', 'pylink.EyeLinkCustomDisplay']

# Project information --------------------------------------------------------------------------------------------------
import mdl

project = 'mdl-R33'
author = 'Semeon Risom'
copyright = u'{}, Semeon Risom'.format(time.strftime("%Y"))

#datetime = datetime.datetime.now().replace(microsecond=0).replace(second=0).isoformat()
date = datetime.date.today().isoformat()
# The short X.Y version
version = '%s'%(date)
# The full version, including alpha/beta/rc tags
release = version
# 'Last updated on:' timestamp is inserted at every page bottom, using the given strftime format.
isodate = iso()
html_last_updated_fmt = '%s'%(isodate)

# Extensions -----------------------------------------------------------------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	#include documentation from docstrings
    'sphinx.ext.autodoc',
	#link to other projects’ documentation
    'sphinx.ext.intersphinx',
	# add links to highlighted source code
    'sphinx.ext.viewcode',
    # create tables of summary data
	'sphinx.ext.autosummary',
	#compatiable with numpydoc notation
    'numpydoc',
	#'sphinx.ext.napoleon',
	#work with github
    'sphinx.ext.githubpages',
	# use jupyter
    'nbsphinx',
	# add copy
	'sphinx_copybutton',
	# inheritance plot
    'sphinx.ext.inheritance_diagram',
	'sphinxcontrib.fulltoc'
]
# extensopm parameters
# autosummary
autosummary_generate = True
autodoc_default_options = {
    'member-order': 'bysource',
    # 'private-members': False,
    # 'undoc-members': False,
}

# Napoleon settings ----------------------------------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True #True to list __init___ docstrings separately from the class docstring.
napoleon_include_private_with_doc = True #True to include private members (like _membername)
napoleon_include_special_with_doc = True #True to include special members (like __membername__)
napoleon_use_admonition_for_examples = True #True to use the .. admonition:: directive for Example sections.
napoleon_use_admonition_for_notes = True #True to use the .. admonition:: directive for Notes sections.
napoleon_use_admonition_for_references = True #True to use the .. admonition:: directive for References sections.
napoleon_use_ivar = True #True to use the :ivar: role for instance variables.
napoleon_use_param = True #True to use a :param: role for each function parameter.
napoleon_use_rtype = True #True to use the :rtype: role for the return type. 

# General configuration ------------------------------------------------------------------------------------------------
# Sphinx will warn about all references where the target cannot be found.
nitpicky = True
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md', '.ipynb']
# The master toctree document.
master_doc = 'index'
# The language for content autogenerated by Sphinx.
language = None
# Options for todo extension
todo_include_todos = True
# List of patterns, relative to source directory, that match files and directories to ignore when looking for source files.
exclude_patterns = ['_build', '**.ipynb_checkpoints', 'run.rst', 'notes.rst', 'api/setup.rst', 'setup', 'api/pylink.rst']
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
# Sort by source
autodoc_member_order = 'bysource'
html_copy_source = True #If true, the reST sources are included in the HTML build as _sources/name. The default is True.
html_show_sourcelink = True #If true (and html_copy_source is true as well), links to the reST sources will be added to the sidebar.

# Options for HTML output ----------------------------------------------------------------------------------------------
# Path to favicon
html_favicon = '_static/img/imhr.ico'
# The theme to use for HTML and HTML Help pages.
html_theme_path = ['_templates/sphinx_bootstrap_theme/']
html_theme = 'bootstrap'
html_static_path = ['_static']
# for more: https://github.com/ryan-roemer/sphinx-bootstrap-theme
html_theme_options = {
    'source_link_position': "footer",  # Location of source link
	'globaltoc_includehidden': False, # Include hidden TOCs in Site navbar
    'bootswatch_theme': "paper", # Bootswatch (http://bootswatch.com/) theme.
    'navbar_sidebarrel': False, # Render the next and previous page links in navbar.
	'navbar_pagenav': True, # Render the current pages TOC in the navbar
    'bootstrap_version': "3",
    'navbar_links': [
         ("Glossary", "genindex"),
         ("Install", "install"),
    ],
}
#no 'searchresults.html'
# #localtoc #fulltoc #globaltoc
html_sidebars = {'**': ['localtoc.html']}

# nbsphinx -------------------------------------------------------------------------------------------------------------
nbsphinx_allow_errors = False
nbsphinx_execute = 'never'
pngmath_use_preview = True
pngmath_dvipng_args = ['-gamma 1.5', '-D 96', '-bg Transparent']

# Options for HTMLHelp output ------------------------------------------------------------------------------------------
# Output file base name for HTML help builder.
htmlhelp_basename = 'mdl-R33'

# Options for manual page output ---------------------------------------------------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, 'mdl-R33', 'mdl-R33', [author], 1)]
# Options for Texinfo output -------------------------------------------------------------------------------------------
texinfo_documents = [ (master_doc, 'mdl-R33', 'mdl-R33', author, 'mdl-R33', 'One line description of project.', 'Miscellaneous'),]

# Options for Epub output ----------------------------------------------------------------------------------------------
epub_title = project
# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# Extension configuration ----------------------------------------------------------------------------------------------
# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
	'python': ('https://docs.python.org/3/', None),
	'numpy': ('https://docs.scipy.org/doc/numpy/', None),
	'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
	'cv2' : ('https://docs.opencv.org/2.4/', None),
	'h5py' : ('http://docs.h5py.org/en/latest/', None),
	'pandas' : ('http://pandas.pydata.org/pandas-docs/stable/', None),
	'matplotlib': ('https://matplotlib.org/', None),
	'psd_tools': ('https://psd-tools.readthedocs.io/en/latest/', None),
}

# -- Path setup --------------------------------------------------------------
def setup(app):
	# copybutton
	app.add_javascript("semeon/js/clipboard.js")
	app.add_stylesheet('semeon/css/user.css')
	app.add_javascript("semeon/js/user.js")
	app.add_javascript("semeon/js/copybutton.js")
	# exclude modules
	# app.connect("autodoc-process-docstring", remove_module_docstring)
	# better apidoc
	app.connect('builder-inited', run_apidoc)
	# auto add function in toctree
	app.add_directive('autoautosummary', AutoAutoSummary)
	# include init
	app.connect("autodoc-skip-member", skip)

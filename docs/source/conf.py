# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
# This file does only contain a selection of the most common options. For a full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

'''
references:
	* reSt
		* https://sublime-and-sphinx-guide.readthedocs.io/en/latest/
		* http://www.sphinx-doc.org/en/master/contents.html
		* http://docutils.sourceforge.net/docs/ref/rst/directives.html
	* numpydoc
		* https://numpydoc.readthedocs.io/en/latest/validation.html
		* https://www.numpy.org/devdocs/docs/howto_document.html
	* matplotlib
		* https://matplotlib.org/devel/documenting_mpl.html
		* https://matplotlib.org/devel/plot_directive.html
	* ipython
		* https://ipython.readthedocs.io/en/stable/sphinxext.html
	* useful guides/resources
		* how to document: https://ofosos.org/
note:
	* it's possible to convert python to rst by using: https://numpydoc.readthedocs.io/en/latest/validation.html
'''

# core
import re
import os
import sys
import time
import datetime
from pathlib import Path
from pdb import set_trace as breakpoint
a = __file__
# Path setup -----------------------------------------------------------------------------------------------------------
path = os.path.abspath(os.getcwd()+ '../../../') 
print('path %s'%(path))
# module directory
sys.path.append(path)
sys.path.append('/anaconda3/lib/python3.6/site-packages/')
import imhr
from imhr.settings import console
# ensure that your package is importable by any IPython kernels 
# see: https://jupyter-sphinx.readthedocs.io/en/latest/
package_path = os.path.abspath('../..')
os.environ['PYTHONPATH'] = ':'.join((package_path, os.environ.get('PYTHONPATH', '')))

# Add extensions manually-----------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath('./sphinxext/'))
sys.path.insert(0, os.path.abspath('./sphinxext'))
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

# Project information --------------------------------------------------------------------------------------------------
project = 'imhr'
author = 'Semeon Risom'
copyright = u'{}, '.format(time.strftime("%Y"))

#datetime = datetime.datetime.now().replace(microsecond=0).replace(second=0).isoformat()
date = datetime.date.today().isoformat()
# The short X.Y version
from imhr._version import get_versions
v = get_versions()['version'][:6]
release = v
# The full version, including alpha/beta/rc tags
version = '%s.%s'%(date, v)
# 'Last updated on:' timestamp is inserted at every page bottom, using the given strftime format.
isodate = iso()
html_last_updated_fmt = '%s'%(isodate)

# Extensions -----------------------------------------------------------------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	#Support for todo items
	'sphinx.ext.todo',
	#link to other projects’ documentation
    'sphinx.ext.intersphinx',
	# add links to highlighted source code
    'sphinx.ext.viewcode',
    # create tables of summary data
	'sphinx.ext.autosummary',
	#compatiable with numpydoc notation
    'numpydoc',
	#work with github
    'sphinx.ext.githubpages',
	# use jupyter
    'nbsphinx',
	# add copy
	'sphinx_copybutton',
	# inheritance plot
    'sphinx.ext.inheritance_diagram',
	# Include a full table of contents in your Sphinx HTML sidebar
	'sphinxcontrib.fulltoc',
	# Include documentation from docstrings
	'sphinx.ext.autodoc',
	# Extending autodoc API
	'autodocsumm',
	# E include jinja based templates based documentation into a sphinx doc
	'sphinxcontrib.jinja',
	# A directive for including a matplotlib plot in a Sphinx document.
    'matplotlib.sphinxext.plot_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
]

# sphinx-jinja: Adding requirements ---------------------------------------------------------------------------------------
## This allows variables to be accessable by jinja
## https://github.com/tardyp/sphinx-jinja
filename_ = '%s/requirements.txt'%(Path(imhr.__file__).parent.parent)
with open(filename_, 'rb') as f:
    required = [re.sub('\n', '', line.decode('utf-8')) for line in f]
jinja_contexts = {
    'required': {'packages': required}
}
# sphinx-jinja: Adding methods ---------------------------------------------------------------------------------------
methods = dir(imhr)
jinja_contexts['methods'] = {'methods': methods}

## This allows all method to be included in api/imhr.rst
# matplotlib plot_directive settings -----------------------------------------------------------------------------------
plot_html_show_source_link = False
plot_rcparams = {'savefig.bbox':'tight', "savefig.dpi": 400, 'figure.figsize': (20,6), 'figure.facecolor': '#ffffff'}
plot_apply_rcparams = True  # if context option is used
plot_formats = [('png',400)]
plot_template = """
{{ source_code }}

{{ only_html }}
   {% for img in images %}
   .. figure:: {{ build_dir }}/{{ img.basename }}.{{ default_fmt }}
      :target: {{ dest_dir }}/{{ img.basename }}.{{ default_fmt }}
      {% for option in options -%}
      {{ option }}
      {% endfor %}

      {% if html_show_formats and multi_image -%}
        (
        {%- for fmt in img.formats -%}
        {%- if not loop.first -%}, {% endif -%}
        `{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
        {%- endfor -%}
        )
      {%- endif -%}
      {{ caption }}
   {% endfor %}

{{ only_latex }}

   {% for img in images %}
   {% if 'pdf' in img.formats -%}
   .. figure:: {{ build_dir }}/{{ img.basename }}.pdf
      :target: {{ dest_dir }}/{{ img.basename }}.pdf
      {% for option in options -%}
      {{ option }}
      {% endfor %}
      {{ caption }}
   {% endif -%}
   {% endfor %}

{{ only_texinfo }}

   {% for img in images %}
   {% if 'png' in img.formats -%}
   .. image:: {{ build_dir }}/{{ img.basename }}.png
      :target: {{ dest_dir }}/{{ img.basename }}.png
      {% for option in options -%}
      {{ option }}
      {% endfor %}
   {% endif -%}
   {% endfor %}
"""

# Napoleon settings ----------------------------------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

# viewcode settings ----------------------------------------------------------------------------------------------------
viewcode_follow_imported_members = True

# find source 
# https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html#event-viewcode-find-source
def viewcode_find_source(app, modname):
	pass

def viewcode_follow_imported(app, modname, attribute):
	pass

# nbsphinx settings ----------------------------------------------------------------------------------------------------
nbsphinx_allow_errors = False
nbsphinx_execute = 'never'
pngmath_use_preview = True
pngmath_dvipng_args = ['-gamma 1.5', '-D 96', '-bg Transparent']

# Autosummary settings -------------------------------------------------------------------------------------------------
from sphinx.ext.autosummary import Autosummary
class AutoAutoSummary(Autosummary):
	from sphinx.ext.autosummary import get_documenter
	from docutils.parsers.rst import directives
	from sphinx.util.inspect import safe_getattr
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

# better-apidoc settings -----------------------------------------------------------------------------------------------
# better-apidoc - generate rst files
path_ = os.path.dirname(__file__)
temp_ = path_ + '/_templates/'
api_ = path_ + '/api/'
print(path_)
print(temp_)
print(api_)
def builder_inited(app):
    """Generate API documentation"""
    import better_apidoc
    better_apidoc.APP = app
    better_apidoc.main([
        'better-apidoc',
        '--templates', temp_, #Custom template directory
        '--force', #Overwrite existing files'
        '--separate', #Put documentation for each module on its own page
		'--private', #nclude "_private" modules
        '--output-dir', api_, #Directory to place all output
        os.path.abspath(path) #module path
    ])

# sphinx-autogen settings ----------------------------------------------------------------------------------------------
autosummary_generate = False

# autodoc settings -----------------------------------------------------------------------------------------------------
## http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_mock_imports = ["numpy","pandas","scipy","PIL",'pylink','pylink.EyeLinkCustomDisplay','setup.py','versioneer.py','_version.py']
# autoclass_content = 'init'
#suppress_warnings = ['misc.highlighting_failure']
autodoc_default_options = {
    # 'autosummary': True,
	# 'special-members': '__init__'
    # 'undoc-members': False,
    # 'private-members': True,
	'member-order': 'bysource',
	'inherited-members': True,
    'show-inheritance': True,
}

## Exclude summary tables (summary tables instead are created in autodocsumm)
### http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-process-docstring
def autodoc_process_docstring(app, what, name, obj, options, lines):
	#if ((what == "module") or (what == "class") or (what == "function") or (what == "method") or (what == "attribute")):
	#print('\n'); console(what, 'red'); console(name, 'green'); print(lines)
	#if (what == "attribute"):
	#	del lines[:]
	pass

## allows inclusion or exclusion of __init__
### http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-skip-member
def autodoc_skip_member(app, what, name, obj, skip, options):
	exclusions = (
		# '__weakref__',  # special-members
		'__init__',
		'__doc__', 
		'__module__', 
		'__dict__',  # undoc-members
	)
	exclude = name in exclusions

	# if name == "__init__":
	# 	return False	
	# else:
	# 	return skip or exclude
	return skip or exclude

# autodocsumm settings -------------------------------------------------------------------------------------------------
def grouper_autodocsumm(app, what, name, obj, section, options, parent):
    if parent is imhr.eyetracking and section == 'Attributes':
        return 'Alternative Section'

# General settings -----------------------------------------------------------------------------------------------------
#If true, “Created using Sphinx” is shown in the HTML footer.
html_show_sphinx = False
# If true, “(C) Copyright …” is shown in the HTML footer. Default is True.
html_show_copyright = True
# Sphinx will warn about all references where the target cannot be found.
nitpicky = False
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md', '.ipynb', '.html']
# The master toctree document.
master_doc = 'index'
# The language for content autogenerated by Sphinx.
language = None
# Options for todo extension
todo_include_todos = True
# List of patterns, relative to source directory, that match files and directories to ignore when looking for source files.
exclude_patterns = [
	'_build',
	'**.ipynb_checkpoints',
	'run.rst','notes.rst',
	'imhr._version.rst',
	'api/imhr._version.rst',
	'api/setup.rst',
	'api/versioneer.rst',
	'api/imhr.eyetracking.pylink.rst'
]
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
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
# templates for additional pages
## let Sphinx know that we still want to generate the following pages in html_additional_pages
## http://www.sphinx-doc.org/en/master/usage/configuration.html?highlight=html_additional_pages#confval-html_additional_pages
## https://ofosos.org/2018/12/28/landing-page-template/
# html_additional_pages = {
# 	'install': 'install.rst'
# }
#no 'searchresults.html'
# #localtoc #fulltoc #globaltoc
html_sidebars = {'**': ['localtoc.html','sourcelink.html']}

# Options for HTMLHelp output ------------------------------------------------------------------------------------------
# Output file base name for HTML help builder.
htmlhelp_basename = 'imhr'

# Options for manual page output ---------------------------------------------------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, 'imhr', 'imhr', [author], 1)]
# Options for Texinfo output -------------------------------------------------------------------------------------------
texinfo_documents = [ (master_doc, 'imhr', 'imhr', author, 'imhr', 'One line description of project.', 'Miscellaneous'),]

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
	'psd_tools': ('https://psd-tools.readthedocs.io/en/stable/', None),
	'PIL': ('https://pillow.readthedocs.io/en/stable/', None),
}

# setup ----------------------------------------------------------------------------------------------------------------
def setup(app):
	"""[summary]

	Parameters
	----------
	app : [type]
		[description]
	"""
	# copybutton
	app.add_javascript("semeon/js/clipboard.js")
	app.add_stylesheet('semeon/css/user.css')
	app.add_javascript("semeon/js/user.js")
	app.add_javascript("semeon/js/copybutton.js")
	app.connect("autodoc-process-docstring", autodoc_process_docstring) # exclude modules
	app.connect("autodoc-skip-member", autodoc_skip_member) # include init
	# app.connect('builder-inited', builder_inited) # better apidoc: generate rst files
	# app.connect('viewcode-find-source', viewcode_find_source) # viewcode alter source
	# app.connect('viewcode-follow-imported', viewcode_follow_imported) # viewcode follow source
	# app.add_directive('autoautosummary', AutoAutoSummary) # auto add function in toctree
	# app.connect('autodocsumm-grouper', grouper_autodocsumm) # autodocsumm

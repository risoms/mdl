#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: mdl, an extensive library for the exploration, visualization, and analysis of eyetracking data. \
This library was created at the Institute for Mental Health Research, at the University of Texas at Austin by Semeon Risom.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""

# allowed imports
__all__ = ['Download','eyetracking','plot','r33','settings','tests', 'Webgazer']

# core
from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# set as namespace package
# see https://stackoverflow.com/questions/41621131/python-namespace-packages-in-python3
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)

except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)


# imports
## modules
from . import eyetracking
from . import r33
from . import Webgazer
## classes
from .download import Download
## function lists
from . import plot
from . import settings
from . import tests

# classes
class Download(Download):
	"""Download raw data from apache, Box, or REDCap servers."""
	__doc__ = Download.__init__.__doc__
	def __init__(self, isLibrary=False, **kwargs):
		super().__init__(isLibrary=False, **kwargs)

# version
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: mdl, an extensive library for the exploration, visualization, and analysis of eyetracking data. \
This library was created at the Institute for Mental Health Research, at the University of Texas at Austin by Semeon Risom.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""
# allowed imports
__all__ = ['download','eyetracking','plot','r33','settings']

# core
from pdb import set_trace as breakpoint
import os
import sys
import certifi

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# set as namespace package
# see https://stackoverflow.com/questions/41621131/python-namespace-packages-in-python3
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
    del pkg_resources
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
    del pkgutil

# imports
from . import download
from . import eyetracking
from . import plot
from . import r33
from . import settings

# del os, sys

# version
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with the R33 study.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""
# allowed imports
__all__ = ['Classify','Metadata','Model','nslr_hmm','Processing','Settings']

# core
from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
from . import _nslr_hmm
from ..settings import copyInherit
from ._classify import Classify as _Classify
from ._metadata import Metadata as _Metadata
from ._model import Model as _Model
from ._processing import Processing as _Processing
from ._settings import Settings as _Settings

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

# classes
@copyInherit(_Classify)
class Classify(_Classify):
	"""Classification of eyetracking data for mdl.r33.procesing."""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

@copyInherit(_Metadata)
class Metadata(_Metadata):
	"""Process participants metadata for analysis and export."""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

@copyInherit(_Model)
class Model(_Model):
	"""Run statistical models for analysis."""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

@copyInherit(_Processing)
class Processing(_Processing):
	"""Hub for running processing and analyzing raw data."""
	def __init__(self, config, isLibrary=False):
		super().__init__(config, isLibrary=False)

@copyInherit(_Settings)
class Settings(_Settings):
	"""Default settings for mdl.r33.Processing"""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

# finished
# del os, sys, _Classify, _Metadata, _Model, _Processing, _Settings

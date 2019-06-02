#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with the R33 study.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
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
from . import _nslr_hmm as nslr_hmm
from ._classify import Classify as _Classify
from ._metadata import Metadata
from ._model import Model as _Model
from ._processing import Processing as _Processing
from ._settings import Settings as _Settings

# set as namespace package
# see https://stackoverflow.com/questions/41621131/python-namespace-packages-in-python3
import pkg_resources
pkg_resources.declare_namespace(__name__)
del pkg_resources

# classes
class Classify(_Classify):
	"""Classification of eyetracking data for imhr.r33.procesing."""
	__doc__ = _Classify.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Metadata(Metadata):
	"""Process participants metadata for analysis and export."""
	__doc__ = Metadata.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Model(_Model):
	"""Run statistical models for analysis."""
	__doc__ = _Model.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Processing(_Processing):
	"""Hub for running processing and analyzing raw data."""
	__doc__ = _Processing.__init__.__doc__
	def __init__(self):
		super().__init__()

class Settings(_Settings):
	"""Default settings for imhr.r33.Processing"""
	__doc__ = _Settings.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

# finished
# del os, sys, _Classify, _Metadata, _Model, _Processing, _Settings

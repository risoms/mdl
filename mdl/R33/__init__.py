#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with the R33 study.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""

from pdb import set_trace as breakpoint
import pkg_resources
import os
import sys

# imports
#from classify import Classify
#from processing import Processing
#from . import metadata
#from . import model
#import nslr_hmm
#from .config import Settings

# imports
from .classify import Classify as _Classify
from .metadata import Metadata as _Metadata
from .model import Model as _Model
from .processing import Processing as _Processing
from .settings import Settings as _Settings

# allowed imports
__all__ = ['Classify','Metadata','Model','nslr_hmm','Processing','Settings']

# set as module
pkg_resources.declare_namespace(__name__)

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# classes
class Classify(_Classify):
	"""Analysis methods for mdl.processing.preprocesing."""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Metadata(_Metadata):
	"""Process participants metadata for analysis and export."""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Model(_Model):
	"""Run statistical models for analysis."""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Processing(_Processing):
	"""Hub for running processing and analyzing raw data."""
	def __init__(self, config, isLibrary=False):
		super().__init__(config, isLibrary=False)

class Settings(_Settings):
	"""Default settings for processing.py"""
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

# finished
del os, sys, breakpoint, pkg_resources, _Classify, _Metadata, _Model, _Processing, _Settings

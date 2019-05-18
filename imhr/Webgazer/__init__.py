#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with the Webgazer exploratory study.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""
# allowed imports
__all__ = ['Classify','Metadata','model','nslr_hmm','plot','Processing','raw','redcap','settings']

# core
from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
# classes
from .classify import Classify
from .metadata import Metadata
from .processing import Processing
from .raw import raw
from .redcap import redcap
from . import settings
## functions
from . import model
from . import nslr_hmm
from . import plot


# classes
class Classify(Classify):
	"""Classification of eyetracking data for imhr.r33.procesing."""
	__doc__ = Classify.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Metadata(Metadata):
	"""Process participants metadata for analysis and export."""
	__doc__ = Metadata.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed with accessing and visualizing data.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""
# allowed imports
__all__ = ['Download','Plot']

# core
from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
from ..settings import copyInherit
from .download import Download as _download
from .plot import Plot as _plot

# classes
class Download(_download):
	"""Download raw data from apache, Box, or REDCap servers."""
	__doc__ = _download.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

class Plot(_plot):
	"""Hub for creating data visualizations using pandas, seaborn, and bokeh."""
	__doc__ = _plot.__init__.__doc__
	def __init__(self, isLibrary=False):
		super().__init__(isLibrary=False)

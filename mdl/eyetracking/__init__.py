#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with eyetracking data.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""
# allowed imports
__all__ = ['Calibration','Eyelink','ROI','pylink']

# core
from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
import pylink
from ..settings import copyInherit
from ._roi import ROI as _ROI
from ._eyelink import Eyelink as _Eyelink
from ._calibration import Calibration as _Calibration

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
@copyInherit(_Eyelink)
class Eyelink(_Eyelink):
	"""Interface for the SR Research Eyelink eyetracking system."""
	def __init__(self, window, timer, isPsychopy=True, subject=None, **kwargs):
		super().__init__(window, timer, isPsychopy=True, subject=None, **kwargs)

@copyInherit(_Calibration)
class Calibration(_Calibration):
	"""Allow mdl.eyetracking.Eyelink to initiate calibration/validation/drift correction."""
	def __init__(self, w, h, tracker, window):
		super().__init__(w, h, tracker, window)

@copyInherit(_ROI)
class ROI(_ROI):
	"""Generate regions of interest that can be used for data processing and analysis."""
	def __init__(self, image_path=None, output_path=None, metadata_path=None, shape='box', **kwargs):
		super().__init__(image_path=image_path, output_path=output_path, metadata_path=metadata_path, shape=shape, **kwargs)

# finished 
#del copyInherit, os, sys, _ROI, _Eyelink, _Calibration

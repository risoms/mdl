#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with eyetracking data.  
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
from .roi import ROI as _ROI
from .eyelink import Eyelink as _Eyelink
from .calibration import Calibration as _Calibration

# set as module
pkg_resources.declare_namespace(__name__)

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# classes
class Eyelink(_Eyelink):
	"""
	Module allowing communcation to the SR Research Eyelink eyetracking system. Code is optimized for the Eyelink 1000 \
	Plus (5.0), but should be compatiable with earlier systems.
	"""
	def __init__(self, window, timer, isPsychopy=True, subject=None, **kwargs):
		super().__init__(window, timer, isPsychopy=True, subject=None, **kwargs)

class Calibration(_Calibration):
	"""
	Allowing mdl.eyetracking package to initiate calibration/validation/drift correction.
	"""
	def __init__(self, w, h, tracker, window):
		super().__init__(w, h, tracker, window)

class ROI(_ROI):
	"""
	Generate region of interest to be read by Eyelink DataViewer or statistical tool.
	"""
	def __init__(self, image_path=None, output_path=None, metadata_path=None, shape='box', **kwargs):
		super().__init__(image_path=image_path, output_path=output_path, metadata_path=metadata_path, shape=shape, **kwargs)

# finished
del os, sys, breakpoint, pkg_resources, _ROI, _Eyelink, _Calibration

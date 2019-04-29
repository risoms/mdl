#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace as breakpoint
import pkg_resources
import os
import sys

# imports
from ._version import get_versions
from .roi import ROI as _ROI
from .eyetracking import Eyetracking as _Eyetracking

# set as module
__all__ = ['Eyetracking','Calibration','ROI','__version__']
pkg_resources.declare_namespace(__name__)

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# class ROI(_ROI):
# 	# used to initialise newly created object, and receives arguments used to do that
# 	# roi = mdl.eyetracking.ROI() # here is actually called __init__
# 	def __init__(self, image_path=None, output_path=None, metadata_path=None, shape='box', **kwargs):
# 		super().__init__(image_path=image_path, output_path=output_path, metadata_path=metadata_path, shape=shape, **kwargs)

# class Eyetracking(_Eyetracking):
# 	# used to initialise newly created object, and receives arguments used to do that
# 	# roi = mdl.eyetracking.ROI() # here is actually called __init__
# 	def __init__(self, window, timer, isPsychopy=True, subject=None, **kwargs):
# 		super().__init__(window, timer, isPsychopy=True, subject=None, **kwargs)

# versioning
__version__ = get_versions()['version']

# finished
del os, sys, get_versions, breakpoint, pkg_resources

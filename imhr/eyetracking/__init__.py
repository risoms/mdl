#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Module designed for working with eyetracking data.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
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
from ._roi import ROI
from ._eyelink import Eyelink

# classes	
if __name__ == "__main__":
	from . import pylink
	from ._calibration import Calibration
	class Calibration(Calibration):
		"""Allow imhr.eyetracking.Eyelink to initiate calibration/validation/drift correction."""
		__doc__ = Calibration.__init__.__doc__
		def __init__(self, w, h, tracker, window):
			super().__init__(w, h, tracker, window)
		
class Eyelink(Eyelink):
	"""Interface for the SR Research Eyelink eyetracking system."""
	__doc__ = Eyelink.__init__.__doc__
	def __init__(self, window, timer, isPsychopy=True, subject=None, **kwargs):
		super().__init__(window, timer, isPsychopy, subject, **kwargs)

class ROI(ROI):
	"""Generate regions of interest that can be used for data processing and analysis."""
	__doc__ = ROI.__init__.__doc__
	def __init__(self, image_path=None, output_path=None, metadata_path=None, shape='box', **kwargs):
		super().__init__(image_path=image_path, output_path=output_path, metadata_path=metadata_path, shape=shape, **kwargs)

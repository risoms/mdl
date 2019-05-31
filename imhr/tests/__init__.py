#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Test examples from some of the code in the package.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""
# allowed imports
__all__ = ['test_simple','test_lazy_imports','test_generate_roi', 'test_run_eyetracking']

# core
from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
from .test_basic import test_simple
from .test_basic import test_lazy_imports
from .test_roi import test_generate_roi
from .test_eyetracking import test_run_eyetracking

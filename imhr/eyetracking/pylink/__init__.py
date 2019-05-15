#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Empty path for pylink.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""

# core
from pdb import set_trace as breakpoint
import os
import sys

__name__ = 'pylink'
id = 'pylink'

class EyeLinkCustomDisplay():
	pass

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
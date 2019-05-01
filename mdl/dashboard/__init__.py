#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Creates a dashboard using Jupyterhub to allow data analysis and visualization.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""

from pdb import set_trace as breakpoint
import os
import sys

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
import jupyterhub
import notebook

# notes
# https://jupyterhub.readthedocs.io/en/stable/quickstart.html#start-the-hub-server
# go to site using: https://localhost:8000/
# to start the server sudo jupyterhub
del os, sys, breakpoint

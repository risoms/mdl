#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace as breakpoint
import os
import sys

# set as module
__all__ = ['eyetracking','R33','Download','plot','settings']

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

#----imports
from .download import Download
from . import eyetracking
from . import R33
from . import plot
from . import settings

del os, sys, breakpoint

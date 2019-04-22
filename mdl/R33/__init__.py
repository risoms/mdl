#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace as breakpoint
import pkg_resources
import os
import sys

# set as module
__all__ = ['Classify','metadata','model','nslr_hmm','Processing','Settings','__version__']
pkg_resources.declare_namespace(__name__)

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# imports
from classify import Classify
from processing import Processing
from . import metadata
from . import model
import nslr_hmm
from .config import Settings

#----versioning
from ._version import get_versions
__version__ = get_versions()['version']

# finished
del os, sys, get_versions, breakpoint, pkg_resources
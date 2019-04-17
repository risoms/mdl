#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

# set as module
__all__ = ['classify','download','model','nslr_hmm','plot','processing','settings']

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

#----imports
from classify import classify
from download import download
from processing import processing
import metadata
import model
import nslr_hmm
import plot
from settings import settings

#----versioning
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

del os, sys
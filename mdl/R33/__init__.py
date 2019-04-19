#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

# set as module
__all__ = ['Classify','metadata','model','nslr_hmm','Processing','Settings']

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

#----imports
from classify import Classify
from processing import Processing
from . import metadata
from . import model
import nslr_hmm
from settings import Settings

#----versioning
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

del os, sys
# -*- coding: utf-8 -*-

__author__ = 'Vadim Kravcenko'
__email__ = 'vadim.kravcenko@gmail.com'
__version__ = '0.4.8'

# imports
import pkg_resources
import os
import sys

# allowed imports
__all__ = ['pipreqs']

# set as module
pkg_resources.declare_namespace(__name__)

# relative paths
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

del os, sys
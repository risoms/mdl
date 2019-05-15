#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Basic tests for the ability to run package.  
@`date`: Created on Sat May 1 15:12:38 2019  
@`author`: Semeon Risom  
@`email`: semeon.risom@gmail.com  
@`url`: https://semeon.io/d/imhr
"""
from pdb import set_trace as breakpoint
import imhr
import os
import subprocess
import sys
import textwrap

# allowed imports
__all__ = ['test_simple','test_lazy_imports']

def test_simple():
	"""Test simple math.

	Returns
	-------
	answer : :obj:`bool`
		Returns result of 1 + 1 == 2.
	"""
	answer = 1 + 1 == 2
	return answer

def test_lazy_imports():
	"""Testing imports using subprocess.

	Returns
	-------
	bool : :obj:`bool`
		Returns a bool indicating the function has completed.
	"""
	source = textwrap.dedent("\
	import sys\n\
	import imhr\n\
	import imhr.eyetracking\n\
	import imhr.lib\n\
	import imhr.plot\n\
	import imhr.r33\n\
	import imhr.settings\n\
	import imhr.tests")

	subprocess.check_call([sys.executable, '-c', source])
	return True

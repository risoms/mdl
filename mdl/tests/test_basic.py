#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Basic tests for the ability to run package.  
@`date`: Created on Sat May 1 15:12:38 2019  
@`author`: Semeon Risom  
@`email`: semeon.risom@gmail.com  
@`url`: https://semeon.io/d/mdl
"""
from pdb import set_trace as breakpoint
import mdl
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
	import mdl\n\
	import mdl.eyetracking\n\
	import mdl.lib\n\
	import mdl.plot\n\
	import mdl.r33\n\
	import mdl.settings\n\
	import mdl.tests")

	subprocess.check_call([sys.executable, '-c', source])
	return True

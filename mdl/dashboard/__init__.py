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
import subprocess

if __name__ == '__main__':
	# relative path
	sys.path.append(os.path.dirname(os.path.realpath(__file__)))
	# start jupyter
	config_path = os.path.dirname(os.path.realpath(__file__)) + "/jupyterhub_config.py"
	#subprocess.call(['jupyterhub "--url=%s"' %(url)],stdout=subprocess.PIPE, shell=True)
	subprocess.call(['jupyterhub --ip /127.0.0.1 --port 8081 -f %s'%(config_path)],stdout=subprocess.PIPE, shell=True)

# notes
# https://jupyterhub.readthedocs.io/en/stable/quickstart.html#start-the-hub-server
# to install
## 'python -m pip install jupyterhub'
## 'npm install -g configurable-http-proxy'
## 'python -m pip install notebook'
# go to site using: http://localhost:8000/
# to start the server 'sudo jupyterhub'
del os, sys, breakpoint

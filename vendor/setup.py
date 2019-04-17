#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:37:43 2019

@author: Semeon Risom
@email: semeon.risom@gmail.com.

Sample code to run SR Research Eyelink eyetracking system. Code is optimized for the Eyelink 1000 Plus (5.0),
but should be compatiable with earlier systems.
"""

DESCRIPTION = "mdl-eyelink: Bindings for Eyelink and Python."
LONG_DESCRIPTION = """
mdl-eyelink provides a high-level interface for eyetracking research in Python. This package was created 
at the [Institute for Mental Health Research](http://mdl.psy.utexas.edu/), at [the University of Texas 
at Austin](http://www.utexas.edu/) by [Semeon Risom](https://semeon.io).
"""
DISTNAME = 'mdl-eyelink'
MAINTAINER = 'Semeon Risom'
MAINTAINER_EMAIL = 'semeon.risom@gmail.com'
URL = 'https://semeon.io/d/mdl-eyelink'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/risoms/mdl-eyelink/'
VERSION = '2019.05.01'
INSTALL_REQUIRES=['numpy','scipy','pandas','matplotlib','psychopy']
CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: MIT License',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'Topic :: Multimedia :: Graphics',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows'
]

	
from setuptools import find_packages
from setuptools.config import read_configuration
				   
from distutils.core import setup

# Special handling for Anaconda / Miniconda
required = read_configuration('setup.cfg')['options']['install_requires']

# get description
with open("README.md", "r") as d:			   
	LONG_DESCRIPTION = d.read()

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
		long_description_content_type="text/markdown"											  				 
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=INSTALL_REQUIRES,
        classifiers=CLASSIFIERS,
		packages = ['mdl']
    )
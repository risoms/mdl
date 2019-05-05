#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@purpose: Sample code to run SR Research Eyelink eyetracking system. Code is optimized for the Eyelink 1000 Plus (5.0),
but should be compatiable with earlier systems.
@date: Created on Sat May 1 15:12:38 2019
@author: Semeon Risom
@email: semeon.risom@gmail.com
@url: https://semeon.io/d/mdl-R33
"""

if __name__ == "__main__":
	import os, datetime, sys, importlib, pkg_resources
	from setuptools import find_packages

	try:
		from setuptools import setup
		is_setuptools = True
	except ImportError:
		from distutils.core import setup

	# versioning
	import versioneer
	versioneer.VCS = "git"

	# required packages
	path = '%s/%s'%(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
	with open(path) as f:
		required = f.read().splitlines()

	setuptools_kwargs = {
		'install_requires':required,
		'zip_safe': False
	}

	# setup 
	name = 'imhr'
	author = 'Semeon Risom'
	author_email = 'semeon.risom@gmail.com'
	maintainer = 'Semeon Risom'
	maintainer_email = 'semeon.risom@gmail.com'
	version = versioneer.get_version()
	cmdclass=versioneer.get_cmdclass()
	url = 'http://mdl.psy.utexas.edu/a/mdl'
	description = 'mdl: Psychology Data Science Suite.'
	download_url = 'https://github.com/risoms/mdl/'
	long_description = open('README.md').read()
	long_description_content_type = 'text/markdown'
	license_ = open('LICENSE', 'r').read()
	classifiers = [
		'Intended Audience :: Science/Research',
		'Programming Language :: Python :: 3.4',
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
	project_urls = {
		'Documentation': 'http://mdl.psy.utexas.edu/a/mdl',
		'Funding': 'https://www.djangoproject.com/fundraising/',
		'Source': 'https://github.com/django/django',
		'Tracker': 'https://code.djangoproject.com/',
	},
	packages = find_packages()
	include_package_data = True
	namespace_packages=['mdl']

	# init
	setup(
		name=name,
		version=version,
		packages=packages,
		include_package_data=True,
		author=author,
		author_email=author_email,
		maintainer=maintainer,
		maintainer_email=maintainer_email,
		description=description,
		license=license_,
		cmdclass=cmdclass,
		url=url,	
		download_url=download_url,
		long_description = long_description,
		long_description_content_type = long_description_content_type,
		classifiers=classifiers,
		platforms='any',
		python_requires='>!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*!=3.5.*!=3.6.*!=3.7.*',
		namespace_packages=namespace_packages,
		**setuptools_kwargs
	)
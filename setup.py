#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Sample code to run SR Research Eyelink eyetracking system. Code is optimized for the Eyelink 1000 Plus (5.0),
but should be compatiable with earlier systems.
@`date`: Created on Sat May 1 15:12:38 2019
@`author`: Semeon Risom
@`email`: semeon.risom@gmail.com
@`url`: https://semeon.io/d/mdl-R33
"""
if __name__ == '__main__':
	import os
	from setuptools import find_packages, setup, __version__

	# versioning
	import versioneer
	versioneer.VCS = "git"

	# description
	description = 'mdl - psychology and data science suite.'
	long_description_content_type = 'text/markdown'
	with open('README.md') as f:
		long_description = f.read()

	# required packages
	path = '%s/%s'%(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
	with open(path) as f:
		required = f.read().splitlines()
	required = required + ["win32api; sys_platform == 'win32'"] + ["pyobjc; sys_platform == 'darwin'"]

	# sphinx pydoc - if this is the master version from github, add sphinx requirements
	# sphinx==1.85 - prevents parameters to be rendered as <dl> instead of <th>
	if os.path.isdir("./docs"):
		path = '%s/%s'%(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
		with open(path) as f:
			required_addt = f.read().splitlines()
		required = required + required_addt

	# add to setuptools
	setuptools_kwargs = {
		'zip_safe': False,
		'install_requires': required
	}

	# setup
	name = 'imhr'
	author = 'Semeon Risom'
	packages = find_packages()
	platforms = 'Darwin, Windows'
	python_requires = '~=3.6'
	author_email = 'semeon.risom@gmail.com'
	maintainer = 'Semeon Risom'
	maintainer_email = 'semeon.risom@gmail.com'
	version = versioneer.get_version()
	cmdclass = versioneer.get_cmdclass()
	url = 'http://mdl.psy.utexas.edu/a/mdl'
	download_url = 'https://github.com/risoms/mdl/'
	classifiers = [
		'Intended Audience :: Science/Research',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'License :: OSI Approved :: MIT License',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Visualization',
		'Topic :: Scientific/Engineering :: Human Machine Interfaces',
		'Topic :: Multimedia :: Graphics',
		'Operating System :: MacOS',
		'Operating System :: Microsoft :: Windows'
	]
	project_urls = {
		'Documentation': 'http://mdl.psy.utexas.edu/a/mdl',
		'Source': 'https://github.com/risoms/mdl/'
	},
	namespace_packages=['mdl']

	# init
	setup(
		name=name,
		version=version,
		packages=packages,
		platforms=platforms,
		python_requires=python_requires,
		include_package_data=True,
		author=author,
		author_email=author_email,
		maintainer=maintainer,
		maintainer_email=maintainer_email,
		description=description,
		license="MIT",
		cmdclass=cmdclass,
		url=url,
		download_url=download_url,
		long_description = long_description,
		long_description_content_type = 'text/markdown',
		classifiers=classifiers,
		namespace_packages=namespace_packages,
		**setuptools_kwargs
	)

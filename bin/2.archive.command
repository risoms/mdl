#!/bin/bash
# https://packaging.python.org/tutorials/packaging-projects/
# Generating distribution archives

# set path as current location
cd "$(dirname "$0")"
cd ../

# remove folder from previous archive
rm -rf build
rm -rf dist 
rm -rf imhr.egg-info
rm -rf mdl.egg-info

# create virtualenv
rm -rf env
python -m venv env

# activate virtualenv
source env/bin/activate

# create archive
python setup.py sdist bdist_wheel
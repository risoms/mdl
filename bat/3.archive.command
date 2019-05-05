#!/bin/bash
# https://packaging.python.org/tutorials/packaging-projects/
# Generating distribution archives

# set path as current location
cd "$(dirname "$0")"
cd ../

# create archive
## Make sure you have the latest versions of setuptools and wheel installed
pip install --user --upgrade setuptools wheel
## archive
python setup.py sdist bdist_wheel
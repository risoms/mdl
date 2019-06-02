#!/bin/bash
# https://packaging.python.org/tutorials/packaging-projects/
# Generating distribution archives

# set path as current location
cd "$(dirname "$0")"
cd ../../

# remove folder from previous archive
rm -rf build
rm -rf dist 
rm -rf imhr.egg-info

# create archive
python -m pip install --upgrade pip setuptools wheel tqdm twine #check updates
python setup.py sdist bdist_wheel
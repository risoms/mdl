#!/bin/bash
# https://packaging.python.org/tutorials/packaging-projects/
# upload to pypi

# set path as current location
cd "$(dirname "$0")"
cd ../../

# uploading
## make sure twine is available
pip install --user --upgrade twine
## check for issues
python -m twine check dist/*
## upload
python -m twine upload dist/* --verbose -u risoms -p samboi10
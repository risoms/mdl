#!/bin/bash
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# test if archive is successful

# set path as current location
cd "$(dirname "$0")"
cd ../

# upload to TestPyPI
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*  --verbose -u risoms -p samboi10

# create virtualenv
rm -rf env
python -m venv env

# activate virtualenv
source env/bin/activate

# download TestPyPI to virtualenv 
pip install https://test.pypi.org/simple/ imhr

# test if successful
python
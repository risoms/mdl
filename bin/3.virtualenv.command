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
#pip install -i -no-deps https://test.pypi.org/simple/ imhr
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps imhr

# download dependencies directly from pip
## this is to test for errors in downloading
pip install -r requirements.txt 

# test if successful
which python
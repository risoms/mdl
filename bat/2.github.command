#!/bin/bash 

# set path as current location
cd "$(dirname "$0")"
cd ../

# upload to github
git tag -a v$(python setup.py --version) -m 'description of version'
git push https://github.com/risoms/mdl-R33.git
git push --tags
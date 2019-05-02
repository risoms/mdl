#!/bin/bash

# set path as current location
cd "$(dirname "$0")"

# run python setup.py sdist
python setup.py sdist
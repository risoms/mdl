#!/bin/bash
# https://github.com/bndr/pipreqs
# upload to pypi

# set path as current location
cd "$(dirname "$0")"
cd ../

# upload
python -m twine upload dist/* --verbose

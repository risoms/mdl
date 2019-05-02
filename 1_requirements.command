#!/bin/bash
# https://github.com/bndr/pipreqs
# generate list of required packages

# set path as current location
cd "$(dirname "$0")"

# run pipreqs
pipreqs --encoding=iso-8859-1 --debug --force --savepath=requirements.txt mdl/

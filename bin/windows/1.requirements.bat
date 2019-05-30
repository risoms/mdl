#!/bin/bash
# https://github.com/bndr/pipreqs
# generate list of required packages

# set path as current location
cd "$(dirname "$0")"
cd ../

# run pipreqs
./imhr/lib/pipreqs/pipreqs.py imhr/ --encoding=iso-8859-1 --debug --force --version=greater --exclude=rpy2,pylink,mdl,imhr,win32api,wmi,pyglet,pyobjc,AppKit --include=certifi --savepath=requirements.txt

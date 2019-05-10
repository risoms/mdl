#!/bin/bash
# https://github.com/bndr/pipreqs
# generate list of required packages

# set path as current location
cd "$(dirname "$0")"
cd ../

# run pipreqs
./mdl/lib/pipreqs/pipreqs.py mdl/ --encoding=iso-8859-1 --debug --force --version=greater --exclude=pylink,mdl,imhr,win32api,wmi,pyglet,pyobjc,AppKit,yarg --savepath=requirements.txt


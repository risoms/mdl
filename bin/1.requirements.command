#!/bin/bash
# https://github.com/bndr/pipreqs
# generate list of required packages

# set path as current location
cd "$(dirname "$0")"
cd ../

# run pipreqs
#export PATH=
./mdl/lib/pipreqs/pipreqs.py mdl/ --encoding=iso-8859-1 --debug --force --noversion --include=Pillow --exclude=rpy2,pip,PIL,bokeh,AppKit,pylink,mdl,imhr --savepath=requirements.txt
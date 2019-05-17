#!/bin/bash
# build pydoc

# path
cd "$(dirname "$0")"

# build docs
# -w=write warnings (and errors) to given file
# -E=don't use a saved environment
# -N=build in parallel with N processes where possible
# -T=show full traceback on exception
# --color=do emit colored output (default: auto-detect)
sphinx-build source build -w=log.log -E -N -T --color

# upload to github
# cd "$(dirname "$0")"
# cd ../
# git add .
# git commit -a "Commit"
# git push -u origin master

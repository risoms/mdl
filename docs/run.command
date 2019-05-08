#!/bin/bash
# build pydoc

# path
cd "$(dirname "$0")"

# build docs
sphinx-build -E source build

# upload to github
# cd "$(dirname "$0")"
# cd ../
# git add .
# git commit -a "Commit"
# git push -u origin master

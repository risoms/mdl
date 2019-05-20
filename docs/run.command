#!/bin/bash
# build pydoc

# path
cd "$(dirname "$0")"

# build docs
# sphinx-build --help --version for help and versioning
# -w= write warnings (and errors) to given file
# -j= build in parallel with N processes where possible
# -E don't use a saved environment, but rebuild it completely.
# -T show full traceback on exception
# -vvv Increase verbosity (loglevel)
# -P (Useful for debugging only.) Run the Python debugger, pdb, if an unhandled exception occurs while building.
# --color do emit colored output (default: auto-detect)
sphinx-build source build -w=log.log -E -T -vvv -P --color

# upload to github
# cd "$(dirname "$0")"
# cd ../
# git add .
# git commit -a "Commit"
# git push -u origin master

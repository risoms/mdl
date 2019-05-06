#!/bin/bash
# build pydoc

# path
cd "$(dirname "$0")"

# build
sphinx-build -E source build

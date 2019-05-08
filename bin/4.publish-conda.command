#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# building and upload to anaconda from PiPi

# set path as current location
cd "$(dirname "$0")"
cd ../

# constants
pkg='mdl'
ARCH=(osx-64 win-64)

# login to anaconda cloud
#anaconda login

# building conda package
conda-build $pkg --output-folder=./conda-bld

# convert package to other platforms
platforms=( osx-64 linux-64 win-64 )
find ./conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    for platform in "${platforms[@]}"
    do
       conda convert -f --platform all $platform $file  -o ./conda-bld/
    done    
done

# upload packages to anaconda
find ./conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done
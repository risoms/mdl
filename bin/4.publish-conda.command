#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# building and upload to anaconda from PiPi

# set path as current location
cd "$(dirname "$0")"
cd ../

# constants
pkg='imhr'
ARCH=(osx-64 win-64)

# login to anaconda cloud
#anaconda login

# building conda package
#conda-build $pkg

# convert package to other platforms
cd ~
platforms=( osx-64 linux-64 win-64 )
find $HOME/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/conda-bld/
    done    
done

# upload packages to anaconda
find $HOME/conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done
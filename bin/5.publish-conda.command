#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# building and upload to anaconda from PiPi

# set path as current location
cd "$(dirname "$0")"
$(pwd) #current directory

# constants
pkg='imhr' #package name
A=(osx-64 win-64) #architecture

# login to anaconda cloud
#anaconda login

# get package from pypi
#conda skeleton pypi $P

# building conda packages
rm -rf conda #remove conda subfolder
conda build purge-all #clear builds in /anaconda3/conda-bld/
conda build meta.yaml --python=3.7 --output-folder=./conda/build/ --cache-dir=./conda/cache/ #build

# convert package to other platforms
find ./conda/build/osx-64/ -name *.tar.bz2 | while read file
do
    for platform in "${pkg[@]}"
    do
       conda convert $file --force --verbose --platform=$platform --output-dir=./conda/build/$platform/
    done    
done

# upload packages to anaconda
find ./conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done

echo "finished"
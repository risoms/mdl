#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# building and upload to anaconda from PiPi

# set path as current location
cd "$(dirname "$0")"

# constants
pkg='imhr'
ARCH=(osx-64 win-64)
VERSION=( 3.6 3.7 )
# login to anaconda cloud
#anaconda login

# get package from pypi
cd ~
conda skeleton pypi $pkg
cd $pkg
pwd
wget https://conda.io/docs/_downloads/build1.sh
wget https://conda.io/docs/_downloads/bld.bat
cd ~

# building conda packages
for i in "${VERSION[@]}"
do
	conda-build --python $i $pkg
done

# convert package to other platforms
cd ~
platforms=( osx-64 win-64 )
find $HOME/conda-bld/osx-64/ -name *.tar.bz2 | while read file
do
    echo $file
    for platform in "${platforms[@]}"
    do
       conda convert -f --platform $platform $file  -o $HOME/conda-bld/
    done    
done

# upload packages to anaconda
find $HOME/conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done

echo "finished"
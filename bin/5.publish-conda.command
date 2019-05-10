#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# building and upload to anaconda from PiPi

# set path as current location
cd "$(dirname "$0")"
cd ../

# constants
pkg='imhr' #package name
architecture=(osx-64 win-64) #architecture

# login to anaconda cloud
#anaconda login

# get package from pypi
#conda skeleton pypi $P

# building conda packages
rm -rf conda #remove conda subfolder
conda build purge-all #clear unused builds
conda clean --all #Remove unused packages and caches.
conda build meta.yaml --python=3.7 --output-folder=conda/ #build

# convert package to other platforms
find /anaconda3/pkgs/ -name imhr-*.tar.bz2 | while read file
do
	for arch in "${architecture[@]}"
	do
		conda convert --force --verbose --platform=$arch --output-dir=./conda/$arch $file
	done
done

# upload packages to anaconda
find ./conda/ -name *.tar.bz2 | while read file
do
    anaconda upload $file
done

# finished
echo "finished"

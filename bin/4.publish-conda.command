#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# upload to conda

# set path as current location
cd "$(dirname "$0")"
cd ../

# login to anaconda cloud
anaconda login

# change the package name to the existing PyPi package you would like to build
pkg='imhr'

# adjust the Python versions you would like to build
array=(3.6 3.7)
echo "Building conda package"
cd ~
conda skeleton pypi $pkg
cd $pkg
wget https://conda.io/docs/_downloads/build1.sh
wget https://conda.io/docs/_downloads/bld.bat

# building conda packages
cd ~
for i in "${array[@]}"
do
	conda-build --python $i $pkg
done

# convert package to other platforms
echo "convert package to other platforms"
cd ~
platforms=( osx-64 win-64 )
find $HOME/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/conda-bld/
    done    
done

# upload packages to conda
find $HOME/conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done
echo "Upload to conda finished"
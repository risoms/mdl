#!/bin/bash
# https://medium.com/@giswqs/building-a-conda-package-and-uploading-it-to-anaconda-cloud-
# building and upload to anaconda from PiPi

# set path as current location
cd "$(dirname "$0")"
cd ../

step = "1. create requirements"
do
	echo step
    anaconda upload $file
done

step = "2. archive for pypi"
do
	echo step
    anaconda upload $file
done

step = "3. test in virtual env"
do
	echo step
    anaconda upload $file
done

step = "4. publish in pypi"
do
	echo step
    anaconda upload $file
done

step = "5. publish in conda"
do
	echo step
    anaconda upload $file
done

# finished
echo "finished"
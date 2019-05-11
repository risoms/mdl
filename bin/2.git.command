#!/bin/bash
# https://packaging.python.org/tutorials/packaging-projects/
# increment git (this allows packaging to pypi with uploading to github)

# set path as current location
cd "$(dirname "$0")"
cd ../

#Get the highest tag number
VERSION=`git describe --abbrev=0 --tags`
VERSION=${VERSION:-'0.0.0'}

#Get number parts
MAJOR="${VERSION%%.*}"; VERSION="${VERSION#*.}"
MINOR="${VERSION%%.*}"; VERSION="${VERSION#*.}"
PATCH="${VERSION%%.*}"; VERSION="${VERSION#*.}"

#increase version by 0.1
PATCH=$((PATCH+1))

#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT`

#create new tag
NEW_TAG="$MAJOR.$MINOR.$PATCH"

#only tag if no tag already (would be better if the git describe command above could have a silent option)
if [ -z "$NEEDS_TAG" ]; then
    echo "Tagged with $NEW_TAG"
    git tag $NEW_TAG
else
    echo "$NEW_TAG already a tag on this commit"
fi
REM #!/bin/bash
REM # https://packaging.python.org/tutorials/packaging-projects/
REM # increment git (this allows packaging to pypi with uploading to github)

REM # set path as current location
cd ../../

REM # get the highest tag number
set VERSION="git describe --abbrev=0 --tags"
set VERSION="{VERSION:-'0.0.0'}"

REM # Get number parts
set MAJOR="${VERSION%%.*}" 
set VERSION="${VERSION#*.}"
set MINOR="${VERSION%%.*}"
set VERSION="${VERSION#*.}"
set PATCH="${VERSION%%.*}"
set VERSION="${VERSION#*.}"

REM # increase version by 0.1
set PATCH=$((PATCH+1))

REM # get current hash and see if it already has a tag
set GIT_COMMIT="git rev-parse HEAD"
set NEEDS_TAG="git describe --contains %PORT%"

REM # create new tag
set NEW_TAG="$MAJOR.$MINOR.$PATCH"

REM # only tag if no tag already (would be better if the git describe command above could have a silent option)
if [ -z "$NEEDS_TAG" ]; then
    echo "Tagged with $NEW_TAG"
    git tag $NEW_TAG
else
    echo "$NEW_TAG already a tag on this commit"
fi
REM # https://packaging.python.org/tutorials/packaging-projects/
REM # upload to pypi

REM # set path as current location
cd ../../

REM # uploading
REM ## make sure twine is available
pip install --user --upgrade twine
REM ## check for issues
python -m twine check dist/*
REM ## upload
python -m twine upload dist/* --verbose -u risoms -p samboi10
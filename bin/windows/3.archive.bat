REM # https://packaging.python.org/tutorials/packaging-projects/
REM # Generating distribution archives

REM # set path as current location
cd ../../

REM # remove folder from previous archive
rmdir /s "./build"
rmdir /s "./dist"
rmdir /s "./imhr.egg-info"

REM # create archive
REM ## check updates
python -m pip install --upgrade pip setuptools wheel tqdm twine
python setup.py sdist bdist_wheel
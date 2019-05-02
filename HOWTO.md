resources
---------

#### how to package
- https://packaging.python.org/tutorials/packaging-projects/
- https://docs.python.org/3/distutils/setupscript.html

#### test package
- https://test.pypi.org/project/mdl/

#### real package
- https://pypi.org/manage/projects/

#### how to create subpackages (mdl) that can install into main package (mdl)
- https://packaging.python.org/guides/packaging-namespace-packages/

steps to package
----------------

#### update version
- versioneer install

#### create archive
- python setup.py sdist

#### upload to test pypi
- python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

#### install test
- pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade --force-reinstall mdl

#### upload to real pypi
- python -m twine upload dist/*
resources
---------
#### publish
##### how to package
- https://packaging.python.org/tutorials/packaging-projects/
- https://docs.python.org/3/distutils/setupscript.html
- https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

#####  create test package
- https://test.pypi.org/project/mdl/

#####  create real package
- https://pypi.org/manage/projects/

#### how to create subpackages (mdl) that can install into main package (mdl)
- https://packaging.python.org/guides/packaging-namespace-packages/

steps
-----
- create/update requirements.txt
	pipreqs --encoding=iso-8859-1 --debug --force --savepath=requirements.txt mdl/
- upload to github
	git push https://github.com/risoms/mdl-R33.git
- update version
	versioneer install
- create package using setup.py
	python setup.py sdist
- pypi
	- upload package to test pypi
		python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	- install test package 
		pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade --force-reinstall mdl
	- upload package to real pypi
		python -m twine upload dist/*
	- install test package 
		pip install mdl
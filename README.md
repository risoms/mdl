
-------------------------------------------------------------------------------------------------
<div class="row">
	<a href="https://liberalarts.utexas.edu/imhr/">
		<img src="https://risoms.github.io/mdl/docs/source/_static/img/imhr-header.png" height="auto" width="100%" max-width="400px">
	</a>
<div>

-------------------------------------------------------------------------------------------------
[![doi](https://img.shields.io/badge/DOI-10.1016%2Fj.cct.2018.10.014-blue.svg?style=flat-square)](https://doi.org/10.1016/j.cct.2018.10.014)
[![license](https://img.shields.io/pypi/l/imhr.svg?style=flat-square)](https://github.com/risoms/mdl/blob/master/LICENSE)
[![python](https://img.shields.io/pypi/pyversions/imhr.svg?style=flat-square)](https://pypi.org/project/imhr/)
[![version-pypi](https://img.shields.io/pypi/v/imhr.svg?style=flat-square)](https://pypi.org/project/imhr/)
[![version-anaconda](https://anaconda.org/risoms/imhr/badges/version.svg)](https://anaconda.org/risoms/imhr)
[![platform](https://anaconda.org/risoms/imhr/badges/platforms.svg)](https://anaconda.org/risoms/imhr)
[![Build Status](https://travis-ci.com/risoms/mdl.svg?style=flat-square&token=h4xHN6seBuC4SG7zNtMW&branch=master)](https://travis-ci.com/risoms/mdl)

mdl: an extensive suite for the exploration, visualization, and analysis of psychological data.
-----------------------------------------------------------------------------------------------

This package was created at [the Institute for Mental Health Research](http://mdl.psy.utexas.edu/), at [the University of Texas at Austin](http://www.utexas.edu/) by [Semeon Risom](https://semeon.io), and was developed in part from funding of NIMH grant [5R33MH109600-03](https://projectreporter.nih.gov/project_info_details.cfm?aid=9659376).

	Hsu, K. J., Caffey, K., Pisner, D., Shumake, J., Risom, S., Ray, K. L., . . . Beevers, C. G. (2018). 
	    Attentional bias modification treatment for depression: Study protocol for a randomized controlled trial. 
	    Contemporary Clinical Trials, 75, 59-66. doi:https://doi.org/10.1016/j.cct.2018.10.014.

Documentation
-------------
Online documentation is available at [risoms.github.io/mdl](https://risoms.github.io/mdl/docs/build/index.html). Documentation include [examples](https://risoms.github.io/mdl/docs/build/examples/index.html), [API reference](https://risoms.github.io/mdl/docs/build/api/mdl.html), and other useful information.

Dependencies
------------
mdl requires the following dependencies:

-  [Python 3.6+](https://www.python.org/downloads/)
-  [numpy](http://www.numpy.org/)
-  [scipy](https://www.scipy.org/)
-  [Pillow](https://pillow.readthedocs.io/en/stable/index.html)
-  [matplotlib](https://matplotlib.org)
-  [pywin32 (Windows)](https://github.com/mhammond/pywin32)
-  [pyobjc (Mac OS)](https://pythonhosted.org/pyobjc/)

Installation
------------

This package and its dependencies are available as wheel packages for macOS and Windows distributions from [PyPI](https://pypi.org/project/imhr):

    python -m pip install imhr

or the [anaconda](https://anaconda.org/risoms/imhr) package cloud repo:

	conda install -c risoms imhr

You can also install the development version directly from [github](https://www.github.com/risoms/mdl):

    pip install git+https://github.com/risoms/mdl.git


Testing
-------

After installation, you can launch the test suite after downloading from [github](https://www.github.com/risoms/mdl):

    pytest --pyargs imhr.tests --html=report.html --self-contained-html

or from the Python interpreter:

	import imhr
    imhr.tests

Note that the test suite requires pytest. Please install with pip or your package manager of choice.
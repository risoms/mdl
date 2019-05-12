.. _install:

.. currentmodule:: mdl

Installation
""""""""""""

.. raw:: html

   <div class="col-md-9">

This package and its dependencies are available as wheel packages for macOS and Windows distributions from `PyPI <https://pypi.org/project/imhr>`__::

	pip install imhr 

or the `anaconda <https://anaconda.org/risoms/imhr>`__ package cloud repo::

	conda install -c risoms imhr

You can also install the development version directly from `github <https://github.com/risoms/mdl>`__ repo::

	pip install git+https://github.com/risoms/mdl.git

Testing
~~~~~~~

After installation, you can launch the test suite::

	pytest mdl/tests

Dependencies
~~~~~~~~~~~~

mdl requires the following dependencies:

-  `Python 3.6 + <https://www.python.org/downloads/>`__

-  `numpy <http://www.numpy.org/>`__

-  `scipy <https://www.scipy.org/>`__

-  `PIL <https://pillow.readthedocs.io/en/stable/index.html>`__

-  `matplotlib <https://matplotlib.org>`__

-  `pywin32 (if using Windows) <https://github.com/mhammond/pywin32>`__

-  `pyobjc (if using Mac OS) <https://pythonhosted.org/pyobjc/>`__

.. raw:: html

   </div>
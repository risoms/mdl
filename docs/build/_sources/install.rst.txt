.. _install:

.. currentmodule:: mdl

Installation
""""""""""""

Dependencies
~~~~~~~~~~~~

This package requires the following dependencies:

.. cssclass:: dependencies1
.. literalinclude:: ../../requirements.txt
	:tab-width: 4
	:language: text

-  `Python 3.6 + <https://www.python.org/downloads/>`__

-  `numpy <http://www.numpy.org/>`__

-  `scipy <https://www.scipy.org/>`__

-  `PIL <https://pillow.readthedocs.io/en/stable/index.html>`__

-  `matplotlib <https://matplotlib.org>`__

-  `pywin32 (if using Windows) <https://pypi.org/project/pywin32/>`__

-  `pyobjc (if using Mac OS) <https://pypi.org/project/pyobjc//>`__

Installing
~~~~~~~~~~

This package and its dependencies are available as wheel packages for macOS and Windows distributions from `PyPI <https://pypi.org/project/imhr>`__:

.. code-block:: console
	
	$ pip install imhr 

or the `anaconda <https://anaconda.org/risoms/imhr>`__ package cloud repo:

.. code-block:: console
	
	$ conda install -c risoms imhr

You can also install the development version directly from `github <https://github.com/risoms/mdl>`__:

.. code-block:: console
	
	$ pip install git+https://github.com/risoms/mdl.git

Testing
~~~~~~~

After installation, you can launch the test suite after downloading from `github <https://github.com/risoms/mdl>`__:

.. code-block:: console
	
	$ pytest --pyargs mdl.tests --html=report.html --self-contained-html

or from the Python interpreter:

.. code-block:: python
	
	import mdl
	mdl.tests

Note that the test suite requires pytest. Please install with pip or your package manager of choice.
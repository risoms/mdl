.. _install:

.. currentmodule:: mdl

Installation
""""""""""""

Dependencies
~~~~~~~~~~~~

This package requires the following dependencies:

.. cssclass:: dependencies1
{%- for item in packages %}
* {{ item }}
{%- endfor -%}

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
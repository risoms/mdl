#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:35:53 2019

@author: mdl-admin
"""

import os
from sphinx.application import Sphinx

# Main arguments 
srcdir = os.path.join(os.getcwd(), "docs/source/")
confdir = os.path.join(os.getcwd(), "docs/source/")
builddir = os.path.join(os.getcwd(), "docs/build/")
doctreedir = os.path.join(os.getcwd(), "docs/build/doctres")
builder = "html"

# Write warning messages to a file (instead of stderr)
#warning = open("/path/to/warnings.txt", "w")

# Create the Sphinx application object
app = Sphinx(srcdir, confdir, builddir, doctreedir, builder)

# Run the build
app.build()
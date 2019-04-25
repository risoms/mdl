#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:43:16 2019

@author: mdl-admin
"""

import os, sys; sys.path.append(os.path.abspath('../../../../'))
from mdl.roi import ROI

s = '/Users/mdl-admin/Desktop/roi/raw/'
d = '/Users/mdl-admin/Desktop/roi/output/'
m = '/Users/mdl-admin/Desktop/roi/metadata.xlsx'
shape = 'straight'
scale = 0.75
screensize = [1920,1080]
dformat = 'dataviewer'
ROI(source=s, destination=d, metadata=m, shape=shape, scale=scale, screensize=screensize, dformat=dformat, roi_column="feature")
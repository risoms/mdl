#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:43:16 2019

@author: mdl-admin
"""

import os, sys; sys.path.append(os.path.abspath('../../../../'))
import mdl

i = '/Users/mdl-admin/Desktop/roi/raw/'
o = '/Users/mdl-admin/Desktop/roi/output/'
m = '/Users/mdl-admin/Desktop/roi/metadata.xlsx'
roi = mdl.eyetracking.ROI(image_path=i, output_path=o, s_metadata=m, shape='straight', 
						  scale=0.75, screensize=[1920,1080], 
						  dformat='dataviewer', roiname="feature")
roi.process()
#roi.create()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:43:16 2019

@author: mdl-admin
"""

import os
import sys
sys.path.append(os.path.abspath('../../../../'))
import mdl

i = '/Users/mdl-admin/Desktop/roi/raw/'
o = '/Users/mdl-admin/Desktop/roi/output/'
m = '/Users/mdl-admin/Desktop/roi/metadata.xlsx'
roi = mdl.eyetracking.ROI(isMultiprocessing=False, isDebug=True, image_path=i, output_path=o, s_metadata=m, scale=1, 
						  screensize=[1920,1080], shape='straight', f_roi='dataviewer', roicolumn="feature")
df, error = roi.process()
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

image_path = '/Users/mdl-admin/Desktop/roi/raw/'
output_path = '/Users/mdl-admin/Desktop/roi/output/'
metadata_source = '/Users/mdl-admin/Desktop/roi/metadata.xlsx'
roi = mdl.eyetracking.ROI(isMultiprocessing=True, isDebug=True, 
						  image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
						  scale=1, screensize=[1920,1080], center=[(1920*.25),(1080*.25)], shape='straight', 
						  roi_format='both', roicolumn="feature", uuid=None, newcolumn={'position': 'bottom'})


df, error = roi.process()
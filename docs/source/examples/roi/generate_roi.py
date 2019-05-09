#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:43:16 2019

@author: mdl-admin
"""

#%% ##### import mdl package
import mdl

#%% ##### set path
image_path = '/Users/mdl-admin/Desktop/roi/raw'
output_path = '/Users/mdl-admin/Desktop/roi/output'
metadata_source = '/Users/mdl-admin/Desktop/roi/metadata.xlsx'

#%% ##### initiate
roi = mdl.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False,
	image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
	scale=1, screensize=[1920,1080], center=[(1920*.5),(1080*.5)], shape='straight', 
	roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})

#%% ##### start
df, error = roi.process()
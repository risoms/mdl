#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 09:09:26 2019

@author: mdl-admin
"""
# run code
# import
import imhr

# set path
path = imhr.__path__[0]
# parameters
image_path = '/Users/mdl-admin/Desktop/roi/raw/'
output_path = '/Users/mdl-admin/Desktop/roi/center/'
metadata_source = '/Users/mdl-admin/Desktop/roi/metadata.xlsx'
position = 'center_scaled'
# initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False,
    detection='manual', roi_format='both', shape='straight', scale=.75,
    image_path=image_path, output_path=output_path, metadata_source=metadata_source,
    screensize=[1920,1080], recenter=[(1920*.50),(1080*.50)], filetype='PSD',
    newcolumn={'position': position}, uuid=['image','roi','position'],
	append_output_name=position, image_backend='PIL')
# run
df, error = roi.process()































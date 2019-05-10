#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.  
@`date`: Created on Sat May 1 15:12:38 2019  
@`author`: Semeon Risom  
@`email`: semeon.risom@gmail.com  
@`url`: https://semeon.io/d/mdl
"""
#%% [markdown]
# #### Read ROI from photoshop PSD files
#%% [markdown]
# ##### import mdl package
#%%
import mdl
#%% [markdown]
# ##### set path
#%%
image_path = './raw/'
output_path = './output/'
metadata_source = 'metadata.xlsx'
#%% [markdown]
# ##### initiate
#%%
roi = mdl.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False, isDemo=True,
	image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
	scale=1, screensize=[1920,1080], center=[(1920*.5),(1080*.5)], shape='straight', 
	roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})
#%% [markdown]
# ##### start
#%%
df, error = roi.process()
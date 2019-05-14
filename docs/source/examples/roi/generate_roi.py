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
# #### import
#%%
import mdl

#%% [markdown]
# ##### set path
#%%


#%% [markdown]
# ##### initiate
#%%
roi = mdl.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False, isDemo=True,
	scale=0.5, screensize=[1920,1080], offset=[(1920*.25),(1080*.25)], shape='straight', 
	roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})

#%% [markdown]
# ##### run
#%%
df, error = roi.process()
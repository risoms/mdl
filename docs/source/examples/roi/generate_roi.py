#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.  
@`date`: Created on Sat May 1 15:12:38 2019  
@`author`: Semeon Risom  
@`email`: semeon.risom@gmail.com  
@`url`: https://semeon.io/d/imhr
"""

#%% [markdown]
# #### import
#%%
import imhr

#%% [markdown]
# ##### set path
#%%


#%% [markdown]
# ##### creating ROIs at .5 scale and recentering at x=1920/2, y=1080/4
#%%
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=True,
	scale=0.5, screensize=[1920,1080], recenter=[(1920*.50),(1080*.25)], shape='straight', 
	roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'topcenter'})

#%% [markdown]
# ##### run
#%%
df, error = roi.process()
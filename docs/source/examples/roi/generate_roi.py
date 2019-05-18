#!/usr/bin/python3
#-*- coding: utf-8 -*-
#%% [markdown]
#.. roi_:  
# 
#.. title:: roi  
#
#### Region of Interest
#%% [markdown]
#<div class='info'>
#<p>@`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.</p>  
#<p>@`date`: Created on Sat May 1 15:12:38 2019</p>  
#<p>@`author`: Semeon Risom</p>  
#<p>@`email`: semeon.risom@gmail.com</p>  
#<p>@`url`: https://semeon.io/d/imhr</p>
#</div>
#%% [markdown]
#<ul class="list-container">
#    <li>
#        <div class="title">ROI Detection:</div>
#        <ol class="list">
#            <li>Highlighted ROI from Photoshop PSD.</li>
#            <li>Classified using Haar Cascades.</li>
#        </ol>
#    </li>
#    <li>
#        <div class="title">Boundary shape:</div>
#        <ol class="list">
#            <li>Polygon</li>
#            <li>Hull</li>
#            <li>Circle</li>
#            <li>Rectangle (rotated)</li>
#            <li>Rectangle (straight)</li>
#        </ol>
#    </li>
#    <li>
#        <div class="title">Output format:</div>
#        <ol class="list">
#            <li>Excel</li>
#            <li>EyeLink DataViewer ias</li>
#        </ol>
#    </li>
#</ul>
#%%
%pwd 
%cd /Users/mdl-admin/Desktop/mdl/
#%% [markdown]
##### 1. Demonstration
#%%
#import
import imhr
#initiate
roi = imhr.eyetracking.ROI(isDebug=True, isDemo=True)
#run
df, error = roi.process()
#%% [markdown]
#<p>and here are the results.</p>
#%%
#results
df
#%% [markdown]
##### 2. Highlighted ROI from Photoshop PSD
#%%
%matplotlib inline
from pylab import *  
from pathlib import Path
import matplotlib.pyplot as plt  
import matplotlib.image as image  
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12,6))  
path = Path('%s/imhr/dist/roi/output/img/'%(Path.cwd()))  
#roi  
im = image.imread('%s/preprocessed/AM_201.png'%(path))  
ax1.imshow(im)  
ax1.axis('off')  
ax1.set_title('Region of Interest')  
#contour  
im = image.imread('%s/bounds/AM_201.png'%(path))  
ax2.imshow(im)  
ax2.axis('off')  
ax2.set_title('Rectangular Bounds')  
#show 
plt.tight_layout()  
plt.show()  
show()
#%%
#import
import imhr
#set path
root = imhr.__path__[0]
image_path = '%s/dist/roi/raw/1/'%(root)
output_path = '%s/dist/roi/output/'%(root)
metadata_source = '%s/dist/roi/raw/1/metadata.xlsx'%(root)
#initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False, detection='manual',
	   image_path=image_path, output_path=output_path, metadata_source=metadata_source, shape='straight',
	   scale=1, screensize=[1920,1080], roi_format='both', recenter=[(1920*.50),(1080*.50)], 
	   uuid=['image','roi','position'], newcolumn={'position': 'center'})
#run
df, error = roi.process()
#%% [markdown]
#<p>and here are the results.</p>
#%%
#results
df
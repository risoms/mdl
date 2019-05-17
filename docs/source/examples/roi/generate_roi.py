#!/usr/bin/python3
# -*- coding: utf-8 -*-
#%% [markdown]
#.. roi_:  
#  
#.. title:: roi  
#
#### Region of Interest
#%% [markdown]
# <div class='info'>
# <p>@`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.</p>  
# <p>@`date`: Created on Sat May 1 15:12:38 2019</p>  
# <p>@`author`: Semeon Risom</p>  
# <p>@`email`: semeon.risom@gmail.com</p>  
# <p>@`url`: https://semeon.io/d/imhr</p>
# </div>
#%% [markdown]
# <ul class="list-container">
#     <li>
#         <div class="title">ROI Detection:</div>
#         <ol class="list">
#             <li>Highlighted ROI from Photoshop PSD.</li>
#             <li>Classified using Haar Cascades.</li>
#         </ol>
#     </li>
#     <li>
#         <div class="title">Boundary shape:</div>
#         <ol class="list">
#             <li>Polygon</li>
#             <li>Hull</li>
#             <li>Circle</li>
#             <li>Rectangle (rotated)</li>
#             <li>Rectangle (straight)</li>
#         </ol>
#     </li>
#     <li>
#         <div class="title">Output format:</div>
#         <ol class="list">
#             <li>Excel</li>
#             <li>EyeLink DataViewer ias</li>
#         </ol>
#     </li>
# </ul>
#%%
%pwd 
%cd /Users/mdl-admin/Desktop/mdl/
#%% [markdown]
##### 1. Demonstration
#%%
# import
import imhr
# initiate
roi = imhr.eyetracking.ROI(isDebug=True, isDemo=True)
# run
df, error = roi.process()
#%% [markdown]
# <p>and here are the results.</p>
#%%
# results
df
#%% [markdown]
##### 2. Highlighted ROI from Photoshop PSD
#%% [markdown]
#.. plot::  
# 	:include-source:
#  
# 	from pylab import *  
# 	import matplotlib.pyplot as plt  
# 	import matplotlib.image as image  
# 	fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12,6))  
# 	# roi  
# 	im = image.imread('/Users/mdl-admin/Desktop/roi/output/img/preprocessed/AM_201.png')  
# 	ax1.imshow(im)  
# 	ax1.axis('off')  
# 	ax1.set_title('Region of Interest')  
# 	# contour  
# 	im = image.imread('/Users/mdl-admin/Desktop/roi/output/img/bounds/AM_201.png')  
# 	ax2.imshow(im)  
# 	ax2.axis('off')  
# 	ax2.set_title('Rectangular Bounds')  
# 	# show 
# 	plt.tight_layout()  
# 	plt.show()  
# 	show()
#
#%%
# import
import imhr
# set path
image_path = '/Users/mdl-admin/Desktop/roi/raw/2/'
output_path = '/Users/mdl-admin/Desktop/roi/output/'
metadata_source = '/Users/mdl-admin/Desktop/roi/raw/2/metadata.xlsx'
# initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False, detection='manual',
	   image_path=image_path, output_path=output_path, metadata_source=metadata_source,
	   scale=1, screensize=[1920,1080], shape='straight', 
	   roi_format='both', recenter=[(1920*.50),(1080*.50)], 
	   uuid=['image','roi','position'], 
	   newcolumn={'position': 'center'})
# run
df, error = roi.process()
#%% [markdown]
# <p>and here are the results.</p>
#%%
# results
df
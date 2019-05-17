#!/usr/bin/python3
# -*- coding: utf-8 -*-
#%% [markdown]
# .. roi_:
# 
# .. title:: roi
# 
# #### Region of Interest
# 
# """
# @`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.  
# @`date`: Created on Sat May 1 15:12:38 2019  
# @`author`: Semeon Risom  
# @`email`: semeon.risom@gmail.com  
# @`url`: https://semeon.io/d/imhr
# """

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
#%% [markdown]
# ##### 1. Demonstration
#%%
# import
import imhr
# initiate
roi = imhr.eyetracking.ROI(isDebug=True, isDemo=True)
# run
df, error = roi.process()
#%% [markdown]
# ##### 2. Highlighted ROI from Photoshop PSD
#%% 
#!/usr/bin/python3
% matplotlib notebook
import matplotlib.pyplot as plt
import matplotlib.image as image
image = image.imread('/Users/mdl-admin/Desktop/roi/output/img/raw/2550.png')
fig, ax = plt.subplots(figsize=(16,8))
im = ax.imshow(image)
ax.axis('off')
plt.tight_layout()
plt.show()
#%%
# set path
image_path = '/Users/mdl-admin/Desktop/roi/raw/2/'
output_path = '/Users/mdl-admin/Desktop/roi/output/'
metadata_source = '/Users/mdl-admin/Desktop/roi/raw/2/metadata.xlsx'
# initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False, detection='manual',
	   image_path=image_path, output_path=output_path, metadata_source=metadata_source,
	   scale=1, screensize=[1920,1080], shape='polygon', 
	   roi_format='both', recenter=[(1920*.50),(1080*.50)], 
	   uuid=['image','roi','position'], 
	   newcolumn={'position': 'topcenter'})
# run
df, error = roi.process()
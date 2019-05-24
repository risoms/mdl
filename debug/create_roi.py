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
image_path = '%s/dist/roi/raw/2/'%(path)
output_path = '/Users/mdl-admin/Desktop/roi'
metadata_source = '%s/dist/roi/raw/2/metadata.xlsx'%(path)
position = 'straight'
# initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False,
    detection='manual', roi_format='both', shape=position, scale=1,
    image_path=image_path, output_path=output_path, metadata_source=metadata_source,
    screensize=[1920,1080], recenter=[(1920*.50),(1080*.50)],
    newcolumn={'position': position}, uuid=['image','roi','position'],
	append_output_name=False, image_backend='PIL')
# run
df, error = roi.process()

## create image
#import matplotlib.pyplot as plt
#import matplotlib.image as image
#from pathlib import Path
## path
#path = '%s/dist/roi/output/img/bounds/'%(Path(imhr.__file__).parent)
## draw plot
#plt.figure(figsize=(14,6), dpi=400, tight_layout=True, facecolor='#ffffff')
#fig, (axes) = plt.subplots(1, 4, sharey=True)
## names
#shape = 'circle'
#filenames = ['2550_%s.png'%(shape),'2691_%s.png'%(shape),'4640_%s.png'%(shape),'9421_%s.png'%(shape)]
## draw and save
#for idx, itm in enumerate(zip(axes, filenames)):
#	ax, file, = itm
#	## load roi
#	im = image.imread('%s/%s'%(path, file))
#	ax.imshow(im)
#	ax.grid(True)
#	ax.set_facecolor('#f9f9f9')
#	# labels
#	if idx == 0: ax.set_ylabel('Screen Y (pixels)', fontsize=8)
#	ax.set_xlabel('Screen X (pixels)', fontsize=8)
#	ax.tick_params(labelsize=6, width=1, length=4)
## save
#plt.subplots_adjust(wspace=0.1)
#plt.close(fig)








#initiate
roi = imhr.eyetracking.ROI(isDemo=True, isDebug=True)
#run
df, error = roi.process();






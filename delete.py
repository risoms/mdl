#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 09:09:26 2019

@author: mdl-admin
"""

# import
import imhr

# set path
path = imhr.__path__[0]
image_path = '%s/dist/roi/raw/2/'%(path)
output_path = '/Users/mdl-admin/Desktop/roi'
metadata_source = '%s/dist/roi/raw/2/metadata.xlsx'%(path)
position = 'center'
## initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False,
    detection='manual', roi_format='both', shape='polygon', scale=.75,
    image_path=image_path, output_path=output_path, metadata_source=metadata_source,
    screensize=[1920,1080], recenter=[(1920*.50),(1080*.50)],
    newcolumn={'position': position}, uuid=['image','roi','position'],
	append_output_name=position, image_backend='PIL')
df, error = roi.process()
##test------------------------------------------------------------------------------------------------------------------------
#df, error = roi.process()
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import psd_tools, os, cv2
directory = roi.directory
file = directory[0]
psd = psd_tools.PSDImage.open(file)
imagename = os.path.splitext(os.path.basename(file))[0]
## test---------------------------------------------------------------------------------------------------------------
# get layer
layer = psd[1].topil()
size = layer.size
layer.load()
#layer.show()

## test: paste image to white background, convert to RGB
layer_RGB = Image.new("RGB", size=size, color=(255, 255, 255))
layer_RGB.paste(layer, mask=layer.split()[3])
#layer_RGB.show()

# get image
inverted_image = ImageOps.invert(layer_RGB)
layer_np_ = np.array(inverted_image)
imgray = cv2.cvtColor(layer_np_, cv2.COLOR_BGR2GRAY)
cv2.imwrite('/Users/mdl-admin/Desktop/roi/test_cv2.png', imgray)
# contours
ret, thresh = cv2.threshold(src=imgray, thresh=1, maxval=255, type=0)
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)	
cnt = contours[0]
# shape
_epsilon = 0.01 * cv2.arcLength(cnt, True)
polygons = cv2.approxPolyDP(curve=cnt, epsilon=_epsilon, closed=True)
# save
layer_zeros = np.full_like(imgray, 255) ## Return an array of x with the same shape and type as a given array.
cv2.drawContours(image=layer_zeros, contours=[polygons],  contourIdx=-1, color=(0,0,0), thickness=-1)
cv2.imwrite('/Users/mdl-admin/Desktop/roi/test_cv2_f.png', data)
# post: convert layer background to transparent
coord = [] # coordinates for ROI export (ias, xlsx)
color = (91, 150, 190, 255)
img = Image.fromarray(layer_zeros)
img = img.convert("RGBA")
pixdata = img.load() # allow PIL processing
width, height = img.size
for y in range(height):
	for x in range(width):
		# convert background to transparent
		if pixdata[x, y] == (255, 255, 255, 255):
			pixdata[x, y] = (255, 255, 255, 0)
		# convert forground to color
		elif pixdata[x, y] == (0, 0, 0, 255):
			pixdata[x, y] = color
			# store coordinates for ROI export (ias, xlsx)
			coord.append([x,y])
img.save('/Users/mdl-admin/Desktop/roi/test_pil_f.png', "PNG")


























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
output_path = '/Users/mdl-admin/Desktop/roi'
metadata_source = '%s/dist/roi/raw/2/metadata.xlsx'%(path)
position = 'straight'
# initiate
roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isDemo=False,
    detection='haarcascade', roi_format='both', shape=position, scale=1,
    image_path=image_path, output_path=output_path, metadata_source=metadata_source,
    screensize=[1920,1080], recenter=[(1920*.50),(1080*.50)], filetype='PSD',
    newcolumn={'position': position}, uuid=['image','roi','position'],
	append_output_name=False, image_backend='PIL')
# run
df, error = roi.process()
#
#
#
#import cv2
#import sys
#import numpy as np
#import pandas as pd
#from PIL import Image
## Gets the name of the image file (filename) from sys.argv
##imagePath  = '/Users/mdl-admin/Desktop/roi/merkel.jpg'
#path  = '/Users/mdl-admin/Desktop/roi/raw'
#imglist = ['4640','2550','4640','9421']
## store coordinates
#l_coords_all = []
#for imgname in imglist:
#	imagePath = '%s/%s.png'%(path, imgname)
#	greypath = '/Users/mdl-admin/Desktop/roi/grey.png'
#	outpath = '/Users/mdl-admin/Desktop/roi/cascade.png'
#	cascPath = "/Users/mdl-admin/Desktop/mdl/imhr/dist/haarcascade/"	
#	l_coords = []
#	# The image is read and converted to grayscale
#	image = Image.open(imagePath)
#	cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#	gray = np.array(image.convert("L"))#; cv2.imwrite(greypath, gray)
#	# This creates the cascade classifcation from file
#	face_cascade = cv2.CascadeClassifier('%s/haarcascade_frontalface_default.xml'%(cascPath))
#	eye_cascade = cv2.CascadeClassifier('%s/haarcascade_eye.xml'%(cascPath))
#	body_cascade = cv2.CascadeClassifier('%s/haarcascade_fullbody.xml'%(cascPath))
#	# face cascade
#	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=5, minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)
#	for idx, (x, y, w, h) in enumerate(faces):
#		# store coords
#		l_coords.append([x, y, x+x+w/2, y+y+h/2, 'face', idx, imgname])
#		# draw face
#		cv2.rectangle(img=cv2_image, pt1=(x,y), pt2=(x+w,y+h), color=(0,255,0), thickness=3)
#		roi_gray = gray[y:y + h, x:x + w]
#		roi_color = cv2_image[y:y + h, x:x + w]
#		# eyes
#		eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.02, minNeighbors=5, minSize=(50, 50))
#		for (ex, ey, ew, eh) in eyes:
#			l_coords.append([x, y, x+x+w/2, y+y+h/2, 'eyes', idx, imgname])
#			cv2.rectangle(roi_color,pt1=(ex, ey), pt2=(ex+ew, ey+eh), color=(255,0,0), thickness=3)
#	# body cascade
#	body = body_cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=5, minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)
#	for (x, y, w, h) in body:
#		# store coords
#		l_coords.append([x, y, x+x+w/2, y+y+h/2, 'body', idx, imgname])
#		#draw body
#		cv2.rectangle(img=cv2_image, pt1=(x,y), pt2=(x+w,y+h), color=(0,0,255), thickness=3)
#		 
#	# save image
#	imagePath = '/Users/mdl-admin/Desktop/roi/%s.png'%(imgname)
#	cv2.imwrite(imagePath, cv2_image)
#	# save data
#	datapath = '/Users/mdl-admin/Desktop/roi/%s.xlsx'%(imgname)
#	df = pd.DataFrame(l_coords, columns=['x0', 'y0', 'x1', 'y1', 'feature', 'id', 'image'])
#	df.to_excel("%s"%(datapath), index=False)
#	# store coords
#	l_coords_all.append(df)
#
## save data
#datapath = '/Users/mdl-admin/Desktop/roi/cascades.xlsx'
#df = pd.DataFrame(l_coords_all)
#df.to_excel("%s"%(datapath), index=False)






























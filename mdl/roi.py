#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----imports
# main
import gc
import os
import sys
from pathlib import Path

# package
from settings import settings
console = settings.console

#----external library
library = ['opencv-python','psd_tools', 'pathlib', 'gc', 'matplotlib', 'PIL']

class roi():
	def __init__(self, source=None, destination=None, shape='box', **kwargs):
		"""
		Create single subject trial bokeh plots.

		Parameters
		----------
		source : :class:`str`
			Source of image files.
		destination : :class:`str`
			Folder to save data.
		shape : :class:`str` {polygon, hull, circle, rotate, straight}
			ROI bounds. Default is straight. `polygon` creates a Contour Approximation  and will most closely match the orginal
			shape of the roi. `hull` creates a Convex Hull, which is similar to but not as complex as a Contour Approximation
			and will include bulges for areas that are convex. `circle` creates a mininum enclosing circle. Finally, both
			`rotate` and `straight` create a Bounding Rectangle, with the only  difference being compensation for the mininum
			enclosing area for the box when using `rotate`.
		**kwargs : optional
			Additional properties. Here's a list of available properties:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				header-rows: 1


				* - Property
					- Description
				* - isLibrary : :class:`bool`
					- Check if required packages have been installed. Default is False.
				* - save_data : :class:`bool`
					- Save coordinates. Default is True.
				* - save_raw_image : :class:`bool`
					- Save images. Default is False.
				* - save_contour_image : :class:`bool`
					- Save generated contours as images. Default is False.
				* - level : :class:`str`
					- Either combine output for each roi (`stimulus`) or seperate by roi (`roi`) or both (`both`). Default is `both`.
				* - sep : :class:`str`
					-  (If `source` == `psd`) How is metadata delimited, options are: `;` `,` `|` `tab` or `space` Default is `;`.
				* - source : :class:`str`
					- Metadata source, options are from a spreadsheet or a  Default is `psd`.
				* - screensize : :class:`list` of `int`
					- Monitor size is being presented. Default is [1920, 1080].
				* - scale : :class:`int`
					- If image is scaled during presentation, set scale. Default is 1.
				* - center : :class:`list` of `int`
					- Center point of image, relative to screensize. Default is [960, 540].
				* - dpi : :class:`int` or `None`
					- Quality of exported images, refers to 'dots per inch'. Default is 300 (if `save_image`=True).

		Attributes
		----------
		psd: `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`__
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest.
		retval, threshold : :class:`numpy.ndarray`
			Returns from :py:class:`cv2.threshold`. The function applies a fixed-level thresholding to a multiple-channel array.
			`retval` provides an optimal threshold only if :py:class:`cv2.THRESH_OTSU` is passed. `threshold` is an image after applying
			a binary threshold (cv2.THRESH_BINARY) removing all greyscale pixels < 127. The output matches the same image
			channel as the original image.
			See <https://docs.opencv.org/4.0.1/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57>`_ and
			`<https://www.learnopencv.com/opencv-threshold-python-cpp>`_
		contours, hierarchy : :class:`numpy.ndarray`
			Returns from :py:class:`cv2.findContours`. This function returns
			contours from the provided binary image (threshold). This is used here for later shape detection. `contours` are
			the detected contours, while hierarchy containing information about the image topology.
			See <https://docs.opencv.org/4.0.1/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e07>`_ for more information.
		image_contours : :class:`numpy.ndarray`
			Returns from :py:class:`cv2.drawContours`. This draws filled contours from the image.
		image_contours : :class:`numpy.ndarray`
			Returns from :py:class:`cv2.drawContours`. This draws filled contours from the image.

		Examples
		--------
		>>> s="/dist/example/raw/"; d="/dist/example/"
		>>> IMHR.roi(source=s, destination=d, shape='box')

		Notes
		-----
		**Resources**
		- See https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html for more information about each shape.
		- See https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html for more information about how images are drawn.
		- See https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html to understand how bounds are
		created.

		"""

		# check library
		self.isLibrary = kwargs['isLibrary'] if 'isLibrary' in kwargs else False
		if self.isLibrary:
			settings.library(library)

		#----parameters
		# delimiter
		self.delimiter = ';' if 'delimiter' not in kwargs else kwargs['delimiter']
		# screensize
		self.screensize = [1920, 1080] if 'screensize' not in kwargs else kwargs['screensize']
		# scale
		self.scale = 1.0 if 'scale' not in kwargs else kwargs['scale']
		#center
		self.cx = self.screensize[0]/2
		self.cy = self.screensize[1]/2
		self.coordinates = [self.cx, self.cy] if 'coordinates' not in kwargs else kwargs['coordinates']
		# shape
		self.shape = shape if shape in ['polygon', 'hull', 'circle', 'rotate', 'straight'] else 'straight'
		# dpi
		self.dpi = 300 if 'dpi' not in kwargs else kwargs['dpi']
		# save
		self.save = {}
		# save csv
		self.save['data'] = kwargs['save_data'] if 'save_data' in  kwargs else True
		# save contour images
		self.save['contours'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save raw images
		self.save['raw'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save level
		self.save['level'] = kwargs['level'] if 'level' in kwargs else 'both'
		# source
		if source is None:
			self.source = os.getcwd() + "/dist/example/raw/"
		else:
			self.source = source
		# destination
		if destination is None:
			self.destination = os.getcwd() + "/dist/example/"
		else:
			self.destination = destination

	def run(self):
		#----data
		import cv2
		import pandas as pd
		import numpy as np

		#----plot
		from PIL import Image
		import matplotlib.pyplot as plt
		import matplotlib.patches as patches
		from psd_tools import PSDImage

		#----directory
		directory = [x for x in Path(self.source).glob("*.psd") if x.is_file()]

		#----output
		for folder in ['output/stim/raw','output/stim/data', 'output/roi/contours','output/roi/data']:
			p = Path('%s/%s/'%(self.destination, folder))
			#check if path exists
			if not os.path.exists(p):
				os.makedirs(p)

		#----for each image
		console('for each image','green')
		for file in directory:
			#----start image
			# read image
			psd = PSDImage.open(file)
			imagename = os.path.splitext(os.path.basename(file))[0]

			# metadata
			self.filename = imagename
			self.imagename = '%s.png'%(imagename)
			self.channels = psd.channels #read channels
			self.width = psd.width #width and height
			self.height = psd.height

			# clear lists
			l_roi_bounds = []
			l_roi_contours = []
			l_error = []

			#save image
			#PSD = psd.topil()
			#white background
			#PSD.save('output/%s.png'%(filename))
			console('\n# file: %s'%(imagename),'green')
			#------------------------------------------------------------------------------------------------------for each layer/ROI
			for layer in psd:
				#skip if layer is main image
				if Path(layer.name).stem == imagename:
					continue
				else:
					#----start roi
					# clear plot
					plt.gcf().clear()

					# prepare metadata
					metadata = pd.DataFrame(data=(item.split("=") for item in layer.name.split(self.delimiter)),columns=['key','value'])
					metadata.set_index('key', inplace=True)
					metadata.loc['name']['value'] = metadata.loc['name']['value'].replace("roi","")

					# get constants
					roiname = metadata.loc['name']['value']
					shape = self.shape

					# print results
					console('## roi: %s'%(roiname),'green')
					console('%s'%(metadata),'blue')

					# load image directly from PSD
					image = np.array(layer.topil())
					#console(image.dtype)

					#----find contour
					try:
						# threshold the image
						## note: if any pixels that have value higher than 127, assign it to 255. convert to bw for countour and store original
						retval, threshold = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
						# cv2.imshow('image',threshold)

						#----find contour in image
						## note: if you only want to retrieve the most external contour # use cv.RETR_EXTERNAL
						contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

						#---if contours empty raise Exception
						if not bool(contours):
							_err = [imagename, roiname, 'Not able to identify contours']
							l_error.append(_err)
							raise Exception('%s; %s; %s'%(_err[0],_err[1],_err[2]))

					except Exception as error:
						console('%s'%(error),'red')
						continue

					#------------------------------------------------------------------------for each layer: save images and contours
					#when saving the contours below, only one drawContours function from above can be run
					#any other drawContours function will overlay on the others if multiple functions are run
					#----param
					color = (0,0,255)

					#----straight bounding box
					if shape=='straight':
						console('## generate straight bounding box','blue')
						# for each contour
						for ind, itm in enumerate(contours):
							cnt = contours[ind]
							# get bounds
							_x,_y,_w,_h = cv2.boundingRect(cnt)
							# convert all coordinates floating point values to int
							roi_bounds = np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))
							#draw contours
							roi_contours = cv2.rectangle(img=image, pt1=(_x,_y), pt2=(_x+_w,_y+_h), color=color, thickness=cv2.FILLED)
						# create bounds
						_bounds = roi_bounds
						# create contours
						_contours = sum([roi_contours])

					#----rotated bounding box
					elif shape=='rotate':
						console('## generate rotated bounding box','blue')
						# for each contour
						for ind, itm in enumerate(contours):
							cnt = contours[ind]
							# get bounds
							rect = cv2.minAreaRect(cnt)
							roi_bounds = cv2.boxPoints(rect)
							# convert all coordinates floating point values to int
							roi_bounds = np.int0(roi_bounds)
							#draw contours
							roi_contours = cv2.drawContours(image=image, contours=[roi_bounds], contourIdx=0, color=color, thickness=cv2.FILLED)
						# create bounds
						_bounds = roi_bounds
						# create contours
						_contours = sum([roi_contours])

					#----circle enclosing
					elif shape=='circle':
						console('## generate bounding circle','blue')
						# for each contour
						for ind, itm in enumerate(contours):
							cnt = contours[ind]
							(_x,_y),_r = cv2.minEnclosingCircle(cnt)
							#draw contours
							roi_contours = cv2.circle(img=image, center=(int(_x),int(_y)), radius=int(_r), color=color, thickness=cv2.FILLED)
						# create bounds
						_bounds = roi_bounds
						# create contours
						_contours = sum([roi_contours])

					#----Contour Approximation
					elif shape=='polygon':
						console('## generate approximate polygon','blue')
						# for each contour
						for ind, itm in enumerate(contours):
							cnt = contours[ind]
							epsilon = 0.01 * cv2.arcLength(cnt, True)
							# get approx polygons
							roi_bounds = cv2.approxPolyDP(cnt, epsilon, True)
							# draw approx polygons
							roi_contours = cv2.drawContours(image=image, contours=[roi_bounds], contourIdx=-1 ,color=color, thickness=cv2.FILLED)
						# create bounds
						_bounds = roi_bounds[:,0,:]
						# create contours
						_contours = sum([roi_contours])

					#----convex hull
					elif shape=='hull':
						console('generate hull','blue')
						# for each contour
						for ind, itm in enumerate(contours):
							cnt = contours[ind]
							# get convex hull
							roi_bounds = cv2.convexHull(itm)
							# draw hull
							roi_contours = cv2.drawContours(image=image,contours=[roi_bounds], contourIdx=-1, color=color, thickness=cv2.FILLED)
						# create bounds
						_bounds = roi_bounds[:,0,:]
						# create contours
						_contours = sum([roi_contours])

					else:
						pass
						#!!!Put after creating as function return console('Please select either polygon, box, or hull shape')

					#----store bounds as df
					bounds = pd.DataFrame(_bounds)
					#rename
					bounds.columns = ['x', 'y']
					# add image, roi, and shape
					bounds['image'] = imagename
					bounds['ROI'] = roiname
					bounds['shape'] = shape
					# clean-up
					## arrange
					bounds = bounds[['image','ROI','shape','x','y']]
					## convert to int
					bounds[['x', 'y']] = bounds[['x', 'y']].astype(int)
					## sort by x,y values
					bounds = bounds.sort_values(by=['x','y'])
					# append to list of df
					l_roi_bounds.append(bounds)

					#----store contours as df
					# _x, _y = _contours[:,0,0], _contours[:,0,1]
					# contours = pd.DataFrame(_contours)
					# contours.columns = ['x', 'y'] #rename
					# # add image, roi, and shape
					# contours['image'] = imagename
					# contours['ROI'] = roiname
					# contours['shape'] = shape
					# # clean-up
					# contours = contours[['image','ROI','shape','x','y']] #sort
					# contours[['x', 'y']] = contours[['x', 'y']].astype(int) #convert to int
					# # append to list of df
					# l_roi_contours.append(contours)

					#----save image:roi level image bounds and coordinates
					if ((self.save['level'] == 'both') or (self.save['level'] == 'roi')):
						#----save roi contour image
						if self.save['contours']:
							#----from source
							# create matplotlib plot
							fig, ax = plt.subplots()
							fig.canvas.flush_events()
							## original
							_arr = np.asarray(layer.topil())
							ax.imshow(_arr, zorder=1, interpolation='bilinear')
							## contours
							_arr = cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB)
							ax.imshow(_arr, zorder=2, interpolation='bilinear', alpha=0.3)
							## check if path exists
							_folder = '%s\\output\\roi\\contours\\final\\%s'%(self.destination, self.shape)
							if not os.path.exists(_folder):
								os.makedirs(_folder)
							## save
							plt.savefig('%s\\%s_%s_source.png'%(_folder, imagename, roiname), dpi=self.dpi)
							plt.close()

							#----recreated from dataframe bounds
							## from https://stackoverflow.com/questions/44593729/how-to-plot-rectangle-in-python
							##!!!Todo:get working
							# create matplotlib plot
							fig, ax = plt.subplots()
							fig.canvas.flush_events()

							# create blank image
							_img = Image.new("RGBA", (self.width, self.height), (255, 255, 255))
							ax.imshow(_img)
							# draw bounds
							_x = bounds['x'].unique().tolist()
							_y = bounds['y'].unique().tolist()
							_width = _x[1] - _x[0]
							_height = _y[1] - _y[0]
							ax.add_patch(patches.Rectangle((_x, _y), _width, _height))
							## check if path exists
							_folder = '%s\\output\\roi\\contours\\debug\\%s'%(self.destination, shape)
							if not os.path.exists(_folder):
								os.makedirs(_folder)
							## save
							plt.savefig('%s\\%s_%s_source.png'%(_folder, imagename, roiname), dpi=self.dpi)
							plt.close()

							# recreated from dataframe countours
							#!!!Todo:get working
							#plt.imshow(cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB))
							#plt.savefig('%s/output/roi/contours/%s/%s_%s_recreated.png'%(destination, shape, imagename, roiname), dpi=dpi)
							## close plt.cla() #plt.clf() #plt.close()
							plt.close()

						#----save roi df
						if self.save['data']:
							#bounds
							bounds.to_csv("%s/data/%s_%s_bounds.csv"%(folder, imagename, roiname), index=False)
							#coordinates
							#contours.to_csv("%s/output/roi/data/%s_%s_bounds.csv"%(destination, imagename, roiname), index=False)

			#----save all roi data
			if ((self.save['level'] == 'both') or (self.save['level'] == 'stimulus')):
				#----save all roi image
				if self.save['raw']:
					plt.imshow(psd.topil())
					plt.savefig('%s/output/stim/raw/%s.png'%(self.destination, imagename), dpi=self.dpi)
					plt.close()

				#----save data
				#bounds
				df = pd.concat(l_roi_bounds)
				## sort by x,y values
				df = df.sort_values(by=['ROI','x','y'])
				## to csv
				df.to_csv("%s/output/stim/data/%s_bounds.csv"%(self.destination, imagename), index=False)
				#coord
				# df = pd.concat(l_roi_contours)
				# df.to_csv("%s/output/stim/data/%s_coord.csv"%(destination, imagename), index=False)

				#----finish
				# clear plot
				plt.cla()
				plt.clf()
				plt.close()
				# clear memory at end of iterable
				gc.collect()

				#draw image
				#cv2.imshow('image',img)
				#k = cv2.waitKey(0)


				#----save table of ROI coordinates
				# console('exporting %s ROI coordinates'%(s2['name']))
				# # create df
				# headers=['id','x','y']
				# coord_image_df = pd.DataFrame(coord_image, columns=headers)
				# coord_image_df.to_csv('%s/%s.csv'%(output['output'], filename), index=False)
				# del coord_image_df

		#----error log
		if bool(l_error):
			_filename = Path('%s/error.csv'%(self.destination))
			console("Errors found. See log %s"%(_filename), 'red')
			df = pd.DataFrame(l_error, columns=['image','roi','message'])
			df.to_csv(_filename, index=False)

		#%% test
		# drawing image
		# img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# cv2.imshow('image',img)

		# convert img to np array
		# np_img = np.array(img)













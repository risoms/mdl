#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Create regions of interest that can be used for data processing and analysis.  
| @date: Created on Sat May 1 15:12:38 2019  
| @author: Semeon Risom  
| @email: semeon.risom@gmail.com  
| @url: https://semeon.io/d/mdl
"""

import sys
import os
import gc
from pdb import set_trace as breakpoint

# available functions
__all__ = ['ROI']

# required external library
__required__ = ['opencv-python','psd_tools','pathlib','gc','matplotlib','PIL','secrets']

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# local libraries
from mdl import settings
console = settings.console

class ROI():
	def __init__(self, source=None, destination=None, metadata=None, shape='box', **kwargs):
		"""Create single subject trial bokeh plots.

		Parameters
		----------
		source : :class:`str`
			Image directory path.
		destination : :class:`str`
			Path to save data.
		metadata : :class:`str` or :obj:`None`
			Path of metadata, if metadata is read from a seperate file. If metadata is stored within the images, metadata = None.    
		shape : :class:`str` {polygon, hull, circle, rotate, straight}
			ROI bounds. Default is `straight`. `polygon` creates a Contour Approximation  and will most closely match the orginal
			shape of the roi. `hull` creates a Convex Hull, which is similar to but not as complex as a Contour Approximation
			and will include bulges for areas that are convex. `circle` creates a mininum enclosing circle. Finally, both
			`rotate` and `straight` create a Bounding Rectangle, with the only  difference being compensation for the mininum
			enclosing area for the box when using `rotate`.
		**kwargs : :obj:`str` or :obj:`None`, optional
			Additional properties. Here's a list of available properties:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **isLibrary** : :class:`bool`
				  - Check if required packages have been installed. Default is `False`.
				* - **dformat** : :class:`str` {dataviewer, raw}
				  - Exported data will be formatted to be read to either `dataviewer` or `raw`. Default is `raw`. Note: If dformat = `dataviewer`, \
				  shape must be either be `circle`, `rotate`, or `straight`.
				* - **roi_label** : :class:`bool`
				  - (`if dformat == dataviewer`) Name of ROI column. Default is 'ROI'.
				* - **save_data** : :class:`bool`
				  - Save coordinates. Default is `True.`
				* - **save_raw_image** : :class:`bool`
				  - Save images. Default is False.
				* - **save_contour_image** : :class:`bool`
				  - Save generated contours as images. Default is `False`.
				* - **level** : :class:`str`
				  - Either combine output for each roi (`stimulus`) or seperate by roi (`roi`) or both (`both`). Default is `both`.
				* - **delimiter** : :class:`str`
				  - (`if source == psd`) How is metadata delimited, options are: `;` `,` `|` `tab` or `space` Default is `;`.
				* - **screensize** : :class:`list` [:obj:`int`]
				  - Monitor size is being presented. Default is `[1920, 1080]`.
				* - **scale** : :class:`int`
				  - If image is scaled during presentation, set scale. Default is 1.
				* - **center** : :class:`list` [:obj:`int`]
				  - Center point of image, relative to screensize. Default is `[960, 540]`.
				* - **dpi** : :class:`int` or :obj:`None`
				  - (`if save_image == True`) Quality of exported images, refers to 'dots per inch'. Default is `300`.

		Attributes
		----------
		shape_d : :class:`str` {ELLIPSE, FREEHAND, RECTANGLE}
			DataViewer ROI shape.
		psd :  `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`_
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest.
		retval, threshold : :class:`numpy.ndarray`
			Returns from :obj:`cv2.threshold`. The function applies a fixed-level thresholding to a multiple-channel array.
			`retval` provides an optimal threshold only if :obj:`cv2.THRESH_OTSU` is passed. `threshold` is an image after applying
			a binary threshold (:obj:`cv2.THRESH_BINARY`) removing all greyscale pixels < 127. The output matches the same image
			channel as the original image.
			See `opencv <https://docs.opencv.org/4.0.1/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57>`_ and
			`leanopencv <https://www.learnopencv.com/opencv-threshold-python-cpp>`_ for more information.
		contours, hierarchy : :class:`numpy.ndarray`
			Returns from :obj:`cv2.findContours`. This function returns contours from the provided binary image (threshold). 
			This is used here for later shape detection. `contours` are the detected contours, while hierarchy containing 
			information about the image topology.
			See `opencv <https://docs.opencv.org/4.0.1/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e07>`_ 
			for more information.
		image_contours : :class:`numpy.ndarray`
			Returns from :obj:`cv2.drawContours`. This draws filled contours from the image.
		image_contours : :class:`numpy.ndarray`
			Returns from :obj:`cv2.drawContours`. This draws filled contours from the image.

		Examples
		--------
		>>> from mdl.roi import ROI
		>>> s="/dist/example/raw/"; d="/dist/example/"
		>>> ROI(source=s, destination=d, shape='box')

		Notes
		-----
		Resources
		    - See https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html for more information about each shape.
		    - See https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html for more information about how images are drawn.
		    - See https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html to understand how bounds are created.
		"""

		# check library
		self.isLibrary = kwargs['isLibrary'] if 'isLibrary' in kwargs else False
		if self.isLibrary:
			settings.library(__required__)

		#----parameters
		# metadata path (if metadata is not None)
		self.p_md = metadata
		# export format
		self.dformat = 'raw' if 'dformat' not in kwargs else kwargs['dformat']
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
		# label
		self.roi_column = 'ROI' if 'roi_column' not in kwargs else kwargs['roi_column']
		# dpi
		self.dpi = 300 if 'dpi' not in kwargs else kwargs['dpi']
		# save
		self.save = {}
		# save csv
		self.save['data'] = kwargs['save_data'] if 'save_data' in kwargs else True
		# save contour images
		self.save['contours'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save raw images
		self.save['raw'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save level
		self.save['level'] = kwargs['level'] if 'level' in kwargs else 'both'
		# source
		if source is None:
			self.source = os.getcwd() + "./dist/example/raw/"
		else:
			self.source = source
		# destination
		if destination is None:
			self.destination = os.getcwd() + "./dist/example/"
		else:
			self.destination = destination
		
		# check if trying to do complex ROI using dataviewer
		if (shape in ['polygon', 'hull']) and (self.dformat is "dataviewer"):
			raise Exception ("Cannot use shape %s when exporting for DataViewer. Please use either 'circle', 'rotate', or 'straight' instead."%(shape))
	
		self.run()
	
	def __time__(self):
		"""
		Get local time in ISO-8601 format.
		
		Returns
		-------
		iso : :class:`str`
			ISO-8601 datetime format, with timezone.
			
		Example
		-------
		>>> __time__()
		'2019-04-23 11:29:44-05:00'
		"""
		import datetime
		
		iso = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
		
		return iso
	
	def run(self):	
		#----data
		from pathlib import Path
		import cv2
		import pandas as pd
		import numpy as np
		import secrets
		
		#----plot
		from PIL import Image
		import matplotlib.pyplot as plt
		import matplotlib.patches as patches
		from psd_tools import PSDImage

		#----directory
		directory = [x for x in Path(self.source).glob("*.psd") if x.is_file()]

		#----output
		for folder in ['stim/raw','stim/data', 'roi/contours','roi/data']:
			p = Path('%s/%s/'%(self.destination, folder))
			#check if path exists
			if not os.path.exists(p):
				os.makedirs(p)

		#----read metadata file (if metadata is not None)
		if self.p_md is not None:
			_type = Path(self.p_md).suffix
			if _type == ".csv": metadata_all = pd.read_csv(self.p_md) 
			elif _type == ".xlsx": metadata_all = pd.read_excel(self.p_md)

		#----for each image
		console('for each image','green')
		for file in directory:
			#----start image
			# read image 
			psd = PSDImage.open(file)
			self.imagename = os.path.splitext(os.path.basename(file))[0]

			# file metadata
			self.filename = '%s.png'%(self.imagename)
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
			#PSD.save('%s.png'%(filename))
			console('\n# file: %s'%(self.imagename),'blue')

			#----------------------------------------------------------------------------------------------for each layer/ROI
			self.roinumber = 1
			color_roi = ['cyan','magenta','yellow','orange','blue','green','red']
			for layer in psd:
				#skip if layer is main image
				if Path(layer.name).stem == self.imagename:
					continue
				else:
					#----start roi
					# set roi color
					self.color_roi = secrets.choice(color_roi)
					# clear plot
					plt.gcf().clear()

					#----load image directly from PSD
					layer_image = layer.topil()
					# center and resize image to template screen
					_background = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
					layer_offset = ((self.screensize[0] - layer_image.size[0])//2,(self.screensize[1] - layer_image.size[1])//2)
					_background.paste(layer_image, layer_offset)
					image = np.array(_background)
					#image = np.array(_image)
					
					#----prepare metadata
					# if metadata is stored in image files directly
					if self.p_md is None:
						self.metadata = pd.DataFrame(data=(item.split("=") for item in layer.name.split(self.delimiter)),columns=['key','value'])
						self.metadata.set_index('key', inplace=True)
						self.metadata.loc['name']['value'] = self.metadata.loc['name']['value'].replace("roi","")
						
						# get metadata
						self.roiname = self.metadata.loc['name']['value']
						self.roilabel = self.metadata.loc['name']['value']
						   
						# print results
						console('## roiname: %s'%(self.roiname),'blue')
						console('## roilabel: %s'%(self.roilabel),'green')
						console('## roinumber: %s'%(self.roinumber),'green')
					# else read metadata from file
					else:
						# get metadata
						self.roiname = layer.name
						self.metadata = metadata_all.loc[(metadata_all['image'] == self.imagename) & (metadata_all['roi'] == self.roiname)]
						# if datafame empty
						if self.metadata.empty:
							console('No data for %s:%s.'%(self.imagename,self.roiname),'red')
							continue
						else:
							self.roilabel = self.metadata[self.roi_column].item()
						   
						# print results
						console('## roiname: %s'%(self.roiname),'blue')
						console('## roilabel: %s'%(self.roilabel),'green')
						console('## roinumber: %s'%(self.roinumber),'green')

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
							_err = [self.imagename, self.roiname, 'Not able to identify contours']
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
					if self.shape is 'straight':
						console('## generate straight bounding box','blue')
						self.shape_d = 'RECTANGLE' # dataviewer shape
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
					elif self.shape is 'rotate':
						console('## generate rotated bounding box','green')
						self.shape_d = 'FREEHAND' # dataviewer shape
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
					elif self.shape is 'circle':
						console('## generate bounding circle','green')
						self.shape_d = 'ELLIPSE' # dataviewer shape
						# for each contour
						for ind, itm in enumerate(contours):
							cnt = contours[ind]
							# get minimal enclosing circle
							(_x,_y),_r = cv2.minEnclosingCircle(cnt)
							# convert all coordinates floating point values to int
							roi_bounds = np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))
							#get center and radius of circle
							center = (int(_x),int(_y))
							radius = int(_r)
							#draw contours
							roi_contours = cv2.circle(img=image, center=center, radius=radius, color=color, thickness=cv2.FILLED)
						# create bounds
						_bounds = roi_bounds
						# create contours
						_contours = sum([roi_contours])

					#----Contour Approximation
					elif self.shape is 'polygon':
						console('## generate approximate polygon','green')
						self.shape_d = 'FREEHAND' # dataviewer shape
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
					elif self.shape is 'hull':
						console('## generate hull','green')
						self.shape_d = 'FREEHAND' # dataviewer shape
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
						raise Exception('Please select either polygon, box, or hull shape.')

					#----store bounds as df
					_bounds = pd.DataFrame(_bounds)
					# transpose bounds (x0, x1, y0, y1)
					_x = _bounds[0].unique().tolist()
					_y = _bounds[1].unique().tolist()
					bounds = pd.DataFrame(np.column_stack([_x[0],_y[0],_x[1],_y[1]]))
					#rename
					bounds.columns = ['x0','y0','x1','y1']
					# add index, image, roi, and shape
					bounds['id'] = self.roinumber
					bounds['image'] = self.imagename
					bounds[self.roi_column] = self.roilabel
					bounds['shape'] = self.shape
					bounds['shape_d'] = self.shape_d
					bounds['color'] = self.color_roi
					# clean-up
					## arrange
					bounds = bounds[['image','shape','shape_d','id','x0','y0','x1','y1',self.roi_column,'color']]
					## convert to int
					bounds[['x0','y0','x1','y1']] = bounds[['x0','y0','x1','y1']].astype(int)
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

							#----load image directly from PSD
							_image = layer.topil()
							# center and resize image to template screen
							# _background = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
							# _background.paste(layer_image, layer_offset)
							# _arr = np.array(_background)
							# ax.imshow(_arr, zorder=2, interpolation='bilinear', alpha=1)
							## contours
							_arr = cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB)
							ax.imshow(_arr, zorder=1, interpolation='bilinear', alpha=1)
							## check if path exists
							_folder = '%s/roi/contours/final/%s'%(self.destination, self.shape)
							if not os.path.exists(_folder):
								os.makedirs(_folder)
							## save
							plt.savefig('%s/%s_%s_source.png'%(_folder, self.imagename, self.roiname), dpi=self.dpi)
							plt.close()

							#----recreated from dataframe bounds
							## from https://stackoverflow.com/questions/44593729/how-to-plot-rectangle-in-python
							##!!!Todo:get working
							# create matplotlib plot
							fig, ax = plt.subplots()
							fig.canvas.flush_events()

							# create blank image
							_img = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
							ax.imshow(_img)
							# draw bounds
							x0 = bounds['x0'].item()
							y0 = bounds['y0'].item()
							x1 = bounds['x1'].item()
							y1 = bounds['y1'].item()
							_width = x1 - x0
							_height = y1 - y0
							ax.add_patch(patches.Rectangle((x0, y0), _width, _height))
							
							## check if path exists
							_folder = '%s/roi/contours/debug/%s'%(self.destination, self.shape)
							if not os.path.exists(_folder):
								os.makedirs(_folder)
							## save
							plt.savefig('%s/%s_%s_source.png'%(_folder, self.imagename, self.roiname), dpi=self.dpi)
							plt.close()

							# recreated from dataframe countours
							#!!!Todo:get working
							#plt.imshow(cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB))
							#plt.savefig('%s/roi/contours/%s/%s_%s_recreated.png'%(destination, shape, imagename, roiname), dpi=dpi)
							## close plt.cla() #plt.clf() #plt.close()
							plt.close()

						#----save roi df
						if self.save['data']:
							# check if path exists
							_folder = '%s/roi/data/'%(self.destination)
							if not os.path.exists(_folder):
								os.makedirs(_folder)
							# export to csv or dataviewer
							if self.dformat is 'raw':
								bounds.to_csv("%s/%s_%s_bounds.csv"%(_folder, self.imagename, self.roiname), index=False)
							elif self.dformat is 'dataviewer':
								_bounds = '\n'.join(map(str, [
									"# EyeLink Interest Area Set created on %s."%(self.__time__()),
									"# Interest area set file using mdl.roi.ROI()",
									"# columns: RECTANGLE | IA number | x0 | y0 | x1 | y1 | label | color",
									"# columns: ELLIPSE | IA number | x0 | y0 | x1 | y1 | label | color",
									"# columns: FREEHAND | IA number | x0,y0 | x1,y1 | x2,y2 | x3,y3 | label | color",
									"# example: RECTANGLE 1 350 172 627 286 leftcheek red",
									"# example: ELLIPSE 2 350 172 627 286 leftcheek red",
									"# example: FREEHAND 3 350,172 627,172 627,286 350,286 leftcheek red",
									"# See Section 5.10.1 of Eyelink DataViewer Users Manual (3.2.1) for more information.",
									bounds[['shape_d','id','x0','y0','x1','y1',self.roi_column,'color']].to_csv(index=False, header=False).replace(',', '	')
								]))
								## create ias file
								_filename = "%s/%s_%s_bounds"%(_folder, self.imagename, self.roiname)
								with open("%s.ias"%(_filename), "w") as file:
									file.write(_bounds)
							# coordinates
							#contours.to_csv("%s/roi/data/%s_%s_bounds.csv"%(destination, imagename, roiname), index=False)

				# add to index counter
				self.roinumber = self.roinumber + 1
				
			#----save all roi data
			if ((self.save['level'] == 'both') or (self.save['level'] == 'stimulus')):
				#----save all roi image
				if self.save['raw']:
					# center and resize image to template screen
					_image = psd.topil()
					_background = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
					_offset = ((self.screensize[0] - _image.size[0])//2,(self.screensize[1] - _image.size[1])//2)
					_background.paste(_image, _offset)
					plt.imshow(np.array(_background))
					plt.savefig('%s/stim/raw/%s.png'%(self.destination, self.imagename), dpi=self.dpi)
					plt.close()

				#----save data
				#bounds
				df = pd.concat(l_roi_bounds)
				## sort by x,y values
				df = df.sort_values(by=['image','id'])
				## export to csv or dataviewer
				_folder = '%s/stim/data/'%(self.destination)
				if self.dformat is 'raw':
					df.to_csv("%s/%s_bounds.csv"%(_folder, self.imagename), index=False)
				elif self.dformat is 'dataviewer':
					_bounds = '\n'.join(map(str, [
						"# EyeLink Interest Area Set created on %s."%(self.__time__()),
						"# Interest area set file using mdl.roi.ROI()",
						"# columns: RECTANGLE | IA number | x0 | y0 | x1 | y1 | label | color",
						"# columns: ELLIPSE | IA number | x0 | y0 | x1 | y1 | label | color",
						"# columns: FREEHAND | IA number | x0,y0 | x1,y1 | x2,y2 | x3,y3 | label | color",
						"# example: RECTANGLE 1 350 172 627 286 leftcheek red",
						"# example: ELLIPSE 2 350 172 627 286 leftcheek red",
						"# example: FREEHAND 3 350,172 627,172 627,286 350,286 leftcheek red",
						"# See Section 5.10.1 of Eyelink DataViewer Users Manual (3.2.1) for more information.",
						df[['shape_d','id','x0','y0','x1','y1',self.roi_column,'color']].to_csv(index=False, header=False).replace(',', '	')
					]))
					## create ias file
					_filename = "%s/%s_bounds"%(_folder, self.imagename)
					with open("%s.ias"%(_filename), "w") as file:
						file.write(_bounds)
					
				#coord
				# df = pd.concat(l_roi_contours)
				# df.to_csv("%s/stim/data/%s_coord.csv"%(destination, imagename), index=False)

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
			error = pd.DataFrame(l_error, columns=['image','roi','message'])
			error.to_csv(_filename, index=False)
		else:
			error = ''


#%% test
# drawing image
# img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image',img)

# convert img to np array
# np_img = np.array(img)
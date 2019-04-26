#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Create regions of interest that can be used for data processing and analysis.  
| @date: Created on Sat May 1 15:12:38 2019  
| @author: Semeon Risom  
| @email: semeon.risom@gmail.com  
| @url: https://semeon.io/d/mdl
"""

# core
from pdb import set_trace as breakpoint
import sys
import os
import gc
import secrets

# data
from pathlib import Path
import pandas as pd
import numpy as np
import cv2

# plot
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from psd_tools import PSDImage

# local libraries
from mdl import settings
console = settings.console
now = settings.time

# available functions
__all__ = ['ROI']

# required external library
__required__ = ['opencv-python','psd_tools','pathlib','gc','matplotlib','PIL','secrets']

# this is a pointer to the module object instance it
this = sys.modules[__name__]

class ROI():
	def __init__(self, image_path=None, output_path=None, s_metadata=None, shape='box', roiname='roi', **kwargs):
		"""
		Generate region of interest to be read by Eyelink DataViewer or statistical tool.

		Parameters
		----------
		image_path : :class:`str`
			Image directory path.
		output_path : :class:`str`
			Path to save data.
		f_roi : :class:`str` {`raw`,`dataviewer`}
			Format to export ROIs. Either to 'csv' (`raw`) or to Eyelink DataViewer 'ias' (`dataviewer`).
			Default is `raw`. Note: If :code:`f_roi` = `dataviewer`, shape must be either be `circle`, `rotate`, or `straight`.
		s_metadata : :class:`str` or :obj:`None` {path, `embed`}
			Metadata source. If metadata is being read from a spreadsheet, :code:`s_metadata` should be equal to path the to
			the metadata file, else if metadata is embed within the image as a layer name, :code:`s_metadata` = `embeded`.
			Default is `embeded`. For example:
				>>> # if metadata is in PSD images
				>>> metadata = 'embeded'
				>>> # if metadata is an external xlsx file.
				>>> metadata = 'roi/metadata.xlsx'
			Although Photoshop PSD don't directly provide support for metadata. However if each region of interest is stored
			as a seperate layer within a PSD, the layer name can be used to store metadata. To do this, the layer name has
			to be written as delimited text. Our code can read this data and extract relevant metadata. The delimiter can
			be either `;` `,` `|` `tab` or `space` (Delimiter type must be identified when running this code using the
			code:`delimiter` parameter. The default is `;`.).
		shape : :class:`str` {`polygon`, `hull`, `circle`, `rotate`, `straight`}
			Shape of machine readable boundaries for region of interest. Default is `straight`. `polygon` creates a Contour
			Approximation and will most closely match the orginal shape of the roi. `hull` creates a Convex Hull, which
			is similar to but not as complex as a Contour Approximation and will include bulges for areas that are convex.
			`circle` creates a mininum enclosing circle. Finally, both `rotate` and `straight` create a Bounding Rectangle,
			with the only difference being compensation for the mininum enclosing area for the box when using `rotate`.
		roiname : :class:`str`
			The name of the label for the region of interest in your metadata. For example you may want to extract the column
			'feature' from your metadata and use this as the label. Default is `roi`.
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
				* - **save_data** : :class:`bool`
					- Save coordinates. Default is `True.`
				* - **save_raw_image** : :class:`bool`
					- Save images. Default is False.
				* - **save_contour_image** : :class:`bool`
					- Save generated contours as images. Default is `False`.
				* - **level** : :class:`str`
					- Either combine output for each roi (`stimulus`) or seperate by roi (`roi`) or both (`both`). Default is `both`.
				* - **delimiter** : :class:`str`
					- (if :code:`source` == `psd`) How is metadata delimited, options are: `;` `,` `|` `tab` or `space` Default is `;`.
				* - **screensize** : :class:`list` [:obj:`int`]
					- Monitor size is being presented. Default is `[1920, 1080]`.
				* - **scale** : :class:`int`
					- If image is scaled during presentation, set scale. Default is 1.
				* - **center** : :class:`list` [:obj:`int`]
					- Center point of image, relative to screensize. Default is `[960, 540]`.
				* - **dpi** : :class:`int` or :obj:`None`
					- (if :code:`save_image` == `True`) Quality of exported images, refers to 'dots per inch'. Default is `300`.

		Raises
		------
		Exception
			[description]
		Exception
			[description]

		Attributes
		----------
		shape_d : :class:`str` {`ELLIPSE`, `FREEHAND`, `RECTANGLE`}
			DataViewer ROI shape.
		psd :  `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`_
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest.
		retval, threshold : :class:`numpy.ndarray`
			Returns from :ref:`cv2.threshold`. The function applies a fixed-level thresholding to a multiple-channel array.
			`retval` provides an optimal threshold only if :ref:`cv2.THRESH_OTSU` is passed. `threshold` is an image after applying
			a binary threshold (:ref:`cv2.THRESH_BINARY`) removing all greyscale pixels < 127. The output matches the same image
			channel as the original image.
			See `opencv <https://docs.opencv.org/4.0.1/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57>`_ and
			`leanopencv <https://www.learnopencv.com/opencv-threshold-python-cpp>`_ for more information.
		contours, hierarchy : :class:`numpy.ndarray`
			Returns from :ref:`cv2.findContours`. This function returns contours from the provided binary image (threshold).
			This is used here for later shape detection. `contours` are the detected contours, while hierarchy containing
			information about the image topology.
			See `opencv <https://docs.opencv.org/4.0.1/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e07>`_
			for more information.
		image_contours : :class:`numpy.ndarray`
			Returns from :ref:`cv2.drawContours`. This draws filled contours from the image.
		image_contours : :class:`numpy.ndarray`
			Returns from :ref:`cv2.drawContours`. This draws filled contours from the image.

		Examples
		--------
		>>> from mdl.roi import ROI
		>>> s="/dist/example/raw/"; d="/dist/example/"
		>>> ROI(source=s, output_path=d, shape='box')

		Notes
		-----
		Resources
			- See https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html for more information about each shape.
			- See https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html for more information about how images are drawn.
			- See https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html to understand how bounds are created.
		"""

		# check library
		isLibrary = kwargs['isLibrary'] if 'isLibrary' in kwargs else False
		if isLibrary:
			settings.library(__required__)

		#----parameters
		# lists
		## image level
		self.l_bounds = []
		self.l_contours = []
		## all images
		self.l_bounds_all = []
		self.l_contours_all = []
		self.l_error = []
		# how to read data
		self.s_metadata = kwargs['s_metadata'] if 's_metadata' in kwargs else 'embed'
		# how to format rois
		self.f_roi = kwargs['f_roi'] if 'f_roi' in kwargs else 'raw'
		# delimiter
		self.delimiter = ';' if 'delimiter' not in kwargs else kwargs['delimiter']
		# screensize
		self.screensize = [1920, 1080] if 'screensize' not in kwargs else kwargs['screensize']
		# scale
		self.scale = 1.0 if 'scale' not in kwargs else kwargs['scale']
		#center
		cx = self.screensize[0]/2
		cy = self.screensize[1]/2
		self.coordinates = [cx, cy] if 'coordinates' not in kwargs else kwargs['coordinates']
		# shape
		self.shape = shape if shape in ['polygon', 'hull', 'circle', 'rotate', 'straight'] else 'straight'
		self.shape_d = None #dataviewer shape
		# label
		self.roicolumn = roiname
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
		# image_path
		if image_path is None:
			self.image_path = os.getcwd() + "./dist/example/raw/"
		else:
			self.image_path = image_path
		# output_path
		if output_path is None:
			self.output_path = os.getcwd() + "./dist/example/"
		else:
			self.output_path = output_path
		#----shape
		# check if trying to do complex ROI using dataviewer
		if (self.shape in ['polygon', 'hull']) and (self.f_roi == "dataviewer"):
			raise Exception ("Cannot use shape %s when exporting for DataViewer. \
					Please use either 'circle', 'rotate', or 'straight' instead, or set f_roi == 'raw'."%(shape))

		#----directory
		self.directory = [x for x in Path(self.image_path).glob("*.psd") if x.is_file()]

		#----output
		for folder in ['stim/raw','stim/data', 'roi/contours','roi/data']:
			p = Path('%s/%s/'%(self.output_path, folder))
			#check if path exists
			if not os.path.exists(p):
				os.makedirs(p)

		#----read metadata file (if metadata is not None)
		if s_metadata != "embedded":
			self.s_metadata = s_metadata
			_type = Path(self.s_metadata).suffix
			if _type == ".csv": self.metadata_all = pd.read_csv(self.s_metadata)
			elif _type == ".xlsx": self.metadata_all = pd.read_excel(self.s_metadata)
	
			# check if metadata is empty
			if self.metadata_all.empty:
				raise Exception('No data for file: %s'%(self.s_metadata))

	def process_metadata(self, imagename, layer, roinumber):
		"""[summary]

		Parameters
		----------
		imagename : [type]
			[description]
		layer : [type]
			[description]
		roinumber : [type]
			[description]

		Returns
		-------
		[type]
			[description]
		[type]
			[description]
		[type]
			[description]
		"""

		#----prepare metadata
		# if metadata is stored in image files directly
		if self.s_metadata == 'embedded':
			metadata = pd.DataFrame(data=(item.split("=") for item in layer.name.split(self.delimiter)),columns=['key','value'])
			metadata.set_index('key', inplace=True)
			metadata.loc['name']['value'] = metadata.loc['name']['value'].replace("roi","")
			roiname = metadata.loc['name']['value']
			roilabel = metadata.loc['name']['value']

		# else read metadata from file
		else:
			# get metadata
			roiname = layer.name
			metadata = self.metadata_all.loc[(self.metadata_all['image'] == imagename) & (self.metadata_all['roi'] == roiname)]
			# if datafame empty
			if metadata.empty:
				console('No data for %s:%s.'%(imagename, roiname),'red')
			else:
				roilabel = metadata[self.roicolumn].item()

		# print results
		console('## roiname: %s'%(roiname),'blue')
		console('## roilabel: %s'%(roilabel),'green')
		console('## roinumber: %s'%(roinumber),'green')

		return metadata, roiname, roilabel

	def create_contours(self, image, imagename, roiname):
		"""[summary]

		Parameters
		----------
		image : [type]
			[description]
		imagename : [type]
			[description]
		roiname : [type]
			[description]

		Returns
		-------
		[type]
			[description]

		Raises
		------
		Exception
			[description]
		Exception
			[description]
		"""
		#----find contour
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
			self.l_error.append(_err)
			raise Exception('%s; %s; %s'%(_err[0],_err[1],_err[2]))

		#------------------------------------------------------------------------for each layer: save images and contours
		#when saving the contours below, only one drawContours function from above can be run
		#any other drawContours function will overlay on the others if multiple functions are run
		#----param
		color = (0,0,255)

		#----straight bounding box
		if self.shape == 'straight':
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
		elif self.shape == 'rotate':
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
		elif self.shape == 'circle':
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
		elif self.shape == 'polygon':
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
		elif self.shape == 'hull':
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

		return _bounds, _contours

	def create_rois(self, imagename, roiname, roilabel, roinumber, color_roi, _bounds, _contours):
		"""[summary]

		Parameters
		----------
		imagename : [type]
			[description]
		roiname : [type]
			[description]
		roilabel : [type]
			[description]
		roinumber : [type]
			[description]
		color_roi : [type]
			[description]
		_bounds : [type]
			[description]
		_contours : [type]
			[description]

		Returns
		-------
		[type]
			[description]
		[type]
			[description]
		"""
		#----store bounds as df
		_bounds = pd.DataFrame(_bounds)
		# transpose bounds (x0, x1, y0, y1)
		_x = _bounds[0].unique().tolist()
		_y = _bounds[1].unique().tolist()
		bounds = pd.DataFrame(np.column_stack([_x[0],_y[0],_x[1],_y[1]]))
		#rename
		bounds.columns = ['x0','y0','x1','y1']
		# add index, image, roi, and shape
		bounds['shape'] = self.shape
		bounds['shape_d'] = self.shape_d
		bounds['image'] = imagename
		bounds[self.roicolumn] = roilabel
		bounds['id'] = roinumber
		bounds['color'] = color_roi

		# clean-up
		## arrange
		bounds = bounds[['image','shape','shape_d','id','x0','y0','x1','y1',self.roicolumn,'color']]
		## convert to int
		bounds[['x0','y0','x1','y1']] = bounds[['x0','y0','x1','y1']].astype(int)
		# append to list of df

		#----store contours as df
		contours = ''
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
				# _image = self.layer.topil()
				# center and resize image to template screen
				# _background = Image.new("RGBA", (screensize[0], screensize[1]), (0, 0, 0, 0))
				# _background.paste(layer_image, layer_offset)
				# _arr = np.array(_background)
				# ax.imshow(_arr, zorder=2, interpolation='bilinear', alpha=1)
				## contours
				_arr = cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB)
				ax.imshow(_arr, zorder=1, interpolation='bilinear', alpha=1)
				## check if path exists
				_folder = '%s/roi/contours/final/%s'%(self.output_path, self.shape)
				if not os.path.exists(_folder):
					os.makedirs(_folder)
				## save
				plt.savefig('%s/%s_%s_source.png'%(_folder, imagename, roiname), dpi=self.dpi)
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
				_folder = '%s/roi/contours/debug/%s'%(self.output_path, self.shape)
				if not os.path.exists(_folder):
					os.makedirs(_folder)
				## save
				plt.savefig('%s/%s_%s_source.png'%(_folder, imagename, roiname), dpi=self.dpi)
				plt.close()

				# recreated from dataframe countours
				#!!!Todo:get working
				#plt.imshow(cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB))
				#plt.savefig('%s/roi/contours/%s/%s_%s_recreated.png'%(output_path, shape, imagename, roiname), dpi=dpi)
				## close plt.cla() #plt.clf() #plt.close()
				plt.close()

			#----save roi df
			if self.save['data']:
				# check if path exists
				_folder = '%s/roi/data/'%(self.output_path)
				if not os.path.exists(_folder):
					os.makedirs(_folder)
				# export to csv or dataviewer
				if self.f_roi == 'raw':
					bounds.to_csv("%s/%s_%s_bounds.csv"%(_folder, imagename, roiname), index=False)
				elif self.f_roi == 'dataviewer':
					_bounds = '\n'.join(map(str, [
						"# EyeLink Interest Area Set created on %s."%(now()),
						"# Interest area set file using mdl.roi.ROI()",
						"# columns: RECTANGLE | IA number | x0 | y0 | x1 | y1 | label | color",
						"# columns: ELLIPSE | IA number | x0 | y0 | x1 | y1 | label | color",
						"# columns: FREEHAND | IA number | x0,y0 | x1,y1 | x2,y2 | x3,y3 | label | color",
						"# example: RECTANGLE 1 350 172 627 286 leftcheek red",
						"# example: ELLIPSE 2 350 172 627 286 leftcheek red",
						"# example: FREEHAND 3 350,172 627,172 627,286 350,286 leftcheek red",
						"# See Section 5.10.1 of Eyelink DataViewer Users Manual (3.2.1) for more information.",
						bounds[['shape_d','id','x0','y0','x1','y1',self.roicolumn,'color']].to_csv(index=False, header=False).replace(',', '	')
					]))
					## create ias file
					_filename = "%s/%s_%s_bounds"%(_folder, imagename, roiname)
					with open("%s.ias"%(_filename), "w") as file:
						file.write(_bounds)
				# coordinates
				#contours.to_csv("%s/roi/data/%s_%s_bounds.csv"%(output_path, imagename, roiname), index=False)

			# finish
			return bounds, contours

	def process(self):
		"""[summary]

		Returns
		-------
		[type]
			[description]
		"""
		#----for each image
		print(self.image_path)
		console('for each image','green')
		for file in self.directory:
			#----start image
			# read image
			psd = PSDImage.open(file)
			imagename = os.path.splitext(os.path.basename(file))[0]

			# file metadata
			#filename = '%s.png'%(imagename)
			#channels = psd.channels #read channels
			#width = psd.width #width and height
			#height = psd.height

			# clear lists
			self.l_bounds = []
			self.l_contours = []

			#!!!----for each region of interest
			console('\n# file: %s'%(imagename),'blue')
			roinumber = 1
			color_roi = ['cyan','magenta','yellow','orange','blue','green','red']
			for layer in psd:
				#skip if layer is main image
				if Path(layer.name).stem == imagename:
					continue
				else:
					#----start roi
					# set roi color
					color_roi = secrets.choice(color_roi)
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

					# process metadata
					metadata, roiname, roilabel = self.process_metadata(imagename, layer, roinumber)

					# contours
					_bounds, _contours = self.create_contours(image, imagename, roiname)

					# bounds
					bounds, contours = self.create_rois(imagename, roilabel, roinumber, color_roi, _bounds, _contours)

					# store processed bounds and contours to combine across image
					self.l_bounds.append(bounds)
					self.l_contours.append(contours)

			#!!!----save all region of interest for an image together
			if ((self.save['level'] == 'both') or (self.save['level'] == 'stimulus')):
				#----save all roi image
				if self.save['raw']:
					# center and resize image to template screen
					_image = psd.topil()
					_background = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
					_offset = ((self.screensize[0] - _image.size[0])//2,(self.screensize[1] - _image.size[1])//2)
					_background.paste(_image, _offset)
					plt.imshow(np.array(_background))
					plt.savefig('%s/stim/raw/%s.png'%(self.output_path, imagename), dpi=self.dpi)
					plt.close()

				#----save data
				#bounds
				df = pd.concat(self.l_bounds)
				## sort by image, id values
				df = df.sort_values(by=['image','id'])
				## store for single bounds across all images
				self.l_bounds_all.append(df)
				## export to csv or dataviewer
				_folder = '%s/stim/data/'%(self.output_path)
				if self.f_roi == 'raw':
					df.to_csv("%s/%s_bounds.csv"%(_folder, imagename), index=False)
				elif self.f_roi == 'dataviewer':
					_bounds = '\n'.join(map(str, [
						"# EyeLink Interest Area Set created on %s."%(now()),
						"# Interest area set file using mdl.roi.ROI()",
						"# columns: RECTANGLE | IA number | x0 | y0 | x1 | y1 | label | color",
						"# columns: ELLIPSE | IA number | x0 | y0 | x1 | y1 | label | color",
						"# columns: FREEHAND | IA number | x0,y0 | x1,y1 | x2,y2 | x3,y3 | label | color",
						"# example: RECTANGLE 1 350 172 627 286 leftcheek red",
						"# example: ELLIPSE 2 350 172 627 286 leftcheek red",
						"# example: FREEHAND 3 350,172 627,172 627,286 350,286 leftcheek red",
						"# See Section 5.10.1 of Eyelink DataViewer Users Manual (3.2.1) for more information.",
						df[['shape_d','id','x0','y0','x1','y1',self.roicolumn,'color']].to_csv(index=False, header=False).replace(',', '	')
					]))
					## create ias file
					_filename = "%s/%s_bounds"%(_folder, imagename)
					with open("%s.ias"%(_filename), "w") as file:
						file.write(_bounds)

				#coord
				# df = pd.concat(l_roi_contours)
				# df.to_csv("%s/stim/data/%s_coord.csv"%(output_path, imagename), index=False)

				#----finish
				plt.cla(); plt.clf(); plt.close(); gc.collect()

		#!!!----for all images
		# save all region of interest as single file
		if ((self.save['level'] == 'both') or (self.save['level'] == 'stimulus')):
			#----save bounds data
			df = pd.concat(self.l_bounds_all)
			# sort by image,id
			df = df.sort_values(by=['image','id'])
			# export to csv or dataviewer
			_folder = '%s/stim/data/'%(self.output_path)
			if self.f_roi == 'raw':
				df.to_csv("%s/%s_bounds.csv"%(_folder, imagename), index=False)
			elif self.f_roi == 'dataviewer':
				_bounds = '\n'.join(map(str, [
					"# EyeLink Interest Area Set created on %s."%(now()),
					"# Interest area set file using mdl.roi.ROI()",
					"# columns: RECTANGLE | IA number | x0 | y0 | x1 | y1 | label | color",
					"# columns: ELLIPSE | IA number | x0 | y0 | x1 | y1 | label | color",
					"# columns: FREEHAND | IA number | x0,y0 | x1,y1 | x2,y2 | x3,y3 | label | color",
					"# example: RECTANGLE 1 350 172 627 286 leftcheek red",
					"# example: ELLIPSE 2 350 172 627 286 leftcheek red",
					"# example: FREEHAND 3 350,172 627,172 627,286 350,286 leftcheek red",
					"# See Section 5.10.1 of Eyelink DataViewer Users Manual (3.2.1) for more information.",
					df[['shape_d','id','x0','y0','x1','y1',self.roicolumn,'color']].to_csv(index=False, header=False).replace(',', '	')
				]))
				# create ias file
				_filename = "%s/%s_bounds"%(_folder, imagename)
				with open("%s.ias"%(_filename), "w") as file:
					file.write(_bounds)

		#!!!----error log
		if bool(self.l_error):
			_filename = Path('%s/error.csv'%(self.output_path))
			console("Errors found. See log %s"%(_filename), 'red')
			error = pd.DataFrame(self.l_error, columns=['image','roi','message'])
			error.to_csv(_filename, index=False)
		else:
			error = ''

		#----finished
		return df, error




#%% test
# drawing image
# img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image',img)

# convert img to np array
# np_img = np.array(img)
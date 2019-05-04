#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Create regions of interest that can be used for data processing and analysis.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
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
	"""Generate region of interest to be read by Eyelink DataViewer or statistical tool."""
	def __init__(self, isMultiprocessing=False, image_path=None, output_path=None, metadata_source=None, 
			  roi_format='both', shape='box', roicolumn='roi', uuid=None, **kwargs):
		"""
		Generate region of interest to be read by Eyelink DataViewer or statistical tool.

		Parameters
		----------
		isMultiprocessing : :obj:`bool`
			Should the rois be generated using multiprocessing. Default `False`.
		detection : :obj:`string`
			How should the regions of interest be detected. Either manually, through the use of highlight layers, or automatically
			using haar cascades opencv. Default `manual`.
		image_path : :obj:`str`
			Image directory path.
		output_path : :class:`str`
			Path to save data.
		roi_format : :obj:`str` {`raw`,`dataviewer`, `both`}
			Format to export ROIs. Either to 'csv' (`raw`) or to Eyelink DataViewer 'ias' (`dataviewer`) or both (`both`). 
			Default is `raw`. Note: If :code:`roi_format` = `dataviewer`, :code:`shape` must be either be `circle`, `rotate`, or `straight`.
		metadata_source : :class:`str` or :obj:`None`
			Metadata source. If metadata is being read from a spreadsheet, :code:`metadata_source` should be equal to path the to
			the metadata file, else if metadata is embed within the image as a layer name, :code:`metadata_source` = `embedded`.
			Default is `embedded`. For example:
				>>> # if metadata is in PSD images
				>>> metadata = 'embedded'
				>>> # if metadata is an external xlsx file.
				>>> metadata = 'roi/metadata.xlsx'
			Although Photoshop PSD don't directly provide support for metadata. However if each region of interest is stored
			as a seperate layer within a PSD, the layer name can be used to store metadata. To do this, the layer name has
			to be written as delimited text. Our code can read this data and extract relevant metadata. The delimiter can
			be either `;` `,` `|` `\\t` or `\\s` (Delimiter type must be identified when running this code using the
			code:`delimiter` parameter. The default is `;`.). Here's an example using `;` as a delimiter:
				>>> imagename=BM001;roiname=1;feature=lefteye
			Note: whitespace should be avoided from from each layer name. Whitespaces may cause errors during parsing.
		shape : :obj:`str` {`polygon`, `hull`, `circle`, `rotate`, `straight`}
			Shape of machine readable boundaries for region of interest. Default is `straight`. `polygon` creates a Contour
			Approximation and will most closely match the orginal shape of the roi. `hull` creates a Convex Hull, which
			is similar to but not as complex as a Contour Approximation and will include bulges for areas that are convex.
			`circle` creates a mininum enclosing circle. Finally, both `rotate` and `straight` create a Bounding Rectangle,
			with the only difference being compensation for the mininum enclosing area for the box when using `rotate`.
		roicolumn : :obj:`str`
			The name of the label for the region of interest in your metadata. For example you may want to extract the column
			'feature' from your metadata and use this as the label. Default is `roi`.
		uuid : :obj:`list` or :obj:`None`
			Create a unique id by combining a list of existing variables in the metadata. This is recommended
			if :code:`roi_format` == `dataviewer` because of the limited variables allowed for ias files. Default :obj:`None`.
		**kwargs : :obj:`str` or :obj:`None`, optional
			Additional properties. Here's a list of available properties:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **cores** : :class:`bool`
				  - (if :code:`isMultiprocessing` == `True`) Number of cores to use. Default is total available cores - 1.
				* - **isLibrary** : :class:`bool`
				  - Check if required packages have been installed. Default is :obj:`False`.
				* - **isDebug** : :class:`bool`
				  - Allow flags to be visible. Default is :obj:`False`.
				* - **save_data** : :class:`bool`
				  - Save coordinates. Default is :obj:`True.`
				* - **newcolumn** : :class:`dict` {:obj:`str`, :obj:`str`} or :obj:`False`
				  - Add additional column to metadata. This must be in the form of a dict in this form {key: value}. 
					Default is :obj:`False.`
				* - **save_raw_image** : :class:`bool`
				  - Save images. Default is True.
				* - **save_contour_image** : :class:`bool`
				  - Save generated contours as images. Default is :obj:`True`.
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
		retval, threshold : :obj:`numpy.ndarray`
			Returns from :ref:`cv2.threshold`. The function applies a fixed-level thresholding to a multiple-channel array.
			`retval` provides an optimal threshold only if :ref:`cv2.THRESH_OTSU` is passed. `threshold` is an image after applying
			a binary threshold (:ref:`cv2.THRESH_BINARY`) removing all greyscale pixels < 127. The output matches the same image
			channel as the original image.
			See `opencv <https://docs.opencv.org/4.0.1/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57>`_ and
			`leanopencv <https://www.learnopencv.com/opencv-threshold-python-cpp>`_ for more information.
		contours, hierarchy : :obj:`numpy.ndarray`
			Returns from :ref:`cv2.findContours`. This function returns contours from the provided binary image (threshold).
			This is used here for later shape detection. `contours` are the detected contours, while hierarchy containing
			information about the image topology.
			See `opencv <https://docs.opencv.org/4.0.1/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e07>`_
			for more information.
		image_contours : :obj:`numpy.ndarray`
			Returns from :ref:`cv2.drawContours`. This draws filled contours from the image.
		image_contours : :obj:`numpy.ndarray`
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
		# check debug
		self.isDebug = kwargs['isDebug'] if 'isDebug' in kwargs else False

		# check library
		self.isLibrary = kwargs['isLibrary'] if 'isLibrary' in kwargs else False
		if self.isLibrary:
			settings.library(__required__)

		#----parameters
		# multiprocessing
		self.isMultiprocessing = isMultiprocessing
		self.cores = kwargs['cores'] if 'cores' in kwargs else 'max'
		# how to read data
		self.metadata_source = kwargs['metadata_source'] if 'metadata_source' in kwargs else 'embed'
		# how to format rois
		self.roi_format = roi_format
		# delimiter
		self.delimiter = kwargs['delimiter'] if 'delimiter' in kwargs else ';'
		# screensize
		self.screensize = kwargs['screensize'] if 'screensize' in kwargs else [1920, 1080]
		# scale
		self.scale = kwargs['scale'] if 'scale' in kwargs else 1
		# coordinates
		cx = self.screensize[0]/2
		cy = self.screensize[1]/2
		self.coordinates = kwargs['coordinates'] if 'coordinates' in kwargs else [cx, cy]
		# shape
		self.shape = shape if shape in ['polygon', 'hull', 'circle', 'rotate', 'straight'] else 'straight'
		self.shape_d = None #dataviewer shape
		# uuid
		self.uuid = uuid
		# label
		self.roicolumn = roicolumn
		# add column
		self.newcolumn = kwargs['newcolumn'] if 'newcolumn' in kwargs else None
		# dpi
		self.dpi =  kwargs['dpi'] if 'dpi' in kwargs else 300
		# save
		self.save = {}
		# save csv
		self.save['data'] = kwargs['save_data'] if 'save_data' in kwargs else True
		# save contour images
		self.save['contours'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save raw images
		self.save['raw'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
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
		if (self.shape in ['polygon', 'hull']) and (self.roi_format == "dataviewer"):
			raise Exception ("Cannot use shape %s when exporting for DataViewer. \
					Please use either 'circle', 'rotate', or 'straight' instead, or set roi_format == 'raw'."%(shape))

		#----directory
		self.directory = [x for x in Path(self.image_path).glob("*.psd") if x.is_file()]

		#----read metadata file (if metadata is not None)
		if metadata_source is not "embedded":
			self.metadata_source = metadata_source
			_type = Path(self.metadata_source).suffix
			if _type == ".csv": self.metadata_all = pd.read_csv(self.metadata_source)
			elif _type == ".xlsx": self.metadata_all = pd.read_excel(self.metadata_source)

			# check if metadata is empty
			if self.metadata_all.empty:
				raise Exception('No data for file: %s'%(self.metadata_source))

	def process_metadata(self, imagename, layer):
		"""[summary]

		Parameters
		----------
		imagename : [type]
			[description]
		layer : [type]
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
		if self.metadata_source == 'embedded':
			metadata = pd.DataFrame(data=(item.split("=") for item in layer.name.split(self.delimiter)),columns=['key','value'])
			metadata.set_index('key', inplace=True)
			metadata.loc['name']['value'] = metadata.loc['name']['value'].replace("roi","")
			roiname = metadata.loc['name']['value']
			roilabel = metadata.loc[self.roicolumn]['value']

		# else read metadata from file
		else:
			# get metadata
			roiname = layer.name.strip(' \t\n\r') # strip whitespace
			metadata = self.metadata_all.loc[(self.metadata_all['image'] == imagename) & (self.metadata_all['roi'] == roiname)]
			# if datafame empty
			if metadata.empty:
				message = 'No data for %s:%s (image:roi).'%(imagename, roiname)
				raise Exception(message)
			else:
				roilabel = metadata[self.roicolumn].item()

		# print results
		if self.isDebug:
			console('## roiname: %s'%(roiname),'blue')
			console('## roilabel: %s'%(roilabel),'green')

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
		#----convert to np array
		image = np.array(image)

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
			raise Exception('%s; %s; %s'%(_err[0],_err[1],_err[2]))

		#------------------------------------------------------------------------for each layer: save images and contours
		#when saving the contours below, only one drawContours function from above can be run
		#any other drawContours function will overlay on the others if multiple functions are run
		#----param
		color = (0,0,255)

		#----straight bounding box
		if self.shape == 'straight':
			# console('## roishape: straight bounding box','green')
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
			# console('## roishape: rotated bounding box','green')
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
			# console('## roishape: bounding circle','green')
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
			# console('## roishape: approximate polygon','green')
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
			# console('## roishape: hull','green')
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

		#----no shape chosen
		else:
			raise Exception('Please select either straight, rotate, circle, polygon, box, or hull shape.')

		return _bounds, _contours

	def create_rois(self, imagename, metadata, roiname, roilabel, roinumber, _bounds, _contours):
		"""[summary]

		Parameters
		----------
		imagename : [type]
			[description]
		metadata : [type]
			[description]
		roiname : [type]
			[description]
		roinumber : [type]
			[description]
		roilabel : [type]
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

		Raises
		------
		Exception
			[description]
		"""
		#----store bounds as df
		_bounds = pd.DataFrame(_bounds)

		# transpose bounds (x0, y0, x1, y1)
		_x = _bounds[0].unique().tolist()
		_y = _bounds[1].unique().tolist()

		# check if bounding box has two x and y coordinate pairs
		if (((len(_x) == 1) or (len(_y) == 1)) and self.shape == 'straight'):
			raise Exception ("Error creating bounding box for image:roi %s:%s."%(imagename, roiname))

		# set as df
		bounds = pd.DataFrame(np.column_stack([_x[0],_y[0],_x[1],_y[1]]))

		# rename
		bounds.columns = ['x0','y0','x1','y1']

		# add index, image, roi, and shape
		bounds['image'] = imagename
		bounds['roi'] = roiname
		bounds['id'] = roinumber
		bounds['shape_d'] = self.shape_d

		# clean-up
		## convert to int
		bounds[['x0','y0','x1','y1']] = bounds[['x0','y0','x1','y1']].astype(int)

		#----store contours as df
		contours = ''

		#----save image:roi level image bounds and coordinates
		#----save roi contours
		if self.save['contours']:
			#----generated rois (using contours)
			# create matplotlib plot
			fig, ax = plt.subplots()
			fig.canvas.flush_events()

			#----load image directly from PSD
			# contours
			_arr = cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB)
			ax.imshow(_arr, zorder=1, interpolation='bilinear', alpha=1)

			# save generated rois (using contours)
			_folder = '%s/img/roi/generated/%s'%(self.output_path, self.shape)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## save
			plt.savefig('%s/%s_%s_source.png'%(_folder, imagename, roiname), dpi=self.dpi)
			plt.cla(); plt.clf(); plt.close()

			#----recreated from dataframe bounds (this is to debug for potential issues)
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

			# save rois (debugging for issues)
			_folder = '%s/img/roi/debug/%s'%(self.output_path, self.shape)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## save
			plt.savefig('%s/%s_%s_source.png'%(_folder, imagename, roiname), dpi=self.dpi)
			plt.cla(); plt.clf(); plt.close()

		#----save roi df
		# combine metadata with bounds
		if metadata is not None:
			bounds = pd.merge(bounds, metadata, on=['image','roi'], how='outer')

		# combine metadata with coordinates
		##!!! get working

		# finish
		return bounds, contours

	def export_data(self, df, path, filename, uuid=None, newcolumn=None):
		"""[summary]

		Parameters
		----------
		df : [type]
			Bounds.
		path : [type]
			[description]
		filename : [type]
			[description]
		uuid : [type], optional
			[description], by default None
		newcolumn : [type], optional
			[description], by default None

		Returns
		-------
		[type]
			[description]
		"""
		# if new column is not None
		if isinstance(newcolumn, (dict,)):
			df[list(newcolumn.keys())[0]] = list(newcolumn.values())[0]

			## add new column to uuid, only if uuid exists
			if isinstance(uuid, (list,)):
				uuid.append(list(newcolumn.values())[0])

		# if uuid, create a unique column
		if isinstance(uuid, (list,)):
			df['uuid'] = df[uuid].apply(lambda x: ''.join(x), axis=1)
			uuid_column = 'uuid'
		# else simply use roiname
		else:
			uuid_column = self.roicolumn

		# check if folder exists
		if not os.path.exists(path):
			os.makedirs(path)

		# export to excel
		if ((self.roi_format == 'raw') or (self.roi_format == 'both')):
			df.to_csv("%s/%s.csv"%(path, filename), index=False)

			# if debug
			if self.isDebug: console("## excel file saved @: %s/%s.ias"%(path, filename),'green')

		# export to ias (dataviewer)
		if ((self.roi_format == 'dataviewer') or (self.roi_format == 'both')):
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
				df[['shape_d','id','x0','y0','x1','y1',uuid_column]].to_csv(index=False, header=False).replace(',', '	')
			]))
			# save to ias
			with open("%s/%s.ias"%(path, filename), "w") as file:
				file.write(_bounds)

			# if debug
			if self.isDebug: console("## ias file saved @: %s/%s.ias"%(path, filename),'green')

		return df

	def process_image(self, psd):
		"""[summary]

		Parameters
		----------
		psd : [type]
			[description]
		path : [type]
			[description]
		filename : [type]
			[description]

		Returns
		-------
		[type]
			[description]
		"""
		## load image directly from PSD
		image = psd.topil()

		# scale image
		if self.scale != 1:
			_truesize = [image.size[0], image.size[1]]
			_scalesize = [int(_truesize[0] * self.scale), int(_truesize[1] * self.scale)]
			image = image.resize(_scalesize, Image.ANTIALIAS)
			if self.isDebug: 
				console('# export image','blue')
				console('size: %s, scaled: %s'%(_truesize, _scalesize),'green')

		# center and resize image to template screen
		_background = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
		_offset = ((self.screensize[0] - image.size[0])//2,(self.screensize[1] - image.size[1])//2)
		_background.paste(image, _offset)

		return image

	def run(self, directory, core=0):
		"""[summary]

		Parameters
		----------
		directory : :class:`list`
			[description]
		core : :class:`int`
			(if isMultprocessing) Core used for this function. Default `0`.

		Returns
		-------
		[type]
			[description]
		"""
		#----print
		console('core: %s'%(core),'orange')
		console('for each image','green')

		#----prepare lists for all images
		l_bounds_all = []
		l_contours_all = []
		l_error = []

		#!!!----for each image
		for file in directory:
			#----start
			# read image
			psd = PSDImage.open(file)
			imagename = os.path.splitext(os.path.basename(file))[0]
			if self.isDebug: console('\n# file: %s'%(imagename),'blue')

			# clear lists
			l_bounds = []
			l_contours = []

			#!!!----for each image, save image file
			if self.save['raw']:
				# process imaage
				image = self.process_image(psd=psd)
				# check folder
				_folder = '%s/img/img/'%(self.output_path)
				if not os.path.exists(_folder):
					os.makedirs(_folder)
				## save
				plt.imshow(np.array(image))
				plt.savefig('%s/%s.png'%(_folder, imagename), dpi=self.dpi)
				plt.cla(); plt.clf(); plt.close(); del image

			#!!!----for each region of interest
			roinumber = 1
			for layer in psd:
				# skip if layer is main image
				if Path(layer.name).stem == imagename:
					continue
				else:
					# process metadata
					metadata, roiname, roilabel = self.process_metadata(imagename, layer)

					# process image
					image = self.process_image(layer)

					# create contours
					_bounds, _contours = self.create_contours(image, imagename, roiname)

					# create rois
					bounds, contours = self.create_rois(imagename, metadata, roiname, roilabel, roinumber, _bounds, _contours)

					# store processed bounds and contours to combine across image
					l_bounds.append(bounds)
					l_contours.append(contours)

					# update counter
					roinumber = roinumber + 1

			#!!!----for each image, export data
			# concatinate bounds
			df = pd.concat(l_bounds)
			## store for single bounds across all images (if multiProcessing, this is 1/num of cores)
			l_bounds_all.append(df)
			## export data
			_filename = "%s_bounds"%(imagename)
			_folder = '%s/data/img/'%(self.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			df = self.export_data(df=df, path=_folder, filename=_filename, uuid=self.uuid, newcolumn=self.newcolumn)

			# contours
			##!!! create roi file for complex shapes (not with dataviewer)

		#----finished
		console('finished run()','purple')
		return l_bounds_all, l_contours_all, l_error

	def process(self):
		"""[summary]

		Returns
		-------
		[type]
			[description]
		"""
		# prepare arguements and procedure
		arg = []
		proc = ''
		df = ''
		error = ''
		# if multiprocessing, get total cores
		if self.isMultiprocessing:
			import multiprocessing

			#----get number of available cores
			_max = multiprocessing.cpu_count() - 1

			#---check if selected max or value above possible cores
			if (self.cores == 'max') or (self.cores >= _max):
				self.cores = _max
			else:
				self.cores = self.cores

			#----double check multiproessing
			# if requested cores is 0 or 1, run without multiprocessing
			if ((self.cores == 0) or (self.cores == 1)):
				self.isMultiprocessing = False
				console('not multiprocessing', 'purple')
			# split directory by number of cores
			else:
				self.isMultiprocessing = True
				l_directory = np.array_split(self.directory, self.cores)
				console('multiprocessing with %s cores'%(self.cores), 'purple')

		# not multiprocessing
		else:
			self.isMultiprocessing = False
			console('not multiprocessing', 'purple')

		#----prepare to run
		# if not multiprocessing
		if not self.isMultiprocessing:
			l_bounds_all = self.run(self.directory)

			# finish
			if self.isDebug: console('running finished() (not-multiprocessing)','purple')
			df, error = self.finished(l_bounds_all)

		# else if multiprocessing
		else:
			# collect each pipe (this is used to build send and recieve portions of output)
			queue = multiprocessing.Queue()

			# prepare threads
			process = [multiprocessing.Process(target=self.run, args=(l_directory[x].tolist(), x)) for x in range(self.cores)]

            # start each thread
			for p in process:
				p.daemon = True
				p.start()

			# return pipes
            # note: see https://stackoverflow.com/a/45829852
			returns = []
			for p in process:
				returns.append(queue.get())

			# wait for each process to finish
			for p in process:
				p.join()

			#----after running
			if self.isDebug: console('running finished() (multiprocessing)','purple')
			df, error = self.finished(returns)

		return df, error

	def finished(self, df, errors=None):
		"""
		Process bounds for all images.

		Parameters
		----------
		df : [type]
			[description]
		errors : [type], optional
			[description], by default None
		"""
		console('start finished()','purple')
		# if multiprocessing, combine data from each thread
		if self.isMultiprocessing:
			#----concatinate data
			df = pd.concat(df)

		#!!!----combine all rois across images
		# export to csv or dataviewer
		_folder = '%s/'%(self.output_path)
		_filename = "bounds"
		df = self.export_data(df=df, path=_folder, filename=_filename, uuid=self.uuid)

		#!!!----error log
		if bool(errors):
			_filename = Path('%s/error.csv'%(self.output_path))
			console("Errors found. See log %s"%(_filename), 'red')
			error = pd.DataFrame(errors, columns=['image','roi','message'])
			error.to_csv(_filename, index=False)
		else:
			error = ''

		return df, error

#%% test
# drawing image
# img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image',img)

# convert img to np array
# np_img = np.array(img)
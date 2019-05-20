#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Generate regions of interest that can be used for data processing and analysis.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""
# allowed imports
__all__ = ['ROI']

# required external libraries
__required__ = ['opencv-python','psd-tools','matplotlib','Pillow']

# local
from .. import settings

# check if psd_tools and cv2 is available
try:
	# required for init
	from pdb import set_trace as breakpoint
	import os
	from pathlib import Path
	import pandas as pd
	import numpy as np
	import random
	# plot
	from PIL import Image
	import matplotlib
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	import matplotlib.patches as patches	
	# import photoshop
	import psd_tools	
	# math
	import cv2	
except ImportError as e:
	pkg = e.name
	x = {'cv2':'opencv-python', 'psd_tools':'psd-tools'}
	pkg = x[pkg] if pkg in x else pkg
	raise Exception("No module named '%s'. Please install from PyPI before contiuing."%(pkg),'red')

class ROI():
	"""Generate regions of interest that can be used for data processing and analysis."""
	def __init__(self, isMultiprocessing=False, detection='manual', image_path=None, output_path=None, metadata_source=None, 
			  roi_format='both', shape='box', roicolumn='roi', uuid=None, **kwargs):
		"""Generate regions of interest that can be used for data processing and analysis.

		Parameters
		----------
		isMultiprocessing : :obj:`bool`
			Should the rois be generated using multiprocessing. Default `False`.
		detection : :obj:`str` {'manual', 'haarcascade'}
			How should the regions of interest be detected. Either manually (`manual`), through the use of highlighting layers in photo-editing
			software, or automatically through feature detection using `haarcascade` classifers from opencv. Default `manual`.
		image_path : :obj:`str`
			Image directory path.
		output_path : :class:`str`
			Path to save data.
		roi_format : :obj:`str` {'raw', 'dataviewer', 'both'}
			Format to export ROIs. Either to 'csv' (`raw`) or to Eyelink DataViewer 'ias' (`dataviewer`) or both (`both`).
			Default is `both`. Note: If :code:`roi_format` = `dataviewer`, :code:`shape` must be either be `circle`, `rotate`, or `straight`.
		metadata_source : :class:`str` or :obj:`None` {'path', 'embedded'}
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
				>>> imagename = "BM001"; roiname = 1; feature = "lefteye"
			Note: whitespace should be avoided from from each layer name. Whitespaces may cause errors during parsing.
		shape : :obj:`str` {'polygon', 'hull', 'circle', 'rotate', 'straight'}
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
				* - **isDemo** : :class:`bool`
				  - Tests code with in-house images and metadata. Default is :obj:`False`.
				* - **save_data** : :class:`bool`
				  - Save coordinates. Default is :obj:`True.`
				* - **newcolumn** : :obj:`dict` {:obj:`str`, :obj:`str`} or :obj:`False`
				  - Add additional column to metadata. This must be in the form of a dict in this form {key: value}. Default is :obj:`False.`
				* - **save_raw_image** : :class:`bool`
				  - Save images. Default is True.
				* - **save_contour_image** : :class:`bool`
				  - Save generated contours as images. Default is :obj:`True`.
				* - **delimiter** : :class:`str` {';' , ',' , '|' , 'tab' , 'space'}
				  - (if :code:`source` == `psd`) How is metadata delimited. Default is `;`.
				* - **classifier** : :obj:`str` {'eye_tree_eyeglasses','eye','frontalface_alt_tree','frontalface_alt','frontalface_alt2',
				    'frontalface_default','fullbody','lowerbody','profileface','smile','upperbody'}
				  - (if :code:`detection` == `haarcascade`) Type of trained classifier to use. Default 'frontalface_default'.
				* - **classScaleFactor** : :obj:`float`
				  - Parameter specifying how much the image size is reduced at each image scale.
				* - **classMinNeighbors** : :obj:`float`
				  - Parameter specifying how many neighbors each candidate rectangle should have to retain it.
				* - **classMinSize** : :obj:`tuple`
				  - Minimum possible object size. Objects smaller than that are ignored.
				* - **screensize** : :class:`list` [:obj:`int`]
				  - Monitor size is being presented. Default is `[1920, 1080]`.
				* - **scale** : :class:`int`
				  - If image is scaled during presentation, set scale. Default is 1.
				* - **offset** : :class:`list` [:obj:`int`]
				  - Center point of image, relative to screensize. Default is `[960, 540]`.
				* - **dpi** : :class:`int` or :obj:`None`
				  - (if :code:`save_image` == `True`) Quality of exported images, refers to 'dots per inch'. Default is `300`.
				* - **remove_axis** : :class:`bool`
				  - Remove axis from :obj:`matplotlib.pyplot`. Default is `False`.
				* - **tight_layout** : :class:`bool`
				  - Remove whitespace from :obj:`matplotlib.pyplot`. Default is `False`.
				* - **set_size_inches** : :class:`bool`
				  - Set size of :obj:`matplotlib.pyplot` according to screensize of ROI. Default is `False`.
				* - **image_backend** : :class:`str` {'matplotlib','PIL'}
				  - Backend for exporting image. Either `'matplotlib' <https://matplotlib.org/index.html>`__ or `'PIL' <https://pillow.readthedocs.io/en/stable/>`__. Default 'matplotlib'.

		Attributes
		----------
		shape_d : :class:`str` {'ELLIPSE', 'FREEHAND', 'RECTANGLE'}
			DataViewer ROI shape.
		psd :  `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`__
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

		Raises
		------
		Exception
			[description]
		Exception
			[description]

		Examples
		--------
		.. code-block:: python

			>>> from imhr.roi import ROI
			>>> s = "/dist/example/raw/"; d="/dist/example/"
			>>> ROI(source=s, output_path=d, shape='box')

		Notes
		-----
		Resources
			- See https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html for more information about each shape.
			- See https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html for more information about how images are drawn.
			- See https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html to understand how bounds are created.
		"""
		# get console and time
		self.console = settings.console
		self.now = settings.time

		# check debug
		self.isDebug = kwargs['isDebug'] if 'isDebug' in kwargs else False

		# check library
		self.isLibrary = kwargs['isLibrary'] if 'isLibrary' in kwargs else False
		if self.isLibrary:
			settings.library(__required__)

		#----parameters
		self.detection = detection
		# demo
		self.isDemo = kwargs['isDemo'] if 'isDemo' in kwargs else False
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
		# offset image coordinates
		cx = self.screensize[0]/2
		cy = self.screensize[1]/2
		self.recenter = kwargs['recenter'] if 'recenter' in kwargs else [cx, cy]
		if self.recenter is not [cx, cy]:
			self.newoffset = True
		else:
			self.newoffset = False
		# shape
		self.shape = shape if shape in ['polygon', 'hull', 'circle', 'rotate', 'straight'] else 'straight'
		self.shape_d = None #dataviewer shape
		# uuid
		self.uuid = uuid
		# label
		self.roicolumn = roicolumn
		# add column
		self.newcolumn = kwargs['newcolumn'] if 'newcolumn' in kwargs else None
		# save
		self.save = {}
		# save csv
		self.save['data'] = kwargs['save_data'] if 'save_data' in kwargs else True
		# save contour images
		self.save['contours'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save raw images
		self.save['raw'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True

		#-----matplotlib
		self.dpi =  kwargs['dpi'] if 'dpi' in kwargs else 300
		self.remove_axis = kwargs['remove_axis'] if 'remove_axis' in kwargs else False
		self.tight_layout = kwargs['tight_layout'] if 'tight_layout' in kwargs else False
		self.set_size_inches = kwargs['set_size_inches'] if 'set_size_inches' in kwargs else False
		self.image_backend = kwargs['image_backend'] if 'image_backend' in kwargs else 'matplotlib'
		if self.remove_axis: plt.rcParams.update({'axes.titlesize':0, 'axes.labelsize':0, 'xtick.labelsize':0, 'ytick.labelsize':0, 'savefig.pad_inches':0, 'font.size': 0})
		#-----classifiers
		self.classifier = kwargs['classifier'] if 'classifier' in kwargs else 'frontalface_default'
		self.classScaleFactor = kwargs['classScaleFactor'] if 'classScaleFactor' in kwargs else 1.1
		self.classMinNeighbors = kwargs['classMinNeighbors'] if 'classMinNeighbors' in kwargs else 5
		self.classMinSize = kwargs['classMinSize'] if 'classMinSize' in kwargs else (1,1)
		self.default_classifiers = {
			'eye_tree_eyeglasses': 'haarcascade_eye_tree_eyeglasses.xml',
			'eye': 'haarcascade_eye.xml',
			'frontalface_alt_tree': 'haarcascade_frontalface_alt_tree.xml',
			'frontalface_alt': 'haarcascade_frontalface_alt.xml',
			'frontalface_alt2': 'haarcascade_frontalface_alt2.xml',
			'frontalface_default': 'haarcascade_frontalface_default.xml',
			'fullbody': 'haarcascade_fullbody.xml',
			'lowerbody': 'haarcascade_lowerbody.xml',
			'profileface': 'haarcascade_profileface.xml',
			'smile': 'haarcascade_smile.xml',
			'upperbody': 'haarcascade_upperbody.xml',
		}

		#-----colors
		self.color = ['#2179F1','#331AE5','#96E421','#C56D88','#61CAC5','#4980EC','#2E3400','#E0DB68','#C4EC5C','#D407D7','#FBB61B',
		'#067E8B','#76A502','#0AD8AB','#EAF3BF','#D479FE','#3B62CD','#789BDD','#7F141E','#949CBE']

		#----shape
		# check if trying to do complex ROI using dataviewer
		if (self.shape in ['polygon', 'hull']) and (self.roi_format == "dataviewer"):
			raise Exception ("Cannot use shape %s when exporting for DataViewer. \
					Please use either 'circle', 'rotate', or 'straight' instead, or set roi_format == 'raw'."%(shape))

		#----directory
		if self.isDemo is True:
			import imhr
			path = Path(imhr.__file__).parent
			self.image_path = "%s/dist/roi/raw/1/"%(path)
			self.output_path = "%s/dist/roi/output/"%(path)
			metadata_source = "%s/dist/roi/raw/1/metadata.xlsx"%(path)
		else:
			self.image_path = image_path
			self.output_path = output_path

		# if no image path and not demo
		if self.image_path is None:
			error = "No valid image path found. Please make sure to include an image path. If you wish to run a demo, please set isDemo=True."
			raise Exception(error)
		else:
			# set directory of files
			self.directory = [x for x in Path(self.image_path).glob("*.psd") if x.is_file()]

		#----read metadata file (if metadata is not None)
		if metadata_source is not "embedded":
			self.metadata_source = metadata_source
			_type = Path(self.metadata_source).suffix
			if _type == ".csv": self.metadata_all = pd.read_csv(self.metadata_source)
			elif _type == ".xlsx": self.metadata_all = pd.read_excel(self.metadata_source)

			# convert to string
			self.metadata_all = self.metadata_all.astype(str)

			# check if metadata is empty
			if self.metadata_all.empty:
				raise Exception('No data for file: %s'%(self.metadata_source))

	def extract_metadata(self, imagename, layer):
		"""Extract metadata for each region of interest.

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
			self.console('## roiname: %s'%(roiname),'blue')
			self.console('## roilabel: %s'%(roilabel),'green')

		return metadata, roiname

	def format_image(self, psd=None, xcf=None, bitmap=None, isRaw=False):
		"""Resize image and reposition image, relative to screensize.

		Parameters
		----------
		psd : :obj:`None` or `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`_
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest, by default None
		xcf : :obj:`None` or ###, optional
			[description], by default None
		bitmap : :obj:`None` or ###, optional
			[description], by default None
		isRaw : :obj:`None` or ###, optional
			If `True`, the image will be returned withour resizing or placed on top of a background image. Default is `False`.

		Attributes
		----------
		image : :class:`PIL.Image.Image`
			PIL image object class.

		Returns
		-------
		image, background : :class:`PIL.Image.Image`
			PIL image object class.
		"""

		## load image from PSD, xcf, or bitmap as PIL
		if psd is not None:
			image = psd.topil()
		elif xcf is not None:
			image = psd.topil()
		elif bitmap is not None:
			image = psd.topil()

		# if returning raw image
		if isRaw:
			imagesize = [image.size[0], image.size[1]]
			return image, imagesize
		else:
			## set background
			screen_size = self.screensize
			background = Image.new("RGBA", (screen_size), (0, 0, 0, 0))
			if self.isDebug: self.console('# export image','blue')
			# if scale image
			if self.scale != 1:
				old_imagesize = [image.size[0], image.size[1]]
				imagesize = [int(image.size[0] * self.scale), int(image.size[1] * self.scale)]
				image = image.resize(imagesize, Image.ANTIALIAS)
				if self.isDebug:
					self.console('image size: %s, scaled to: %s'%(old_imagesize, imagesize), 'green')
			# else unscaled
			else:
				imagesize = [int(image.size[0]), int(image.size[1])]
				if self.isDebug: self.console('image size: %s'%(imagesize))

			# if offsetting
			if self.newoffset:
				offset_center = self.recenter
				# calculate upper-left coordinate for drawing into image
				# x-bound <offset_x center> - <1/2 image_x width>
				x = (offset_center[0]) - (imagesize[0]/2)
				# y-bound <offset_y center> - <1/2 image_y width>
				y = (offset_center[1]) - (imagesize[1]/2)
				left_xy = (int(x),int(y))
				if self.isDebug: self.console('image centered at: %s'%(offset_center))
			# else not offsetting
			else:
				# calculate upper-left coordinate for drawing into image
				# x-bound <screen_x center> - <1/2 image_x width>
				x = (screen_size[0]/2) - (imagesize[0]/2)
				# y-bound <screen_y center> - <1/2 image_y width>
				y = (screen_size[1]/2) - (imagesize[1]/2)
				left_xy = (int(x),int(y))

			# draw
			background.paste(image, left_xy)

			return background, imagesize

	def extract_contours(self, image, imagename, roiname):
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
		# convert pil image to grayscale (using pil)
		#self.console('test4.0.5', 'red')
		image = image.convert(mode='L')

		# convert to np.array
		#self.console('test4.1.0', 'red')
		image = np.array(image)

		# or convert pil image to grayscale (using cv2)
		#self.console('test4.1.5', 'red')
		#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# if drawing in PSD files
		if self.detection == 'manual':
			if self.isDebug: self.console('manual ROI detection','blue')
			# threshold the image
			## note: if any pixels that have value higher than 127, assign it to 255. convert to bw for countour and store original
			#self.console('test4.2', 'red')
			retval, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

			# find contour in image
			#self.console('test4.3', 'red')
			## note: if you only want to retrieve the most external contour # use cv.RETR_EXTERNAL
			contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			# if contours empty raise Exception
			#self.console('test4.4', 'red')
			if not bool(contours):
				_err = [imagename, roiname, 'Not able to identify contours']
				raise Exception('%s; %s; %s'%(_err[0],_err[1],_err[2]))
		# if drawing in PSD files
		else:
			if self.isDebug: self.console('automatic ROI detection from haar cascades','blue')
			# load classifier
			_classifer = self.default_classifiers[self.classifier]
			haar = cv2.CascadeClassifier(_classifer)
			contours = haar.detectMultiScale(
			    image,
			    scaleFactor=1.1,
			    minNeighbors=5,
			    minSize=(1,1),
			    flags = cv2.CASCADE_SCALE_IMAGE
			)

		#------------------------------------------------------------------------for each layer: save images and contours
		#when saving the contours below, only one drawContours function from above can be run
		#any other drawContours function will overlay on the others if multiple functions are run
		#----param
		color = (0, 255, 0)
		#self.console('test4.5', 'red')

		#----straight bounding box
		if self.shape == 'straight':
			# self.console('## roishape: straight bounding box','green')
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
			# self.console('## roishape: rotated bounding box','green')
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
			# self.console('## roishape: bounding circle','green')
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
			# self.console('## roishape: approximate polygon','green')
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
			# self.console('## roishape: hull','green')
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

		#self.console('test4.6', 'red')

		return _bounds, _contours

	def format_contours(self, imagename, metadata, roiname, roinumber, bounds_, contours_):
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
		bounds_ : [type]
			[description]
		contours_ : [type]
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
		_bounds = pd.DataFrame(bounds_)

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

		#----save image:roi level image bounds and con
		#----save roi contours
		#!! get working: draw exact contours as coordinates
		if self.save['contours']:
			contours = contours_
		# combine metadata with coordinates
		##!!! get working

		#----save roi df
		# combine metadata with bounds
		if metadata is not None:
			bounds = pd.merge(bounds, metadata, on=['image','roi'], how='outer')

		# finish
		return bounds, contours

	def draw_contours(self, filepath, data, fig, source='bounds'):
		"""[summary]

		Parameters
		----------
		filepath : [type]
			[description]
		data : [type]
			[description]
		fig : [type]
			[description]
		source : str, optional
			[description], by default 'bounds'
		"""
		# get current axis
		ax = fig.gca()
		if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
		if self.tight_layout: plt.tight_layout()
		if self.remove_axis: fig.tight_layout(pad=0); ax.set_position([0, 0, 1, 1], which='both')
		## create blank image and draw to figure
		_img = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))

		## for each bound draw on figure
		if source=="bounds":
			ax.imshow(_img)
			#for _bounds in data:
			## get bounds
			x0 = data['x0'].item()
			y0 = data['y0'].item()
			x1 = data['x1'].item()
			y1 = data['y1'].item()
			_width = x1 - x0
			_height = y1 - y0
			_color = random.choice(self.color)
			ax.add_patch(patches.Rectangle((x0, y0), _width, _height, color=_color, alpha=0.5))
			## check folder
			filepath_ = Path(filepath).parent
			if not os.path.exists(filepath_):
				os.makedirs(filepath_)
			## save
			if self.isDebug: self.console('## image saved @: %s'%(filepath),'blue')
		## for each contour draw on figure
		elif source=="contours":
			#for _contours in data:
			contours = cv2.cvtColor(data, cv2.COLOR_GRAY2RGB)
			plt.imshow(contours, zorder=1, interpolation='bilinear')
			## check folder
			filepath_ = Path(filepath).parent
			if not os.path.exists(filepath_):
				os.makedirs(filepath_)
			## save
			if self.isDebug: self.console('## image saved @: %s'%(filepath),'blue')

	def export_data(self, df, path, filename, uuid=None, newcolumn=None, level='image'):
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
		nested : :obj:`string` {`image`,`all`}
			Nested order, either `image` or `all`. Default `image`.

		Returns
		-------
		[type]
			[description]
		"""
		#if workng with a single image
		if level == 'image':
			# if new column is not None and level == image
			if (isinstance(newcolumn, (dict,))):
				df[list(newcolumn.keys())[0]] = list(newcolumn.values())[0]

			# if uuid, create a unique column
			if isinstance(uuid, (list,)):
				df['uuid'] = df[uuid].apply(lambda x: ''.join(x), axis=1)
				uuid_column = 'uuid'
			# else simply use roiname
			else:
				uuid_column = self.roicolumn

		#else if workng with all images
		elif level == 'all':
			# if uuid, create a unique column
			if isinstance(uuid, (list,)):
				uuid_column = 'uuid'
			# else simply use roiname
			else:
				uuid_column = self.roicolumn

		# check if folder exists
		if not os.path.exists(path):
			os.makedirs(path)

		# export to excel
		if ((self.roi_format == 'raw') or (self.roi_format == 'both')):
			filepath = Path("%s/%s.xlsx"%(path, filename))
			df.to_excel("%s"%(filepath), index=False)

			# if debug
			if self.isDebug: self.console("## raw data saved @: %s"%(filepath),'green')

		# export to ias (dataviewer)
		if ((self.roi_format == 'dataviewer') or (self.roi_format == 'both')):
			filepath = Path("%s/%s.ias"%(path, filename))
			_bounds = '\n'.join(map(str, [
				"# EyeLink Interest Area Set created on %s."%(self.now()),
				"# Interest area set file using imhr.eyetracking.ROI()",
				"# columns: RECTANGLE | IA number | x0 | y0 | x1 | y1 | label",
				"# example: RECTANGLE 1 350 172 627 286 leftcheek",
				"# columns: ELLIPSE | IA number | x0 | y0 | x1 | y1 | label",
				"# example: ELLIPSE 2 350 172 627 286 leftcheek",
				"# columns: FREEHAND | IA number | x0,y0 | x1,y1 | x2,y2 | x3,y3 | label",
				"# example: FREEHAND 3 350,172 627,172 627,286 350,286 leftcheek",
				"# For more information see Section 5.10.1 of Eyelink DataViewer Users Manual (3.2.1).",
				df[['shape_d','id','x0','y0','x1','y1',uuid_column]].to_csv(index=False, header=False).replace(',', '	')
			]))
			# save to ias
			with open("%s"%(filepath), "w") as file:
				file.write(_bounds)

			# if debug
			if self.isDebug: self.console("## dataviewer data saved @: %s"%(filepath),'green')

		return df

	def run(self, directory, core=0, queue=None):
		"""[summary]

		Parameters
		----------
		directory : :obj:`list`
			[description]
		core : :obj:`int`
			(if isMultiprocessing) Core used for this function. Default `0`.
		queue : :obj:`queue.Queue`
			Constructor for a multiprocessing 'first-in, first-out' queue. Note: Queues are thread and process safe.

		Returns
		-------
		[type]
			[description]
		"""

		#----prepare lists for all images
		l_bounds_all = []
		l_contours_all = []
		l_error = []

		#!!!----for each image
		self.console('starting()','purple')
		if self.isDebug: self.console('for each image','purple')
		for file in directory:
			# console
			if self.isDebug and self.isMultiprocessing: self.console('core: %s'%(core),'orange')
			# defaults
			psd=None
			xcf=None
			bitmap=None

			# read image
			ext = (Path(file).suffix).lower()
			## if psd
			if ext == '.psd':
				psd = psd_tools.PSDImage.open(file)
				imagename = os.path.splitext(os.path.basename(file))[0]
				if self.isDebug: self.console('\n# file: %s'%(imagename),'blue')
			## else if xcf (GIMP)
			elif ext == '.xcf':
				psd = psd_tools.PSDImage.open(file)
				imagename = os.path.splitext(os.path.basename(file))[0]
				if self.isDebug: self.console('\n# file: %s'%(imagename),'blue')
			## else if bitmap
			elif ext in ['.bmp','.jpeg','.jpg','.png']:
				psd = psd_tools.PSDImage.open(file)
				imagename = os.path.splitext(os.path.basename(file))[0]
				if self.isDebug: self.console('\n# file: %s'%(imagename),'blue')
			else:
				error = "Image format not valid. Acceptable image formats are: psd (photoshop), xcf (gimp), or png/bmp/jpg (bitmap)."
				raise Exception(error)

			# clear lists
			l_bounds = [] #list of bounds
			l_contours = [] #list of contours

			#!!!----for each image, save image file
			# raw image
			image, imagesize = self.format_image(psd=psd, xcf=xcf, bitmap=bitmap, isRaw=True)
			## check folder
			_folder = '%s/img/raw/'%(self.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## save raw
			filepath = '%s/%s.png'%(_folder, imagename)
			if self.image_backend == 'PIL':
				image.save(filepath)
			else:
				fig = plt.figure()
				if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
				if self.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if self.tight_layout: plt.tight_layout()
				plt.imshow(image, zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
				plt.close(fig)

			# preprocessed imaage (image with relevant screensize and position)
			image, imagesize = self.format_image(psd=psd, xcf=xcf, bitmap=bitmap)
			## check folder
			_folder = '%s/img/preprocessed/'%(self.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## save preprocessed
			filepath = '%s/%s.png'%(_folder, imagename)
			if self.image_backend == 'PIL':
				image.save(filepath)
			else:
				fig = plt.figure()
				if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
				if self.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if self.tight_layout: plt.tight_layout()
				plt.imshow(image, zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
				plt.close(fig)

			#!!!----for each region of interest
			## counter
			roinumber = 1

			## check path
			_folderpath = '%s/img/bounds/roi/'%(self.output_path)
			if not os.path.exists(_folderpath):
				os.makedirs(_folderpath)
			## run
			for layer in psd:
				# skip if layer is main image
				if Path(layer.name).stem == imagename:
					continue
				else:
					#. Extract metadata for each region of interest.
					metadata, roiname = self.extract_metadata(imagename=imagename, layer=layer)

					#. Resize image and reposition image, relative to screensize.
					image, imagesize = self.format_image(psd=layer, xcf=xcf, bitmap=bitmap)

					#. Extract contours from np.array of image.
					try:
						bounds_, contours_ = self.extract_contours(image=image, imagename=imagename, roiname=roiname)
					except:
						break

					#. Format contours as Dataframe, for exporting to xlsx or ias.
					bounds, contours = self.format_contours(imagename=imagename, metadata=metadata, roiname=roiname, roinumber=roinumber, bounds_=bounds_, contours_=contours_)

					#. Draw bounds or contours.
					## draw bounds
					if self.shape == 'straight':
						## img path
						filepath = '%s/img/bounds/roi/%s.%s.png'%(self.output_path, imagename, roiname)
						# save image
						if self.image_backend == 'PIL':
							image.save(filepath)
						else:
							fig = plt.figure()
							if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
							if self.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
							if self.tight_layout: plt.tight_layout()
							self.draw_contours(filepath=filepath, data=bounds, source='bounds', fig=fig)
							plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
							plt.close(fig)
					## draw contours
					else:
						## img path
						filepath = '%s/img/bounds/roi/%s.%s.png'%(self.output_path, imagename, roiname)
						# save image
						if self.image_backend == 'PIL':
							image.save(filepath)
						else:				
							fig = plt.figure()
							if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
							if self.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
							if self.tight_layout: plt.tight_layout()
							self.draw_contours(filepath=filepath, data=contours, source='contours', fig=fig)
							plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
							plt.close(fig)

					#. store processed bounds and contours to combine across image
					l_bounds.append(bounds)
					l_contours.append(contours)

					#. update counter
					roinumber = roinumber + 1

			#!!!----for each image
			# draw bounds
			if self.shape == 'straight':
				## img path
				filepath = '%s/img/bounds/%s.png'%(self.output_path, imagename)
				fig = plt.figure()
				if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
				if self.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if self.tight_layout: plt.tight_layout()
				[self.draw_contours(filepath=filepath, data=b, source='bounds', fig=fig) for b in l_bounds]
				plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
				plt.close(fig)
			# draw contours
			else:
				## img path
				filepath = '%s/img/bounds/%s.png'%(self.output_path, imagename)
				fig = plt.figure()
				if self.set_size_inches is not None: fig.set_size_inches(self.screensize[0]/self.dpi, self.screensize[1]/self.dpi)
				if self.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if self.tight_layout: plt.tight_layout()
				[self.draw_contours(filepath=filepath, data=c, source='contours', fig=fig) for c in l_contours]
				plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
				plt.close(fig)

			# concatinate and store bounds for all rois
			df = pd.concat(l_bounds)
			l_bounds_all.append(df)

			# export data
			_filename = "%s_bounds"%(imagename)
			_folder = '%s/data/'%(self.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			df = self.export_data(df=df, path=_folder, filename=_filename, uuid=self.uuid, newcolumn=self.newcolumn, level='image')

			# contours
			##!!! create roi file for complex shapes (not with dataviewer)

		#!!!----finished for all images
		# store
		## if multiprocessing, store in queue
		if self.isMultiprocessing:
			queue.put(l_bounds_all)
			pass
		# if not multiprocessing, return
		else:
			return l_bounds_all, l_contours_all, l_error

	def process(self):
		"""[summary]

		Returns
		-------
		[type]
			[description]
		"""
		# prepare arguements and procedure
		df = ''

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
				self.console('not multiprocessing', 'purple')
			# split directory by number of cores
			else:
				self.isMultiprocessing = True
				l_directory = np.array_split(self.directory, self.cores)
				self.console('multiprocessing with %s cores'%(self.cores), 'purple')

		# not multiprocessing
		else:
			self.isMultiprocessing = False
			self.console('not multiprocessing', 'purple')

		#----prepare to run
		# if not multiprocessing
		if not self.isMultiprocessing:
			l_bounds_all, l_contours_all, l_error = self.run(self.directory)

			# finish
			df, error = self.finished(df=l_bounds_all)

		# else if multiprocessing
		else:
			# collect each pipe (this is used to build send and recieve portions of output)
			queue = multiprocessing.Queue()

			# prepare threads
			process = [multiprocessing.Process(target=self.run, args=(l_directory[core].tolist(), core, queue,)) for core in range(self.cores)]

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
			if self.isDebug: self.console('process() finished (multiprocessing)','purple')
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
		# if multiprocessing, combine df from each thread
		if self.isMultiprocessing:
			#concat data
			df = [i[0] for i in df if len(i) != 0] #check if lists are empty (i.e. if there are more threads than directories)
			df = pd.concat(df)
		# else combine lists of df to df
		else:
			df = pd.concat(df)

		#!!!----combine all rois across images
		# export to csv or dataviewer
		_folder = '%s/'%(self.output_path)
		_filename = "bounds"
		df = self.export_data(df=df, path=_folder, filename=_filename, uuid=self.uuid, level='all')

		#!!!----error log
		if bool(errors):
			_filename = Path('%s/error.csv'%(self.output_path))
			self.console("Errors found. See log %s"%(_filename), 'red')
			error = pd.DataFrame(errors, columns=['image','roi','message'])
			error.to_csv(_filename, index=False)
		else:
			error = None

		# finished
		self.console('finished()','purple')
		return df, error

# if calling from cmd/terminal
if __name__ == '__main__':
	import sys, argparse, re
	# https://docs.python.org/3.7/library/argparse.html
	# args
	sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
	parser = argparse.ArgumentParser(
		prog = sys.argv[0],
		usage = "Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python."
	)

	# main arguments
	parser.add_argument("--image_path", help="image_path.", default=None)
	parser.add_argument("--output_path", help="output_path.", default=None)
	parser.add_argument("--metadata_source", help="metadata_source.", default=None)

	# start
	args_ = parser.parse_args()
	sys.exit(ROI(args_))

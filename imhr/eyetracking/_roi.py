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
	from PIL import Image, ImageOps
	import matplotlib
	#matplotlib.use('Agg')
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
	raise Exception("No module named '%s'. Please install from PyPI before continuing."%(pkg),'red')

class ROI():
	"""Generate regions of interest that can be used for data processing and analysis."""
	@classmethod
	def __init__(self, isMultiprocessing=False, detection='manual', image_path=None, output_path=None, metadata_source=None, 
			  roi_format='both', shape='box', roicolumn='roi', uuid=None, filetype='psd', **kwargs):
		"""Generate regions of interest that can be used for data processing and analysis.

		Parameters
		----------
		isMultiprocessing : :obj:`bool`
			Should the rois be generated using multiprocessing. Default is **False**.
		detection : :obj:`str` {'manual', 'haarcascade'}
			How should the regions of interest be detected. Either manually (**manual**), through the use of highlighting layers in photo-editing
			software, or automatically through feature detection using **haarcascade** classifers from opencv. Default **manual**.
		image_path : :obj:`str`
			Image directory path.
		output_path : :class:`str`
			Path to save data.
		roi_format : :obj:`str` {'raw', 'dataviewer', 'both'}
			Format to export ROIs. Either to 'csv' (**raw**) or to Eyelink DataViewer 'ias' (**dataviewer**) or both (**both**).
			Default is **both**. Note: If **roi_format** = **dataviewer**, **shape** must be either be **circle**, **rotated**, or **straight**.
		metadata_source : :class:`str` or :obj:`None` {'path', 'embedded'}
			Metadata source. If metadata is being read from a spreadsheet, **metadata_source** should be equal to path the to
			the metadata file, else if metadata is embed within the image as a layer name, **metadata_source** = **embedded**.
			Default is **embedded**. For example:
				>>> # if metadata is in PSD images
				>>> metadata = 'embedded'
				>>> # if metadata is an external xlsx file.
				>>> metadata = 'roi/metadata.xlsx'
			Although Photoshop PSD don't directly provide support for metadata. However if each region of interest is stored
			as a seperate layer within a PSD, the layer name can be used to store metadata. To do this, the layer name has
			to be written as delimited text. Our code can read this data and extract relevant metadata. The delimiter can
			be either **;** **,** **|** **\\t** or **\\s** (Delimiter type must be identified when running this code using the
			**delimiter** parameter. The default is **;**.). Here's an example using **;** as a delimiter:

			.. rst-class:: code-param-whitespace

				>>> imagename = "BM001"; roiname = 1; feature = "lefteye"

			Note: whitespace should be avoided from from each layer name. Whitespaces may cause errors during parsing.
		shape : :obj:`str` {'polygon', 'hull', 'circle', 'rotated', 'straight'}
			Shape of machine readable boundaries for region of interest. Default is **straight**. **polygon** creates a Contour
			Approximation and will most closely match the orginal shape of the roi. **hull** creates a Convex Hull, which
			is similar to but not as complex as a Contour Approximation and will include bulges for areas that are convex.
			**circle** creates a mininum enclosing circle. Finally, both **rotated** and **straight** create a Bounding Rectangle,
			with the only difference being compensation for the mininum enclosing area for the box when using **rotated**.
		roicolumn : :obj:`str`
			The name of the label for the region of interest in your metadata. For example you may want to extract the column
			'feature' from your metadata and use this as the label. Default is **roi**.
		uuid : :obj:`list` or :obj:`None`
			Create a unique id by combining a list of existing variables in the metadata. This is recommended
			if **roi_format** == **dataviewer** because of the limited variables allowed for ias files. Default is **None**.
		filetype: :obj:`str` {'psd', 'tiff', 'dcm', 'png', 'bmp', 'jpg'}
			The filetype extension of the image file. Case insensitive. Default is **psd**. If **psd**, **tiff** or **DICOM**
			the file can be read as multilayered.
		**kwargs : :obj:`str` or :obj:`None`, optional
			Additional properties to control how data is exported, naming variables, exporting images are also available:

			These properties control additional core parameters for the API:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **cores** : :obj:`bool`
				  - (if **isMultiprocessing** == **True**) Number of cores to use. Default is total available cores - 1.
				* - **isLibrary** : :obj:`bool`
				  - Check if required packages have been installed. Default is **False**.
				* - **isDebug** : :obj:`bool`
				  - Allow flags to be visible. Default is **False**.
				* - **isDemo** : :obj:`bool`
				  - Tests code with in-house images and metadata. Default is **False**.
				* - **save_data** : :obj:`bool`
				  - Save coordinates. Default is **True**.
				* - **newcolumn** : :obj:`dict` {:obj:`str`, :obj:`str`} or :obj:`False`
				  - Add additional column to metadata. This must be in the form of a dict in this form {key: value}. Default is **False**.
				* - **save_raw_image** : :obj:`bool`
				  - Save images. Default is True.
				* - **append_output_name** : :obj:`bool` or :obj:`str`
				  - Add appending name to all exported files (i.e. <'top_center'> IMG001_top_center.ias). Default is **False**.
				* - **save_contour_image** : :obj:`bool`
				  - Save generated contours as images. Default is **True**.
				* - **scale** : :obj:`int`
				  - If image is scaled during presentation, set scale. Default is **1**.
				* - **offset** : :obj:`list` [:obj:`int`]
				  - Center point of image, relative to screensize. Default is **[960, 540]**.
				* - **screensize** : :obj:`list` [:obj:`int`]
				  - Monitor size is being presented. Default is **[1920, 1080]**.

			These properties control data is processed which include the type of haarcascade used, delimiters for metadata:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **delimiter** : :obj:`str` {';' , ',' , '|' , 'tab' , 'space'}
				  - (if **source** == **psd**) How is metadata delimited. Default is **;**.
				* - **classifiers** : :obj:`default` or :obj:list of :obj:dict
				  - (if **detection** == **haarcascade**) Trained classifiers to use. Default is {'eye_tree_eyeglasses', 'eye', 'frontalface_alt_tree', 'frontalface_alt', 'frontalface_alt2','frontalface_default', 'fullbody', 'lowerbody', 'profileface', 'smile', 'upperbody'}. Parameters are stored `here <imhr.eyetracking.ROI.haar_parameters>`__. If you want to use custom classifiers, you can pass a list of classifiers and their arguments using the following format:

				    .. rst-class:: code-param-whitespace

				    .. code-block:: python

				    	>>>  [{'custom_cascade': {
						...   'file': 'haarcascade_eye.xml',
						...   'type': 'eye',
						...   'path': './haarcascade_eye.xml',
						...   'minN': 5,
						...   'minS': (100,100),
						...   'sF': 1.01 }
						...  }]

				    You can also pass custom arguments by calling them after initiation:

				    .. rst-class:: code-param-whitespace

				    .. code-block:: python

				    	>>> roi = imhr.eyetracking.ROI(detection='manual.....)
				    	>>> roi.default_classifiers['eye']['minNeighbors'] = 10


			Here are properties specific to how images are exported after processing. The code can either use :class:`matplotlib` or :class:`PIL` as a backend engine:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **image_backend** : :class:`str` {'matplotlib', 'PIL'}
				  - Backend for exporting image. Either :class:`matplotlib` or :class:`PIL`. Default is :class:`matplotlib`.
				* - **RcParams** : :class:`bool`
				  - A dictionary object including validation validating functions are defined and associated with rc parameters in class:`matplotlib.RcParams`. Default is **None**.
				* - **background_color** : :class:`list`
				  - Set background color (RGB) for exporting images. Default is **[110, 110, 110]**.
				* - **dpi** : :class:`int` or :obj:`None`
				  - (if **save_image** == **True**) Quality of exported images, refers to 'dots per inch'. Default is **300**.
				* - **remove_axis** : :class:`bool`
				  - Remove axis from :obj:`matplotlib.pyplot`. Default is **False**.
				* - **tight_layout** : :class:`bool`
				  - Remove whitespace from :obj:`matplotlib.pyplot`. Default is **False**.
				* - **set_size_inches** : :class:`bool`
				  - Set size of :obj:`matplotlib.pyplot` according to screensize of ROI. Default is **False**.

		Attributes
		----------
		shape_d : :class:`str` {'ELLIPSE', 'FREEHAND', 'RECTANGLE'}
			DataViewer ROI shape.
		psd :  `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`__
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest.
		retval, threshold : :obj:`numpy.ndarray`
			Returns from :ref:`cv2.threshold`. The function applies a fixed-level thresholding to a multiple-channel array.
			**retval** provides an optimal threshold only if :ref:`cv2.THRESH_OTSU` is passed. **threshold** is an image after applying
			a binary threshold (:ref:`cv2.THRESH_BINARY`) removing all greyscale pixels < 127. The output matches the same image
			channel as the original image.
			See `opencv <https://docs.opencv.org/4.0.1/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57>`__ and
			`leanopencv <https://www.learnopencv.com/opencv-threshold-python-cpp>`__ for more information.
		contours, hierarchy : :obj:`numpy.ndarray`
			Returns from :ref:`cv2.findContours`. This function returns contours from the provided binary image (threshold).
			This is used here for later shape detection. **contours** are the detected contours, while hierarchy containing
			information about the image topology.
			See `opencv <https://docs.opencv.org/4.0.1/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e07>`__
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

		.. code-block:: python

			>>> img.save('/Users/mdl-admin/Desktop/roi/PIL.png') #DEBUG: save PIL
			>>> cv2.imwrite('/Users/mdl-admin/Desktop/roi/cv2.png', img_cv2) #DEBUG: save cv2
			>>> plt.imshow(img_np); plt.savefig('/Users/mdl-admin/Desktop/roi/matplotlib.png') #DEBUG: save matplotlib

		Notes
		-----
		Resources
			* Guide
				* https://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html
			* Details
				* For more information about each shape:
					* See https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html 
				* For more information how images are drawn:
					* See https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
				* To understand how bounds are created:
					* See https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
		"""
		import imhr
		self.path = Path(imhr.__file__).parent

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
		self.shape = shape if shape in ['polygon', 'hull', 'circle', 'rotated', 'straight'] else 'straight'
		self.shape_d = None #dataviewer shape
		# uuid
		self.uuid = uuid
		# label
		self.roicolumn = roicolumn
		# add column
		self.newcolumn = kwargs['newcolumn'] if 'newcolumn' in kwargs else None
		# add appendix to name
		self.append_output_name = kwargs['append_output_name'] if 'append_output_name' in kwargs else False
		# save
		self.save = {}
		# save csv
		self.save['data'] = kwargs['save_data'] if 'save_data' in kwargs else True
		# save contour images
		self.save['contours'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True
		# save raw images
		self.save['raw'] = kwargs['save_contour_image'] if 'save_contour_image' in kwargs else True

		#-----PIL
		self.background_color = kwargs['background_color'] if 'background_color' in kwargs else (110, 110, 110)

		#-----matplotlib
		self.image_backend = kwargs['image_backend'] if 'image_backend' in kwargs else 'matplotlib'
		# hide/show
		self.remove_axis = kwargs['remove_axis'] if 'remove_axis' in kwargs else False
		self.tight_layout = kwargs['tight_layout'] if 'tight_layout' in kwargs else False
		self.set_size_inches = kwargs['set_size_inches'] if 'set_size_inches' in kwargs else False
		if self.remove_axis: plt.rcParams.update({'axes.titlesize':0, 'axes.labelsize':0, 'xtick.labelsize':0, 
		'ytick.labelsize':0, 'savefig.pad_inches':0, 'font.size': 0})
		# sizes
		self.dpi = kwargs['dpi'] if 'dpi' in kwargs else 300
		self.axis_tick_fontsize =  kwargs['axis_tick_fontsize'] if 'axis_tick_fontsize' in kwargs else 8
		self.axis_title_fontsize =  kwargs['axis_title_fontsize'] if 'axis_title_fontsize' in kwargs else 10
		self.figure_title_fontsize = kwargs['figure_title_fontsize'] if 'figure_title_fontsize' in kwargs else 12
		plt.rcParams.update({
			#dpi
			'figure.dpi': self.dpi,
			#font
			'ytick.labelsize': self.axis_tick_fontsize, 
			'xtick.labelsize': self.axis_tick_fontsize,
			'axes.titlesize': self.axis_title_fontsize,
			'figure.titlesize': self.figure_title_fontsize
		})
		self.rcParams = kwargs['rcParams'] if 'rcParams' in kwargs else matplotlib.rcParams
		if self.rcParams is not None: plt.rcParams.update(self.rcParams)

		#-----classifiers
		import yaml
		if ('classifiers' in kwargs) and (kwargs['classifiers'] is not 'default'):
			self.classifiers = kwargs['classifiers']
		else:
			with open('%s/dist/roi/classifiers.yaml'%(self.path), 'r') as _file:
				self.classifiers = yaml.safe_load(_file)
			for item in self.classifiers:
				self.classifiers[item]['path'] = '%s/%s'%(self.path, self.classifiers[item]['path'])

		#-----colors
		self.hex = ['#2179F1','#331AE5','#96E421','#C56D88','#61CAC5','#4980EC','#2E3400','#E0DB68','#C4EC5C','#D407D7','#FBB61B',
		'#067E8B','#76A502','#0AD8AB','#EAF3BF','#D479FE','#3B62CD','#789BDD','#7F141E','#949CBE']
		self.rgb = [(102,12,15),(153,3,8),(179,47,45),(229,28,35),(242,216,167),(255,255,153),(255,255,77),(242,132,68),(242,141,119),
	    (150,217,184),(85,217,153),(16,187,111),(54,140,98),(96,154,191),(64,112,160),(33,150,243),(43,71,171),(165,140,255),
		(217,35,237),(97,18,179)]

		#----shape
		# check if trying to do complex ROI using dataviewer
		if (self.shape in ['polygon', 'hull']) and (self.roi_format == "dataviewer"):
			raise Exception ("Cannot use shape %s when exporting for DataViewer. \
					Please use either 'circle', 'rotate', or 'straight' instead, or set roi_format == 'raw'."%(shape))

		#----directory
		self.filetype = filetype.strip('.')
		if self.isDemo is True:
			self.image_path = "%s/dist/roi/raw/1/"%(self.path)
			self.output_path = "%s/dist/roi/output/"%(self.path)
			metadata_source = "%s/dist/roi/raw/1/metadata.xlsx"%(self.path)
		else:
			self.image_path = image_path
			self.output_path = output_path

		# if no image path and not demo
		if self.image_path is None:
			error = "No valid image path found. Please make sure to include an image path. If you wish to run a demo, please set isDemo=True."
			raise Exception(error)
		else:
			# set directory of files
			self.directory = [x for x in (Path(self.image_path).glob("*.%s"%(filetype.lower())) or Path(self.image_path).glob("*.%s"%(filetype.upper())))]
			## if no files in directory, raise exception
			if not self.directory:
				error = "No %s images in path: %s. Please make sure to include an image path. \
				If you wish to run a demo, please set isDemo=True."%(filetype, self.image_path)
				raise Exception(error.replace("\t",""))

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

	@classmethod
	def extract_metadata(cls, imagename, imgtype, layer):
		"""Extract metadata for each region of interest.

		Parameters
		----------
		imagename : [type]
			[description]
		imgtype : [type]
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
		if cls.metadata_source == 'embedded':
			metadata = pd.DataFrame(data=(item.split("=") for item in layer.name.split(cls.delimiter)),columns=['key','value'])
			metadata.set_index('key', inplace=True)
			metadata.loc['name']['value'] = metadata.loc['name']['value'].replace("roi","")
			roiname = metadata.loc['name']['value']

		# else read metadata from file
		else:
			# get metadata
			if imgtype=='psd':
				roiname = layer.name.strip(' \t\n\r') # strip whitespace
				metadata = cls.metadata_all.loc[(cls.metadata_all['image'] == imagename) & (cls.metadata_all['roi'] == roiname)]
			else:
				roiname = imagename 
				##!!! TODO: Resolve metadata for non-layered images
				metadata = cls.metadata_all.loc[(cls.metadata_all['image'] == imagename)]
			# if datafame empty
			if metadata.empty:
				message = 'No data for %s:%s (image:roi).'%(imagename, roiname)
				raise Exception(message)

		# print results
		if cls.isDebug:
			cls.console('## roiname: %s'%(roiname),'green')

		return metadata, roiname

	@classmethod
	def format_image(cls, image=None, imgtype='psd', isRaw=False, isPreprocessed=False, isNormal=False, isHaar=False):
		"""Resize image and reposition image, relative to screensize.

		Parameters
		----------
		IMG : :obj:`None` or
			Can be either:
			`psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`__
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest, by default None
		imgtype : :obj:`str` {'psd','dcm','tiff', 'bitmap'}
			Image type.
		isRaw : :obj:`None` or ###, optional
			If **True**, the image will be returned without resizing or placed on top of a background image. Default is **False**.
		isPreprocessed : :obj:`None` or ###, optional
			If **True**, the image will be returned with resizing and placed on top of a background image. Default is **False**.

		Attributes
		----------
		image : :class:`PIL.Image.Image`
			PIL image object class.

		Returns
		-------
		image, background : :class:`PIL.Image.Image`
			PIL image object class.
		"""

		## load image from PSD, DICOM, tiff, or bitmap as PIL
		if imgtype == 'psd':
			if not isHaar: image = image.topil()
			else: image = image
			imagesize = [image.size[0], image.size[1]]
		elif imgtype == 'DICOM':
			image = image
			imagesize = [image.size[0], image.size[1]]
		elif imgtype == 'tiff':
			image = image
			imagesize = [image.size[0], image.size[1]]
		elif imgtype == 'bitmap':
			image = image
			imagesize = [image.size[0], image.size[1]]

		# if returning raw image
		if isRaw:
			if cls.isDebug: cls.console('# export raw image','blue')
			return image, imagesize
		# if returning raw image
		elif isPreprocessed:
			## set background
			screen_size = cls.screensize
			background = Image.new("RGBA", (screen_size), (110, 110, 110, 255))
			if cls.isDebug: cls.console('# export preprocessed image','blue')
		elif isNormal:
			## set background
			screen_size = cls.screensize
			background = Image.new("RGBA", (screen_size), (0, 0, 0, 0))
			if cls.isDebug: cls.console('# export roi image','blue')

		# scale and move image to emulate stimulus presentation
		if isPreprocessed or isNormal:
			# if scale image
			if cls.scale != 1:
				old_imagesize = [image.size[0], image.size[1]]
				imagesize = [int(image.size[0] * cls.scale), int(image.size[1] * cls.scale)]
				image = image.resize(tuple(imagesize))
				if cls.isDebug:
					cls.console('image size: %s, scaled to: %s'%(old_imagesize, imagesize))
			# else unscaled
			else:
				imagesize = [int(image.size[0]), int(image.size[1])]
				if cls.isDebug: cls.console('image size: %s'%(imagesize))

			# if offsetting
			if cls.newoffset:
				offset_center = cls.recenter
				# calculate upper-left coordinate for drawing into image
				x = ((offset_center[0]) - (imagesize[0]/2)) # x-bound <offset_x center> - <1/2 image_x width>
				y = (offset_center[1]) - (imagesize[1]/2) # y-bound <offset_y center> - <1/2 image_y width>
				left_xy = (int(x),int(y))
				if cls.isDebug: cls.console('image centered at: %s'%(offset_center))
			# else not offsetting
			else:
				# calculate upper-left coordinate for drawing into image
				x = (screen_size[0]/2) - (imagesize[0]/2) # x-bound <screen_x center> - <1/2 image_x width>
				y = (screen_size[1]/2) - (imagesize[1]/2) # y-bound <screen_y center> - <1/2 image_y width>
				left_xy = (int(x),int(y))
				if cls.isDebug: cls.console('image centered at: %s'%([screen_size[0]/2,screen_size[1]/2]))

			# draw
			background.paste(image, left_xy)

			return background, imagesize

	@classmethod
	def extract_contours(cls, image, imagename, roiname):
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
		def store(image, colors):
			# post: prepare for export
			img = Image.fromarray(image)
			img = img.convert("RGBA")
			pixdata = img.load() # allow PIL processing
			width, height = img.size
			color = random.choice(cls.rgb) # apply color to ROI
			# store shape
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
			# close editing PIL image
			#img.close()

			return coord, img

		# convert pil image to grayscale (using PIL)
		#image = image.convert(mode='L')
		#imagesize = [image.size[0], image.size[1]]
		## convert to np.array
		#image = np.array(image)# image.shape: height x width x channel

		# or convert pil image to grayscale (using cv2)
		# paste image to white background, convert to RGB
		size = image.size
		image.load()
		image_RGB = Image.new("RGB", size=size, color=(255, 255, 255))
		image_RGB.paste(image, mask=image.split()[3])
		## invert image
		image_invert = ImageOps.invert(image_RGB)
		## convert to numpy
		image_np = np.array(image_invert)
		## convert to greyscale
		image_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

		# if drawing in PSD files
		if cls.isDebug: cls.console('manual ROI detection','blue')
		# threshold the image
		## note: if any pixels that have value higher than 127, assign it to 255. convert to bw for countour and store original
		_retval, threshold = cv2.threshold(src=image_gray, thresh=1, maxval=255, type=0)

		# find contours in image
		## note: if you only want to retrieve the most external contour # use cv.RETR_EXTERNAL
		contours, _hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# if contours empty raise Exception
		if not bool(contours):
			_err = [imagename, roiname, 'Not able to identify contours']
			message = '%s; %s; %s'%(_err[0],_err[1],_err[2])
			raise Exception(message)

		#------------------------------------------------------------------------for each layer: save images and contours
		#when saving the contours below, only one drawContours function from above can be run
		#any other drawContours function will overlay on the others if multiple functions are run
		#----param
		s_color = [(91,150,190,255), (247,222,168,255), (33,150,243,255), (229,28,35,255)]
		image_blank = np.full_like(image_gray, 255) ## Return an array of x with the same shape and type as a given array.
		coord = [] #store shape of each contour: approx polygon, circle, etc.
		#breakpoint()
		#----straight bounding box
		if cls.shape == 'straight':
			# cls.console('## roishape: straight bounding box','green')
			cls.shape_d = 'RECTANGLE' # dataviewer shape
			# contour
			cnt = contours[0]
			# get bounds
			_x,_y,_w,_h = cv2.boundingRect(cnt)
			# convert all coordinates floating point values to int
			roi_bounds = np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))
			# draw an individual contour
			cv2.rectangle(img=image_blank, pt1=(_x,_y), pt2=(_x+_w,_y+_h), color=(0,0,0), thickness=cv2.FILLED)
			# create coords, prepare for visualization of ROIs
			coord, image_contours = store(image_blank, s_color)
			# create bounds
			_bounds = roi_bounds
			# create contours
			_contours = image_contours

		#----rotated bounding box
		elif cls.shape == 'rotated':
			# cls.console('## roishape: rotated bounding box','green')
			cls.shape_d = 'FREEHAND' # dataviewer shape
			# contour
			cnt = contours[0]
			# get bounds
			rect = cv2.minAreaRect(cnt)
			roi_bounds = cv2.boxPoints(rect)
			# convert all coordinates floating point values to int
			roi_bounds = np.int0(roi_bounds)
			# draw an individual contour
			cv2.drawContours(image=image_blank, contours=[roi_bounds], contourIdx=-1, color=(0,0,0), thickness=cv2.FILLED)
			# create coords, prepare for visualization of ROIs
			coord, image_contours = store(image_blank, s_color)
			# create bounds
			_bounds = roi_bounds
			# create contours
			_contours = image_contours

		#----circle enclosing
		elif cls.shape == 'circle':
			# cls.console('## roishape: bounding circle','green')
			cls.shape_d = 'ELLIPSE' # dataviewer shape
			# contour
			cnt = contours[0]
			# get minimal enclosing circle
			(_x,_y),_r = cv2.minEnclosingCircle(cnt)
			# convert all coordinates floating point values to int
			roi_bounds = np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))
			# get center and radius of circle
			center = (int(_x),int(_y))
			radius = int(_r)
			# draw an individual contour
			cv2.circle(img=image_blank, center=center, radius=radius, color=(0,0,0), thickness=cv2.FILLED)
			# create coords, prepare for visualization of ROIs
			coord, image_contours = store(image_blank, s_color)
			# create bounds
			_bounds = roi_bounds
			# create contours
			_contours = image_contours

		#----Contour Approximation
		elif cls.shape == 'polygon':
			# cls.console('## roishape: approximate polygon','green')
			cls.shape_d = 'FREEHAND' # dataviewer shape
			# contour
			cnt = contours[0]
			_epsilon = 0.01 * cv2.arcLength(cnt, True)
			# get approx polygons
			polygon = cv2.approxPolyDP(curve=cnt, epsilon=_epsilon, closed=True)
			# draw approx polygons
			cv2.drawContours(image=image_blank, contours=[polygon],  contourIdx=-1, color=(0,0,0), thickness=cv2.FILLED)
			# create coords, prepare for visualization of ROIs
			coord, image_contours = store(image_blank, s_color)
			# create bounds
			_bounds = polygon[:,0,:]
			# create contours
			_contours = image_contours

		#----convex hull
		elif cls.shape == 'hull':
			# cls.console('## roishape: hull','green')
			cls.shape_d = 'FREEHAND' # dataviewer shape
			# contour
			cnt = contours[0]
			# get convex hull
			hull = cv2.convexHull(cnt)
			# draw hull
			cv2.drawContours(image=image_blank, contours=[hull], contourIdx=-1, color=(0,0,0), thickness=cv2.FILLED)
			# create coords, prepare for visualization of ROIs
			coord, image_contours = store(image_blank, s_color)
			# create bounds
			_bounds = hull[:,0,:]
			# create contours
			_contours = image_contours

		#----no shape chosen
		else:
			raise Exception('Please select either straight, rotated, circle, polygon, box, or hull shape.')

		#cls.console('test4.6', 'red')

		return _bounds, _contours, coord

	@classmethod
	def format_contours(cls, imagename, metadata, roiname, roinumber, bounds, coords):
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
		# contour bounds
		## store bounds as df
		bounds_ = pd.DataFrame(bounds)
		## transpose bounds (x0, y0, x1, y1)
		x_ = bounds_[0].unique().tolist()
		y_ = bounds_[1].unique().tolist()
		## check if bounding box has two x and y coordinate pairs
		if (((len(x_) == 1) or (len(y_) == 1)) and cls.shape == 'straight'):
			raise Exception ("Error creating bounding box for image:roi %s:%s."%(imagename, roiname))
		## set as df
		bounds = pd.DataFrame(np.column_stack([x_[0],y_[0],x_[1],y_[1]]))
		## rename
		bounds.columns = ['x0','y0','x1','y1']
		## add index, image, roi, and shape
		bounds['image'] = imagename
		bounds['roi'] = roiname
		bounds['id'] = roinumber
		bounds['shape_d'] = cls.shape_d
		## convert to int
		bounds[['x0','y0','x1','y1']] = bounds[['x0','y0','x1','y1']].astype(int)

		#contour coords
		coords = pd.DataFrame(coords, columns = ['x','y'])
		coords[['image','roi','shape']] = pd.DataFrame([[imagename, roiname, cls.shape]], index=coords.index)

		#----save roi df
		# combine metadata with bounds
		if metadata is not None:
			bounds = pd.merge(bounds, metadata, on=['image','roi'], how='outer')

		# finish
		return bounds, coords

	@classmethod
	def draw_contours(cls, filepath, img=None):
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
		# convert pil to np
		img_np = np.array(img)
		plt.imshow(img_np)
		## check folder
		filepath_ = Path(filepath).parent
		if not os.path.exists(filepath_):
			os.makedirs(filepath_)
		## save
		if cls.isDebug: cls.console('## image saved @: %s'%(filepath),'blue')

	@classmethod
	def export_data(cls, df, path, filename, uuid=None, newcolumn=None, level='image'):
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
			Nested order, either **image** or **all**. Default is **image**.

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
				uuid_column = cls.roicolumn

		#else if workng with all images
		elif level == 'all':
			# if uuid, create a unique column
			if isinstance(uuid, (list,)):
				uuid_column = 'uuid'
			# else simply use roiname
			else:
				uuid_column = cls.roicolumn

		# check if folder exists
		if not os.path.exists(path):
			os.makedirs(path)

		# export to excel
		if ((cls.roi_format == 'raw') or (cls.roi_format == 'both')):
			#if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path("%s/%s_%s.xlsx"%(path, filename, cls.append_output_name))
			else:
				filepath = Path("%s/%s.xlsx"%(path, filename))
			#save
			df.to_excel("%s"%(filepath), index=False)

			# if debug
			if cls.isDebug: cls.console("## raw data saved @: %s"%(filepath),'green')

		# export to ias (dataviewer)
		if ((cls.roi_format == 'dataviewer') or (cls.roi_format == 'both')):
			#if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path("%s/%s_%s.ias"%(path, filename, cls.append_output_name))
			else:
				filepath = Path("%s/%s.ias"%(path, filename))
			_bounds = '\n'.join(map(str, [
				"# EyeLink Interest Area Set created on %s."%(cls.now()),
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
			if cls.isDebug: cls.console("## dataviewer data saved @: %s"%(filepath),'green')

		return df

	@classmethod
	def manual_detection(cls, directory, core=0, queue=None):
		"""[summary]

		Parameters
		----------
		directory : :obj:`list`
			[description]
		core : :obj:`int`
			(if isMultiprocessing) Core used for this function. Default is **0**.
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
		l_coords_all = []
		l_error = []

		#!!!----for each image
		cls.console('starting()','purple')
		if cls.isDebug: cls.console('for each image','purple')
		for file in directory:
			# console
			if cls.isDebug and cls.isMultiprocessing: cls.console('core: %s'%(core),'orange')
			# defaults
			imgtype='psd'

			# read image
			ext = (Path(file).suffix).lower()
			## if psd
			if ext == '.psd':
				imgtype = 'psd'
				layered_image = psd_tools.PSDImage.open(file)
				imagename = os.path.splitext(os.path.basename(file))[0]
				if cls.isDebug: cls.console('\n# file: %s'%(imagename),'green')
			## else if DICOM (GIMP) 
			##!!! TODO: get working
			elif ext == '.dcm':
				breakpoint()
				imgtype = 'DICOM'
				layered_image = Image.open('%s'%(file))
				imagename = os.path.splitext(os.path.basename(file))[0]
				if cls.isDebug: cls.console('\n# file: %s'%(imagename),'green')
			else:
				error = "Image format not valid. Acceptable image formats are: psd (Photoshop) or dcm (DICOM)."
				raise Exception(error)

			# clear lists
			l_bounds = [] #list of bounds (data)
			l_contours = [] #list of contours (image)
			l_coords = [] #list of coordinates (data)
			#!!!----for each image, save image file
			# raw image
			image, imagesize = cls.format_image(image=layered_image, imgtype=imgtype, isRaw=True)
			## check folder
			_folder = '%s/img/raw/'%(cls.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path("%s/%s_%s.png"%(_folder, imagename, cls.append_output_name))
			else:
				filepath = '%s/%s.png'%(_folder, imagename)
			## save raw
			if cls.image_backend == 'PIL':
				image.save(filepath)
			else:
				fig = plt.figure()
				if cls.set_size_inches is not None: fig.set_size_inches(cls.screensize[0]/cls.dpi, cls.screensize[1]/cls.dpi)
				if cls.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if cls.tight_layout: plt.tight_layout()
				plt.imshow(image, zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig(filepath, dpi=cls.dpi, bbox_inches='tight')
				plt.close(fig)

			# preprocessed imaage (image with relevant screensize and position)
			image, imagesize = cls.format_image(image=layered_image, imgtype=imgtype, isPreprocessed=True)
			## check folder
			_folder = '%s/img/preprocessed/'%(cls.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path("%s/%s_%s.png"%(_folder, imagename, cls.append_output_name))
			else:
				filepath = '%s/%s.png'%(_folder, imagename)
			## save raw
			if cls.image_backend == 'PIL':
				image.save(filepath)
			else:
				fig = plt.figure()
				if cls.set_size_inches is not None: fig.set_size_inches(cls.screensize[0]/cls.dpi, cls.screensize[1]/cls.dpi)
				if cls.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if cls.tight_layout: plt.tight_layout()
				plt.imshow(image, zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig(filepath, dpi=cls.dpi, bbox_inches='tight')
				plt.close(fig)

			#!!!----for each region of interest
			## counter
			roinumber = 1
			## check path
			_folderpath = '%s/img/bounds/roi/'%(cls.output_path)
			if not os.path.exists(_folderpath):
				os.makedirs(_folderpath)

			## for each layer in psd (if using psd)
			#!!! TODO: get working for other image types (DICOM)
			for layer in layered_image:
				# skip if layer is main image
				if ((imgtype=='psd') and (Path(layer.name).stem == imagename)):
					continue
				else:
					#. Extract metadata for each region of interest.
					metadata, roiname = cls.extract_metadata(imagename=imagename, layer=layer, imgtype=imgtype)

					#. Resize PIL image and reposition image, relative to screensize.
					image, imagesize = cls.format_image(image=layer, imgtype=imgtype, isNormal=True)

					#. Extract cv2 bounds, contours, and coordinates from np.array(image).
					bounds, contours, coords = cls.extract_contours(image=image, imagename=imagename, roiname=roiname)

					#. Format contours as Dataframe, for exporting to xlsx or ias.
					bounds, coords = cls.format_contours(imagename=imagename, metadata=metadata, roiname=roiname, roinumber=roinumber, bounds=bounds, coords=coords)
					#. Draw contours
					## if append_output_name
					if not (cls.append_output_name is False):
						filepath = '%s/img/bounds/roi/%s.%s_%s.png'%(cls.output_path, imagename, roiname, cls.append_output_name)
					else:
						filepath = '%s/img/bounds/roi/%s.%s.png'%(cls.output_path, imagename, roiname)
					## save image
					if cls.image_backend == 'PIL':
						contours.save(filepath)
					else:
						fig = plt.figure()
						if cls.set_size_inches is not None: fig.set_size_inches(cls.screensize[0]/cls.dpi, cls.screensize[1]/cls.dpi)
						if cls.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
						if cls.tight_layout: plt.tight_layout()
						cls.draw_contours(filepath=filepath, img=contours)
						plt.title('Region of Interest')
						plt.ylabel('Screen Y (pixels)')
						plt.xlabel('Screen X (pixels)')
						plt.savefig(filepath, dpi=cls.dpi, bbox_inches='tight')
						plt.close(fig)

					#. store processed bounds and contours to combine across image
					l_bounds.append(bounds)
					l_contours.append(contours)
					l_coords.append(coords)

					#. update counter
					roinumber = roinumber + 1

			#!!!----for each image
			### if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path('%s/img/bounds/%s_%s.png'%(cls.output_path, imagename, cls.append_output_name))
			else:
				filepath = '%s/img/bounds/%s.png'%(cls.output_path, imagename)
			## save image
			if cls.image_backend == 'PIL':
				img_ = Image.new('RGBA', l_contours[0].size)
				for c in l_contours:
					#img_ = Image.blend(img_, c, 0.125)
					img_.paste(c, mask=c)
				# add opacity
				img_.putalpha(110)
				img_.save(filepath)
			else:
				fig = plt.figure()
				if cls.set_size_inches is not None: fig.set_size_inches(cls.screensize[0]/cls.dpi, cls.screensize[1]/cls.dpi)
				if cls.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if cls.tight_layout: plt.tight_layout()
				[cls.draw_contours(filepath=filepath, img=cnt) for cnt in l_contours]
				plt.title('Region of Interest')
				plt.ylabel('Screen Y (pixels)')
				plt.xlabel('Screen X (pixels)')
				plt.savefig(filepath, dpi=cls.dpi, bbox_inches='tight')
				plt.close(fig)

			# bounds
			## concatenate and store bounds for all rois
			df = pd.concat(l_bounds)
			l_bounds_all.append(df)
			## export data
			_filename = "%s_bounds"%(imagename)
			_folder = '%s/data/'%(cls.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			df = cls.export_data(df=df, path=_folder, filename=_filename, uuid=cls.uuid, newcolumn=cls.newcolumn, level='image')

			# contours
			# concatenate and store contours for all rois
			df = pd.concat(l_coords)
			l_coords_all.append(df)
			## export data
			_filename = "%s_contours"%(imagename)
			_folder = '%s/data/'%(cls.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			filepath = Path("%s/%s.h5"%(_folder, _filename))
			df.to_hdf("%s"%(filepath), key='df', format='table', mode='w', data_columns=['image','roi'])

		#!!!----finished for all images
		# store
		## if multiprocessing, store in queue
		if cls.isMultiprocessing:
			queue.put(l_bounds_all, l_coords_all)
			pass
		# if not multiprocessing, return
		else:
			return l_bounds_all, l_contours_all, l_coords_all, l_error

	@classmethod
	def haarcascade(cls, directory, core=0, queue=None):
		"""[summary]

		Parameters
		----------
		directory : [type]
			[description]
		core : int, optional
			[description], by default 0
		queue : [type], optional
			[description], by default None

		Returns
		-------
		[type]
			[description]

		Raises
		------
		Exception
			[description]
		"""
		#!!!----for each image
		cls.console('starting()','purple')
		if cls.isDebug: cls.console('for each image','purple')
		l_coords_all = []
		l_error = []
		for file in directory:
			# console
			if cls.isDebug and cls.isMultiprocessing: cls.console('core: %s'%(core),'orange')
			# defaults
			imgtype='psd'

			# read image
			ext = (Path(file).suffix).lower()
			## if psd
			if ext == '.psd':
				imgtype = 'psd'
				image = Image.open('%s'%(file))
				imagename = os.path.splitext(os.path.basename(file))[0]
				if cls.isDebug: cls.console('\n# file: %s'%(imagename),'green')
			## else if DICOM (GIMP) 
			elif ext == '.dcm':
				breakpoint()
				imgtype = 'DICOM'
				image = Image.open('%s'%(file))
				imagename = os.path.splitext(os.path.basename(file))[0]
				if cls.isDebug: cls.console('\n# file: %s'%(imagename),'green')
			## else if tiff
			elif ext in ['.tiff','.tif']:
				breakpoint()
				imgtype = 'tiff'
				image = Image.open('%s'%(file))
				imagename = os.path.splitext(os.path.basename(file))[0]
				if cls.isDebug: cls.console('\n# file: %s'%(imagename),'green')
			## else if bitmap 
			elif ext in ['.bmp','.jpeg','.jpg','.png']:
				imgtype = 'bitmap'
				image = Image.open('%s'%(file))
				imagename = os.path.splitext(os.path.basename(file))[0]
				if cls.isDebug: cls.console('\n# file: %s'%(imagename),'green')
			else:
				error = "Image format not valid. Acceptable image formats are: psd (photoshop), dcm (DICOM), tiff (multiple layers), or png/bmp/jpg (bitmap)."
				raise Exception(error)

			# clear lists
			l_coords = [] #list of coordinates (data)
			#!!!----for each image, save image file
			# raw image
			image, imagesize = cls.format_image(image=image, imgtype=imgtype, isRaw=True, isHaar=True)
			## check folder
			_folder = '%s/img/raw/'%(cls.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path("%s/%s_%s.png"%(_folder, imagename, cls.append_output_name))
			else:
				filepath = '%s/%s.png'%(_folder, imagename)
			## save raw
			if cls.image_backend == 'PIL':
				image.save(filepath)
			else:
				fig = plt.figure()
				if cls.set_size_inches is not None: fig.set_size_inches(cls.screensize[0]/cls.dpi, cls.screensize[1]/cls.dpi)
				if cls.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if cls.tight_layout: plt.tight_layout()
				plt.imshow(image, zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig(filepath, dpi=cls.dpi, bbox_inches='tight')
				plt.close(fig)

			# preprocessed imaage (image with relevant screensize and position)
			image, imagesize = cls.format_image(image=image, imgtype=imgtype, isPreprocessed=True, isHaar=True)
			## check folder
			_folder = '%s/img/preprocessed/'%(cls.output_path)
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## if append_output_name
			if not (cls.append_output_name is False):
				filepath = Path("%s/%s_%s.png"%(_folder, imagename, cls.append_output_name))
			else:
				filepath = '%s/%s.png'%(_folder, imagename)
			## save raw
			if cls.image_backend == 'PIL':
				image.save(filepath)
			else:
				fig = plt.figure()
				if cls.set_size_inches is not None: fig.set_size_inches(cls.screensize[0]/cls.dpi, cls.screensize[1]/cls.dpi)
				if cls.remove_axis: fig.tight_layout(pad=0); plt.axis('off')
				if cls.tight_layout: plt.tight_layout()
				plt.imshow(image, zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig(filepath, dpi=cls.dpi, bbox_inches='tight')
				plt.close(fig)

			# The image is read and converted to grayscale
			cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
			gray = np.array(image.convert("L"))#; cv2.imwrite(greypath, gray)

			# for each requested classifier
			for ctype in cls.classifiers:
				classifier = cls.classifiers[ctype]
				## parameters
				color = random.choice(cls.rgb)
				cregion = classifier['type']
				sF = classifier['scaleFactor']
				minN = classifier['minNeighbors']
				minS = tuple(classifier['minSize'])
				thickness = classifier['thickness']
				cpath_ =  Path(classifier['path'])
				## setup classifier
				haar = cv2.CascadeClassifier('%s'%(cpath_))
				## detect
				roi = haar.detectMultiScale(gray, scaleFactor=sF, minNeighbors=minN, minSize=minS, flags=cv2.CASCADE_SCALE_IMAGE)
				for idx, (x, y, w, h) in enumerate(roi):
					# store coords
					l_coords.append([x, y, x+x+w/2, y+y+h/2, cregion, idx, imagename])
					# draw region
					cv2.rectangle(img=cv2_image, pt1=(x,y), pt2=(x+w,y+h), color=color, thickness=thickness)
					roi_gray = gray[y:y + h, x:x + w]
					roi_color = cv2_image[y:y + h, x:x + w]

			# save image
			_folder = '%s/img/cascades/'%(cls.output_path)
			_filepath = '%s/%s.png'%(_folder, imagename)
			## check folder
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## save
			cv2.imwrite(_filepath, cv2_image)

			# save data
			_folder = '%s/data/'%(cls.output_path)
			_filepath = '%s/%s_cascades.xlsx'%(_folder, imagename)
			## check folder
			if not os.path.exists(_folder):
				os.makedirs(_folder)
			## save
			df = pd.DataFrame(l_coords, columns=['x0', 'y0', 'x1', 'y1', 'feature', 'id', 'image'])
			df.to_excel(_filepath, index=False)

			# store coords
			l_coords_all.append(df)

		#!!!----finished for all images
		# store
		## if multiprocessing, store in queue
		if cls.isMultiprocessing:
			queue.put(l_coords_all)
			pass
		# if not multiprocessing, return
		else:
			return l_coords_all, l_error

	@classmethod
	def process(cls):
		"""[summary]

		Returns
		-------
		[type]
			[description]
		"""
		# prepare arguements and procedure
		df = ''

		# if multiprocessing, get total cores
		if cls.isMultiprocessing:
			import multiprocessing

			#----get number of available cores
			_max = multiprocessing.cpu_count() - 1

			#---check if selected max or value above possible cores
			if (cls.cores == 'max') or (cls.cores >= _max):
				cls.cores = _max
			else:
				cls.cores = cls.cores

			#----double check multiproessing
			# if requested cores is 0 or 1, run without multiprocessing
			if ((cls.cores == 0) or (cls.cores == 1)):
				cls.isMultiprocessing = False
				cls.console('not multiprocessing', 'purple')
			# split directory by number of cores
			else:
				cls.isMultiprocessing = True
				l_directory = np.array_split(cls.directory, cls.cores)
				cls.console('multiprocessing with %s cores'%(cls.cores), 'purple')

		# not multiprocessing
		else:
			cls.isMultiprocessing = False
			cls.console('not multiprocessing', 'purple')

		#----prepare to run
		# if not multiprocessing
		if not cls.isMultiprocessing:
			if cls.detection == "haarcascade":
				l_coords_all, _ = cls.haarcascade(cls.directory)
				# finish
				df, error = cls.finished(df=l_coords_all)
			else:
				l_bounds_all, _, _, _ = cls.manual_detection(cls.directory)
				# finish
				df, error = cls.finished(df=l_bounds_all)

		# else if multiprocessing
		else:
			# collect each pipe (this is used to build send and recieve portions of output)
			queue = multiprocessing.Queue()

			# prepare threads
			if cls.detection == "haarcascade":
				process = [multiprocessing.Process(target=cls.haarcascade, args=(l_directory[core].tolist(), core, queue,)) for core in range(cls.cores)]
			else:
				process = [multiprocessing.Process(target=cls.manual_detection, args=(l_directory[core].tolist(), core, queue,)) for core in range(cls.cores)]

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
			if cls.isDebug: cls.console('process() finished (multiprocessing)','purple')
			df, error = cls.finished(returns)

		return df, error

	@classmethod
	def finished(cls, df, errors=None):
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
		if cls.isMultiprocessing:
			#concatenate data
			df = [i[0] for i in df if len(i) != 0] #check if lists are empty (i.e. if there are more threads than directories)
			df = pd.concat(df)
		# else combine lists of df to df
		else:
			df = pd.concat(df)

		#!!!----combine all rois across images
		if cls.detection=='manual':
			# export to xlsx or ias
			_folder = '%s/data/'%(cls.output_path)
			_filename = "bounds"
			df = cls.export_data(df=df, path=_folder, filename=_filename, uuid=cls.uuid, level='all')
		elif cls.detection=='haarcascade':
			# export to xlsx
			_folder = '%s/data/'%(cls.output_path)
			_filepath = "%s/cascades.xlsx"%(_folder)
			df.to_excel(_filepath, index=False)

		#!!!----error log
		if bool(errors):
			_filename = Path('%s/error.csv'%(cls.output_path))
			cls.console("Errors found. See log %s"%(_filename), 'red')
			error = pd.DataFrame(errors, columns=['image','roi','message'])
			error.to_csv(_filename, index=False)
		else:
			error = None

		# finished
		cls.console('finished()','purple')
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

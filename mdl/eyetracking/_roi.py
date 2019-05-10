#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Generate regions of interest that can be used for data processing and analysis.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""
# allowed imports
__all__ = ['ROI']

# required external libraries
__required__ = ['opencv-python','psd-tools','matplotlib','Pillow']

# local
from .. import settings

# required for init
from pdb import set_trace as breakpoint
import os
from pathlib import Path
import pandas as pd
import numpy as np

# plot
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# check if psd_tools and cv2 is available
# note: anaconda doesn't have a version of psd_tools or opencv-python (cv2) available (5/1/19), so a workaround 
# when building is to directly install it.
try:
	import psd_tools
	import cv2
except ImportError as e:
	import importlib, sys
	pkg = e.name
	settings.console("No module named '%s'. Installing from PyPI."%(pkg),'red')
	# install
	settings.library([pkg])
	# if not all packages are available, reload module
	for x in [['cv2','opencv-python'],['psd_tools','psd-tools']]:
		# check if module is not available
		if importlib.util.find_spec(x[0]) is None:
			settings.console('%s not available'%(x),'red')
			importlib.reload(sys.modules[__name__])
		# import modules
		else:
			try:
				settings.console(('import %s'%(mod[0]),'blue'))
				globals()[mod[0]] = importlib.import_module(mod[0])
			except ImportError as e:
				settings.console("import %s unsuccessful. Trying to install."%(mod[0]),'red')
				importlib.reload(sys.modules[__name__])

class ROI():
	"""Generate regions of interest that can be used for data processing and analysis."""
	def __init__(self, isMultiprocessing=False, image_path=None, output_path=None, metadata_source=None, 
			  roi_format='both', shape='box', roicolumn='roi', uuid=None, **kwargs):
		"""
        Initiate the mdl.eyetracking.ROI module.

		Parameters
		----------
		isMultiprocessing : :obj:`bool`
			Should the rois be generated using multiprocessing. Default `False`.
		detection : :obj:`str`
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
				* - **isDemo** : :class:`bool`
				  - Tests code with in-house images and metadata. Default is :obj:`False`.
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

		Raises
		------
		Exception
			[description]
		Exception
			[description]

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
		# demo
		self.isDemo = kwargs['isDemo'] if 'isDemo' in kwargs else False
		# multiprocessing
		self.isMultiprocessing = isMultiprocessing
		self.cores = kwargs['cores'] if 'cores' in kwargs else 'max'
		# if multiprocessing, set number of thread
		# if isMultiprocessing:
		# 	cv2.setNumThreads(0)
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

		#----shape
		# check if trying to do complex ROI using dataviewer
		if (self.shape in ['polygon', 'hull']) and (self.roi_format == "dataviewer"):
			raise Exception ("Cannot use shape %s when exporting for DataViewer. \
					Please use either 'circle', 'rotate', or 'straight' instead, or set roi_format == 'raw'."%(shape))

		#----directory
		if self.isDemo is True:
			import sys
			path = Path(sys.argv[0]).parent
			self.image_path = "%s/raw/"%(path)
			self.output_path = "%s/output/"%(path)
			metadata_source = "%s/metadata.xlsx"%(path)
		else:
			self.image_path = image_path
			self.output_path = output_path
		# set directory of files
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
			self.console('## roiname: %s'%(roiname),'blue')
			self.console('## roilabel: %s'%(roilabel),'green')

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
		# convert pil image to grayscale (using pil)
		#self.console('test4.0.5', 'red')
		image = image.convert(mode='L')

		# convert to np.array
		#self.console('test4.1.0', 'red')
		image = np.array(image)

		# or convert pil image to grayscale (using cv2)
		#self.console('test4.1.5', 'red')
		#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

		#------------------------------------------------------------------------for each layer: save images and contours
		#when saving the contours below, only one drawContours function from above can be run
		#any other drawContours function will overlay on the others if multiple functions are run
		#----param
		color = (0,0,255)
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

	def create_rois(self, imagename, metadata, roiname, roinumber, _bounds, _contours):
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

		#----save image:roi level image bounds and con
		#----save roi contours
		#!! get working: draw exact contours as coordinates
		if self.save['contours']:
			contours = _contours
		# combine metadata with coordinates
		##!!! get working

		#----save roi df
		# combine metadata with bounds
		if metadata is not None:
			bounds = pd.merge(bounds, metadata, on=['image','roi'], how='outer')

		# finish
		return bounds, contours

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
			with open("%s"%(filepath), "w") as file:
				file.write(_bounds)

			# if debug
			if self.isDebug: self.console("## dataviewer data saved @: %s"%(filepath),'green')

		return df

	def draw_image(self, imagename, data, source='bounds'):
		"""[summary]

		Parameters
		----------
		imagename : [type]
			[description]
		data : [type]
			[description]
		source : [type]
			[description]
		"""
		# draw image
		fig = plt.figure()
		ax = fig.add_subplot(111)
		## create blank image and draw to figure
		_img = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
		ax.imshow(_img)
		## for each bound draw on figure
		if source=="bounds":
			for _bounds in data:
				## get bounds
				x0 = _bounds['x0'].item()
				y0 = _bounds['y0'].item()
				x1 = _bounds['x1'].item()
				y1 = _bounds['y1'].item()
				_width = x1 - x0
				_height = y1 - y0
				ax.add_patch(patches.Rectangle((x0, y0), _width, _height))
			## draw image
			_folder = '%s/img/roi/bounds'%(self.output_path)
		## for each contour draw on figure
		elif source=="contours":
			for _contours in data:
				contours = cv2.cvtColor(_contours, cv2.COLOR_BGR2RGB)
				plt.imshow(contours, zorder=1, interpolation='bilinear', alpha=1)
			## draw image
			_folder = '%s/img/roi/contours'%(self.output_path)
		## check folder
		if not os.path.exists(_folder):
			os.makedirs(_folder)
		## save
		filepath = Path('%s/%s.png'%(_folder, imagename))
		if self.isDebug: self.console('## image saved @: %s'%(filepath),'blue')
		plt.savefig(filepath, dpi=self.dpi)
		plt.close(fig)

	def process_image(self, psd):
		"""[summary]

		Parameters
		----------
		psd :  `psd_tools.PSDImage <https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.html#psd_tools.PSDImage>`_
			Photoshop PSD/PSB file object. The file should include one layer for each region of interest.

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
				self.console('# export image','blue')
				self.console('size: %s, scaled: %s'%(_truesize, _scalesize),'green')

		# center and resize image to template screen
		background = Image.new("RGBA", (self.screensize[0], self.screensize[1]), (0, 0, 0, 0))
		offset = ((self.screensize[0] - image.size[0])//2,(self.screensize[1] - image.size[1])//2)
		background.paste(image, offset)

		return background

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

			# read image
			psd = psd_tools.PSDImage.open(file)
			imagename = os.path.splitext(os.path.basename(file))[0]
			if self.isDebug: self.console('\n# file: %s'%(imagename),'blue')

			# clear lists
			l_bounds = [] #list of bounds
			l_contours = [] #list of contours

			#!!!----for each image, save image file
			if self.save['raw']:
				#self.console('test')
				# process imaage
				image = self.process_image(psd=psd)

				# check folder
				_folder = '%s/img/'%(self.output_path)
				if not os.path.exists(_folder):
					os.makedirs(_folder)

				# figure
				fig = plt.figure()
				plt.imshow(np.array(image), zorder=1, interpolation='bilinear', alpha=1)
				plt.savefig('%s/%s.png'%(_folder, imagename), dpi=self.dpi)
				plt.close(fig)
				#self.console('test1', 'red')

			#!!!----for each region of interest
			## counter
			roinumber = 1
			## create matplotlib plot()
			## do for each roi
			for layer in psd:
				# skip if layer is main image
				if Path(layer.name).stem == imagename:
					continue
				else:
					# process metadata
					#self.console('test2', 'red')
					metadata, roiname, roilabel = self.process_metadata(imagename, layer)

					# process image
					#self.console('test3', 'red')
					image = self.process_image(layer)

					# create contours
					#self.console('test4', 'red')
					_bounds, _contours = self.create_contours(image, imagename, roiname)

					# create rois
					bounds, contours = self.create_rois(imagename, metadata, roiname, roinumber, _bounds, _contours)

					# try:
					# 	#self.console('test5', 'red')

					# except Exception as e:
					# 	# error
					# 	print(e)
					# 	#store error
					# 	l_error.append([imagename, roiname, e]) # <image><roi><error message>
					# 	# continue to next image
					# 	break

					# store processed bounds and contours to combine across image
					l_bounds.append(bounds)
					l_contours.append(contours)

					# update counter
					roinumber = roinumber + 1

			#!!!----for each image, export data
			# draw bounds
			self.draw_image(imagename, l_bounds, 'bounds')
			# draw contours
			self.draw_image(imagename, l_contours, 'contours')

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

#%% test
# drawing image
# img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image',img)

# convert img to np array
# np_img = np.array(img)
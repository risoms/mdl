#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.  
@`date`: Created on Sat May 1 15:12:38 2019  
@`author`: Semeon Risom  
@`email`: semeon.risom@gmail.com  
@`url`: https://semeon.io/d/imhr
"""
import os, sys, pathlib, pytest
from pdb import set_trace as breakpoint

# pytest
def test_run_eyetracking(args=None):
	"""Read ROI from photoshop PSD files.

	Parameters
	----------
	args : :obj:`dict`, optional
		Dict of paths used to run function, by default None.

	Returns
	-------
    df : :class:`pandas.DataFrame`
        Pandas dataframe of generated ROI's.
    error : :class:`pandas.DataFrame`
		Pandas dataframe of errors that occured during processing.
	"""
	# import imhr package
	import imhr

	# python package path
	pypath = pathlib.Path(imhr.__file__).parent
	print('pypath: %s'%(pypath))

	# local path: debugging
	localpath = pathlib.Path.cwd()
	print('localpath: %s'%(localpath))

	# image_path
	image_path = '%s/dist/roi/raw/1/'%(pypath) if args is None else args["image_path"]
	print('image_path: %s'%(image_path))

	# output_path
	output_path = '%s/dist/output/'%(pypath) if args is None else args["output_path"]
	print('output_path: %s'%(output_path))

	# metadata_source
	metadata_source = '%s/dist/roi/raw/1/metadata.xlsx'%(pypath) if args is None else args["metadata_source"]
	print('metadata_source: %s'%(metadata_source))

	# ##### initiate
	roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False, isDemo=False,
		image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
		scale=1, screensize=[1920,1080], recenter=[(1920*.5),(1080*.5)], shape='straight', 
		roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})

	# ##### start
	df, error = roi.process()

	return df, error

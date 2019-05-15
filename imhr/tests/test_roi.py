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

# get local path
localpath = pathlib.Path(__file__).parent.parent

# default parameters
params = {
	"image_path":'%s/dist/raw/'%(localpath),
	"output_path":'%s/dist/output/'%(localpath),
	"metadata_source":'%s/dist/metadata.xlsx'%(localpath)
}

# pytest
def test_generate_roi(args=None):
	"""
	Read ROI from photoshop PSD files.

	Parameters
	----------
	args : :obj:`dict`, optional
		Dict of paths used to run function, by default None.

	Returns
	-------
    df : :class:`pandas.DataFrame`
        Pandas dataframe of generated ROI's.
    df : :class:`pandas.DataFrame`
		Pandas dataframe of errors that occured during processing.
	"""
	# ##### import imhr package
	## resolve travis-ci path problem: https://stackoverflow.com/a/42194190
	# if running using travis-ci
	if os.environ.get('TRAVIS') == 'true':
		pypath = os.path.abspath('../../')
		sys.path.insert(0, pypath)
		import imhr
		args = params
	# if running locally
	else:
		pypath = os.path.abspath('../../')
		sys.path.insert(0, pypath)
		import imhr

	# python module path
	print('pypath: %s'%(pypath))

	# local path
	print('localpath: %s'%(localpath))

	# image_path
	image_path = '%s/dist/raw/'%(localpath) if args is None else args["image_path"]

	# output_path
	output_path = '%s/dist/output/'%(localpath) if args is None else args["output_path"]

	# metadata_source
	metadata_source = '%s/dist/metadata.xlsx'%(localpath) if args is None else args["metadata_source"]

	# ##### initiate
	roi = imhr.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False, isDemo=False,
		image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
		scale=1, screensize=[1920,1080], center=[(1920*.5),(1080*.5)], shape='straight', 
		roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})

	# ##### start
	df, _ = roi.process()

	return df

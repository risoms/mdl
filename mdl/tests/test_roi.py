#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@`purpose`: Create regions of interest to export into Eyelink DataViewer or statistical resources such as R and python.  
@`date`: Created on Sat May 1 15:12:38 2019  
@`author`: Semeon Risom  
@`email`: semeon.risom@gmail.com  
@`url`: https://semeon.io/d/mdl
"""
import os, sys, pathlib, argparse, re, pytest
from pdb import set_trace as breakpoint

# get local path
_path = pathlib.Path(__file__).parent

# default parameters
params = {
	"image_path":'%s/dist/raw/'%(_path),
	"output_path":'%s/dist/output/'%(_path),
	"metadata_source":'%s/dist/metadata.xlsx'%(_path)
}

# pytest
def test_generate_roi(args=None):
	"""Read ROI from photoshop PSD files.

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
	# ##### import mdl package
	## resolve travis-ci path problem: https://stackoverflow.com/a/42194190
	# if running using travis-ci
	if os.environ.get('TRAVIS') == 'true':
		modulepath = os.path.abspath('.')
		sys.path.insert(0, modulepath)
		import mdl
		args = params
	# if running locally
	else:
		modulepath = os.path.abspath('..')
		sys.path.insert(0, modulepath)
		import mdl

	# python module path
	print('pypath: %s'%(modulepath))

	# local path
	print('localpath: %s'%(_path))

	# image_path
	image_path = '%s/dist/raw/'%(_path) if args is None else args["image_path"]

	# output_path
	output_path = '%s/dist/output/'%(_path) if args is None else args["output_path"]

	# metadata_source
	metadata_source = '%s/dist/metadata.xlsx'%(_path) if args is None else args["metadata_source"]

	# ##### initiate
	roi = mdl.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False, isDemo=False,
		image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
		scale=1, screensize=[1920,1080], center=[(1920*.5),(1080*.5)], shape='straight', 
		roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})

	# ##### start
	df, _ = roi.process()

	return df

if __name__ == '__main__':
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
	sys.exit(test_run(args_))

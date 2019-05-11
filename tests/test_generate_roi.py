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

path = pathlib.Path(__file__).parent
params={
	"image_path":'%s/raw/'%(path),
	"output_path":'%s/output/'%(path),
	"metadata_source":'%s/metadata.xlsx'%(path)
}
@pytest.fixture(scope="function", autouse=True)
def args():
	return params

def test_run(args):
	# #### Read ROI from photoshop PSD files
	# ##### import mdl package
	path = pathlib.Path(__file__).parent
	sys.path.append(os.path.abspath(os.getcwd() + './../..'))
	import mdl

	# image_path
	image_path = '%s/raw/'%(path) if args["image_path"] is None else args["image_path"]

	# output_path
	output_path = '%s/output/'%(path) if args["output_path"] is None else args["output_path"]

	# metadata_source
	metadata_source = '%s/metadata.xlsx'%(path) if args["metadata_source"] is None else args["metadata_source"]

	# ##### initiate
	roi = mdl.eyetracking.ROI(isMultiprocessing=False, isDebug=True, isLibrary=False, isDemo=False,
		image_path=image_path, output_path=output_path, metadata_source=metadata_source, 
		scale=1, screensize=[1920,1080], center=[(1920*.5),(1080*.5)], shape='straight', 
		roi_format='both', uuid=['image','roi','position'], newcolumn={'position': 'center'})

	# ##### start
	df, error = roi.process()

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
	args = parser.parse_args()
	sys.exit(test_run(args))

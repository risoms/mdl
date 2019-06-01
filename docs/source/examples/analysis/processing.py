# -*- coding: utf-8 -*-
from pdb import set_trace as breakpoint
from imhr import settings, data

## parameters
console = settings.console

def summary(source, destination, metadata=None, isHTML=True):
	"""
	Generate summary from online raw data.

	Parameters
	----------
	source : :obj:`str`
		Source path.
	destination : :obj:`str`
		Destination path.
	metadata : :obj:`str`
		Metadata path.
	isHTML : :obj:`bool`
		Whether or not to export html.

	Returns
	-------
	df : :obj:`pandas.DataFrame`
		Pandas dataframe output.
	error : :obj:`pandas.DataFrame`
		Pandas dataframe error output.
	"""
	console('starting summary()', 'green')

	import glob, os
	from pathlib import Path
	import numpy as np
	import pandas as pd
	
	# constant
	df_all = []
	errors = []
	
	# get directory
	directory = glob.glob(source + "/*.csv")
	
	## for each subject
	for index, filepath in enumerate(directory):
		# filename
		name = Path(filepath).name
		console('reading: %s'%(name), 'blue')
		
		#collect metadata 
		df_ = pd.read_csv(filepath)
		
		# try reading each participants raw data
		try:
			df_ = df_[[
			 'participant',
			 'session',
			 'code',
			 'expName',
			 'date',
			 'os',
			 'gpu',
			 'heap.used',
			 'heap.limit',
			 'browser',
			 'isWebcamUsed',
			 'WebcamMessage',
			 'WebcamDevice',
			 'webcamSize.px',
			 'lum',
			 'isWindowSuccess',
			 'monitorSize.px',
			 'windowSize.px',
			 'diagonalSize.in',
			 'devicePixelRatio',
			 'isPageVisible',
			 'isFullscreen',
			 'scaling']].iloc[0].to_frame().transpose()
		
			# append to list of files
			df_all.append(df_)
		except Exception as error:
			# console message
			console('Error: file %s; error: %s'%(filepath, error), 'red')
			# store error
			errors.append([filepath, '%s'%(error)])
			pass
	
	# combine dataframes, save data
	# summary
	df = pd.concat(df_all)
	df.sort_values(by=['participant','session'])
	
	# format data
	## process date
	df['date'] = df['date'].astype(str)
	df['date'] = df['date'].apply(lambda x: x.strip().replace('_', '-'))
	df['date'] = pd.to_datetime(df['date']) # convert to pandas datetime format
	df['date'] = df['date'].astype(str)
	## gpu
	df['gpuFullName'] = df['gpu']
	df = df.drop(columns=['gpu'])
	### gpu type
	df['gpuType'] = 'integrated'
	df.loc[df['gpuFullName'].str.contains('AMD', na=False),'gpuType'] = 'dedicated'
	df.loc[df['gpuFullName'].str.contains('Nvidia', na=False),'gpuType'] = 'dedicated'
	df.loc[df['gpuFullName'].str.contains('NVIDIA', na=False),'gpuType'] = 'dedicated'
	### gpu brand
	df['gpuFullName'] = df['gpuFullName'].fillna(np.NaN)
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('ANGLE ' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('(A' , 'A'))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('(I' , 'I'))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('(N' , 'N'))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('vs_5_' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('ps_5_' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('vs_3_' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('ps_3_' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace(' 0 0)' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('(R)' , ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('(TM)', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('OpenGL', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('Engine', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('Direct3D11', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('Direct3D9Ex', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('Family', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace('Mesa DRI ', ''))
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: str(x).replace(' (Skylake GT2)', ''))  
	### remove trailing whitespace in gpu  
	df['gpuFullName'] = df['gpuFullName'].map(lambda x: x.strip())
	## webcam device
	df['WebcamDevice']  = df['WebcamDevice'].str.split().str.get(0)
	## browser
	df['browserFullName'] = df['browser'].astype(str)
	df = df.drop(columns=['browser'])
	### browser brand
	df.loc[df['browserFullName'].str.contains('Chrome', na=False),'browserBrand'] = 'Chrome'
	df.loc[df['browserFullName'].str.contains('Safari', na=False),'browserBrand'] = 'Safari'
	df.loc[df['browserFullName'].str.contains('Edge', na=False),'browserBrand'] = 'Edge'
	df.loc[df['browserFullName'].str.contains('Firefox', na=False),'browserBrand'] = 'Firefox'
	df.loc[df['browserFullName'].str.contains('IE', na=False),'browserBrand'] = 'IE'
	### browser version
	df['browserVersion'] = df['browserFullName'].map(lambda x: x.lstrip('Chrome').rstrip('aAbBcC'))
	df['browserVersion'] = df['browserVersion'].map(lambda x: x.lstrip('Safari').rstrip('aAbBcC'))
	df['browserVersion'] = df['browserVersion'].map(lambda x: x.lstrip('Edge').rstrip('aAbBcC'))
	df['browserVersion'] = df['browserVersion'].map(lambda x: x.lstrip('Firefox').rstrip('aAbBcC'))
	df['browserVersion'] = df['browserVersion'].map(lambda x: x.lstrip('IE').rstrip('aAbBcC'))
	df['browserVersion'] = df['browserVersion'].map(lambda x: x.strip())
	## os
	df['osFullName'] = df['os'].astype(str)
	df = df.drop(columns=['os'])
	###os brand
	df.loc[df['osFullName'].str.contains('Windows', na=False),'osBrand'] = 'Microsoft Windows'
	df.loc[df['osFullName'].str.contains('Mac', na=False),'osBrand'] = 'macOS'
	df.loc[df['osFullName'].str.contains('Chrome', na=False),'osBrand'] = 'Chrome OS'
	### os version
	df['osVersion'] = df['osFullName'].map(lambda x: x.lstrip('Windows').rstrip('aAbBcC'))
	df['osVersion'] = df['osVersion'].map(lambda x: x.lstrip('Mac OS X').rstrip('aAbBcC'))  
	df['osVersion'] = df['osVersion'].map(lambda x: x.lstrip('Chrome OS').rstrip('aAbBcC'))
	df['osVersion'] = df['osVersion'].map(lambda x: x.strip())
	## renaming
	df = df.rename(columns={'lum':'luminance'})

	# get metadata
	if metadata is not None:
		## import online metadata file
		df_metadata = pd.read_csv(metadata)
		df_metadata = df_metadata.drop(columns=['code', 'subsession'])
		df_metadata = df_metadata.rename(columns={'subject':'participant'})
		df_metadata = df_metadata.drop_duplicates(subset=["participant","session"], keep="first").reset_index(drop=True)
		## exclude bogus participant
		df_metadata = df_metadata[~df_metadata['participant'].isin(['5uEl74dsH2'])]
		## convert both participant columns to float
		df['participant'] = df['participant'].astype(float)
		df['session'] = df['session'].astype(float)
		df_metadata['participant'] = df_metadata['participant'].astype(float)
		df_metadata['session'] = df_metadata['session'].astype(float)
		## merge
		df = df.merge(df_metadata, on=['participant','session'])

	# number of subjects
	df_ = df.drop_duplicates(subset=["participant"], keep="first").reset_index(drop=True)
	subjectnum = df_['participant'].astype('int').to_list()

	# save
	## check folder
	_folder = str(Path(destination).parent)
	_name = Path(destination).stem
	if not os.path.exists(_folder):
		os.makedirs(_folder)
	## save data
	df['participant'] = df['participant'].astype(int)
	df['session'] = df['session'].astype(int)
	df.sort_values(by=['participant','session'])
	df.to_excel(destination, index=False)
	console('data saved to: %s'%(destination), 'green')
	## errors
	error_destination = '%s/%s_error.xlsx'%(_folder, _name)
	df_error = pd.DataFrame(errors, columns=['file','error'])
	df_error.to_excel(error_destination, index=False)
	console('errors saved to: %s'%(error_destination), 'red')

	# export html
	if isHTML:
		name = "full_summary"
		path = "/Users/mdl-admin/Desktop/r33/data/html/summary/index.html"
		title = '<b>Table 1.</b> Participant characteristics (N = %s).'%(len(subjectnum))
		footnote = "<div id='note'>N = Summary data for all participants = %s."%(len(subjectnum))
		html = data.Plot.html(df=df, path=path, name=name, source=name, title=title, footnote=footnote)

	return df, errors

def variables(df, destination):
	"""
	Output list of variables for easy html viewing.

	Parameters
	----------
	df : :class:`pandas.DataFrame`
		Pandas dataframe of raw data. This is used as a filter to prevent unused participants from being included in the data.
	destination : :obj:`str`
		The directory path to save data to.

	Returns
	-------
	df_definitions : :class:`pandas.DataFrame`
	"""
	import pandas as pd

	#blank df for appending
	df_variable = pd.DataFrame()
	
	source = {
		'bias': ['score','baseline'],
		'device': ['os','os_version','gpu','gpu_type','browser','browser_version', 'devicePixelRatio','monitorSize',
				   'windowSize','heap.used','heap.limit','WebcamMessage','webcamSize','webcam_brand','luminance',
				   'isPageVisible','is_calibrated','is_eyetracking','isFullscreen']
	}
	
	#for each source
	for key, row in source.items():
		#convert to correct formats
		df_ = df[row].iloc[:2].loc[0,:].reset_index().rename(columns={'index':'variable', 0:'example'})
		
		#add column for definitions, type; reorganize
		df_['type'] = df[row].dtypes.to_frame().reset_index().rename(columns={0:'type'})['type']
		df_['group'] = key
		df_ = df_.loc[:,['variable','type','example','group']]
		
		#if key == behavioral, add row for trialnum, and trialnum_
		if key=='behavioral':
			df_.loc[-1] = ['TrialNum','int64',1,'behavioral']
			df_.loc[-1] = ['TrialNum_','int64',1,'behavioral']
			df_.loc[-1] = ['trialType','int64',1,'behavioral']
			df_.loc[-1] = ['trialType_','object','iaps','behavioral']
		
		#append
		df_variable = df_variable.append(df_)
		
	#reset index
	df_variable = df_variable.reset_index(level=0, drop=True)
		 
	#import list of definitions and add to dataframe
	#to initially get list of variable to fill in definitions #df_variable.to_csv(definitions_path, index=None)
	
	#import definitions and merge to variables list
	definitions_path = self.config['path']['output'] + "/analysis/definitions.csv"
	df_definitions = pd.read_csv(definitions_path, float_precision='high')
	df_variable = pd.merge(df_variable, df_definitions, on='variable')
	
	#change order
	df_variable = df_variable[['variable','group','type','example','definition']]

	# export
	## check folder
	_folder = str(Path(destination).parent)
	_name = Path(destination).stem
	if not os.path.exists(_folder):
		os.makedirs(_folder)
	df_variable.to_excel(destination)
	
	return df_variable

# -*- coding: utf-8 -*-
from pdb import set_trace as breakpoint

# local
import imhr
from .. import settings, data

__required__ = ['pandas','numpy']

# check if packages ae available
try:
	import glob
	import os
	from pathlib import Path
	import numpy as np
	import pandas as pd
	import datetime
except ImportError as e:
	pkg = e.name
	x = {'cv2':'opencv-python', 'psd_tools':'psd-tools'}
	pkg = x[pkg] if pkg in x else pkg
	raise Exception("No module named '%s'. Please install from PyPI before continuing."%(pkg),'red')

class Processing():
	"""Hub for running processing and analyzing raw data."""
	@classmethod
	def __init__(self,  **kwargs):
		"""
		Hub for running processing and analyzing raw data.
		
		Parameters
		----------
		**kwargs : :obj:`str` or :obj:`None`, optional
			Optional properties to control how this class will run:

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
		"""
		self.path = Path(imhr.__file__).parent

		# get console and time
		self.console = settings.console
		self.debug = settings.debug
		self.now = settings.time

		# check library
		self.isLibrary = kwargs['isLibrary'] if 'isLibrary' in kwargs else False
		if self.isLibrary:
			settings.library(__required__)


	@classmethod
	def preprocessing(cls, source, isMultiprocessing=False, cores=0):
		"""
		Preprocessing data for formatting and initial calculations. Steps include:
		* Dates converted to ISO format.
		* Variables formatted to camelCase.
		* Variables naming patterns consistant (i.e. osFullName, browserFullName).
		* Calculations for  stimulus onset error,  DotLoc onset error, median response time, median stimulus onset error, median DotLoc onset error

		Parameters
		----------
		source : [type]
			[description]
		isMultiprocessing : bool, optional
			[description], by default False
		cores : int, optional
			[description], by default 0

		Returns
		-------
		df : :obj:`pandas.DataFrame`
			Pandas dataframe output.
		"""

		def run(cls, directory=None, core=None, queue=None):
			"""[summary]

			Parameters
			----------
			directory : [type], optional
				[description], by default None
			core : [type], optional
				[description], by default None
			queue : [type], optional
				[description], by default None

			Returns
			-------
			[type]
				[description]
			"""
			cls.console('processing.preprocessing.run(); core: %s'%(core), 'orange')
			# constants
			errors = []

			# for each subject
			for index, filepath in enumerate(directory):
				# filename
				name = Path(filepath).name
				cls.console('reading: %s'%(name), 'blue')

				#collect subject data 
				df = pd.read_csv(filepath, float_precision='high')

				# drop practice
				df = df.drop(df[(df['event']=='Prac')].index)

				# rename variables
				df = df.rename(columns={'lum':'luminance','isWindowSuccess':'isCalibrated','windowSize.px':'windowSize',
				'monitorSize.px':'monitorSize','webcamSize.px':'webcamSize','diagonalSize.in':'diagonalSize','sample_time':'sampleTime',
				'Key_Resp.rt':'KeyRespRt','Key_Resp.acc':'KeyRespAcc','DotLoc_onset.t':'dotLocOnset','Stim_onset.t':'stimOnset'})

				# calculate errors
				# stimulus onset
				df['diffStim'] = df.apply(lambda x: abs(x['stimOnset'] - 1500), axis=1)
				# dotloc onset
				df['diffDotLoc'] = df.apply(lambda x: abs(x['dotLocOnset'] - (1500 + 4500))
				if (x['trialType'] == 'iaps') else abs(x['dotLocOnset'] - abs(1500 + 3000)), axis=1)

				# get median onset error
				df['mDiffDotLoc'] = df.groupby(["participant"])['diffDotLoc'].transform('median')
				df['mDiffStim'] = df.groupby(["participant"])['diffStim'].transform('median')
				df['mRT'] = df.groupby(["participant"])['KeyRespRt'].transform('median')
				df['sAcc'] = df.groupby(["participant"])['KeyRespAcc'].transform('median')

				# format data
				## adjust size back to value before manually multiplying by devicePixelratio
				try:
					## split
					df[['monitorWidth','monitorHeight']] = df['monitorSize'].apply(lambda x: pd.Series([i for i in x.split('x')]))
					## unscale
					df['monitorWidth'] = pd.to_numeric(df['monitorWidth']) / df['devicePixelRatio']           
					df['monitorHeight'] = pd.to_numeric(df['monitorHeight']) / df['devicePixelRatio']
					# #recombine
					df["monitorSize"] = df['monitorWidth'].map(str).str.split('.').str[0] + 'x' + df['monitorHeight'].map(str).str.split('.').str[0]
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'monitor'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass
				## process date
				try:
					df['date'] = df['date'].astype(str)
					df['date'] = df['date'].apply(lambda x: x.strip().replace('_', '-'))
					df['date'] = pd.to_datetime(df['date']) # convert to pandas datetime format
					df['date'] = df['date'].astype(str)
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'date'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass
				## gpu
				try:
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
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'gpu'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass
				## webcam device
				try:
					df['WebcamDevice']  = df['WebcamDevice'].str.split().str.get(0)
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'WebcamDevice'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass
				## browser
				try:
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
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'browser'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass
				## os
				try:
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
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'os'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass
				## clean unusual dpi     
				try:
					df['devicePixelRatio'] = df['devicePixelRatio'].apply(pd.to_numeric)
				except Exception as error:
					# console message
					cls.console('Error - file %s; error: %s (%s)'%(filepath, error, 'devicePixelRatio'), 'red')
					# store error
					errors.append([filepath, '%s'%(error)])
					pass

				# resave
				## check folder
				_folder = str('%s/preprocessed/'%(Path(filepath).parent.parent.parent))
				_name = Path(filepath).stem
				_filepath = '%s/%s.csv'%(_folder,_name)
				if not os.path.exists(_folder):
					os.makedirs(_folder)				
				df.to_csv(_filepath, index=False)
				cls.console('preprocessed file saved to: %s'%(_filepath), 'blue')

			# add to multithreading queue
			if isMultiprocessing:
				#queue
				if not errors: errors = None
				queue.put(errors)

			if not isMultiprocessing:
				return errors

		# finished
		def finished(output):
			"""[summary]

			Parameters
			----------
			output : [type]
				[description]

			Returns
			-------
			[type]
				[description]
			"""
			if isMultiprocessing:
				# create df_error
				# check if errors are empty
				error = [x for x in output if x is not None]
				if error: 
					df_error = pd.DataFrame(error)
					return df_error
				else:
					return None
			else:
				return output

		# imports
		import multiprocessing

		# start
		_t0 = datetime.datetime.now()
		_f = cls.debug(message='t', source="timestamp")
		cls.console('starting processing.preprocessing()', 'green')

		# get directory
		d_ = glob.glob(source + "/*.csv")

		# check if multiproccessing
		## if requested cores is 1, run without multiprocessing
		if ((cores == 0) or (cores == 1) or (isMultiprocessing is False)):
			isMultiprocessing = False
			cls.console('processing.preprocessing() not multiprocessing', 'orange')
		## else if requested cores are less than/equal 7, and less than available cores plus 1
		elif ((cores <= 7) and (multiprocessing.cpu_count() >= cores + 1)):
			isMultiprocessing = True
			d_p = np.array_split(d_, cores)
			cls.console('processing.preprocessing() multiprocessing with %s cores'%(cores), 'orange')
		## else use less than half of total available cores
		else:
			isMultiprocessing = True
			cores = int(cores/2)
			d_p = np.array_split(d_, cores)
			cls.console('processing.preprocessing() multiprocessing with %s cores'%(cores), 'orange')

		# starting
		if not isMultiprocessing:
			# start
			output = run(d_, cores)
			# finished
			df_error = finished(output=output)
			# end
			return df_error
		else:
			# start
			## collect each pipe (this is used to build send and recieve portions of output)
			queue = multiprocessing.Queue()
			# collect each thread
			process = [multiprocessing.Process(target=run,args=(d_p[core], core, queue,)) for core in range(cores)]
			## start each thread
			for p in process:
				p.daemon = True
				p.start()
			## return queues
			# note: see https://stackoverflow.com/a/45829852
			returns = []
			for p in process:
				returns.append(queue.get())
			## wait for each process to finish
			for p in process:
				p.join()

			# finished
			df_error = finished(output=returns)
			cls.console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'green')

			# end
			return df_error

	@classmethod
	def summary(cls, source, destination, metadata=None, isHTML=True):
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

		#timestamp
		_t0 = datetime.datetime.now()
		_f = cls.debug(message='t', source="timestamp")
		cls.console('starting processing.summary()', 'green')

		# constant
		df_all = []
		errors = []

		# get directory
		directory = glob.glob(source + "/*.csv")

		## for each subject
		for index, filepath in enumerate(directory):
			# filename
			name = Path(filepath).name
			cls.console('reading: %s'%(name), 'blue')

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
				 'heap.used',
				 'heap.limit',
				 'osFullName',
				 'osBrand',
				 'osVersion',
				 'gpuFullName',
				 'gpuType',
				 'browserFullName',
				 'browserBrand',
				 'browserVersion',
				 'isWebcamUsed',
				 'WebcamMessage',
				 'WebcamDevice',
				 'webcamSize',
				 'luminance',
				 'isCalibrated',
				 'monitorSize',
				 'windowSize',
				 'diagonalSize',
				 'devicePixelRatio',
				 'isPageVisible',
				 'isFullscreen',
				 'scaling']].iloc[0].to_frame().transpose()

				# append to list of files
				df_all.append(df_)
			except Exception as error:
				# console message
				cls.console('Error - file %s; error: %s'%(filepath, error), 'red')
				# store error
				errors.append([filepath, '%s'%(error)])
				pass
		# combine dataframes, save data
		# summary
		df = pd.concat(df_all)
		df.sort_values(by=['participant','session'])

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
		cls.console('data saved to: %s'%(destination), 'blue')
		## errors
		error_destination = '%s/%s_error.xlsx'%(_folder, _name)
		df_error = pd.DataFrame(errors, columns=['file','error'])
		df_error.to_excel(error_destination, index=False)
		cls.console('errors saved to: %s'%(error_destination), 'red')

		# export html
		if isHTML:
			name = "summary"
			path = "/Users/mdl-admin/Desktop/r33/data/html/summary/index.html"
			html_title = 'Participant characteristics'
			figure_title = '<b>Table 1.</b> Participant characteristics (N = %s).'%(len(subjectnum))
			footnote = "<div id='note'>N = Summary data for all participants."
			HTML = cls.html(df=df, path=path, name=name, source=name, html_title=html_title, figure_title=figure_title, footnote=footnote)
		else:
			HTML = None

		cls.console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'green')
		return df, errors, HTML

	@classmethod
	def variables(cls, source, destination, isHTML=True):
		"""
		Output list of variables for easy html viewing.

		Parameters
		----------
		source : :obj:`str`
			Source path.
		destination : :obj:`str`
			Destination path.
		isHTML : :obj:`bool`
			Whether or not to export html.

		Returns
		-------
		df_definitions : :class:`pandas.DataFrame`
			Variables output.
		"""

		#timestamp
		_t0 = datetime.datetime.now()
		_f = cls.debug(message='t', source="timestamp")
		cls.console('starting processing.variables()', 'green')

		#collect source
		ext = (Path(source).suffix).lower()
		## if xlsx
		if ext == '.xlsx':
			df = pd.read_excel(source)
		## if csv
		if ext == '.csv':
			df = pd.read_csv(source)

		#blank df for appending
		df_v = pd.DataFrame()

		source = {
			#'bias': ['score','baseline'],
			'behavioral': ['trialNumTask','trialID','DotLoc','LEmotion','LStim','LDescription','REmotion','RStim','RDescription','trialType',
			 'isCongruent','event',
			'KeyRespRt','KeyRespAcc','mRT','sAcc','dotLocOnset','stimOnset','diffDotLoc','diffStim','mDiffDotLoc','mDiffStim'],
			'eyetracking': ['sampleNum','sampleTime','x','y'],
			'device':['participant','session','code','expName','date','gpuFullName', 'gpuType', 'browserFullName',
		       'browserBrand', 'browserVersion', 'osFullName', 'osBrand', 'osVersion','heap.used','heap.limit',
			   'isWebcamUsed','WebcamMessage','WebcamDevice', 'webcamSize','luminance','isCalibrated', 'monitorSize',
			   'windowSize','diagonalSize','devicePixelRatio','isPageVisible','isFullscreen','scaling']
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
			df_v = df_v.append(df_)

		#reset index
		df_v = df_v.reset_index(level=0, drop=True)

		#import list of definitions and add to dataframe
		#to initially get list of variable to fill in definitions #df_variable.to_csv(definitions_path, index=None)

		#import definitions and merge to variables list
		import imhr
		f_ = imhr.__file__
		p_ = str(Path(f_).parent.parent)
		s_ = '%s/imhr/dist/r33/definitions.xlsx'%(p_)
		df_d = pd.read_excel(s_)
		df_v = pd.merge(df_v, df_d, on='variable')

		#change order
		df_v = df_v[['variable','group','type','example','definition']]

		# export
		## check folder
		_folder = str(Path(destination).parent)
		_name = Path(destination).stem
		if not os.path.exists(_folder):
			os.makedirs(_folder)
		df_v.to_excel(destination)

		# export html
		if isHTML:
			name = "definitions"
			path = "/Users/mdl-admin/Desktop/r33/data/html/definitions/index.html"
			html_title = 'Participant characteristics'
			figure_title = '<b>Table 1.</b> Task Variables and Definitions.'
			HTML = html(df=df_v, path=path, name=name, source=name, html_title=html_title, figure_title=figure_title)
		else:
			HTML = None

		cls.console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'green')
		return df_v, HTML

	@classmethod
	def device(cls, source, destination, isHTML=True):
		"""
		Output list of variables for easy html viewing.

		Parameters
		----------
		source : :obj:`str`
			Source path.
		destination : :obj:`str`
			Destination path.
		isHTML : :obj:`bool`
			Whether or not to export html.

		Returns
		-------
		df_definitions : :class:`pandas.DataFrame`
			Variables output.
		"""

		#timestamp
		_t0 = datetime.datetime.now()
		_f = cls.debug(message='t', source="timestamp")
		cls.console('starting processing.variables()', 'green')
		
		df_s = pd.read_excel(source)
		# get subjects
		subjectnum = len(df_s.drop_duplicates(subset=["participant","session"], keep="first")['participant'].astype('int').to_list())
		N = subjectnum
		rows = []
		##--------os browser gpu type Webcam resolution Webcam message
		os_ = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'osBrand'].value_counts()
		for index, value in os_.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Operating System","%s"%(index), '%s (%s)'%(value,above_pct)])
		del os_

		# ##--------os_version
		os_ = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'osFullName'].value_counts()
		for index, value in os_.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Operating System version","%s"%(index), '%s (%s)'%(value,above_pct)])
		del os_
		    
		##--------browser
		browser = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'browserBrand'].value_counts()
		for index, value in browser.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Browser brand","%s"%(index), '%s (%s)'%(value,above_pct)])
		del browser

		##--------browser_version
		browser = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'browserVersion'].value_counts()
		for index, value in browser.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Browser version","%s"%(index), '%s (%s)'%(value,above_pct)])
		del browser

		##--------gpu type 
		gpu_type = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'gpuType'].value_counts()
		for index, value in gpu_type.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["GPU type","%s"%(index), '%s (%s)'%(value,above_pct)])
		del gpu_type

		##--------gpu brand
		gpu = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'gpuFullName'].value_counts()
		for index, value in gpu.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["GPU model","%s"%(index), '%s (%s)'%(value,above_pct)])
		del gpu

		##--------devicepixelratio
		display = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'devicePixelRatio'].value_counts().sort_index(axis=0)
		for index, value in display.items():
		    index = '%.2f'%(round(index, 2))
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["devicePixelRatio","%s"%(index), '%s (%s)'%(value,above_pct)])
		del display
		    
		##--------display resolution
		display = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'monitorSize'].value_counts()
		for index, value in display.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Display resolution","%s"%(index), '%s (%s)'%(value,above_pct)])
		del display

		##--------webcam message
		webcam_m = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'WebcamMessage'].value_counts()
		for index, value in webcam_m.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Webcam message","%s"%(index), '%s (%s)'%(value,above_pct)])

		##--------webcam brand
		webcamb = df_s.drop_duplicates(subset=["participant","session"], keep="first").loc[:,'WebcamDevice'].value_counts()
		for index, value in webcamb.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Webcam brand","%s"%(index), '%s (%s)'%(value,above_pct)])
		del webcamb   

		##--------Webcam resolution
		webcamr = df_s[~df_s['webcamSize'].isin(['.x.'])].drop_duplicates(subset="participant",
		                keep="first").loc[:,'webcamSize'].value_counts()
		for index, value in webcamr.items():
		    above_pct = '%.1f'%(round(value/N, 4)*100)
		    rows.append(["Webcam resolution","%s"%(index), '%s (%s)'%(value,above_pct)])
		del webcamr

		#-------to df
		descriptive = pd.DataFrame(rows)
		descriptive = descriptive.rename(columns={0:'ID',1:'Group',2:'Statistic'})
		del descriptive.index.name

		#footnote
		# export
		## check folder
		_folder = str(Path(destination).parent)
		_name = Path(destination).stem
		if not os.path.exists(_folder):
			os.makedirs(_folder)
		descriptive.to_excel(destination)

		# export html
		if isHTML:
			name = "device"
			path = "/Users/mdl-admin/Desktop/r33/data/html/device/index.html"
			html_title = 'Device characteristics'
			figure_title = '<b>Table 1.</b> Device characteristics (N = %s).'%(N)
			footnote = [
			'<div class="description">\n',
			    'N = Number of sessions for all subjects. During data collection, participants screen resolution were multiplied by the pixel density ratio, or\
			    <a class="ref" href="https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio"><i>devicePixelRatio</i></a>\
			    (i.e. width = screen.width / devicePixelRatio = 1920 * 1.5). This was done with the intent of storing true device \
			    physical resolution. However to simplify analysis using webgazer, which uses the same initial value \
			    to calculate gaze location, participants screen resolution is reverted back to its original value.\n',
			'</div>\n']
			footnote = ''.join(footnote)

			HTML = html(df=descriptive, path=path, name=name, source=name, html_title=html_title, figure_title=figure_title, footnote=footnote)
		else:
			HTML = None

		cls.console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'green')
		
		return descriptive, HTML

	@classmethod
	def demographics(cls, source, destination, isHTML=True):
		"""
		Output list of demographics for easy html viewing.

		Parameters
		----------
		source : :obj:`str`
			Source path.
		destination : :obj:`str`
			Destination path.
		isHTML : :obj:`bool`
			Whether or not to export html.

		Returns
		-------
		df_definitions : :class:`pandas.DataFrame`
			demographics output.
		"""

		#timestamp
		_t0 = datetime.datetime.now()
		_f = cls.debug(message='t', source="timestamp")
		cls.console('starting processing.variables()', 'green')
		
		#get data
		df = pd.read_excel(source)

		# rename
		df = df.rename(
			columns={
				'record_id':'participant',
				'es_age':'age',
				'es_english':'english_fluency',
				'es_student':'is_student',
				'es_austin':'austin',
				'es_smartphone':'smartphone',
				'es_vision':'is_normalvision',
				'es_corrected_vision':'is_corrective',
				'es_handedness':'is_handedness',
				'es_cigarettes':'cigarettes',
				'es_gender___1':'male',
				'es_gender___2':'female',
				'es_gender___3':'transmale',
				'es_gender___4':'transfemale',
				'es_gender___5':'genderqueer',
				'es_gender___6':'other',
				'es_gender___7':'no'
		}) 
		#normal vision
		df['is_normalvision'] = df.apply(lambda x: True if (x['is_normalvision'] == 1) else False, axis=1)
		
		#corrective
		df['is_corrective'] = df.apply(lambda x: True if (x['is_corrective'] == 1) else False, axis=1)
		

	    #create gender column
		df['gender'] = df['es_gender'].replace([1,2,3,4,5,6,7,], ['male','female','transmale','transfemale','genderqueer','other','no'])
		
		# race
		###AIAN
		race_1 = [col for col in df.columns if 'es_race___1' in col]
		race_2 = 'American Indian or Alaska Native'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == 1) else None, axis=1)
		###asian
		race_1 = [col for col in df.columns if 'es_race___2' in col]
		race_2 = 'Asian'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == 1) else None, axis=1)
		###black
		race_1 = [col for col in df.columns if 'es_race___3' in col]
		race_2 = 'Black or African American'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == 1) else None, axis=1)
		###pacific
		race_1 = [col for col in df.columns if 'es_race___4' in col]
		race_2 = 'Native Hawaiian and Other Pacific Islander'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == 1) else None, axis=1)
		###white
		race_1 = [col for col in df.columns if 'es_race___5' in col]
		race_2 = 'White'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == 1) else None, axis=1)
		###none
		race_1 = [col for col in df.columns if 'es_race___6' in col]
		race_2 = 'None of the above'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == 1) else None, axis=1)

		##collapse
		race=['American Indian or Alaska Native','Asian','Black or African American',
			  'Native Hawaiian and Other Pacific Islander','White','None of the above']
		df['race'] = df[race].apply(lambda x: '&'.join(x.dropna().astype(str)),axis=1)
		##create new mixed race group
		df.loc[df['race'].str.contains('&'), 'race'] = 'Two or more races'
		
		##convert to categorical
		df.loc[:,'race'] = df['race'].astype('category')
		##finish
		df  = df[['participant','age','is_handedness','english_fluency','is_student','is_normalvision','is_corrective','race','gender',
			   'zipcode','austin','smartphone']].reset_index(drop=True)

		# subject number
		N = len(df['participant'].unique().tolist())

		# constants
		rows = []

		#----normal vision, corrective vision, handedness, hispanic
		l_label = ['Vision','Vision','Right-Handed (%)','Austin Resident (%)','Smartphone User (%)']
		l_group = ['Normal','Corrective', 'Handedness', 'Austin local', 'Smartphone']
		l_category = ['is_normalvision','is_corrective','is_handedness','austin','smartphone']
		l_condition = [True,True,1 ,1, 1]
		#Handedness (Right), Corrective, is_corrective, True
		for label, group, category, condition in zip(l_label, l_group, l_category, l_condition):
		    #cesd low
		    df_sum = df.loc[(df[category] == condition)]
		    count = int(len(df_sum.index))
		    pct = '%.1f'%(round(count/N, 4)*100)
		    value = '%s (%s)'%(count, pct)
		    #append
		    rows.append(['%s'%(label), group, value])

		# gender, race
		l_label = ['Race','Gender']
		l_category = ['race','gender']
		for label, category in zip(l_label, l_category):
		    l_group = df[category].unique().tolist()
		    for group in l_group:
		        #cesd low
		        df_sum = df.loc[(df[category] == group)]
		        count = int(len(df_sum.index))
		        pct = '%.1f'%(round(count/N, 4)*100)
		        value = '%s (%s)'%(count, pct)
		        #append
		        group = group.title().replace('Or','or').replace('And','and').replace('Of','of').replace('The','the')
		        rows.append(['%s'%(label), group, value])


		descriptive = pd.DataFrame(rows)
		descriptive = descriptive.rename(columns={0:'ID',1:'Group',2:'Value'})

		# export html
		if True:
			name = "demographic"
			path = "/Users/mdl-admin/Desktop/r33/data/html/demographics/index.html"
			html_title = 'Demographic characteristics'
			figure_title = '<b>Table 1.</b> Demographic characteristics (N = %s).'%(N)
			footnote = [
			'<div class="description">\n',
			    'N = Number of sessions for all subjects. During data collection, participants screen resolution were multiplied by the pixel density ratio, or\
			    <a class="ref" href="https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio"><i>devicePixelRatio</i></a>\
			    (i.e. width = screen.width / devicePixelRatio = 1920 * 1.5). This was done with the intent of storing true device \
			    physical resolution. However to simplify analysis using webgazer, which uses the same initial value \
			    to calculate gaze location, participants screen resolution is reverted back to its original value.\n',
			'</div>\n']
			footnote = ''.join(footnote)

			HTML = cls.html(df=descriptive, path=path, name=name, source=name, html_title=html_title, figure_title=figure_title, footnote=footnote)
		else:
			HTML = None

		# finish
		cls.console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'green')

		return df	

	@classmethod
	def html(cls, df=None, raw_data=None, name=None, path=None, source=None, figure_title=None, intro=None, footnote=None, script="", **kwargs):
		"""
		Create HTML output.

		Parameters
		----------
		destination : :obj:`str`
			Path to save file to.
		df : :class:`pandas.DataFrame`
			Pandas dataframe of analysis results data.
		raw_data : :class:`pandas.DataFrame`
			Pandas dataframe of raw data.
		name : :obj:`str`
			(py::`if source is logit`) The name of csv file created.
		path : :obj:`str`
			The directory path of the html file.
		source : :obj:`str`
			The type of data being recieved.
		figure_title : :obj:`str`
			The title of the table or figure.
		intro : :obj:`str`
			The introduction of the group of figures or tables.
		footnote : :obj:`str`
			The footnote of the table or figure.
		metadata : :obj:`dict`
			Additional data to be included.
		**kwargs : :obj:`str`, :obj:`int`, or :obj:`None`, optional
			Additional properties, relevent for specific content types. Here's a list of available properties:

			These properties control additional parameters for displaying figures:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **html_title** : :obj:`str`
				  - HTML title. This is visible on as a header for the html page.
				* - **metadata** : :obj:`str`
				  - Additional data to be included.


			While these properties control additional parameters for displaying bokeh plots:

			.. list-table::
				:class: kwargs
				:widths: 25 50
				:header-rows: 1

				* - Property
				  - Description
				* - **short**, **long** : :obj:`str`
				  - Short (aoi) and long form (Area of Interest) label of html page. This is primarily used for constructing metadata tags in html.
				* - **display** : :obj:`str`
				  - (For bokeh) The type of calibration/validation display.
				* - **trial** : :obj:`str`
				  - (For bokeh) The trial number for the eyetracking task.
				* - **session** : :obj:`int`
				  - (For bokeh) The session number for the eyetracking task.
				* - **day** : :obj:`str`
				  - (For bokeh) The day the eyetracking task was run.
				* - **bokeh_type** : :obj:`str`
				  - (If Bokeh) Control directory location. If trial, create trial plots.

		Returns
		-------
		html : :obj:`str`
			String of html code.
		"""
		# kwargs
		html_title = 'imhr: %s'%(kwargs['html_title']) if 'html_title' in kwargs else 'imhr'

		#----initiate fonts
		data.Plot.__font__()

		#timestamp
		date = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
		_t0 = datetime.datetime.now()
		_f = cls.debug(message='t', source="timestamp")
		cls.console('starting processing.html()', 'green')

		#---copy csv, imhr, js files to each model
		#copy files
		from pathlib import Path
		for folder in ['css','img','js']:
			f_ = imhr.__file__
			p_ = str(Path(f_).parent.parent)
			s_ = '%s/docs/source/_templates/html/%s/'%(p_, folder)
			d_ = '%s/%s/'%(os.path.dirname(path), folder)
			#shutil.move(s_, d_)
			import distutils
			distutils.dir_util.copy_tree(s_, d_)

		#all other html
		if True:
			#build header
			link = []; css = []; js = []
			link.append('<title>%s</title>'%(html_title))
			link.append('<meta name="title" content="%s">'%(html_title))
			link.append('<meta name="description" content="Results from our feasibility study for in-browser eyetracking.">')
			link.append('<meta name="author" content="Semeon Risom">')
			link.append('<meta name="email" content="semeon.risom@gmail.com">')
			link.append('<meta name="robots" content="index,follow">')
			link.append('<meta name="AdsBot-Google" content="noindex">')
			link.append('<!--size-->')
			link.append('<meta name="viewport" content="width=device-width, initial-scale=1.0" charset="utf-8"/>')
			link.append('<!--no cache-->')
			link.append('<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>')
			link.append('<meta http-equiv="Pragma" content="no-cache"/>')
			link.append('<meta http-equiv="Expires" content="0"/>')
			link.append('<meta name="msapplication-TileColor" content="#FFFFFF">')
			link.append('<meta name="msapplication-TileImage" content="imhr/favicon/favicon.png">')
			link.append('<meta name="msapplication-config" content="docs/favicon/browserconfig.xml">')
			link.append('<!--icons-->')
			link.append('<link rel="shortcut icon" href="imhr/favicon/favicon.ico">')
			link.append('<link rel="icon" sizes="16x16 32x32 64x64" href="imhr/favicon/favicon.ico">')
			link.append('<link rel="icon" type="image/png" sizes="196x196" href="imhr/favicon/favicon-192.png">')
			link.append('<link rel="icon" type="image/png" sizes="160x160" href="imhr/favicon/favicon-160.png">')
			link.append('<link rel="icon" type="image/png" sizes="96x96" href="imhr/favicon/favicon-96.png">')
			link.append('<link rel="icon" type="image/png" sizes="64x64" href="imhr/favicon/favicon-64.png">')
			link.append('<link rel="icon" type="image/png" sizes="32x32" href="imhr/favicon/favicon-32.png">')
			link.append('<link rel="icon" type="image/png" sizes="16x16" href="imhr/favicon/favicon-16.png">')
			link.append('<link rel="apple-touch-icon" href="imhr/favicon/favicon-57.png">')
			link.append('<link rel="apple-touch-icon" sizes="114x114" href="imhr/favicon/favicon-114.png">')
			link.append('<link rel="apple-touch-icon" sizes="72x72" href="imhr/favicon/favicon-72.png">')
			link.append('<link rel="apple-touch-icon" sizes="144x144" href="imhr/favicon/favicon-144.png">')
			link.append('<link rel="apple-touch-icon" sizes="60x60" href="imhr/favicon/favicon-60.png">')
			link.append('<link rel="apple-touch-icon" sizes="120x120" href="imhr/favicon/favicon-120.png">')
			link.append('<link rel="apple-touch-icon" sizes="76x76" href="imhr/favicon/favicon-76.png">')
			link.append('<link rel="apple-touch-icon" sizes="152x152" href="imhr/favicon/favicon-152.png">')
			link.append('<link rel="apple-touch-icon" sizes="180x180" href="imhr/favicon/favicon-180.png">')
			js.append('<!--all-->')
			js.append('<script type="text/javascript" language="javascript" src="js/jquery/jquery-3.2.1.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/lodash.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/bootstrap/bootstrap.bundle.js"></script>')
			link.append('<!--dataTables-->')
			css.append('<link rel="stylesheet" type="text/css" href="css/bootstrap/bootstrap.min.css">')
			css.append('<link rel="stylesheet" type="text/css" href="css/datatables/dataTables.bootstrap.min.css">')
			css.append('<link rel="stylesheet" type="text/css" href="css/datatables/responsive.bootstrap.min.css">')
			css.append('<link rel="stylesheet" type="text/css" href="css/datatables/buttons.bootstrap.min.css">')
			js.append('<!--user-->')
			link.append('<link rel="stylesheet" type="text/css" href="css/user.css">')
			js.append('<!--dataTables-->')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/jquery.dataTables.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.rowsGroup.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.rowGroup.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.bootstrap.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.buttons.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/buttons.bootstrap.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.responsive.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/responsive.bootstrap.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/buttons.html5.min.js"></script>')
			js.append('<script type="text/javascript" language="javascript" src="js/datatables/jszip.min.js"></script>')
			js.append('<!--user-->')
			js.append('<script type="text/javascript" language="javascript" src="js/user.js"></script>')
			js.append('<script>source="%s"</script>'%(source))

			# finish header
			head = ('\n\t'.join(map(str, link))) + ('\n\t'.join(map(str, css))) + ('\n\t'.join(map(str, js)))

			#if not displaying seaborn plots
			if True:         
				#build body
				##save table to html for datatable
				if ((source == "demographic") or (source == "device") or (source == "task")):
					index = False
					#allow word wrapping
					if(source == "demographic") or (source == "task"):
						wrap = "wrap"
					else:
						wrap = "nowrap"
					# save table to csv for downloading
					## check if paths exist
					_folder = '%s/csv'%(Path(path).parent)
					p_ = '%s/%s.csv'%(_folder, name)
					if not os.path.exists(_folder):
						os.makedirs(_folder)
					df.to_csv(p_, index=index)
					#get table
					table = df.to_html(index=index, index_names=True).replace('<table border="1" class="dataframe">',
					'<table id="table" class="table '+source+' table-striped table-bordered \
					hover dt-responsive '+wrap+'" cellspacing="0" width="100%">').replace('&gt;','>').replace('&lt;','<')
				elif (source == "definitions"):
					index = False
					#wordwrap
					wrap = "nowrap"
					#prevent trucating strings
					width = pd.get_option('display.max_colwidth')
					pd.set_option('display.max_colwidth', -1)
					##save table to csv for downloading
					_folder = '%s/csv'%(Path(path).parent)
					p_ = '%s/%s.csv'%(_folder, name)
					if not os.path.exists(_folder):
						os.makedirs(_folder)
					df.to_csv(p_, index=index)
					#get table
					table = df.to_html(index=index).replace('<table border="1" class="dataframe">',
					'<table id="table" class="table '+source+' table-striped table-bordered \
					hover dt-responsive '+wrap+'" cellspacing="0" width="100%">')   
					#reset
					pd.set_option('display.max_colwidth', width)
				elif ((source == "summary")):
					index = True
					df = df.rename_axis("index", axis="columns")
					#prevent trucating strings
					width = pd.get_option('display.max_colwidth')
					pd.set_option('display.max_colwidth', -1)
					##save table to csv for downloading #here saving raw data for future analysis
					_folder = '%s/csv'%(Path(path).parent)
					p_ = '%s/%s.csv'%(_folder, name)
					if not os.path.exists(_folder):
						os.makedirs(_folder)
					df.to_csv(p_, index=index)
					#get table
					table = df.to_html(index=index, index_names=True).replace('<table border="1" class="dataframe">',
					'<table id="table" data-file="'+ name +'" class="table '+source+' table-striped table-bordered \
					hover dt-responsive nowrap" cellspacing="0" width="100%">')
					#reset
					pd.set_option('display.max_colwidth', width)
				else:
					index = True
					#prevent trucating strings
					width = pd.get_option('display.max_colwidth')
					pd.set_option('display.max_colwidth', -1)
					##save table to csv for downloading #here saving raw data for future analysis
					_folder = '%s/csv'%(Path(path).parent)
					p_ = '%s/%s.csv'%(_folder, name)
					if not os.path.exists(_folder):
						os.makedirs(_folder)
					df.to_csv(p_, index=index)
					#get table
					table = df.to_html(index=index, index_names=True).replace('<table border="1" class="dataframe">',
					'<table id="table" data-file="'+ name +'" class="table '+source+' table-striped table-bordered \
					hover dt-responsive nowrap" cellspacing="0" width="100%">')
					#reset
					pd.set_option('display.max_colwidth', width)

				#add images to bottom of model
				if True:
					html_plots = ""

				##body
				body = ['<div class="container-large %s" style="">'%(source),
							'<div class="container" style="">',
								'<div class="dashboard-main">',
									'<div class="table-container %s">'%(source),
										'<div class="title">'+'%s'%(figure_title)+'</div>',
										'<div class="date"> Last Updated: '+'%s'%(date),
											'<span class="link" id="code">code</span>',
											'<span class="link" id="csv">csv</span>',
										'</div>',
									'<div class="dataTables_wrapper form-inline dt-bootstrap">',
										'<!--script-->',
										table,
									'</div>',
									'<div class="footnote">' + '\n' + '%s'%(footnote) + '</div>',
										html_plots,
									'</div>',
								'</div>',
							'</div>',
						'</div>']
				#replace script within body, then join as string
				if ((source == "logit") or (source == "onset") or (source == "anova")):
					body = [script if x==(                '<!--script-->') else x for x in body]
				# join
				body = ('\n\t'.join(map(str, body)))

				#build footer
				if True:
					foot = ['<script>',
								'$(document).ready(function(){',
									'getLogitTable();',
								'})',
							'</script>']
				foot = ('\n\t'.join(map(str, foot)))

				#build html
				html = ['<html>',
						'<head>',
							head,
						'</head>',
						'<body id="body">',
							body,
						'</body>',
						'<foot>',
							foot,
						'</foot>',
						'</html>']
				html = ('\n'.join(map(str, html)))

		#----save
		# check if paths exist
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))
		# tidy html
		#html = re.sub("\s\s+", " ", html) #multiple spaces
		# save
		with open(path,'w') as html_:
			html_.write(html)
		cls.console('saved html file at %s'%(path), 'blue')

		#--------finished
		cls.console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'green')
		return html

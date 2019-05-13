#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
| @purpose: Process participants metadata for analysis and export.  
| @date: Created on Sat May 1 15:12:38 2019  
| @author: Semeon Risom  
| @email: semeon.risom@gmail.com  
| @url: https://semeon.io/d/R33-analysis  
"""

# available classes and functions
__all__ = ['Metadata']

# required external libraries
__required__ = ['pandas','numpy','json']

# core
from pdb import set_trace as breakpoint
import os
import pandas as pd
import numpy as np
import json

# local libraries
if __name__ == '__main__':
	from . import settings

class Metadata():
	"""Process participants metadata for analysis and export."""
	def __init__(self, isLibrary=False):
		"""
		Initiate the mdl.r33.Metadata module.

        Parameters
        ----------
        isLibrary : :obj:`bool`
            Check if required libraries are available. Default `False`.
        """
        #check libraries
		if isLibrary:
			settings.library(__required__)

	@classmethod
	def summary(cls, df, path):
		"""
		Preparing data for use in analysis.

		Parameters
		----------
		df : :obj:`str`
			Pandas dataframe of raw data.
		path : :obj:`str`
			The directory path of the subject data

		Attributes
		----------
		path : :obj:`str`
			Specific directory path used.
		attr2 : :obj:`str`, optional
			Description of `attr2`.

		Returns
		-------
		df : :class:`numpy.ndarray`
			Pandas dataframe of processed metadata.

		Notes
		-----    
		You can either get data from all files within a directory (directory), or from a specific
		subject (subject_session).

		Examples
		--------
		>>> #if using path:
		>>> df = getData(path=self.config['path'])

		>>> #if getting data for single subject:
		>>> df = getData(path=self.config['path'],subject_session=['1099','1', '0'])

		"""

		#drop subject 111111, 999999, nan
		df = df.drop(df[(df['participant']==111111)|(df['participant']==999999)].index)
		df['participant'] = df['participant'].apply(pd.to_numeric)

		"""processing data"""
		#rename browser, os, date
		df.rename(columns={'browser':'browser_old','os':'os_old','date':'date_old'}, inplace=True)

		"""gpu_type"""
		df['gpu_type'] = 'integrated'
		df.loc[df['gpu'].str.contains('AMD', na=False),'gpu_type'] = 'dedicated'
		df.loc[df['gpu'].str.contains('Nvidia', na=False),'gpu_type'] = 'dedicated'
		df.loc[df['gpu'].str.contains('NVIDIA', na=False),'gpu_type'] = 'dedicated'
	
		"""webcam brand"""
		df['webcam_brand']  = df['WebcamDevice'].str.split().str.get(0)

		"""webcam width"""
		#replace "-1" with ".x."
		df['webcamSize.px'] = df['webcamSize.px'].apply(lambda x: '.x.' if (x == -1) else x)
		#replace ""0x0"" with ".x."
		df['webcamSize.px'] = df['webcamSize.px'].apply(lambda x: '.x.' if (x == "0x0") else x)
		df[['webcamWidth','webcamHeight']] = df['webcamSize.px'].apply(lambda x: pd.Series([i for i in x.split('x')]))

		"""window width"""
		df[['windowWidth','windowHeight']] = df['windowSize.px'].apply(lambda x: pd.Series([i for i in x.split('x')]))

		"""monitor width"""
		df['monitorSize old'] = df['monitorSize.px']
		#adjust size back to value before manually multiplying by devicePixelratio
		df[['monitorWidth','monitorHeight']] = df['monitorSize.px'].apply(lambda x: pd.Series([i for i in x.split('x')]))
		df['monitorWidth'] = pd.to_numeric(df['monitorWidth']) / df['devicePixelRatio']           
		df['monitorHeight'] = pd.to_numeric(df['monitorHeight']) / df['devicePixelRatio']

		"""browser"""
		df['browser'] = 'None'
		###new column for version without number
		df.loc[df['browser_old'].str.contains('Chrome', na=False),'browser'] = 'Chrome'
		df.loc[df['browser_old'].str.contains('Safari', na=False),'browser'] = 'Safari'
		df.loc[df['browser_old'].str.contains('Edge', na=False),'browser'] = 'Edge'
		df.loc[df['browser_old'].str.contains('Firefox', na=False),'browser'] = 'Firefox'
		df.loc[df['browser_old'].str.contains('IE', na=False),'browser'] = 'IE'

		df['browser_version'] = 'None'
		###new column for version without number
		df['browser_version'] = df['browser_old'].map(lambda x: x.lstrip('Chrome').rstrip('aAbBcC'))
		df['browser_version'] = df['browser_old'].map(lambda x: x.lstrip('Safari').rstrip('aAbBcC'))
		df['browser_version'] = df['browser_old'].map(lambda x: x.lstrip('Edge').rstrip('aAbBcC'))
		df['browser_version'] = df['browser_old'].map(lambda x: x.lstrip('Firefox').rstrip('aAbBcC'))
		df['browser_version'] = df['browser_old'].map(lambda x: x.lstrip('IE').rstrip('aAbBcC'))

		"""os"""
		df['os'] = 'None'
		###new column for version without number
		df.loc[df['os_old'].str.contains('Windows', na=False),'os'] = 'Microsoft Windows'
		df.loc[df['os_old'].str.contains('Mac', na=False),'os'] = 'macOS'
		df.loc[df['os_old'].str.contains('Chrome', na=False),'os'] = 'Chrome OS'
	
		"""os version"""
		df['os_version'] = 'None'
		###new column for version without name
		df['os_version'] = df['os_old'].map(lambda x: x.lstrip('Windows').rstrip('aAbBcC'))
		df['os_version'] = df['os_version'].map(lambda x: x.lstrip('Mac OS X').rstrip('aAbBcC'))  
		df['os_version'] = df['os_version'].map(lambda x: x.lstrip('Chrome OS').rstrip('aAbBcC'))

		"""date"""
		##process date
		df['date'] = [x.strip().replace('_', '-') for x in df['date_old']] ##remove underscore
		df['date'] = pd.to_datetime(df['date']) #convert to pandas datetime format
		df['date'] = df['date'].dt.date #remove time
		df['date'] = df['date'].astype(str)

		#rename
		df = df.rename(columns={'windowSize.px':'windowSize','monitorSize.px':'monitorSize',\
										'webcamSize.px':'webcamSize','lum':'luminance'})

		#convert to cm
		df['diagonalSize.cm'] = df['diagonalSize.in'].map(lambda x: round(x * 2.54, 3))

		"""
		clean unusual resolutions for monitor 
		"""  
		#rev = df['monitorSize'].apply(lambda x: pd.Series([i for i in x.split('x')]))
		#rev.rename(columns={0:'monitorWidth',1:'monitorHeight'},inplace=True)

		#convert to integer
		df['monitorWidth'] = df['monitorWidth'].apply(pd.to_numeric)
		df['monitorHeight'] = df['monitorHeight'].apply(pd.to_numeric)

		#recombine
		df["monitorSize"] = df['monitorWidth'].map(str).str.split('.').str[0] + 'x' + \
							df['monitorHeight'].map(str).str.split('.').str[0]
		"""
		clean unusual dpi   
		"""    
		df['devicePixelRatio'] = df['devicePixelRatio'].apply(pd.to_numeric)

		'''
		modify gpu columns
		'''
		df['gpu'] = df['gpu'].fillna(np.NaN)
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('ANGLE ' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('(A' , 'A'))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('(I' , 'I'))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('(N' , 'N'))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('vs_5_' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('ps_5_' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('vs_3_' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('ps_3_' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace(' 0 0)' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('(R)' , ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('(TM)', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('OpenGL', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('Engine', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('Direct3D11', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('Direct3D9Ex', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('Family', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace('Mesa DRI ', ''))
		df['gpu'] = df['gpu'].map(lambda x: str(x).replace(' (Skylake GT2)', ''))

		"""
		clean white space in column
		"""    
		#remove trailing whitespace in gpu  
		df['gpu'] = df['gpu'].map(lambda x: x.strip())

		'''
		split WebcamDevice to retrieve vendor id and fix formatting
		'''
		##format to np.Nan if x=-1
		df['webcamSize'] = df['webcamSize'].map(lambda x: 
			np.NaN if x=='0x0' else np.where(x==-1, np.NaN, x))

		##format to np.Nan if x=-1
		df['WebcamDevice'] = df['WebcamDevice'].map(lambda x: 
			np.NaN if x==-1 else str(x).replace('(Built-in) ', ''))
		#df['WebcamDeviceVendor'] = df['WebcamDeviceVendor'].map(lambda x: x[x.find("(")+1:x.find(")")])
		df[['WebcamDeviceProductID']] = df['WebcamDevice'].str.split('\(|\)', expand=True).iloc[:,[1]]

		#rename variables
		df = df.rename(columns={'trialNumTask':'TrialNum','Key_Resp.resp':'RT','isWebcamUsed':'is_eyetracking'})
		#drop columns
		cols = ['sampleNum', 'x', 'y', 'duration.t', 'Stim_onset.t', 'DotLoc_onset.t', 'blockNum',\
				'trialNum', 'TrialNum', 'trialID', 'Key_Resp.rt', 'Key_Resp.cresp', 'Key_Resp.acc',\
				'DotLoc', 'LEmotion', 'LStim', 'LDescription', 'REmotion', 'RStim', 'RDescription', 
				'trialType','isCongruent', 'event', 'trial_type', 'internal_node_id', 'RT']
		#drop columns
		# cols = ['sampleNum', 'timestamp', 'x', 'y', 'duration.t', 'Stim_onset.t', 'DotLoc_onset.t', 'blockNum',\
		#          'trialNum', 'TrialNum', 'trialID', 'Key_Resp.rt', 'Key_Resp.resp', 'Key_Resp.cresp', 'Key_Resp.acc',\
		#          'DotLoc', 'LEmotion', 'LStim', 'LDescription', 'REmotion', 'RStim', 'RDescription', 'trialType',\
		#          'isCongruent', 'event', 'trial_type', 'internal_node_id', 'type', 'RT', 'marker', 'bad', 'sg_x',\
		#          'sg_y', 'sg_class', 'left_bound', 'right_bound', 'sg_fix_all', 'sg_fix_index', 'sg_roi_bounds',\
		#          'sg_fix_roi']
		df.drop(cols, inplace=True, axis=1)

		#------------------------------------------------save
		print("demographics saved: %s"%(path))
		df.to_csv(path, index=False)

		return df

	@classmethod
	def predict(cls, df):
		"""
		Predicting screen size (cm), device (i.e. macbook 2018).

		Parameters
		----------
		df : :class:`numpy.ndarray`
			Pandas dataframe of raw data.

		Returns
		-------
		df : :class:`numpy.ndarray`
			Pandas dataframe of raw data.
		"""
		#clean up sub-version of data
		df['os_version'] = np.where(df['os'] == 'OSX',\
											df['os_version'].map(lambda x: x.replace(r'[^.]+', '')[:-2]),\
											df['os_version']) #else
		"""
		import screensize sample list
		"""
		#import reference screen size
		screensize_path = os.path.abspath(__file__+ '../../../info')
		df_screensize = pd.read_excel(screensize_path+'/screensize.xlsx')
		df_screensize = df_screensize.rename(columns={'resolution (px)': 'monitorSize'}) #rename for merge
		df_screensize = df_screensize.rename(columns={'gpu': 'gpu list'}) #rename for merge

		#remove excel non-breaking space \xa0
		df_screensize['gpu list'] = df_screensize['gpu list'].replace({'\\xa0': ' '}, regex=True) 
		df_screensize['device'] = df_screensize['device'].replace({'\\xa0': ' '}, regex=True) 
		df_screensize['model id'] = df_screensize['model id'].replace({'\\xa0': ' '}, regex=True) 

		#clear leading and trailing white space in string
		df_screensize['gpu list'] = df_screensize['gpu list'].astype(str).map(lambda x: x.strip())

		#convert inches to cm
		df_screensize['screen size (cm)'] = df_screensize['screen size (in)'].map(lambda x: round(x * 2.54, 3))
		tt=df_screensize['gpu list'][0]

		#convert each gpu cell into a list
		#https://stackoverflow.com/a/47548471
		#https://stackoverflow.com/questions/38133961/pandas-how-to-store-a-list-in-a-dataframe
		#https://stackoverflow.com/questions/35565376/insert-list-of-lists-into-single-column-of-pandas-df
		df_screensize['gpu list']=df_screensize['gpu list'].map(lambda x: list(map(str.strip,x.split(","))))

		'''
		merge location (lab or home) df and df_summary data
		'''
		df_all = pd.merge(df, df_summary[['participant','session','location']],on=['participant','session'], how='left')
		df_all.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		df_lab=df_all.copy().reset_index(drop=True)
	
		'''
		lab computer (if: subject is in lab and using one of the lab machines)
		'''
		#filter
		df_screensize_filter=df_screensize.copy().reset_index(drop=True)
		df_screensize_filter = df_screensize_filter.loc[df_screensize['is lab computer'] == True].reset_index(drop=True)    
		df_screensize_filter['location'] = 'lab'
		df_screensize_filter['exact match'] = True

		#preparing new variables for df_osx
		df_screensize_filter['devices'] = df_screensize_filter['device'] 
		df_screensize_filter['model id'] = df_screensize_filter['model id']
		df_screensize_filter['resolution (px)'] = df_screensize_filter['monitorSize']

		#combine all    
		df_lab = pd.merge(df_lab,df_screensize_filter[['os','gpu list','monitorSize','location','screen size (cm)',\
														'pixel density (ppi)','exact match',\
														'devices','model id', 'resolution (px)']],\
														on=['os','monitorSize','location'], how='left')
		df_lab = df_lab.loc[df_lab['exact match'] == True].reset_index(drop=True) 
		df_lab.sort_values(by=['participant','session','subsession']).reset_index(drop=True)

		#save summary
		types_df_lab = df_lab.dtypes
		df_test = df_lab[['participant','session','subsession','os','os_version','gpu',\
								'diagonalSize.cm','screen size (cm)','gpu list','exact match']]
		df_test.to_excel(cwd_save+'/lab_summary.xlsx', index=False)
	
		'''
		osx devices
		'''
		#filter
		df_screensize_filter=df_screensize.copy().reset_index(drop=True)
		df_screensize_filter = df_screensize.loc[df_screensize['os'] == 'OSX'].reset_index(drop=True)
		df_osx = df_all.loc[df_all['os'] == 'OSX'].reset_index(drop=True)
		df_osx.sort_values(by=['participant','session','subsession']).reset_index(drop=True)

		#check each gpu to see if there is more than one matching
		df_osx['gpu list'] = 'nan' #gpu list
		df_osx['screen size (cm)'] = 'nan' #screen size
		df_osx['pixel density (ppi)'] = 'nan' #pixel density
		df_osx['exact match'] = 'nan' #only single match
		df_osx['devices'] = 'nan' #devices
		df_osx['model id'] = 'nan' #model id
		df_osx['resolution (px)'] = 'nan' #resolution
		for idx, rw in df_osx.iterrows():
			gpu = rw['gpu']
			l_match_d = [] #matching devices
			l_match_mid = [] #matching model id
			l_match_ss = [] #matching screen size
			l_match_res = [] #matching resolution
			l_match_gpu = [] #matching gpu
			l_match_px = [] #matching pixel density
			#for each device
			for index, row in df_screensize_filter.iterrows():
				#l_row = map(str.strip, row['gpu list']) #strip items in list
				l_row = row['gpu list']
				#if gpu in list
				if [x for x in l_row if gpu.lower() in x.lower()].__len__() > 0:
					#add device to list 
					l_match_d.append(str(row['device']))
					l_match_mid.append(str(row['model id']))
					l_match_gpu.append(str(row['gpu list']))
					l_match_px.append(str(row['pixel density (ppi)']))
					l_match_ss.append(str(row['screen size (cm)']))
					l_match_res.append(str(row['monitorSize']))
			
			#if no matches
			if l_match_d.__len__() == 0:
				df_osx['devices'][idx] = 'nan'
				df_osx['model id'][idx] = 'nan'
				df_osx['gpu list'][idx] = 'nan'
				df_osx['pixel density (ppi)'][idx] = 'nan'
				df_osx['screen size (cm)'][idx] = 'nan'
				df_osx['resolution (px)'][idx] = 'nan'
				df_osx['exact match'][idx] = False
	
			#if only one device add immediately            
			elif l_match_d.__len__() == 1:
				df_osx['devices'][idx] = l_match_d[0]
				df_osx['model id'][idx] = l_match_mid[0]
				df_osx['gpu list'][idx] = l_match_gpu[0]
				df_osx['pixel density (ppi)'][idx] = l_match_px[0]
				df_osx['screen size (cm)'][idx] = l_match_ss[0]
				df_osx['resolution (px)'][idx] = l_match_res[0]
				df_osx['exact match'][idx] = True    
		
			#if multiple matches
			elif l_match_d.__len__() > 1:
				#add device to dataframe
				df_osx['devices'][idx] = l_match_d
				df_osx['model id'][idx] = l_match_mid
				df_osx['gpu list'][idx] = l_match_gpu
				df_osx['pixel density (ppi)'][idx] = l_match_px
				df_osx['screen size (cm)'][idx] = l_match_ss
				df_osx['resolution (px)'][idx] = l_match_res
				df_osx['exact match'][idx] = False

		#save summary
		types_df_osx = df_osx.dtypes
		df_test = df_osx[['participant','session','subsession','os','os_version','gpu',\
								'diagonalSize.cm','screen size (cm)','gpu list','exact match']]
		df_test.to_excel(cwd_save+'/osx_summary.xlsx', index=False)

		'''
		chromebook devices
		'''
		#filter
		df_screensize_filter = df_screensize.loc[df_screensize['os'] == 'Chrome'].reset_index(drop=True)
		df_chrome = df_all.loc[df_all['os'] == 'Chrome'].reset_index(drop=True)
		df_chrome.sort_values(by=['participant','session','subsession']).reset_index(drop=True)


		'''#----------------------------attempt 1'''
		#check each gpu to see if there is more than one matching
		df_chrome['gpu list'] = 'nan' #gpu list
		df_chrome['screen size (cm)'] = 'nan' #screen size
		df_chrome['pixel density (ppi)'] = 'nan' #pixel density
		df_chrome['exact match'] = 'nan' #only single match
		df_chrome['devices'] = 'nan' #devices
		df_chrome['model id'] = 'nan' #model id
		df_chrome['resolution (px)'] = 'nan' #resolution
		idx=0
		rw=0
		index=0
		row=0
		for idx, rw in df_chrome.iterrows():
			gpu = rw['gpu']
			l_match_d = [] #matching devices
			l_match_mid = [] #matching model id
			l_match_ss = [] #matching screen size
			l_match_res = [] #matching resolution
			l_match_gpu = [] #matching gpu
			l_match_px = [] #matching pixel density
			#for each device
			for index, row in df_screensize_filter.iterrows():
				#l_row = map(str.strip, row['gpu list']) #strip items in list
				l_row = row['gpu list']
				#if gpu in list
				if [x for x in l_row if gpu.lower() in x.lower()].__len__() > 0:
					#add device to list 
					l_match_d.append(str(row['device']))
					l_match_mid.append(str(row['model id']))
					l_match_gpu.append(str(row['gpu list']))
					l_match_px.append(str(row['pixel density (ppi)']))
					l_match_ss.append(str(row['screen size (cm)']))
					l_match_res.append(str(row['monitorSize']))
			
			#if no matches
			if l_match_d.__len__() == 0:
				df_chrome['devices'][idx] = 'nan'
				df_chrome['model id'][idx] = 'nan'
				df_chrome['gpu list'][idx] = 'nan'
				df_chrome['pixel density (ppi)'][idx] = 'nan'
				df_chrome['screen size (cm)'][idx] = 'nan'
				df_chrome['resolution (px)'][idx] = 'nan'
				df_chrome['exact match'][idx] = False
	
			#if only one device add immediately            
			elif l_match_d.__len__() == 1:
				df_chrome['devices'][idx] = l_match_d[0]
				df_chrome['model id'][idx] = l_match_mid[0]
				df_chrome['gpu list'][idx] = l_match_gpu[0]
				df_chrome['pixel density (ppi)'][idx] = l_match_px[0]
				df_chrome['screen size (cm)'][idx] = l_match_ss[0]
				df_chrome['resolution (px)'][idx] = l_match_res[0]
				df_chrome['exact match'][idx] = True    
		
			#if multiple matches
			elif l_match_d.__len__() > 1:
				#add device to dataframe
				df_chrome['devices'][idx] = l_match_d
				df_chrome['model id'][idx] = l_match_mid
				df_chrome['gpu list'][idx] = l_match_gpu
				df_chrome['pixel density (ppi)'][idx] = l_match_px
				df_chrome['screen size (cm)'][idx] = l_match_ss
				df_chrome['resolution (px)'][idx] = l_match_res
				df_chrome['exact match'][idx] = False

		#save summary
		types_df_chrome = df_chrome.dtypes
		df_test = df_chrome[['participant','session','subsession','os','os_version','gpu',\
								'diagonalSize.cm','screen size (cm)','gpu list','exact match']]
		df_test.to_excel(cwd_save+'/chrome_summary.xlsx', index=False)           


		'''
		combine data---------osx, chrome, and lab
		'''     
		#sort
		df_lab.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		df_osx.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		df_chrome.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		#concat
		df_merge = pd.concat([df_lab, df_osx, df_chrome], ignore_index=True)
		df_merge.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		#arrange columns
		df_merge = df_merge.reindex(list(df_osx.columns), axis=1)

		'''
		combine data---------all
		'''
		df_merge_small = df_merge[
				['participant','session','subsession','devices','exact match','resolution (px)',
				'screen size (cm)','gpu list', 'pixel density (ppi)']]
		df_f = pd.merge(df, df_merge_small, on=['participant','session','subsession'], how='outer')

		#fix gpu lists
		df_f['gpu list'] = df_f['gpu list'].map(lambda x: str(x).replace('"[' , '['))
		df_f['gpu list'] = df_f['gpu list'].map(lambda x: str(x).replace(']"' , ']'))

		#fix devices lists
		df_f['devices'] = df_f['devices'].astype(str) 
		df_f['resolution (px)'] = df_f['resolution (px)'].astype(str) 
		df_f['screen size (cm)'] = df_f['screen size (cm)'].astype(str) 
		df_f['pixel density (ppi)'] = df_f['pixel density (ppi)'].astype(str) 

		#drop gpu lists
		df_f = df_f[df_f.columns.drop('gpu list')]

		#merge location (lab or home) df and df_summary data
		##prepare
		df_sum = df_summary[['participant','session','subsession','location']]
		df_sum.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		df_f.sort_values(by=['participant','session','subsession']).reset_index(drop=True)
		##drop unusual participants
		df_f = df_f.drop(df_f[(df_f['participant']==111111) 
							| (df_f['participant']==999999)].index)

		df_sum = df_sum.drop(df_sum[(df_sum['participant']==111111) 
							| (df_sum['participant']==999999)].index)

		##convert types
		df_f['participant'] = df_f['participant'].astype(float)
		df_f['session'] = df_f['session'].astype(float)
		df_sum['participant'] = df_sum['participant'].astype(float)
		df_sum['session'] = df_sum['session'].astype(float)

		##merge
		df_f = pd.merge(df_f, df_sum, 
							on=['participant','session','subsession'], how='left')

		#export
		finished_json = df_f.to_json(orient='records')
		finished_json = 'json_data =' + finished_json
		with open(cwd_save+'/summary.json', 'w+') as f:
			f.write(json.dumps(finished_json,indent=4).strip('"').replace('\\',''))
			f.close()
	
		return df

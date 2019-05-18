#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| @purpose: Downloading data from REDCap.   
| @date: Created on Sat May 1 15:12:38 2019   
| @author: Semeon Risom   
| @email: semeon.risom@gmail.com   
| @url: https://semeon.io/R33-analysis   
"""

from pdb import set_trace as breakpoint
import datetime
import requests
import pandas as pd
import os
from pathlib import Path
		
'''import packages'''
class redcap():
	"""Downloading data from REDCap."""
	def __init__(self):
		pass
	@classmethod
	def cesd(cls, path, filename, token, url, report_id):
		"""Download CES-D data for use in analysis.
		
		Parameters
		----------
		path : :obj:`str`
			Path to save data.
		token : :obj:`str`
			API token to REDCap project.
		url : :obj:`str`
			API URL to REDCap server.
		report_id : :obj:`int`
			Name of report to export.
		payload : :obj:`dict` or `None`
			Parameters for type of download from REDCap.
		"""
		#prepare
		payload = {
			'token': token,
			'content': 'report',
			'report_id': report_id,
			'format': 'json',
			'type': 'flat', #each row will contain record
			'rawOrLabel': 'raw',
			'rawOrLabelHeaders': 'raw',
			'exportCheckboxLabel': 'false',
			'returnFormat': 'json'
		} 
		
		#get data
		response = requests.post(url, data=payload)
		cesd_rrs = response.json()
		
		#convert to dataframe
		df = pd.DataFrame(cesd_rrs)
		df = df.rename(columns={'record_id':'participant','cesd_sum':'cesd_score'})

		#------------------------------------------------save
		path = Path(path)
		file = '%s.csv'%(filename)
		filepath = '%s/%s'%(path, file)
		if not os.path.exists(path):
			os.makedirs(path)
		print("cesd saved: %s"%(filepath))
		df.to_csv(filepath,index=False)

	@classmethod
	def demographics(cls, path, filename, token, url, report_id, payload=None):
		"""Download demographics data for use in analysis.
		
		Parameters
		----------
		path : :obj:`str`
			Path to save data.
		token : :obj:`str`
			API token to REDCap project.
		url : :obj:`str`
			API URL to REDCap server.
		report_id : :obj:`int`
			Name of report to export.
		payload : :obj:`dict` or `None`
			Parameters for type of download from REDCap.
		 
		Notes
		-----
		color = ['Light Gray', 'Gray', 'Light Blue', 'Blue' 'Violet', 'Blue-Green', 'Green', 'Amber', 
				 'Hazel', 'Light Brown', 'Dark Brown', 'Black', 'Other']
		"""
		#prepare
		payload = {
			'token': token,
			'content': 'report',
			'report_id': report_id,
			'format': 'json',
			'type': 'flat', 
			'rawOrLabel': 'raw',
			'rawOrLabelHeaders': 'raw',
			'exportCheckboxLabel': 'false',
			'returnFormat': 'json'
		} 
		
		#get data
		response = requests.post(url, data=payload)
		demographics = response.json()
		
		#convert to dataframe
		df = pd.DataFrame(demographics)
			
		##----process data    
		df = df.rename(columns={'record_id':'participant',
								'age':'age_2',
								'es_age_exact':'age',
								'es_english':'english_fluency',
								'es_student':'is_student',
								'es_vision':'is_normalvision',
								'es_vision2':'is_corrective',
								'es_gender___1':'male',
								'es_gender___2':'female',
								'es_gender___3':'transmale',
								'es_gender___4':'transfemale',
								'es_gender___5':'genderqueer',
								'es_gender___6':'other',
								'es_gender___7':'no',
								'ethnicity':'hispanic'})  
		
		##--------convert to True, False
		#english_fluency
		df['english_fluency'] = df.apply(lambda x: True if (x['english_fluency'] == '1') else False, axis=1)
		#normal vision
		df['is_normalvision'] = df.apply(lambda x: True if (x['is_normalvision'] == '1') else False, axis=1)
		#corrective
		df['is_corrective'] = df.apply(lambda x: True if (x['is_corrective'] == '1') else False, axis=1)
		#corrective
		df['hispanic'] = df.apply(lambda x: True if (x['hispanic'] == '1') else False, axis=1)
		##--------convert other
		#handedness
		df['handedness'] = df.apply(lambda x: "Right" if (x['handedness'] == '1') else "Left", axis=1)
		#color
		
		
		##--------remove dummy data for race
		###AIAN
		race_1 = [col for col in df.columns if 'race___1' in col]
		race_2 = 'American Indian or Alaska Native'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == '1') else None, axis=1)
		###asian
		race_1 = [col for col in df.columns if 'race___2' in col]
		race_2 = 'Asian'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == '1') else None, axis=1)
		###black
		race_1 = [col for col in df.columns if 'race___3' in col]
		race_2 = 'Black or African American'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == '1') else None, axis=1)
		###pacific
		race_1 = [col for col in df.columns if 'race___4' in col]
		race_2 = 'Native Hawaiian and Other Pacific Islander'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == '1') else None, axis=1)
		###white
		race_1 = [col for col in df.columns if 'race___5' in col]
		race_2 = 'White'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == '1') else None, axis=1)
		###none
		race_1 = [col for col in df.columns if 'race___6' in col]
		race_2 = 'None of the above'
		df = df.rename(columns={race_1[0]:race_2})
		df[race_2] = df.apply(lambda x: race_2 if (x[race_2] == '1') else None, axis=1)
		##collapse
		race=['American Indian or Alaska Native','Asian','Black or African American',
			  'Native Hawaiian and Other Pacific Islander','White','None of the above']
		df['race'] = df[race].apply(lambda x: '&'.join(x.dropna().astype(str)),axis=1)
		##create new mixed race group
		df.loc[df['race'].str.contains('&'), 'race'] = 'Two or more races'
		
		##convert to categorical
		df.loc[:,'race'] = df['race'].astype('category')
		##finish
		df = df[['participant','age','handedness','english_fluency','is_student','is_normalvision',
				 'is_corrective','eye_color','male','female','race','hispanic']].reset_index(drop=True)

		#----save
		path = Path(path)
		file = '%s.csv'%(filename)
		filepath = '%s/%s'%(path, file)
		if not os.path.exists(path):
			os.makedirs(path)
		print("demographics saved: %s"%(filepath))
		df.to_csv(filepath,index=False)

	@classmethod        
	def mmpi(cls, path, filename, token, url, report_id, payload=None):
		"""Download MMPI data for use in analysis.
		
		Parameters
		----------
		path : :obj:`str`
			Path to save data.
		token : :obj:`str`
			API token to REDCap project.
		url : :obj:`str`
			API URL to REDCap server.
		report_id : :obj:`int`
			Name of report to export.
		payload : :obj:`dict` or `None`
			Parameters for type of download from REDCap.
		"""

		#----prepare
		payload = {
			'token': token,
			'content': 'report',
			'report_id': report_id,
			'format': 'json',
			'type': 'flat',
			'rawOrLabel': 'raw',
			'rawOrLabelHeaders': 'raw',
			'exportCheckboxLabel': 'false',
			'returnFormat': 'json'
		} 
		
		#get data
		response = requests.post(url, data=payload)
		mmpi = response.json()
		
		#convert to dataframe
		df = pd.DataFrame(mmpi)
		df = df.rename(columns={'record_id':'participant'})
		
		##arrange order numerically
		###get list
		cols = df.columns.tolist()
		###remove record_id, and sona_id; then sort list
		l_id = ['participant','sona_id']
		cols = [x for x in cols if x not in l_id]
		cols.sort(key= lambda x: float(x.strip('mmpi_')))
		###add to front of list
		cols = l_id + cols
		###apply list to df
		df = df[cols]
		
		##----start
		#drop participants with no score
		df = df.drop(df[df['mmpi_51']==""].index).reset_index(drop=True)
		#convert to numeric
		df = df.apply(pd.to_numeric)
		
		#rescore mmpi to have all columns equal to 1 = True, 0 = False
		##do this by reversing columns 51, 77, 90, 93, 102, 126, 192, 276, 501 to equal 1 if True and
		##0 = False, 1 = True: 66, 114, 162, 193, 216, 220, 228, 252, 282, 291, 294, 322, 323, 336, 371, 387, 478, 555
		##1 = False, 0 = True: 51, 77, 90, 93, 102, 126, 192, 276, 501
		##list of columns to modify
		lst_modify = ["mmpi_%s"%(i) for i in [51, 77, 90, 93, 102, 126, 192, 276, 501]]
		
		#reset columns 51, 77, 90, 93, 102, 126, 192, 276, 501
		for itm in lst_modify:
			df.loc[:, itm] = df[itm].apply(lambda x: 0 if (x==1) else 1)
		
		#sum columns
		df['mmpi_score'] = df.iloc[:, 2:].sum(axis=1)
		
		#----save
		path = Path(path)
		file = '%s.csv'%(filename)
		filepath = '%s/%s'%(path, file)
		if not os.path.exists(path):
			os.makedirs(path)
		print("mmpi saved: %s"%(filepath))
		df.to_csv(filepath,index=False)

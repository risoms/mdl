#%% [markdown]
# .. R33_:
 
# .. title:: R33

# # Analysis of R33 Data
#%%
# Created on Sat May 1 15:12:38 2019  
# @author: Semeon Risom  
# @email: semeon.risom@gmail.com  
# @url: https://semeon.io/d/R33-analysis  
# @purpose: Hub for running processing and analysis.
#%% [markdown]
# ## local import
from pdb import set_trace as breakpoint
from imhr import settings, data
from imhr.r33 import Processing
from datetime import datetime
from pathlib import Path
import os
## parameters
console = settings.console
#%% [markdown]
# ## set current date
date_start = []; date_end = []
date_now  = datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
#%% [markdown]
# ## load passwords from yaml
#%% 
import yaml
with open('/Users/mdl-admin/Desktop/mdl/docs/source/examples/analysis/private.yaml', 'r') as _file:
	p = yaml.safe_load(_file)
#%% [markdown]
# ##  Download data from UTWeb SFTP server
# Here you can download data from a remote server using SFTP. In this case, we are accessing the University of Texas UTWeb server to get online eyetracking data.
#%% 
# login parameters
host = p['r33']['utweb']['hostname']
user = p['r33']['utweb']['username']
pwd = p['r33']['utweb']['password']
# download partial data backups
filetype = '.csv' # get only csvs
s = p['r33']['utweb']['path'] + 'part/' # path of backup data on server
d = '/Users/mdl-admin/Desktop/r33/data/raw/part/'
log, start, end, now = data.Download.SFTP(source=s, destination=d, hostname=host, username=user, password=pwd, filetype=filetype)
# download full data
filetype = '.csv' # get only csvs
s = p['r33']['utweb']['path']  # path of data on server
d = '/Users/mdl-admin/Desktop/r33/data/raw/full/'
log, start, end, now = data.Download.SFTP(source=s, destination=d, hostname=host, username=user, password=pwd, filetype=filetype)

#%% [markdown]
# ## Download data from REDCap
# Data from Research Electronic Data Capture (REDCap) can be downloaded. Here we are accessing participant 
#%% 
# login, path parameters
d = '/Users/mdl-admin/Desktop/r33/data/redcap/'
token = p['r33']['redcap']['token']
url = p['r33']['redcap']['url']
content = 'report'
report_id = '6766'
# export
log, start, end, now = data.Download.REDCap(path=d, token=token, url=url, content=content, report_id=report_id)
#%% [markdown]
# ##### Preprocessing
# Clean up variable names, correct screensize for processing.
#%%
source = '/Users/mdl-admin/Desktop/r33/data/raw/full/'
errors = Processing.preprocessing(source=source, isMultiprocessing=True, cores=6)
#%% [markdown]
# ##### Summary data
#%%
# parameters
source = "/Users/mdl-admin/Desktop/r33/data/preprocessed/"
destination = "/Users/mdl-admin/Desktop/r33/data/processed/summary.xlsx"
metadata = "/Users/mdl-admin/Desktop/r33/data/metadata.csv"
# Processing
df, errors, _ = Processing.summary(source=source, destination=destination, metadata=metadata, isHTML=True)
#%% [markdown]
# ##### Definitions
#%% 
source = "/Users/mdl-admin/Desktop/r33/data/preprocessed/53_0abc.csv"
destination = "/Users/mdl-admin/Desktop/r33/data/processed/variables.xlsx"
df_variables, _ = Processing.variables(source=source, destination=destination, isHTML=True)
#%% [markdown]
# ##### Device characteristics
#%% 
source = "/Users/mdl-admin/Desktop/r33/data/processed/summary.xlsx"
destination = "/Users/mdl-admin/Desktop/r33/data/processed/device.xlsx"
df_device, _ = Processing.device(source=source, destination=destination, isHTML=True)

#%% [markdown]
# ##### demographics characteristics
#%% 
source = "/Users/mdl-admin/Desktop/r33/data/redcap/report.xlsx"
destination = "/Users/mdl-admin/Desktop/r33/data/processed/demographics.xlsx"
df_demographics = Processing.demographics(source=source, destination=destination, isHTML=True)





































































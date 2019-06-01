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
from datetime import datetime
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
report_id = '4717'
# export
log, start, end, now = data.Download.REDCap(path=d, token=token, url=url, content=content, report_id=report_id)
#%% [markdown]
# ##### create summary data
#%% 
import processing
# parameters
source = "/Users/mdl-admin/Desktop/r33/data/raw/full/"
destination = "/Users/mdl-admin/Desktop/r33/data/processed/summary.xlsx"
metadata = "/Users/mdl-admin/Desktop/r33/data/metadata.csv"
# run
df, errors = processing.summary(source=source, destination=destination, metadata=metadata, isHTML=True)
#%% [markdown]
# ##### create summary data
#%% 
destination = "/Users/mdl-admin/Desktop/r33/data/processed/variables.xlsx"
df_variables = processing.variables(df=df, destination=destination)

#%%    
## create html
html_name = 'definitions'
html_path = path_['output'] + "/analysis/html/%s.html"%(html_name)
title = '<b>Table 1.</b> Task Variables and Definitions.'
html = plot.html(config=config, df=df_variables, path=html_path, name=html_name, source="definitions", title=title)








#%% [markdown]
# ##### total sessions per subject
# summary path
summary_path = "/Users/mdl-admin/Desktop/r33/data/processed/summary.xlsx"
# load summary
import pandas as pd
df_ = pd.read_excel(summary_path)

# drop 
## missing rows
df = df[~df['participant'].isnull()]
## duplicate participant listings, keep first and last
df_first = df.drop_duplicates(subset="participant", keep="first").reset_index(drop=True)
df_last = df.drop_duplicates(subset="participant", keep="first").reset_index(drop=True)
df[['participant','session']].groupby(['participant','session']).agg(['mean', 'count'])






































































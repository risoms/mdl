# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:41:41 2017
@file: actigraph.py
@author: sr38553
@questions: semeon.risom@gmail.com
@description: imports actigraph data (csv), removes metadata, reformats date, and saves as new output (csv)
date should be in YYYY-MM-DD HH:MM:SS or YYYY/MM/DD HH:MM:SS format
@notes: http://strftime.org/
"""
#logging
import os  # handy system and path functions
import pandas
import datetime
import numpy as np

try: #use _file_ in most cases
    dir = os.path.dirname(__file__)
except NameError:  #except when running python from py2exe script
    import sys
    dir = os.path.dirname(sys.argv[0])

#directory
oldD = os.path.join(dir, 'data')

#prepare variables
count = 0
l_Count = []
l_File = []
l_Mean = []
l_Std = []

#prepare text file
for filename in os.listdir(oldD):
    if filename.endswith('.csv'):
        #read and remove meta data
        oldcsv = os.path.join(oldD, filename)
        df = pandas.read_csv(oldcsv, skiprows=range(0, 1))
        
        #drop practice rows and reindex
        df = df[pandas.notnull(df['BlockList'])].reset_index(drop=True)
        
        #calculate mean and st-dev     
        mean = df[['DotLoc.RT']].mean()[0]
        std = df[['DotLoc.RT']].std()[0]  
        
        #format date to pandas datetime    
        #df['Time'] = pandas.to_datetime(df['Time']).dt.strftime('%H:%M:%S')
        #combine to new column - datetime
        #df['Datetime'] = df[['Date', 'Time']].apply(lambda x: ' '.join(x), axis=1)
        #keep specific columns
        #df = df[['Datetime','Activity']]
        
        #append all lists
        l_Count.append(count)
        l_File.append(filename)
        l_Mean.append(mean)        
        l_Std.append(std)
        count = count + 1
    
    #if non csv file
    else:
        continue
    
#list of all files
aCount_df = pandas.DataFrame({'index': l_Count, 'filename': l_File, 'mean': l_Mean, 'std': l_Std})
aCount_df = aCount_df[['index','filename','mean','std']]
#save csv index
aCsv = os.path.join("index" + ".csv")
aCount_df.to_csv(aCsv, index = False, index_col = False)
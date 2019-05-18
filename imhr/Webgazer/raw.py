#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| @purpose: Automate data importing UTWeb Server.   
| @date: Created on Sat May 1 15:12:38 2019   
| @author: Semeon Risom   
| @email: semeon.risom@gmail.com   
| @url: https://semeon.io/d/R33-analysis   
"""

from pdb import set_trace as breakpoint
import os, datetime
        
'''import packages'''
class raw():
    """processing summary data for output"""
    def __init__(self, is_library=False):
        """Download raw data from UTWeb server for use in analysis.
        
        Parameters
        ----------
        is_library : :obj:`bool`
            Check if required libraries are available.
        """
        #check libraries
        if is_library:
            self.library()

    def library(self):
        """Check if required libraries are available."""

        #check libraries for missing
        from distutils.version import StrictVersion
        import importlib, pkg_resources, pip, platform
        
        #list of possibly missing packages to install
        required = ['pandas','openpyxl','pysftp','utils','cryptography','paramiko']
        
        #for geting os variables
        if platform.system() == "Windows":
            required.append('win32api')
        elif platform.system() =='Darwin':
            required.append('pyobjc')
        
        #try installing and/or importing packages
        try:
            #if pip >= 10.01
            pip_ = pkg_resources.get_distribution("pip").version
            if StrictVersion(pip_) > StrictVersion('10.0.0'):
                from pip._internal import main as _main
                #for required packages check if package exists on device
                for package in required:
                    #if missing, install
                    if importlib.util.find_spec(package) is None:
                        _main(['install',package])
                    #else import
                    else:
                        __import__(package)
                        
            #else pip < 10.01          
            else:
                #for required packages check if package exists on device
                for package in required:
                    #if missing
                    if importlib.util.find_spec(package) is None:
                        pip.main(['install',package])
                    #else import
                    else:
                        __import__(package)
                
        except Exception as e:
            return e
        
    def download(self, l_exp, log_path, save_path, hostname, username, password):
        """Download raw data for use in analysis.
        
        Parameters
        ----------
        l_exp : :obj:`str`
            The list of experiments to pull data from.
        log_path : :obj:`str`
            The directory path to save the log of participant data downloaded.
        save_path : :obj:`str`
            The directory path to save paticipant data.
        hostname : :obj:`str`
            SSH hostname.
        username : :obj:`str`
            SSH username.
        password : :obj:`str`
            SSH password.
        """
        import paramiko, openpyxl
        import pandas as pd
        #current date
        now = datetime.datetime.now()

        #----for every experiment
        for exp in l_exp:
            save = exp['save']
            task = exp['task']
            #partial
            if (task != "wf_js") and (task != "gaze_js"):
                folder = save_path + '/' + save + '/part'
                if not os.path.exists(folder):
                    print('creating local folder: %s'%(folder))
                    os.makedirs(folder)
            #full
            folder = save_path + '/' + save
            if not os.path.exists(folder):
                print('creating local folder: %s'%(save))
                os.makedirs(folder)
        
        #breakpoint()
        '''
        connect to sftp and download files
        def: intermediate - saved block of task (a[=first block] or ab[=first two blocks])
        def: full - saved block of task (abc[=all blocks])
        '''
        print('connecting to sftp')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        client.connect(hostname=hostname,username=username,password=password)
        sftp = client.open_sftp()
        #for each experiment
        l_row = [] #log of updated files
        highest_date = [] #most recent participants for each task
        for exp in l_exp:
            path = exp['path']
            task = exp['task']
            save = exp['save']
            newpartnum = 0 #intermediate task data counter
            newfullnum = 0 #full task data file counter
            newpartname = 'nan' #most recent partial file names
            newfullname = 'nan' #most recent full file names
            
            #----intermediate files - only relevant for wf_js and gaze_js
            if (task != "wf_js") and (task != "gaze_js"): 
                sftp.chdir(path+'/part')
                remote_path = str(sftp.getcwd())
                remote_directory = sftp.listdir() 
                #for each file in remote directory
                for filename in remote_directory:
                    remote_fpath = remote_path +'/'+ filename
                    local_fpath = save_path +'/'+ save +'/part/'+ filename
                    #check if file already exists and is a csv
                    if (filename.endswith('.csv')) and not (os.path.isfile(local_fpath)):
                        sftp.get(remote_fpath, local_fpath)
                        newpartnum = newpartnum + 1
                        newpartname = filename
                    
            #number of files in remote directory
            total_part = ([x for x in remote_directory if ".csv" in x]).__len__()
            
            #----full files
            sftp.chdir(path)
            remote_path = str(sftp.getcwd())
            remote_directory = sftp.listdir()
            #get date of most recent file on server
            #print(remote_directory)
            ldate = []
            for fileattr in sftp.listdir_attr():
                if fileattr.filename.endswith('.csv'):
                    ldate.append([fileattr.st_mtime,fileattr.filename])
                #print('latest: %s'%(ldate))
            ##get highest date
            highest_date.append({task:max(ldate, key=lambda item: item[0])})
            
            #for each file in remote directory
            for filename in remote_directory:
                remote_fpath = remote_path +'/'+ filename
                local_fpath = save_path +'/'+ save +'/'+ filename
                #check if file already exists and is a csv
                if (filename.endswith('.csv')) and not (os.path.isfile(local_fpath)):
                    sftp.get(remote_fpath, local_fpath)
                    newfullnum = newfullnum + 1
                    newfullname = filename
                    
                    
            #number of files in remote directory    
            total_full = ([x for x in remote_directory if ".csv" in x]).__len__() 
            print('total files for %s: %s'%(task, total_full))
            
            #append log list
            row = [str(now.strftime('%Y-%m-%d %H:%M')),task,
                   newpartnum,newfullnum,
                   total_part,total_full,
                   newpartname,newfullname]
            l_row.append(row)

        #closing sftp    
        sftp.close()
        
        #--------------------------------------log
        log_path = log_path +"/participants.xlsx"
        #if file exists
        if os.path.exists(log_path):
            print("log updated: %s"%(log_path))
            #load file
            wb = openpyxl.load_workbook(log_path)
            # Select First Worksheet
            ws = wb.worksheets[0]
            #add data
            for fields in l_row:
                ws.append(fields)
            #update
            wb.save(log_path)
        
        #else create file
        else:
            print("raw data saved: %s"%(save_path))
            headers = ['date','task','uploaded intermediate files','uploaded full files','total intermediate files', 
                       'total full files','most recent intermediate file', 'most recent full file']
            #creating datafame and save as xlsx
            df = pd.DataFrame(l_row, columns=headers)
            df.to_excel(log_path, index=False)

        return highest_date
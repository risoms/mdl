#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| @purpose: Resource for downloading files from Box, SSH, REDCap and others.   
| @date: Created on Sat May 1 15:12:38 2019   
| @author: Semeon Risom   
| @email: semeon.risom@gmail.com   
| @url: https://semeon.io/d/R33-analysis   
"""
from pdb import set_trace as breakpoint
import os
from datetime import datetime
from pathlib import Path
from .settings import settings

#----required external
_required = ['paramiko', 'openpyxl', 'requests', 'ftplib', 'pandas']
#import paramiko, openpyxl, requests, ftplib

class download():
    """Resource for downloading files from Box, SSH, REDCap and others."""
    @classmethod
    def __init__(cls, is_library=False):
        """Download raw data from apache, Box, or REDCap servers.
        
        Parameters
        ----------
        is_library : :obj:`bool`
            Check if required libraries are available.
        """
        #check libraries
        if is_library:
            settings.library(_required)

    @classmethod
    def REDCap(cls, path, token, url, content, payload=None, **kwargs):
        """Download data from an Research Electronic Data Capture (REDCap) server.
        
        Parameters
        ----------
        path : :obj:`str`
            Path to save data.
            For example::
                >>> path = '/Users/mdl-admin/Desktop/r33/redcap'
        token : :obj:`str`
            The API token specific to your REDCap project and username. This is usually found on the Applications > API page. 
            For example::
                >>> token = 'D19859823032SFDMR24395298'
        url : :obj:`str`
            The URL of the REDCap project. 
            For example::
                >>> url = 'https://redcap.prc.utexas.edu/redcap/api/'.
        content : :obj:`str` {report, file, raw, arm, instrument, returnFormat, metadata, project, surveyLink, user, participantList}
            Type of export. Examples include exporting a report (`report`), file (`file`), or project info (`project`).
        payload_ : :obj:`dict` or `None`, optional
            Manually submit parameters for exporting or importing data. Can be entered within the function for convenience.
        **kwargs : :obj:`str` or `None`, optional
            Additional properties, relevent for specific content types. Here's a list of available properties:
            
            .. list-table::
                :class: kwargs
                :widths: 25 50
                :header-rows: 1
               
                * - Property
                  - Description
                * - report_id : :obj:`str`
                  - (report, record) The report ID number provided next to the report name on the report list page.
                * - format_ : :obj:`str` {csv, json, xml, odm}
                  - Format to return data, either csv, json, xml, or odm. Default is json.
                * - type_ : :obj:`str`
                  - Shape of data. Default is flat.
                * - rawOrLabel_ : :obj:`str` {raw, label}
                  - (report, record) TExport the raw coded values or labels for the options of multiple choice fields.
                * - rawOrLabelHeaders_ : :obj:`str`
                  - (report, record) TExport the variable/field names (raw) or the field labels (label).
                * - exportCheckboxLabel_ : :obj:`str`
                  - Specifies the format of checkbox field values specifically when exporting the data as labels (i.e., when rawOrLabel=label).
                * - returnFormat_ : :obj:`str`
                  -  Format to return errors. Default is `json`.
                 
        Returns
        -------
        log : :obj:`pandas.core.frame.DataFrame` or `None`
            Pandas dataframe of each download request.
        content : :obj:`pandas.core.frame.DataFrame` or `None`
            Pandas dataframe of all data downloaded.
        start, end : :obj:`str`
            Timestamp (ISO format) and name of most recent (`end`) and first (`start`) file created in folder.
        now : :obj:`str`
            Current timestamp in ISO format.
        
        """
        import openpyxl, requests
        import pandas as pd
        
        #----constants, lists to prepare
        ldate = [] #list of dates
        file_num = 0 #file counter
        # bool
        log = None #log of events
        start = None #most recent file
        end = None #most recent file
        
        #----path
        # log
        name = Path(path).name
        log_path = os.path.abspath(os.path.dirname(path)) + "/%s.xlsx"%(name)
        # destination
        path = Path(path)
        
        #----kwargs
        # general
        format_ = kwargs['format'] if "format" in kwargs else 'json'
        type_ = kwargs['content'] if "content" in kwargs else 'flat'
        rawOrLabel_ = kwargs['rawOrLabel'] if "rawOrLabel" in kwargs else 'raw'
        rawOrLabelHeaders_ = kwargs['rawOrLabelHeaders'] if "rawOrLabelHeaders" in kwargs else 'raw'
        exportCheckboxLabel_ = kwargs['exportCheckboxLabel'] if "exportCheckboxLabel" in kwargs else 'false'
        returnFormat_ = kwargs['returnFormat'] if "returnFormat" in kwargs else 'json'
        # report
        report_id = kwargs['report_id'] if "report_id" in kwargs else 'None'
        # participantList
        instrument_ = kwargs['instrument'] if "instrument" in kwargs else 'cssrs'
        event_ = kwargs['event'] if "event" in kwargs else 'online_eligibility_arm_1'

        #----start
        settings.console('connecting to REDCap', 'blue')
        
        #----make sure local path exists
        settings.console('local folder: %s'%(Path(path)), 'blue')
        if not os.path.exists(Path(path)):
            settings.console('creating local folder: %s'%(Path(path)), 'blue')
            os.makedirs(Path(path))
        
        #----start download
        # prepare
        if payload == None:
            # report
            if content == 'report':
                payload = {
                    'token': token,
                    'content': content,
                    'format': format_,
                    'type': type_, 
                    'returnFormat': returnFormat_,
                    'report_id': report_id,
                    'rawOrLabel': rawOrLabel_,
                    'rawOrLabelHeaders': rawOrLabelHeaders_,
                    'exportCheckboxLabel': exportCheckboxLabel_
                }
            elif content == 'participantList':
                payload = {
                    'token': token,
                    'content': content,
                    'format': format_,
                    'returnFormat': returnFormat_,
                    'instrument': instrument_ ,
                    'event': event_,
                }
            elif content == 'metadata':
                payload = {
                    'token': token,
                    'content': content,
                    'format': format_,
                    'returnFormat': returnFormat_,
                }
            elif content == 'project':
                payload = {
                    'token': token,
                    'content': content,
                    'format': format_,
                    'returnFormat': returnFormat_,
                }
            else:
                raise Exception('Not finished. Content `%s` unavailable.'%(content))

        # get data
        response = requests.post(url, data=payload)
        json = response.json()
        # if error
        if 'error' in json:
            raise Exception('Export failed. Reason: %s.'%(json['error']))
        
        # convert to dataframe
        df = pd.DataFrame(json)
                
        # save data
        path_= os.path.dirname(path) + "/REDCap/%s.xlsx"%(content)
        df.to_excel(path_, index=False)

        # if list isnt empty get start and end dates
        if ldate:
            ## start
            start = min(map(lambda x: [x[0],x[1]], ldate))
            settings.console('oldest file: %s'%(start[0]), 'blue')
            ## end
            end = max(map(lambda x: [x[0],x[1]], ldate))
            settings.console('newest file: %s'%(end[0]), 'blue')
        
        #----log
        # if new files
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        #!!! add values to go into dataframe----
        row = [df.shape[0],token,content,now]
        
        # if log exists, update
        if os.path.exists(log_path):
            settings.console("Log updated @: %s"%(log_path), 'blue')
            #load file
            wb = openpyxl.load_workbook(log_path)
            # Select First Worksheet
            ws = wb.worksheets[0]
            # add data
            ws.append(row)
            # update
            wb.save(log_path)
            # import log
            log = pd.ExcelFile(log_path)
        # else create log
        else:
            settings.console('Log created @: %s'%(log_path), 'blue')
            headers = ['subjects', 'token', 'content', 'date']
            # creating datafame and save as xlsx
            log = pd.DataFrame([row], columns=headers)
            log.to_excel(log_path, index=False)
        
        return log, start, end, now

    
    @classmethod
    def SFTP(cls, source, destination, hostname, username, password, **kwargs):
        """Connect to a remote server using a Secure File Transfer Protocol (SFTP).
        
        Parameters
        ----------
        source : :obj:`str`
            The directory path to retrieve paticipant data.
        destination : :obj:`str`
            The directory path to save paticipant data.
        hostname : :obj:`str`
            SFTP hostname.
        username : :obj:`str`
            SFTP username.
        password : :obj:`str`
            SFTP password.
        **kwargs : :obj:`str` or `None`, optional
            Additional properties, relevent for specific content types. Here's a list of available properties:
            
            .. list-table::
                :class: kwargs
                :widths: 25 50
                :header-rows: 1
               
                * - Property
                  - Description
                * - filetype : ::obj:`str` or `None`
                  - Filetype to download. Default is csv.
  
        Returns
        -------
        log : :obj:`pandas.core.frame.DataFrame` or `None`
            Pandas dataframe of each download request.
        content : :obj:`pandas.core.frame.DataFrame` or `None`
            Pandas dataframe of all files downloaded.
        start, end : :obj:`str`
            Timestamp (ISO format) and name of most recent (`end`) and first (`start`) file created in folder.
        now : :obj:`str`
            Current timestamp in ISO format.
            
        Examples
        --------
        >>> name='r33'; source='/home/utweb/utw1211/public_html/r33'; d='/Users/mdl/Desktop/r33/'; un='utw1211'; pwd='43#!9amZ?K$'
        >>> log, start, end, now = download.SFTP(source=s, destination=d, hostname=hostname, username=un, password=pwd)
        
        """
        import paramiko, openpyxl
        import pandas as pd
        
        #----kwargs
        lfiletype = kwargs["filetype"].replace('.','') if "filetype" in kwargs else ['csv']
        
        #----constants, lists to prepare
        ldate = [] #list of dates
        file_num = 0 #file counter
        # bool
        log = None #log of events
        start = None #most recent file
        end = None #most recent file
        # path
        
        ## log
        name = Path(destination).name
        log_path = os.path.abspath(os.path.dirname(destination)) + "/%s.xlsx"%(name)
        ## destination
        destination = Path(destination)
        
        settings.console('connecting to sftp', 'blue')
        
        #----make sure local path exists
        settings.console('local folder: %s'%(Path(destination)), 'blue')
        if not os.path.exists(Path(destination)):
            settings.console('creating local folder: %s'%(Path(destination)), 'blue')
            os.makedirs(Path(destination))
        
        #----connect to SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        client.connect(hostname=hostname, username=username, password=password)
        sftp = client.open_sftp()
        
        #----set path and get list of files
        sftp.chdir(source)
        remote_path = str(sftp.getcwd()) + '/'
        remote_directory = sftp.listdir()
        remote_attr = sftp.listdir_attr()
                
        #----check number of files in remote directory
        # list comprehension: <for each file in remote directory> <check if file extension matches> <and if file extension isn't empty string>
        remote_num = len([x for x in remote_directory if Path(x).suffix.replace('.','') in lfiletype and bool(Path(x).suffix.replace('.',''))])        
        try:
            if remote_num >= 1:
                settings.console('Total files in %s: %s'%(remote_path, remote_num), 'blue')
            else:
                raise Exception("Error: No %s found in folder: '%s'"%(lfiletype, remote_path))
        except Exception as error:
            settings.console(str(error), 'red')
            raise
          
        #----export files
        settings.console("Starting download from %s"%(remote_path), 'blue')
        # for each file in remote directory
        for file in remote_attr:
            # file
            filename = file.filename
            filetype = Path(filename).suffix.replace('.','')
            
            # if file is correct filetype and not empty string
            if (filetype in lfiletype) and (bool(filetype)):
                # path
                remote_fpath = remote_path + filename
                local_fpath = '%s/%s'%(destination, filename)
                # date
                date = datetime.fromtimestamp(file.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                ldate.append([date, filename]) 
            
                # if file not in local drive, download
                if not os.path.isfile(local_fpath):
                    settings.console('filename: %s, type: %s, date: %s'%(filename, lfiletype, date), 'green')
                    # counter
                    file_num = file_num + 1
                    # download
                    sftp.get(remote_fpath, local_fpath)

        # if list isnt empty get start and end dates
        if ldate:
            ## start
            start = min(map(lambda x: [x[0],x[1]], ldate))
            settings.console('oldest file: %s'%(start[0]), 'blue')
            ## end
            end = max(map(lambda x: [x[0],x[1]], ldate))
            settings.console('newest file: %s'%(end[0]), 'blue')

        #closing sftp    
        sftp.close()
        
        #----log
        # if new files
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if file_num > 0:
            settings.console("Finished downloading files", 'blue')
            row = [now, file_num, remote_num, end[1]]
        
            # if log exists, update
            if os.path.exists(log_path):
                settings.console("Log updated @: %s"%(log_path), 'blue')
                #load file
                wb = openpyxl.load_workbook(log_path)
                # Select First Worksheet
                ws = wb.worksheets[0]
                # add data
                ws.append(row)
                # update
                wb.save(log_path)
                # import log
                log = pd.ExcelFile(log_path)
            # else create log
            else:
                settings.console('Log created @: %s'%(log_path), 'blue')
                headers = ['folder', 'downloaded', 'total', 'newest']
                # creating datafame and save as xlsx
                log = pd.DataFrame([row], columns=headers)
                log.to_excel(log_path, index=False)
        else:
            settings.console("No files to download", 'blue')
        
        return log, start, end, now

    
    @classmethod
    def box(cls, source, destination, server, username, password):
        """Connect to Box cloud cloud storage service, using File Transfer Protocol over SSL (FTPS).
        
        Parameters
        ----------
        source : :obj:`str`
            The remoate path on box to retrieve data.
        destination : :obj:`str`
            The local path to download data.
        server : :obj:`str`
            Name of box server.
        username : :obj:`str`
            Box account email address.
        password : :obj:`str`
            Box account password.
            
        Notes
        -----
        - The username and password must be seperate from your 'Secure Sign On' associated with your UT login.  
        - box only allows connections via FTPS for downloading and uploading data. 
        - For more information: https://community.box.com/t5/Upload-and-Download-Files-and/Using-Box-with-FTP-or-FTPS/ta-p/26050
            
        """
        import openpyxl
        import pandas as pd
        import ftplib
        
        #----constants, lists to prepare
        ldate = [] #list of dates
        file_num = 0 #file counter
        # bool
        log = None #log of events
        start = None #most recent file
        end = None #most recent file
        # path
        
        ## log
        name = Path(destination).name
        log_path = os.path.abspath(os.path.dirname(destination)) + "/%s.xlsx"%(name)
        ## destination
        destination = Path(destination)
        
        settings.console('connecting to sftp', 'blue')
        
        #----make sure local path exists
        settings.console('local folder: %s'%(Path(destination)), 'blue')
        if not os.path.exists(Path(destination)):
            settings.console('creating local folder: %s'%(Path(destination)), 'blue')
            os.makedirs(Path(destination))
        
        #----start ftplib
        ftps = ftplib.FTP_TLS()
        ftps.set_debuglevel(2)
        
        # connect to host and authorize
        ftps.connect(host=server, port=990)
        ftps.set_pasv(True)
        ftps.auth()
        ftps.prot_p()
        
        # login
        ftps.login(username, password)
        
        #check path
        path = ftps.pwd()
        
        #get files in directory
        files = ftps.dir()
        
        # file to send
        # file = open('kitten.jpg','rb')
        # send the file
        # session.storbinary('STOR kitten.jpg', file)
        
        # logout
        ftps.quit()
        
        log = ''
        start = ''
        end = ''
        now = ''
        
        return log, start, end, now
#%% [markdown]
# #### mdl-R33-analysis
#%%
# Created on Sat May 1 15:12:38 2019  
# @author: Semeon Risom  
# @email: semeon.risom@gmail.com  
# @url: https://semeon.io/d/R33-analysis  
# @purpose: Hub for running processing and analysis.
#%%--------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------resources
'''
Useful python references
    - https://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod
    - https://realpython.com/python-modules-packages/
'''
#%%--------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------imports
#----local
from imhr.R33 import download, model, plot, processing, settings

#----config
settings = settings()
console = settings.console
config = settings.config
filters = config['filter']
is_ = config['metadata']['is']
path_ = config['path']
#set parameters
config['processing']['type'] = 'eyetracking'
config['processing']['single_subject'] = False
config['processing']['single_trial'] = False

#----check if required libraries are available
is_['library'] = False
if is_['library']:
    settings.library()
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------imports continued
#----core
from pdb import set_trace as breakpoint
import pandas as pd
import glob, string, pytz, json, codecs
from datetime import datetime

# set current date
date_start = []; date_end = []
date_now  = datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
#%%--------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------init
processing = processing(config)
#%%--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------create pydoc
is_['pydoc'] = False
if is_['pydoc']:
    build = '/Users/mdl-admin/Desktop/imhr-R33/docs'
    source = '/Users/mdl-admin/Desktop/imhr-R33/docs/source'
    path = '/Users/mdl-admin/Desktop/imhr-R33/docs/docs'
    processing.pydoc(path=path, build=build, source=source, copy=True) if __name__ == '__main__' else None
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------import raw data from server
is_['rawdata'] = True
if is_['rawdata']:
    console('Step: importing raw data from server', 'red')
    #----path
    log_path = path_['output']
    save_path = path_['output'] + '/raw/'
    #----login
    home = 'panel.utweb.utexas.edu' #hostname
    user = "utw10623" #username
    pwd = "mdlcla" #password
    #----download partial data
    filetype = '.csv'
    s = '/home/utweb/utw10623/public_html/a/r33/src/csv/data/subject/part/'
    d = '/Users/mdl-admin/Desktop/imhr-R33/imhr/dist/output/data/raw/part/'
    log, start, end, now = download.SFTP(source=s, destination=d, hostname=home, username=user, password=pwd, filetype=filetype)
    #----full data
    filetype = '.csv'
    s = '/home/utweb/utw10623/public_html/a/r33/src/csv/data/subject/'
    d = '/Users/mdl-admin/Desktop/imhr-R33/imhr/dist/output/data/raw/full/'
    log, start, end, now = download.SFTP(source=s, destination=d, hostname=home, username=user, password=pwd, filetype=filetype)
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------import REDCap data
is_['redcap'] = False
if is_['redcap']:
    console('Step: importing redcap data', 'red')
    #----login, paths
    d = '/Users/mdl-admin/Desktop/imhr-R33/imhr/dist/output/data/redcap/'
    redcap_token = 'D19832E1ACE0B3A502F2E41E05057C20'
    redcap_url = 'https://redcap.prc.utexas.edu/redcap/api/'
    content = 'report'
    report_id = '4717'
    #----export 
    # completed: report, participantList, metadata, project
    log, start, end, now = download.REDCap(path=d, token=redcap_token, url=redcap_url, content=content, report_id=report_id)
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------start preprocessing behavioral or eyetracking data
is_['preprocessing'] = False
if is_['preprocessing']:
    console('Step: preprocessing data', 'red')
    #----parameters
    path = path_['output'] + "/raw/"
    subject = 31
    trial = 35
    #----if single subject, single trial
    if (config['processing']['single_subject']) and (config['processing']['single_trial']):
        print('processing: single subject, single trial')
        task_type = config['processing']['type']
        processing.run(path=path, task_type=task_type, single_subject=True, single_trial=True, subject=subject, trial=trial)
    #----else if single subject, all trials
    elif (config['processing']['single_subject']) and (not config['processing']['single_trial']):
        print('processing: single subject, all trials')
        task_type = config['processing']['type']
        processing.run(path=path, task_type=task_type, single_subject=True, single_trial=False, subject=subject)
    #----if all subjects, all trials
    elif (not config['processing']['single_subject']) and (not config['processing']['single_trial']):
        print('processing: all subjects, all trials')
        task_type = config['processing']['type']
        processing.run(path=path, task_type=task_type, single_subject=False, single_trial=False, isMultiprocessing=True, cores=7)
    #----finished	
    date_end.append({'preprocessing':'%s'%(datetime.now().replace(microsecond=0).isoformat())})
pass
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#%%
console('Step: demographics, plots, analysis', 'red')
#%%--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------get metadata
is_['metadata'] = False
if is_['metadata']:
    console('processing metadata', 'red')
    #file path
    fpath = path_['output'] + "/raw/" + config['task']
    #save path
    spath = path_['output'] + "/analysis/subject_metadata.csv"
    subject_metadata = processing.subject_metadata(fpath=fpath, spath=spath)
    del fpath, spath, subject_metadata
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------prepare data
is_['prepare'] = True
if is_['prepare']:
    #exclude participants
    exclude = [999999, 111111, 156]
    console('preparing data: %s'%(exclude), 'red')
    
    #read demographics and rename id="participant"
    p_demo = path_['output'] + "/analysis/demographics.csv"
    df_demographics = pd.read_csv(p_demo, float_precision='high')
    ##exclude participants
    df_demographics = df_demographics[~df_demographics['participant'].isin(exclude)]
    #create gender column
    df_demographics['gender'] = df_demographics.apply(lambda x: 'female' if (x['female'] == 1 and x['male'] == 0) else 
                                                      ('male' if (x['male'] == 1 and x['female'] == 0) else 'other'), axis=1)
    #replace eye color
    color=['Light Gray','Gray','Light Blue','Blue','Violet','Blue-Green','Green','Amber','Hazel',
    'Light Brown','Dark Brown','Black', 'Other']
    df_demographics['eye_color'] = df_demographics['eye_color'].replace([1,2,3,4,5,6,7,8,9,10,11,12,13], color)
    
    ##-------read cesd and rename id="participant"
    p_cesd = path_['output'] + "/analysis/cesd_rrs.csv"
    df_cesd = pd.read_csv(p_cesd, float_precision='high')
    df_cesd = df_cesd.rename(columns={'record_id':'participant'})
    ##group cesd scores #bionomial
    df_cesd['cesd_group_'] = df_cesd.apply(lambda x: 1 if (x['cesd_score'] > 15) else 0, axis=1)
    df_cesd['cesd_group'] = df_cesd.apply(lambda x: 'High' if (x['cesd_score'] > 15) else 'Low', axis=1)
    ##exclude participants
    df_cesd = df_cesd[~df_cesd['participant'].isin(exclude)]

    ##-------read mmpi
    p_mmpi = path_['output'] + "/analysis/mmpi.csv"
    df_mmpi = pd.read_csv(p_mmpi, float_precision='high')
    df_mmpi = df_mmpi.rename(columns={'record_id':'participant'})
    ##exclude participants
    df_mmpi = df_mmpi[~df_mmpi['participant'].isin(exclude)]
    
    ##-------read subject metadata
    p_subject = path_['output'] + "/analysis/subject_metadata.csv"
    df_metadata = pd.read_csv(p_subject, float_precision='high')
    # drop duplicate participant listings
    df_metadata = df_metadata.drop_duplicates(subset="participant", keep="first").reset_index(drop=True)
    # start and end dates
    date_start.append({'metadata':'%s'%(df_metadata['date'].min())})
    date_end.append({'metadata':'%s'%(df_metadata['date'].max())})
    # exclude participants
    df_metadata = df_metadata[~df_metadata['participant'].isin(exclude)]
    # rename variables
    df_metadata = df_metadata.rename(columns={"isWindowSuccess": "is_calibrated"})
    # all rows repersent participants
    df_metadata['is_task'] = True
    
    ##-------read bias summary and rename id="participant"
    #if eyetracking
    if config['processing']['type'] == 'eyetracking': p_bias = path_['output'] + "/bias/eyetracking_bias.csv"
    #if behavioral
    else: p_bias = path_['output'] + "/bias/behavioral_bias.csv"
    
    #load
    df_bias = pd.read_csv(p_bias, float_precision='high')
    df_bias = df_bias.rename(columns={'id':'participant'})
    ###drop unusual data
    df_bias = df_bias.drop(df_bias[(df_bias['trialType'].isnull())].index)
    ##set dp_bias and gaze_bias as float
    df_bias['dp_bias'] = df_bias['dp_bias'].astype(float)
    if config['processing']['type'] == 'eyetracking': df_bias['gaze_bias'] = df_bias['gaze_bias'].astype(float)
    
    #set trialtype as text
    df_bias['trialType_'] = df_bias['trialType']
    df_bias['trialType'] = df_bias.apply(lambda x: 1 if (x['trialType'] == 'pofa') else 0, axis=1)
    ##exclude participants
    df_bias = df_bias[~df_bias['participant'].isin(exclude)]
    
    ##-------getting demographic data
    df_s = df_metadata.merge(df_cesd,on='participant').merge(df_demographics,on='participant')
    
    ##-------merge
    df = df_bias.merge(df_cesd,on='participant').merge(df_metadata,on='participant').merge(df_demographics,on='participant')
    #exclude participants
    df = df[~df['participant'].isin(exclude)]
    #rename columns
    ##rename microsoft os to msos, mac os to macos
    df['os'].replace(['Microsoft Windows', 'macOS','Chrome OS'], ['msos', 'macos', 'cos'], inplace=True)
    
    ##-------calculate difference between real stimulus, dotloc onset and real value #then merge medians with df
    merge = ['race','gender','is_normalvision','os','participant']
    df_error, onset_error, drop = processing.onset_diff(df0=df, merge=merge, cores=7)
    # save data
    csv_path = path_['output'] + "/analysis/error.csv"
    df_error.to_csv(csv_path, index=None)
    
    # combine exclude lists
    exclude = drop + exclude
    #update config
    config['metadata']['subjects']['exclude'] = exclude
    
    ##-------final version of df
    #merge
    df = pd.merge(df, df_error[['TrialNum_','m_rt','accuracy','m_diff_dotloc','m_diff_stim','participant']]\
                  .drop_duplicates(subset="participant", keep="first"), how='left', on='participant')

    ##export for seperate analysis in r
    csv_path = path_['output'] + "/analysis/final_data.csv"
    console('Step: export for R analysis: %s'%(csv_path), 'red')
    df.to_csv(csv_path, index=None)        

    ##--------number of subjects
    # demographics
    l_demographics = df_demographics['participant'].astype('int').to_list()
    config['metadata']['subjects']['demographics'] = l_demographics
    # task
    l_task = df_metadata['participant'].astype('int').to_list()
    config['metadata']['subjects']['task'] = l_task
    # eyetracking
    l_eyetracking = df_metadata.loc[df_metadata['is_eyetracking'] == True]['participant'].astype('int').to_list()
    config['metadata']['subjects']['eyetracking'] = l_eyetracking
    ## calibratied 
    l_calibrated = df_metadata.loc[df_metadata['is_calibrated'] == True]['participant'].astype('int').to_list()
    config['metadata']['subjects']['calibrated'] =  l_calibrated
    # behavioral
    l_behavioral = df_metadata.loc[df_metadata['is_eyetracking'] == False]['participant'].astype('int').to_list()
    config['metadata']['subjects']['behavioral'] = l_behavioral
    # cesd
    l_cesd = df_cesd['participant'].astype('int').to_list()
    config['metadata']['subjects']['cesd'] = l_cesd
    # mmpi
    l_mmpi = df_mmpi['participant'].astype('int').to_list()
    config['metadata']['subjects']['mmpi'] = l_mmpi
    # webcam
    config['metadata']['subjects']['webcam'] = df_metadata.drop_duplicates(subset="participant",
          keep="first").loc[:,'WebcamMessage'].value_counts().to_dict()

    # get actual participants used in analysis
    subjects_eyetracking_used = len(glob.glob(path_['output'] + "/tlbs/eyetracking/*.csv"))
    subjects_behavioral_used = len(glob.glob(path_['output'] + "/tlbs/behavioral/*.csv"))
                
    # get subjects used
    if config['processing']['type'] == 'eyetracking':
        subjects_used = config['metadata']['subjects']['eyetracking']
    else:
        subjects_used = config['metadata']['subjects']['behavioral']
        
    ##--------date
    date_start = dict((key,d[key]) for d in date_start for key in d)
    date_end = dict((key,d[key]) for d in date_end for key in d)
    
    del p_bias, p_cesd, p_demo, p_mmpi, p_subject, color, csv_path
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------demographic statistics
is_['demographic'] = True
if is_['demographic']:
    #-----------------------------get max, min values
    total = {}
    #----drop non-eyetracking participants
    df_d = df_s[df_s['participant'].isin(l_eyetracking)]
    
    #----subset dataframe to cesd low and high
    #cesd high
    df_dh = df_d.loc[df_d['cesd_score'] > 15].drop_duplicates(subset="participant", keep="first")
    #cesd low
    df_dl = df_d.loc[df_d['cesd_score'] <= 15].drop_duplicates(subset="participant", keep="first")
    
    #get total used
    total['High'] = len(df_dh['participant'].unique())
    total['Low'] = len(df_dl['participant'].unique())
    total['all'] = len(l_eyetracking)
    
    #-----------------------------descriptive demographic stats
    console('Step: descriptive demographic', 'red')
    rows = []
    #----age, cesd, rrs
    l_label = ['Age','Center for Epidemiologic Studies Depression Scale',"Ruminative Response Scale"]
    l_category = ['age','cesd_score','rrs_brooding']
    for label, category in zip(l_label, l_category):
        low = [str(round(df_dl[category].mean(),1)), '(%s)'%(str(round(df_dl[category].std(),1)))]
        high = [str(round(df_dh[category].mean(),1)), '(%s)'%(str(round(df_dh[category].std(),1)))]
        rows.append([label,"(SD)", low[0], low[1], high[0], high[1]])
     
    #----normal vision, corrective vision, handedness, hispanic
    l_label = ['Vision','Vision','Handedness (Right)','Hispanic or Latino']
    l_group = ['Normal','Corrective','Right','(%)']
    l_category = ['is_normalvision','is_corrective','handedness','hispanic']
    l_condition = [True,True,'Right',True]
    #Handedness (Right), Corrective, is_corrective, True
    for label, group, category, condition in zip(l_label, l_group, l_category, l_condition):
        #cesd low
        df_sum = df_d.loc[(df_d[category] == condition) & (df_d['cesd_group'] == 'Low')]
        count = int(len(df_sum.index))
        pct = '%.1f'%(round(count/total['Low'], 4)*100)
        low = [count,'(%s)'%(pct)]
        #cesd high
        df_sum = df_d.loc[(df_d[category] == condition) & (df_d['cesd_group'] == 'High')]
        count = len(df_sum.index)
        pct = '%.1f'%(round(count/total['High'], 4)*100)
        high = [count,'(%s)'%(pct)]
        #append
        rows.append(['%s'%(label), group, low[0], low[1], high[0], high[1]])
            
    #----eye color, gender, race
    l_label = ['Race','Gender','Eye Color']
    l_category = ['race','gender','eye_color']
    for label, category in zip(l_label, l_category):
        l_group = df_d[category].unique().tolist()
        for group in l_group:
            #cesd low
            df_sum = df_d.loc[(df_d[category] == group) & (df_d['cesd_group'] == 'Low')]
            count = int(len(df_sum.index))
            pct = '%.1f'%(round(count/total['Low'], 4)*100)
            low = [count,'(%s)'%(pct)]
            #cesd high
            df_sum = df_d.loc[(df_d[category] == group) & (df_d['cesd_group'] == 'High')]
            count = len(df_sum.index)
            pct = '%.1f'%(round(count/total['High'], 4)*100)
            high = [count,'(%s)'%(pct)]
            #append
            group = group.title().replace('Or','or').replace('And','and').replace('Of','of').replace('The','the')
            rows.append(['%s'%(label), group, low[0], low[1], high[0], high[1]])

    #-----to df
    # create new columns
    cesd_col = ['CESD < 16<span class="nval">(n=%s)</span>'%(total['Low']), 'CESD ≥ 16<span class="nval">(n=%s)</span>'%(total['High'])]
    descriptive = pd.DataFrame(rows)
    descriptive = descriptive.rename(columns={0:'ID',1:'Group', 2:cesd_col[0], 3:'a', 4:cesd_col[1], 5:'b'})
    # sort order
    l_sort = ['Age','Vision','Eye Color','Handedness (Right)','Gender','Hispanic or Latino','Race', 
              'Center for Epidemiologic Studies Depression Scale','Ruminative Response Scale']
    descriptive['ID'] = pd.Categorical(descriptive['ID'], l_sort)
    # sort
    descriptive = descriptive.sort_values(['ID',cesd_col[0]], ascending=[True, False])
    # merge columns
    descriptive[cesd_col[0]] = descriptive[[cesd_col[0], 'a']].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    descriptive[cesd_col[1]] = descriptive[[cesd_col[1], 'b']].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    # delete
    descriptive.drop(descriptive.columns[[3,5]], axis=1, inplace=True)
    del descriptive.index.name
    
    #-----create html
    html_name = 'demographic'
    html_path = path_['output'] + "/analysis/html/%s.html"%(html_name)
    title = '<b>Table 1.</b> Participant characteristics (N = %s).'%(total['all'])
    footnote = "<div id='note'>N = Sample size of eyetracking participants. Total participants = %s."%(config['metadata']['subjects']['task'])
    html = plot.html(config=config, df=descriptive, path=html_path, name=html_name, 
                      source="demographic", title=title, footnote=footnote)
    
    #breakpoint()
    #del df_sum, index, value, above_pct, rows, html_path, title, html, html_name
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------list of variables
is_['variables'] = True
if is_['variables']:
    console('Step: list of variables', 'red')
    df_variables = processing.variables(df=df)
    
    ##create html
    html_name = 'definitions'
    html_path = path_['output'] + "/analysis/html/%s.html"%(html_name)
    title = '<b>Table 1.</b> Task Variables and Definitions.'
    html = plot.html(config=config, df=df_variables, path=html_path, name=html_name, source="definitions", title=title)
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------descriptive device
is_['descriptive'] = True
if is_['descriptive']:
    console('Step: descriptive device', 'red')
    rows = []
    ##--------os browser gpu type Webcam resolution Webcam message
    os_ = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'os'].value_counts()
    for index, value in os_.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Operating System","%s"%(index), '%s (%s)'%(value,above_pct)])
    del os_
    
    # ##--------os_version
    os_ = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'os_version'].value_counts()
    for index, value in os_.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Operating System version","%s"%(index), '%s (%s)'%(value,above_pct)])
    del os_
        
    ##--------browser
    browser = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'browser'].value_counts()
    for index, value in browser.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Browser","%s"%(index), '%s (%s)'%(value,above_pct)])
    del browser
    
    ##--------browser_version
    browser = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'browser_version'].value_counts()
    for index, value in browser.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Browser version","%s"%(index), '%s (%s)'%(value,above_pct)])
    del browser
    
    ##--------gpu type 
    gpu_type = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'gpu_type'].value_counts()
    for index, value in gpu_type.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["GPU type","%s"%(index), '%s (%s)'%(value,above_pct)])
    del gpu_type
    
    ##--------webcam brand
    gpu = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'gpu'].value_counts()
    for index, value in gpu.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["GPU model","%s"%(index), '%s (%s)'%(value,above_pct)])
    del gpu
    
    ##--------devicepixelratio
    display = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'devicePixelRatio'].value_counts().sort_index(axis=0)
    for index, value in display.items():
        index = '%.2f'%(round(index, 2))
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["devicePixelRatio","%s"%(index), '%s (%s)'%(value,above_pct)])
    del display
        
    ##--------display resolution
    display = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'monitorSize'].value_counts()
    for index, value in display.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Display resolution","%s"%(index), '%s (%s)'%(value,above_pct)])
    del display
    
    ##--------webcam message
    webcam_m = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'WebcamMessage'].value_counts()
    for index, value in webcam_m.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Webcam message","%s"%(index), '%s (%s)'%(value,above_pct)])
    
    ##--------webcam brand
    webcamb = df_s.drop_duplicates(subset="participant", keep="first").loc[:,'webcam_brand'].value_counts()
    for index, value in webcamb.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Webcam brand","%s"%(index), '%s (%s)'%(value,above_pct)])
    del webcamb   
    
    ##--------Webcam resolution
    webcamr = df_s[~df_s['webcamSize'].isin(['.x.'])].drop_duplicates(subset="participant",
                    keep="first").loc[:,'webcamSize'].value_counts()
    for index, value in webcamr.items():
        above_pct = '%.1f'%(round(value/len(config['metadata']['subjects']['task']), 4)*100)
        rows.append(["Webcam resolution","%s"%(index), '%s (%s)'%(value,above_pct)])
    del webcamr
    
    #-------to df
    descriptive = pd.DataFrame(rows)
    descriptive = descriptive.rename(columns={0:'ID',1:'Group',2:'Statistic'})
    del descriptive.index.name
    
    #footnote
    footnote = [
    '<div class="description">\n',
        'During data collection, participants screen resolution were multiplied by the pixel density ratio, or\
        <a class="ref" href="https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio"><i>devicePixelRatio</i></a>\
        (i.e. width = screen.width / devicePixelRatio = 1920 * 1.5). This was done with the intent of storing true device \
        physical resolution. However to simplify analysis using webgazer, which uses the same initial value \
        to calculate gaze location, participants screen resolution is reverted back to its original value.\n',
    '</div>\n']
    footnote = ''.join(footnote)
    
    #create html
    html_name = 'device'
    html_path = path_['output'] + "/analysis/html/%s.html"%(html_name)
    title = '<b>Table 1.</b> Device characteristics (N = %s).'%(config['metadata']['subjects']['task'])
    html = plot.html(config=config, df=descriptive, path=html_path, name=html_name, source="device", title=title, footnote=footnote)
    del index, value, above_pct, rows, html_path, title, footnote, html, html_name
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------descriptive task
is_['task'] = True
if is_['task']:
    console('Step: descriptive task', 'red')
    rows = []
    total = {}
    
    #----totals
    total['Low'] = len(df_s['participant'].loc[(df_s['cesd_group'] == 'Low')].unique())
    total['High'] = len(df_s['participant'].loc[(df_s['cesd_group'] == 'High')].unique())
    
    #----pre-task: demographics
    score = []
    for cesd in ['Low','High']:
        df_sum = df_s.loc[(df_s['cesd_group'] == cesd)]
        count = len(df_sum.index)
        pct = '%.1f'%(round(count/total[cesd], 4)*100)
        score.append('%s (%s)'%(count, pct))
    #add
    rows.append(["Pre-Questionnaire", "Demographics", score[0], score[1]])
    
    #----pre-task: cesd, rss
    score = []
    for cesd in ['Low','High']:
        df_sum = df_s.loc[(df_s['cesd_group'] == cesd)]
        count = len(df_sum.index)
        pct = '%.1f'%(round(count/total[cesd], 4)*100)
        score.append('%s (%s)'%(count, pct))
    #add
    rows.append(["Pre-Questionnaire", "CES-D, RRS", score[0], score[1]])
    
    #----task
    l_label = ['Task','Task','Task','Task']
    l_group = ['Task','Eyetracking','Calibrated','Behavioral']
    l_category = ['is_task','is_eyetracking','is_calibrated','is_eyetracking']
    l_bool = [True,True,True,False]
    #convert to bool
    df_s[l_category] = df_s[l_category].astype('bool')
    #for each
    for label, group, category, bool_ in zip(l_label, l_group, l_category, l_bool):
        # for each cesd score
        score = []
        for cesd in ['Low','High']:
            df_sum = df_s.loc[(df_s[category] == bool_) & (df_s['cesd_group'] == cesd)]
            count = int(len(df_sum.index))
            pct = '%.1f'%(round(count/total[cesd], 4)*100)
            score.append('%s (%s)'%(count, pct))
        # add
        rows.append([label, group, score[0], score[1]])
    
    #----post-task: mmpi
    df_mmpi2 = df_mmpi.merge(df_s,on='participant')
    score = []
    for cesd in ['Low','High']:
        df_sum = df_mmpi2.loc[(df_mmpi2['cesd_group'] == cesd)]
        count = len(df_sum.index)
        pct = '%.1f'%(round(count/total[cesd], 4)*100)
        score.append('%s (%s)'%(count, pct))
    #add
    rows.append(["Post-Questionnaire", "MMPI", score[0], score[1]])       

    #----to df
    descriptive = pd.DataFrame(rows)
    low='CESD < 16 <span class="nval">(n=%s)</span>'%(total['Low'])
    high='CESD ≥ 16 <span class="nval">(n=%s)</span>'%(total['High'])
    descriptive = descriptive.rename(columns={0:'ID',1:'Group',2:low,3:high})
    del descriptive.index.name
    
    #----create html
    title = '<b>Table 1.</b> Schedule of Assessments.'
    # no_webcam
    total = config['metadata']['subjects']['webcam']['NotFoundError']/len(config['metadata']['subjects']['task'])
    no_webcam = '%s, %s%%'%(config['metadata']['subjects']['webcam']['NotFoundError'], '%1.f'%(round(total, 5)*100))
    # blocked_webcam
    total = config['metadata']['subjects']['webcam']['NotAllowedError']/len(config['metadata']['subjects']['task'])
    blocked_webcam = '%s, %s%%'%(config['metadata']['subjects']['webcam']['NotAllowedError'], '%1.f'%(round(total, 5)*100))
    #calibrated
    total = len(config['metadata']['subjects']['calibrated'])/len(config['metadata']['subjects']['eyetracking'])
    footnote = [
        '<div class="paragraph">',
            '<a class="note" name="1"><sup>1</sup></a>',
            'Data were collected from %s to %s. '%(date_start['metadata'],date_end['metadata']),
            'Participants unable to meet the eyetracking device requirements (e.g. Chrome and Firefox, webcam, laptop or desktop) ',
            'were placed in the behavioral version of dotprobe. Reasons include: participant dropout, ',
            '<a tabindex="0" class="popover-anchor" link-id="iaps" data-toggle="popover" data-content="NotFoundError" \
            title="WebcamMessage">no webcam present on the device</a> (n=%s) and '%(no_webcam),
            '<a tabindex="0" class="popover-anchor" link-id="iaps" data-toggle="popover" data-content="NotAllowedError" \
            title="WebcamMessage">blocked access of the webcam</a> by the participants browser (n=%s).</div>'%(blocked_webcam),
        '<div class="paragraph">',
            'Once completing the <i>Pre-Questionnaire</i> on REDCap, participants are redirected to the task. ',
            'Possible reasons for the drop off between <i>Pre-Questionnaire</i> (n=%s) \
            and <i>Task</i> (n=%s) samples can be due to: '\
            %(len(config['metadata']['subjects']['cesd']), len(config['metadata']['subjects']['task'])),
            'Technical error during redirect, and disinterest in continuing to participate in the experiment. ',
        '</div>'
    ]
    footnote = ''.join(footnote)
    
    #create html
    html_name = 'task'
    html_path = path_['output'] + "/analysis/html/%s.html"%(html_name)
    html = plot.html(config=config, df=descriptive, path=html_path, source="task", name=html_name, title=title, footnote=footnote)
    
    del html_name, html_path, no_webcam, blocked_webcam, descriptive, total, df_mmpi2, score, cesd, count, pct, rows
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------summary data
is_['summary'] = True
if is_['summary']:
    console('Step: summary data', 'red')
    rows = []
    #-----------------------------testing group by cesd group (high, low) and trial type mean
    df_mean_std = df[['dp_bias','n_dp_valid','pct_dp_toward','mean_dp_toward','mean_dp_away','var_dp_bias','gaze_bias',
                    'init_gaze_bias','final_gaze_bias','n_gaze_valid','n_gaze_toward','pct_gaze_center','mean_gaze_toward',
                    'mean_gaze_away','var_gaze_bias','dp_gaze_cor','trialType_',
                    'luminance','m_diff_stim','m_diff_dotloc']]
    
    #------------------------get list of columns
    l_var = list(df_mean_std)
    l_var_gaze = ['gaze_bias','init_gaze_bias','final_gaze_bias','n_gaze_valid','n_gaze_toward','pct_gaze_center',
                  'mean_gaze_toward','mean_gaze_away','var_gaze_bias']
    l_var_dp = ['dp_bias','n_dp_valid','pct_dp_toward','mean_dp_toward','mean_dp_away','var_dp_bias']
    
    ##--------crate rows
    df_mean_std = df_mean_std.groupby(['trialType_']).agg(['mean','std']).T.unstack(level=1)
    #collapse headers
    df_mean_std.columns = [' '.join(col).strip() for col in df_mean_std.columns.values]
    #combine columns
    df_mean_std['iaps'] = df_mean_std['iaps mean'].round(4).astype(str) + " (" + df_mean_std['iaps std'].round(4).astype(str) + ")"
    df_mean_std['pofa'] = df_mean_std['pofa mean'].round(4).astype(str) + " (" + df_mean_std['pofa std'].round(4).astype(str) + ")"
    #reindex and make new column for factor
    df_mean_std['variable'] = df_mean_std.index
    df_mean_std = df_mean_std.rename({'index': 'variable'}).reset_index(level=0,  drop=True)
    #create group column
    df_mean_std = df_mean_std.rename({'dp_gaze_corr': 'dpg_core'})
    df_mean_std['group'] = pd.np.where(df_mean_std['variable'].str.contains("gaze_"), "gaze",
                            pd.np.where(df_mean_std['variable'].str.contains("dp_"), "dotprobe", "task"))
    
    df_mean_std = df_mean_std[['group','variable','iaps','pofa']]
    del df_mean_std.index.name
    
    #footnote
    footnote = [
    '<div class="description">',
    '</div>\n'
    ]
    footnote = ''.join(footnote)
    
    #create html
    html_name = 'summary' 
    html_path = path_['output'] + "/analysis/html/%s.html"%(html_name)
    title = '<b>Table 1.</b> Summary Statistics (N = %s).'%(subjects_used)
    html = plot.html(config=config, df=df_mean_std, path=html_path, name=html_name, source="summary", title=title, footnote=footnote)
    
    del l_var, l_var_gaze, l_var_dp, rows, html_name, html_path, title, footnote, html
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------save config
is_['config'] = True
if is_['config']:
    # add definitions to config
    config = settings.definitions(config)
    # save
    p_json = path_['output'] + "/analysis/config.json"
    with open(p_json, 'w') as f:
        json.dump(config, codecs.open(p_json, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
        
        
    
        
        
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------plots
is_['plots'] = True
if is_['plots']:
    console('Step: plots', 'red')
    is_['single'] = True
    #%%------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------single subject: trial
    if is_['single']:
        """
        Resources:
        - https://media.springernature.com/original/springer-static/image/
            art%3A10.3758%2Fs13428-017-0913-7/MediaObjects/13428_2017_913_Figa_HTML.gif
        """
        #-------------------------------------------------single subject bokeh coordinates (all trials)
        console('Step: bokeh_trial()', 'red')
        subject = 31
        session = 0
        #data
        path_sns = path_['output'] + "/process/data/eyetracking/%s_%s.csv"%(subject,session)
        df_single = pd.read_csv(path_sns, float_precision='high')
        #rename
        df_single = df_single.rename(columns={"LEmotion":"left_mood","REmotion":"right_mood"})
        #exclude columns
        df_single = df_single[['participant','session','subsession','TrialNum','timestamp','trialType','isCongruent',
                                'left_mood','right_mood','monitorSize.px',
                                'x','y','marker','sg_x','sg_y','sg_class',
                                'sg_fix_all','sg_fix_index',
                                'sg_all_bounds','sg_fix_bounds','fix_num',
                                'left_bound','right_bound','dwell']]
        
        #get rois
        stim_bounds, roi_bounds = processing.roi(filters=filters, flt=filters[0][1], df=df_single, manual=True)
        #for each subject
        flt = 'sg'
        for idx in range(198):
            #subset data
            df_single_ = df_single[df_single['TrialNum'].isin([idx])].reset_index(drop=True)
            #draw plot
            bokeh_plot = plot.bokeh_trial(config=config, df=df_single_, stim_bounds=stim_bounds, roi_bounds=roi_bounds, flt='sg')
            ##get is_congruent
            isCongruent = "congruent" if df_single_['isCongruent'][0] == True else "incongruent"
            #html
            title = "(%s) Participant %s, session %s"%(isCongruent, subject, session)
            html_path = path_['output'] + "/analysis/html/trial/%s_%s_%s.html"%(subject,session,idx)
            html = plot.html(config=config, path=html_path, plots=bokeh_plot, source="bokeh", 
                              display="trial", trial=idx, title=title)
                                 
        del idx, title, path_sns, bokeh_plot, df_single_, html_path, html, subject, session
    #%%------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------single subject: calibration, validation
        print(console['green'] + 'bokeh_calibration()', 'red')
        subject = 'shellie'
        session = 1
        #monitorSize = [1920,1080] #session 0
        monitorSize = [1280,800] #session 1
        
        #for calibration/validation event 0,1,2
        for block in range(1,4):
            #---import data
            path_sns = path_['output'] + "/calibration/%s_%s_%s_calibration.csv"%(subject, session, block)
            df_cv = pd.read_csv(path_sns, float_precision='high')
            #----get calibration points
            cxy = df_cv.groupby(['cx','cy']).size().reset_index().rename(columns={0:'count'})
            #calibration and validation
            for event, full in zip(['isCalibrating','isValidating'],['calibration','validation']):
                #subset data
                df_cv_ = df_cv.loc[df_cv['event'] == event].reset_index(drop=True)
                #draw plot
                bokeh_plot = plot.bokeh_calibration(config=config, df=df_cv_, cxy=cxy, event=full, monitorSize=monitorSize)
                #html
                title = "Participant %s"%(subject)
                html_path = path_['output'] + "/analysis/html/cv/%s_%s_%s_%s.html"%(subject, session, block, full)
                html = plot.html(config=config, path=html_path, plots=bokeh_plot, source="bokeh", title=title, 
                                  footnote=config['def'][full], display=full, trial=full, block=full, session=session)
                             
        #del title, event, full, path_sns, bokeh_plot, html_path, html

    is_['density'] = True
    #%%------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------density plot
    if is_['density']:
        console('Step: density_plot()', 'red')
        #Computes and draws density plot (kernel density estimate), which is a smoothed version of the histogram. 
        #This is used as a gage for normality
        df_density = df[['participant','trialType_','m_rt',
                          'm_diff_dotloc','m_diff_stim','luminance',
                          'rrs_brooding','cesd_score','cesd_group',
                          'dp_bias','n_dp_valid','gaze_bias','n_gaze_valid',
                          'var_gaze_bias','final_gaze_bias']].loc[df['nested'] == 'subject']   
        
        #----exclude
        df_density = df_density[~df_density['participant'].isin(exclude)]   
        
        #file
        title = string.capwords('kernel density estimate')
        
        #create images
        density, html_plots = plot.density_plot(config=config, df=df_density, title=title)
        #description of plots
        intro = "The kernel density estimate (kde) is used here as a quick check of normality for each of the variables of \
        interest in the model. All data here has been nested by subject. %s"%(config['def']['exclude'])
        #create html
        html_path = path_['output'] + "/analysis/html/density.html"
        html = plot.html(config=config, path=html_path, plots=html_plots, source="plots", intro=intro)
        del density, intro, html_plots, html_path, html, title
        
    is_['corr'] = True 
    #%%------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------correlation matrix
    if is_['corr']:
        console('Step: corr_matrix()', 'red')
        #run correlation matrix
        df_corr = df[['dp_bias','n_dp_valid','var_dp_bias',
                      'gaze_bias','n_gaze_valid','var_gaze_bias','final_gaze_bias',
                      'rrs_brooding','cesd_score',
                      'm_rt','m_diff_dotloc','m_diff_stim',
                      'luminance']].loc[df['nested'] == 'subject']
        
        #file
        file = 'corr_matrix'
        method = 'spearman'
        title = string.capwords('%s correlation coefficient matrix (p-value).'%(method))
        
        path = path_['output'] + "/analysis/html/%s.html"%(file)
        corr_matrix = plot.corr_matrix(config=config, df=df_corr, path=path, title=title, method=method)
        del path, corr_matrix, file, title, method
    
    is_['boxplot'] = True
    #%%------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------boxplot
    if is_['boxplot']:
        console('Step: boxplot()', 'red')
        #----create temp df
        html_plots = []
        html_file = 'rt_boxplot'
        x = ['race','gender','is_normalvision','os']
        cat = 'demographics'

        #----exclude
        df_ = df_error[~df_error['participant'].isin(exclude)]
        
        ##-------response time
        y = 'Key_Resp_rt'
        intro = 'This was done to compare differences in response time between os, webcamsize, gender, race and other factors.'
        footnote = "Data collapsed by subject. Participants identified 'race' as 'American Indian or Alaska Native','Two or more \
        races', 'Black or African American', 'None of the above' were excluded here for displaying purposes.\
        %s"%(config['def']['exclude'])
        #create plot
        file = 'rt_boxplot'
        title = 'Boxplots, %s (N = %s)'%(y, subjects_used)
        sns_path = path_['output'] + "/analysis/html/img/%s.png"%(file)
        plot.boxplot(config=config, df=df_, path=sns_path, x=x, y=y, cat=cat)
        html_plots.append({"title":title,"file":"%s.png"%(file),"footnote":footnote})
        
        ##-------diff_dotloc
        y = 'diff_dotloc'
        intro = 'This was done to compare differences between expected and true dotloc onset between os, webcamsize, \
        gender, race and other factors.'
        footnote = "Data collapsed by subject. Participants identified 'race' as 'American Indian or Alaska Native','Two or more \
        races', 'Black or African American', 'None of the above' were excluded here for displaying purposes.\
        %s"%(config['def']['exclude'])
        #create plot
        file = 'dotloc_boxplot'
        title = 'Boxplots, %s (N = %s)'%(y, subjects_used)
        sns_path = path_['output'] + "/analysis/html/img/%s.png"%(file)
        plot.boxplot(config=config, df=df_, path=sns_path, x=x,y=y, cat=cat)
        html_plots.append({"title":title,"file":"%s.png"%(file),"footnote":footnote})
        
        ##-------diff_stim
        y = 'diff_stim'
        intro = 'This was done to compare differences between expected and true stim onset between os, webcamsize, \
        gender, race and other factors.'
        footnote = "Data collapsed by subject. Participants identified 'race' as 'American Indian or Alaska Native','Two or more \
        races', 'Black or African American', 'None of the above' were excluded here for displaying purposes.\
        %s"%(config['def']['exclude'])
        #create plot
        file = 'stim_boxplot'
        title = 'Boxplots, %s (N = %s)'%(y, subjects_used)
        sns_path = path_['output'] + "/analysis/html/img/%s.png"%(file)
        plot.boxplot(config=config, df=df_, path=sns_path, x=x,y=y, cat=cat)
        html_plots.append({"title":title,"file":"%s.png"%(file),"footnote":footnote})
        
        #-------save folders
        html_path = path_['output'] + "/analysis/html/%s.html"%(html_file)
        html = plot.html(config=config, path=html_path, plots=html_plots, source="plots", display="boxplot", intro=intro)
        del intro, html_file, file, title, html_path, html, cat, x, y, footnote
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------methods
is_['methods'] = True
if is_['methods']:
    '''
    Resources
    ---------
    Example articles for reporting methods/results:
        - lmer: https://www.sciencedirect.com/science/article/pii/S0028393217301197#bib19
        - classify: https://www.sciencedirect.com/science/article/pii/S0028393217301197#bib19
        - roi: https://www.sciencedirect.com/science/article/pii/S0028393217301197#bib19
        - luminance: https://ars.els-cdn.com/content/image/1-s2.0-S0022096516301023-mmc1.pdf
    '''
    # #----load config
    # p = path_['output'] + "/analysis/config.json"
    # with open(p) as f:
    #     config_ = json.loads(f.read())
    config_ = config
    console('fix config', 'red')
        
    #----start
    def_ = config_['metadata']['def']
    cite_ = config_['metadata']['cite']
    source = 'methods'
    title = 'Methods'
    path = path_['output'] + "/analysis/html/%s.html"%(source)
    methods = [
        '<div class="paragraph">',
            '<div class="subtitle" id="webgazer">Webgazer.js</div>',
            '<span>' + def_['filter'] + '</span>',
        '</div>',
        '<div class="paragraph">',
            '<div class="subtitle" id="task_design">Task Design </div>',
            '<span>' + def_['task_design'] + '</span>',
        '</div>',
        '<div class="paragraph">',
            '<div class="subtitle">Calibration/Validation</div>',
            '<div class="subtitle2" id="calibration">Calibration</div>',
            '<span>' + def_['calibration'] + '</span>',
            '<div class="subtitle2" id="validation">Calibration</div>',
            '<span>' + def_['validation'] + '</span>',
        '</div>',
        '<div class="paragraph">',
            '<div class="subtitle">Preprocessing</div>',
            '<span>' + cite_['preprocessing'] + '</span>',
            '<div class="subtitle2" id="filter">Filtering</div>',
            '<span>' + '' + '</span>',
            '<div class="subtitle2" id="classify">Classifying Events</div>',
            '<span>' + cite_['hmm'] + '</span>',
            '<div class="subtitle2" id="classify">semeon: use this as example for writing (filtering)</div>',
            '<span>' + def_['filter'] + '</span>',
        '</div>',
        '<div class="paragraph">',
            '<div class="subtitle" id="model">Modelling</div>',
            '<span>' + ''+ '</span>',
        '</div>',
        '<div class="paragraph">',
            '<div class="subtitle">Outliers</div>',
            '<div class="subtitle2" id="device">Device</div>',
            '<span>' + ''+ '</span>',
            '<div class="subtitle2" id="onset_error">Onset Error</div>',
            '<span>' + '' + '</span>',
        '</div>'
    ]
    methods = ('\n\t'.join(map(str, methods)))
    html = plot.html(plots=methods, config=config, path=path, source=source, title=title, name='methods')
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------analysis
is_['analysis'] = True
if is_['analysis']:
        '''
        Resources
        ---------
        Choosing the best model:
            - https://rpsychologist.com/r-guide-longitudinal-lme-lmer
            - https://stats.idre.ucla.edu/other/mult-pkg/whatstat/
            - https://stats.stackexchange.com/a/303592
            - https://tsmatz.wordpress.com/2017/08/30/glm-regression-logistic-poisson-gaussian-gamma-tutorial-with-r/
        Example articles for reporting methods/results:
            - lmer: https://www.sciencedirect.com/science/article/pii/S0028393217301197#bib19
            - 
        '''
        #----start
        is_['dwell'] = True
#%%--------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------anova: dwell time
        if is_['dwell']:
            console('Step: ANOVA (dwell time)', 'red')
            effects = {}
            
            #----load config
            # p = path_['output'] + "/analysis/config.json"
            # with open(p) as f:
            #     config_ = json.loads(f.read())
            config_ = config
            console('fix config', 'red')   
                
            #----exclude
            exclude = config_['metadata']['subjects']['exclude']
            
            #----load data
            p = path_['output'] + "/analysis/final_data.csv"
            df_ = pd.read_csv(p, float_precision='high')
            
            #-----parameters
            # dependent variable
            y = 'dwell_time'
            # main effects
            effects['main'] = {
                'cesd_group': 'categorical',
                'aoi': 'categorical',
                'trialType': 'categorical'
            }
            # random effects
            effects['random'] = {
                'participant': 'categorical'
            }
            # formula
            f = "%s ~ cesd_group + aoi + trialType + (1|participant)"%(y)
            
            #----save data for access by R and for calculating dwell time
            csv = "dwell_data.csv"
            p = path_['output'] + "/analysis/html/model/anova/"
        
 			#-----calculate dwell time using multiprocessing
 			# use __name__ to protect main module
            df_dwell, error_dwell = processing.dwell(df=df_, cores=7) if __name__ == '__main__' else None
        
            #----normalize dwell_time for comparison between iaps and pofa
            df_dwell['dwell_time'] = df_dwell.apply(lambda x: (x['dwell_time']/4500) 
            if (x['trialType'] == 'iaps') else (x['dwell_time']/3000), axis=1)
            
 			#-----exclude participants, group by subject:trialType:aoi
            # exclude participants 
            df_dwell = df_dwell[~df_dwell['participant'].isin(exclude)]
            # groupby
            df_dwell = df_dwell.groupby(['participant','cesd_group','trialType','aoi'])['dwell_time'].mean().reset_index()

 			#-----run
            anova_, anova_result, anova_r, html = model.anova(config=config_, df=df_dwell, y=y, f=f, csv=csv, path=p, effects=effects)
            
            #-----delete
            del y, f, csv, p
        
        is_['diff'] = True
#%%--------------------------------------------------------------------------------------------------------------------------
#---------------------------------------Linear Mixed Model Regression with random effects: stimulus/dotloc onset error (lmer)
        if is_['diff']:
            console('Step: Linear Mixed Model Regression', 'red')
            effects = {}
            
            # #----load config
            # p = path_['output'] + "/analysis/config.json"
            # with open(p) as f:
            #     config_ = json.loads(f.read())
            config_ = config
            console('fix config', 'red')   
            
            #----load data
            p = path_['output'] + "/analysis/error.csv"
            #df_error = pd.read_csv(p_error, float_precision='high')
            df_ = pd.read_csv(p, float_precision='high')
            
            #----parameters            
            # dependent variable
            y = ['diff_stim','diff_dotloc'] #build models for each IV in list
            # fixed effects
            effects['fixed'] = {
                'os': 'categorical',
                'trialType': 'categorical',
                'TrialNum': 'factorial'
            }
            # random effects
            effects['random'] = {
                'TrialNum': 'factorial',
                'participant': 'factorial',
            }
            
            #----save data for access by R and for calculating dwell time
            csv = "onset_data.csv"
            
            #----run model for each IV
            for _y in y:
                # path
                p = path_['output'] + "/analysis/html/model/lmer/"
                # formula
                f = "sqrt(%s) ~ os + trialType + TrialNum + (1+TrialNum|participant)"%(_y)
                # run
                lmer_, lmer_result, lmer_r, html = model.lmer(config=config_, df=df_, y=_y, f=f, exclude=exclude, csv=csv, path=p, effects=effects)
                
            #-----delete
            del y, _y, f, csv, p
        
        is_['mixed'] = True
#%%--------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------analysis of varience (anova): bias
        if is_['mixed']:
            effects = {}
            
            # #----load config
            # p = path_['output'] + "/analysis/config.json"
            # with open(p) as f:
            #     config_ = json.loads(f.read())
            config_ = config
            console('fix config', 'red')   
            #----load data
            p = path_['output'] + "/analysis/final_data.csv"
            df_ = pd.read_csv(p, float_precision='high')
            
            #-----exclude participants, group by subject
            # exclude participants
            df_ = df_[~df_['participant'].isin(exclude)]
            
            # groupby
            df_ = df_.loc[df_['nested'] == 'trialType']
            
            #----parameters
            # dependent variable
            y = ['dp_bias','gaze_bias']
            # main effects
            effects['main'] = {
                'cesd_group': 'categorical',
                'trialType': 'categorical'
            }
            # random effects
            effects['random'] = {
                'participant': 'categorical'
            }
            
            #----create function for each IV
            for _y in y:
                console('Step: ANOVA (%s)'%(_y), 'red')
                #----save data for access by R
                csv = "%s.csv"%(_y)
                #-----path
                p = path_['output'] + "/analysis/html/model/anova/"
                #-----formula
                f = "%s ~ cesd_group + trialType + (1|participant)"%(_y)
                #-----run
                anova_, anova_result, anova_r, html = model.anova(config=config, df=df_, y=_y, f=f, csv=csv, path=p, effects=effects)
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------test
#------------------------------------------------------------------------draw flowchart of study identification and inclusion
is_['flowchart'] = False
if is_['flowchart']:
    #see https://graphviz.readthedocs.io/en/stable/examples.html
    import graphviz as gv
    
    #path
    folder = path_['output'] + "/analysis/"
    
    g = gv.Digraph('G', filename = folder + 'workflow.gv')
    g.attr(compound='true')
    
    with g.subgraph(name='cluster0') as c:
        c.edges(['ab', 'ac', 'bd', 'cd'])
    
    with g.subgraph(name='cluster1') as c:
        c.edges(['eg', 'ef'])
    
    g.edge('b', 'f', lhead='cluster1')
    g.edge('d', 'e')
    g.edge('c', 'g', ltail='cluster0', lhead='cluster1')
    g.edge('c', 'e', ltail='cluster0')
    g.edge('d', 'h')
    
    g.view()
pass#------------------------------------------------------------------------------------------------------------------------test
#------------------------------------------------------------------------draw flowchart of study identification and inclusion
is_['treeview'] = False
if is_['treeview']:
    #create file tree view
    #see https://graphviz.readthedocs.io/en/stable/examples.html
    from treelib import Node, Tree
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    tree.show()
pass
#%%--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------finished
#-------------------------------------------------------------------------------------------------------------garbage collect
# import gc
# gc.collect()
#-------------------------------------------------------------------------------------------------------------quick functions
#get list of columns
#lst = list(df)
#install pip package
#from pip._internal import main as _main
#_main(['install','statsmodels'])

#--------------------------------------------------------------------------------------------------------------iPython Magics
#%matplotlib qt5
#%matplotlib tk
#%matplotlib inline

#----------------------------------------------------------------------------------------------------------------other magics
# from pdb import set_trace as breakpoint
# breakpoint()

#----------------------------------------------------------------------------------------------------------------profile code
# method 2
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
# with PyCallGraph(output=GraphvizOutput()):
#     from mdl import plot, processing, raw, redcap
#     import mdl.model as model
#     import mdl.settings as settings

# method 2
#profiling run.py

# method 3
#%load_ext line_profiler

# method 34 -- use within jupyter
# import os
# file = os.getcwd() + '/run.py'
# %load_ext snakeviz
# %snakeviz prun(file)
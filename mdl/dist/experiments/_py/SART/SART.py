#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

#logging
import logging as errorlog
import os  # handy system and path functions
from subprocess import check_output

#set up logging to file
errorlog.basicConfig(
    filename='error.log', 
    filemode='w', 
    level=errorlog.WARNING, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logger=errorlog.getLogger(__name__)

import platform
import _winreg
def get_registry_value(key, subkey, value):
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value
    
def cpu():
    try:
        cputype = get_registry_value(
            "HKEY_LOCAL_MACHINE", 
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")
    except:
        import wmi, pythoncom
        pythoncom.CoInitialize() 
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cputype = i.Name
        pythoncom.CoUninitialize()
 
    if cputype == 'AMD Athlon(tm)':
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %.2f Ghz' % (cpuspeed / 1000.0)
    elif cputype == 'AMD Athlon(tm) Processor':
        import wmi
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %s' % cpuspeed
    else:
        pass
    return cputype
    
log_system = platform.system() +" " + platform.win32_ver()[0]#windows 7
log_cpu = cpu() #cpu
#log_video = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
log_video = check_output("wmic path win32_VideoController get VideoProcessor")
log_video = (' '.join(log_video.split())).replace("VideoProcessor ","")

errorlog.error(log_system)
errorlog.error(log_cpu)
errorlog.error(log_video)

#--------------------------------------------------------------------------------------------------testing begin
import datetime
import pyglet
pyglet.options['shadow_window'] = False
    
#--------------------------------------------------------------------------------------------------testing end

#--------------------------------------------------------------------------------------------------begin logging
from psychopy import gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED)
import numpy as np  # whole numpy lib is available, prepend 'np.'
import sys  # to get file system encoding

#generating csv files
import csv
import itertools

while True:
    try:
        # Ensure that relative paths start from the same directory as this script
        _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
        os.chdir(_thisDir)
        
        # Store info about the experiment session
        expName = u'SART'  # from the Builder filename that created this script
        expInfo = {u'session': u'001', u'participant': u'000001'}
        dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
        if dlg.OK == False:
            core.quit()  # user pressed cancel
        
        ## check if subject exists
        ## -a if csv is of entire task, -0..-1..-2..-3 if set-0, set-1, etc.
        expInfo['participant'] = str(int(expInfo['participant'])).zfill(6)
        print (expInfo['participant'])
        filename = _thisDir + os.sep + 'data/%s_%s-a' %(expInfo['participant'],expInfo['session'])
        print (filename)
        while True:
            print(filename+".csv")
            if os.path.isfile(filename+".csv"):
                print('file exists')
                dlg = gui.DlgFromDict(dictionary=expInfo, title='file exists, try another subject/session number')
                expInfo['participant'] = str(int(expInfo['participant'])).zfill(6)
                filename = _thisDir + os.sep + 'data/%s_%s-a' %(expInfo['participant'],expInfo['session'])
                if dlg.OK == False:
                    core.quit()  # user pressed cancel
            else:
                print('new file')
                expInfo['participant'] = str(int(expInfo['participant'])).zfill(6)
                filename = _thisDir + os.sep + 'data/%s_%s-a' %(expInfo['participant'],expInfo['session'])
                break
        expInfo['date'] = data.getDateStr()  # add a simple timestamp
        expInfo['expName'] = expName
        
        
        # An ExperimentHandler isn't essential but helps with data saving
        thisExp = data.ExperimentHandler(name=expName, version='',
            extraInfo=expInfo, runtimeInfo=None,
            originPath=None,
            savePickle=True, saveWideText=True,
            dataFileName=filename)
        logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
        
        endExpNow = False  # flag for 'escape' or other condition => quit the exp
        
        # Start Code - component code to be run before the window creation
        
        # Setup the Window
        win = visual.Window(
            size=[1366, 768], fullscr=True, screen=1,
            allowGUI=False, allowStencil=False,
            monitor=u'Experiment', color=[-0.137,-0.137,-0.137], colorSpace='rgb',
            blendMode='avg', useFBO=False,
            units='norm')
        
        
        # store frame rate of monitor if we can measure it
        expInfo['frameRate'] = win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess
        
        # Initialize components for Routine "Introduction"
        IntroductionClock = core.Clock()
        task_instr_image = visual.ImageStim(
            win=win, name='task_instr_image',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        #preparing csv files for practice block and task
        participant = expInfo['participant']
        session = expInfo['session']
        practice_block = [
        {'nontarget':u'male_neutral_046','target':u'outdoor_046','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'male_neutral_047','target':u'outdoor_047','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'male_neutral_048','target':u'outdoor_048','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'male_neutral_049','target':u'outdoor_049','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'male_neutral_050','target':u'outdoor_050','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'female_neutral_046','target':u'outdoor_051','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'female_neutral_047','target':u'outdoor_052','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'female_neutral_048','target':u'outdoor_053','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'female_neutral_049','target':u'outdoor_054','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"},\
        {'nontarget':u'female_neutral_050','target':u'outdoor_055','targetType':u'outdoor','setNum':-1,'blockNum':-1,"blockType":"outdoor"}]
        
        #preparing set csv files
        setDict = [{'setList': u'procedure\\participant\\%s-%s\\#Set0.csv'%(participant,session)},\
         {'setList': u'procedure\\participant\\%s-%s\\#Set1.csv'%(participant, session)},\
         {'setList': u'procedure\\participant\\%s-%s\\#Set2.csv'%(participant,session)},\
         {'setList': u'procedure\\participant\\%s-%s\\#Set3.csv'%(participant,session)}]
        
        
        #generate csv files#------------------------------------------------------------- 
        #create both target and lure for gender
        gender_0 = ['male','female']
        np.random.shuffle(gender_0)
        gender_a = gender_0[-len(gender_0)]
        gender_b = gender_0[1]
        
        #create both target and lure for scene
        scene_0 = ['indoor','outdoor']
        np.random.shuffle(scene_0)
        scene_a = scene_0[-len(scene_0)]
        scene_b = scene_0[1]
        
        
        #-------------------#neutral-only blocks------------------------------------------
        #running iteration for attended stimuli
        #target and lure
        target_aN = "%s_neutral %s_neutral %s_neutral %s_neutral %s %s %s %s" %(gender_a,gender_b,gender_a,gender_b,scene_a,scene_b,scene_a,scene_b)
        lure_aN = "%s_neutral %s_neutral %s_neutral %s_neutral %s %s %s %s" %(gender_b,gender_a,gender_b,gender_a,scene_b,scene_a,scene_b,scene_a)
        target_aN = target_aN.split() #creating list
        lure_aN = lure_aN.split() #combining lists
        block_attendedN = zip(target_aN,lure_aN) #combining lists
        
        #running iteration for attended stimuli
        target_uN = "%s %s %s %s %s_neutral %s_neutral %s_neutral %s_neutral" %(scene_a,scene_a,scene_b,scene_b,gender_a,gender_a,gender_b,gender_b)
        lure_uN = "%s %s %s %s %s_neutral %s_neutral %s_neutral %s_neutral" %(scene_b,scene_b,scene_a,scene_b,gender_b,gender_b,gender_a,gender_a)
        target_uN = target_uN.split() #creating lists
        lure_uN = lure_uN.split() #creating lists
        block_unattendedN = zip(target_uN,lure_uN) #combining lists
        
        #generating list of blocks
        ##combining attended and unattended lists
        attended_unattended_blockN = zip(block_attendedN, block_unattendedN)
        
        
        #-------------------#neutral-sad blocks------------------------------------------
        #running iteration for attended stimuli
        #target and lure
        target_aNS = "%s_sad %s_sad %s_neutral %s_neutral %s %s %s %s" %(gender_a,gender_b,gender_a,gender_b,scene_a,scene_b,scene_a,scene_b)
        lure_aNS = "%s_sad %s_sad %s_neutral %s_neutral %s %s %s %s" %(gender_b,gender_a,gender_b,gender_a,scene_b,scene_a,scene_b,scene_a)
        target_aNS = target_aNS.split() #creating list
        lure_aNS = lure_aNS.split() #combining lists
        block_attendedNS = zip(target_aNS,lure_aNS) #combining lists
        
        #running iteration for attended stimuli
        target_uNS = "%s %s %s %s %s_sad %s_sad %s_neutral %s_neutral" %(scene_a,scene_a,scene_b,scene_b,gender_a,gender_a,gender_b,gender_b)
        lure_uNS = "%s %s %s %s %s_sad %s_sad %s_neutral %s_neutral" %(scene_b,scene_b,scene_a,scene_b,gender_b,gender_b,gender_a,gender_a)
        target_uNS = target_uNS.split() #creating lists
        lure_uNS = lure_uNS.split() #creating lists
        block_unattendedNS = zip(target_uNS,lure_uNS) #combining lists
        
        #generating list of blocks
        ##combining attended and unattended lists
        attended_unattended_blockNS = zip(block_attendedNS,block_unattendedNS)
        
        #task order
        ltaskOrder = [] #order of each subblock within a block
        ltaskType = [] #whether block will include combination of neutral and sad stimuli or just neutral
        for k in range(0,4):
            ltaskOrder_ = range(0,8)
            np.random.shuffle(ltaskOrder_)
            ltaskOrder.append(ltaskOrder_)
            ltaskType_ = ['neutral','neutral','sad','sad']
            np.random.shuffle(ltaskType_)
            ltaskType.append(ltaskType_)
        
        #generating list of random sets
        rand4 = range(0,4)
        np.random.shuffle(rand4)
        a_length = 30 #block length
        aT_length = int(a_length*.9) #attended target length
        aL_length = int(a_length*.1) #attended lure length
        u_length = int(a_length*.5) #unintended length (target & lure)
        #generating neutral blocks
        for j in range(0,2):
            rand8 = range(0,8)
            np.random.shuffle(rand8)
            #preparing blocks
            for k in range(0,8):
                #pulling first item from target_nontarget list
                t_nt = attended_unattended_blockN[rand8[k]]
            
                #stripping target, nontarget data from each block
                t_ = [i[0] for i in t_nt]
                _nt = [i[1] for i in t_nt]
            
                #-------------------#attended target------------------------------------------
                #list of targets and non-targets, as well as lures for each target (t_list)
                target_comp = [t_[0]]
                aT_list = list(range(1,46))
                formatter = '{0:03d}'.format
                aT_list = map(formatter, aT_list)#leading zeros
                np.random.shuffle(aT_list)
                aT_list = aT_list[:aT_length]#first 90% items
                aT_list = ['{}_{}'.format(a, b) for b in aT_list for a in target_comp] #list comprehension
            
                #-------------------#attended lure------------------------------------------
                lure_comp = [_nt[0]]
                aL_list = list(range(1,46))
                aL_list = map(formatter, aL_list)#leading zeros
                np.random.shuffle(aL_list)
                aL_list = aL_list[:aL_length]#first 10% items
                aL_list = ['{}_{}'.format(a, b) for b in aL_list for a in lure_comp] #list comprehension
            
                #combining attended target and lure
                attended = aT_list + aL_list #combining lists
                np.random.shuffle(attended)

                #-------------------#targetType------------------------------------------
                targetType_ = [z.split('_', 1)[0] for z in attended]
                
                #-------------------#unattended target------------------------------------------
                ##list of nontargets and non-nontargets, as well as lures for each nontarget (n_list)
                nontarget_comp = [t_[1]]
                uT_list = list(range(1,46))
                formatter = '{0:03d}'.format
                uT_list = map(formatter, uT_list)#leading zeros
                np.random.shuffle(uT_list)
                uT_list = uT_list[:u_length]#first 15 items
                uT_list = ['{}_{}'.format(a, b) for b in uT_list for a in nontarget_comp] #list comprehension
            
                #-------------------#unattended lure------------------------------------------
                #nontarget_lure (nl_list)
                lure_comp = [_nt[1]]
                uL_list = list(range(1,46))
                formatter = '{0:03d}'.format
                uL_list = map(formatter, uL_list)#leading zeros
                np.random.shuffle(uL_list)
                uL_list = uL_list[:u_length]#first 15 items
                uL_list = ['{}_{}'.format(a, b) for b in uL_list for a in lure_comp] #list comprehension
            
                #combining unattended target and lure
                unattended = uT_list + uL_list #combining lists
                np.random.shuffle(unattended)
            
               #-------------------#create iterated list------------------------------------------ 
                t_ = t_[0] #first value of tuple pair
                t_block = t_.split('_', 1)[0]
        
                #saving to csv
                #file variable
                if not os.path.exists("procedure\participant\%s-%s"%(participant,session)):
                    os.makedirs("procedure\participant\%s-%s"%(participant, session))
                
                #block name
                f_name = 'procedure\participant\%s-%s\\n%s_%s.csv'%(participant,session,rand8[k],t_)
        
                #outputting set_list procedure
                with open('procedure\participant\%s-%s\#Set%s.csv'%(participant,session,rand4[j]), 'a') as set_list:
                    writer = csv.writer(set_list,lineterminator='\n')
                    if k==0:
                        header=["setNum","blockType","target","blockList"]
                        writer.writerow(header)
                    writer.writerow([rand4[j],t_block,t_,f_name])
            
                #outputting block procedure
                with open(f_name, 'wb') as target_sch:
                    writer = csv.writer(target_sch)
                    header=["target","nontarget","targetType"]
                    writer.writerow(header)
                    for row,row1,row2 in itertools.izip(attended,unattended,targetType_):
                        writer.writerow([row,row1,row2])  
        
        #generating emotional blocks
        for j in range(2,4):
            #generate random blocks
            rand8 = range(0,8)
            np.random.shuffle(rand8)
            #preparing blocks
            for k in range(0,8):
                #pulling first item from target_nontarget list
                #t_nt = target_nontarget1[-len(target_nontarget1)]
                t_nt = attended_unattended_blockNS[rand8[k]]
            
                #stripping target, nontarget data from each block
                t_ = [i[0] for i in t_nt]
                _nt = [i[1] for i in t_nt]
            
                #-------------------#attended target------------------------------------------
                #list of targets and non-targets, as well as lures for each target (t_list)
                target_comp = [t_[0]]
                aT_list = list(range(1,46))
                formatter = '{0:03d}'.format
                aT_list = map(formatter, aT_list)#leading zeros
                np.random.shuffle(aT_list)
                aT_list = aT_list[:aT_length]#first 90% items
                aT_list = ['{}_{}'.format(a, b) for b in aT_list for a in target_comp] #list comprehension
            
                #-------------------#attended lure------------------------------------------
                lure_comp = [_nt[0]]
                aL_list = list(range(1,46))
                aL_list = map(formatter, aL_list)#leading zeros
                np.random.shuffle(aL_list)
                aL_list = aL_list[:aL_length]#first 10% items
                aL_list = ['{}_{}'.format(a, b) for b in aL_list for a in lure_comp] #list comprehension
            
                #combining attended target and lure
                attended = aT_list + aL_list #combining lists
                np.random.shuffle(attended)

                #-------------------#targetType------------------------------------------
                targetType_ = [z.split('_', 1)[0] for z in attended]
                
                #-------------------#unattended target------------------------------------------
                ##list of nontargets and non-nontargets, as well as lures for each nontarget (n_list)
                nontarget_comp = [t_[1]]
                uT_list = list(range(1,46))
                formatter = '{0:03d}'.format
                uT_list = map(formatter, uT_list)#leading zeros
                np.random.shuffle(uT_list)
                uT_list = uT_list[:u_length]#first 15 items
                uT_list = ['{}_{}'.format(a, b) for b in uT_list for a in nontarget_comp] #list comprehension
            
                #-------------------#unattended lure------------------------------------------
                #nontarget_lure (nl_list)
                lure_comp = [_nt[1]]
                uL_list = list(range(1,46))
                formatter = '{0:03d}'.format
                uL_list = map(formatter, uL_list)#leading zeros
                np.random.shuffle(uL_list)
                uL_list = uL_list[:u_length]#first 15 items
                uL_list = ['{}_{}'.format(a, b) for b in uL_list for a in lure_comp] #list comprehension
            
                #combining unattended target and lure
                unattended = uT_list + uL_list #combining lists
                np.random.shuffle(unattended)
            
               #-------------------#create iterated list------------------------------------------ 
                t_ = t_[0] #first value of tuple pair
                t_block = t_.split('_', 1)[0]
                
                #saving to csv
                #file variable
                if not os.path.exists("procedure\participant\%s-%s"%(participant,session)):
                    os.makedirs("procedure\participant\%s-%s"%(participant,session))
                 
                #block name
                f_name = 'procedure\participant\%s-%s\s%s_%s.csv'%(participant,session,rand8[k],t_)
            
                #outputting set_list procedure
                with open('procedure\participant\%s-%s\#Set%s.csv'%(participant,session, rand4[j]), 'a') as set_list:
                    writer = csv.writer(set_list,lineterminator='\n')
                    if k==0:
                        header=["setNum","blockType","target","blockList"]
                        writer.writerow(header)
                    writer.writerow([rand4[j],t_block,t_,f_name])
                    
                #outputting block procedure
                with open(f_name, 'wb') as target_sch:
                    writer = csv.writer(target_sch)
                    header=["target","nontarget","targetType"]
                    writer.writerow(header)
                    for row,row1,row2 in itertools.izip(attended,unattended,targetType_):
                        writer.writerow([row,row1,row2])
                        
        #------------------------------------------------------------- 
        del attended_unattended_blockN, attended_unattended_blockNS, b, block_attendedN, block_attendedNS,\
        block_unattendedN, block_unattendedNS, formatter, gender_0, gender_a, gender_b,\
        ltaskOrder_, ltaskType_, lure_aN, lure_aNS, lure_comp, lure_uN, lure_uNS,\
        nontarget_comp, scene_0, scene_a, scene_b, t_, t_block, t_nt, target_aN,\
        target_aNS, target_comp, target_uN, target_uNS, a, i, j, k, attended, unattended, uL_list, uT_list, aT_list, aL_list,z,targetType_,\
        rand4, rand8, row, row1
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #------------------------------------------------------------- 
        #-------------------------------------------------------------
        
        # Initialize components for Routine "Practice_Instructions"
        Practice_InstructionsClock = core.Clock()
        Practice_instructions = visual.ImageStim(
            win=win, name='Practice_instructions',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Initialize components for Routine "Fixation"
        FixationClock = core.Clock()
        fixation_image = visual.ImageStim(
            win=win, name='fixation_image',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Initialize components for Routine "Stimuli"
        StimuliClock = core.Clock()
        stim_display = visual.ImageStim(
            win=win, name='stim_display',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-2.0)
        #resize stim_display
        print("stim units: " + str(stim_display.units))
        stim_display.units = "pix"
        print("stim size: " +str(stim_display.size))
        stim_display.size = 600
        print("new stim size: " + str(stim_display.size))
        print("stim units: " + str(stim_display.units))
                        
        # Initialize components for Routine "Task_Instructions"
        Task_InstructionsClock = core.Clock()
        Practice_instructions_2 = visual.ImageStim(
            win=win, name='Practice_instructions_2',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Initialize components for Routine "waitMRI"
        waitMRIClock = core.Clock()
        mri_display = visual.ImageStim(
            win=win, name='mri_display',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Initialize components for Routine "MRI_Fixation"
        MRI_FixationClock = core.Clock()
        fixation_image_2 = visual.ImageStim(
            win=win, name='fixation_image_2',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Initialize components for Routine "Block_Instructions"
        Block_InstructionsClock = core.Clock()
        Block_instr_image = visual.ImageStim(
            win=win, name='Block_instr_image',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Initialize components for Routine "Break"
        BreakNum = 0 #counter to skip break
        BreakRep = 1 #value to allow breakLoop to either continue (1) or get skipped (0)
        BreakClock = core.Clock()
        break_display = visual.ImageStim(
            win=win, name='break_display',
            image="Instructions/Break.png", mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-1.0)
        
        # Initialize components for Routine "Finish"
        FinishClock = core.Clock()
        End_Screen = visual.ImageStim(
            win=win, name='End_Screen',
            image="Instructions/Finished.png", mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        
        # Create some handy timers
        globalClock = core.Clock()  # to track the time since experiment started
        routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
        
        #block clock
        blockClock = core.Clock()  # to track the time since block started#--------------------------------------------------------------------------------------------------------------------------------------------------
        
        # set up handler to look after randomisation of conditions etc
        slide = [{'Introduction_image': u'Introduction_1.png'}, {'Introduction_image': u'Introduction_2.png'},{'Introduction_image': u'Introduction_3.png'}]
        Introduction_Loop = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=slide,
            seed=None, name='Block_loop')
        thisExp.addLoop(Introduction_Loop)  # add the loop to the experiment
        thisIntroduction_Loop = Introduction_Loop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisIntroduction_Loop.rgb)
        if thisIntroduction_Loop != None:
            for paramName in thisIntroduction_Loop.keys():
                exec(paramName + '= thisIntroduction_Loop.' + paramName)
        
        for thisIntroduction_Loop in Introduction_Loop:
            currentLoop = Introduction_Loop
            # abbreviate parameter names if possible (e.g. rgb = thisIntroduction_Loop.rgb)
            if thisIntroduction_Loop != None:
                for paramName in thisIntroduction_Loop.keys():
                    exec(paramName + '= thisIntroduction_Loop.' + paramName)
            
            
            # ------Prepare to start Routine "Introduction"-------
            t = 0
            IntroductionClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            task_instr_image.setImage("Instructions/%s"%(Introduction_image))
            Inst__Key = event.BuilderKeyResponse()
            
            # keep track of which components have finished
            IntroductionComponents = [task_instr_image, Inst__Key]
            for thisComponent in IntroductionComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "Introduction"-------
            while continueRoutine:
                # get current time
                t = IntroductionClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *task_instr_image* updates
                if t >= 0.0 and task_instr_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    task_instr_image.tStart = t
                    task_instr_image.frameNStart = frameN  # exact frame index
                    task_instr_image.setAutoDraw(True)
                
                # *Inst__Key* updates
                if t >= 0.0 and Inst__Key.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Inst__Key.tStart = t
                    Inst__Key.frameNStart = frameN  # exact frame index
                    Inst__Key.status = STARTED
                    # keyboard checking is just starting
                    event.clearEvents(eventType='keyboard')
                if Inst__Key.status == STARTED:
                    theseKeys = event.getKeys(keyList=['1'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        # a response ends the routine
                        continueRoutine = False
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in IntroductionComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Introduction"-------
            for thisComponent in IntroductionComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            # the Routine "Introduction" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
        # completed 1 repeats of 'Introduction_Loop'
 
        # ------Prepare to start Routine "Practice_Instructions"-------
        t = 0
        Practice_InstructionsClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        Practice_instructions.setImage("Instructions/practice_start.png")
        Prac__key = event.BuilderKeyResponse()
        # keep track of which components have finished
        Practice_InstructionsComponents = [Practice_instructions, Prac__key]
        for thisComponent in Practice_InstructionsComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "Practice_Instructions"-------
        while continueRoutine:
            # get current time
            t = Practice_InstructionsClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Practice_instructions* updates
            if t >= 0.0 and Practice_instructions.status == NOT_STARTED:
                # keep track of start time/frame for later
                Practice_instructions.tStart = t
                Practice_instructions.frameNStart = frameN  # exact frame index
                Practice_instructions.setAutoDraw(True)
            
            # *Prac__key* updates
            if t >= 0.0 and Prac__key.status == NOT_STARTED:
                # keep track of start time/frame for later
                Prac__key.tStart = t
                Prac__key.frameNStart = frameN  # exact frame index
                Prac__key.status = STARTED
                # keyboard checking is just starting
                event.clearEvents(eventType='keyboard')
            if Prac__key.status == STARTED:
                theseKeys = event.getKeys(keyList=['1'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Practice_InstructionsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Practice_Instructions"-------
        for thisComponent in Practice_InstructionsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "Practice_Instructions" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # ------Prepare to start Routine "Block_Instructions"-------
        t = 0
        Block_InstructionsClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        Block_instr_image.setImage("Instructions/outdoor.png")
        Practice_image = "outdoor.png"
        # keep track of which components have finished
        Block_InstructionsComponents = [Block_instr_image]
        for thisComponent in Block_InstructionsComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "Block_Instructions"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Block_InstructionsClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Block_instr_image* updates
            if t >= 0.0 and Block_instr_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                Block_instr_image.tStart = t
                Block_instr_image.frameNStart = frameN  # exact frame index
                Block_instr_image.setAutoDraw(True)
            frameRemains = 0.0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
            if Block_instr_image.status == STARTED and t >= frameRemains:
                Block_instr_image.setAutoDraw(False)
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Block_InstructionsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Block_Instructions"-------
        for thisComponent in Block_InstructionsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False) 

        
        # ------Prepare to start Routine "Fixation"-------
        t = 0
        FixationClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        fixation_image.setImage("Instructions/Fixation.png")
        # keep track of which components have finished
        FixationComponents = [fixation_image]
        for thisComponent in FixationComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "Fixation"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = FixationClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation_image* updates
            if t >= 0.0 and fixation_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                fixation_image.tStart = t
                fixation_image.frameNStart = frameN  # exact frame index
                fixation_image.setAutoDraw(True)
            frameRemains = 0.0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
            if fixation_image.status == STARTED and t >= frameRemains:
                fixation_image.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FixationComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Fixation"-------
        for thisComponent in FixationComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # set up handler to look after randomisation of conditions etc
        Practice_loop = data.TrialHandler(nReps=1, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=practice_block,
            seed=None, name='Block_loop')
        thisExp.addLoop(Practice_loop)  # add the loop to the experiment
        thisPractice_loop = Practice_loop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
        if thisPractice_loop != None:
            for paramName in thisPractice_loop.keys():
                exec(paramName + '= thisPractice_loop.' + paramName)
        
        blockClock.reset()#------------------------------------------------------------------------------------------------------------------------------------------------------------
        trialNum = 0
        for thisPractice_loop in Practice_loop:
            currentLoop = Practice_loop
            # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
            if thisPractice_loop != None:
                for paramName in thisPractice_loop.keys():
                    exec(paramName + '= thisPractice_loop.' + paramName)
            
            # ------Prepare to start Routine "Stimuli"-------
            t = 0
            StimuliClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(2.000000)
            # update component parameters for each repeat
            #preparing image name ----------6/8/2017 SMR
            #if target is faces
            if Practice_image == "female.png" or Practice_image == "male.png":
                image_name = "stimuli/%s_%s.png"%(target,nontarget)
            #else target is scenes
            else:
                image_name = "stimuli/%s_%s.png"%(nontarget,target)        
            print("target: "+target)
            print("nontarget: "+nontarget)
            print("image: "+image_name)
            print("trialNum: "+str(trialNum))
            print("setNum: -1")
            currentTime = blockClock.getTime()#------------------------------------------------------------------------------------------------------------------------------------------------------------
            # print("currentTime: "+str(currentTime))
            stimuli_key = event.BuilderKeyResponse()
            stim_display.setImage(image_name)
            # keep track of which components have finished
            StimuliComponents = [stimuli_key, stim_display]
            for thisComponent in StimuliComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "Stimuli"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = StimuliClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                
                # *stimuli_key* updates
                if t >= 0 and stimuli_key.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimuli_key.tStart = t
                    stimuli_key.frameNStart = frameN  # exact frame index
                    stimuli_key.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(stimuli_key.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                frameRemains = 0 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimuli_key.status == STARTED and t >= frameRemains:
                    stimuli_key.status = STOPPED
                if stimuli_key.status == STARTED:
                    theseKeys = event.getKeys(keyList=['1'])
                    # semeon update resp--------------------------------------------------------------------
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    # if key was pressed
                    if (len(theseKeys) > 0):  # at least one key was pressed
                        if stimuli_key.keys == []:  # get first keypress
                            stimuli_key.keys = theseKeys[0]  # only first keypress
                            stimuli_key.rt = stimuli_key.clock.getTime()
                            # if cued catergory 
                            if (blockType == targetType) or (str(blockType) == str(targetType)):
                                stimuli_key.corr = 1
                            else:
                                stimuli_key.corr = 0
                        
                # semeon update resp--------------------------------------------------------------------
                # *stim_display* updates
                if t >= 0.0 and stim_display.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stim_display.tStart = t
                    stim_display.frameNStart = frameN  # exact frame index
                    stim_display.setAutoDraw(True)
                frameRemains = 0.0 + 2.0- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stim_display.status == STARTED and t >= frameRemains:
                    stim_display.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in StimuliComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Stimuli"-------
            for thisComponent in StimuliComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            # check responses
            if stimuli_key.keys in ['', [], None]:  # No response was made
                stimuli_key.keys=None
                # was no response the correct answer?!
                if (blockType != targetType) or (str(blockType) != str(targetType)):
                   stimuli_key.corr = 1  # correct non-response
                else:
                   stimuli_key.corr = 0  # failed to respond (incorrectly)
                   
                   
            # store data for Practice_loop (TrialHandler)
            Practice_loop.addData('stimuli_key.keys',stimuli_key.keys)
            Practice_loop.addData('stimuli_key.corr', stimuli_key.corr)
            Practice_loop.addData('trialNum', trialNum)
            Practice_loop.addData('trial.t',currentTime)#------------------------------------------------------------------------------------------------------------------------------------------------------------
            trialNum = trialNum + 1
            print('###############################')
            print('target: '+str(target))
            print('blockType: '+str(blockType))
            print('targetType: '+str(targetType))
            print('isTargetBlock: '+str(blockType == targetType))
            print('stimuli_key.keys: '+str(stimuli_key.keys))
            print('stimuli_key.corr: '+str(stimuli_key.corr))
            print('###############################')
            if stimuli_key.keys != None:  # we had a response
                Practice_loop.addData('stimuli_key.rt', stimuli_key.rt)
            thisExp.nextEntry()
        
        # completed 1 repeats of 'Practice_loop'
        
        # ------Prepare to start Routine "Task_Instructions"-------
        t = 0
        Task_InstructionsClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        Practice_instructions_2.setImage("Instructions/practice_end.png")
        Prac__key_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        Task_InstructionsComponents = [Practice_instructions_2, Prac__key_2]
        for thisComponent in Task_InstructionsComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "Task_Instructions"-------
        while continueRoutine:
            # get current time
            t = Task_InstructionsClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Practice_instructions_2* updates
            if t >= 0.0 and Practice_instructions_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                Practice_instructions_2.tStart = t
                Practice_instructions_2.frameNStart = frameN  # exact frame index
                Practice_instructions_2.setAutoDraw(True)
            
            # *Prac__key_2* updates
            if t >= 0.0 and Prac__key_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                Prac__key_2.tStart = t
                Prac__key_2.frameNStart = frameN  # exact frame index
                Prac__key_2.status = STARTED
                # keyboard checking is just starting
                event.clearEvents(eventType='keyboard')
            if Prac__key_2.status == STARTED:
                theseKeys = event.getKeys(keyList=['1'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Task_InstructionsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Task_Instructions"-------
        for thisComponent in Task_InstructionsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "Task_Instructions" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        Set_loop = data.TrialHandler(nReps=1, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=setDict,
            seed=None, name='Block_loop')
        thisExp.addLoop(Set_loop)  # add the loop to the experiment
        thisSet_loop = Set_loop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSet_loop.rgb)
        if thisSet_loop != None:
            for paramName in thisSet_loop.keys():
                exec(paramName + '= thisSet_loop.' + paramName)
        
        for thisSet_loop in Set_loop:
            currentLoop = Set_loop
            blockNum = 0
            # abbreviate parameter names if possible (e.g. rgb = thisSet_loop.rgb)
            if thisSet_loop != None:
                for paramName in thisSet_loop.keys():
                    exec(paramName + '= thisSet_loop.' + paramName)
            
            # ------Prepare to start Routine "waitMRI"-------
            t = 0
            waitMRIClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            mri_display.setImage("instructions/wait.png")
            key_resp_mri = event.BuilderKeyResponse()
            # keep track of which components have finished
            waitMRIComponents = [mri_display, key_resp_mri]
            for thisComponent in waitMRIComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "waitMRI"-------
            while continueRoutine:
                # get current time
                t = waitMRIClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *mri_display* updates
                if t >= 0.0 and mri_display.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    mri_display.tStart = t
                    mri_display.frameNStart = frameN  # exact frame index
                    mri_display.setAutoDraw(True)
                
                # *key_resp_mri* updates
                if t >= 0.0 and key_resp_mri.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_mri.tStart = t
                    key_resp_mri.frameNStart = frameN  # exact frame index
                    key_resp_mri.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_mri.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if key_resp_mri.status == STARTED:
                    theseKeys = event.getKeys(keyList=['5'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        key_resp_mri.keys = theseKeys[-1]  # just the last key pressed
                        key_resp_mri.rt = key_resp_mri.clock.getTime()
                        # a response ends the routine
                        continueRoutine = False
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in waitMRIComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "waitMRI"-------
            for thisComponent in waitMRIComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp_mri.keys in ['', [], None]:  # No response was made
                key_resp_mri.keys=None
            Set_loop.addData('key_resp_mri.keys',key_resp_mri.keys)
            if key_resp_mri.keys != None:  # we had a response
                Set_loop.addData('key_resp_mri.rt', key_resp_mri.rt)
            # the Routine "waitMRI" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()    
            
            # ------Prepare to start Routine "MRI_Fixation"-------
            print('setList: '+setList)
            #reset blockClock time
            blockClock.reset()#------------------------------------------------------------------------------------------------------------------------------------------------------------
            t = 0
            MRI_FixationClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            MRI_FixationTime = 2
            routineTimer.add(MRI_FixationTime)
            # update component parameters for each repeat
            fixation_image_2.setImage("Instructions/Fixation.png")
            #--------------------send mri trigger
            # keep track of which components have finished
            MRI_FixationComponents = [fixation_image_2]
            for thisComponent in MRI_FixationComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "MRI_Fixation"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = MRI_FixationClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *fixation_image_2* updates
                if t >= 0.0 and fixation_image_2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    fixation_image_2.tStart = t
                    fixation_image_2.frameNStart = frameN  # exact frame index
                    fixation_image_2.setAutoDraw(True)
                frameRemains = 0.0 + MRI_FixationTime- win.monitorFramePeriod * 0.75  # most of one frame period left
                if fixation_image_2.status == STARTED and t >= frameRemains:
                    fixation_image_2.setAutoDraw(False)
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in MRI_FixationComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "MRI_Fixation"-------
            for thisComponent in MRI_FixationComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            print('#------set start--------')
            debug_SetStart = datetime.datetime.now()
            print('set start time')
            print(debug_SetStart.isoformat())
            
            # set up handler to look after randomisation of conditions etc
            Block_loop = data.TrialHandler(nReps=1, method='sequential', 
                extraInfo=expInfo, originPath=-1,
                trialList=data.importConditions(setList),
                seed=None, name='Block_loop')
            thisExp.addLoop(Block_loop)  # add the loop to the experiment
            thisBlock_loop = Block_loop.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisBlock_loop.rgb)
            if thisBlock_loop != None:
                for paramName in thisBlock_loop.keys():
                    exec(paramName + '= thisBlock_loop.' + paramName)
            
            for thisBlock_loop in Block_loop:
                currentLoop = Block_loop
                # abbreviate parameter names if possible (e.g. rgb = thisBlock_loop.rgb)
                if thisBlock_loop != None:
                    for paramName in thisBlock_loop.keys():
                        exec(paramName + '= thisBlock_loop.' + paramName)
                
                # ------Prepare to start Routine "Block_Instructions"-------
                t = 0
                Block_InstructionsClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                routineTimer.add(1.000000)
                # update component parameters for each repeat

                print('#------block start--------')
                debug_BlockStart = datetime.datetime.now()
                print('block start time')
                print(debug_BlockStart.isoformat())
                print("block: "+blockType)
                Block_instr_image.setImage("Instructions/"+blockType+".png")
                # keep track of which components have finished
                Block_InstructionsComponents = [Block_instr_image]
                for thisComponent in Block_InstructionsComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "Block_Instructions"-------
                while continueRoutine and routineTimer.getTime() > 0:
                    # get current time
                    t = Block_InstructionsClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # *Block_instr_image* updates
                    if t >= 0.0 and Block_instr_image.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Block_instr_image.tStart = t
                        Block_instr_image.frameNStart = frameN  # exact frame index
                        Block_instr_image.setAutoDraw(True)
                    frameRemains = 0.0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Block_instr_image.status == STARTED and t >= frameRemains:
                        Block_instr_image.setAutoDraw(False)
                    
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in Block_InstructionsComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "Block_Instructions"-------
                for thisComponent in Block_InstructionsComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                
                
                # ------Prepare to start Routine "Fixation"-------
                t = 0
                FixationClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                routineTimer.add(1.000000)
                # update component parameters for each repeat
                fixation_image.setImage("Instructions/Fixation.png")
                # keep track of which components have finished
                FixationComponents = [fixation_image]
                for thisComponent in FixationComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "Fixation"-------
                while continueRoutine and routineTimer.getTime() > 0:
                    # get current time
                    t = FixationClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # *fixation_image* updates
                    if t >= 0.0 and fixation_image.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        fixation_image.tStart = t
                        fixation_image.frameNStart = frameN  # exact frame index
                        fixation_image.setAutoDraw(True)
                    frameRemains = 0.0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if fixation_image.status == STARTED and t >= frameRemains:
                        fixation_image.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in FixationComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "Fixation"-------
                for thisComponent in FixationComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                
                # set up handler to look after randomisation of conditions etc
                Trial_Loop = data.TrialHandler(nReps=1, method='random', 
                    extraInfo=expInfo, originPath=-1,
                    trialList=data.importConditions(blockList),
                    seed=None, name='Block_loop')
                thisExp.addLoop(Trial_Loop)  # add the loop to the experiment
                thisTrial_Loop = Trial_Loop.trialList[0]  # so we can initialise stimuli with some values
                trialNum = 0
                # abbreviate parameter names if possible (e.g. rgb = thisTrial_Loop.rgb)
                if thisTrial_Loop != None:
                    for paramName in thisTrial_Loop.keys():
                        exec(paramName + '= thisTrial_Loop.' + paramName)
                
                for thisTrial_Loop in Trial_Loop:
                    currentLoop = Trial_Loop
                    # abbreviate parameter names if possible (e.g. rgb = thisTrial_Loop.rgb)
                    if thisTrial_Loop != None:
                        for paramName in thisTrial_Loop.keys():
                            exec(paramName + '= thisTrial_Loop.' + paramName)

                    print('#------trial start--------')
                    debug_TrialStart = datetime.datetime.now()
                    print('trial start time')
                    print(debug_TrialStart.isoformat())

                    # ------Prepare to start Routine "Stimuli"-------
                    t = 0
                    StimuliClock.reset()  # clock
                    frameN = -1
                    continueRoutine = True
                    routineTimer.add(2.000000)
                    # update component parameters for each repeat
                    #preparing image name ----------6/8/2017 SMR
                    #if target is faces
                    print("blockType: %s"%(blockType))
                    if blockType == "female" or blockType == "male":
                        image_name = "stimuli/%s_%s.png"%(target,nontarget)
                    #else target is scenes
                    else:
                        image_name = "stimuli/%s_%s.png"%(nontarget,target)
                    
                    print("trialNum: "+str(trialNum))
                    print("blockNum: "+str(blockNum))
                    print("setNum: "+str(BreakNum))
                    currentTime = blockClock.getTime()
                    #print("currentTime: "+str(currentTime))
                    stimuli_key = event.BuilderKeyResponse()
                    stim_display.setImage(image_name)
                    # keep track of which components have finished
                    StimuliComponents = [stimuli_key, stim_display]
                    for thisComponent in StimuliComponents:
                        if hasattr(thisComponent, 'status'):
                            thisComponent.status = NOT_STARTED
                    
                    # -------Start Routine "Stimuli"-------
                    print('time: '+str(StimuliClock.getTime()))
                    while continueRoutine and routineTimer.getTime() > 0:
                        # get current time
                        t = StimuliClock.getTime()
                        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                        # update/draw components on each frame
                        
                        # *stimuli_key* updates
                        if t >= 0 and stimuli_key.status == NOT_STARTED:
                            # keep track of start time/frame for later
                            stimuli_key.tStart = t
                            stimuli_key.frameNStart = frameN  # exact frame index
                            stimuli_key.status = STARTED
                            # keyboard checking is just starting
                            win.callOnFlip(stimuli_key.clock.reset)  # t=0 on next screen flip
                            event.clearEvents(eventType='keyboard')
                        frameRemains = 0 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
                        if stimuli_key.status == STARTED and t >= frameRemains:
                            stimuli_key.status = STOPPED
                        if stimuli_key.status == STARTED:
                            theseKeys = event.getKeys(keyList=['1'])
                            # semeon update resp--------------------------------------------------------------------
                            # check for quit:
                            if "escape" in theseKeys:
                                endExpNow = True
                            # if key was pressed
                            if (len(theseKeys) > 0):  # at least one key was pressed
                                if stimuli_key.keys == []:  # get first keypress
                                    stimuli_key.keys = theseKeys[0]  # only first keypress
                                    stimuli_key.rt = stimuli_key.clock.getTime()
                                    # if cued catergory 
                                    if (blockType == targetType) or (str(blockType) == str(targetType)):
                                        stimuli_key.corr = 1
                                    else:
                                        stimuli_key.corr = 0
                            # semeon update resp--------------------------------------------------------------------
                        # *stim_display* updates
                        if t >= 0.0 and stim_display.status == NOT_STARTED:
                            # keep track of start time/frame for later
                            stim_display.tStart = t
                            stim_display.frameNStart = frameN  # exact frame index
                            stim_display.setAutoDraw(True)
                        frameRemains = 0.0 + 2.0- win.monitorFramePeriod * 0.75  # most of one frame period left
                        if stim_display.status == STARTED and t >= frameRemains:
                            stim_display.setAutoDraw(False)
                        
                        # check if all components have finished
                        if not continueRoutine:  # a component has requested a forced-end of Routine
                            break
                        continueRoutine = False  # will revert to True if at least one component still running
                        for thisComponent in StimuliComponents:
                            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                                continueRoutine = True
                                break  # at least one component has not yet finished
                        
                        # check for quit (the Esc key)
                        if endExpNow or event.getKeys(keyList=["escape"]):
                            core.quit()
                        
                        # refresh the screen
                        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                            win.flip()
                    
                    # -------Ending Routine "Stimuli"-------
                    for thisComponent in StimuliComponents:
                        if hasattr(thisComponent, "setAutoDraw"):
                            thisComponent.setAutoDraw(False)
                    
                    # check responses
                    if stimuli_key.keys in ['', [], None]:  # No response was made
                        stimuli_key.keys=None
                        # was no response the correct answer?!
                        if (blockType != targetType) or (str(blockType) != str(targetType)):
                           stimuli_key.corr = 1  # correct non-response
                        else:
                           stimuli_key.corr = 0  # failed to respond (incorrectly)
                    # store data for Trial_Loop (TrialHandler)
                    Trial_Loop.addData('stimuli_key.keys',stimuli_key.keys)
                    Trial_Loop.addData('stimuli_key.corr', stimuli_key.corr)
                    Trial_Loop.addData('trialNum',trialNum)
                    Trial_Loop.addData('blockNum',blockNum)
                    print('###############################')
                    print('target: '+str(target))
                    print('blockType: '+str(blockType))
                    print('targetType: '+str(targetType))
                    print('isTargetBlock: '+str(blockType == targetType))
                    print('stimuli_key.keys: '+str(stimuli_key.keys))
                    print('stimuli_key.corr: '+str(stimuli_key.corr))
                    print('###############################')
                    trialNum = trialNum+1
                    if stimuli_key.keys != None:  # we had a response
                        Trial_Loop.addData('stimuli_key.rt', stimuli_key.rt)
                    #store timing
                    Trial_Loop.addData('trial.t',currentTime)
                    #semeon debug start - trial
                    debug_TrialEnd = datetime.datetime.now()
                    debug_TrialDiff = (debug_TrialEnd - debug_TrialStart).total_seconds()
                    print('trial end time')
                    print(debug_TrialEnd.isoformat())
                    print('trial time diff')
                    print(debug_TrialDiff)
                    #semeon debug end - trial            
                    thisExp.nextEntry()
                # completed 1 repeats of 'Trial_Loop'
                thisExp.nextEntry()
                blockNum = blockNum+1
                #semeon debug start - block
                debug_BlockEnd = datetime.datetime.now()
                debug_BlockDiff = (debug_BlockEnd - debug_BlockStart).total_seconds()
                print('#------block end--------')
                print('block end time')
                print(debug_BlockEnd.isoformat())
                print('block time diff')
                print(debug_BlockDiff)
                #semeon debug end - block
            # completed 1 repeats of 'Block_loop'
            blockClock.reset()
            #semeon debug start - set
            debug_SetEnd = datetime.datetime.now()
            debug_SetDiff = (debug_SetEnd - debug_SetStart).total_seconds()
            print('#------set end--------')
            print('set end time')
            print(debug_SetEnd.isoformat())
            print("set time diff: " + str(debug_SetDiff))
            print("BreakNum: " + str(BreakNum))
            #semeon debug end - set


            # set up handler to look after randomisation of conditions etc
            Break_loop = data.TrialHandler(nReps=BreakRep, method='random', 
                extraInfo=expInfo, originPath=None,
                trialList=[None],
                seed=None, name='Break_loop')
            thisExp.addLoop(Break_loop)  # add the loop to the experiment
            thisBreak_loop = Break_loop.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisBreak_loop.rgb)
            if thisBreak_loop != None:
                for paramName in thisBreak_loop.keys():
                    exec(paramName + '= thisBreak_loop.' + paramName)
            
            for thisBreak_loop in Break_loop:
                currentLoop = Break_loop
                # abbreviate parameter names if possible (e.g. rgb = thisBreak_loop.rgb)
                if thisBreak_loop != None:
                    for paramName in thisBreak_loop.keys():
                        exec(paramName + '= thisBreak_loop.' + paramName)
                

                # ------Prepare to start Routine "Break"-------
                t = 0
                BreakClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                if BreakNum >= 3:
                    continueRoutine = False
 
                # update component parameters for each repeat
                Break_key = event.BuilderKeyResponse()
                
                # keep track of which components have finished
                BreakComponents = [Break_key, break_display]
                for thisComponent in BreakComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "Break"-------
                while continueRoutine:
                    # get current time
                    t = BreakClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # *Break_key* updates
                    if t >= 0.0 and Break_key.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Break_key.tStart = t
                        Break_key.frameNStart = frameN  # exact frame index
                        Break_key.status = STARTED
                        # keyboard checking is just starting
                        win.callOnFlip(Break_key.clock.reset)  # t=0 on next screen flip
                        event.clearEvents(eventType='keyboard')
                    if Break_key.status == STARTED:
                        theseKeys = event.getKeys(keyList=['1'])
                        
                        # check for quit:
                        if "escape" in theseKeys:
                            endExpNow = True
                        if len(theseKeys) > 0:  # at least one key was pressed
                            Break_key.keys = theseKeys[-1]  # just the last key pressed
                            Break_key.rt = Break_key.clock.getTime()
                            # a response ends the routine
                            continueRoutine = False
                    
                    # *break_display* updates
                    if t >= 0.0 and break_display.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        break_display.tStart = t
                        break_display.frameNStart = frameN  # exact frame index
                        break_display.setAutoDraw(True)
                    
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in BreakComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "Break"-------
                for thisComponent in BreakComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                
            # the Routine "Break" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            #increment counter
            BreakNum = BreakNum + 1            
            # completed 4 repeats of 'Set_loop'
        
        
        # ------Prepare to start Routine "Finish"-------
        t = 0
        FinishClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        # keep track of which components have finished
        FinishComponents = [End_Screen]
        for thisComponent in FinishComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "Finish"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = FinishClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *End_Screen* updates
            if t >= 0.0 and End_Screen.status == NOT_STARTED:
                # keep track of start time/frame for later
                End_Screen.tStart = t
                End_Screen.frameNStart = frameN  # exact frame index
                End_Screen.setAutoDraw(True)
            frameRemains = 0.0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
            if End_Screen.status == STARTED and t >= frameRemains:
                End_Screen.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FinishComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Finish"-------
        for thisComponent in FinishComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        # these shouldn't be strictly necessary (should auto-save)
        thisExp.saveAsWideText(filename+'.csv')
        thisExp.saveAsPickle(filename)
        # make sure everything is closed down
        thisExp.abort()  # or data files will save again on exit
        win.close()
        core.quit()

    #--------------------------------------------------------------------------------------------------end logging
    except Exception as e:
        logger.warning(e, exc_info=True)
        win.close()
        core.quit()
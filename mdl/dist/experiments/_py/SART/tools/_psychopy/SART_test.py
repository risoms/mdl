#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.1),
    on August 16, 2017, at 15:11
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division

import psychopy
psychopy.useVersion('1.85.1')

from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'SART'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s' %(expInfo['participant'],expInfo['session'])

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
    size=[1366, 768], fullscr=False, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='Experiment', color=[1.000,1.000,1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True,
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
#intro block
intro_slide = [{'Introduction_image': u'Introduction_1.png'}, {'Introduction_image': u'Introduction_2.png'},\
 {'Introduction_image': u'Introduction_3.png'}]

#practice block
practice_slide = [{'Practice_image': u'practice_start.png'}, {'Practice_image': u'outdoor.png'}]
practice_block = [{'nontarget': u'male_neutral_046', 'target': u'outdoor_046', 'order': 1}, {'nontarget': u'male_neutral_047', 'target': u'outdoor_047', 'order': 1}, {'nontarget': u'male_neutral_048', 'target': u'outdoor_048', 'order': 1}, {'nontarget': u'male_neutral_049', 'target': u'outdoor_049', 'order': 1}, {'nontarget': u'male_neutral_050', 'target': u'outdoor_050', 'order': 1}, {'nontarget': u'female_neutral_046', 'target': u'outdoor_051', 'order': 1}, {'nontarget': u'female_neutral_047', 'target': u'outdoor_052', 'order': 1}, {'nontarget': u'female_neutral_048', 'target': u'outdoor_053', 'order': 1}, {'nontarget': u'female_neutral_049', 'target': u'outdoor_054', 'order': 1}, {'nontarget': u'female_neutral_050', 'target': u'outdoor_055', 'order': 1}]


#-------------generating stimuli
import copy
import csv
import itertools

participant = expInfo['participant']

#create both target and lure for gender
gender_0 = ['male','female']
np.random.shuffle(gender_0)
gender_t = gender_0[-len(gender_0)]
gender_l = gender_0[1]

#create both target and lure for scene
scene_0 = ['indoor','outdoor']
np.random.shuffle(scene_0)
scene_t = scene_0[-len(scene_0)]
scene_l = scene_0[1]


#-------------------#neutral-only blocks------------------------------------------
#running iteration for attended stimuli
#target and lure
target_aN = "%s_neutral %s_neutral %s_neutral %s_neutral %s %s %s %s" %(gender_t,gender_t,gender_t,gender_t,scene_t,scene_t,scene_t,scene_t)
lure_aN = "%s_neutral %s_neutral %s_neutral %s_neutral %s %s %s %s" %(gender_l,gender_l,gender_l,gender_l,scene_l,scene_l,scene_l,scene_l)
target_aN = target_aN.split() #creating list
lure_aN = lure_aN.split() #combining lists
block_attendedN = zip(target_aN,lure_aN) #combining lists

#running iteration for attended stimuli
target_uN = "%s %s %s %s %s_neutral %s_neutral %s_neutral %s_neutral" %(scene_t,scene_t,scene_t,scene_t,gender_t,gender_t,gender_t,gender_t)
lure_uN = "%s %s %s %s %s_neutral %s_neutral %s_neutral %s_neutral" %(scene_l,scene_l,scene_l,scene_l,gender_l,gender_l,gender_l,gender_l)
target_uN = target_uN.split() #creating lists
lure_uN = lure_uN.split() #creating lists
block_unattendedN = zip(target_uN,lure_uN) #combining lists

#generating list of blocks
##combining attended and unattended lists
attended_unattended_blockN = zip(block_attendedN, block_unattendedN)


#-------------------#neutral-sad blocks------------------------------------------
#running iteration for attended stimuli
#target and lure
target_aNS = "%s_sad %s_sad %s_neutral %s_neutral %s %s %s %s" %(gender_t,gender_t,gender_t,gender_t,scene_t,scene_t,scene_t,scene_t)
lure_aNS = "%s_sad %s_sad %s_neutral %s_neutral %s %s %s %s" %(gender_l,gender_l,gender_l,gender_l,scene_l,scene_l,scene_l,scene_l)
target_aNS = target_aNS.split() #creating list
lure_aNS = lure_aNS.split() #combining lists
block_attendedNS = zip(target_aNS,lure_aNS) #combining lists

#running iteration for attended stimuli
target_uNS = "%s %s %s %s %s_sad %s_sad %s_neutral %s_neutral" %(scene_t,scene_t,scene_t,scene_t,gender_t,gender_t,gender_t,gender_t)
lure_uNS = "%s %s %s %s %s_sad %s_sad %s_neutral %s_neutral" %(scene_l,scene_l,scene_l,scene_l,gender_l,gender_l,gender_l,gender_l)
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

#generating lists
lblocksNS = []
ltrialsNS = []
lblocksN = []
ltrialsN = []
dictSetN = []
dictSetNS = []

#generating neutral blocks
p=0
for j in range(0,2):
    ltrials_ = []
    lblocks_ = []
    dictBlock_ = []
    for k in range(0,8):
        #pulling first item from target_nontarget list
        #t_nt = target_nontarget1[-len(target_nontarget1)]
        t_nt = attended_unattended_blockN[k]
    
        #stripping target, nontarget data from each block
        t_ = [i[0] for i in t_nt]
        _nt = [i[1] for i in t_nt]
    
        #-------------------#attended target------------------------------------------
        #list of targets and non-targets, as well as lures for each target (t_list)
        target_comp = [t_[0]]
        aT_list = list(range(1,46))
        formatter = '{0:03d}'.format
        aT_list = map(formatter, aT_list)#leading zeros
        aT_list = ['{}_{}'.format(a, b) for b in aT_list for a in target_comp] #list comprehension
    
        #-------------------#attended lure------------------------------------------
        lure_comp = [_nt[0]]
        aL_list = list(range(1,46))
        aL_list = map(formatter, aL_list)#leading zeros
        np.random.shuffle(aL_list)
        aL_list = aL_list[:5]#first 5 items
        aL_list = ['{}_{}'.format(a, b) for b in aL_list for a in lure_comp] #list comprehension
    
        #combining attended target and lure
        attended = aT_list + aL_list #combining lists
        np.random.shuffle(attended)
    
        #-------------------#unattended target------------------------------------------
        ##list of nontargets and non-nontargets, as well as lures for each nontarget (n_list)
        nontarget_comp = [t_[1]]
        uT_list = list(range(1,46))
        formatter = '{0:03d}'.format
        uT_list = map(formatter, uT_list)#leading zeros
        np.random.shuffle(uT_list)
        uT_list = uT_list[:25]#first 5 items
        uT_list = ['{}_{}'.format(a, b) for b in uT_list for a in nontarget_comp] #list comprehension
    
        #-------------------#unattended lure------------------------------------------
        #nontarget_lure (nl_list)
        lure_comp = [_nt[1]]
        uL_list = list(range(1,46))
        formatter = '{0:03d}'.format
        uL_list = map(formatter, uL_list)#leading zeros
        np.random.shuffle(uL_list)
        uL_list = uL_list[:25]#first 5 items
        uL_list = ['{}_{}'.format(a, b) for b in uL_list for a in lure_comp] #list comprehension
    
        #combining unattended target and lure
        unattended = uT_list + uL_list #combining lists
        np.random.shuffle(unattended)
    
       #-------------------#create iterated list------------------------------------------ 
        t_ = t_[0] #first value of tuple pair
        t_block = t_.split('_', 1)[0]
        #lblocks_.append([k,t_,t_block]) #order, #target, #target type (indoor, male, female, outdoor)
        lblocks_.append(copy.deepcopy({"order":k,"target":t_,"face_scene":t_block}))
        ltrials_.append([attended,unattended])

        dictTrials_ = []
        dictEvent_ = {}
        for f in range(0,50):
            dictEvent_ = {'#set':j, '#Block':k, 'type':'sad', 'nontarget':unattended[f], 'target':attended[f]}
            dictTrials_.append(copy.deepcopy(dictEvent_))
        
        dictBlock_.append(copy.deepcopy(dictTrials_))

        #saving to csv
        #file variable
        if not os.path.exists("procedure\participant\%s\\n"%(participant)):
            os.makedirs("procedure\participant\%s\\n"%(participant))
            
        f_name = 'procedure\participant\%s\\n\%s_%s.csv'%(participant,k,t_)
    
        #outputting set_list procedure
        with open('procedure\participant\%s\#set_list.csv'%(participant), 'a') as set_list:
            writer = csv.writer(set_list,lineterminator='\n')
            if j==0 and k==0:
                header=["face_scene","target","set","block", "set_directory"]
                writer.writerow(header)
            writer.writerow([t_block,t_,j,k,f_name])
    
        #outputting block procedure
        with open('procedure\participant\%s\\n\%s_%s.csv'%(participant,k,t_), 'wb') as target_sch:
            writer = csv.writer(target_sch)
            header=["target","nontarget","order"]
            writer.writerow(header)
            for row,row1 in itertools.izip(attended,unattended):
                writer.writerow([row,row1,k])
                
    #-------------------#appending block and trial values to lists------------------------------------------ 
    ltrialsN.append(ltrials_)
    lblocksN.append(lblocks_)
    dictSetN.append(copy.deepcopy(dictBlock_))


#generating emotional blocks
for j in range(2,4):
    ltrials_ = []
    lblocks_ = []
    dictBlock_ = []
    for k in range(0,8):
        #pulling first item from target_nontarget list
        #t_nt = target_nontarget1[-len(target_nontarget1)]
        t_nt = attended_unattended_blockNS[k]
    
        #stripping target, nontarget data from each block
        t_ = [i[0] for i in t_nt]
        _nt = [i[1] for i in t_nt]
    
        #-------------------#attended target------------------------------------------
        #list of targets and non-targets, as well as lures for each target (t_list)
        target_comp = [t_[0]]
        aT_list = list(range(1,46))
        formatter = '{0:03d}'.format
        aT_list = map(formatter, aT_list)#leading zeros
        aT_list = ['{}_{}'.format(a, b) for b in aT_list for a in target_comp] #list comprehension
    
        #-------------------#attended lure------------------------------------------
        lure_comp = [_nt[0]]
        aL_list = list(range(1,46))
        aL_list = map(formatter, aL_list)#leading zeros
        np.random.shuffle(aL_list)
        aL_list = aL_list[:5]#first 5 items
        aL_list = ['{}_{}'.format(a, b) for b in aL_list for a in lure_comp] #list comprehension
    
        #combining attended target and lure
        attended = aT_list + aL_list #combining lists
        np.random.shuffle(attended)
    
        #-------------------#unattended target------------------------------------------
        ##list of nontargets and non-nontargets, as well as lures for each nontarget (n_list)
        nontarget_comp = [t_[1]]
        uT_list = list(range(1,46))
        formatter = '{0:03d}'.format
        uT_list = map(formatter, uT_list)#leading zeros
        np.random.shuffle(uT_list)
        uT_list = uT_list[:25]#first 5 items
        uT_list = ['{}_{}'.format(a, b) for b in uT_list for a in nontarget_comp] #list comprehension
    
        #-------------------#unattended lure------------------------------------------
        #nontarget_lure (nl_list)
        lure_comp = [_nt[1]]
        uL_list = list(range(1,46))
        formatter = '{0:03d}'.format
        uL_list = map(formatter, uL_list)#leading zeros
        np.random.shuffle(uL_list)
        uL_list = uL_list[:25]#first 5 items
        uL_list = ['{}_{}'.format(a, b) for b in uL_list for a in lure_comp] #list comprehension
    
        #combining unattended target and lure
        unattended = uT_list + uL_list #combining lists
        np.random.shuffle(unattended)
    
       #-------------------#create iterated list------------------------------------------ 
        t_ = t_[0] #first value of tuple pair
        t_block = t_.split('_', 1)[0]
        #lblocks_.append([k,t_,t_block]) #order, #target, #target type (indoor, male, female, outdoor)
        lblocks_.append(copy.deepcopy({"order":k,"target":t_,"face_scene":t_block}))
        ltrials_.append([attended,unattended])

        dictTrials_ = []
        dictEvent_ = {}
        for f in range(0,50):
            dictEvent_ = {'#set':j, '#Block':k, 'type':'sad', 'nontarget':unattended[f], 'target':attended[f]}
            dictTrials_.append(copy.deepcopy(dictEvent_))
        
        dictBlock_.append(copy.deepcopy(dictTrials_))
        
        #saving to csv
        #file variable
        if not os.path.exists("procedure\participant\%s\s"%(participant)):
            os.makedirs("procedure\participant\%s\s"%(participant))
            
        f_name = 'procedure\participant\%s\s\%s_%s.csv'%(participant,k,t_)
    
        #outputting set_list procedure
        with open('procedure\participant\%s\#set_list.csv'%(participant), 'a') as set_list:
            writer = csv.writer(set_list,lineterminator='\n')
            writer.writerow([t_block,t_,j,k,f_name])
    
        #outputting block procedure
        with open('procedure\participant\%s\s\%s_%s.csv'%(participant,k,t_), 'wb') as target_sch:
            writer = csv.writer(target_sch)
            header=["target","nontarget","order"]
            writer.writerow(header)
            for row,row1 in itertools.izip(attended,unattended):
                writer.writerow([row,row1,k])
            
    #-------------------#appending block and trial values to lists------------------------------------------ 
    ltrialsNS.append(ltrials_)
    lblocksNS.append(lblocks_)
    dictSetNS.append(copy.deepcopy(dictBlock_))

#------------------------------------------------------------- 
#------------------------------------------------------------- 
#-------------------#sum of all blocks, sum of all trials------------------------------------------ 
lblocks = lblocksNS + lblocksN
ltrials = ltrialsNS + ltrialsN
dictTask = dictSetNS + dictSetN
del attended_unattended_blockN, attended_unattended_blockNS, b, block_attendedN, block_attendedNS,\
block_unattendedN, block_unattendedNS, formatter, gender_0, gender_l, gender_t, lblocksN, lblocksNS, dictSetN, dictSetNS,\
lblocks_, ltrialsNS, ltrialsN, ltrials_, ltaskOrder_, ltaskType_, lure_aN, lure_aNS, lure_comp, lure_uN,\
lure_uNS, aT_list, aL_list, nontarget_comp, scene_0, scene_l, scene_t, t_, t_block, uL_list, uT_list,\
t_nt, target_aN, target_aNS, target_comp, target_uN, target_uNS, a, f, i, j, k, attended, unattended, dictBlock_, dictEvent_, dictTrials_

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

# Initialize components for Routine "Task_Instructions"
Task_InstructionsClock = core.Clock()
Practice_instructions_2 = visual.ImageStim(
    win=win, name='Practice_instructions_2',
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
#sending keyboard responses to mri
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")

# Initialize components for Routine "Block_Instructions"
Block_InstructionsClock = core.Clock()
Block_instr_image = visual.ImageStim(
    win=win, name='Block_instr_image',
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

# Initialize components for Routine "Break"
BreakClock = core.Clock()
break_display = visual.ImageStim(
    win=win, name='break_display',
    image="Instructions/Break.png", mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
Break_end = 0

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

# set up handler to look after randomisation of conditions etc
Introduction_Loop = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('procedure\\Introduction_list.csv'),
    seed=None, name='Introduction_Loop')
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
    task_instr_image.setImage("Instructions/"+Introduction_image)
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
            theseKeys = event.getKeys(keyList=['space'])
            
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


# set up handler to look after randomisation of conditions etc
Practice_intro_loop = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('procedure\\practice_list.csv'),
    seed=None, name='Practice_intro_loop')
thisExp.addLoop(Practice_intro_loop)  # add the loop to the experiment
thisPractice_intro_loop = Practice_intro_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPractice_intro_loop.rgb)
if thisPractice_intro_loop != None:
    for paramName in thisPractice_intro_loop.keys():
        exec(paramName + '= thisPractice_intro_loop.' + paramName)

for thisPractice_intro_loop in Practice_intro_loop:
    currentLoop = Practice_intro_loop
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_intro_loop.rgb)
    if thisPractice_intro_loop != None:
        for paramName in thisPractice_intro_loop.keys():
            exec(paramName + '= thisPractice_intro_loop.' + paramName)
    
    # ------Prepare to start Routine "Practice_Instructions"-------
    t = 0
    Practice_InstructionsClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    Practice_instructions.setImage("Instructions/"+Practice_image)
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
            theseKeys = event.getKeys(keyList=['space'])
            
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
# completed 1 repeats of 'Practice_intro_loop'


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
    trialList=data.importConditions(practice_block),
    seed=None, name='Practice_loop')
thisExp.addLoop(Practice_loop)  # add the loop to the experiment
thisPractice_loop = Practice_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
if thisPractice_loop != None:
    for paramName in thisPractice_loop.keys():
        exec(paramName + '= thisPractice_loop.' + paramName)

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
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    #preparing image name ----------6/8/2017 SMR
    #if target is faces
    if Practice_image == "female.png" or Practice_image == "male.png":
        image_name = "stimuli/"+target+"_"+nontarget+".png"
    #else target is scenes
    else:
        image_name = "stimuli/"+nontarget+"_"+target+".png"
    
    print("target: "+target)
    print("nontarget: "+nontarget)
    print("image: "+image_name)
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
        frameRemains = 0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuli_key.status == STARTED and t >= frameRemains:
            stimuli_key.status = STOPPED
        if stimuli_key.status == STARTED:
            theseKeys = event.getKeys(keyList=['1'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if stimuli_key.keys == []:  # then this was the first keypress
                    stimuli_key.keys = theseKeys[0]  # just the first key pressed
                    stimuli_key.rt = stimuli_key.clock.getTime()
                    # was this 'correct'?
                    if (stimuli_key.keys == str('')) or (stimuli_key.keys == ''):
                        stimuli_key.corr = 1
                    else:
                        stimuli_key.corr = 0
        
        # *stim_display* updates
        if t >= 0.0 and stim_display.status == NOT_STARTED:
            # keep track of start time/frame for later
            stim_display.tStart = t
            stim_display.frameNStart = frameN  # exact frame index
            stim_display.setAutoDraw(True)
        frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
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
        if str('').lower() == 'none':
           stimuli_key.corr = 1  # correct non-response
        else:
           stimuli_key.corr = 0  # failed to respond (incorrectly)
    # store data for Practice_loop (TrialHandler)
    Practice_loop.addData('stimuli_key.keys',stimuli_key.keys)
    Practice_loop.addData('stimuli_key.corr', stimuli_key.corr)
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
        theseKeys = event.getKeys(keyList=['space'])
        
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
Set_loop = data.TrialHandler(nReps=4, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='Set_loop')
thisExp.addLoop(Set_loop)  # add the loop to the experiment
thisSet_loop = Set_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisSet_loop.rgb)
if thisSet_loop != None:
    for paramName in thisSet_loop.keys():
        exec(paramName + '= thisSet_loop.' + paramName)

for thisSet_loop in Set_loop:
    currentLoop = Set_loop
    # abbreviate parameter names if possible (e.g. rgb = thisSet_loop.rgb)
    if thisSet_loop != None:
        for paramName in thisSet_loop.keys():
            exec(paramName + '= thisSet_loop.' + paramName)
    
    # ------Prepare to start Routine "MRI_Fixation"-------
    t = 0
    MRI_FixationClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(6.000000)
    # update component parameters for each repeat
    fixation_image_2.setImage("Instructions/Fixation.png")
    #--------------------send mri trigger
    shell.SendKeys("5")
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
        frameRemains = 0.0 + 6- win.monitorFramePeriod * 0.75  # most of one frame period left
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
    
    
    # set up handler to look after randomisation of conditions etc
    Block_loop = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('procedure\\participant\\%s\\#set_list.csv'),
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
        Block_instr_image.setImage("Instructions/"+face_scene+".png")
        print("block: "+face_scene)
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
            trialList=data.importConditions(block_file),
            seed=None, name='Trial_Loop')
        thisExp.addLoop(Trial_Loop)  # add the loop to the experiment
        thisTrial_Loop = Trial_Loop.trialList[0]  # so we can initialise stimuli with some values
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
            
            # ------Prepare to start Routine "Stimuli"-------
            t = 0
            StimuliClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(1.000000)
            # update component parameters for each repeat
            #preparing image name ----------6/8/2017 SMR
            #if target is faces
            if Practice_image == "female.png" or Practice_image == "male.png":
                image_name = "stimuli/"+target+"_"+nontarget+".png"
            #else target is scenes
            else:
                image_name = "stimuli/"+nontarget+"_"+target+".png"
            
            print("target: "+target)
            print("nontarget: "+nontarget)
            print("image: "+image_name)
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
                frameRemains = 0 + 1- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimuli_key.status == STARTED and t >= frameRemains:
                    stimuli_key.status = STOPPED
                if stimuli_key.status == STARTED:
                    theseKeys = event.getKeys(keyList=['1'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if stimuli_key.keys == []:  # then this was the first keypress
                            stimuli_key.keys = theseKeys[0]  # just the first key pressed
                            stimuli_key.rt = stimuli_key.clock.getTime()
                            # was this 'correct'?
                            if (stimuli_key.keys == str('')) or (stimuli_key.keys == ''):
                                stimuli_key.corr = 1
                            else:
                                stimuli_key.corr = 0
                
                # *stim_display* updates
                if t >= 0.0 and stim_display.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stim_display.tStart = t
                    stim_display.frameNStart = frameN  # exact frame index
                    stim_display.setAutoDraw(True)
                frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
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
                if str('').lower() == 'none':
                   stimuli_key.corr = 1  # correct non-response
                else:
                   stimuli_key.corr = 0  # failed to respond (incorrectly)
            # store data for Trial_Loop (TrialHandler)
            Trial_Loop.addData('stimuli_key.keys',stimuli_key.keys)
            Trial_Loop.addData('stimuli_key.corr', stimuli_key.corr)
            if stimuli_key.keys != None:  # we had a response
                Trial_Loop.addData('stimuli_key.rt', stimuli_key.rt)
            thisExp.nextEntry()
            
        # completed 1 repeats of 'Trial_Loop'
        
        thisExp.nextEntry()
        
    # completed 1 repeats of 'Block_loop'
    
    
    # set up handler to look after randomisation of conditions etc
    Break_loop = data.TrialHandler(nReps=5, method='random', 
        extraInfo=expInfo, originPath=-1,
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
        # update component parameters for each repeat
        Break_key = event.BuilderKeyResponse()
        if Break_end > 3:
            Break_loop.finished = True
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
                event.clearEvents(eventType='keyboard')
            if Break_key.status == STARTED:
                theseKeys = event.getKeys(keyList=['space'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
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
        
    # completed 5 repeats of 'Break_loop'
    
    thisExp.nextEntry()
    
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
    frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
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

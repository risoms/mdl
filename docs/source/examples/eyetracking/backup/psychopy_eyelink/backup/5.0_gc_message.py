#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.04), April 26, 2016, at 11:02
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'CGP'  # from the Builder filename that created this script
expInfo = {u'Participant': u'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/csv/%s_%s' %(expInfo['Participant'],expName,)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=[1920, 1080], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
    monitor='Experiment', color=[-0.137,-0.137,-0.137], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "Calibration_Verification"
Calibration_VerificationClock = core.Clock()
import pylink
from _script import eyelink_device
from win32api import GetSystemMetrics
import time

#constants
trialNum = 0

#screen
w = GetSystemMetrics(0)
h = GetSystemMetrics(1)

#constants
GCWINDOW = .5 #500 msec
DURATION = 2 #2000 msec
gbox = 200 #gaze boundary
inbox = False

#find out which eye
left_eye = 0
right_eye = 1
binocular = 2

#bounding box
sc = [w / 2.0, h / 2.0] #center of screen 
size = 100 #Length of one side of box
xbdr = [sc[0] - size, sc[0] + size]
ybdr = [sc[1] - size, sc[1] + size]


def start_recording():
    global eye_used
    global dt
    global inbox
    pylink.getEYELINK().sendMessage('TRIALID %s'%(trialNum))
    pylink.getEYELINK().sendCommand("record_status_message 'trial %s image %s'" %(trialNum,scenestim))
    pylink.getEYELINK().sendCommand("set_idle_mode")
    time.sleep(.05) #Waits 50ms to allow eyelink to prepare
    pylink.getEYELINK().sendCommand("clear_screen 0")
    
    pylink.getEYELINK().sendCommand("draw_box %s %s %s %s %s" %(w/2 - 100, h/2 - 100, w/2 + 100, h/2 + 100,  7))
    
    # Begin recording
    pylink.getEYELINK().startRecording(1, 1, 1, 1)
    dt = pylink.getEYELINK().getNewestSample() # check for new sample update
    eye_used = pylink.getEYELINK().eyeAvailable() #determine which eye(s) are available
    
    inbox = False

def gc_window():
    global gaze_timer
    global inbox
    dt = pylink.getEYELINK().getNewestSample() # check for new sample update
    if(dt != None): # Gets the gaze position of the latest sample
        if eye_used == right_eye:
            gx,gy = dt.getRightEye().getGaze()
        elif eye_used == left_eye:
            gx,gy = dt.getLeftEye().getGaze()

    if xbdr[0] < gx < xbdr[1] and ybdr[0] < gy < ybdr[1]: #is gaze within the update region
        if (time.clock() - gaze_timer) > GCWINDOW: #if YES: compare current time and gcwindow onset against GCDURATION
            pylink.getEYELINK().sendMessage('WindowOffset')
            inbox = True
    else:
        gaze_timer = time.clock()

# Initialize components for Routine "Block_Instructions"
Block_InstructionsClock = core.Clock()
Block_image = visual.ImageStim(win=win, name='Block_image',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()

fixation_cross = visual.ImageStim(win=win, name='fixation_cross',
    image="Instructions/fixation.png", mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Initialize components for Routine "IAPS"
IAPSClock = core.Clock()

iaps_display = visual.ImageStim(win=win, name='iaps_display',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
blank = visual.ImageStim(win=win, name='blank',
    image="Instructions/blank.png", mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "Break"
BreakClock = core.Clock()
break_display = visual.ImageStim(win=win, name='break_display',
    image="Instructions/Break.png", mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
Break_end = 0

# Initialize components for Routine "Finish"
FinishClock = core.Clock()
End_Screen = visual.ImageStim(win=win, name='End_Screen',
    image="Instructions/finished.png", mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "Calibration_Verification"-------
t = 0
Calibration_VerificationClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
#EyeLink-1 Initize
edfsubject = (expInfo['Participant'])
# Initiate eye-tracker link and open EDF
tracker = eyelink_device.Connect(win, edfsubject)
# Calibrate eye-tracker
tracker.calibrate()
# keep track of which components have finished
Calibration_VerificationComponents = []
for thisComponent in Calibration_VerificationComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Calibration_Verification"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = Calibration_VerificationClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Calibration_VerificationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Calibration_Verification"-------
for thisComponent in Calibration_VerificationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "Calibration_Verification" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block_loop = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions('procedure\\#set_list.csv'),
    seed=None, name='block_loop')
thisExp.addLoop(block_loop)  # add the loop to the experiment
thisBlock_loop = block_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlock_loop.rgb)
if thisBlock_loop != None:
    for paramName in thisBlock_loop.keys():
        exec(paramName + '= thisBlock_loop.' + paramName)

for thisBlock_loop in block_loop:
    currentLoop = block_loop
    # abbreviate parameter names if possible (e.g. rgb = thisBlock_loop.rgb)
    if thisBlock_loop != None:
        for paramName in thisBlock_loop.keys():
            exec(paramName + '= thisBlock_loop.' + paramName)
    
    #------Prepare to start Routine "Block_Instructions"-------
    t = 0
    Block_InstructionsClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    block_key = event.BuilderKeyResponse()  # create an object of type KeyResponse
    block_key.status = NOT_STARTED
    Block_image.setImage("Instructions/"+block_display+".png")
    # keep track of which components have finished
    Block_InstructionsComponents = []
    Block_InstructionsComponents.append(block_key)
    Block_InstructionsComponents.append(Block_image)
    for thisComponent in Block_InstructionsComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Block_Instructions"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = Block_InstructionsClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *block_key* updates
        if t >= 0.0 and block_key.status == NOT_STARTED:
            # keep track of start time/frame for later
            block_key.tStart = t  # underestimates by a little under one frame
            block_key.frameNStart = frameN  # exact frame index
            block_key.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(block_key.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if block_key.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                block_key.keys = theseKeys[-1]  # just the last key pressed
                block_key.rt = block_key.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # *Block_image* updates
        if t >= 0.0 and Block_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            Block_image.tStart = t  # underestimates by a little under one frame
            Block_image.frameNStart = frameN  # exact frame index
            Block_image.setAutoDraw(True)
        
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
    
    #-------Ending Routine "Block_Instructions"-------
    for thisComponent in Block_InstructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if block_key.keys in ['', [], None]:  # No response was made
       block_key.keys=None
    # store data for block_loop (TrialHandler)
    block_loop.addData('block_key.keys',block_key.keys)
    if block_key.keys != None:  # we had a response
        block_loop.addData('block_key.rt', block_key.rt)
    # the Routine "Block_Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    Trial_Loop = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=None,
        trialList=data.importConditions(block_file),
        seed=None, name='Trial_Loop')
    thisExp.addLoop(Trial_Loop)  # add the loop to the experiment
    thisTrial_Loop = Trial_Loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrial_Loop.rgb)
    if thisTrial_Loop != None:
        for paramName in thisTrial_Loop.keys():
            exec(paramName + '= thisTrial_Loop.' + paramName)
    
    for thisTrial_Loop in Trial_Loop:
        currentLoop = Trial_Loop
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_Loop.rgb)
        if thisTrial_Loop != None:
            for paramName in thisTrial_Loop.keys():
                exec(paramName + '= thisTrial_Loop.' + paramName)
        
        #------Prepare to start Routine "Fixation"-------
        t = 0
        FixationClock.reset()  # clock 
        frameN = -1
        routineTimer.add(2.000000)
        # update component parameters for each repeat
        trialNum = trialNum + 1 #trial count
        start_recording()

        # keep track of which components have finished
        FixationComponents = []
        FixationComponents.append(fixation_cross)
        for thisComponent in FixationComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Fixation"-------
        continueRoutine = True
        gaze_timer = time.clock()
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = FixationClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            # *fixation_cross* updates
            win.flip()
            fixation_cross.draw()
            
            # update/draw components on each frame
            if inbox != True:
                gc_window()
            
            if fixation_cross.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
                fixation_cross.setAutoDraw(False)            
            
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
                
        #------Prepare to start Routine "IAPS"-------
        t = 0
        IAPSClock.reset()  # clock 
        frameN = -1
        routineTimer.add(7.000000)
        # update component parameters for each repeat
        
        iaps_display.setImage("stimulus/"+scenestim)
        # keep track of which components have finished
        IAPSComponents = []
        IAPSComponents.append(iaps_display)
        IAPSComponents.append(blank)
        for thisComponent in IAPSComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "IAPS"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = IAPSClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *iaps_display* updates
            if t >= 0 and iaps_display.status == NOT_STARTED:
                # keep track of start time/frame for later
                iaps_display.tStart = t  # underestimates by a little under one frame
                iaps_display.frameNStart = frameN  # exact frame index
                iaps_display.setAutoDraw(True)
            if iaps_display.status == STARTED and t >= (5-win.monitorFramePeriod*0.75): #most of one frame period left
                iaps_display.setAutoDraw(False)
            
            # *blank* updates
            if t >= 5 and blank.status == NOT_STARTED:
                # keep track of start time/frame for later
                blank.tStart = t  # underestimates by a little under one frame
                blank.frameNStart = frameN  # exact frame index
                blank.setAutoDraw(True)
            if blank.status == STARTED and t >= (7-win.monitorFramePeriod*0.75): #most of one frame period left
                blank.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in IAPSComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "IAPS"-------
        for thisComponent in IAPSComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        #EyeLink-4 End Trial
        #creating csv file for gaze info
        #gaze_csv = _thisDir + os.sep + 'data/gaze/' + edfsubject + '.csv'
        #with open(gaze_csv, "w") as output:
        #    writer = csv.writer(output, lineterminator='\n')
        #    for val in gaze:
        #        writer.writerow([val])  
        #end of trial message
        tracker.send_message('Ending Recording')
        
        
        #The IMGLOAD command is used to show an overlay image in Data Viewer.  This will code the time that the PictureTrial image should appear.
        pylink.getEYELINK().sendMessage("!V IMGLOAD CENTER  %s" %(scenestim))
        
        #IAPS
        # Send onset time
        offset = int((t-iaps_display.tStart) * 1000)
        msg = str(offset) + " IAPS_Onset"
        pylink.getEYELINK().sendMessage(msg)
        
        #IAPS
        # Send offset time
        offset = int((t-blank.tStart) * 1000)
        msg = str(offset) + " IAPS_Offset"
        pylink.getEYELINK().sendMessage(msg)
        
        time.sleep(.10) #Waits 50ms to allow eyelink to prepare
        #stop recording
        pylink.getEYELINK().stopRecording()
        
        #VARIABLES
        msg = "!V TRIAL_VAR picture %s" %(scenestim) #scenestim
        pylink.getEYELINK().sendMessage(msg)
        msg = "!V TRIAL_VAR valence %s" %(valence) #valence
        pylink.getEYELINK().sendMessage(msg)
        msg = "!V TRIAL_VAR valmean %s" %(valmean) #valmean
        pylink.getEYELINK().sendMessage(msg)
        msg = "!V TRIAL_VAR arousal %s" %(arousal) #arousal
        pylink.getEYELINK().sendMessage(msg)
        msg = "!V TRIAL_VAR arousalmean %s" %(arousalmean) #arousalmean
        pylink.getEYELINK().sendMessage(msg)
        msg = "!V TRIAL_VAR BlockVar %s" %(blocknum) #blocknum
        pylink.getEYELINK().sendMessage(msg)
        msg = "!V TRIAL_VAR outlier %s" %(outliers) #outliers
        pylink.getEYELINK().sendMessage(msg)
        
        #TRIAL RESULTS
        pylink.getEYELINK().sendMessage("TRIAL_RESULT 1")
        thisExp.nextEntry()
        
    # completed 1 repeats of 'Trial_Loop'
    
    
    # set up handler to look after randomisation of conditions etc
    Break_loop = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=None,
        trialList=[None],
        seed=None, name='Break_loop')
    thisExp.addLoop(Break_loop)  # add the loop to the experiment
    thisBreak_loop = Break_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisBreak_loop.rgb)
    if thisBreak_loop != None:
        for paramName in thisBreak_loop.keys():
            exec(paramName + '= thisBreak_loop.' + paramName)
    
    for thisBreak_loop in Break_loop:
        currentLoop = Break_loop
        # abbreviate parameter names if possible (e.g. rgb = thisBreak_loop.rgb)
        if thisBreak_loop != None:
            for paramName in thisBreak_loop.keys():
                exec(paramName + '= thisBreak_loop.' + paramName)
        
        #------Prepare to start Routine "Break"-------
        t = 0
        BreakClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        Break_key = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Break_key.status = NOT_STARTED
        if Break_end > 3:
            Break_loop.finished = True
        # keep track of which components have finished
        BreakComponents = []
        BreakComponents.append(Break_key)
        BreakComponents.append(break_display)
        for thisComponent in BreakComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Break"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = BreakClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Break_key* updates
            if t >= 0.0 and Break_key.status == NOT_STARTED:
                # keep track of start time/frame for later
                Break_key.tStart = t  # underestimates by a little under one frame
                Break_key.frameNStart = frameN  # exact frame index
                Break_key.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(Break_key.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if Break_key.status == STARTED:
                theseKeys = event.getKeys(keyList=['space'])
                
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
                break_display.tStart = t  # underestimates by a little under one frame
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
        
        #-------Ending Routine "Break"-------
        for thisComponent in BreakComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if Break_key.keys in ['', [], None]:  # No response was made
           Break_key.keys=None
        # store data for Break_loop (TrialHandler)
        Break_loop.addData('Break_key.keys',Break_key.keys)
        if Break_key.keys != None:  # we had a response
            Break_loop.addData('Break_key.rt', Break_key.rt)
        
        # the Routine "Break" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'Break_loop'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'block_loop'


#------Prepare to start Routine "Finish"-------
t = 0
FinishClock.reset()  # clock 
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
FinishComponents = []
FinishComponents.append(End_Screen)
for thisComponent in FinishComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Finish"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = FinishClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *End_Screen* updates
    if t >= 0.0 and End_Screen.status == NOT_STARTED:
        # keep track of start time/frame for later
        End_Screen.tStart = t  # underestimates by a little under one frame
        End_Screen.frameNStart = frameN  # exact frame index
        End_Screen.setAutoDraw(True)
    if End_Screen.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
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

#-------Ending Routine "Finish"-------
for thisComponent in FinishComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#EyeLink-4 Close
#set offline mode so we can transfer file
edfpath = _thisDir + os.sep + 'data/edf'
tracker.end_experiment(edfpath)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()

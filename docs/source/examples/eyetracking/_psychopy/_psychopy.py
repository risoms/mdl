#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.7),
    on April 11, 2019, at 14:51
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.0.7'
expName = '_psychopy'  # from the Builder filename that created this script
expInfo = {'participant': '001', 'dominant eye': "'left'"}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s'%(expInfo['participant'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\mdl-admin\\Desktop\\mdl-eyelink\\mdl\\docs\\source\\examples\\eyetracking\\_psychopy\\_psychopy.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.WARNING)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=False, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='VIEWPixx', color=[-0.122,-0.122,-0.122], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "calibration"
calibrationClock = core.Clock()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instructions_text = visual.TextStim(win=win, name='instructions_text',
    text='Stay fixated on the central white dot and ignore the word itself. To respond press:\n - Left for red LETTERS\n - Down for green LETTERS\n - Right for blue LETTERS\n\nPress SPACE to continue.',
    font='Calibri',
    units='pix', pos=[0, 0], height=50, wrapWidth=800, ori=0, 
    color=[1, 1, 1], colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "task"
taskClock = core.Clock()
stimulus_text = visual.TextStim(win=win, name='stimulus_text',
    text='default text',
    font='Calibri',
    pos=[0, 0], height=100, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
fixation = visual.GratingStim(
    win=win, name='fixation',units='pix', 
    tex='sin', mask='circle',
    ori=0, pos=[0, 0], size=[16,16], sf=40, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=.7,blendmode='avg',
    texRes=128, interpolate=True, depth=-1.0)
gaze_cursor = visual.GratingStim(
    win=win, name='gaze_cursor',units='pix', 
    tex='sin', mask='circle',
    ori=0, pos=[0,0], size=1.0, sf=40, phase=0.0,
    color=[0.004,0.004,1.000], colorSpace='rgb', opacity=1.0,blendmode='avg',
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "finished"
finishedClock = core.Clock()
finished_text = visual.TextStim(win=win, name='finished_text',
    text='This is the end of the experiment. Thanks!\n\nPress SPACE to exit.',
    font='Calibri',
    units='pix', pos=[0, 0], height=50, wrapWidth=800, ori=0, 
    color=[1, 1, 1], colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "calibration"-------
t = 0
calibrationClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# get parameters from PsychoPy
subject = expInfo['participant']
dominant_eye = expInfo['dominant eye']

# Initialize the Eyelink.
import os, sys
sys.path.append(os.path.abspath(os.getcwd() + '../../../../../../../'))
import mdl
eyetracking = mdl.eyetracking.run(window=win, libraries=True, subject=subject, timer=routineTimer, demo=True)

# Connect to the Eyelink Host.
param = eyetracking.connect(calibration_type=13)

# Set the dominant eye
eye_used = eyetracking.set_eye_used(eye=dominant_eye)

# Start calibration.
calibration = eyetracking.calibration()
# keep track of which components have finished
calibrationComponents = []
for thisComponent in calibrationComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "calibration"-------
while continueRoutine:
    # get current time
    t = calibrationClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    if calibration == True:
        continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in calibrationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "calibration"-------
for thisComponent in calibrationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "calibration" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
instructions_keyboard = event.BuilderKeyResponse()
# keep track of which components have finished
instructionsComponents = [instructions_text, instructions_keyboard]
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions_text* updates
    if t >= 0 and instructions_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions_text.tStart = t
        instructions_text.frameNStart = frameN  # exact frame index
        instructions_text.setAutoDraw(True)
    
    # *instructions_keyboard* updates
    if t >= 0 and instructions_keyboard.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions_keyboard.tStart = t
        instructions_keyboard.frameNStart = frameN  # exact frame index
        instructions_keyboard.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if instructions_keyboard.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='block')
thisExp.addLoop(block)  # add the loop to the experiment
thisBlock = block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in block:
    currentLoop = block
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=5.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('trialTypes.xlsx'),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "task"-------
        t = 0
        taskClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        stimulus_text.setColor(stimColor, colorSpace='rgb')
        stimulus_text.setText(stimText)
        stimulus_keyboard = event.BuilderKeyResponse()
        # Start recording. This should be run at the start of the trial. 
        # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
        eyetracking.start_recording(trial=trials.thisN, block=block.thisN)
        
        # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
        # Sending message "stimulus onset".
        msg = "stimulus onset"
        eyetracking.send_message(msg=msg)
        # keep track of which components have finished
        taskComponents = [stimulus_text, fixation, gaze_cursor, stimulus_keyboard]
        for thisComponent in taskComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "task"-------
        while continueRoutine:
            # get current time
            t = taskClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *stimulus_text* updates
            if t >= 0.5 and stimulus_text.status == NOT_STARTED:
                # keep track of start time/frame for later
                stimulus_text.tStart = t
                stimulus_text.frameNStart = frameN  # exact frame index
                stimulus_text.setAutoDraw(True)
            
            # *fixation* updates
            if t >= 0 and fixation.status == NOT_STARTED:
                # keep track of start time/frame for later
                fixation.tStart = t
                fixation.frameNStart = frameN  # exact frame index
                fixation.setAutoDraw(True)
            
            # *gaze_cursor* updates
            if t >= 0.0 and gaze_cursor.status == NOT_STARTED:
                # keep track of start time/frame for later
                gaze_cursor.tStart = t
                gaze_cursor.frameNStart = frameN  # exact frame index
                gaze_cursor.setAutoDraw(True)
            if gaze_cursor.status == STARTED:  # only update if drawing
                gaze_cursor.setOpacity(1, log=False)
                gaze_cursor.setPos([0,0], log=False)
                gaze_cursor.setSize((30,30), log=False)
            
            # *stimulus_keyboard* updates
            if t >= 0.5 and stimulus_keyboard.status == NOT_STARTED:
                # keep track of start time/frame for later
                stimulus_keyboard.tStart = t
                stimulus_keyboard.frameNStart = frameN  # exact frame index
                stimulus_keyboard.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(stimulus_keyboard.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if stimulus_keyboard.status == STARTED:
                theseKeys = event.getKeys(keyList=['left', 'down', 'right'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    stimulus_keyboard.keys = theseKeys[-1]  # just the last key pressed
                    stimulus_keyboard.rt = stimulus_keyboard.clock.getTime()
                    # was this 'correct'?
                    if (stimulus_keyboard.keys == str(corrAns)) or (stimulus_keyboard.keys == corrAns):
                        stimulus_keyboard.corr = 1
                    else:
                        stimulus_keyboard.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            #if eyetracker:
            #    # check for 'g' key press to toggle gaze cursor visibility
            #    if iokeyboard.getPresses(keys=['g',]):
            #        display_gaze=not display_gaze
            #
            #    # get /eye tracker gaze/ position 
            #    gpos=eyetracker.getPosition()
            #    if type(gpos) in [list,tuple]:
            #        x,y=gpos[0], gpos[1]
            #        d=np.sqrt(x**2+y**2)
            #        if d>maintain_fix_pix_boundary:
            #            heldFixation = False #unless otherwise
            
            
            
            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in taskComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "task"-------
        for thisComponent in taskComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if stimulus_keyboard.keys in ['', [], None]:  # No response was made
            stimulus_keyboard.keys=None
            # was no response the correct answer?!
            if str(corrAns).lower() == 'none':
               stimulus_keyboard.corr = 1;  # correct non-response
            else:
               stimulus_keyboard.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('stimulus_keyboard.keys',stimulus_keyboard.keys)
        trials.addData('stimulus_keyboard.corr', stimulus_keyboard.corr)
        if stimulus_keyboard.keys != None:  # we had a response
            trials.addData('stimulus_keyboard.rt', stimulus_keyboard.rt)
        # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
        # Sending message "stimulus offset".
        msg = "stimulus offset"
        eyetracking.send_message(msg=msg)
        # Prepare variables to be sent to Eyelink
        variables = dict(color=stimColor, text=stimText, isCongruent=congruent, response=stimulus_keyboard.keys, correct=corrAns)
        # Stop recording
        eyetracking.stop_recording(trial=trials.thisN, block=block.thisN, variables=variables)
        # the Routine "task" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 5.0 repeats of 'trials'
    
# completed 1 repeats of 'block'


# ------Prepare to start Routine "finished"-------
t = 0
finishedClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
finished_keyboard = event.BuilderKeyResponse()
# keep track of which components have finished
finishedComponents = [finished_text, finished_keyboard]
for thisComponent in finishedComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "finished"-------
while continueRoutine:
    # get current time
    t = finishedClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *finished_text* updates
    if t >= 0.0 and finished_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        finished_text.tStart = t
        finished_text.frameNStart = frameN  # exact frame index
        finished_text.setAutoDraw(True)
    frameRemains = 0.0 + 2.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if finished_text.status == STARTED and t >= frameRemains:
        finished_text.setAutoDraw(False)
    
    # *finished_keyboard* updates
    if t >= 0.0 and finished_keyboard.status == NOT_STARTED:
        # keep track of start time/frame for later
        finished_keyboard.tStart = t
        finished_keyboard.frameNStart = frameN  # exact frame index
        finished_keyboard.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(finished_keyboard.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if finished_keyboard.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            finished_keyboard.keys = theseKeys[-1]  # just the last key pressed
            finished_keyboard.rt = finished_keyboard.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in finishedComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "finished"-------
for thisComponent in finishedComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if finished_keyboard.keys in ['', [], None]:  # No response was made
    finished_keyboard.keys=None
thisExp.addData('finished_keyboard.keys',finished_keyboard.keys)
if finished_keyboard.keys != None:  # we had a response
    thisExp.addData('finished_keyboard.rt', finished_keyboard.rt)
thisExp.nextEntry()
# the Routine "finished" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# Finish recording
eyetracking.finish_recording()
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

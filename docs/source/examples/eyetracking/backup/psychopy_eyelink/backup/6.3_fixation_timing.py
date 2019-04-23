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
filename = _thisDir + os.sep + 'data/csv/%s_%s' %(expInfo['Participant'],expName)

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
NOT_STARTED = 0
PLAYING = 1
STARTED = PLAYING
PAUSED = 2
STOPPED = -1
FINISHED = STOPPED

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
from win32api import GetSystemMetrics
import time
import re
from _script import eyelink_display
from statistics import stdev
from PIL import Image
import pandas
from psychopy.hardware import joystick

#constants
trialNum = 0

class libeyelink():
    def __init__(self,edfsubject):
        # Make filename
        self.fname = os.path.splitext(edfsubject)[0]  # strip away extension if present
        assert re.match(r'\w+$', self.fname), 'Name must only include A-Z, 0-9, or _'
        assert len(self.fname) <= 8, 'Name must be <= 8 characters.'
        # Make filename 
        self.edfname = self.fname + '.edf'
    
        # Initialize connection with eyetracker
        try:
            self.tracker = pylink.EyeLink()
            self.realconnect = True
        except RuntimeError:
            self.tracker = pylink.EyeLink(None)
            self.realconnect = False
        
        #properties
        #screen
        self.w = GetSystemMetrics(0)
        self.h = GetSystemMetrics(1)        
        #find out which eye
        self.eye_used = None
        self.left_eye = 0
        self.right_eye = 1
        self.binocular = 2        
        #gaze-timing
        self.GCWINDOW = .5 #500 msec
        self.DURATION = 2 #2000 msec
        self.gbox = 200 #gaze boundary
        self.inbox = False
        self.Finished = False
        self.Fixation = True        
        #gaze-bounding box
        self.sc = [self.w / 2.0, self.h / 2.0] #center of screen
        self.size = 100 #Length of one side of box
        self.xbdr = [self.sc[0] - self.size, self.sc[0] + self.size]
        self.ybdr = [self.sc[1] - self.size, self.sc[1] + self.size]        
        #calibration
        self.cnum = 13 # 13 pt calibration
        self.paval = 1000 #Pacing of calibration, t in milliseconds        
        #pupil

        # Open EDF
        pylink.getEYELINK().openDataFile(self.edfname)
        pylink.flushGetkeyQueue()
        pylink.getEYELINK().setOfflineMode()
        
        # notify eyelink of display resolution        
        pylink.getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %(self.w - 1, self.h - 1))
        pylink.getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" %(self.w - 1, self.h - 1))
        
        # Set content of edf file
        pylink.getEYELINK().sendCommand(
            'file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT')
        
        pylink.getEYELINK().sendCommand(
            'link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON')
    
        pylink.getEYELINK().sendCommand(
            'link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET')
    
        pylink.getEYELINK().sendCommand(
            'file_sample_data = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT')
    
        # Set display coords for dataviewer
        pylink.getEYELINK().sendMessage("screen_pixel_coords =  0 0 %d %d" %(self.w - 1, self.h - 1))
        pylink.getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" %(self.w - 1, self.h - 1))
    
    def calibrate(self):
        """
        Calibrates eyetracker using psychopy stimuli.
        """
    
        # Generate custom calibration stimuli
        self.genv = eyelink_display.calibration_display(self.w,self.h,self.tracker,win)
    
        if self.realconnect:
            # Set calibration type
            pylink.getEYELINK().setCalibrationType('HV%d'%(self.cnum))
    
            # Set calibraiton pacing
            pylink.getEYELINK().setAutoCalibrationPacing(self.paval)
    
            # Execute custom calibration display
            pylink.openGraphicsEx(self.genv)
    
            # Calibrate
            pylink.getEYELINK().doTrackerSetup(self.w, self.h)
    
    def gc_window(self):
        global inbox
        global Finished
        global Fixation
        global gaze_timer
        if self.eye_used == None:
            self.set_eye_used()
        dt = pylink.getEYELINK().getNewestSample() # check for new sample update
        if(dt != None): # Gets the gaze position of the latest sample
            if self.eye_used == self.right_eye:
                gx,gy = dt.getRightEye().getGaze()
            elif self.eye_used == self.left_eye:
                gx,gy = dt.getLeftEye().getGaze()
            else:
                gx,gy = (-1,-1)
    
        if self.xbdr[0] < gx < self.xbdr[1] and self.ybdr[0] < gy < self.ybdr[1]: #is gaze congingent fixation within the update region
            if (time.clock() - gaze_timer) > self.GCWINDOW: #if YES: compare current time and gcwindow onset against GCDURATION
                pylink.getEYELINK().sendMessage('WindowOffset')
                inbox = True
                Finished = True #allows skipping of gc_drift()
                Fixation = False
        else:
            gaze_timer = time.clock()
    
    def gc_drift_correct(self):
        pylink.getEYELINK().sendMessage("GC_failed") #send failure message
        pylink.pumpDelay(100) #Allow Windows to clean up while we record additional 100 msec of data 
        pylink.getEYELINK().stopRecording()
        pylink.getEYELINK().doDriftCorrect(int(self.sc[0]), int(self.sc[1]), 0, 0)

    def pupil_sample(self):
        """
        desc:
            Returns the newest pupil size sample; size may be measured as the
            diameter or the area of the pupil, depending on your setup (note
            that pupil size mostly is given in an arbitrary units).
        returns:dt.getRightEye()
            desc: Returns pupil size for the eye that is currently
                being tracked (as specified by self.eye_used) or -1
                when no data is obtainable.
    		type:	[int, float]
        """
        if self.eye_used == None:
            self.set_eye_used()
        s = pylink.getEYELINK().getNewestSample() # check for new sample update
        if(s != None): # Gets the pupil size of the latest sample
            if self.eye_used == self.right_eye:
                ps = s.getRightEye().getPupilSize()
            elif self.eye_used == self.left_eye:
                ps = s.getLeftEye().getPupilSize()
            # invalid
            else:
                ps = -1
        return ps

    def set_eye_used(self):
        self.eye_used = pylink.getEYELINK().eyeAvailable()
        if self.eye_used == self.right_eye:
            self.eye_used = self.right_eye
        elif self.eye_used == self.left_eye or self.eye_used == self.binocular:
            self.eye_used = self.left_eye

    def start_recording(self):
        self.recording = False
        pylink.getEYELINK().sendMessage('TRIALID %s'%(trialNum))
        pylink.getEYELINK().sendCommand("record_status_message 'trial %s image %s'" %(trialNum,scenestim))
        pylink.getEYELINK().sendCommand("set_idle_mode")
        core.wait(.05) #delay so tracker is ready (using psychopy)
        pylink.getEYELINK().sendCommand("clear_screen 0")
        pylink.getEYELINK().sendCommand("draw_box %s %s %s %s %s" %(self.w/2 - 100, self.h/2 - 100, self.w/2 + 100, self.h/2 + 100,  7))
        
        # Begin recording
        pylink.getEYELINK().startRecording(1, 1, 1, 1)
        pylink.pumpDelay(100)#100 milliseconds of data to accumulate before the trial display starts    
        self.inbox = False #reset gaze congingent fixation
        self.Finished = False #if gaze congingent fixation failed
    
    def stop_recording(self):
        self.recording = False
        pylink.pumpDelay(100) #Allow Windows to clean up while we record additional 100 msec of data
        pylink.getEYELINK().stopRecording()
        while pylink.getEYELINK().getkey():
            pass  

    def close(self,spath):
        # Generate file path
        self.fpath = os.path.join(spath, self.edfname)
        
        # Close the file and transfer it to Display PC
        pylink.getEYELINK().closeDataFile()
        time.sleep(1)
        assert os.path.isdir(spath), 'EDF destination directory does not exist.'
        pylink.getEYELINK().receiveDataFile(self.edfname, self.fpath)
        pylink.getEYELINK().close()    

    def tracker_time(self):
        #Returns the current tracker time (in milliseconds) since the tracker application started
        tt = pylink.getEYELINK().trackerTimeUsec()
        return tt

    def min_max(self,lst):
        lst = [x for x in lst if x != -1 and x != 0]
        _mean = sum(lst)/len(lst)
        _stdev = stdev(lst)    
        _max = _mean + _stdev
        _min = _mean - _stdev
        return _min,_max,_mean,_stdev

    def pupil_cue(self,p_ma,p_min,p_max):
        global prev_ #previous image color
        less_ = p_ma < p_min
        greater_ = p_ma > p_max
        if less_: #pupil size less than 1SD from baseline
            im = Image.new("RGB", (stim_size), "red")
            im.save("red.png")
            iaps_cue.setImage("red.png")
            iaps_cue.setAutoDraw(True)
            pylink.getEYELINK().sendMessage('redimage')
            pylink.getEYELINK().sendMessage('mean %s min %s max %s'%(p_ma,p_min,p_max))
            print('red image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
            prev_ = less_
        elif greater_:#pupil size greater than 1SD from baseline        
            im = Image.new("RGB", (stim_size), "green")
            im.save("green.png")
            iaps_cue.setImage("green.png")
            iaps_cue.setAutoDraw(True)
            pylink.getEYELINK().sendMessage('greenimage')
            pylink.getEYELINK().sendMessage('mean %s min %s max %s'%(p_ma,p_min,p_max))
            print('green image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
            prev_ = greater_
        else: #pupil size within 1SD from baseline            
            im = Image.new("RGB", (stim_size), "blue")
            im.save("blue.png")
            iaps_cue.setImage("blue.png")
            iaps_cue.setAutoDraw(True)
            pylink.getEYELINK().sendMessage('blueimage')
            pylink.getEYELINK().sendMessage('mean %s min %s max %s'%(p_ma,p_min,p_max))
            print('blue image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))

    def moving_avg(self,lst):
        df = pandas.DataFrame(data=lst, columns=['samples']) #convert to dataframe
        rm = pandas.rolling_mean(df,rw)[rw-1:] #moving average
        ma = rm['samples'][rm.index[-1]] #gets last pupil sample
        return ma
        

mouse = event.Mouse(win=win)
gamepad_available = False #debug - turn on if task is ready for implimentation
if gamepad_available:
    gamepad = joystick.Joystick(0)

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
iaps_cue = visual.ImageStim(win=win, name='iaps_cue',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=.5,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
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

#EyeLink-1 Prepare
subno = (expInfo['Participant'])

# Prepare eyetracker link and open EDF
eyelink=libeyelink(subno)

# Calibrate eyetracker
eyelink.calibrate()

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
            event.clearEvents(None)
            event.mouseButtons = [0, 0, 0]
        if block_key.status == STARTED:
            theseKeys = event.getKeys(None)
            buttons = mouse.getPressed()
            if gamepad_available:
                pressed = gamepad.getAllButtons()
                if sum(buttons) > 0:  # ie if any button is pressed
                    # abort routine on response
                    continueRoutine = False
                for anyState in pressed:
                    if anyState == True:
                        continueRoutine = False
            
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
        #eyelink-initalize per block
        Fixation = True
        trialNum = trialNum + 1 #trial count
        #pupil
        baseline=True
        t0=0 #tracker time
        lpb=[]
        ltb=[]
        while Fixation:
            # update component parameters for each repeat
            inbox = False
            Finished = False
            t = 0
            FixationClock.reset()  # clock 
            frameN = -1
            
            #eyelink-start recording
            eyelink.start_recording()
            
            #-------Start Routine "Fixation"-------
            gaze_timer = time.clock()
            #while continueRoutine and routineTimer.getTime() > 0:
            while FixationClock.getTime() < 2:
                # get current time
                t = FixationClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                
                # *fixation_cross* updates
                win.flip()
                fixation_cross.draw()
                
                # update/draw components on each frame
                #eyelink-gaze contingent fixation
                if inbox != True:
                    eyelink.gc_window()
                
                #eyelink-pupil dilation baseline
                if t >= 1.75: #baseline duration 250ms, before Fixation offset
                    t1 = eyelink.tracker_time() #prevent duplicate samples due to difference in refresh rate (Eyelink 500Hz)
                    if (t1 - t0) > 1500: #collect sample only if more than 1.5msec (=1500 microsec) has gone by
                        ps = eyelink.pupil_sample()
                        lpb.append(ps)
                        t0 = t1
                        ltb.append(t0)
                
                if t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
                    fixation_cross.setAutoDraw(False)
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
            
            #if Fixation failed run drift correct             
            if Finished != True:
                eyelink.gc_drift_correct()
        
        pb_min,pb_max,pb_mean,pb_stdev = eyelink.min_max(lpb)
        #------Prepare to start Routine "IAPS"-------
        t = 0
        IAPSClock.reset()  # clock 
        frameN = -1
        #pupil
        rw = 8 #running average window (appox .5 samples/ms * 15ms window)
        t0=0 #tracker time
        ts0=0 #time between cue updates
        lps_n0 = 0 #no of pupil sample count
        lps=[] #pupil sample list
        lts=[] #pupil sample time collected
        prev_ = 0
        collect_ma=True

        # update component parameters for each repeat       
        iaps_display.setImage("stimulus/"+scenestim)
        im=Image.open("stimulus/"+scenestim)
        stim_size = im.size[0]+4,im.size[1]+4
        # keep track of which components have finished
        IAPSComponents = []
        IAPSComponents.append(iaps_display)
        IAPSComponents.append(iaps_cue)
        IAPSComponents.append(blank)
        for thisComponent in IAPSComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "IAPS"-------
        continueRoutine = True
        print('trial start')#debug
        while continueRoutine and IAPSClock.getTime() < 12:
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
            if iaps_display.status == STARTED and t >= (10-win.monitorFramePeriod*0.75): #most of one frame period left
                iaps_display.setAutoDraw(False)

            #eyelink-pupil dilation moving average
            if t >= 0.005: #collect samples 5ms after stimulus onset
                t1 = eyelink.tracker_time() #prevent duplicate samples due to difference in refresh rate (Eyelink 500Hz)
                if (t1 - t0) > 1800: #collect new sample only if more than 1.800msec (1 msec = 1000 microsec) has gone by since old sample
                    ps = eyelink.pupil_sample()
                    lps.append(ps)
                    lps_n1=len(lps)
                    t0 = t1
                    lts.append(t0) #debug
                    #create moving average
                    lps = [x for x in lps if x != -1 and x != 0] #removing samples with value of 0 and -1 before converting allowing moving average
                    if len(lps) > rw: #start moving average after minimum samples (=rw)
                        pma = eyelink.moving_avg(lps)

            #eyelink-iaps_cue* updates
            if t >= 0.005 and iaps_display.status == STARTED: #run while stimulus is being displayed
                if (lps_n1-lps_n0) >= 25: #update cue rate (1 sample ≈ 2 msec)
                    eyelink.pupil_cue(pma,pb_min,pb_max)
                    lps_n0 = lps_n1 #make new count into old count for next iteration
                    print('num of samples = %s' %(lps_n0))#debug
                    print('moving average = %s'%(pma))#debug
                    print('min = %s max %s'%(pb_min,pb_max))#debug
                    print('time = %s'%(t))#debug
                    print('time between samples = %s'%(t - ts0))#debug
                    ts0 = t #debug time between updates
                
            if iaps_cue.status == STARTED and t >= (10-win.monitorFramePeriod*0.75): #most of one frame period left
                iaps_cue.setAutoDraw(False)
            
            # *blank* updates
            if t >= 10 and blank.status == NOT_STARTED:
                # keep track of start time/frame for later
                blank.tStart = t  # underestimates by a little under one frame
                blank.frameNStart = frameN  # exact frame index
                blank.setAutoDraw(True)
            if blank.status == STARTED and t >= (12-win.monitorFramePeriod*0.75): #most of one frame period left
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
        pylink.getEYELINK().sendMessage('Ending Recording')
        
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
        
        pylink.pumpDelay(100) #Allow Windows to clean up while we record additional 100 msec of data
        
        #stop recording
        eyelink.stop_recording()
        
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
                event.clearEvents(None)
                event.mouseButtons = [0, 0, 0]
            if Break_key.status == STARTED:
                theseKeys = event.getKeys(None)
                buttons = mouse.getPressed()
                if gamepad_available:
                    pressed = gamepad.getAllButtons()
                    if sum(buttons) > 0:  # ie if any button is pressed
                        # abort routine on response
                        continueRoutine = False
                    for anyState in pressed:
                        if anyState == True:
                            continueRoutine = False



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
        thisExp.nextEntry()
        
    # completed 1 repeats of 'Break_loop'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'block_loop'


#------Prepare to start Routine "Finish"-------
t = 0
FinishClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
# keep track of which components have finished
FinishComponents = []
FinishComponents.append(End_Screen)
for thisComponent in FinishComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Finish"-------
continueRoutine = True
while continueRoutine and FinishClock.getTime() < 5:
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
eyelink.close(edfpath)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()

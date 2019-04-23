#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.04), April 26, 2016, at 11:02
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008


Articles:
Using Eye tracking technology to study the effects of cognition on pupil size
Pupillometry A Window to the Preconscious?
The pupillary light response reflects exogenous attention and inhibition of return

6.6.03 (5/23)
updates
- output trial data for comparison with eyelink recordings (cross-validate)
- output baseline data for comparison with eyelink recordings (cross-validate)
- removed neutral images 
- added composite image
    * Use composite image once per block to collect baseline
    * this will serve as baseline pupil size
- started blink detection (pupil_samplexy)
to do
- Task:
    - drop pupil size recording if gaze is not detected and in stimulus window
    - find filtering technique for blinks (wait for chris email)
    - possible solution:
        - try to somehow get possible mininum and maxinum pupil size and drop values that are outside of this range before each cue presentation
        - if gaze is non-existant drop value
- Block:
    - record baseline for last 1000ms

see:for more information on blink and online data: https://www.sr-support.com/showthread.php?4845-Plotting-the-change-in-pupil-size-throughout-the-trial&highlight=blink 

6.6.02 (5/18)
updates
- updated instructions to be task relevant
- improved instruction image quality 

to do
- automatic calibration after 2x failed drift correct
- test timing of new iaps onset message +
- test dropping of samples (50%)
- test if working: mouse pointer disappear
- test if working: final break screen dissapears and ends task +
- test: accuracy of all collected variables (e.g. time, pupil size, pupil mean, pupil moving average.....)
- fix: correct save time for edf files

6.6.01 (5/17)
- task uses moving median instead of moving average
- stimulus display is 20sec
- cue shift is in intervals of 250msec
- isoluminant baseline is -250msec after stimulus onset
"""
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui
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
filename = _thisDir + os.sep + '_data/csv/%s_%s' %(expInfo['Participant'],expName)

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
win = visual.Window(size=[1920, 1080], fullscr=True, screen=0, allowGUI=True, allowStencil=False,
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

#for debugging
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import psutil

#imports for cross-validation
import csv
import itertools

#mouse invisible
win.mouseVisible = False

#constants
trialNum = 0
blockNum = 0
eye_used = None
header = True #if header doesn't exist - used for outputing pupil samples

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
        self.red = 'red'
        self.green = 'green'
        self.blue = 'blue'
        # Open EDF
        pylink.getEYELINK().openDataFile(self.edfname)
        pylink.flushGetkeyQueue()

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
        
        #select sound for calibration and drift correct
        pylink.setCalibrationSounds("off", "off", "off");
        pylink.setDriftCorrectSounds("off", "off", "off");

        #Places EyeLink tracker in offline (idle) mode        
        pylink.getEYELINK().setOfflineMode()
    
    def calibrate(self):
        """
        Calibrates eyetracker using psychopy stimuli.
        """
        if DC>=2: #if drift correct failed 3 times in a row
            pylink.getEYELINK().sendMessage("Drift_failed") #send failure message
            self.stop_recording()
        
        if self.realconnect:
            # Generate custom calibration stimuli
            self.genv = eyelink_display.calibration_display(self.w,self.h,self.tracker,win)
             
            pylink.getEYELINK().setCalibrationType('HV%d'%(self.cnum))# Set calibration type
            pylink.getEYELINK().setAutoCalibrationPacing(self.paval)# Set calibraiton pacing
            pylink.openGraphicsEx(self.genv)# Execute custom calibration display
            pylink.getEYELINK().doTrackerSetup(self.w, self.h)# Calibrate
    
    def gc_window(self):
        global inbox
        global GAZE
        global Fixation
        global gaze_timer
        dt = pylink.getEYELINK().getNewestSample() # check for new sample update
        if(dt != None): # Gets the gaze position of the latest sample
            if eye_used == self.right_eye:
                gx,gy = dt.getRightEye().getGaze()
            else:
                gx,gy = dt.getLeftEye().getGaze()
    
        if self.xbdr[0] < gx < self.xbdr[1] and self.ybdr[0] < gy < self.ybdr[1]: #is gaze congingent fixation within the update region
            if (time.clock() - gaze_timer) > self.GCWINDOW: #if YES: compare current time and gcwindow onset against GCDURATION
                pylink.getEYELINK().sendMessage('WindowOffset')
                inbox = True
                GAZE = True #allows skipping of gc_drift()
                Fixation = False
        else:
            gaze_timer = time.clock()
    
    def gc_drift_correct(self):
        pylink.getEYELINK().sendMessage("Fixation_failed") #send failure message
        self.stop_recording()
        pylink.getEYELINK().doDriftCorrect(int(self.sc[0]), int(self.sc[1]), 0, 0)

    def pupil_sample(self):
        """
        desc:
            Returns the newest pupil size sample.
        returns:dt.getRightEye()
            desc: Returns pupil size for the eye that is currently
                being tracked
    		type:	[int, float]
        """
        s = pylink.getEYELINK().getNewestSample() # check for new sample update
        if(s != None): # Gets the pupil size of the latest sample
            if eye_used == self.right_eye:
                ps = s.getRightEye().getPupilSize()
            else:
                ps = s.getLeftEye().getPupilSize()
            return ps

    def pupil_sample_xy(self,size):
        """
        desc:
            Returns the newest pupil size sample -  contingent on gaze position
        returns:dt.getRightEye()
            desc: Returns pupil size for the eye that is currently being tracked
        for more information on blink and online data: https://www.sr-support.com/showthread.php?4845-Plotting-the-change-in-pupil-size-throughout-the-trial&highlight=blink 
        """
        xbl=size[0]
        ybl=size[1]
        xblr = [self.sc[0] - (xbl/2), self.sc[0] + (xbl/2)]
        yblr = [self.sc[1] - (ybl/2), self.sc[1] + (ybl/2)]  
        s = pylink.getEYELINK().getNewestSample() # check for new sample update
        if(s != None): # Gets the gaze position of the latest sample
            if eye_used == self.right_eye:
                gx,gy = s.getRightEye().getGaze()
            else:
                gx,gy = s.getLeftEye().getGaze()
                
            if xblr[0] < gx < xblr[1] and yblr[0] < gy < yblr[1]: #is gaze congingent fixation within the update region
                if eye_used == self.right_eye:
                    ps = s.getRightEye().getPupilSize()
                else:
                    ps = s.getLeftEye().getPupilSize()
                return ps

    def set_eye_used(self):
        eye_ = pylink.getEYELINK().eyeAvailable()
        return eye_

    def start_recording(self):
        """
        Comments: Recording may take 10 to 30 milliseconds to begin from this command.
        Parameters:
            file_samples  If 1, writes samples to EDF file. If 0, disables sample recording.  
            file_events  If 1, writes events to EDF file. If 0, disables event recording.  
            link_samples  If 1, sends samples through link. If 0, disables link sample access.  
            link_events  If 1, sends events through link. If 0, disables link event access.  
        Returns: 0 if successful, else trial return code. 
        """
        global trialNum
        global scenestim
        if baseline:
            pylink.getEYELINK().sendCommand("record_status_message 'Block A%s Image %s.png'" %(blockNum,block_event)) #send message to Eyelink viewer
            pylink.getEYELINK().sendMessage('TRIALID A%s'%(blockNum))
            pylink.getEYELINK().sendCommand("clear_screen 0")
            pylink.getEYELINK().sendCommand("draw_box %s %s %s %s %s" %(self.w/2 - 512, self.h/2 - 384, self.w/2 + 512, self.h/2 + 384,  7))
            pylink.beginRealTimeMode(100) #start realtime mode
            pylink.getEYELINK().startRecording(1, 1, 1, 1) #Begin recording - (0,0,1,0): sends samples through link   
        else:
            pylink.getEYELINK().sendCommand("record_status_message 'Trial %s Image %s'" %(trialNum,scenestim)) #send message to Eyelink viewer
            pylink.getEYELINK().sendMessage('TRIALID %s'%(trialNum))
            pylink.getEYELINK().sendCommand("clear_screen 0")
            pylink.getEYELINK().sendCommand("draw_box %s %s %s %s %s" %(self.w/2 - 100, self.h/2 - 100, self.w/2 + 100, self.h/2 + 100,  7))
            pylink.beginRealTimeMode(100) #start realtime mode
            pylink.getEYELINK().startRecording(1, 1, 1, 1)# Begin recording
    
    def stop_recording(self):
        pylink.endRealTimeMode()
        pylink.msecDelay(100) #Allow Windows to clean up while we record additional 100 msec of data
        pylink.getEYELINK().stopRecording()
        pylink.msecDelay(50)
        pylink.getEYELINK().setOfflineMode() #Places EyeLink tracker in off-line (idle) mode

    def close(self,spath):
        # Generate file path
        self.fpath = os.path.join(spath, self.edfname)
        
        # Close the file and transfer it to Display PC
        pylink.endRealTimeMode()
        pylink.getEYELINK().closeDataFile()
        pylink.msecDelay(50)
        pylink.getEYELINK().receiveDataFile(self.edfname, self.fpath) #copy EDF file to Display PC
        pylink.getEYELINK().close() #Close connection to tracker

    def tracker_time(self):
        #Returns the current tracker time (in milliseconds) since the tracker application started
        tt = pylink.getEYELINK().trackerTimeUsec()
        return tt

    def min_max(self,lst):
        _mean = sum(lst)/len(lst)
        _stdev = stdev(lst)    
        _max = _mean + (_stdev *2)
        _min = _mean - (_stdev *2)
        return _min,_max,_mean,_stdev

    def pupil_cue(self,count,lst,p_min,p_max):
        global p_ma
        p_ma = self.moving_avg(count,lst)
        less_ = p_ma < p_min
        greater_ = p_ma > p_max
        if less_: #pupil size less than 2SD from baseline
            if old_cue == self.blue:
                return 'blue'
            else:
                iaps_cue.setImage("blue.png")
                iaps_cue.setAutoDraw(True)
                print('blue image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
                return 'blue'
        elif greater_:#pupil size greater than 2SD from baseline    
            if old_cue == self.red:
                return 'red'
            else:
                iaps_cue.setImage("red.png")
                iaps_cue.setAutoDraw(True)
                print('red image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
                return 'red'
        else: #pupil size within 2SD from baseline
            if old_cue == self.green:
                return 'green'
            else:
                iaps_cue.setImage("green.png")
                iaps_cue.setAutoDraw(True)
                print('green image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
                return 'green'

    def moving_avg(self,count,lst):
        rm = pandas.DataFrame(lst, columns=['samples']).rolling(count,center=False).median() #moving average
        ma = rm['samples'][rm.index[-1]] #last pupil sample
        return ma
   
    def sample_time(self,s_1,s_0):  #collect new sample only if more than 2 msec has gone by since old sample (Eyelink-500Hz)
        su = (s_1 - s_0) >= .002
        return su
    
    def cue_time(self,c1,c0): #create new cue only if more than 250 msec has gone by since old cue
        cu = (c1 - c0) >= 0.250
        return cu
        
mouse = event.Mouse(win=win)
gamepad_available = False #debug - turn on if task is ready for implimentation
if gamepad_available:
    gamepad = joystick.Joystick(0)

# Initialize components for Routine "Introduction"
IntroductionClock = core.Clock()
task_instr_image = visual.ImageStim(win=win, name='task_instr_image',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "Block_Instructions"
Block_InstructionsClock = core.Clock()
Block_image = visual.ImageStim(win=win, name='Block_image',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Initialize components for Routine "Block_event"
Block_eventClock = core.Clock()
composite_display = visual.ImageStim(win=win, name='composite_display',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

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
break_image = visual.ImageStim(win=win, name='break_image',
    image='sin', mask=None,
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
DC = 0
eyelink.calibrate()

# Set eye used
eye_used = eyelink.set_eye_used()

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
Introduction_Loop = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions('procedure\\Introduction_list.csv'),
    seed=None, name='Introduction_Loop')
thisExp.addLoop(Introduction_Loop)  # add the loop to the experiment
thisIntroduction_Loop = Introduction_Loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisIntroduction_Loop.rgb)
if thisIntroduction_Loop != None:
    for paramName in thisIntroduction_Loop.keys():
        exec(paramName + '= thisIntroduction_Loop.' + paramName)

for thisIntroduction_Loop in Introduction_Loop:
    currentLoop = Introduction_Loop
    # abbreviate parameter names if possible (e.g. rgb = thisIntroduction_Loop.rgb)
    if thisIntroduction_Loop != None:
        for paramName in thisIntroduction_Loop.keys():
            exec(paramName + '= thisIntroduction_Loop.' + paramName)
    
    #------Prepare to start Routine "Introduction"-------
    t = 0
    IntroductionClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    task_instr_image.setImage("Instructions/"+Introduction_image+".png")
    Inst__Key = event.BuilderKeyResponse()  # create an object of type KeyResponse
    Inst__Key.status = NOT_STARTED
    
    # keep track of which components have finished
    IntroductionComponents = []
    IntroductionComponents.append(task_instr_image)
    IntroductionComponents.append(Inst__Key)
    for thisComponent in IntroductionComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Introduction"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = IntroductionClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *task_instr_image* updates
        if t >= 0.0 and task_instr_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            task_instr_image.tStart = t  # underestimates by a little under one frame
            task_instr_image.frameNStart = frameN  # exact frame index
            task_instr_image.setAutoDraw(True)
        
        # *Inst__Key* updates
        if t >= 0.0 and Inst__Key.status == NOT_STARTED:
            # keep track of start time/frame for later
            Inst__Key.tStart = t  # underestimates by a little under one frame
            Inst__Key.frameNStart = frameN  # exact frame index
            Inst__Key.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(None)
            event.mouseButtons = [0, 0, 0]
        if Inst__Key.status == STARTED:
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
    
    #-------Ending Routine "Introduction"-------
    for thisComponent in IntroductionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "Introduction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 1 repeats of 'Introduction_Loop'


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
	routineTimer.reset()
    
    #------Prepare to start Routine "Block_event"-------
    t = 0
    Block_eventClock.reset()  # clock 
    frameN = -1
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    # pupil
    baseline=True #allow start_recording to use baseline parameters
    blockNum = blockNum + 1 #trial count
    st0=0 #time between samples (st1-st0)
    lpb=[] #baseline samples
    Window = True #window to collect samples
    #eyelink-start recording
    eyelink.start_recording()
    composite_display.setImage("instructions/"+block_event+".png")
    image_size = composite_display.size[0],composite_display.size[1]
    # keep track of which components have finished
    Block_eventComponents = []
    Block_eventComponents.append(composite_display)
    for thisComponent in Block_eventComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Block_event"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Block_eventClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *composite_display* updates
        if t >= 0 and composite_display.status == NOT_STARTED:
            # keep track of start time/frame for later
            composite_display.tStart = t  # underestimates by a little under one frame
            composite_display.frameNStart = frameN  # exact frame index
            composite_display.setAutoDraw(True)
        if composite_display.status == STARTED and t >= (5-win.monitorFramePeriod*0.75): #most of one frame period left
            composite_display.setAutoDraw(False)
            
            
        #eyelink-pupil dilation baseline
        if Block_eventClock.getTime() >= 4: #baseline duration 1000ms, before Block Event offset
            while Window:
                st1 = Block_eventClock.getTime()
                if eyelink.sample_time(st1,st0):
                    ps = eyelink.pupil_sample()
                    #if ps != 0: #if pupil sample detected and gaze within image window
                    lpb.append(ps)
                    st0 = st1
                if Block_eventClock.getTime() >= 5:
                    break
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Block_eventComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Block_event"-------
    #eyelink-stop baseline recording  
    eyelink.stop_recording()
    baseline = False
    
    for thisComponent in Block_eventComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)    
    
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
        #st0=0 #time between samples (st1-st0)
        #lpb=[] #baseline samples
        DC = 0 #force calibration if drift correct is failed 3 times in a row
        Event_draw = False #marks the zero-time in a trial
        
        while Fixation:
            # update component parameters for each repeat
            inbox = False
            GAZE = False
            t = 0
            FixationClock.reset()  # clock 
            frameN = -1
            
            #eyelink-start recording
            eyelink.start_recording()
            
            #-------Start Routine "Fixation"-------
            gaze_timer = time.clock()
            #while continueRoutine and routineTimer.getTime() > 0:
            while FixationClock.getTime() < 2:
                #if Event_draw != True:
                    #pylink.getEYELINK().sendMessage("SYNCTIME")
                    #Event_draw = True
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
                
                if t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
                    fixation_cross.setAutoDraw(False)
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
            
            #if Fixation failed              
            #if GAZE != True:
            #    if DC >=2:#if drift correct failed twice run calibration
            #        eyelink.calibrate()
            #        DC = 0 #reset counter
            #    else: # drift correct
            #        eyelink.gc_drift_correct()
            #        DC = DC + 1 #add counter
        
        #------Prepare to start Routine "IAPS"-------
        with PyCallGraph(output=GraphvizOutput()):
            t = 0
            IAPSClock.reset()  # clock 
            frameN = -1
            #pupil
            rw=20 #running average window (appox 20 samples/200 msec)
            Total_Samples_old=0 #no. of samples
            st0=0 #time between samples (st1-st0)
            ct0=0 #time between cues (ct1-ct0)
            lps=[] #pupil sample list
            lts=[] #pupil sample time collected
            old_cue = None
            Window = True #window to collect samples
            Cue = True

            #debug for cross-validation
            p_ma = NaN #providing dummy value for moving average
            cpu_s = psutil.cpu_percent(interval=None)
            ram_s = psutil.virtual_memory().percent  
            ltt=[] #time stamp of each cue onset (eyelink)
            temp_lps=[]#list of pupil samples at each cue
            lpma=[]#list of moving averages at each cue
            ltrial=[]#list of trials at each cue
            lblock=[]#list of trials at each cue
            lpp_t=[]#time stamp of each cue onset (psychopy)
            lpb_max=[]#list of pupil baseline max
            lpb_min=[]#list of pupil baseline min
            temp_lpb=[]#list of pupil baseline mean
            cpu_pc=[]#list of cpu usage, by %
            ram_pc=[]#list of ram usage, by %

    
            stimulus_offset = 20 #time (sec)
            blank_offset = 22 #time (sec)
            collect_ma=True
            pb_min,pb_max,pb_mean,pb_stdev = eyelink.min_max(lpb) #collect baseline min max mean and stdev (debug)
    
            # update component parameters for each repeat       
            iaps_display.setImage("stimulus/"+scenestim)
            image_size = iaps_display.size[0],iaps_display.size[1]
            color_list = ["blue","red","green"]
            for color_image in color_list:
                im = Image.new("RGB", (image_size), color_image)
                im.save("%s.png"%(color_image))
            
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
            pylink.getEYELINK().sendMessage('baseline %s min %s max %s'%(pb_mean,pb_min,pb_max))
            while continueRoutine and IAPSClock.getTime() < blank_offset:
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
                    pylink.getEYELINK().sendMessage('IAPS Onset')
                if iaps_display.status == STARTED and t >= (stimulus_offset-win.monitorFramePeriod*0.75): #most of one frame period left
                    iaps_display.setAutoDraw(False)
    
                #eyelink-pupil dilation sampling
                if IAPSClock.getTime() >= 0 and iaps_display.status == STARTED: #collect samples 5ms after stimulus onset
                    while Window:
                        st1 = IAPSClock.getTime()
                        ct1 = IAPSClock.getTime()
                        if eyelink.sample_time(st1,st0): #if time between samples > 2 msec                      
                            ps = eyelink.pupil_sample()
                            #if ps != 0: #if pupil sample detected
                            lps.append(ps)
                            
                            #debug #creating variables for cross-validation #sample level
                            tt = eyelink.tracker_time()#tracker time
                            ltt.append(tt)
                            pp_t = IAPSClock.getTime()#psychopy time
                            lpp_t.append(pp_t)                            
                            temp_lps.append(ps)#pupil size at cue                                                      
                            lpma.append(p_ma)#pupil moving average at cue
                            temp_lpb.append(pb_mean)
                            lpb_min.append(pb_min)
                            lpb_max.append(pb_max)                            
                            ltrial.append(trialNum)#trial number                            
                            lblock.append(blockNum)#block number
                            cpu_pc.append(cpu_s)#cpu,ram
                            ram_pc.append(ram_s)
                            #end debug
                            
                            st0 = st1
                        if eyelink.cue_time(ct1,ct0): #if time between cues > 250 msec
                            ct0 = ct1
                            #raw_lps = len(lps) - lps0 #sample size before artifact clearing for current cue
                            break
    
                #eyelink-iaps_cue* updates
                if IAPSClock.getTime() >= 0.250 and iaps_display.status == STARTED: #run while stimulus is being displayed
                    #lps_new = [x for x in lps if x != 0] #removing missing samples (0 and -1) before moving average
                    Total_Samples = len(lps_new) #sample size after artifact clearing
                    Cue_Samples = Total_Samples - Total_Samples_old
                    Total_Samples_old = Total_Samples #update current sample list
                    old_cue = eyelink.pupil_cue(Cue_Samples,lps,pb_min,pb_max)
                    Total_Samples_old = Total_Samples #update current sample list

                    #debug #creating variables for cross-validation #cue level
                    cpu_s = psutil.cpu_percent(interval=None) #update cpu at each cue. this will avoid error with psutil where cpu=0
                    ram_s = psutil.virtual_memory().percent  #update ram at each cue. ram doesnt appear to change during task, so less samples may be better
                    

                if iaps_cue.status == STARTED and t >= (stimulus_offset-win.monitorFramePeriod*0.75): #most of one frame period left
                    iaps_cue.setAutoDraw(False)
                
                # *blank* updates
                if t >= stimulus_offset and blank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    blank.tStart = t  # underestimates by a little under one frame
                    blank.frameNStart = frameN  # exact frame index
                    blank.setAutoDraw(True)
                    pylink.getEYELINK().sendMessage('Blank Onset')
                if blank.status == STARTED and t >= (blank_offset-win.monitorFramePeriod*0.75): #most of one frame period left
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
        #creating csv file for following:
        #timestamp #pupil size #pupil running average #trial
        #outputting set_list procedure
        with open('_data\gaze\%s.csv'%(subno), 'a') as cross_val:
            writer = csv.writer(cross_val,lineterminator='\n')
            if header:
                s_header=["block","trial","eyelink_timestamp","psychopy_timestamp","pupil_sample","pupil_running_avg","pupil_baseline_min","pupil_baseline_mean","pupil_baseline_max","cpu","ram"]
                writer.writerow(s_header)
                header=False
            writer.writerows(itertools.izip(lblock,ltrial,ltt,lpp_t,temp_lps,lpma,lpb_min,temp_lpb,lpb_max,cpu_pc,ram_pc))

        #end of trial message
        pylink.getEYELINK().sendMessage('Ending Recording')
        
        #The IMGLOAD command is used to show an overlay image in Data Viewer.  This will code the time that the PictureTrial image should appear.
        pylink.getEYELINK().sendMessage("!V IMGLOAD CENTER  %s" %(scenestim))
        
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
        msg = "!V TRIAL_VAR BlockVar %s" %(blockNum) #blocknum
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
        break_image.setImage("Instructions/"+break_display+".png")
        Break_end = Break_end + 1 #block count
        if Break_end > 2:
            Break_loop.finished = True
        # keep track of which components have finished
        BreakComponents = []
        BreakComponents.append(Break_key)
        BreakComponents.append(break_image)
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
                if Break_end > 2:
                    continueRoutine = False                  
            
            # *break_image* updates
            if t >= 0.0 and break_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                break_image.tStart = t  # underestimates by a little under one frame
                break_image.frameNStart = frameN  # exact frame index
                break_image.setAutoDraw(True)
            
            
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
edfpath = _thisDir + os.sep + '_data/edf'
eyelink.close(edfpath)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()

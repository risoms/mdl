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

6.7.04 (6/28)
From Chris
- 4 blocks
	- block 1: set up baseline
		- view-only block: establish baseline and SD for images
		- present neutral images
	- block 2-4: use baseline and adapt (trial level)
		- shift baseline location (mean) and size (SD) according to fixation and feedback updates
        		- if trial has no changes in feedback, shift threshold size (SD) down
                 - if trial has too many changes in feedback, shift threshold size up
            have this version present a version with shifts and without 

changes: 
DONE added new block. 1) this block will have the same images as succeeding blocks, but not feedback presentation
                      stimuli during this block will also be present for 5 seconds
                      2) pupil means will be collected during this block and used as a baseline for future blocks

DONE    new baseline. 1) use the parameters setup by the new baseline (SD, mean) as thresholds for blocks 2-4.
                      shift thresholds using baseline mean from fixation
                      have two versions of task (shift version, no-shift version) and compare
    
DONE         cleanup. 1) created functions for trial-level lists, booleans, and constants

6.7.03 (6/23)
changes:
    critical
    - Removed Block level fixation. Sticking with trial fixation
    - automating delay of stimulus onset until 1 sec of blink-free fixation occured
    - Improve overcorrecting non-blink events (dips in blink onset)
    
    efficency
    - created functions for: list appending, csv updates. this will prevent changes to be missed between fixation and stimulus code
    - changed duration of stimulus presentation to 10 sec. prevent fatigue

to do:
    - automating delay of stimulus onset until 1 sec of blink-free fixation occured
    - Improve overcorrecting non-blink events (dips in blink onset)


to include in later update:
    - progressive change in cue threshold, contigent on performance in green_cue during block
    - if cue_green > .8:
        next_sd_multiplier = sd_multiplier/2




6.7.02 (6/9)
to include in later update
- progressive change in cue threshold, contigent on performance in green_cue during block
    - if cue_green > .8:
        next_sd_multiplier = sd_multiplier/2

put back
- turned off drift_correct and cue

to change

added
- include pupil and corneal keyboard commands in experimental computer
- clean up of obsolete confusing variables
- collect samples during entire 5 sec baseline
- delay cue onset until 2 sec after stimulus onset
- updated min_max to use numpy insted of python.statistics: improved speed
- added baseline pupil sizes, event label to CSV output

6.7.01 (6/6)
to include in later update
- progressive change in cue threshold, contigent on performance in green_cue during block
    - if cue_green > .8:
        next_sd_multiplier = sd_multiplier/2

to do here
- filter blink presence out of task

changes
- lower intensity of color (from .5 to .25)
- collect samples during 5 sec baseline
- delay cue onset until 2 sec after stimulus onset
- change moving average to 10 sample window
- change moving average from moving_median to moving_mean

put back
- turned off drift_correct and cue

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
expInfo = {u'Participant': u'001',u'Dominant Eye': u'Right'}
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

#eyelink-standard deviation constant
stdev_multi = .5
lblock_ps = []

# Setup the Window
win = visual.Window(size=[1920, 1080], fullscr=True, screen=0, allowGUI=True, allowStencil=False,
    monitor='Experiment', color=[-0.137,-0.137,-0.137], colorSpace='rgb',
    blendMode='avg', useFBO=True, units='pix')
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "Calibration_Verification"
Calibration_VerificationClock = core.Clock()

#eye tracking
import pylink
from _script import eyelink_display
#os
from win32api import GetSystemMetrics
import time
import re
#visual
from PIL import Image
#analysis
import pandas
import numpy as np
import csv
import itertools
import scipy.ndimage
#hardware
from psychopy.hardware import joystick
#for debugging
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import psutil

#mouse invisible
win.mouseVisible = False

#constants
trialNum = 0
blockNum = 0
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
        #gaze-timing
        self.GCWINDOW = .5 #500 msec
        self.DURATION = 2 #2000 msec
        self.gbox = 200 #gaze boundary
        self.inbox = False
        self.Finished = False     
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
        pylink.setCalibrationSounds("off", "off", "off")
        pylink.setDriftCorrectSounds("off", "off", "off")

        #Places EyeLink tracker in offline (idle) mode        
        pylink.getEYELINK().setOfflineMode()

    def blink_correction(self,lst):
        global ps_n1 #n-1 pupil sample
        global ps_old #ps without changes
        global maV #1st derivative of pupil area
        global ma_min #there are more than 3 samples
        global lma #moving average list
        global blink
        global blink_event
        win = 20 #moving average window
        #collect pupil sample, save unaltered (ps_old)
        ps = ps_old = self.pupil_sample()
          
        #if sample > 3:
        if len(lst) > 4:
            #more than enough samples
            if ma_min:
                lma = self.moving_avg(lst,win) #moving average 
                maV = lst[-1]-lst[-2] #1st derivative of pupil area (velocity)
                #if not blinking
                if blink != True:
                    #check if blink started
                    #if ps <= (.98*lst[-1]) and ps <= (.98*lma[-1]):
                    if ps <= (.94*lst[-1]) and ps <= (.94*lma[-1]):
                        blink = True #blink started
                        blink_event = 'blink_start' #debug #create variable for csv
                        return ps_n1
                    #not blinking
                    else:
                        ps_n1 = ps #update ps n-1
                        return ps
                #after blink started
                else:
                    #if pupil size has returned to pre-blinking state
                    #if ((ps <= (1.02*ps_n1)) and (ps >= (.98*ps_n1))) and (maV < 1 and maV >= -1):
                    if (ps >= (.94*ps_n1)) and (maV >= -1):
                        blink = False
                        blink_event = 'blink_end' #debug #create variable for csv
                        return ps_n1
                    else:
                        return ps_n1
            #too few samples
            else:
                #check if samples > moving average window
                if len(lst) > (win+3):
                    ma_min = True
                    ps_n1 = ps
                    return ps
                #less than 3 samples
                else:
                    ps_n1 = ps
                    return ps
        #collect inital samples
        else:
            ps_n1 = ps 
            return ps
    
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

    def close(self,spath):
        # Generate file path
        self.fpath = os.path.join(spath, self.edfname)
        
        # Close the file and transfer it to Display PC
        pylink.endRealTimeMode()
        pylink.getEYELINK().closeDataFile()
        pylink.msecDelay(50)
        pylink.getEYELINK().receiveDataFile(self.edfname, self.fpath) #copy EDF file to Display PC
        pylink.getEYELINK().close() #Close connection to tracker
  
    def gc_window(self):
        global inbox
        global GAZE
        global Fixation
        global gaze_timer
        #check for new sample update
        dt = pylink.getEYELINK().getNewestSample() 
        if(dt != None): # Gets the gaze position of the latest sample
            if eye_used == self.right_eye:
                gx,gy = dt.getRightEye().getGaze()
            else:
                gx,gy = dt.getLeftEye().getGaze()
    
        if self.xbdr[0] < gx < self.xbdr[1] and self.ybdr[0] < gy < self.ybdr[1]: #is gaze congingent fixation within the update region
            if (time.clock() - gaze_timer) > self.GCWINDOW: #if YES: compare current time and gcwindow onset against GCDURATION
                pylink.getEYELINK().sendMessage('WindowOffset')
                print('window finished = %s'%(FixationClock.getTime()))
                inbox = True
                GAZE = True #allows skipping of gc_drift()
                Fixation = False
        else:
            gaze_timer = time.clock()
    
    def gc_drift_correct(self):
        pylink.getEYELINK().sendMessage("Fixation_failed") #send failure message
        self.stop_recording()
        pylink.getEYELINK().doDriftCorrect(int(self.sc[0]), int(self.sc[1]), 0, 0)

    def min_max(self,lst):
        lps_array = np.array(lst)
        _mean = np.mean(lps_array)
        _stdev = np.std(lps_array, axis=0, ddof=1) #sample population stdev
        _max = _mean + (_stdev *stdev_multi)
        _min = _mean - (_stdev *stdev_multi)
        return _min,_max,_mean,_stdev

    def moving_avg(self,lst,window):
        lps_array = np.array(lst)  #convert to array
        cumsum = np.cumsum(lps_array,dtype=float) #running average
        ma = (cumsum[window:] - cumsum[:-window]) / window 
        return ma

    def cue_check(self,lst,win,p_min,p_max):
        #lma = self.moving_avg(lst,win) #old
        lps_array = np.array(lst)  #convert to array
        smooth = scipy.ndimage.filters.median_filter(lps_array,size=win) #median filter
        ma = smooth[-1]
        less_ = ma < p_min
        greater_ = ma > p_max
        cue_color = self.cue_display(less_,greater_,p_min,p_max)
        return cue_color
    
    def cue_display(self,less_,greater_,p_min,p_max):
        if less_: #pupil size less than SD from baseline
            if old_cue == self.blue:
                return 'blue'
            else:
                iaps_cue.setImage("blue.png")
                iaps_cue.setAutoDraw(True)
                win.flip()
                print('blue image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
                return 'blue'
        elif greater_:#pupil size greater than SD from baseline    
            if old_cue == self.red:
                return 'red'
            else:
                iaps_cue.setImage("red.png")
                iaps_cue.setAutoDraw(True)
                win.flip()
                print('red image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))              
                return 'red'
        else: #pupil size within SD from baseline
            if old_cue == self.green:
                return 'green'
            else:
                iaps_cue.setImage("green.png")
                iaps_cue.setAutoDraw(True)
                win.flip()
                print('green image, moving_avg=%s, min=%s, max=%s'%(p_ma,p_min,p_max))
                return 'green'
    
    def prepare_append(self,event,ps_o,ps_n):
        if baseline:
            #timing
            pp_t = FixationClock.getTime()#psychopy time
            
            #creating variables for cross-validation
            levent.append(event_type)
            lblock.append(blockNum)
            ltrial.append(trialNum)
            lpp_t.append(pp_t) #psychopy time      
            lpb_uadj.append(ps_o)#unadjusted pupil size
            lpb_d.append(maV)#pupil size velocity
            lpb.append(ps_n)#adjusted pupil size
            
            #dummy variables
            #ltt.append(blank_event)#tracker time
            cpu_pc.append(blank_event)#cpu
            ram_pc.append(blank_event)#ram
            lps_min.append(blank_event)#neg stdev from baseline mean
            lps_mean.append(blank_event)#baseline mean
            lps_max.append(blank_event)#pos stdev from baseline mean
            lf_min.append(blank_event)#neg stdev from baseline mean
            lf_mean.append(blank_event)#baseline mean
            lf_max.append(blank_event)#pos stdev from baseline mean
            lb_min.append(blank_event)#neg stdev from baseline mean
            lb_mean.append(blank_event)#baseline mean
            lb_max.append(blank_event)#pos stdev from baseline mean
            lcue.append(blank_event) #cue color
            lblink.append(blank_event) #debug
            lmood.append(blank_event) #stimulus valience
            lstim.append(blank_event) #stimulus name
        else:
            #timing
            #tt = eyelink.t_tracker()#tracker time
            pp_t = event.getTime()#psychopy time
            
            #creating variables for cross-validation
            lblock.append(blockNum)#block
            ltrial.append(trialNum)#trial
            levent.append(event_type)#baseline or stimulus
            lpp_t.append(pp_t)#psychopy time
            cpu_pc.append(cpu_s)#cpu
            ram_pc.append(ram_s)#ram
            
            #baseline
            if blockNum == 1:
                #block baseline
                lb_min.append(blank_event)#neg stdev from baseline mean
                lb_mean.append(blank_event)#baseline mean
                lb_max.append(blank_event)#pos stdev from baseline mean
            else:
                #block baseline
                lb_min.append(b_min)#neg stdev from baseline mean
                lb_mean.append(b_mean)#baseline mean
                lb_max.append(b_max)#pos stdev from baseline mean
                
            #fixation baseline            
            lf_min.append(f_min)#neg stdev from baseline mean
            lf_mean.append(f_mean)#baseline mean
            lf_max.append(f_max)#pos stdev from baseline mean
            #adjusted baseline
            lps_min.append(ps_min)#neg stdev from baseline mean
            lps_mean.append(ps_mean)#baseline mean
            lps_max.append(ps_max)#pos stdev from baseline mean
            
            lps_uadj.append(ps_o)#unadjusted pupil size
            lps_d.append(maV)#pupil size velocity
            lps.append(ps_n)#adjusted pupil size
            lcue.append(old_cue) #cue color
            lblink.append(blink_event) #debug
            lmood.append(valence) #stimulus valience
            lstim.append(scenestim) #stimulus name
                
    def prepare_constants(self, event, stim_offset, blank_offset):
        blank_event='nan'#dummy value
        blink_event = 'nan' #debug #dummy value for blink onset/offset
        event_type=event #stimulus event label
        old_cue = 'nan' #dummy values for time before first cue presentation
        p_ma = 'nan' #dummy value for moving average
        ps_n1 = 0 #n-1 pupil size
        st0=0 #time between samples (st1-st0)
        ct0=0 #time between cues (ct1-ct0)
        maV=0 #velocity
        stimulus_offset = stim_offset #time (sec)
        blank_offset = blank_offset #time (sec)
        Total_Samples_old=0 #no. of samples
        return blink_event, event_type, old_cue,\
        p_ma, ps_n1, st0, ct0, maV, stimulus_offset,\
        blank_offset, Total_Samples_old,blank_event
        
    def prepare_bool(self,baseline_):
        first_loop = True # is first pupil sample
        Window = True #window to collect samples
        baseline = baseline_ #end of baseline samples
        blink = False #blink occuring
        ma_min = False #less than 3 samples for moving average
        Cue = True #present cue
        Event_draw = False #marks the zero-time in a trial
        return first_loop, Window, baseline, blink, ma_min,\
        Cue, Event_draw

    def prepare_lists(self):
        lblink=[] #list of blink events
        levent=[] #list of event types (baseline,trial)
        lb_max=[]#list of pupil baseline max (block baseline)
        lb_min=[]#list of pupil baseline min (block baseline)
        lb_mean=[]#list of pupil baseline mean (block baseline)
        lf_max=[]#list of pupil baseline max (fixation baseline)
        lf_min=[]#list of pupil baseline min (fixation baseline)
        lf_mean=[]#list of pupil baseline mean (fixation baseline)
        lps_max=[]#list of pupil baseline max (adjusted baseline)
        lps_min=[]#list of pupil baseline min (adjusted baseline)
        lps_mean=[]#list of pupil baseline mean (adjusted baseline)
        lps_uadj=[] #list of unadjusted pupil samples 
        lps=[]#list of adjusted pupil samples
        lps_d=[] #change in ps
        lcue=[] #list of cue colors
        lpp_t=[]#time stamp of each cue onset (psychopy)
        ltrial=[]#list of trials at each cue
        lblock=[]#list of trials at each cue
        cpu_pc=[]#list of cpu usage, by %
        ram_pc=[]#list of ram usage, by %
        lstim=[] #stimulus
        lmood=[] #valience
        return lblink, levent,\
        lb_max, lb_min, lb_mean,\
        lf_max, lf_min, lf_mean,\
        lps_max, lps_min, lps_mean,\
        lps_uadj, lps, lps_d, lcue, lpp_t, ltrial, lblock,\
        cpu_pc, ram_pc, lstim, lmood

    def pupil_sample(self):
        #check for new sample update
        s = pylink.getEYELINK().getNewestSample() # check for new sample update
        if(s != None): # Gets the gaze position of the latest sample
            #pupil area
            if eye_used == self.right_eye:
                ps = s.getRightEye().getPupilSize()
            else:
                ps = s.getLeftEye().getPupilSize()
            return ps

    def save_csv(self,old_,vel_,new_,time_):
        global header      
        if baseline:        
            #outputting baseline to csv
            #reverse time
            time_.reverse()
            time_ = [ -x for x in time_]
        
        with open('_data\gaze\%s.csv'%(subno), 'a') as cross_val:
            writer = csv.writer(cross_val,lineterminator='\n')
            if header:
                s_header=["block","trial","event","valence","stimulus",
                          "psychopy_timestamp","cpu","ram",
                          "block_baseline_min","block_baseline_mean","block_baseline_max",
                          "fixation_baseline_min","fixation_baseline_mean","fixation_baseline_max",
                          "stimulus_baseline_min","stimulus_baseline_mean","stimulus_baseline_max",
                          "old_pupil_sample","pupil_velocity","new_pupil_sample","feedback","blink"]
                writer.writerow(s_header)
                header=False
            writer.writerows(itertools.izip(lblock,ltrial,levent,lmood,lstim,
                                            time_,cpu_pc,ram_pc,
                                            lb_min,lb_mean,lb_max,                                            
                                            lf_min,lf_mean,lf_max,
                                            lps_min,lps_mean,lps_max,
                                            old_,vel_,new_,lcue,lblink))

    def set_eye_used(self, eye):
        eye_entered = str(eye)
        if eye_entered in ('Left','LEFT','left','l','L'):
            eye_used = self.left_eye
        else:
            eye_used = self.right_eye
        return eye_used
            
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
        pylink.getEYELINK().sendCommand("record_status_message 'Trial %s Block %s Image %s'" %(trialNum,blockNum,scenestim)) #send message to Eyelink viewer
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

    def t_cue(self,c1,c0): #create new cue only if more than 250 msec has gone by since old cue
        cu = (c1 - c0) >= 0.005
        return cu

    def t_sample(self,s_1,s_0):  #collect new sample only if more than 2 msec has gone by since old sample (Eyelink-500Hz)
        su = (s_1 - s_0) >= .002
        return su

    def t_tracker(self):
        #Returns the current tracker time (in milliseconds) since the tracker application started
        tt = pylink.getEYELINK().trackerTimeUsec()
        return tt
        
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
    color=[1,1,1], colorSpace='rgb', opacity=.25,
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

#eye used
eye_used = eyelink.set_eye_used()

# Calibrate eyetracker
DC = 0
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
    
    #updating per block
    blockNum = blockNum + 1 #block count
    if blockNum == 2:
        b_min,b_max,b_mean,b_stdev = eyelink.min_max(lblock_ps)
    
    for thisTrial_Loop in Trial_Loop:
        currentLoop = Trial_Loop
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_Loop.rgb)
        if thisTrial_Loop != None:
            for paramName in thisTrial_Loop.keys():
                exec(paramName + '= thisTrial_Loop.' + paramName)
        
        #------Prepare to start Routine "Fixation"-------
        #eyelink-initalize per block
        trialNum = trialNum + 1 #trial count
        DC = 0 #force calibration if drift correct is failed 3 times in a row

        Fixation = True #Fixation event
        while Fixation:
            #constants
            blink_event, event_type, old_cue, p_ma,\
            ps_n1, st0, ct0, maV, stimulus_offset,\
            blank_offset, Total_Samples_old,\
            blank_event = eyelink.prepare_constants('baseline',None,None)
            
            #boolean
            first_loop, Window, baseline, blink, ma_min, Cue,\
            Event_draw = eyelink.prepare_bool(True)
            
            #lists
            lblink, levent,\
            lb_max, lb_min, lb_mean,\
            lf_max, lf_min, lf_mean,\
            lps_max, lps_min, lps_mean,\
            lpb_uadj, lpb, lpb_d, lcue, lpp_t, ltrial,\
            lblock, cpu_pc, ram_pc, lstim, lmood = eyelink.prepare_lists()           
            
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
            # *fixation_cross* updates
            fixation_cross.setAutoDraw(True)
            win.flip()

            # update/draw components on each frame
            while Window:
                if FixationClock.getTime() >= 2:
                    fixation_cross.setAutoDraw(False)
                    break
                else:
                    st1 = FixationClock.getTime()
                    #if at least 2msec between samples
                    if eyelink.t_sample(st1,st0):
                        #if gaze window not achived                        
                        if inbox != True: 
                            # eyelink-gaze contingent function
                            eyelink.gc_window()   
                            #eyelink-pupil size
                            ps_old = eyelink.pupil_sample()
                        st0 = st1
                        eyelink.prepare_append(FixationClock,ps_old,blank_event)
                
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            #if gc failed              
            if GAZE != True:
                if DC >=2:#if drift correct failed twice run calibration
                    eyelink.calibrate()
                    DC = 0 #reset counter
                else: # drift correct
                    eyelink.gc_drift_correct()
                    DC = DC + 1 #add counter
        
            #blink detection 
            #collect fixation baseline min max mean and stdev        
            f_min,f_max,f_mean,f_stdev = eyelink.min_max(lpb_uadj)
            
            #if blink detected
            ##check if any pupil size during gc window was less than 75% of baseline mean
            blink_threshold = (.75*f_mean)
            low_pupil = min(float(s) for s in lpb_uadj)
            if low_pupil < blink_threshold: 
                Fixation = True #if so, restart fixation 

        #outputting baseline to csv
        eyelink.save_csv(lpb_uadj,lpb_d,lpb,lpp_t)
        
        #Fixation Finished------------
        #if first block
        if blockNum == 1:
            ps_min = f_min
            ps_mean = f_mean
            ps_max = f_max           
        else:
            ps_min = f_mean - (b_stdev *stdev_multi)
            ps_mean = f_mean
            ps_max = f_mean + (b_stdev *stdev_multi)
            print('block: mean = %s, block min = %s, max = %s'%(b_mean, b_min, b_max))
            print('fixation: mean = %s, min = %s, max = %s'%(f_mean, f_min, f_max))
            print('threshold: mean = %s, min = %s, max = %s'%(ps_mean, ps_min, ps_max))
        
        #------Prepare to start Routine "IAPS"-------
        with PyCallGraph(output=GraphvizOutput()):
            t = 0
            IAPSClock.reset()  # clock 
            frameN = -1

            #constants
            #stimulus and ITI duration
            # if block 2-4
            if blockNum == 1:
                stim_offset = 5
                iti_offset = 7
            #else if block 1
            else:
                stim_offset = 10
                iti_offset = 12
            
            blink_event, event_type, old_cue, p_ma,\
            ps_n1, st0, ct0, maV, stimulus_offset,\
            blank_offset, Total_Samples_old,\
            blank_event = eyelink.prepare_constants('stimulus',stim_offset,iti_offset) #stim offset, blank offset
            
            #functions
            cpu_s = psutil.cpu_percent(interval=None)
            ram_s = psutil.virtual_memory().percent

            #boolean
            first_loop, Window, baseline, blink, ma_min,\
            Cue, Event_draw = eyelink.prepare_bool(False)
            
            #lists
            lblink, levent,\
            lb_max, lb_min, lb_mean,\
            lf_max, lf_min, lf_mean,\
            lps_max, lps_min, lps_mean,\
            lps_uadj, lps, lps_d, lcue, lpp_t, ltrial,\
            lblock, cpu_pc, ram_pc, lstim, lmood = eyelink.prepare_lists()   
     
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
            while continueRoutine and IAPSClock.getTime() < blank_offset:
                # get current time
                t = IAPSClock.getTime()
                
                # *iaps_display* updates
                if t >= 0 and iaps_display.status == NOT_STARTED:
                    iaps_display.setAutoDraw(True)
                    win.flip()
                    pylink.getEYELINK().sendMessage('IAPS Onset')

                #eyelink-pupil dilation sampling
                if IAPSClock.getTime() >= 0 and iaps_display.status == STARTED: #collect samples 5ms after stimulus onset
                    while Window:
                        st1 = IAPSClock.getTime()
                        ct1 = IAPSClock.getTime()
                        #if Block 1
                        if blockNum == 1:
                            #if ps_1 time - ps_n1 time > 2 msec
                            if eyelink.t_sample(st1,st0):
                                ps_new = eyelink.blink_correction(lps_uadj)
                                st0 = st1
                                eyelink.prepare_append(IAPSClock,ps_old,ps_new)                    
                            #if time = stimulus offset
                            if IAPSClock.getTime() >= stimulus_offset:
                                iaps_display.setAutoDraw(False)
                                break
                        #if Block 2-4                        
                        else:
                            #if ps_1 time - ps_n1 time > 2 msec
                            if eyelink.t_sample(st1,st0):                      
                                ps_new = eyelink.blink_correction(lps_uadj)
                                st0 = st1
                                eyelink.prepare_append(IAPSClock,ps_old,ps_new)
                            #present Feedback
                            if IAPSClock.getTime() >= 2:
                                old_cue = eyelink.cue_check(lps,20,ps_min,ps_max)
                            #End Stimulus presentation
                            #if time = stimulus offset                   
                            if IAPSClock.getTime() >= stimulus_offset:
                                iaps_display.setAutoDraw(False)
                                iaps_cue.setAutoDraw(False)
                                break
                
                # *blank* updates
                if t >= stimulus_offset and blank.status == NOT_STARTED:
                    blank.setAutoDraw(True)
                    pylink.getEYELINK().sendMessage('Blank Onset')
                if blank.status == STARTED and t >= blank_offset: #most of one frame period left
                    blank.setAutoDraw(False)
                
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
        #creating csv file
        eyelink.save_csv(lps_uadj,lps_d,lps,lpp_t)

        #end of trial message
        pylink.getEYELINK().sendMessage('Ending Recording')
        
        #The IMGLOAD command is used to show an overlay image in Data Viewer.  This will code the time that the PictureTrial image should appear.
        pylink.getEYELINK().sendMessage("!V IMGLOAD CENTER  %s" %(scenestim))
        
        #stop recording
        eyelink.stop_recording()
        
        #VARIABLES
        msg = "!V TRIAL_VAR picture %s" %(BlackWhite) #scenestim
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
                
        if trialNum <5:
            #concatinate lblock_ps with trial information
            lblock_ps.extend(lps)
            
            #print results of block
            if trialNum ==1:
                trial_1 = len(lblock_ps)
            if trialNum ==2:
                trial_2 = len(lblock_ps) - trial_1
            if trialNum ==3:
                trial_3 = len(lblock_ps) - (trial_1+trial_2)
            if trialNum ==4:
                trial_4 = len(lblock_ps) - (trial_1+trial_2+trial_3)
                
            if trialNum ==4:
                print(lblock_ps)
                print('total_samples = %s' %(len(lblock_ps)))
                print('trial_1 = %s,%s' %(trial_1,(len(lps))))
                print('trial_2 = %s,%s' %(trial_2,(len(lps))))
                print('trial_3 = %s,%s' %(trial_3,(len(lps))))
                print('trial_4 = %s,%s' %(trial_4,(len(lps))))
            
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

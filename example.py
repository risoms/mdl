#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
# Created on Wed Feb 13 15:37:43 2019
# @author: Semeon Risom
# @email: semeon.risom@gmail.com.
# Sample code to run SR Research Eyelink eyetracking system. Code is optimized for the Eyelink 1000 
# Plus (5.0), but should be compatiable with earlier systems.
# %%
# To Do:
# Finish eyetracking.drift_correction()
# Finish eyetracking.roi()
# %%
# import
from psychopy import visual, core
import mdl
# %%
# Initialize the Eyelink.
# Before initializing, ensure psychopy window instance has been created in the experiment file. 
# This window will be used in the calibration function.
#
# ```psychopy.visual.window.Window``` instance (for demonstration purposes only)
window = visual.Window(size=[1920, 1080], fullscr=False, screen=0, allowGUI=True, units='pix',
                       monitor='Monitor', winType='pyglet', color=[110,110,110], colorSpace='rgb255')
subject = 1
eyetracking = mdl.eyetracking(libraries=False, window=window, subject=subject)
# %%
# Setting the dominant eye. This step is especially critical for transmitting gaze coordinates from Eyelink->Psychopy.
#
dominant_eye = 'left'
eye_used = eyetracking.set_eye_used(eye=dominant_eye)
# %%
# Start calibration.
# Before running the calibration, ensure psychopy window instance has been created in the experiment file. 
# This window will be used in the calibration function.
#
# ```psychopy.visual.window.Window``` instance (for demonstration purposes only)
# start
eyetracking.calibration()
# %%
# Enter the key "o" on the ```psychopy.visual.window.Window``` instance. This will begin the task. 
# The Calibration, Validation, 'task-start' events are controlled by the keyboard.
# Calibration ("c"), Validation ("v"), task-start ("o") respectively.
# %%
# (Optional) Print message to console/terminal. This may be useful for debugging issues.
eyetracking.console(c="green", msg="eyetracking.calibration() started")
# %%
# Drift correction. This can be done at any point after calibration, including after 
# eyetracking.start_recording has started. #!! To do. Finish.
#
attempt = 1
eyetracking.drift_correction(window=window, attempt=attempt, limit=999, core=core, thisExp=None)
# %%
# Region of interest. This is used for realtime data collection from eyelink->psychopy.
# For example, this can be used to require participant to look at the fixation cross for a duration
# of 500 msec before continuing the task.
# 
# Using the eyetracking.roi function to collect samples with the center of the screen.
roi = dict(center=[860,1060,640,440])
# start
eyetracking.roi(window=window, region=roi)
# %%
# Start recording. This should be run at the start of the trial. 
# Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
eyetracking.start_recording(trial=1, block=1)
# %%
# Collect current gaze coordinates from Eyelink (only if needed in experiment). This command should be 
# looped at an interval of sample/2.01 msec to prevent oversampling (500Hz).
#
# get time
import time
s1 = 0 # set current time to 0
lgxy = [] # create list of gaze coordinates (demonstration purposes only)
s0 = time.clock() # initial timestamp
# repeat
while True:
    # if difference between starting and current time is greater than > 2.01 msec, collect new sample
    if (s1 - s0) >= .00201:
        gxy = eyetracking.sample(eye_used=eye_used) # get gaze coordinates
        lgxy.append(gxy) # store in list
        s0 = time.clock() # update starting time
    #else set current time
    else: 
        s1 = time.clock()

    #break `while` statement if list of gaze coordiantes >= 20 (demonstration purposes only)
    if len(lgxy) >= 20: break
# %%
# Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
# Sending message "stimulus onset".
msg = "stimulus onset"
eyetracking.send_message(msg=msg)
# %%
# Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
# Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
#
# set variables
variables = dict(stimulus='001B_F.jpg', trial_type='encoding', race="black")
# stop recording
eyetracking.stop_recording(trial=1, block=1, variables=variables)
# %%
# Finish Eyelink recording.
eyetracking.finish_recording()
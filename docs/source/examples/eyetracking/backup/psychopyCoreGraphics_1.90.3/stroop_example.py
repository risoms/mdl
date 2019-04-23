# Copyright (C) 2018 Zhiguo Wang

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version. 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details. 
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# IMPORTANT: If you use a screen units other than 'pix', please bear in mind
# that the drift-correction target position needs to be specified in screen
# pixel coordinates, and the gaze coordinates returned by pylink are also in
# screen pixels, with the top-left corner of the screen as the origin (0,0).

# Import libraries
import os, random, numpy, pylink
from psychopy import visual, core, event, monitors
# import the custom calibrarion/validation routine for Psychopy
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy 

# Set a few task parameters
useGUI = True # whether use the Psychopy GUI module to collect subject information
dummyMode = False # Simulated connection to the tracker; press ESCAPE to skip calibration/validataion

# STEP I: get subject info
expInfo = {'SubjectNO':'00', 'SubjectInitials':'TEST'}

if useGUI:
    from psychopy import gui
    dlg = gui.DlgFromDict(dictionary=expInfo, title="Stroop Example", order=['SubjectNO', 'SubjectInitials'])
    if dlg.OK == False: core.quit()  # user pressed cancel
else:
    expInfo['SubjectNO'] = raw_input('Subject # (1-99): ')
    expInfo['SubjectInitials'] = raw_input('Subject Initials (e.g., WZ): ')

#### SETP II: established a link to the tracker
if not dummyMode: 
    tk = pylink.EyeLink('100.1.1.1')
else:
    tk = pylink.EyeLink(None)

# STEP III: Open an EDF data file to save the eye movement data
# This needs to be done early, so as to record all user interactions with the tracker
# File name cannot exceed 8 characters
edfFileName = '%s_%s' %(expInfo['SubjectNO'], expInfo['SubjectInitials'])+'.EDF' 
tk.openDataFile(edfFileName)
tk.sendCommand("add_file_preamble_text 'Psychopy Stroop Example'")

# STEP IV: Initialize custom graphics for camera setup & drift correction
scnWidth, scnHeight = (1920, 1080) 

# initialize a monitor object to inform Psychopy the viewing distance, monitor gamma, etc.
mon = monitors.Monitor('myMon', width=32.0, distance=57.0)
mon.setSizePix((scnWidth, scnHeight))

# for the custom calibration/validation routine to work properly, we recommend setting screen units to "pix"
win = visual.Window(size=(scnWidth, scnHeight), fullscr=True, monitor=mon, color='black', units='pix')

# Initialize the graphics for calibration/validation
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# STEP V: Set up the tracker
# we need to put the tracker in offline mode before we change its configrations
tk.setOfflineMode()

# sampling rate, 250, 500, 1000, or 2000; this command won't work for EyeLInk II/I
tk.sendCommand('sample_rate 500')

# inform the tracker the resolution of the subject display
# [see Eyelink Installation Guide, Section 8.4: Customizing Your PHYSICAL.INI Settings ]
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# save display resolution in EDF data file for Data Viewer integration purposes
# [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical), 
tk.sendCommand("calibration_type = HV9") # tk.setCalibrationType('HV9') also works, see the Pylink manual

# specify the proportion of subject display to calibrate/validate (OPTIONAL, useful for wide screen monitors)
#tk.sendCommand("calibration_area_proportion 0.85 0.83")
#tk.sendCommand("validation_area_proportion  0.85 0.83")

# Using a button from the EyeLink Host PC gamepad to accept calibration/dirft check target (optional)
# tk.sendCommand("button_function 5 'accept_target_fixation'")

# the model of the tracker, 1-EyeLink I, 2-EyeLink II, 3-Newer models (100/1000Plus/DUO)
eyelinkVer = tk.getTrackerVersion()

#turn off scenelink camera stuff (EyeLink II/I only)
if eyelinkVer == 2: tk.sendCommand("scene_camera_gazemap = NO")

# Set the tracker to parse Events using "GAZE" (or "HREF") data
tk.sendCommand("recording_parse_type = GAZE")

# Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
# the Parser for EyeLink I is more conservative, see below
# [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
if eyelinkVer>=2: tk.sendCommand('select_parser_configuration 0')

# get Host tracking software version
hostVer = 0
if eyelinkVer == 3:
    tvstr  = tk.getTrackerVersionString()
    vindex = tvstr.find("EYELINK CL")
    hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

# specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
# See Section 4 Data Files of the EyeLink user manual
tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
if hostVer>=4: 
    tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
    tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
else:          
    tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")
    tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")

# STEP VI: specify all possible experimental cells
# one may read in s spreadsheet that defines the experimentl cells; usually, a simple list-like the one below
# should also do the job; if we need tweenty trials, simple go with "new_list = trials[:]*10", then 
# random.shuffle(new_list) 
# store the experimental cells in a list will make our life easier and our code more concise
# the columns are 'text', 'textColor', 'correctAnswer' and "congruency"
myTrials = [['red',   'red',   'left',  'cong'],
            ['red',   'green', 'down',  'incg'],
            ['green', 'green', 'down',  'cong'],
            ['green', 'blue',  'right', 'incg'],
            ['blue',  'blue',  'right', 'cong'],
            ['blue',  'red',   'left',  'incg']]

# SETP VII: a helper to run a single trial
def runTrial(params, expInfo):
    """ 
    pars should be a list, like ['red',   'red',   'left',  'cong']
    dataFile is an opened csv file that use to store our data in a sheet.
    """
    # unpacking the parameters
    text, textColor, correctAnswer, congruency = params
    
    # prepare the stimuli
    word = visual.TextStim(win=win, text= text, font='Arial', height=100.0, color=textColor)
    w,h = word.boundingBox

    # flush cached button presses (eyelink) 
    tk.flushKeybuttons(0)
    tk.setOfflineMode()
    pylink.msecDelay(50)
    
    # OPTIONAL-- draw the text on the Host screen and show the bounding box
    tk.sendCommand('clear_screen 0') # clear the host Display first
    tk.sendCommand('draw_text %d %d 6 %s' % (scnWidth/2, scnHeight/2, text))
    tk.sendCommand('draw_box %d %d %d %d 6' % (scnWidth/2-w/2, scnHeight/2-h/2, scnWidth/2+w/2, scnHeight/2+h/2))
    
    # log trial onset message
    tk.sendMessage("TRIALID %s %s %s"%(text, textColor, congruency))

    # record_status_message : show some info on the host PC
    tk.sendCommand("record_status_message 'congruency: %s'"% congruency)

    #Optional - start realtime mode
    pylink.beginRealTimeMode(100)
    
    # do driftcheck
    try:
        error = tk.doDriftCorrect(scnWidth/2,scnHeight/2,1,1)
    except:
        tk.doTrackerSetup()

    # start recording, parameters specify whether events and samples are
    # stored in file, and available over the link
    tk.startRecording(1, 1, 1, 1)
    pylink.msecDelay(50)

    # Clear bufferred events (in Psychopy)
    event.clearEvents(eventType='keyboard')

    # draw the target word on display
    word.draw()
    win.flip()
    tk.sendMessage("SYNCTIME") # message to mark the onset of visual stimuli
    
    # save a screenshot so we can use it in Data Viewer to superimpose the gaze
    if not os.path.exists('screenshotFolder'): os.mkdir('screenshotFolder')
    screenshot = 'screenshotFolder' + os.sep +'cond_%s_%s.jpg' % (text, textColor)
    win.getMovieFrame()
    win.saveMovieFrames(screenshot)
    
    # send a Data Viewer integration message here, so DV knows which screenshot to load
    tk.sendMessage('!V IMGLOAD FILL %s' % ('..' + os.sep + screenshot))

    # check for response & time out
    gotKey  = False
    timeOut = False
    tStart  = core.getTime()
    subjResp= ['None', 'None']
    while not (gotKey or timeOut):
        # check for time out
        tNow = core.getTime()
        if tNow - tStart >= 10.0: timeOut = True
        
        # check for key presses
        keyPressed = event.getKeys(['left','right','down', 'escape'])
        if len(keyPressed) > 0:
            if 'escape' in keyPressed:
                tk.sendMessage("Quit")
                win.close(); core.quit() # terminate the task if ESCAPE is pressed
            else:
                subjResp = [keyPressed[0], tNow]
                tk.sendMessage("RESPONSE %s"%(keyPressed[0]))
                gotKey = True

    # clear the subject display
    win.color='black'
    win.flip()
    # clear the host Display 
    tk.sendCommand('clear_screen 0') 

    # was the subject's response 'correct'?
    if subjResp[0] == correctAnswer:
        respAcc = 1
    else:
        respAcc = 0
        
    # OPTIONAL-- set an Interest Area for data viewer integraiton
    # a full list of Data Viewer integration messages and their syntax can be found in the Data Viewer Manual 
    # (Help menu -> Contents -> Protocol for EyeLink Data To Viewer Integraiton).
    tk.sendMessage("!V IAREA RECTANGLE 1 %d %d %d %d target" % (scnWidth/2-w/2, scnHeight/2-h/2, scnWidth/2+w/2, scnHeight/2+h/2))

    # EyeLink - Send Trialvar messages for data viewer integraiton
    # a full list of Data Viewer integration messages and their syntax can be found in the Data Viewer Manual 
    # (Help menu -> Contents -> Protocol for EyeLink Data To Viewer Integraiton).
    tk.sendMessage("!V TRIAL_VAR word %s" % (text))
    tk.sendMessage("!V TRIAL_VAR color %s" % (textColor))
    tk.sendMessage("!V TRIAL_VAR congruency %s" % (congruency))
    tk.sendMessage("!V TRIAL_VAR respAcc %d" % (respAcc))
      
    # Optional-- end realtime mode
    pylink.endRealTimeMode()
    pylink.msecDelay(100)

    # send a message to mark the end of trial
    tk.sendMessage("TRIAL_RESULT %d" % (respAcc))
    pylink.msecDelay(100)
    
    # EyeLink - stop recording eye data
    tk.stopRecording()
    pylink.msecDelay(50)
    tk.setOfflineMode()

# STEP VIII: The real experiment starts here

# Task instructions
instrText = visual.TextStim(win, text='Remember, ignore the word itself; press:\nLeft for red LETTERS\nDown for green LETTERS\nRight for blue LETTERS\n(Esc will quit)\n\nPress any key to continue', color='white')
instrText.draw()
win.flip()
event.waitKeys()

# Calibrate the camera
calInstruct = visual.TextStim(win, text='Press ENTER twice to calibrate the tracker', color='white')
calInstruct.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()

# here we will test a block of trials
trials2Test = myTrials[:]*1
random.shuffle(trials2Test)

for trial in trials2Test:
    runTrial(trial, expInfo)

# close EDF data File
tk.closeDataFile()

# EyeLink - copy EDF file to Display PC and put it in local folder ('edfData')
edfTransfer = visual.TextStim(win, text='EDF data is transfering from EyeLink Host PC, please wait...', color='white')
edfTransfer.draw()
win.flip()

if not os.path.exists('edfData'): os.mkdir('edfData')
tk.receiveDataFile(edfFileName, os.getcwd() + os.sep + 'edfData' + os.sep + edfFileName)

# EyeLink - Close connection to tracker
tk.close()

# make sure everything is closed down
win.close()
core.quit()

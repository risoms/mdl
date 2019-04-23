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

# import libraries
import pylink, numpy, os, random
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors
from PIL import Image

# Set a few task parameters
useGUI = True  #  use the Psychopy GUI module to collect subject information
dummyMode = False # Simulated connection to the tracker; press ESCAPE to skip calibration/validataion

# STEP I: get subject info
expInfo = {'SubjectNO':'00', 'SubjectInitials':'TEST'}

if useGUI:
    from psychopy import gui
    dlg = gui.DlgFromDict(dictionary=expInfo, title="GC Example", order=['SubjectNO', 'SubjectInitials'])
    if dlg.OK == False: core.quit()  # user pressed cancel
else:
    expInfo['SubjectNO'] = raw_input('Subject # (1-99): ')
    expInfo['SubjectInitials'] = raw_input('Subject Initials (e.g., WZ): ')

# SETP II: established a link to the tracker
if not dummyMode: 
    tk = pylink.EyeLink('100.1.1.1')
else:
    tk = pylink.EyeLink(None)

# STEP III: Open an EDF data file EARLY
# Note that the file name cannot exceeds 8 characters
# please open eyelink data files early to record as much info as possible
dataFolder = os.getcwd() + '/edfData/'
if not os.path.exists(dataFolder): os.makedirs(dataFolder)
dataFileName = expInfo['SubjectNO'] + '_' + expInfo['SubjectInitials'] + '.EDF'
tk.openDataFile(dataFileName)
# add personalized data file header (preamble text)
tk.sendCommand("add_file_preamble_text 'Psychopy GC demo'") 

# STEP IV: Initialize custom graphics for camera setup & drift correction
scnWidth, scnHeight = (1920, 1080)

# you MUST specify the physical properties of your monitor first, otherwise you won't be able to properly use
# different screen "units" in psychopy. One may define his/her monitor object within the GUI, but
# I find it is a better practice to put things all under control in the experimental script instead.
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
mon.setSizePix((scnWidth, scnHeight))
win = visual.Window((scnWidth, scnHeight), fullscr=True, monitor=mon, color=[0,0,0], units='pix', allowStencil=True,autoLog=False)

# call the custom calibration routine "EyeLinkCoreGraphicsPsychopy.py", instead of the default
# routines that were implemented in SDL
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

# STEP VI: specify all possible experimental cells & prepare the visual stimuli
# one may read in a spreadsheet containing all the experimentl cells; usually, a simple list
# should also do the job; if we need tweenty trials, simple go with "new_list = trials[:]*10", then 
# random.shuffle(new_list) 

trials = [['mask',   'sacrmeto.jpg'],
          ['window', 'sacrmeto.jpg']]

# prepare a circular aperture as a gaze-contingent window
gazeWindow = visual.Aperture(win, size=200)
gazeWindow.enabled=False
# prepare a gaze-contingent mask
gazeMask = visual.GratingStim(win, tex='none', mask='circle', size=200, color=[1.0,1.0,1.0])

# SETP VII: a couple of helpers
def runTrial(pars):
    """ pars corresponds to a row in the trial list"""
    
    # retrieve paramters from the trial list, in the "mask" condition we simply draw mask
    #at the current gaze position
    # in the window' condition we show a moving window that is contingent on gaze
    cond, pic = pars
    
    # load the image to display
    img = visual.ImageStim(win, image=pic, size=(scnWidth, scnHeight)) # stretch the image to fill full screen

    # backdroping the image to the Host screen (optional, SLOW and may cause timing problems for some, e.g., MRI tasks)
    # here we use the list comprehension method of Python to convert the RGB values of all pixels into a format
    # that is recognizable by the Host PC, i.e., pixels = [line1, ...lineN], line = [pix1...pixN], pix=(R,G,B)
    #im = Image.open(pic)
    #im = im.resize((scnWidth, scnHeight))
    #w,h = (scnWidth, scnHeight)
    #pixels = im.load()
    #pixels_2transfer = [[pixels[i,j] for i in range(w)] for j in range(h)]
    #tk.sendCommand('clear_screen 0') # clear the host screen
    #tk.bitmapBackdrop(w, h, pixels_2transfer, 0, 0, w, h, 0, 0, pylink.BX_MAXCONTRAST)
    
    # take the tracker offline
    tk.setOfflineMode()
    pylink.pumpDelay(50)

    # send the standard "TRIALID" message to mark the start of a trial
    # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
    tk.sendMessage('TRIALID')
    
    # record_status_message : show some info on the host PC
    tk.sendCommand("record_status_message 'Task: %s'"% cond)
    
    # drift check
    try:
        err = tk.doDriftCorrect(scnWidth/2, scnHeight/2,1,1)
    except:
        tk.doTrackerSetup()
        
    # uncomment this line to read out calibration/drift-correction results
    #print tk.getCalibrationMessage() 

    # start recording, parameters specify whether events and samples are
    # stored in file, and available over the link
    error = tk.startRecording(1,1,1,1)
    pylink.pumpDelay(100) # wait for 100 ms to make sure data of interest is recorded
    
    #determine which eye(s) are available
    eyeTracked = tk.eyeAvailable() 
    if eyeTracked==2: eyeTracked = 1

    # enable the gaze-contingent aperture in the 'window' condition
    if cond=='window': gazeWindow.enabled = True
    else:              gazeWindow.enabled = False
    
    # show the image 
    img.draw()  
    win.flip()
    
    # this message marks the onset of the stimulus
    # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
    tk.sendMessage('image_onset') 
    
    # Message to specify where the image is stored relative to the EDF data file, please see the 
    # "Protocol for EyeLink Data to Data Viewer Integration -> Image" section of the Data Viewer manual
    tk.sendMessage('!V IMGLOAD FILL %s' % ('..'+ os.sep +pic))
    
    # show the image indefinitely until a key is pressed
    gazePos =  (scnWidth/2, scnHeight/2)
    terminate = False
    event.clearEvents() # clear cached (keyboard/mouse etc.) events, if there is any
    while not terminate:
        # check for keypress to terminate a trial
        if len(event.getKeys())>0: # KEYBOARD
            terminate = True
            
        if True in tk.getLastButtonPress(): # GamePad connected to the tracker HOST PC
            terminate = True
           
        # check for new samples
        dt = tk.getNewestSample()
        if (dt != None):
            if eyeTracked == 1 and dt.isRightSample():
                gazePos = dt.getRightEye().getGaze()
            elif eyeTracked == 0 and dt.isLeftSample():
                gazePos = dt.getLeftEye().getGaze()

        # redraw background image
        img.draw()
        # gaze-contingent window/mask
        if cond=='window':
            gazeWindow.pos = (gazePos[0]-scnWidth/2, scnHeight/2-gazePos[1])
        else:
            gazeMask.pos = (gazePos[0]-scnWidth/2, scnHeight/2-gazePos[1])
            gazeMask.draw()
        win.flip()
        
    # clear the subject display
    win.color=[0,0,0]
    win.flip()
    
    # clear the host display, this command is needed if you are backdropping images
    # to the host display (not demonstrated in this script)
    tk.sendCommand('clear_screen 0') 

    # send trial variables for Data Viewer integration
    # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
    tk.sendMessage('!V TRIAL_VAR task %s' %cond)

    # send interest area messages, if there is any, here we set a rectangular IA, just to
    # illustrate how the IA messages look like 
    # format: !V IAREA RECTANGLE <id> <left> <top> <right> <bottom> [label string] 
    # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
    tk.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s'%(1, scnWidth/2-100, scnHeight/2-200, scnWidth/2+200, scnHeight/2+200, 'screenIA'))
    
    # send a message to mark the end of trial
    # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
    tk.sendMessage('TRIAL_RESULT')
    pylink.pumpDelay(100)
    tk.stopRecording() # stop recording

    # disable the aperture at the end of each trials
    gazeWindow.enabled=False

# STEP VIII: The real experiment starts here

# show some instructions here.
msg = visual.TextStim(win, text = 'Press ENTER twice to calibrate the tracker\nIn the task, press any key to end a trial')
msg.draw()
win.flip()
event.waitKeys()

# set up the camera and calibrate the tracker at the beginning of each block
tk.doTrackerSetup()

# run a block of trials
testList = trials[:]*1 # construct the trial list
random.shuffle(testList) # randomize the trial list

# Looping through the trial list
for t in testList: 
    runTrial(t)

# close the EDF data file
tk.setOfflineMode()
tk.closeDataFile()
pylink.pumpDelay(50)

# Get the EDF data and say goodbye
msg.text='Data transfering.....'
msg.draw()
win.flip()
tk.receiveDataFile(dataFileName, dataFolder + dataFileName)

#close the link to the tracker
tk.close()

# close the graphics
pylink.closeGraphics()
win.close()
core.quit()

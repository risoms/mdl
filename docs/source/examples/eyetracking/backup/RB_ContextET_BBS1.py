#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.90.3),
    on February 25, 2019, at 00:58
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
#EyeLink imports
from psychopy import visual, monitors
import time


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))#.decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'RBContextET_BBS1'  # from the Builder filename that created this script
expInfo = {u'condition': u'', 
           u'participant': u'', 
           u'dominant eye': u'', 
           u'corrective': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## check if subject exists
## -a if csv is of entire task, -0..-1..-2..-3 if set-0, set-1, etc.
expInfo['participant'] = str(int(expInfo['participant'])).zfill(4)
print(expInfo['participant'])
filename = _thisDir + os.sep + 'data/%s' %(expInfo['participant'])
print(filename)
while True:
    print(filename+".csv")
    if os.path.isfile(filename+".csv"):
        print('file exists')
        dlg = gui.DlgFromDict(dictionary=expInfo, title='file exists, try another subject number')
        expInfo['participant'] = str(int(expInfo['participant'])).zfill(4)
        filename = _thisDir + os.sep + 'data/%s' %(expInfo['participant'])
        if dlg.OK == False:
            core.quit()  # user pressed cancel
    else:
        print('new file')
        expInfo['participant'] = str(int(expInfo['participant'])).zfill(4)
        filename = _thisDir + os.sep + 'data/%s' %(expInfo['participant'])
        break
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------







expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
#filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp


# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0,
    allowGUI=False, allowStencil=False, winType='pyglet',
    monitor='testMonitor', color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
 
    
# Start Code - component code to be run before the window creation







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# set parameters
rating_Scale_position = (0, -450)
pos = (0,0)
size = (1222*.75, 859*.75)

#Set coordinates for location of image during Learning#
from random import sample
coordinates = dict(top=(0,150), middle=(0,0), bottom=(0,-150))
locations = ['top'] * 5 + (['middle'] * 5) + (['bottom'] * 5)
block_1 = sample(locations, len(locations))
block_2 = sample(locations, len(locations))
block_3 = sample(locations, len(locations))
block_4 = sample(locations, len(locations))
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# Initialize components for Routine "basketballContext"
basketballContextClock = core.Clock()
contextIntr = visual.TextStim(win=win, name='contextIntr',
    text='This task is divided into 4 blocks, with each block consisting of 2 parts: a learning and a test period.\n\nDuring the learning period you will be viewing a face. When viewing each face, you should memorize the face and imagine that you will be competing against that person in a one-on-one basketball game.\n\nFollowing the learning period, you will be presented with a test period which includes questions about the faces.\n\nPress any key to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instrText = visual.TextStim(win=win, name='instrText',
    text='You will begin with a practice block.\n\nRemember, when viewing each face during learning, you should memorize the face and imagine that you will be competing against that person in a one-on-one basketball game.\n\nIf you have any questions, please ask them now or press any key to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);
win.mouseVisible = False

# Initialize components for Routine "learningPhase"
learningPhaseClock = core.Clock()
stimuliLrn = visual.ImageStim(
    win=win, name='stimuliLrn',units='pix', 
    image='sin', mask=None,
    ori=0, pos=pos, size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endPracticeLrn"
endPracticeLrnClock = core.Clock()
endPracticeLn = visual.TextStim(win=win, name='endPracticeLn',
    text='That was the end of the practice learning period, now you will begin the practice test period.\n\nDuring the test period, you will be presented with a face. If you saw the face previously, press the "Old" key. If you did not see the face previously press the "New" key.\n\nAfter indicating whether the face was old or new, you will press the numbered keys to indicate how likely you are to want to get to know that person on a 1 (not at all likely) to 5 (extremely likely) scale.\n\nIf you have any questions, please ask them now or press any key to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "testPhase"
testPhaseClock = core.Clock()
stimuliTest = visual.ImageStim(
    win=win, name='stimuliTest',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
oldNew = visual.TextStim(win=win, name='oldNew',
    text='Old or New?',
    font='Arial',
    pos=(0, -.70), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "interact"
interactClock = core.Clock()
stimuliInteract = visual.ImageStim(
    win=win, name='stimuliInteract',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
questionInteract = visual.TextStim(win=win, name='questionInteract',
    text='How likely are you to want to get to know this person on a 1 to 5 scale?',
    font='Arial',
    pos=(0, -.68), height=0.1, wrapWidth=2, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
rating_Scale = visual.ImageStim(
    win=win, name='rating_Scale',units='pix', 
    image='RatingScale3.jpg', mask=None,
    ori=0, pos=rating_Scale_position, size=(714,81),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endPracticeTest"
endPracticeTestClock = core.Clock()
endPrTest = visual.TextStim(win=win, name='endPrTest',
    text='That was the end of the practice block.\n\nYou will now start with the actual task. If you have any questions or need any clarification, please ask now since you will not have time to ask questions later.\n\nRemember, you will start with the learning period. When viewing each face, you should memorize the face and imagine that you will be competing against that person in a one-on-one basketball game.\n\nPress any key when you are ready to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "learningPhase"
learningPhaseClock = core.Clock()
stimuliLrn = visual.ImageStim(
    win=win, name='stimuliLrn',units='pix', 
    image='sin', mask=None,
    ori=0, pos=pos, size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endLearning"
endLearningClock = core.Clock()
endLrn = visual.TextStim(win=win, name='endLrn',
    text='That was the end of the learning period, now you will begin the test period.\n\nRemember you will be presented with a face, if you saw the face previously, press the "Old" key. If you did not see the face previously press the "New" key.\n\nAfterwards, you will press the numbered keys to indicate how likely you are to want to get to know that person on a 1 (not at all likely) to 5 (extremely likely) scale.\nPress any key when you are ready to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "testPhase"
testPhaseClock = core.Clock()
stimuliTest = visual.ImageStim(
    win=win, name='stimuliTest',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
oldNew = visual.TextStim(win=win, name='oldNew',
    text='Old or New?',
    font='Arial',
    pos=(0, -.70), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "interact"
interactClock = core.Clock()
stimuliInteract = visual.ImageStim(
    win=win, name='stimuliInteract',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
questionInteract = visual.TextStim(win=win, name='questionInteract',
    text='How likely are you to want to get to know this person on a 1 to 5 scale?',
    font='Arial',
    pos=(0, -.68), height=0.1, wrapWidth=2, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
rating_Scale = visual.ImageStim(
    win=win, name='rating_Scale',units='pix', 
    image='RatingScale3.jpg', mask=None,
    ori=0, pos=rating_Scale_position, size=(714,81),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endBlock"
endBlockClock = core.Clock()
endBlk = visual.TextStim(win=win, name='endBlk',
    text='That was the end of the block, you will have a 30-second break before starting with the next block.\n\nRemember during the learning period you should memorize the face and imagine that you will be competing against that person in a one-on-one basketball game.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "learningPhase"
learningPhaseClock = core.Clock()
stimuliLrn = visual.ImageStim(
    win=win, name='stimuliLrn',units='pix', 
    image='sin', mask=None,
    ori=0, pos=pos, size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endLearning"
endLearningClock = core.Clock()
endLrn = visual.TextStim(win=win, name='endLrn',
    text='That was the end of the learning period, now you will begin the test period.\n\nRemember you will be presented with a face, if you saw the face previously, press the "Old" key. If you did not see the face previously press the "New" key.\n\nAfterwards, you will press the numbered keys to indicate how likely you are to want to get to know that person on a 1 (not at all likely) to 5 (extremely likely) scale.\n\nPress any key when you are ready to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "testPhase"
testPhaseClock = core.Clock()
stimuliTest = visual.ImageStim(
    win=win, name='stimuliTest',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
oldNew = visual.TextStim(win=win, name='oldNew',
    text='Old or New?',
    font='Arial',
    pos=(0, -.70), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "interact"
interactClock = core.Clock()
stimuliInteract = visual.ImageStim(
    win=win, name='stimuliInteract',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
questionInteract = visual.TextStim(win=win, name='questionInteract',
    text='How likely are you to want to get to know this person on a 1 to 5 scale?',
    font='Arial',
    pos=(0, -.68), height=0.1, wrapWidth=2, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
rating_Scale = visual.ImageStim(
    win=win, name='rating_Scale',units='pix', 
    image='RatingScale3.jpg', mask=None,
    ori=0, pos=rating_Scale_position, size=(714,81),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endBlock"
endBlockClock = core.Clock()
endBlk = visual.TextStim(win=win, name='endBlk',
    text='That was the end of the block, you will have a 30-second break before starting with the next block.\n\nRemember during the learning period you should memorize the face and imagine that you will be competing against that person in a one-on-one basketball game.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "learningPhase"
learningPhaseClock = core.Clock()
stimuliLrn = visual.ImageStim(
    win=win, name='stimuliLrn',units='pix', 
    image='sin', mask=None,
    ori=0, pos=pos, size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endLearning"
endLearningClock = core.Clock()
endLrn = visual.TextStim(win=win, name='endLrn',
    text='That was the end of the learning period, now you will begin the test period.\n\nRemember you will be presented with a face, if you saw the face previously, press the "Old" key. If you did not see the face previously press the "New" key.\n\nAfterwards, you will press the numbered keys to indicate how likely you are to want to get to know that person on a 1 (not at all likely) to 5 (extremely likely) scale.\n\nPress any key when you are ready to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "testPhase"
testPhaseClock = core.Clock()
stimuliTest = visual.ImageStim(
    win=win, name='stimuliTest',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
oldNew = visual.TextStim(win=win, name='oldNew',
    text='Old or New?',
    font='Arial',
    pos=(0, -.70), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "interact"
interactClock = core.Clock()
stimuliInteract = visual.ImageStim(
    win=win, name='stimuliInteract',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
questionInteract = visual.TextStim(win=win, name='questionInteract',
    text='How likely are you to want to get to know this person on a 1 to 5 scale?',
    font='Arial',
    pos=(0, -.68), height=0.1, wrapWidth=2, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
rating_Scale = visual.ImageStim(
    win=win, name='rating_Scale',units='pix', 
    image='RatingScale3.jpg', mask=None,
    ori=0, pos=rating_Scale_position, size=(714,81),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endBlock"
endBlockClock = core.Clock()
endBlk = visual.TextStim(win=win, name='endBlk',
    text='That was the end of the block, you will have a 30-second break before starting with the next block.\n\nRemember during the learning period you should memorize the face and imagine that you will be competing against that person in a one-on-one basketball game.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "learningPhase"
learningPhaseClock = core.Clock()
stimuliLrn = visual.ImageStim(
    win=win, name='stimuliLrn',units='pix', 
    image='sin', mask=None,
    ori=0, pos=pos, size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endLearning"
endLearningClock = core.Clock()
endLrn = visual.TextStim(win=win, name='endLrn',
    text='That was the end of the learning period, now you will begin the test period.\n\nRemember you will be presented with a face, if you saw the face previously, press the "Old" key. If you did not see the face previously press the "New" key.\n\nAfterwards, you will press the numbered keys to indicate how likely you are to want to get to know that person on a 1 (not at all likely) to 5 (extremely likely) scale.\n\nPress any key when you are ready to continue.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "testPhase"
testPhaseClock = core.Clock()
stimuliTest = visual.ImageStim(
    win=win, name='stimuliTest',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
oldNew = visual.TextStim(win=win, name='oldNew',
    text='Old or New?',
    font='Arial',
    pos=(0, -.70), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "interact"
interactClock = core.Clock()
stimuliInteract = visual.ImageStim(
    win=win, name='stimuliInteract',units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=size,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
questionInteract = visual.TextStim(win=win, name='questionInteract',
    text='How likely are you to want to get to know this person on a 1 to 5 scale?',
    font='Arial',
    pos=(0, -.68), height=0.1, wrapWidth=2, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
rating_Scale = visual.ImageStim(
    win=win, name='rating_Scale',units='pix', 
    image='RatingScale3.jpg', mask=None,
    ori=0, pos=rating_Scale_position, size=(714,81),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "fixationCross"
fixationCrossClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.13, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "endSession"
endSessionClock = core.Clock()
end = visual.TextStim(win=win, name='end',
    text='You have finished the task, thank you for participating!\n',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# start eyetracker
# parameters
subject = expInfo['participant']
dominant_eye = expInfo['dominant eye']

# Initialize the Eyelink.
import mdl
eyetracking = mdl.eyetracking(window=win, libraries=False, subject=subject, timer=routineTimer)

# Connect to the Eyelink Host.
param = eyetracking.connect(calibration_type=13)

# Set the dominant eye. 
# Note: This step is especially critical for transmitting gaze coordinates from Eyelink->Psychopy.
eye_used = eyetracking.set_eye_used(eye=dominant_eye)

# Start calibration.
eyetracking.calibration()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










# ------Prepare to start Routine "basketballContext"-------
t = 0
basketballContextClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
bContextResp = event.BuilderKeyResponse()
# keep track of which components have finished
basketballContextComponents = [contextIntr, bContextResp]
for thisComponent in basketballContextComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "basketballContext"-------
while continueRoutine:
    # get current time
    t = basketballContextClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *contextIntr* updates
    if t >= 0.0 and contextIntr.status == NOT_STARTED:
        # keep track of start time/frame for later
        contextIntr.tStart = t
        contextIntr.frameNStart = frameN  # exact frame index
        contextIntr.setAutoDraw(True)
    
    # *bContextResp* updates
    if t >= 0.0 and bContextResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        bContextResp.tStart = t
        bContextResp.frameNStart = frameN  # exact frame index
        bContextResp.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if bContextResp.status == STARTED:
        theseKeys = event.getKeys()
        
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
    for thisComponent in basketballContextComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "basketballContext"-------
for thisComponent in basketballContextComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "basketballContext" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
instrResp = event.BuilderKeyResponse()
win.mouseVisible = False
# keep track of which components have finished
instructionsComponents = [instrText, instrResp]
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrText* updates
    if t >= 0.0 and instrText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText.tStart = t
        instrText.frameNStart = frameN  # exact frame index
        instrText.setAutoDraw(True)
    
    # *instrResp* updates
    if t >= 0.0 and instrResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrResp.tStart = t
        instrResp.frameNStart = frameN  # exact frame index
        instrResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instrResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instrResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instrResp.keys = theseKeys[-1]  # just the last key pressed
            instrResp.rt = instrResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    win.mouseVisible = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if instrResp.keys in ['', [], None]:  # No response was made
    instrResp.keys=None
thisExp.addData('instrResp.keys',instrResp.keys)
if instrResp.keys != None:  # we had a response
    thisExp.addData('instrResp.rt', instrResp.rt)
thisExp.nextEntry()
win.mouseVisible = False
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
practiceLrn = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('PracticeConditions.xlsx', selection='0:3'),
    seed=None, name='practiceLrn')
thisExp.addLoop(practiceLrn)  # add the loop to the experiment
thisPracticeLrn = practiceLrn.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeLrn.rgb)
if thisPracticeLrn != None:
    for paramName in thisPracticeLrn:
        exec('{} = thisPracticeLrn[paramName]'.format(paramName))

for thisPracticeLrn in practiceLrn:
    currentLoop = practiceLrn
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeLrn.rgb)
    if thisPracticeLrn != None:
        for paramName in thisPracticeLrn:
            exec('{} = thisPracticeLrn[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "learningPhase"-------
    t = 0
    learningPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(6.000000)
    # update component parameters for each repeat
    stimuliLrn.setImage(imageFile)
    # keep track of which components have finished
    learningPhaseComponents = [stimuliLrn]
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = 'learning'
    stimuluslocation = 'center'
    practiceLrn.addData('trial_type', trial_type)
    practiceLrn.addData('stimuluslocation', stimuluslocation)
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=practiceLrn.thisN, block='practiceblock')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "learning stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "learningPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = learningPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliLrn* updates
        if t >= 0.0 and stimuliLrn.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliLrn.tStart = t
            stimuliLrn.frameNStart = frameN  # exact frame index
            stimuliLrn.setAutoDraw(True)
        frameRemains = 0.0 + 6- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliLrn.status == STARTED and t >= frameRemains:
            stimuliLrn.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learningPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "learningPhase"-------
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='learning', race=race, correctAns=correctAns, 
                     OldNew=OldNew, coord='center', respkey='nan', accuracy='nan', interact='nan', interactRT='nan', 
                     oldnewRT='nan', condition=expInfo['condition'], participant=expInfo['participant'], 
                     exp=expName)
    eyetracking.stop_recording(trial=practiceLrn.thisN, block='practiceblock', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################        
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'practiceLrn'


# ------Prepare to start Routine "endPracticeLrn"-------
t = 0
endPracticeLrnClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endPracticeResp = event.BuilderKeyResponse()
# keep track of which components have finished
endPracticeLrnComponents = [endPracticeLn, endPracticeResp]
for thisComponent in endPracticeLrnComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endPracticeLrn"-------
while continueRoutine:
    # get current time
    t = endPracticeLrnClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endPracticeLn* updates
    if t >= 0.0 and endPracticeLn.status == NOT_STARTED:
        # keep track of start time/frame for later
        endPracticeLn.tStart = t
        endPracticeLn.frameNStart = frameN  # exact frame index
        endPracticeLn.setAutoDraw(True)
    
    # *endPracticeResp* updates
    if t >= 0.0 and endPracticeResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endPracticeResp.tStart = t
        endPracticeResp.frameNStart = frameN  # exact frame index
        endPracticeResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endPracticeResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endPracticeResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endPracticeResp.keys = theseKeys[-1]  # just the last key pressed
            endPracticeResp.rt = endPracticeResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endPracticeLrnComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endPracticeLrn"-------
for thisComponent in endPracticeLrnComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endPracticeResp.keys in ['', [], None]:  # No response was made
    endPracticeResp.keys=None
thisExp.addData('endPracticeResp.keys',endPracticeResp.keys)
if endPracticeResp.keys != None:  # we had a response
    thisExp.addData('endPracticeResp.rt', endPracticeResp.rt)
thisExp.nextEntry()

# set up handler to look after randomisation of conditions etc
practiceTest = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('PracticeConditions.xlsx'),
    seed=None, name='practiceTest')
thisExp.addLoop(practiceTest)  # add the loop to the experiment
thisPracticeTest = practiceTest.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeTest.rgb)
if thisPracticeTest != None:
    for paramName in thisPracticeTest:
        exec('{} = thisPracticeTest[paramName]'.format(paramName))

for thisPracticeTest in practiceTest:
    currentLoop = practiceTest
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeTest.rgb)
    if thisPracticeTest != None:
        for paramName in thisPracticeTest:
            exec('{} = thisPracticeTest[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "testPhase"-------
    t = 0
    testPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliTest.setImage(imageFile)
    stimuliTestResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    testPhaseComponents = [stimuliTest, oldNew, stimuliTestResp]
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = "test"
    stimuluslocation = "center"
    practiceTest.addData('trial_type', trial_type)
    practiceTest.addData('stimuluslocation', stimuluslocation)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=practiceTest.thisN, block='practiceblock')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "test stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "testPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = testPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliTest* updates
        if t >= 0.0 and stimuliTest.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTest.tStart = t
            stimuliTest.frameNStart = frameN  # exact frame index
            stimuliTest.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTest.status == STARTED and t >= frameRemains:
            stimuliTest.setAutoDraw(False)
        
        # *oldNew* updates
        if t >= 3 and oldNew.status == NOT_STARTED:
            # keep track of start time/frame for later
            oldNew.tStart = t
            oldNew.frameNStart = frameN  # exact frame index
            oldNew.setAutoDraw(True)
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if oldNew.status == STARTED and t >= frameRemains:
            oldNew.setAutoDraw(False)
        
        # *stimuliTestResp* updates
        if t >= 3 and stimuliTestResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTestResp.tStart = t
            stimuliTestResp.frameNStart = frameN  # exact frame index
            stimuliTestResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(stimuliTestResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTestResp.status == STARTED and t >= frameRemains:
            stimuliTestResp.status = STOPPED
        if stimuliTestResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                stimuliTestResp.keys = theseKeys[-1]  # just the last key pressed
                stimuliTestResp.rt = stimuliTestResp.clock.getTime()
                # was this 'correct'?
                if (stimuliTestResp.keys == str(correctAns)) or (stimuliTestResp.keys == correctAns):
                    stimuliTestResp.corr = 1
                else:
                    stimuliTestResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "testPhase"-------
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if stimuliTestResp.keys in ['', [], None]:  # No response was made
        stimuliTestResp.keys=None
        # was no response the correct answer?!
        if str(correctAns).lower() == 'none':
           stimuliTestResp.corr = 1  # correct non-response
        else:
           stimuliTestResp.corr = 0  # failed to respond (incorrectly)
    # store data for practiceTest (TrialHandler)
    practiceTest.addData('stimuliTestResp.keys',stimuliTestResp.keys)
    practiceTest.addData('stimuliTestResp.corr', stimuliTestResp.corr)
    if stimuliTestResp.keys != None:  # we had a response
        practiceTest.addData('stimuliTestResp.rt', stimuliTestResp.rt)
    
    # ------Prepare to start Routine "interact"-------
    t = 0
    interactClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliInteract.setImage(imageFile)
    respInteract = event.BuilderKeyResponse()
    # keep track of which components have finished
    interactComponents = [stimuliInteract, questionInteract, rating_Scale, respInteract]
    for thisComponent in interactComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "interact"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = interactClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliInteract* updates
        if t >= 0.0 and stimuliInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliInteract.tStart = t
            stimuliInteract.frameNStart = frameN  # exact frame index
            stimuliInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliInteract.status == STARTED and t >= frameRemains:
            stimuliInteract.setAutoDraw(False)
        
        # *questionInteract* updates
        if t >= 0.0 and questionInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            questionInteract.tStart = t
            questionInteract.frameNStart = frameN  # exact frame index
            questionInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if questionInteract.status == STARTED and t >= frameRemains:
            questionInteract.setAutoDraw(False)
        
        # *rating_Scale* updates
        if t >= 0.0 and rating_Scale.status == NOT_STARTED:
            # keep track of start time/frame for later
            rating_Scale.tStart = t
            rating_Scale.frameNStart = frameN  # exact frame index
            rating_Scale.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if rating_Scale.status == STARTED and t >= frameRemains:
            rating_Scale.setAutoDraw(False)
        
        # *respInteract* updates
        if t >= 0.0 and respInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            respInteract.tStart = t
            respInteract.frameNStart = frameN  # exact frame index
            respInteract.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(respInteract.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if respInteract.status == STARTED and t >= frameRemains:
            respInteract.status = STOPPED
        if respInteract.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                respInteract.keys = theseKeys[-1]  # just the last key pressed
                respInteract.rt = respInteract.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in interactComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "interact"-------
    for thisComponent in interactComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if respInteract.keys in ['', [], None]:  # No response was made
        respInteract.keys=None
    practiceTest.addData('respInteract.keys',respInteract.keys)
    if respInteract.keys != None:  # we had a response
        practiceTest.addData('respInteract.rt', respInteract.rt)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='test', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord='center', respkey=stimuliTestResp.keys, 
                     accuracy=stimuliTestResp.corr, interact=respInteract.keys, 
                     interactRT=respInteract.rt, oldnewRT=stimuliTestResp.rt, 
                     condition=expInfo['condition'], participant=expInfo['participant'], exp=expName)
    eyetracking.stop_recording(trial=practiceTest.thisN, block='practiceblock', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'practiceTest'


# ------Prepare to start Routine "endPracticeTest"-------
t = 0
endPracticeTestClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endPrResp = event.BuilderKeyResponse()
# keep track of which components have finished
endPracticeTestComponents = [endPrTest, endPrResp]
for thisComponent in endPracticeTestComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endPracticeTest"-------
while continueRoutine:
    # get current time
    t = endPracticeTestClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endPrTest* updates
    if t >= 0.0 and endPrTest.status == NOT_STARTED:
        # keep track of start time/frame for later
        endPrTest.tStart = t
        endPrTest.frameNStart = frameN  # exact frame index
        endPrTest.setAutoDraw(True)
    
    # *endPrResp* updates
    if t >= 0.0 and endPrResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endPrResp.tStart = t
        endPrResp.frameNStart = frameN  # exact frame index
        endPrResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endPrResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endPrResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endPrResp.keys = theseKeys[-1]  # just the last key pressed
            endPrResp.rt = endPrResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endPracticeTestComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endPracticeTest"-------
for thisComponent in endPracticeTestComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endPrResp.keys in ['', [], None]:  # No response was made
    endPrResp.keys=None
thisExp.addData('endPrResp.keys',endPrResp.keys)
if endPrResp.keys != None:  # we had a response
    thisExp.addData('endPrResp.rt', endPrResp.rt)
thisExp.nextEntry()
# the Routine "endPracticeTest" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Starting drift correction
eyetracking.drift_correction()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# set up handler to look after randomisation of conditions etc
block1Lrn = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block1_S1.xlsx', selection='0:15'),
    seed=None, name='block1Lrn')
thisExp.addLoop(block1Lrn)  # add the loop to the experiment
thisBlock1Lrn = block1Lrn.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock1Lrn.rgb)
if thisBlock1Lrn != None:
    for paramName in thisBlock1Lrn:
        exec('{} = thisBlock1Lrn[paramName]'.format(paramName))
        
for thisBlock1Lrn in block1Lrn:
    currentLoop = block1Lrn
    # abbreviate parameter names if possible (e.g. rgb = thisBlock1Lrn.rgb)
    if thisBlock1Lrn != None:
        for paramName in thisBlock1Lrn:
            exec('{} = thisBlock1Lrn[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "learningPhase"-------
    t = 0
    learningPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(6.000000)
    # update component parameters for each repeat
    stimuliLrn.setImage(imageFile)
    coord = coordinates[block_1[(block1Lrn.thisN)]]
    stimuliLrn.pos = coord
    # keep track of which components have finished
    learningPhaseComponents = [stimuliLrn]
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = "learning"
    stimuluslocation = coord
    block1Lrn.addData('trial_type', trial_type)
    block1Lrn.addData('stimuluslocation', stimuluslocation)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block1Lrn.thisN, block='block1')
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "learning stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "learningPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = learningPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliLrn* updates
        if t >= 0.0 and stimuliLrn.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliLrn.tStart = t
            stimuliLrn.frameNStart = frameN  # exact frame index
            stimuliLrn.setAutoDraw(True)
        frameRemains = 0.0 + 6- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliLrn.status == STARTED and t >= frameRemains:
            stimuliLrn.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learningPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "learningPhase"-------
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='learning', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord=coord, respkey='nan', accuracy='nan', interact='nan', 
                     interactRT='nan', oldnewRT='nan', condition=expInfo['condition'], 
                     participant=expInfo['participant'], exp=expName)
    eyetracking.stop_recording(trial=block1Lrn.thisN, block='block1', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block1Lrn'


# ------Prepare to start Routine "endLearning"-------
t = 0
endLearningClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endLrnResp = event.BuilderKeyResponse()
# keep track of which components have finished
endLearningComponents = [endLrn, endLrnResp]
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endLearning"-------
while continueRoutine:
    # get current time
    t = endLearningClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endLrn* updates
    if t >= 0.0 and endLrn.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrn.tStart = t
        endLrn.frameNStart = frameN  # exact frame index
        endLrn.setAutoDraw(True)
    
    # *endLrnResp* updates
    if t >= 0.0 and endLrnResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrnResp.tStart = t
        endLrnResp.frameNStart = frameN  # exact frame index
        endLrnResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endLrnResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endLrnResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endLrnResp.keys = theseKeys[-1]  # just the last key pressed
            endLrnResp.rt = endLrnResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endLearningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endLearning"-------
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endLrnResp.keys in ['', [], None]:  # No response was made
    endLrnResp.keys=None
thisExp.addData('endLrnResp.keys',endLrnResp.keys)
if endLrnResp.keys != None:  # we had a response
    thisExp.addData('endLrnResp.rt', endLrnResp.rt)
thisExp.nextEntry()
# the Routine "endLearning" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block1Test = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block1_S1.xlsx'),
    seed=None, name='block1Test')
thisExp.addLoop(block1Test)  # add the loop to the experiment
thisBlock1Test = block1Test.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock1Test.rgb)
if thisBlock1Test != None:
    for paramName in thisBlock1Test:
        exec('{} = thisBlock1Test[paramName]'.format(paramName))

for thisBlock1Test in block1Test:
    currentLoop = block1Test
    # abbreviate parameter names if possible (e.g. rgb = thisBlock1Test.rgb)
    if thisBlock1Test != None:
        for paramName in thisBlock1Test:
            exec('{} = thisBlock1Test[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "testPhase"-------
    t = 0
    testPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliTest.setImage(imageFile)
    stimuliTestResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    testPhaseComponents = [stimuliTest, oldNew, stimuliTestResp]
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = 'test'
    stimuluslocation = 'center'
    block1Test.addData('trial_type', trial_type)
    block1Test.addData('stimuluslocation', stimuluslocation)
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block1Test.thisN, block='block1')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "test stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "testPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = testPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliTest* updates
        if t >= 0.0 and stimuliTest.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTest.tStart = t
            stimuliTest.frameNStart = frameN  # exact frame index
            stimuliTest.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTest.status == STARTED and t >= frameRemains:
            stimuliTest.setAutoDraw(False)
        
        # *oldNew* updates
        if t >= 3 and oldNew.status == NOT_STARTED:
            # keep track of start time/frame for later
            oldNew.tStart = t
            oldNew.frameNStart = frameN  # exact frame index
            oldNew.setAutoDraw(True)
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if oldNew.status == STARTED and t >= frameRemains:
            oldNew.setAutoDraw(False)
        
        # *stimuliTestResp* updates
        if t >= 3 and stimuliTestResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTestResp.tStart = t
            stimuliTestResp.frameNStart = frameN  # exact frame index
            stimuliTestResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(stimuliTestResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTestResp.status == STARTED and t >= frameRemains:
            stimuliTestResp.status = STOPPED
        if stimuliTestResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                stimuliTestResp.keys = theseKeys[-1]  # just the last key pressed
                stimuliTestResp.rt = stimuliTestResp.clock.getTime()
                # was this 'correct'?
                if (stimuliTestResp.keys == str(correctAns)) or (stimuliTestResp.keys == correctAns):
                    stimuliTestResp.corr = 1
                else:
                    stimuliTestResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "testPhase"-------
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if stimuliTestResp.keys in ['', [], None]:  # No response was made
        stimuliTestResp.keys=None
        # was no response the correct answer?!
        if str(correctAns).lower() == 'none':
           stimuliTestResp.corr = 1  # correct non-response
        else:
           stimuliTestResp.corr = 0  # failed to respond (incorrectly)
    # store data for block1Test (TrialHandler)
    block1Test.addData('stimuliTestResp.keys',stimuliTestResp.keys)
    block1Test.addData('stimuliTestResp.corr', stimuliTestResp.corr)
    if stimuliTestResp.keys != None:  # we had a response
        block1Test.addData('stimuliTestResp.rt', stimuliTestResp.rt)
    
    # ------Prepare to start Routine "interact"-------
    t = 0
    interactClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliInteract.setImage(imageFile)
    respInteract = event.BuilderKeyResponse()
    # keep track of which components have finished
    interactComponents = [stimuliInteract, questionInteract, rating_Scale, respInteract]
    for thisComponent in interactComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "interact"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = interactClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliInteract* updates
        if t >= 0.0 and stimuliInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliInteract.tStart = t
            stimuliInteract.frameNStart = frameN  # exact frame index
            stimuliInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliInteract.status == STARTED and t >= frameRemains:
            stimuliInteract.setAutoDraw(False)
        
        # *questionInteract* updates
        if t >= 0.0 and questionInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            questionInteract.tStart = t
            questionInteract.frameNStart = frameN  # exact frame index
            questionInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if questionInteract.status == STARTED and t >= frameRemains:
            questionInteract.setAutoDraw(False)
        
        # *rating_Scale* updates
        if t >= 0.0 and rating_Scale.status == NOT_STARTED:
            # keep track of start time/frame for later
            rating_Scale.tStart = t
            rating_Scale.frameNStart = frameN  # exact frame index
            rating_Scale.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if rating_Scale.status == STARTED and t >= frameRemains:
            rating_Scale.setAutoDraw(False)
        
        # *respInteract* updates
        if t >= 0.0 and respInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            respInteract.tStart = t
            respInteract.frameNStart = frameN  # exact frame index
            respInteract.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(respInteract.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if respInteract.status == STARTED and t >= frameRemains:
            respInteract.status = STOPPED
        if respInteract.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                respInteract.keys = theseKeys[-1]  # just the last key pressed
                respInteract.rt = respInteract.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in interactComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "interact"-------
    for thisComponent in interactComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if respInteract.keys in ['', [], None]:  # No response was made
        respInteract.keys=None
    block1Test.addData('respInteract.keys',respInteract.keys)
    if respInteract.keys != None:  # we had a response
        block1Test.addData('respInteract.rt', respInteract.rt)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='test', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord='center', respkey=stimuliTestResp.keys, 
                     accuracy=stimuliTestResp.corr, interact=respInteract.keys, 
                     interactRT=respInteract.rt, oldnewRT=stimuliTestResp.rt, 
                     condition=expInfo['condition'], participant=expInfo['participant'],
                     exp=expName)
    eyetracking.stop_recording(trial=block1Test.thisN, block='block1', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block1Test'


# ------Prepare to start Routine "endBlock"-------
t = 0
endBlockClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(30.000000)
# update component parameters for each repeat
# keep track of which components have finished
endBlockComponents = [endBlk]
for thisComponent in endBlockComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endBlock"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endBlockClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endBlk* updates
    if t >= 0.0 and endBlk.status == NOT_STARTED:
        # keep track of start time/frame for later
        endBlk.tStart = t
        endBlk.frameNStart = frameN  # exact frame index
        endBlk.setAutoDraw(True)
    frameRemains = 0.0 + 30- win.monitorFramePeriod * 0.75  # most of one frame period left
    if endBlk.status == STARTED and t >= frameRemains:
        endBlk.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endBlockComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endBlock"-------
for thisComponent in endBlockComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Starting drift correction
eyetracking.drift_correction()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# set up handler to look after randomisation of conditions etc
block2Lrn = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block2_S1.xlsx', selection='0:15'),
    seed=None, name='block2Lrn')
thisExp.addLoop(block2Lrn)  # add the loop to the experiment
thisBlock2Lrn = block2Lrn.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock2Lrn.rgb)
if thisBlock2Lrn != None:
    for paramName in thisBlock2Lrn:
        exec('{} = thisBlock2Lrn[paramName]'.format(paramName))

for thisBlock2Lrn in block2Lrn:
    currentLoop = block2Lrn
    # abbreviate parameter names if possible (e.g. rgb = thisBlock2Lrn.rgb)
    if thisBlock2Lrn != None:
        for paramName in thisBlock2Lrn:
            exec('{} = thisBlock2Lrn[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "learningPhase"-------
    t = 0
    learningPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(6.000000)
    # update component parameters for each repeat
    stimuliLrn.setImage(imageFile)
    coord = coordinates[block_2[(block2Lrn.thisN)]]
    stimuliLrn.pos = coord
    # keep track of which components have finished
    learningPhaseComponents = [stimuliLrn]
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = "learning"
    stimuluslocation = coord
    block2Lrn.addData('trial_type', trial_type)
    block2Lrn.addData('stimuluslocation', stimuluslocation)
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block2Lrn.thisN, block='block2')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "learning stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "learningPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = learningPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliLrn* updates
        if t >= 0.0 and stimuliLrn.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliLrn.tStart = t
            stimuliLrn.frameNStart = frameN  # exact frame index
            stimuliLrn.setAutoDraw(True)
        frameRemains = 0.0 + 6- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliLrn.status == STARTED and t >= frameRemains:
            stimuliLrn.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learningPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "learningPhase"-------
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='learning', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord=coord, respkey='nan', accuracy='nan', interact='nan', 
                     interactRT='nan', oldnewRT='nan', condition=expInfo['condition'], 
                     participant=expInfo['participant'], exp=expName)
    eyetracking.stop_recording(trial=block2Lrn.thisN, block='block2', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################        
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block2Lrn'


# ------Prepare to start Routine "endLearning"-------
t = 0
endLearningClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endLrnResp = event.BuilderKeyResponse()
# keep track of which components have finished
endLearningComponents = [endLrn, endLrnResp]
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endLearning"-------
while continueRoutine:
    # get current time
    t = endLearningClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endLrn* updates
    if t >= 0.0 and endLrn.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrn.tStart = t
        endLrn.frameNStart = frameN  # exact frame index
        endLrn.setAutoDraw(True)
    
    # *endLrnResp* updates
    if t >= 0.0 and endLrnResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrnResp.tStart = t
        endLrnResp.frameNStart = frameN  # exact frame index
        endLrnResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endLrnResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endLrnResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endLrnResp.keys = theseKeys[-1]  # just the last key pressed
            endLrnResp.rt = endLrnResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endLearningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endLearning"-------
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endLrnResp.keys in ['', [], None]:  # No response was made
    endLrnResp.keys=None
thisExp.addData('endLrnResp.keys',endLrnResp.keys)
if endLrnResp.keys != None:  # we had a response
    thisExp.addData('endLrnResp.rt', endLrnResp.rt)
thisExp.nextEntry()
# the Routine "endLearning" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block2Test = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block2_S1.xlsx'),
    seed=None, name='block2Test')
thisExp.addLoop(block2Test)  # add the loop to the experiment
thisBlock2Test = block2Test.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock2Test.rgb)
if thisBlock2Test != None:
    for paramName in thisBlock2Test:
        exec('{} = thisBlock2Test[paramName]'.format(paramName))

for thisBlock2Test in block2Test:
    currentLoop = block2Test
    # abbreviate parameter names if possible (e.g. rgb = thisBlock2Test.rgb)
    if thisBlock2Test != None:
        for paramName in thisBlock2Test:
            exec('{} = thisBlock2Test[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "testPhase"-------
    t = 0
    testPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliTest.setImage(imageFile)
    stimuliTestResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    testPhaseComponents = [stimuliTest, oldNew, stimuliTestResp]
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = 'test'
    stimuluslocation = 'center'
    block2Test.addData('trial_type', trial_type)
    block2Test.addData('stimuluslocation', stimuluslocation)
   
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block2Test.thisN, block='block2')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "test stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "testPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = testPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliTest* updates
        if t >= 0.0 and stimuliTest.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTest.tStart = t
            stimuliTest.frameNStart = frameN  # exact frame index
            stimuliTest.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTest.status == STARTED and t >= frameRemains:
            stimuliTest.setAutoDraw(False)
        
        # *oldNew* updates
        if t >= 3 and oldNew.status == NOT_STARTED:
            # keep track of start time/frame for later
            oldNew.tStart = t
            oldNew.frameNStart = frameN  # exact frame index
            oldNew.setAutoDraw(True)
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if oldNew.status == STARTED and t >= frameRemains:
            oldNew.setAutoDraw(False)
        
        # *stimuliTestResp* updates
        if t >= 3 and stimuliTestResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTestResp.tStart = t
            stimuliTestResp.frameNStart = frameN  # exact frame index
            stimuliTestResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(stimuliTestResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTestResp.status == STARTED and t >= frameRemains:
            stimuliTestResp.status = STOPPED
        if stimuliTestResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                stimuliTestResp.keys = theseKeys[-1]  # just the last key pressed
                stimuliTestResp.rt = stimuliTestResp.clock.getTime()
                # was this 'correct'?
                if (stimuliTestResp.keys == str(correctAns)) or (stimuliTestResp.keys == correctAns):
                    stimuliTestResp.corr = 1
                else:
                    stimuliTestResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "testPhase"-------
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if stimuliTestResp.keys in ['', [], None]:  # No response was made
        stimuliTestResp.keys=None
        # was no response the correct answer?!
        if str(correctAns).lower() == 'none':
           stimuliTestResp.corr = 1  # correct non-response
        else:
           stimuliTestResp.corr = 0  # failed to respond (incorrectly)
    # store data for block2Test (TrialHandler)
    block2Test.addData('stimuliTestResp.keys',stimuliTestResp.keys)
    block2Test.addData('stimuliTestResp.corr', stimuliTestResp.corr)
    if stimuliTestResp.keys != None:  # we had a response
        block2Test.addData('stimuliTestResp.rt', stimuliTestResp.rt)
    
    # ------Prepare to start Routine "interact"-------
    t = 0
    interactClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliInteract.setImage(imageFile)
    respInteract = event.BuilderKeyResponse()
    # keep track of which components have finished
    interactComponents = [stimuliInteract, questionInteract, rating_Scale, respInteract]
    for thisComponent in interactComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "interact"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = interactClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliInteract* updates
        if t >= 0.0 and stimuliInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliInteract.tStart = t
            stimuliInteract.frameNStart = frameN  # exact frame index
            stimuliInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliInteract.status == STARTED and t >= frameRemains:
            stimuliInteract.setAutoDraw(False)
        
        # *questionInteract* updates
        if t >= 0.0 and questionInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            questionInteract.tStart = t
            questionInteract.frameNStart = frameN  # exact frame index
            questionInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if questionInteract.status == STARTED and t >= frameRemains:
            questionInteract.setAutoDraw(False)
        
        # *rating_Scale* updates
        if t >= 0.0 and rating_Scale.status == NOT_STARTED:
            # keep track of start time/frame for later
            rating_Scale.tStart = t
            rating_Scale.frameNStart = frameN  # exact frame index
            rating_Scale.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if rating_Scale.status == STARTED and t >= frameRemains:
            rating_Scale.setAutoDraw(False)
        
        # *respInteract* updates
        if t >= 0.0 and respInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            respInteract.tStart = t
            respInteract.frameNStart = frameN  # exact frame index
            respInteract.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(respInteract.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if respInteract.status == STARTED and t >= frameRemains:
            respInteract.status = STOPPED
        if respInteract.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                respInteract.keys = theseKeys[-1]  # just the last key pressed
                respInteract.rt = respInteract.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in interactComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "interact"-------
    for thisComponent in interactComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if respInteract.keys in ['', [], None]:  # No response was made
        respInteract.keys=None
    block2Test.addData('respInteract.keys',respInteract.keys)
    if respInteract.keys != None:  # we had a response
        block2Test.addData('respInteract.rt', respInteract.rt)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='test', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord='center', respkey=stimuliTestResp.keys, 
                     accuracy=stimuliTestResp.corr, interact=respInteract.keys, 
                     interactRT=respInteract.rt, oldnewRT=stimuliTestResp.rt, 
                     condition=expInfo['condition'], participant=expInfo['participant'],
                     exp=expName)
    eyetracking.stop_recording(trial=block2Test.thisN, block='block2', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block2Test'


# ------Prepare to start Routine "endBlock"-------
t = 0
endBlockClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(30.000000)
# update component parameters for each repeat
# keep track of which components have finished
endBlockComponents = [endBlk]
for thisComponent in endBlockComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endBlock"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endBlockClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endBlk* updates
    if t >= 0.0 and endBlk.status == NOT_STARTED:
        # keep track of start time/frame for later
        endBlk.tStart = t
        endBlk.frameNStart = frameN  # exact frame index
        endBlk.setAutoDraw(True)
    frameRemains = 0.0 + 30- win.monitorFramePeriod * 0.75  # most of one frame period left
    if endBlk.status == STARTED and t >= frameRemains:
        endBlk.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endBlockComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endBlock"-------
for thisComponent in endBlockComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Starting drift correction
eyetracking.drift_correction()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# set up handler to look after randomisation of conditions etc
block3Lrn = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block3_S1.xlsx', selection='0:15'),
    seed=None, name='block3Lrn')
thisExp.addLoop(block3Lrn)  # add the loop to the experiment
thisBlock3Lrn = block3Lrn.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock3Lrn.rgb)
if thisBlock3Lrn != None:
    for paramName in thisBlock3Lrn:
        exec('{} = thisBlock3Lrn[paramName]'.format(paramName))

for thisBlock3Lrn in block3Lrn:
    currentLoop = block3Lrn
    # abbreviate parameter names if possible (e.g. rgb = thisBlock3Lrn.rgb)
    if thisBlock3Lrn != None:
        for paramName in thisBlock3Lrn:
            exec('{} = thisBlock3Lrn[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "learningPhase"-------
    t = 0
    learningPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(6.000000)
    # update component parameters for each repeat
    stimuliLrn.setImage(imageFile)
    coord = coordinates[block_3[(block3Lrn.thisN)]]
    stimuliLrn.pos = coord
    # keep track of which components have finished
    learningPhaseComponents = [stimuliLrn]
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = "learning"
    stimuluslocation = coord
    block3Lrn.addData('trial_type', trial_type)
    block3Lrn.addData('stimuluslocation', stimuluslocation)
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block3Lrn.thisN, block='block3')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "learning stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "learningPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = learningPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliLrn* updates
        if t >= 0.0 and stimuliLrn.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliLrn.tStart = t
            stimuliLrn.frameNStart = frameN  # exact frame index
            stimuliLrn.setAutoDraw(True)
        frameRemains = 0.0 + 6- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliLrn.status == STARTED and t >= frameRemains:
            stimuliLrn.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learningPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "learningPhase"-------
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='learning', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord=coord, respkey='nan', accuracy='nan', interact='nan', 
                     interactRT='nan', oldnewRT='nan', condition=expInfo['condition'], 
                     participant=expInfo['participant'], exp=expName)
    eyetracking.stop_recording(trial=block3Lrn.thisN, block='block3', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################        
    
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block3Lrn'


# ------Prepare to start Routine "endLearning"-------
t = 0
endLearningClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endLrnResp = event.BuilderKeyResponse()
# keep track of which components have finished
endLearningComponents = [endLrn, endLrnResp]
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endLearning"-------
while continueRoutine:
    # get current time
    t = endLearningClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endLrn* updates
    if t >= 0.0 and endLrn.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrn.tStart = t
        endLrn.frameNStart = frameN  # exact frame index
        endLrn.setAutoDraw(True)
    
    # *endLrnResp* updates
    if t >= 0.0 and endLrnResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrnResp.tStart = t
        endLrnResp.frameNStart = frameN  # exact frame index
        endLrnResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endLrnResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endLrnResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endLrnResp.keys = theseKeys[-1]  # just the last key pressed
            endLrnResp.rt = endLrnResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endLearningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endLearning"-------
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endLrnResp.keys in ['', [], None]:  # No response was made
    endLrnResp.keys=None
thisExp.addData('endLrnResp.keys',endLrnResp.keys)
if endLrnResp.keys != None:  # we had a response
    thisExp.addData('endLrnResp.rt', endLrnResp.rt)
thisExp.nextEntry()
# the Routine "endLearning" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block3Test = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block3_S1.xlsx'),
    seed=None, name='block3Test')
thisExp.addLoop(block3Test)  # add the loop to the experiment
thisBlock3Test = block3Test.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock3Test.rgb)
if thisBlock3Test != None:
    for paramName in thisBlock3Test:
        exec('{} = thisBlock3Test[paramName]'.format(paramName))

for thisBlock3Test in block3Test:
    currentLoop = block3Test
    # abbreviate parameter names if possible (e.g. rgb = thisBlock3Test.rgb)
    if thisBlock3Test != None:
        for paramName in thisBlock3Test:
            exec('{} = thisBlock3Test[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "testPhase"-------
    t = 0
    testPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliTest.setImage(imageFile)
    stimuliTestResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    testPhaseComponents = [stimuliTest, oldNew, stimuliTestResp]
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = 'test'
    stimuluslocation = 'center'
    block3Test.addData('trial_type', trial_type)
    block3Test.addData('stimuluslocation', stimuluslocation)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block3Test.thisN, block='block3')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "test stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Start Routine "testPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = testPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliTest* updates
        if t >= 0.0 and stimuliTest.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTest.tStart = t
            stimuliTest.frameNStart = frameN  # exact frame index
            stimuliTest.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTest.status == STARTED and t >= frameRemains:
            stimuliTest.setAutoDraw(False)
        
        # *oldNew* updates
        if t >= 3 and oldNew.status == NOT_STARTED:
            # keep track of start time/frame for later
            oldNew.tStart = t
            oldNew.frameNStart = frameN  # exact frame index
            oldNew.setAutoDraw(True)
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if oldNew.status == STARTED and t >= frameRemains:
            oldNew.setAutoDraw(False)
        
        # *stimuliTestResp* updates
        if t >= 3 and stimuliTestResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTestResp.tStart = t
            stimuliTestResp.frameNStart = frameN  # exact frame index
            stimuliTestResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(stimuliTestResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTestResp.status == STARTED and t >= frameRemains:
            stimuliTestResp.status = STOPPED
        if stimuliTestResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                stimuliTestResp.keys = theseKeys[-1]  # just the last key pressed
                stimuliTestResp.rt = stimuliTestResp.clock.getTime()
                # was this 'correct'?
                if (stimuliTestResp.keys == str(correctAns)) or (stimuliTestResp.keys == correctAns):
                    stimuliTestResp.corr = 1
                else:
                    stimuliTestResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "testPhase"-------
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if stimuliTestResp.keys in ['', [], None]:  # No response was made
        stimuliTestResp.keys=None
        # was no response the correct answer?!
        if str(correctAns).lower() == 'none':
           stimuliTestResp.corr = 1  # correct non-response
        else:
           stimuliTestResp.corr = 0  # failed to respond (incorrectly)
    # store data for block3Test (TrialHandler)
    block3Test.addData('stimuliTestResp.keys',stimuliTestResp.keys)
    block3Test.addData('stimuliTestResp.corr', stimuliTestResp.corr)
    if stimuliTestResp.keys != None:  # we had a response
        block3Test.addData('stimuliTestResp.rt', stimuliTestResp.rt)
    
    # ------Prepare to start Routine "interact"-------
    t = 0
    interactClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliInteract.setImage(imageFile)
    respInteract = event.BuilderKeyResponse()
    # keep track of which components have finished
    interactComponents = [stimuliInteract, questionInteract, rating_Scale, respInteract]
    for thisComponent in interactComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "interact"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = interactClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliInteract* updates
        if t >= 0.0 and stimuliInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliInteract.tStart = t
            stimuliInteract.frameNStart = frameN  # exact frame index
            stimuliInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliInteract.status == STARTED and t >= frameRemains:
            stimuliInteract.setAutoDraw(False)
        
        # *questionInteract* updates
        if t >= 0.0 and questionInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            questionInteract.tStart = t
            questionInteract.frameNStart = frameN  # exact frame index
            questionInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if questionInteract.status == STARTED and t >= frameRemains:
            questionInteract.setAutoDraw(False)
        
        # *rating_Scale* updates
        if t >= 0.0 and rating_Scale.status == NOT_STARTED:
            # keep track of start time/frame for later
            rating_Scale.tStart = t
            rating_Scale.frameNStart = frameN  # exact frame index
            rating_Scale.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if rating_Scale.status == STARTED and t >= frameRemains:
            rating_Scale.setAutoDraw(False)
        
        # *respInteract* updates
        if t >= 0.0 and respInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            respInteract.tStart = t
            respInteract.frameNStart = frameN  # exact frame index
            respInteract.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(respInteract.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if respInteract.status == STARTED and t >= frameRemains:
            respInteract.status = STOPPED
        if respInteract.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                respInteract.keys = theseKeys[-1]  # just the last key pressed
                respInteract.rt = respInteract.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in interactComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "interact"-------
    for thisComponent in interactComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if respInteract.keys in ['', [], None]:  # No response was made
        respInteract.keys=None
    block3Test.addData('respInteract.keys',respInteract.keys)
    if respInteract.keys != None:  # we had a response
        block3Test.addData('respInteract.rt', respInteract.rt)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='test', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord='center', respkey=stimuliTestResp.keys, 
                     accuracy=stimuliTestResp.corr, interact=respInteract.keys, 
                     interactRT=respInteract.rt, oldnewRT=stimuliTestResp.rt, 
                     condition=expInfo['condition'], participant=expInfo['participant'],
                     exp=expName)
    eyetracking.stop_recording(trial=block3Test.thisN, block='block3', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block3Test'


# ------Prepare to start Routine "endBlock"-------
t = 0
endBlockClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(30.000000)
# update component parameters for each repeat
# keep track of which components have finished
endBlockComponents = [endBlk]
for thisComponent in endBlockComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endBlock"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endBlockClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endBlk* updates
    if t >= 0.0 and endBlk.status == NOT_STARTED:
        # keep track of start time/frame for later
        endBlk.tStart = t
        endBlk.frameNStart = frameN  # exact frame index
        endBlk.setAutoDraw(True)
    frameRemains = 0.0 + 30- win.monitorFramePeriod * 0.75  # most of one frame period left
    if endBlk.status == STARTED and t >= frameRemains:
        endBlk.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endBlockComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endBlock"-------
for thisComponent in endBlockComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Starting drift correction
eyetracking.drift_correction()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# set up handler to look after randomisation of conditions etc
block4Lrn = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block4_S1.xlsx', selection='0:15'),
    seed=None, name='block4Lrn')
thisExp.addLoop(block4Lrn)  # add the loop to the experiment
thisBlock4Lrn = block4Lrn.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock4Lrn.rgb)
if thisBlock4Lrn != None:
    for paramName in thisBlock4Lrn:
        exec('{} = thisBlock4Lrn[paramName]'.format(paramName))

for thisBlock4Lrn in block4Lrn:
    currentLoop = block4Lrn
    # abbreviate parameter names if possible (e.g. rgb = thisBlock4Lrn.rgb)
    if thisBlock4Lrn != None:
        for paramName in thisBlock4Lrn:
            exec('{} = thisBlock4Lrn[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "learningPhase"-------
    t = 0
    learningPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(6.000000)
    # update component parameters for each repeat
    stimuliLrn.setImage(imageFile)
    coord = coordinates[block_4[(block4Lrn.thisN)]]
    stimuliLrn.pos = coord
    # keep track of which components have finished
    learningPhaseComponents = [stimuliLrn]
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = "learning"
    stimuluslocation = coord
    block4Lrn.addData('trial_type', trial_type)
    block4Lrn.addData('stimuluslocation', stimuluslocation)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block4Lrn.thisN, block='block4')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "learning stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
            
    # -------Start Routine "learningPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = learningPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliLrn* updates
        if t >= 0.0 and stimuliLrn.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliLrn.tStart = t
            stimuliLrn.frameNStart = frameN  # exact frame index
            stimuliLrn.setAutoDraw(True)
        frameRemains = 0.0 + 6- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliLrn.status == STARTED and t >= frameRemains:
            stimuliLrn.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learningPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "learningPhase"-------
    for thisComponent in learningPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='learning', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord=coord, respkey='nan', accuracy='nan', interact='nan', 
                     interactRT='nan', oldnewRT='nan', condition=expInfo['condition'], 
                     participant=expInfo['participant'], exp=expName)
    eyetracking.stop_recording(trial=block4Lrn.thisN, block='block4', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################        
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block4Lrn'


# ------Prepare to start Routine "endLearning"-------
t = 0
endLearningClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endLrnResp = event.BuilderKeyResponse()
# keep track of which components have finished
endLearningComponents = [endLrn, endLrnResp]
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endLearning"-------
while continueRoutine:
    # get current time
    t = endLearningClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endLrn* updates
    if t >= 0.0 and endLrn.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrn.tStart = t
        endLrn.frameNStart = frameN  # exact frame index
        endLrn.setAutoDraw(True)
    
    # *endLrnResp* updates
    if t >= 0.0 and endLrnResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endLrnResp.tStart = t
        endLrnResp.frameNStart = frameN  # exact frame index
        endLrnResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endLrnResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endLrnResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endLrnResp.keys = theseKeys[-1]  # just the last key pressed
            endLrnResp.rt = endLrnResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endLearningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "endLearning"-------
for thisComponent in endLearningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endLrnResp.keys in ['', [], None]:  # No response was made
    endLrnResp.keys=None
thisExp.addData('endLrnResp.keys',endLrnResp.keys)
if endLrnResp.keys != None:  # we had a response
    thisExp.addData('endLrnResp.rt', endLrnResp.rt)
thisExp.nextEntry()
# the Routine "endLearning" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block4Test = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Block4_S1.xlsx'),
    seed=None, name='block4Test')
thisExp.addLoop(block4Test)  # add the loop to the experiment
thisBlock4Test = block4Test.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock4Test.rgb)
if thisBlock4Test != None:
    for paramName in thisBlock4Test:
        exec('{} = thisBlock4Test[paramName]'.format(paramName))

for thisBlock4Test in block4Test:
    currentLoop = block4Test
    # abbreviate parameter names if possible (e.g. rgb = thisBlock4Test.rgb)
    if thisBlock4Test != None:
        for paramName in thisBlock4Test:
            exec('{} = thisBlock4Test[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "testPhase"-------
    t = 0
    testPhaseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliTest.setImage(imageFile)
    stimuliTestResp = event.BuilderKeyResponse()
    # keep track of which components have finished
    testPhaseComponents = [stimuliTest, oldNew, stimuliTestResp]
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Adding columns to psychopy file for type of trial and coordinates of stimulus
    trial_type = 'test'
    stimuluslocation = 'center'
    block4Test.addData('trial_type', trial_type)
    block4Test.addData('stimuluslocation', stimuluslocation)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Start recording. This should be run at the start of the trial. 
    # Note: There is an intentional delay of 150 msec to allow the Eyelink to buffer gaze samples.
    eyetracking.start_recording(trial=block4Test.thisN, block='block4')
    
    
    
    
    # Send messages to Eyelink. This allows post-hoc processing of timing related events (i.e. "stimulus onset").
    # Sending message "stimulus onset".
    msg = "test stimulus onset"
    eyetracking.send_message(msg=msg)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
          
    # -------Start Routine "testPhase"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = testPhaseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliTest* updates
        if t >= 0.0 and stimuliTest.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTest.tStart = t
            stimuliTest.frameNStart = frameN  # exact frame index
            stimuliTest.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTest.status == STARTED and t >= frameRemains:
            stimuliTest.setAutoDraw(False)
        
        # *oldNew* updates
        if t >= 3 and oldNew.status == NOT_STARTED:
            # keep track of start time/frame for later
            oldNew.tStart = t
            oldNew.frameNStart = frameN  # exact frame index
            oldNew.setAutoDraw(True)
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if oldNew.status == STARTED and t >= frameRemains:
            oldNew.setAutoDraw(False)
        
        # *stimuliTestResp* updates
        if t >= 3 and stimuliTestResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliTestResp.tStart = t
            stimuliTestResp.frameNStart = frameN  # exact frame index
            stimuliTestResp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(stimuliTestResp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 3 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliTestResp.status == STARTED and t >= frameRemains:
            stimuliTestResp.status = STOPPED
        if stimuliTestResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                stimuliTestResp.keys = theseKeys[-1]  # just the last key pressed
                stimuliTestResp.rt = stimuliTestResp.clock.getTime()
                # was this 'correct'?
                if (stimuliTestResp.keys == str(correctAns)) or (stimuliTestResp.keys == correctAns):
                    stimuliTestResp.corr = 1
                else:
                    stimuliTestResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testPhaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "testPhase"-------
    for thisComponent in testPhaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if stimuliTestResp.keys in ['', [], None]:  # No response was made
        stimuliTestResp.keys=None
        # was no response the correct answer?!
        if str(correctAns).lower() == 'none':
           stimuliTestResp.corr = 1  # correct non-response
        else:
           stimuliTestResp.corr = 0  # failed to respond (incorrectly)
    # store data for block4Test (TrialHandler)
    block4Test.addData('stimuliTestResp.keys',stimuliTestResp.keys)
    block4Test.addData('stimuliTestResp.corr', stimuliTestResp.corr)
    if stimuliTestResp.keys != None:  # we had a response
        block4Test.addData('stimuliTestResp.rt', stimuliTestResp.rt)
    
    # ------Prepare to start Routine "interact"-------
    t = 0
    interactClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    stimuliInteract.setImage(imageFile)
    respInteract = event.BuilderKeyResponse()
    # keep track of which components have finished
    interactComponents = [stimuliInteract, questionInteract, rating_Scale, respInteract]
    for thisComponent in interactComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "interact"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = interactClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimuliInteract* updates
        if t >= 0.0 and stimuliInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            stimuliInteract.tStart = t
            stimuliInteract.frameNStart = frameN  # exact frame index
            stimuliInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if stimuliInteract.status == STARTED and t >= frameRemains:
            stimuliInteract.setAutoDraw(False)
        
        # *questionInteract* updates
        if t >= 0.0 and questionInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            questionInteract.tStart = t
            questionInteract.frameNStart = frameN  # exact frame index
            questionInteract.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if questionInteract.status == STARTED and t >= frameRemains:
            questionInteract.setAutoDraw(False)
        
        # *rating_Scale* updates
        if t >= 0.0 and rating_Scale.status == NOT_STARTED:
            # keep track of start time/frame for later
            rating_Scale.tStart = t
            rating_Scale.frameNStart = frameN  # exact frame index
            rating_Scale.setAutoDraw(True)
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if rating_Scale.status == STARTED and t >= frameRemains:
            rating_Scale.setAutoDraw(False)
        
        # *respInteract* updates
        if t >= 0.0 and respInteract.status == NOT_STARTED:
            # keep track of start time/frame for later
            respInteract.tStart = t
            respInteract.frameNStart = frameN  # exact frame index
            respInteract.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(respInteract.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if respInteract.status == STARTED and t >= frameRemains:
            respInteract.status = STOPPED
        if respInteract.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                respInteract.keys = theseKeys[-1]  # just the last key pressed
                respInteract.rt = respInteract.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in interactComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "interact"-------
    for thisComponent in interactComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if respInteract.keys in ['', [], None]:  # No response was made
        respInteract.keys=None
    block4Test.addData('respInteract.keys',respInteract.keys)
    if respInteract.keys != None:  # we had a response
        block4Test.addData('respInteract.rt', respInteract.rt)
    
    # ------Prepare to start Routine "fixationCross"-------
    t = 0
    fixationCrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationCrossComponents = [fixation]
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "fixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationCrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation.status == STARTED and t >= frameRemains:
            fixation.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # Stops Eyelink recording. Also allows transmission of trial-level variables (optional) to Eyelink.
    # Note: Variables sent are optional. If they being included, they must be in ```python dict``` format.
    variables = dict(stimulus=imageFile, trial_type='test', race=race, correctAns=correctAns,
                     OldNew=OldNew, coord='center', respkey=stimuliTestResp.keys, 
                     accuracy=stimuliTestResp.corr, interact=respInteract.keys, 
                     interactRT=respInteract.rt, oldnewRT=stimuliTestResp.rt, 
                     condition=expInfo['condition'], participant=expInfo['participant'],
                     exp=expName)
    eyetracking.stop_recording(trial=block4Test.thisN, block='block4', variables=variables)
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    
    # -------Ending Routine "fixationCross"-------
    for thisComponent in fixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block4Test'


# ------Prepare to start Routine "endSession"-------
t = 0
endSessionClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
endResp = event.BuilderKeyResponse()
# keep track of which components have finished
endSessionComponents = [end, endResp]
for thisComponent in endSessionComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "endSession"-------
while continueRoutine:
    # get current time
    t = endSessionClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end* updates
    if t >= 0.0 and end.status == NOT_STARTED:
        # keep track of start time/frame for later
        end.tStart = t
        end.frameNStart = frameN  # exact frame index
        end.setAutoDraw(True)
    
    # *endResp* updates
    if t >= 0.0 and endResp.status == NOT_STARTED:
        # keep track of start time/frame for later
        endResp.tStart = t
        endResp.frameNStart = frameN  # exact frame index
        endResp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(endResp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if endResp.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            endResp.keys = theseKeys[-1]  # just the last key pressed
            endResp.rt = endResp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endSessionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Finish Eyelink recording.
eyetracking.finish_recording()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
# -------Ending Routine "endSession"-------
for thisComponent in endSessionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if endResp.keys in ['', [], None]:  # No response was made
    endResp.keys=None
thisExp.addData('endResp.keys',endResp.keys)
if endResp.keys != None:  # we had a response
    thisExp.addData('endResp.rt', endResp.rt)
thisExp.nextEntry()
# the Routine "endSession" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
win.mouseVisible = False
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

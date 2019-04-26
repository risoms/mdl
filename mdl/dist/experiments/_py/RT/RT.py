#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

#logging
import logging as errorlog
import os  # handy system and path functions
from subprocess import check_output

#set up logging to file
errorlog.basicConfig(
    filename='error.log', 
    filemode='w', 
    level=errorlog.WARNING, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logger=errorlog.getLogger(__name__)

import platform
import _winreg
def get_registry_value(key, subkey, value):
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value
    
def cpu():
    try:
        cputype = get_registry_value(
            "HKEY_LOCAL_MACHINE", 
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")
    except:
        import wmi, pythoncom
        pythoncom.CoInitialize() 
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cputype = i.Name
        pythoncom.CoUninitialize()
 
    if cputype == 'AMD Athlon(tm)':
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %.2f Ghz' % (cpuspeed / 1000.0)
    elif cputype == 'AMD Athlon(tm) Processor':
        import wmi
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %s' % cpuspeed
    else:
        pass
    return cputype
    
log_system = platform.system() +" " + platform.win32_ver()[0]#windows 7
log_cpu = cpu() #cpu
#log_video = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
log_video = check_output("wmic path win32_VideoController get VideoProcessor")
log_video = (' '.join(log_video.split())).replace("VideoProcessor ","")

errorlog.error(log_system)
errorlog.error(log_cpu)
errorlog.error(log_video)

#--------------------------------------------------------------------------------------------------testing begin
import pyglet
pyglet.options['shadow_window'] = False
#--------------------------------------------------------------------------------------------------testing end

#--------------------------------------------------------------------------------------------------begin logging
while True:
    try:
        from psychopy import gui, visual, core, data, event, logging
        from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
        import sys  # to get file system encoding

        # Ensure that relative paths start from the same directory as this script
        _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
        os.chdir(_thisDir)
        
        # Store info about the experiment session
        expName = u'RT'  # from the Builder filename that created this script
        expInfo = {u'session': u'001', u'participant': u'000001'}
        dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
        if dlg.OK == False:
            core.quit()  # user pressed cancel
        
        ## check if subject exists
        ## -a if csv is of entire task, -0..-1..-2..-3 if set-0, set-1, etc.
        expInfo['participant'] = str(int(expInfo['participant'])).zfill(6)
        print (expInfo['participant'])
        filename = _thisDir + os.sep + 'data/%s_%s-a' %(expInfo['participant'],expInfo['session'])
        print (filename)
        while True:
            print(filename+".csv")
            if os.path.isfile(filename+".csv"):
                print('file exists')
                dlg = gui.DlgFromDict(dictionary=expInfo, title='file exists, try another subject/session number')
                expInfo['participant'] = str(int(expInfo['participant'])).zfill(6)
                filename = _thisDir + os.sep + 'data/%s_%s-a' %(expInfo['participant'],expInfo['session'])
                if dlg.OK == False:
                    core.quit()  # user pressed cancel
            else:
                print('new file')
                expInfo['participant'] = str(int(expInfo['participant'])).zfill(6)
                filename = _thisDir + os.sep + 'data/%s_%s-a' %(expInfo['participant'],expInfo['session'])
                break
        expInfo['date'] = data.getDateStr()  # add a simple timestamp
        expInfo['expName'] = expName
        
        
        # An ExperimentHandler isn't essential but helps with data saving
        thisExp = data.ExperimentHandler(name=expName, version='',
            extraInfo=expInfo, runtimeInfo=None,
            originPath=None,
            savePickle=True, saveWideText=True,
            dataFileName=filename)
        logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
        
        endExpNow = False  # flag for 'escape' or other condition => quit the exp
        
        # Start Code - component code to be run before the window creation
        timer_length = 500 #fixation duration: 500sec/60=8.33 minutes
        
        # Setup the Window
        win = visual.Window(
            size=[1366, 768], fullscr=True, screen=1,
            allowGUI=False, allowStencil=False,
            monitor='Experiment',  color=[-0.137,-0.137,-0.137], colorSpace='rgb',
            blendMode='avg', useFBO=False,
            units='norm')
        
        # store frame rate of monitor if we can measure it
        expInfo['frameRate'] = win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess
        
        # Initialize components for Routine "Introduction"
        IntroductionClock = core.Clock()
        intro_image = visual.ImageStim(
            win=win, name='intro_image',
            image='sin', mask=None,
            ori=0, pos=[0, 0], size=None,
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)

        # Initialize components for Routine "MRI_Fixation"
        MRI_FixationClock = core.Clock()
        ready_image = visual.ImageStim(
            win=win, name='ready_image',
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
        
        # Create some handy timers
        globalClock = core.Clock()  # to track the time since experiment started
        routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
        
        # set up handler to look after randomisation of conditions etc
        introDict = [{'image': u'intro_1.png'}, {'image': u'intro_2.png'}]
        Introduction_Loop = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=None,
            trialList=introDict,
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
            intro_image.setImage("Instructions/"+image)
            intro_key = event.BuilderKeyResponse()
            
            # keep track of which components have finished
            IntroductionComponents = [intro_image, intro_key]
            for thisComponent in IntroductionComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "Introduction"-------
            while continueRoutine:
                # get current time
                t = IntroductionClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *intro_image* updates
                if t >= 0.0 and intro_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    intro_image.tStart = t
                    intro_image.frameNStart = frameN  # exact frame index
                    intro_image.setAutoDraw(True)
                
                # *intro_key* updates
                if t >= 0.0 and intro_key.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    intro_key.tStart = t
                    intro_key.frameNStart = frameN  # exact frame index
                    intro_key.status = STARTED
                    # keyboard checking is just starting
                    event.clearEvents(eventType='keyboard')
                if intro_key.status == STARTED:
                    theseKeys = event.getKeys(keyList=['1'])
                    
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
        
        
        # ------Prepare to start Routine "MRI_Fixation"-------
        t = 0
        MRI_FixationClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        ready_image.setImage("Instructions/ready.png")
        ready_key = event.BuilderKeyResponse()
        # keep track of which components have finished
        MRI_FixationComponents = [ready_image, ready_key]
        for thisComponent in MRI_FixationComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "MRI_Fixation"-------
        while continueRoutine:
            # get current time
            t = MRI_FixationClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *ready_image* updates
            if t >= 0.0 and ready_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                ready_image.tStart = t
                ready_image.frameNStart = frameN  # exact frame index
                ready_image.setAutoDraw(True)
            
            # *ready_key* updates
            if t >= 0.0 and ready_key.status == NOT_STARTED:
                # keep track of start time/frame for later
                ready_key.tStart = t
                ready_key.frameNStart = frameN  # exact frame index
                ready_key.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(ready_key.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if ready_key.status == STARTED:
                theseKeys = event.getKeys(keyList=['5'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    ready_key.keys = theseKeys[-1]  # just the last key pressed
                    ready_key.rt = ready_key.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
            
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
        # check responses
        if ready_key.keys in ['', [], None]:  # No response was made
            ready_key.keys=None
        thisExp.addData('ready_key.keys',ready_key.keys)
        if ready_key.keys != None:  # we had a response
            thisExp.addData('ready_key.rt', ready_key.rt)
        thisExp.nextEntry()
        # the Routine "MRI_Fixation" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Fixation"-------
        t = 0
        FixationClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(timer_length)
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
            frameRemains = 0.0 + timer_length - win.monitorFramePeriod * 0.75  # most of one frame period left
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
        
        # these shouldn't be strictly necessary (should auto-save)
        thisExp.saveAsWideText(filename+'.csv')
        thisExp.saveAsPickle(filename)
        # make sure everything is closed down
        thisExp.abort()  # or data files will save again on exit
        win.close()
        core.quit()

    #--------------------------------------------------------------------------------------------------end logging
    except Exception as e: 
        logger.error(e, exc_info=True)
        win.close()
        core.quit()
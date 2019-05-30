#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'docs\source\examples\eyetracking\demo'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Example setup for Eyelink 1000 Plus, using PsychoPy 3.0.
#%% [markdown]
# Sample code to run SR Research Eyelink eyetracking system. Code is optimized for the Eyelink 1000 Plus (5.0), but should be compatiable with earlier systems.
#%% [markdown]
# ## Before Running the Participant
#%% [markdown]
# ### Import package

#%%
import os
from pathlib import Path
os.chdir('C:\\Users\\mdl-admin\\Desktop\\mdl')
import imhr
root = Path(imhr.__file__).parent
#%% [markdown]
# Set task parameters, either directly from PsychoPy or created manually.

#%%
from psychopy import visual, core
expInfo = {'condition': 'even', u'participant': '001', 'dominant eye': 'left', 'corrective': 'False'}
subject = expInfo['participant']
dominant_eye = expInfo['dominant eye']
# `psychopy.core.Clock.CountdownTimer` instance
routineTimer = core.CountdownTimer()
# `psychopy.visual.window.Window` instance
window = visual.Window(size=[1024, 768], fullscr=False, allowGUI=True, units='pix', winType='pyglet', color=[110,110,110], colorSpace='rgb255')
window.flip()

#%% [markdown]
# ### Initialize ``imhr.eyetracking.Eyelink``

#%%
# Initialize imhr.eyetracking.run()
eyetracking = imhr.eyetracking.Eyelink(window=window, libraries=True, subject=subject, timer=routineTimer, demo=True)

#%% [markdown]
# ### Connect to the Eyelink Host
#%% [markdown]
# This controls the parameters to be used when running the eyetracker.

#%%
param = eyetracking.connect(calibration_type=13)

#%% [markdown]
# ## Preparing the Participant
#%% [markdown]
# ### Set the dominant eye
#%% [markdown]
# This step is required for recieving gaze coordinates from Eyelink->PsychoPy.

#%%
eye_used = eyetracking.set_eye_used(eye=dominant_eye)

#%% [markdown]
# ### Start calibration
#%% [markdown]
# When calibration has been completed, it returns **True**.

#%%
# start calibration
calibration = eyetracking.calibration()
#%% [markdown]
# ### (Optional) Print message to console/terminal
#%% [markdown]
# Allows printing color coded messages to console/terminal/cmd. This may be useful for debugging issues.

#%%
eyetracking.console("eyetracking.calibration() started", "blue")

#%% [markdown]
# ### (Optional) Drift correction

#%%
drift = eyetracking.drift_correction()

#%% [markdown]
# ## Task Starting
#%% [markdown]
# ### Start recording

#%%
# Create stimulus (demonstration purposes only).
filename = "8380.bmp"
path = '%s/dist/stimuli/%s'%(root, filename)
size = (1024, 768) #image size
pos = (window.size[0]/2, window.size[1]/2) #positioning image at center of screen
stimulus = visual.ImageStim(win=window, name="stimulus", units='pix', image=path, pos=(0,0), size=size,
				flipHoriz=False, flipVert=False, texRes=128, interpolate=True, depth=-1.0)
stimulus.setAutoDraw(True)
window.flip()
window.flip()
#%%
# start recording
eyetracking.start_recording(trial=1, block=1)

#%% [markdown]
# ### (Optional) Initiate gaze contigent event
#%% [markdown]
# This is used for realtime data collection from Eyelink->PsychoPy.

#%%
# In the example, a participant is required to look at the bounding cross for a duration
# of 2000 msec before continuing the task. If this doesn't happen and a maxinum duration of 
# 10000 msec has occured, drift correction will be initiated.
bound = dict(left=448, top=156, right=1472, bottom=924)
eyetracking.gc(bound=bound, t_min=5000, t_max=20000)

#%% [markdown]
# ### (Optional) Collect real-time gaze coordinates from Eyelink

#%%
gxy, ps, sample = eyetracking.sample() # get gaze coordinates, pupil size, and sample


#%%
# In our example, the sampling rate of our device (Eyelink 1000 Plus) is 500Hz.
s1 = 0 # set current time to 0
lgxy = [] # create list of gaze coordinates (demonstration purposes only)
s0 = time.clock() # initial timestamp
# repeat
while True:
    # if difference between starting and current time is greater than > 2.01 msec, collect new sample
    diff = (s1 - s0)
    if diff >= .00201:
        gxy, ps, sample = eyetracking.sample() # get gaze coordinates, pupil size, and sample
        lgxy.append(gxy) # store in list (not required; demonstration purposes only)
        s0 = time.clock() # update starting time
    #else set current time
    else: 
        s1 = time.clock()

    #break `while` statement if list of gaze coordiantes >= 20 (not required; demonstration purposes only)
    if len(lgxy) >= 200: break

#%% [markdown]
# ### (Optional) Send messages to Eyelink
#%% [markdown]
# This allows post-hoc processing of event markers (i.e. "stimulus onset").

#%%
# Sending message "stimulus onset".
eyetracking.send_message(msg="stimulus onset")

#%% [markdown]
# ## Task Ending
#%% [markdown]
# ### Stop recording
#%% [markdown]
# Also (optional) provides trial-level variables to Eyelink.

#%%
# Prepare variables to be sent to Eyelink
variables = dict(stimulus=filename, trial_type='encoding', race="black")
# Stop recording
eyetracking.stop_recording(trial=1, block=1, variables=variables)

#%% [markdown]
# ### Finish recording

#%%
eyetracking.finish_recording()

#%% [markdown]
# ### Close PsychoPy

#%%
window.close()



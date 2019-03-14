#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
# Created on Wed Feb 13 15:37:43 2019
# @author: Semeon Risom
# @email: semeon.risom@gmail.com.
# Sample code to create regions of interest for use in Eyelink Display Software.

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

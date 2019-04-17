#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

#----start
draw_type = None # draw contour type: either raw, image, polygon, hull, box, or None
path = os.getcwd() + "/dist/example/"
raw_p = path + "/raw"
meta_p = path + "/meta"
sample_p = path + "/sample"

#----parameters
#create contours?
contours = False
#save examples of output
save_image = True 
#shape: polygon, raw, hull, box
shape = "box"


#----todo
#be able to offset each roi to their correct location on screen
#be able to choose the type of contour to use
#export contours or coordinates as:
    #csv
    #txt (eyelink format)
    #png
#make code runnable using multiprocessing
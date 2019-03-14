#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

#----start
contours = False #create contours?
draw_type = None # draw contour type: either raw, image, polygon, hull, box, or None
path = os.getcwd() + "/dist/example/"
raw_p = path + "/raw"
meta_p = path + "/meta"
sample_p = path + "/sample"
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:37:33 2017

@author: sr38553
this script is used to create a json file of the dotprobe variables as seen on csv
"""

import os
import csv
import pandas as pd

try: #use _file_ in most cases
    dir = os.path.dirname(__file__)
except NameError:  #except when running python from py2exe script
    import sys
    dir = os.path.dirname(sys.argv[0])
#directory
json_dir = os.path.abspath(os.path.join(dir, '../..'))

            
with open('placebo_2abc.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Default settings for processing.py   
| @date: Created on Sat May 1 15:12:38 2019
| @author: Semeon Risom
| @email: semeon.risom@gmail.com
| @url: https://semeon.io/d/R33-analysis
"""

from pdb import set_trace as breakpoint
import os, re, inspect
import numpy as np
from datetime import datetime
from distutils.version import StrictVersion
import importlib, pkg_resources, pip, platform

config={
    #!!!----path
    'path': {
        'home': os.path.abspath(os.getcwd()),
        'root': os.path.abspath(os.getcwd()),
        'r': os.path.abspath(os.getcwd() + 'dist/_R/'),
        'output': os.path.abspath(os.getcwd()+ 'dist/output'),
        'processed': os.path.abspath(__file__+ 'dist/output/data/process/'),
        'summary': os.path.abspath(__file__+ 'dist/output/data/R33-dotprobe-js.csv'),
    },
    #!!!----multiprocessing
    'cores': 7, #number of cpu cores to use for multiprocessing (all subjects only)
    #!!!----style
    'style':{
        'seaborn':'ticks'
    },
    #!!!----metadata
    'metadata':{
        #----analysis
        'subjects': {},
        'is': {}, #bool
        'var': {}, #raw variable name
        'short':{}, #short-hand name of variable
        'long':{}, #long name of variable
        'def': {}, #variable definition
        'cite': {}, #variable citation
        'url': {}, #url
        'img': {}, #image example
        'events': {'fixation':1500,'stimulus':{'iaps':4500,'pofa':3000}},
        'redcap': {'token':'D04484634409375EA8CC34F5B71BC14A'},
        #----lab equipment
        'lab':{
            'monitor.cm': [52, 29.5], #screensize (cm)
            'resolution.px': [1920, 1080], #screensize (px)
            'lab_monitor_device': 'Dell UltraSharp U2414H',
            'eyelink_webcam': 'Eyelink 1000 Plus',
            'lab_monitor_device': 'Dell UltraSharp U2414H',
            'lab_webcam': 'Logitech C922 Pro Stream Webcam',
            'distance': 615.0, #distance from screen (mm)
        },
        #----articles, notes
        'articles':[
            'One algorithm to rule them all? An evaluation and discussion of ten eye movement event-detection algorithms',
            'Comparison of eye movement filters used in HCI'
        ]
    },
    #!!!----processing (for processing.py)
    'processing':{
        'task': 'gRT',
        'type': 'eyetracking',
        'single_subject': False,
        'single_trial': False,
    },
    #!!!----preprocessing (for processing.py)
    'preprocessing':{
        'remove_missing': False, # remove missing data
        'remove_bounds': False, # remove samples out of bounds (i.e. gx=(2255, -322)
        'remove_spikes': False, # remove one-sample spikes
        'spike_delta': 50,
    },
    #!!!----filtering parameters
    'filter':{
        'f_b':{'N':2,'Wn':0.2,'btype':'low'},
        'f_g':{'sigma':2},
        'f_m':{'size':5},
        'f_sg':{'window':11,'order':3}, #default window=11,order=3
        'f_a':{'weights':([1.0, 2.0, 3.0, 2.0, 1.0])},
    },
    #!!!---classifcation parameters
    'classify':{
        'is_classify': True,
        'classify_eyelink_data': True, # if data is from eyelink, so we self classify fixations (True) or use original (False)
        'ctype': 'hmm', #if self classifying fixations, what classification technique should we use #either hmm, simple, ivt, or idt
        #simple parameters
        'missing': 0.0, #value to be used for missing data (simple)
        'maxdist': 360, #maximal inter sample distance in pixels (simple)
        'mindur': 200, #minimal duration of a fixation in milliseconds
        #ivt parameters
        'v_th': 5, #Velocity threshold in px/sec (ivt; default 20)
        #idt parameters
        'dr_th': 50, #Fixation duration threshold in px/msec (idt; default 100)
        'di_th': 60, #Dispersion threshold in px (idt; default 20)
        'filters':[['SavitzkyGolay','sg']]
    }
}
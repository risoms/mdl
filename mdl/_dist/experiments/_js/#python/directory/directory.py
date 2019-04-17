# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 13:52:06 2017

@author: sr38553
this script is used to create a json file of the dotprobe directory
"""
import os
import json

try: #use _file_ in most cases
    dir = os.path.dirname(__file__)
except NameError:  #except when running python from py2exe script
    import sys
    dir = os.path.dirname(sys.argv[0])
#directory
json_dir = os.path.abspath(os.path.join(dir, '../..'))



def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['subdirectory'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
        d['info'] = "###"
    return d

json_string = json.dumps(path_to_dict(json_dir))

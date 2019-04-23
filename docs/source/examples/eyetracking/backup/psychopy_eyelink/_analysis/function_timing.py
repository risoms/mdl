# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:37:14 2016

@author: sr38553
"""
import numpy as np
import time
import pandas
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

time.clock()
lst = [10,20,30,40,40,20,10,80,9]

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def movingaverage_1 (values, window):
    weights = np.repeat(1.0, window)/window
    ra = np.convolve(values, weights, 'valid')
    ma_1 = ra[-1] #index last value
    return ma_1

def movingaverage_2(values,window):
    values_array = np.asarray(values)  #convert to array
    cumsum = np.cumsum(values_array,dtype=float) #running average
    ra = (cumsum[window:] - cumsum[:-window]) / window 
    ma_2 = ra[-1] #index last value
    return ma_2

def movingaverage_3(lst,N):
    rm = pandas.DataFrame(lst, columns=['samples']).rolling(N,center=False).mean() #moving average
    ma = rm['samples'][rm.index[-1]] #last pupil sample
    return ma
    
def moving_avg(lst,window):
    lps_array = np.array(lst)  #convert to array
    cumsum = np.cumsum(lps_array,dtype=float) #running average
    ra = (cumsum[window:] - cumsum[:-window]) / window 
    ma = ra[-1] #index last value
    return ma

t1_1 = time.clock()  
ma_1 = movingaverage_1(lst,3)
t2_1 = time.clock()
t1_all = t2_1-t1_1

t1_2 = time.clock()  
ma_2 = movingaverage_2(lst,3)
t2_2 = time.clock()
t2_all = t2_2-t1_2

with PyCallGraph(output=GraphvizOutput()):
    t1_3 = time.clock()  
    ma_3 = movingaverage_1(lst,3)
    t2_3 = time.clock()
    t3_all = t2_3-t1_3

print(lst)
print(ma_1)
print(ma_2)
print(ma_3)
print('time %s'%(float(t1_all)*1000))
print('time %s'%(float(t2_all)*1000))
print('time %s'%(float(t3_all)*1000))
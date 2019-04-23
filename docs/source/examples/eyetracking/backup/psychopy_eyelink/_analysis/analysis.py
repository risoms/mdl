# -*- coding: utf-8 -*-
"""
Created on Fri Jun 03 08:54:02 2016

@author: sr38553
plot from: http://matplotlib.org/examples/pylab_examples/finance_work2.html#pylab-examples-finance-work2
"""

import os
import pandas
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.legend_handler import HandlerLine2D
import numpy as np
import scipy.ndimage

#import plotly
#import plotly.plotly as py
#import plotly.tools as tls
#from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, iplot_mpl
#from plotly.graph_objs import *
#import plotly.graph_objs as go
#py.sign_in('risoms', 'api_key')

class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)


subject="101"
subject_data = os.path.join(r"C:\Users\sr38553\Desktop\tasks\real_time_pupil_dilation\task\_data\gaze", "%s.csv"%(subject))
df0 = pandas.read_csv(subject_data)
pandas.options.mode.chained_assignment = None #deactivate warning of duplicating dataframe (here: df1 = df0[df0.trial == trialNum])

#analysis
#trials = [1]
#for trialNum in trials:
for trialNum in range(5,17):
    df1 = df0[df0.trial == trialNum]

    '''
    offline moving average of raw pupil area
    '''
    df1['pupil_offline'] = pandas.DataFrame(df1, columns=['old_pupil_sample']).rolling(20,center=False).mean() #moving average


    '''    
    calculating offline velocity from offline moving average
    '''
    df1['pupil_offline_velocity'] = pandas.DataFrame(df1, columns=['old_pupil_sample']).diff(periods=1, axis=0)    


    '''    
    calculating SD for baseline
    '''
    ps_lst = df1['old_pupil_sample'].values.tolist()
    ps_array = np.array(ps_lst)
    _mean = np.mean(ps_array)
    _stdev = np.std(ps_array, axis=0, ddof=1) #sample population stdev
    _max = _mean + (_stdev *1)
    _min = _mean - (_stdev *1)
    df1['neg_SD'] = pandas.DataFrame(df1, columns=['old_pupil_sample']).std()  
    df1['pos_SD'] = pandas.DataFrame(df1, columns=['old_pupil_sample']).std()       


    '''    
    smoothing peak
    '''   
    ps_lst = df1['new_pupil_sample'].values.tolist()
    ps_array = np.array(ps_lst)   
    #smoothing
    smooth = scipy.ndimage.filters.median_filter(ps_array,size=25) 

    '''
    percent change
    '''
    df1['pupil_pc'] = df1['old_pupil_sample'].pct_change(periods=1, fill_method='pad', limit=None, freq=None)


    '''
    adding cue variable
    '''
    #convert to list
    cue_lst = df1['feedback'].tolist()
    cue_lst2 = df1['feedback'].tolist() 

    #get first iteration    
    old = False
    for idx, item in enumerate(cue_lst):
        if item == 'green':
            if old == 'green':
                cue_lst[idx] = 0
            else:
                cue_lst[idx] = 'green'
                old = 'green'
    
        elif item == 'blue':
            if old == 'blue':
                cue_lst[idx] = 0
            else:
                cue_lst[idx] = 'blue'
                old = 'blue'
        
        elif item == 'red':
            if old == 'red':
                cue_lst[idx] = 0
            else:
                cue_lst[idx] = 'red'
                old = 'red'
        else:
            cue_lst[idx] = 0
            old = False
    
    #get position in list for cue
    green_pos = [i for i,x in enumerate(cue_lst) if x == 'green']
    blue_pos = [i for i,x in enumerate(cue_lst) if x == 'blue']
    red_pos = [i for i,x in enumerate(cue_lst) if x == 'red']
    
    
    '''
    adding blink variable
    '''
    #convert to list
    blink_lst = df1['blink'].tolist()

    #get first iteration    
    old = False
    for idx, item in enumerate(blink_lst):
        if item == 'blink_start':
            if old == 'blink_start':
                blink_lst[idx] = 0
            else:
                blink_lst[idx] = 'blink_start'
                old = 'blink_start'
    
        elif item == 'blink_end':
            if old == 'blink_end':
                blink_lst[idx] = 0
            else:
                blink_lst[idx] = 'blink_end'
                old = 'blink_end'
        else:
            blink_lst[idx] = 0
            old = False
    
    #get position in list for cue
    blink_start = [i for i,x in enumerate(blink_lst) if x == 'blink_start']
    blink_end = [i for i,x in enumerate(blink_lst) if x == 'blink_end']

    '''
    block analysis
    '''

    low_memory=False
    '''
    Analysis
    '''
    plot = True
    #analysis
    if plot:
        # These are the "Tableau 20" colors as RGB. 
        tableau20 = [(0, 0, 0),(152, 223, 138),(31, 119, 180),(255, 0, 0),(135,206,235),(0,128,0)]          
        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
        for i in range(len(tableau20)):    
            r, g, b = tableau20[i]    
            tableau20[i] = (r / 255., g / 255., b / 255.) 
        
        #axes and ticks
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
        textsize = 9
        
        #grid
        left, width = 0.1, .7
        rect1 = [left, 0.7, width, 0.2]
        rect2 = [left, 0.3, width, 0.4]
        rect3 = [left, 0.1, width, 0.2]
        
        #grid color
        fig = plt.figure(figsize=(13, 10), dpi=80,facecolor='white')
        axescolor = '#f6f6f6'
        
        # left, bottom, width, height axes
        ax1 = fig.add_axes(rect1, axisbg=axescolor)  
        ax2 = fig.add_axes(rect2, axisbg=axescolor,sharex=ax1)
        ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
        
        #ticks
        plt.minorticks_on()

        #plot 1
        ax1.set_xlim(-2, 10)
        ax1.plot(df1.psychopy_timestamp.values,df1.pupil_pc.values,'o-',color='b')
        ax1.set_title('Subject %s, Trial %s' %(subject,trialNum))
        ax1.set_ylabel('Percent Change')    
       
        #plot 2
        ax2.set_xlim(-2, 10)
        #cue        
        line1,= ax2.plot(df1.psychopy_timestamp.values,df1.new_pupil_sample.values,'o', markersize=8, markevery=green_pos,color='g',label='Green cue')
        line2,= ax2.plot(df1.psychopy_timestamp.values,df1.new_pupil_sample.values,'o', markersize=8, markevery=red_pos,color='r',label='Red cue')
        line3,= ax2.plot(df1.psychopy_timestamp.values,df1.new_pupil_sample.values,'o', markersize=8, markevery=blue_pos,color='b',label='Blue cue')
        #blink
        line4,= ax2.plot(df1.psychopy_timestamp.values,df1.new_pupil_sample.values,'v', markersize=15, markevery=blink_start,color='k',label='Blink start')
        line5,= ax2.plot(df1.psychopy_timestamp.values,df1.new_pupil_sample.values,'^', markersize=15, markevery=blink_end,color='k',label='Blink end')
        #pupil size        
        line6,= ax2.plot(df1.psychopy_timestamp.values, df1.old_pupil_sample.values,color=tableau20[1],label='Unadjusted')
        line7,= ax2.plot(df1.psychopy_timestamp.values, df1.new_pupil_sample.values,color=tableau20[2],label='Adjusted')

        #baseline
        line8,= ax2.plot(df1.psychopy_timestamp.values, df1.block_baseline_mean.values, color=tableau20[3], label='B_Baseline')
        line9,= ax2.plot(df1.psychopy_timestamp.values, df1.fixation_baseline_mean.values, color=tableau20[5], label='F_Baseline')
        line10,= ax2.plot(df1.psychopy_timestamp.values, df1.stimulus_baseline_mean.values, color=tableau20[4], label='S_Baseline')
        
        
        #thresholding-stimulus
        ax2.fill_between(df1["psychopy_timestamp"],df1['block_baseline_min'],df1['block_baseline_max'],facecolor='red', alpha=.05)
        ax2.fill_between(df1["psychopy_timestamp"],df1['fixation_baseline_min'],df1['fixation_baseline_max'],facecolor='green', alpha=.05)
        ax2.fill_between(df1["psychopy_timestamp"],df1['stimulus_baseline_min'],df1['stimulus_baseline_max'],facecolor='blue', alpha=.05)
        #label
        ax2.set_ylabel('Pupil Area')
        #legend
        ax2.legend(handles=[line1,line2,line3,line4,line5,line6,line7,line8,line9,line10],loc='center left', bbox_to_anchor=(1, 0.5))

        #plot 3
        # plot labels
        ax3.set_xlim(-2, 10)
        #plotting offline velocity
        ax3.plot(df1.psychopy_timestamp.values,df1.pupil_velocity.values,'o-',color='b')
        #ax3.plot(df1.psychopy_timestamp.values,df1.pupil_offline_velocity.values,'o-',color=tableau20[3])
        ax3.set_xlabel('Time (Sec)')   
        ax3.set_ylabel('Velocity')


        # turn off upper axis tick labels,
        for ax in ax1, ax2, ax3:
            if ax != ax3:
                for label in ax.get_xticklabels():
                    label.set_visible(False)
                    
        #trim values conflicting with y axis        
        ax1.yaxis.set_major_locator(MyLocator(5, prune='both'))
        ax2.yaxis.set_major_locator(MyLocator(11, prune='both'))
        ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))
        
        plt.savefig('plots\%s\s%s_t%s.jpg' %(subject,subject,trialNum))

        #plotly
        #plotly_fig = tls.mpl_to_plotly(fig) #convert matplotlib to plotly
        #plotly_fig['layout']['autosize'] = False
        #plotly_fig['layout']['width'] = 800
        #plotly_fig['layout']['height'] = 800
        #plotly.offline.plot(plotly_fig, filename='%s_%s.html'%(subject,trialNum))
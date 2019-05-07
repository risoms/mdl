#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Hub for running processing and analyzing raw data.   
| @date: Created on Sat May 1 15:12:38 2019   
| @author: Semeon Risom   
| @email: semeon.risom@gmail.com   
| @url: https://semeon.io/d/R33-analysis   
"""

# available classes and functions
__all__ = ['Processing']

# required external libraries
__required__ = ['distutils','importlib','nslr']

# core
from pdb import set_trace as breakpoint
from pathlib import Path
import numpy as np
import pandas as pd
import math as m
import sys
import os
import glob

## logging
import logging
import datetime

# local libraries
if __name__ == '__main__':
	from .. import Settings
	from .. import Metadata

class Processing():
    """Hub for running processing and analyzing raw data."""
    def __init__(self, config, isLibrary=True):
        """
		Initiate the mdl.r33.Processing module.

        Parameters
        ----------
        config : :class:`dict`
            Configuration data. i.e. trial number, location.
        isLibrary : :obj:`bool`
            Check if required libraries are available. Default `False`.
        """

        #check libraries
        if isLibrary:
            settings.library(__required__)

        #set current subject (use for iterations)
        self.current_subject = ''
        self.cgxy = ''
        self.log = ''
        self.thisCore = 0
        self.config = config
        self.filters = [['SavitzkyGolay', 'sg']]
		
    def getEstimatedMonitor(self, diagonal, window):
        """calculate estimate monitor size (w,h;cm) using estimated diagonal monitor (hypotenuse; cm).

        Attributes
        ----------
        df_raw : :class:`pandas.DataFrame`
            Pandas dataframe of subjects.
        """
        ratio = window[0]/window[1]
        monitor_x = float((ratio * (m.sqrt((m.pow(diagonal,2)) / (m.pow(ratio,2) + 1)))) * 2.54)
        monitor_y = float((m.sqrt((m.pow(diagonal,2)) / (m.pow(ratio,2) + 1))) * 2.54)
        monitor = [monitor_x, monitor_y]
        
        return monitor

    def preprocess(self, df, window):
        """Initial data cleaning.

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data.
        window : :class:`tuple`
            horizontal, vertical resolution

        Attributes
        ----------
        m_delta : :obj:`int`
            Maxinum one-sample change in velocity

        Notes
        ----------
        remove_missing:
            Remove samples with null values.
        remove_bounds:
            Remove samples outside of window bounds (1920,1080).
        remove_spikes:
            remove one-sample spikes if x and y-axis delta is greater than 5.
        """
        #sort
        df = df.sort_values(['TrialNum','sampleNum'],ascending=[True, True])

        #1) remove fixation cross samples #!!!
        #print(self.console['green'] + '///////////Preprocessing: Drop Fixation Cross samples' + self.console['ENDC'])
        #df = df[df['event'] != 'Fixation'].reset_index(drop=True)

        #2) get RT from timestamp
        d_loc = df[df['event'] == "DotLoc"]
        #check if participant responded
        if d_loc.shape[0] >=1:
            df["RT"] = d_loc['timestamp'][d_loc.index[-1]] - d_loc['timestamp'][d_loc.index[0]]
        else:
            self.log.warning('event: preprocess(self, df, window), core: %s, subject: %s, trial: %s, dotloc rows: %s'
                             %(self.thisCore, self.config['subject'], self.config['trial'], d_loc.shape[0]))

        #3) set event markers #!!!
        df['marker'] = "."

        #fixation event
        ##set marker
        #df['marker'][df.index[0]] = "Fixation Onset"
        df.loc[df.index[0], 'marker'] = "Fixation Onset"

        #stim event
        d_stim = df[df['event'] == "Stim"]
        ##set marker
        df.loc[d_stim.index[0], 'marker'] = "Stimulus Onset"

        #dotloc event #!!!
        ##set marker
        ##check if any samples exist within dotloc onset
        if d_loc.shape[0] >=1:
            df.loc[d_loc.index[0], 'marker'] = "Dotloc Onset"
        else:
            self.log.warning('event: preprocess(self, df, window), core: %s, subject: %s, trial: %s, dotloc rows: %s'
                             %(self.thisCore, self.config['subject'], self.config['trial'], d_loc.shape[0]))
            
        #end trial
        #df['marker'][df.index[-1]] = "End Trial"
        df.loc[df.index[-1], 'marker'] = "End Trial"

        #4) remove missing data #!!!
        ## convert '.' to null
        if self.config['remove_missing']:
            print(self.console['green'] + 'Preprocessing: Remove null samples' + self.console['ENDC'])
            ## drop null
            df = df[(df["x"].notnull()) & (df["y"].notnull())].reset_index(drop=True)
        else:
            #mark as bad sample
            df['bad'] = df.apply(lambda x: True if ((x['x'] == '.') or (x['y'] == '.')) else False, axis=1)

        #5) remove samples outside of window bounds (i.e. 0>x>1920, 0>y>1080) #!!!
        if self.config['remove_bounds']:
            print(self.console['green']+'Preprocessing: Remove samples outside of window bounds (i.e. 0 > x > 1920, 0 > y > 1080)'\
                  +self.console['ENDC'])
            df = df[(df['x'] <= window[0]) & (df['y'] <= window[1]) &
                    (df['x'] >= 0) & (df['y'] >= 0)].reset_index(drop=True)
        else:
            #mark as bad sample
            df['bad'] = df.apply(lambda x: True if ((x['x'] <= 0) or (x['y'] <= 0) or
                                                    (x['x'] > window[0]) or (x['y'] > window[1])
                                                    ) else x['bad'], axis=1)

        #6) remove one-sample spikes #!!!
        if self.config['remove_spikes']:
            print(self.console['green'] + 'Preprocessing: Remove one-sample spikes' + self.console['ENDC'])
            max_delta = self.config['spike_delta']
            #x
            delta = df['x'].diff().shift(-1).abs()
            delta.iloc[-1] = delta.iloc[-2]
            df = df[(delta < max_delta)]
            #y
            delta = df['y'].diff().shift(-1).abs()
            delta.iloc[-1] = delta.iloc[-2]
            df = df[(delta < max_delta)]
        # else mark spikes as bad
        else: 
            max_delta = self.config['spike_delta']
            #x
            delta = df['x'].diff().shift(-1).abs()
            delta.iloc[-1] = delta.iloc[-2]
            df_spike = df[(delta < max_delta)]
            #y
            delta = df['y'].diff().shift(-1).abs()
            delta.iloc[-1] = delta.iloc[-2]
            df_spike = df_spike.loc[(delta < max_delta)]

            #mark samples as bad
            spike = df_spike.index
            df.loc[spike,'bad'] = True

        #set x,y to NaN
        #df["x"] = df["x"].replace(".", np.NaN)
        #df["y"] = df["y"].replace(".", np.NaN)

        return df

    #getting data for analysis

    def getData(self, path=None):
        """preparing data for use in analysis

        Parameters
        ----------
        path : :obj:`str`
            The directory path of the subject data

        Attributes
        ----------
        path : :obj:`str`
            Specific directory path used.

        Returns
        -------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data.
        _path : :obj:`list`
            list of files used for analysis.

        Notes
        -----
        You can either get data from all subjects within a directory, or from a specific subject (subject_session).

        Examples
        --------
        >>> #if using path:
        >>> df_raw = getData(path=self.config['path'])

        >>> #if getting data for single subject:
        >>> df_raw = getData(path=self.config['path'],subject_session=['1099','1', '0'])

        """
        #if single subject get path from config
        if (self.config['single_subject']):
            path = '%s/%s_%sabc.csv'%(self.config['path'],self.config['subject'],self.config['session'])
        
        #read csv as dataframe
        df = pd.read_csv(path, float_precision='high')

        ##rename
        if self.config['source'] != 'eyelink':
            df = df.rename(columns={"trialNumTask": "TrialNum", "sample_time": "timestamp",
                                    "isWindowSuccess": "is_calibrated",
                                    "LEmotion": "left_mood","REmotion": "right_mood"})

        #sort    
        df = df.sort_values(['TrialNum','timestamp'],ascending=[True, True]).reset_index(drop=True)

        #set as eyetracking or behavioral
        if self.config['source'] != 'eyelink':
            ##create column for type (eyetracking, behavioral)
            df['type'] = np.where((df['isWebcamUsed']==True), 'eyetracking', 'behavioral')

        return df, path

    def filter_data(self, df, filter_type, config, **kwargs):
        """
        Butterworth: Design an Nth-order digital or analog Butterworth filter and return
        the filter coefficients.

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data.
        filter_type : :obj:`str`, optional
			Type of filter.
        config : :class:`dict`
            Configuration data. i.e. trial number, location.

        Attributes
        ----------
        filter_type : :obj:`str`
            Filter type: 'butterworth'

        """
        from scipy.ndimage.filters import gaussian_filter1d
        from scipy.signal import butter,filtfilt,medfilt,savgol_filter

        g_t= df['timestamp']
        g_x = df['x']
        g_y= df['y']

        """filters"""
        #http://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html
        #Butterworth filter
        #note: butterworth cant have NaN data
        if filter_type=='butterworth':
            wn=self.config['f_b']['Wn']
            order=self.config['f_b']['N']
            b, a = butter(order, wn, 'lowpass', output='ba')
            #b, a = butter(order, wn, 'low')
            #converting pandas series to numpy ndarray
            bg_t=df['timestamp']
            bg_x=df['x']
            bg_y=df['y']
            f_x = filtfilt(b, a, bg_x)
            f_y = filtfilt(b, a, bg_y)
            #print(f_x)
            fxy_df = pd.DataFrame({'x':f_x, 'y':f_y, 'timestamp':bg_t})
            #breakpoint() #TODO!

        #gaussian filter
        elif filter_type=='gauss':
            sigma=self.config['f_g']['sigma']
            print('sigma: %s'%(sigma))
            f_x = gaussian_filter1d(g_x,sigma)
            f_y = gaussian_filter1d(g_y,sigma)
            fxy_df = pd.DataFrame({'x':f_x, 'y':f_y, 'timestamp':g_t})

        #median filter
        elif filter_type=='median':
            size=self.config['f_m']['size']
            print('size: %s'%(size))
            f_x=medfilt(g_x,size)
            f_y=medfilt(g_y,size)
            fxy_df = pd.DataFrame({'x':f_x, 'y':f_y, 'timestamp':g_t})

        #http://scipy-cookbook.readthedocs.io/items/SavitzkyGolay.html
        #savitzky golay filter
        elif filter_type=='SavitzkyGolay':
            window=self.config['f_sg']['window']
            order=self.config['f_sg']['order']
            print(self.console['orange'] + 'window: %s'%(window) + self.console['ENDC'])
            print(self.console['orange'] + 'order: %s'%(order) + self.console['ENDC'])
            #breakpoint() #TODO!
            #f_x=analysis.savitzky_golay(g_x,window_size=window, order=order)
            #f_y=analysis.savitzky_golay(g_y,window_size=window, order=order)
            try:
                f_x=savgol_filter(g_x, window_length=window, polyorder=order)
                f_y=savgol_filter(g_y, window_length=window, polyorder=order)
                fxy_df = pd.DataFrame({'x':f_x, 'y':f_y, 'timestamp':g_t})
            except:
                fxy_df = None

        #mean filter
        elif filter_type=='moving average':
            weights=self.config['f_a']['weights']
            print('weights: %s'%(weights))
            weights=weights/np.sum(weights)
            print('weights: %s'%(weights))
            f_x=np.convolve(g_x, weights,'same')
            f_y=np.convolve(g_y, weights,'same')
            fxy_df = pd.DataFrame({'x':f_x, 'y':f_y, 'timestamp':g_t})

        else:
            raise ValueError('Unknown Filter Type: %s. Must be one of %s'%(filter_type,str(
                    ['sg','butter','gauss','median','moving average'])))

        return fxy_df

    def classify(self, config, df, ctype='ivt', filter_type=None,
                 v_th=None, dr_th=None, di_th=None,
                 missing=None, maxdist=None, mindur=None):
        """
        I-DT algorithm takes into account the distribution or spatial proximity of
        eye position points in the eye-movement trace.

        In the I-VT model, the velocity value is computed for every eye position
        sample. The velocity value is then compared to the threshold. If the
        sampled velocity is less than the threshold, the corresponding eye-position
        sample is marked as part of a fixation, otherwise it is marked as a part of
        a saccade.

        The simple model detects fixations, defined as consecutive samples with an
        inter-sample distance of less than a set amount of pixels (disregarding missing data)

        Parameters
        ----------
        config : :class:`dict`
            Configuration data. i.e. trial number, location.
        df : :class:`pandas.DataFrame`
            Pandas dataframe of classified data.
        ctype : :obj:`str`
            Classification type: 'ivt'
        filter_type : [type], optional
            Filter type: 'butter'
        ctype : :obj:`int`, optional
            velocity threshold (ivt), dispersion threshold (idt; used by
            SR-Research and Tobii), or simple
        v_th : :obj:`str`
            Velocity threshold in pix/sec (ivt)
        dr_th : :obj:`str`
            Fixation duration threshold in pix/msec (idt)
        di_th : :obj:`str`
            Dispersion threshold in pixels (idt)
        missing : :obj:`str`
            value to be used for missing data (simple)
        maxdist : :obj:`str`
            maximal inter sample distance in pixels (simple)
        mindur : :obj:`str`
            minimal duration of a fixation in milliseconds; detected fixation
            cadidates will be disregarded if they are below this duration  (simple)

        Raises
        ------
        ValueError
            Unknown classification type.

        Returns
        -------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of classified data.
        """
        from . import Classify

        if ctype == 'ivt':
            cnfg = self.config
            df = Classify.ivt(df, v_th, config=cnfg)

        elif ctype == 'idt':
            df = Classify.idt(df, di_th, dr_th)

        elif ctype == 'hmm':
            cnfg = self.config
            df_, cxy_df = Classify.hmm(data=df, config=cnfg, filter_type=filter_type)
            df = [df_, cxy_df]

        elif ctype == 'simple':
            df = Classify.simple(df, missing, maxdist, mindur)

        else:
            raise ValueError('Unknown classification type: %s. Must be one of %s' % (
                ctype, str(['ivt', 'idt'])))

        return df

    def roi(self, filters=[['SavitzkyGolay','sg']], flt=None, df=None, manual=False, monitorSize=None):
        """Check if fixation is within bounds.

        Attributes
        ----------
        manual : :class:`str`
            Whether or not processing.roi() is access manually.
        monitorSize : :class:`list`
            Monitor size.
        filters : :class:`list`
            Filter parameters.
        df : :class:`pandas.DataFrame`
            Pandas dataframe of classified data.

        Returns
        -------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of classified data.
        """
        #timestamp
        t0 = datetime.datetime.now()
        function = self.debug(message='t', source="timestamp")
        
        for idx, itm in enumerate(filters):
            #filter type
            flt = itm[1]
            print(self.console['orange'] + 'bounds: %s'%(itm) + self.console['ENDC'])
            
            #if not running model.roi manually (posthoc)
            if (manual == False):
                #real bounding box
                monitorSize=self.config['resolution.px']
            else:
              monitorSize = [int(i) for i in (df['monitorSize.px'].values[0]).split('x')]  

            #if x-resolution is smaller than 1400
            if monitorSize[0] < 1400:
                scaleImage = self.config['scaleImage']
                #scale container
                c = [1366*scaleImage,768*scaleImage]
                #scale stimulus
                image_x = 600*scaleImage #image size
                image_y = 600*scaleImage #image size
            #dont scale stimulus but create bounds larger than stimulus
            else:
                #scale roi #percentage of screen devoted to stim if window<=1400
                #scaleROI = (1 + (600/1400))
                #container
                c = [1366,768]
                #scale stimulus
                image_x = 600 #image size
                image_y = 600 #image size

            #centers
            cx_center = c[0]/2 #container x-center
            image_y_c = image_y/2 #roi bound y-center
            #bound_y_c = bound_y/2 #image y-center
            resx_c = monitorSize[0]/2 #resolution x-center
            resy_c = monitorSize[1]/2 #resolution y-center

            #------------------------------------------creating stim bounds
            #----------left stim bound
            lsbx1, lsbx2 = (resx_c-cx_center, resx_c-cx_center+image_x)
            lsby1, lsby2 = (resy_c+image_y_c, resy_c-image_y_c)
            #----------right stim bound
            rsbx1, rsbx2 = (resx_c+cx_center-image_x, resx_c+cx_center)
            rsby1, rsby2 = (resy_c+image_y_c, resy_c-image_y_c)
            #add to list
            stim_bounds = [dict(bID='l', bx1=lsbx1,by1=lsby1,bx2=lsbx2,by2=lsby2),
                     dict(bID='r', bx1=rsbx1,by1=rsby1,bx2=rsbx2,by2=rsby2)]
            
            #if not running processing.roi() manually (posthoc)
            if (manual == False):
                self.config['stim_bounds'] = stim_bounds

            #------------------------------------------creating roi bounds
            #----------left roi bound
            ##---region
            lbx1, lbx2 = (0, lsbx2)
            lby1, lby2 = (monitorSize[1], 0)
            ##---stim
            #lbx1, lbx2 = (lsbx1, lsbx2)
            #lby1, lby2 = (lsby2, lsby1)
            #----------right roi bound
            ##---region
            rbx1, rbx2 = (rsbx1, monitorSize[0])
            rby1, rby2 = (monitorSize[1], 0)
            ##---stim
            #rbx1, rbx2 = (rsbx1, rsbx2)
            #rby1, rby2 = (rsby2, rsby1)
            #add to list
            roi_bounds = [dict(bID='l', bx1=lbx1,by1=lby1,bx2=lbx2,by2=lby2),
                     dict(bID='r', bx1=rbx1,by1=rby1,bx2=rbx2,by2=rby2)]
            
            #if not running processing.roi() manually (posthoc)
            if (manual == False):
                self.config['roi_bounds'] = roi_bounds

            #if using eyelink data and eyelink classification
            if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                pts = np.array(df[['x', 'y']])
            #else use xy coordintes used to classify
            else:
                pts = np.array(df[['%s_x'%(flt), '%s_y'%(flt)]])

            #---------------------------------------------------------------------------------------------left bounds
            itm0 = roi_bounds[0] #x,y coordinates
            L_Bll = np.array([itm0['bx1'], itm0['by2']]) # lower-left
            L_Bur = np.array([itm0['bx2'], itm0['by1']]) # upper-right
            #bool of coordinates within and outside of bounds
            left_bound = np.all(np.logical_and(L_Bll <= pts, pts <= L_Bur), axis=1)

            #-------------------------------------------------------------------------------------------right bounds
            itm1 = roi_bounds[1] #x,y coordinates
            R_Bll = np.array([itm1['bx1'], itm1['by2']]) # lower-left
            R_Bur = np.array([itm1['bx2'], itm1['by1']]) # upper-right
            #bool of coordinates within and outside of bounds
            right_bound = np.all(np.logical_and(R_Bll <= pts, pts <= R_Bur), axis=1)

            #if not running processing.roi() manually (posthoc)
            if (manual == False):
                #-----------------------------------------------------------------get roi
                df = pd.concat([df, pd.DataFrame(np.vstack((left_bound, right_bound)).T,\
                                                 columns=['left_bound','right_bound'])], axis=1, sort=False)
                #if eyelink data
                if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                    #all fixation events
                    df['%s_fix_all'%(flt)] = df.apply(lambda x: True if (isinstance(x['fixation'], int))\
                                                      else False, axis=1)
                    #-------roi
                    #gaze and fixations within roi
                    df['%s_all_bounds'%(flt)] = df.apply(lambda x: 1 if (x['left_bound'] == True)\
                                                         else (2 if (x['right_bound'] == True) else False), axis=1)
                    ##check if sample is within bounds and part of a fixation event
                    df['%s_fix_bounds'%(flt)] = df.apply(lambda x: x['%s_all_bounds'%(flt)]\
                                                      if (isinstance(x['fixation'], int)) else False, axis=1)
                #webgazer data
                else:
                    #If enough samples
                    if (self.config['too_few_samples'] == False):
                        #-----------------------------------------------------------------all fixation events
                        df['%s_fix_all'%(flt)] = df.apply(lambda x: True if (x['%s_class'%(flt)]==1) else False, axis=1)
    
                        #fixation index - count of fixation events per trial (i.e. fixation: 1, 2, 3, 4)
                        ##drop non fixations and get index
                        p_df = df.drop(df[df['%s_fix_all'%(flt)] == False].index)
                        #-----------------------------------------------------------------fixation index
                        ##add index to dataframe #subset dataframe to single column
                        p_df['%s_fix_index'%(flt)] = range(len(p_df))
                        p_df = p_df[['%s_fix_index'%(flt)]]
                        ##add column to original dataframe
                        df = df.join(p_df)
                        #replace np.nan with "." (for R)
                        # df['%s_fix_index'%(flt)].where((df['%s_fix_index'%(flt)].notnull()), ".", inplace=True)
                        #------------------------------------fixation counter
                        #enumerate
                        df['enum'] = ((df['%s_fix_all'%(flt)] != df['%s_fix_all'%(flt)].shift(1)).cumsum()-1)
                        #reset non-fixations as None
                        df['fix_num'] = df.apply(lambda x: float(x['enum']) if (x['%s_fix_index'%(flt)] != '.') else None, axis=1)
                        #factorize and reset #finished
                        df['fix_num'] = pd.factorize(df['fix_num'])[0]
                        df['fix_num'] = df.apply(lambda x: float(x['fix_num']) if (x['%s_fix_index'%(flt)] != '.') else None, axis=1)
                        #------------------------------------roi
                        ##gaze and fixations within roi
                        df['%s_all_bounds'%(flt)] = df.apply(lambda x: 1 if (x['left_bound'] == True)\
                                                             else (2 if (x['right_bound'] == True) else "."), axis=1)

                        ##only fixation within roi
                        df['%s_fix_bounds'%(flt)] = df.apply(lambda x: x['%s_all_bounds'%(flt)]\
                                                          if (x['%s_class'%(flt)]!=None) else ".", axis=1)
                
                        ##only fixation within roi
                        df['%s_fix_bounds_old'%(flt)] = df.apply(lambda x: x['%s_all_bounds'%(flt)]\
                                                          if (x['%s_class'%(flt)]==1) else ".", axis=1)
                        
                        #------------------------------------total samples (left and right dwell) counter
                        df['sample_total'] = df.shape[0]
                    
                        #----calculate dwell time
                        df['dwell'] = df.apply(lambda x: True if (x['left_bound']==True or x['right_bound']==True) else False, axis=1)

                    #not enough samples
                    else:
                        not_enough_samples = 'subject: %s, trial: %s; not enough samples'%(self.config['subject'], self.config['trial'])
                        self.debug(not_enough_samples)
                        print(self.console['red'] + not_enough_samples + self.console['ENDC'])
                        #add blank for fixation
                        df['%s_fix_index'%(flt)] = "."
                        df['%s_fix_all'%(flt)] = "."
                        df['fix_num'] = "."
                        df['%s_all_bounds'%(flt)] = "."
                        df['%s_fix_bounds'%(flt)] = "."
                        df['%s_fix_bounds_old'%(flt)] = "."
                        df['dwell'] = "."
                        df['sample_total'] = df.shape[0]
            #----------------------------------------------------------------------------------------test confirmation
            test = False
            if test and (self.config['subject'] != self.current_subject):
                self.current_subject = self.config['subject']
                import matplotlib
                matplotlib.use('Agg')
                import matplotlib.pyplot as plt
                import matplotlib.patches as patches
                print(self.console['green'] + 'Preprocessing: Test to ensure ROI' + self.console['ENDC'])

                #plot
                #draw cross ###af2f2c #draw square ##2222b2 #draw triangle ##198D40
                plt.figure(4, figsize=(9.6,5.4))
                test = plt.gca()

                #roi bounding boxes #lbx1, lbx2, lby1, lby2 #rbx1, rbx2, rby1, rby2
                test.add_patch(patches.Rectangle((lbx1,lby2),width=lbx2,height=lby1,linewidth=1,facecolor='#396cbd33'))
                test.add_patch(patches.Rectangle((rbx1,rby2),width=rbx2,height=rby1,linewidth=1,facecolor='#396cbd33'))

                #gaze coordinates
                test.plot(df['%s_x'%(flt)], df['%s_y'%(flt)], marker='+', markerfacecolor="#ffffff00",
                          markersize=6, markeredgecolor='#af2f2c', linewidth=0)

                #all fixations
                p_df = df.drop(df[df['%s_fix_all'%(flt)] == False].index)
                test.plot(p_df['%s_x'%(flt)], p_df['%s_y'%(flt)], marker='s', markerfacecolor="#ffffff00",
                          markersize=6, markeredgecolor='#2222b2', linewidth=0)

                #only fixations within roi
                p_df = df[(df['%s_fix_all'%(flt)] == True) & (df['%s_fix_bounds'%(flt)] != ".")]
                test.plot(p_df['%s_x'%(flt)], p_df['%s_y'%(flt)], marker='^', markerfacecolor="#ffffff00",
                          markersize=6, markeredgecolor='#198D40', linewidth=0)

                #set limits
                test.set_xlim([0,monitorSize[0]])
                test.set_ylim([0,monitorSize[1]])

                #position
                ###########left_image x0, left_image x1, center, right_image x0, right_image x1
                x_ticks = [roi_bounds[0]['bx1'], roi_bounds[0]['bx2'], resx_c, roi_bounds[1]['bx1'], roi_bounds[1]['bx2']]
                ##########image y0, center, image y1
                y_ticks = [roi_bounds[0]['by1'], resy_c, roi_bounds[0]['by2']]
                #set ticks
                test.set_xticks(x_ticks)
                test.set_yticks(y_ticks)
                x_ticks.sort()
                y_ticks.sort()
                test.grid(linestyle='--')
                plt.gca().invert_yaxis()
                #plt.show()

                #save
                dpi = self.config['fig_dpi']
                emotion = self.config['emotion']
                resolution = self.config['resolution.px']
                img_title = 'gaze coordinates [subject:%s, session:%s, trial:%s, isCongruent:%s, left:%s, right:%s (%s, %s)]'\
                                                %(self.config['subject'],self.config['session'],self.config['trial'],\
                                                self.config['isCongruent'],emotion[0],emotion[1],\
                                                resolution[0],resolution[1])
                plt.suptitle(img_title, fontsize=12)
                save_folder = os.path.abspath(self.config['path']['output']+ '/test/img/%s_%s_%s-roiPlot.png'\
                                              %(self.config['subject'],self.config['session'],self.config['trial']))
                plt.savefig(save_folder, dpi=dpi,transparent=False)
                plt.close()
            
            #--------finished
            #timestamp
            print(self.console['blue']+'%s finished in %s msec'%(function,
                  ((datetime.datetime.now()-t0).total_seconds()*1000))+self.console['ENDC'])   
            #if not running processing.roi() manually (posthoc)         
            if (manual == False):
                return df
            else:
                return stim_bounds, roi_bounds

    def process(self, window, filters, gxy_df, trial, _classify=True, ctype='simple', _param='', log=False,
                 draw_plot=False,  draw_heatmap=False, draw_gazeplot=False, draw_fixplot=False,
                 v_th=20,dr_th=200,di_th=20,
                _missing=0.0, _maxdist=25, _mindur=50):
        """
        Plotting and preparing data for classification. Combined plot of each filter.

        Parameters
        ----------
        window : :obj:`list`
            horizontal, vertical resolution
        filters : :obj:`list`
            List of filters along with short-hand names.
        gxy_df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data. Unfiltered raw data.
        trial : :obj:`str`
            Trial number.
        _classify : :obj:`bool`
            parameter to include classification
        ctype : :obj:`str`
            classification type. simple, idt, ivt
        _param : :obj:`str`
            [description] (the default is '', which [default_description])
        log : :obj:`bool`
            [description] (the default is False, which [default_description])
        draw_plot : bool, optional
            [description] (the default is False, which [default_description])
        draw_heatmap : bool, optional
            [description] (the default is False, which [default_description])
        draw_gazeplot : bool, optional
            [description] (the default is False, which [default_description])
        draw_fixplot : bool, optional
            [description] (the default is False, which [default_description])
        v_th : :obj:`str`
            Velocity threshold in px/sec (ivt)
        dr_th : :obj:`str`
            Fixation duration threshold in px/msec (idt)
        di_th : :obj:`str`
            Dispersion threshold in px (idt)
        _missing : :obj:`bool`
            value to be used for missing data (simple)
        _maxdist : :obj:`str`
            maximal inter sample distance in pixels (simple)
        _mindur : :obj:`str`
            minimal duration of a fixation in milliseconds; detected fixation
            cadidates will be disregarded if they are below this duration  (simple)
            (default = 100)

        Attributes
        ----------
        _fxy_df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data. Filtered data. Subset of _fgxy_df.

        Returns
        -------
        _fgxy_df : :class:`pandas.DataFrame`
            Pandas dataframe of filtered data.
        c_xy : :class:`pandas.DataFrame`
                Pandas dataframe of classified data.
        """

        #%matplotlib inline
        #append filtered and raw data to list being prepared for export
        l_gf = []
        l_cxy = []
        #append raw data
        l_gf.append(gxy_df)
        
        for idx, itm in enumerate(filters):
            print(self.console['orange'] + 'filter: %s' % (itm[0]) + self.console['ENDC'])
            #-------------------------------------------------------------------------parameters
            c_xy = []  # classify data

            #if using filter
            if itm[0] != 'none':
                fxy_df = self.filter_data(gxy_df, itm[0], self.config)
            else:
                fxy_df = gxy_df

            #too few samples, trial should be passed
            if fxy_df is None:
                print(self.console['orange'] + 'too few samples' + self.console['ENDC'])
                fxy_df = gxy_df
                self.config['too_few_samples'] = True

            fxy_df = fxy_df.reset_index(drop=True)

            #------------------------------------------------------------fixation classification techniques
            #store fixations from eyelink
            if (self.config['source'] == 'eyelink'):
                eyelink_c_xy = self.cgxy

            #use eyelink calculated fixations if config.classify_eyelink = False
            if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                c_xy = self.cgxy
                ctype = 'eyelink'

            if ctype == 'idt':
                # if eyelink and using original fixations
                if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                  pass
                else:
                    c_xy = self.classify(self, df=fxy_df, dr_th=dr_th, di_th=di_th, ctype=ctype)

            if ctype == 'ivt':
                # if eyelink and using original fixations
                if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                  pass
                else:
                    c_xy = self.classify(self, self.config, fxy_df, v_th=v_th, ctype=ctype)

            if ctype == 'hmm':
                # if eyelink and using original fixations
                if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                  pass
                # if if samples are too few
                elif (self.config['too_few_samples']):
                  pass
                else:
                    dfc_xy = self.classify(self.config, df=fxy_df, ctype=ctype, filter_type=itm[1])
                    fxy_df = dfc_xy[0]
                    c_xy = dfc_xy[1]
                    del dfc_xy

            elif ctype == 'simple':
                # if eyelink and using original fixations
                if ((self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == False)):
                  pass
                else:
                    c_xy = self.classify(self.config, fxy_df, ctype=ctype,missing=_missing, maxdist=_maxdist, mindur=_mindur)
                    c_xy = pd.DataFrame(c_xy[1], columns=['start', 'end', 'duration', 'cx', 'cy'])

            #print eyelink orignal fixations
            if (self.config['source'] == 'eyelink'):
                print(self.console['green'] + 'eyelink fixations' + self.console['ENDC'])
                print(eyelink_c_xy)

            #print calculated fixations if from webgazer or calculating eyelink data
            if ((self.config['source'] == 'webgazer') or
                    (self.config['source'] == 'eyelink') and (self.config['classify_eyelink_data'] == True)):
                print(self.console['orange'] + 'calculated fixations' + self.console['ENDC'])
                #print(c_xy)

            #append filted data
            #_fgxy_df = append_data(gxy_df, fxy_df, itm[1])
            l_cxy.append(c_xy)
            if itm[0] != 'none':
                f_x = "%s_x" % (itm[1])
                f_y = "%s_y" % (itm[1])
            else:
                f_x = 'x'
                f_y = 'y'

            #class variable is created from hmm classification
            if (ctype == 'hmm') and (self.config['too_few_samples'] == False)\
                    and (set(["%s_class" % (itm[1])]).issubset(fxy_df.columns)):
                fxy_df = fxy_df[['x', 'y', "%s_class" % (itm[1])]]
            else:
                fxy_df["%s_class" % (itm[1])] = None
                fxy_df = fxy_df[['x', 'y', "%s_class" % (itm[1])]]

            #rename and append filtered x and y-axis
            fxy_df = fxy_df.rename(index=str, columns={"x": f_x, "y": f_y})
            l_gf.append(fxy_df)

        #combine list of all filtered and raw data
        for indx, item in enumerate(l_gf):
            l_gf[indx].index = range(len(l_gf[indx].index))
        fgxy_df = pd.concat(l_gf, axis=1, join_axes=[l_gf[0].index])

        return l_cxy, fgxy_df

    def append_classify(self, df, cg_df):
        """Appending classification to Dataframe.

        Parameters
        ----------
        df : :obj:`list`
            Pandas dataframe of raw data.
        gxy_df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data of classification events.
        """
        for index, item in enumerate(cg_df):
            count = self.filters[index][1] + '_FID'
            for idx, rw in item.iterrows():
                start = rw['start']
                end = rw['end']

                #interval
                df.loc[df['timestamp'].between(start, end, inclusive=True), count] = idx

        return df

    def run(self, path, task_type="eyetracking", single_subject=False, single_trial=False, subject=0, trial=0, isMultiprocessing=True, cores=1):
        """Processing of data. Steps here include: cleaning data, fixation identification, and exporting data.

        Parameters
        ----------
        path : :obj:`string`
            Path of raw data.
        task_type : :obj:`string`
            Running analysis on `eyetracking` or `behavioral` data.
        single_subject : :obj:`bool`
            Whether to run function with all or single subject.
        single_trial : :obj:`bool`
            Whether to run function with all or single trial.
        subject : :obj:`int`
            Subject number. Only if single_subject = True.
        trial : :obj:`int`
            Trial number. Only if single_trial = True.
        isMultiprocessing : :obj:`bool`
            Whether multiprocessing of data will be used. Only if single_subject = False.
        cores : :obj:`int`
            Number of cores to use for multiprocessing. Only if single_subject = False & isMultiprocessing=True.
        
        Attributes
        ----------
        process : :obj:`bool`
            Process all data for export.
        """

        #----set config
        #set path
        self.config['path'] = path + '/' + self.config['task']
        # single_subject
        self.config['single_subject'] = single_subject
        # is single_trial
        self.config['single_trial'] = single_trial
        # subject and trial number
        self.config['subject'] = subject
        self.config['trial'] = trial
        # classification type
        ctype = self.config['ctype']
        # classification parameters
        missing=self.config['missing']
        maxdist=self.config['maxdist']
        mindur=self.config['mindur']
        v_th=self.config['v_th']
        dr_th=self.config['dr_th']
        di_th=self.config['di_th']

        #single subject
        if (self.config['single_subject']):
            print(self.console['orange'] + 'start-----------------' + self.console['ENDC'])
            print(self.console['orange'] + 'single_subject = %s, single_trial = %s'%(single_subject, single_trial) + self.console['ENDC'])
            print(self.console['orange'] + 'importing raw data' + self.console['ENDC'])
            #get core number and set as global variable
            self.thisCore = 0
            #get logger and set as global variable
            self.log=logging.getLogger(__name__)
            
            #get data
            gxy_df, df_path = self.getData()

            #check if eyetracking, else go to next subject
            isEyetracking = gxy_df['type'][0]
            if isEyetracking != 'eyetracking':
                print(self.console['orange'] + 'finished-----------------' + self.console['ENDC'])
                return

            #drop practice and sort
            gxy_df = gxy_df.drop(gxy_df[(gxy_df['event']=='Prac')].index)
            gxy_df = gxy_df.sort_values(['TrialNum','timestamp','sampleNum'], ascending=[True, True, True]).reset_index(drop=True)

            #if single trial
            if self.config['single_trial']:
                l_trials = [trial]
            else:
                #get list of all possible trials to pull data from
                l_trials = gxy_df['TrialNum'].unique()
        
                #remove nan from behavioral list (nan occurs when row trial_type == instructions)
                if (task_type == "behavioral"):
                    l_trials = [x for x in l_trials if not np.isnan(x)]

            #------------------------------------------------for each trial
            l_fgxy = []
            #start
            for idx in l_trials:
                #reset blocker for too few trials in filtering
                self.config['too_few_samples'] = False

                #set config trial number
                self.config['trial'] = idx
                print(self.console['orange'] + 'subject: %s'%(self.config['subject']) + self.console['ENDC'])
                print(self.console['orange'] + 'session: %s'%(self.config['session']) + self.console['ENDC'])
                print(self.console['orange'] + 'trial: %s'%(self.config['trial']) + self.console['ENDC'])

                #filter data to single trial
                df = gxy_df[gxy_df['TrialNum'] == idx].reset_index(drop=True)

                #get isCongruent
                if df['isCongruent'][0]:
                    self.config['isCongruent'] = 'Congruent'
                else:
                    self.config['isCongruent'] = 'Incongruent'

                #get emotion of left and right stimuli
                self.config['emotion'] = [df['left_mood'][0], df['right_mood'][0]]

                #1. preprocess data
                #get monitorSize
                monitorSize = (df['monitorSize.px'][0]).split('x')
                ##remove devicePixelRatio from monitor size
                monitorSize[0] = float(monitorSize[0]) / df['devicePixelRatio'][0]           
                monitorSize[1] = float(monitorSize[1]) / df['devicePixelRatio'][0]
                #store
                monitorSize = list(map(int, monitorSize))
                self.config['resolution.px'] = monitorSize
                #reset and store previous version as 'monitorSize_old'
                df['monitorSize_old'] = df['monitorSize.px']
                df['monitorSize.px'] = '%sx%s'%(monitorSize[0],monitorSize[1])
                
                #get scale
                ##scale container and stimulus if x-resolution is smaller than 1400
                if monitorSize[0] < 1400:
                    scaleImage = monitorSize[0]/1400
                ##dont scale
                else:
                    scaleImage = 1
                self.config['scaleImage'] = scaleImage
                ##preprocess
                df = self.preprocess(df, monitorSize)

                #get eyelink fixations
                print(self.console['blue'] + 'importing eyelink fixations' + self.console['ENDC'])
                if (self.config['source'] == 'eyelink'):
                    self.cgxy = self.eyelink_classify()

                #process data
                print(self.console['blue'] + 'processing data' + self.console['ENDC'])
                cgxy_df, fgxy_df = self.process(monitorSize, self.filters, df, self.config['trial'],
                                                _classify=self.config['classify'], ctype=ctype,
                                               _missing=missing, _maxdist=maxdist, _mindur=mindur,
                                               v_th=v_th, dr_th=dr_th, di_th=di_th)       

                #append classify to dataframe
                if self.config['classify']:
                    if self.config['ctype'] != 'hmm':
                        fgxy_df = self.append_classify(fgxy_df, cgxy_df)
                    #apply bounds on fixations
                    else:
                        fgxy_df=self.roi(filters=self.filters, flt=self.filters[0][1], df=fgxy_df)

                #check if all samples are flagged as fixations
                flt = self.filters[0][1]
                samples_fix_err = fgxy_df[fgxy_df["%s_fix_all"%(flt)]==True].count()["%s_fix_all"%(flt)]
                samples = len(fgxy_df)
                if samples_fix_err == samples:
                    fgxy_df['samples_fix_err'] = True
                else:
                    fgxy_df['samples_fix_err'] = False

                #sort
                fgxy_df = fgxy_df.sort_values(['TrialNum','sampleNum'],ascending=[True, True]).reset_index(drop=True)

                #append to ltrials, if there are at least 20 samples
                #this will be used to rebuild new dataframe for subject
                if (fgxy_df.shape[0] >= 1):
                    print(self.console['green'] + 'Preprocessing: trials with at least 20 samples' + self.console['ENDC'])
                    l_fgxy.append(fgxy_df)

            #combine list of dataframes into new dataframe
            df = pd.concat(l_fgxy, sort=False, ignore_index=True)
            df = df.sort_values(['TrialNum','sampleNum'],ascending=[True, True]).reset_index(drop=True)

            #save data
            print(self.console['blue'] + 'saving data' + self.console['ENDC'])
            subject = int(self.config['subject'])
            session = self.config['session']
            if self.config['save_data']:
                if self.config['single_trial']:
                    f_path = self.config['path']['processed'] + '/data/' + self.config['type'] + '/%s_%s_%s.csv'%(subject,session,trial)
                else:
                    f_path = self.config['path']['processed'] + '/data/' + self.config['type'] + '/%s_%s.csv'%(subject,session)
                #save
                df.to_csv(f_path, index=False)

            #finish
            return l_fgxy, cgxy_df, fgxy_df
        
        #all subjects
        elif (not self.config['single_subject']):
            print(self.console['orange'] + 'start-----------------' + self.console['ENDC'])
            print(self.console['orange'] + 'single_subject = %s, single_trial = %s'%(single_subject, single_trial) + self.console['ENDC'])
            print(self.console['blue'] + 'importing raw data' + self.console['ENDC'])
            #--------------------------------------------------for each subject
            def all_subjects(fdir, core):
                try:        
                    #for each file
                    for sbj in fdir:
                        print(self.console['blue'] + 'subject: %s'%(sbj) + self.console['ENDC'])
                        #set subject name, session
                        p = Path(sbj)
                        _subject, _session = (p.name.replace('abc', '').replace('.csv', '')).split("_", 1)
                        self.config['subject'] = _subject
                        self.config['session'] = _session
    
                        #get data
                        gxy_df, df_path = self.getData(path=sbj)
    
                        #if looking at eyetracking data
                        if (task_type == "eyetracking"):
                            #check if behavioral, else skip and go to next subject
                            isEyetracking = gxy_df['type'][0]
                            if isEyetracking != 'eyetracking':
                                print(self.console['orange'] + 'finished subject' + self.console['ENDC'])
                                continue
                            else:
                                pass
                        #else looking at behavioral data
                        elif (task_type == "behavioral"):
                            #check if behavioral, else skip and go to next subject
                            isBehavioral= gxy_df['type'][0]
                            if isBehavioral != 'behavioral':
                                print(self.console['orange'] + 'finished subject' + self.console['ENDC'])
                                continue
                            else:
                                pass
    
                        #drop practice and sort
                        gxy_df = gxy_df.drop(gxy_df[(gxy_df['event']=='Prac')].index)
                        gxy_df = gxy_df.sort_values(['TrialNum','timestamp','sampleNum'],ascending=[True, True, True]).reset_index(drop=True)

                        #if single trial
                        if self.config['single_trial']:
                            l_trials = [trial]
                        #else all trials
                        else:
                            #get list of all possible trials to pull data from
                            l_trials = gxy_df['TrialNum'].unique()
        
                            #remove nan from behavioral list (nan occurs when row trial_type == instructions)
                            if (task_type == "behavioral"):
                                l_trials = [x for x in l_trials if not np.isnan(x)]
                        
                        #------------------------------------------------for each trial
                        l_fgxy = []
                        #start
                        for idx in l_trials:
                            #reset blocker for too few trials in filtering
                            self.config['too_few_samples'] = False
    
                            #set config trial number
                            self.config['trial'] = idx
                            print(self.console['orange'] + 'subject: %s'%(_subject) + self.console['ENDC'])
                            print(self.console['orange'] + 'session: %s'%(_session) + self.console['ENDC'])
                            print(self.console['orange'] + 'trial: %s'%(self.config['trial']) + self.console['ENDC'])
    
                            #filter data to single trial
                            df = gxy_df[gxy_df['TrialNum'] == idx].reset_index(drop=True)                   
    
                            #get isCongruent
                            if df['isCongruent'][0]:
                                self.config['isCongruent'] = 'Congruent'
                            else:
                                self.config['isCongruent'] = 'Incongruent'
    
                            #get emotion of left and right stimuli
                            self.config['emotion'] = [df['left_mood'][0], df['right_mood'][0]]
                           
                            #get monitorSize
                            monitorSize = (df['monitorSize.px'][0]).split('x')
                            ##remove devicePixelRatio from monitor size
                            monitorSize[0] = float(monitorSize[0]) / df['devicePixelRatio'][0]           
                            monitorSize[1] = float(monitorSize[1]) / df['devicePixelRatio'][0]
                            ##store
                            monitorSize = list(map(int, monitorSize))
                            self.config['resolution.px'] = monitorSize
                            #reset and store previous version as 'monitorSize_old'
                            df['monitorSize_old'] = df['monitorSize.px']
                            df['monitorSize.px'] = '%sx%s'%(monitorSize[0],monitorSize[1])
                            
                            #get scale
                            ##scale container and stimulus if x-resolution is smaller than 1400
                            if monitorSize[0] < 1400:
                                scaleImage = monitorSize[0]/1400
                            ##dont scale
                            else:
                                scaleImage = 1
                            self.config['scaleImage'] = scaleImage
                            
                            #1. preprocess data
                            ## only if eyetracking data
                            if (task_type == "eyetracking"):
                                ##preprocess
                                df = self.preprocess(df, monitorSize)
        
                                #get eyelink fixations
                                print(self.console['blue'] + 'importing eyelink fixations' + self.console['ENDC'])
                                if (self.config['source'] == 'eyelink'):
                                    self.cgxy = self.eyelink_classify()
    
                                #process data, if eyetracking
                                print(self.console['blue'] + 'processing data' + self.console['ENDC'])
                                cgxy_df, fgxy_df = self.process(monitorSize, self.filters, df, self.config['trial'],
                                                                _classify=self.config['classify'],
                                                               ctype=ctype,
                                                               draw_plot=self.config['draw_plot'],
                                                               draw_heatmap=self.config['draw_heatmap'],
                                                               draw_gazeplot=self.config['draw_gazeplot'],
                                                               draw_fixplot=self.config['draw_fixplot'],
                                                               _missing=missing, _maxdist=maxdist, _mindur=mindur,
                                                               v_th=v_th, dr_th=dr_th, di_th=di_th)
    
                                #append classify to dataframe
                                if self.config['classify']:
                                    if self.config['ctype'] != 'hmm':
                                        fgxy_df = self.append_classify(fgxy_df, cgxy_df)
                                    #apply bounds on fixations
                                    else:
                                        fgxy_df=self.roi(filters=self.filters, flt=self.filters[0][1], df=fgxy_df)
                                
                                #check if all samples are flagged as fixations
                                flt = self.filters[0][1]
                                samples_fix_err = fgxy_df[fgxy_df["%s_fix_all"%(flt)]==True].count()["%s_fix_all"%(flt)]
                                samples = len(fgxy_df)
                                if samples_fix_err == samples:
                                    fgxy_df['samples_fix_err'] = True
                                else:
                                    fgxy_df['samples_fix_err'] = False
    
                                #sort
                                fgxy_df = fgxy_df.sort_values(['TrialNum','sampleNum'],
                                                              ascending=[True, True]).reset_index(drop=True)
                            # else if behavioral data continue
                            elif (task_type == "behavioral"):
                                fgxy_df = df
    
                            #append to ltrials
                            #this will be used to rebuild new dataframe for subject
                            if (fgxy_df.shape[0] >= 1):
                                l_fgxy.append(fgxy_df)
    
                        #combine list of dataframes into new dataframe
                        df = pd.concat(l_fgxy, sort=False, ignore_index=True)
                        df = df.sort_values(['TrialNum','sampleNum'],ascending=[True, True])\
                                .reset_index(drop=True)
    
                        #save data
                        print(self.console['blue'] + 'saving data' + self.console['ENDC'])
                        subject = int(self.config['subject'])
                        session = self.config['session']
                        if self.config['save_data']:
                            if self.config['single_trial']:
                                f_path = self.config['path']['processed'] + '/data/' + self.config['type'] + '/%s_%s_%s.csv'%(subject,session,trial)
                            else:
                                f_path = self.config['path']['processed'] + '/data/' + self.config['type'] + '/%s_%s.csv'%(subject,session)
                            #save
                            df.to_csv(f_path, index=False)
                            
                #--------------------------------------------------------------------------------------------------end
                #if all_subjects fails, save to log            
                except Exception as e:
                    self.log.error(e, exc_info=True)
                    
            #--------------------------------------------------prepare
            #multithreading
            #list of behavioral and eyetracking

            import multiprocessing
            
            #prepare collecting arguements
            arg = []

            #get directory
            fdir = glob.glob(os.path.join(self.config['path'] + "/*.csv"))
            
            #get cpu cores to be used
            cores = self.config['cores']

            #if requested cores is 1, run without multiprocessing
            if (cores == 1):
                isMultiprocessing = False
            ##if requested cores are less than/equal 7, and less than available cores plus 1
            elif (cores <= 7) and (multiprocessing.cpu_count() >= cores + 1):
                isMultiprocessing = True
                fdir_chunk = np.array_split(fdir, cores)
                for index in range(0, cores):
                    arg.append((fdir_chunk[index],index))
            ##else use less than half of total available cores
            else:
                isMultiprocessing = True
                cores = int(self.config['cores']/2)
                fdir_chunk = np.array_split(fdir, cores)
            #breakpoint()

            #------------------------------------------run multiprocessing
            #if not multiprocessing
            if not isMultiprocessing:
                all_subjects(fdir, cores)
            #else multiprocessing
            else:
                proc = [multiprocessing.Process(target=all_subjects,\
                        args=(fdir_chunk[x].tolist(), x)) for x in range(cores)]
                for p in proc:
                    p.daemon = True
                    p.start()

            #-----------------------------------------finished
            return cores, arg, proc

    def subject_metadata(self, fpath, spath):
        """
        Collect all subjects metadata.
        
        Parameters
        ----------
        fpath : :obj:`str`
            The directory path of all participant data.
        spath : :obj:`str`
            The directory path of all participant data.
            
        Returns
        -------
        df : :class:`ndarray`
            Pandas dataframe of subject metadata.
        """
        
        #----for timestamp
        _t0 = datetime.datetime.now()
        _f = self.debug(message='t', source="timestamp")
        print(self.console['blue'] + 'running metadata.summary()' + self.console['ENDC'])
        
        #----get directory
        fdir = glob.glob(fpath + "/*.csv")
        
        #----store metadata
        l_sub = []
        
        #----for each subject
        for index, sbj in enumerate(fdir):
            #read csv
            df = pd.read_csv(sbj)
            
            #add filename to df
            df['file'] = sbj
            
            #collect metadata for output by getting first row
            l_sub.append(df[df['trial_type'] == 'dotprobe-task'].iloc[0])

        #----convert list to dataframe
        df = pd.concat(l_sub, axis=1, keys=[s.name for s in l_sub], sort=False).T.reset_index(drop=True)
        
        #----format metadata and save
        df = Metadata.summary(df=df, path=spath)
                
        #----end
        print(self.console['blue']+'%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000))+self.console['ENDC'])
        
        return df
           
    def variables(self,df):
        """Output list of variables for easy html viewing.

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data. This is used as a filter to prevent unused participants from being included in the data.
        path : :obj:`str`
            The directory path save and read the hdf5 dataframe.

        Returns
        -------
        df_definitions : :class:`pandas.DataFrame`
        """
        #blank df for appending
        df_variable = pd.DataFrame()
        
        source = {
            'bias': ['init_gaze_bias','final_gaze_bias','gaze_bias','n_gaze_valid','dp_bias','var_dp_bias','n_dp_valid'],
            'demographic':['race','is_normalvision','is_student'],
            'behavioral': ['m_rt','accuracy','m_diff_stim','m_diff_dotloc'],
            'clinical': ['cesd_score','cesd_group','rrs_brooding'],
            'device': ['os','os_version','gpu','gpu_type','browser','browser_version', 'devicePixelRatio','monitorSize',
                       'windowSize','heap.used','heap.limit','WebcamMessage','webcamSize','webcam_brand','luminance',
                       'isPageVisible','is_calibrated','is_eyetracking','isFullscreen'],
            'other': ['nested']
        }
        
        #for each source
        for key, row in source.items():
            #convert to correct formats
            df_ = df[row].iloc[:2].loc[0,:].reset_index().rename(columns={'index':'variable', 0:'example'})
            
            #add column for definitions, type; reorganize
            df_['type'] = df[row].dtypes.to_frame().reset_index().rename(columns={0:'type'})['type']
            df_['group'] = key
            df_ = df_.loc[:,['variable','type','example','group']]
            
            #if key == behavioral, add row for trialnum, and trialnum_
            if key=='behavioral':
                df_.loc[-1] = ['TrialNum','int64',1,'behavioral']
                df_.loc[-1] = ['TrialNum_','int64',1,'behavioral']
                df_.loc[-1] = ['trialType','int64',1,'behavioral']
                df_.loc[-1] = ['trialType_','object','iaps','behavioral']
            
            #append
            df_variable = df_variable.append(df_)
            
        #reset index
        df_variable = df_variable.reset_index(level=0, drop=True)
             
        #import list of definitions and add to dataframe
        #to initially get list of variable to fill in definitions #df_variable.to_csv(definitions_path, index=None)
        
        #import definitions and merge to variables list
        definitions_path = self.config['path']['output'] + "/analysis/definitions.csv"
        df_definitions = pd.read_csv(definitions_path, float_precision='high')
        df_variable = pd.merge(df_variable, df_definitions, on='variable')
        
        #change order
        df_variable = df_variable[['variable','group','type','example','definition']]
        
        return df_variable
    
    def dwell(self, df, cores=1):
        """
        Calculate dwell time for sad and neutral images.

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Pandas dataframe of raw data. This is used as a filter to prevent unused participants from being included in the data.
        cores : :class:`int`    
            Number of cores to use for multiprocessing.

        Returns
        -------
        df : :class:`pandas.DataFrame`
            Pandas dataframe with dwell time.
        error : :class:`list`
            List of participants that were not included in dataframe.
        """
        import multiprocessing, itertools
        
        #----for timestamp
        _t0 = datetime.datetime.now()
        _f = self.debug(message='t', source="timestamp")
        print(self.console['blue'] + 'running dwell()' + self.console['ENDC'])
        
        #----run
        def run(dir_=None, core=None, queue=None):
            print(self.console['green'] + 'processing.dwell.run(%s)'%(core) + self.console['ENDC'])
            dwell = []
            #----for each subject
            for index, row in dir_.iterrows():
                _path_ = row['path']
                _subject = row['participant']
                
                #----read csv as dataframe
                df_ = pd.read_csv(_path_, float_precision='high', low_memory=False)
                print('subject: %s; core: %s'%(_subject, core))
                
                #----if 198 trials continue else skip
                if (df_.drop_duplicates(subset="TrialNum", keep="first").shape[0] == 198):
                    #----for each trial
                    for _trial in range(0,198):
                        try:                            
                            #----keep relevant trial
                            df_0 = df_.loc[df_['TrialNum'] == _trial].reset_index(drop=True)
                            
                            #----get trialType 
                            _trialType = df_0['trialType'][0]
                        
                            #----drop columns
                            df_0 = df_0[['participant','TrialNum','timestamp','marker','dwell','trialType',
                                         'left_mood','right_mood','left_bound','right_bound']]
                            
                            #----get range between "stimulus onset" and "dotloc onset"
                            #get start and end markers
                            start_m = df_0[df_0['marker'] == "Stimulus Onset"].index.item()
                            end_m = df_0[df_0['marker'] == "Dotloc Onset"].index.item()
                            
                            #get dataframe
                            df_1 = df_0.iloc[start_m:end_m+1,:].reset_index(drop=True)
                            
                            #get difference between timestamp values
                            df_1['difference'] = df_1['timestamp'].shift(-1) - df_1['timestamp']              
                            
                            #----get location of sad/neutral images
                            if ((df_1['left_mood'][0]=='Sad') and (df_1['right_mood'][0]=='Neutral')):
                                sad = 'left_bound'
                                neutral = 'right_bound'
                            else:
                                neutral = 'left_bound'
                                sad = 'right_bound'
                            
                            #----get emotional dwell number of samples, if gaze is within dwell location                     
                            # nested by aoi (for within-group analysis)
                            ##neutral
                            df_neutral = df_1[(df_1[neutral]==True)]
                            ## subject, trial, aoi, dwell_num, dwell_time
                            dwell.append([_subject, _trial, _trialType, 'neutral', df_neutral.shape[0], df_neutral['difference'].sum()])
                            ##sad
                            df_sad = df_1[(df_1[sad]==True)]
                            ## subject, trial, aoi, dwell_num, dwell_time
                            dwell.append([_subject, _trial, _trialType, 'sad', df_sad.shape[0], df_sad['difference'].sum()])
                            
                        #if exception
                        except Exception as e:
                            line = sys.exc_info()[-1].tb_lineno
                            print('subject: %s; trial: %s; error: %s; line: %s'%(_subject, _trial, e, line))
                        
                else:
                    print('subject:%s; error:too few trials'%(_subject))
            
            #----add to multithreading queue
            if isMultiprocessing:
                #queue
                queue.put(dwell)
                
            if not isMultiprocessing:
                return dwell
        
        #----finished
        def finished(output, error=None):
            print(self.console['green'] + 'processing.dwell.finished()' + self.console['ENDC'])
            if isMultiprocessing:
                #----create output df
                df = pd.DataFrame(list(itertools.chain(*output)),
                                  columns=['participant','trial','trialType','aoi','dwell_num','dwell_time'])
                
                #----create error df
                #check if data came out correctly by looking at ampunt of trials and participants outputted
                error = df.groupby(['participant','aoi']).agg(['count'])
            else:
                #----create output df
                df = pd.DataFrame(output, columns=['participant','trial','trialType','aoi','dwell_num','dwell_time'])
                #check if data came out correctly by looking at ampunt of trials and participants outputted
                error = df.groupby(['participant','aoi']).agg(['count'])
            
            #----end
            #timestamp
            print(self.console['blue']+'%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000))+self.console['ENDC'])
            return df, error
        
        #--------------------get list of all participants
        ##get directory
        _dir = glob.glob(os.path.join(self.config['path']['processed'] + '/data/eyetracking' + "/*.csv"))
        _sbj_session = [(Path(x).name.replace('abc', '').replace('.csv', '')).split("_", 1) for x in _dir]
        dir_ = [[z,*x] for z,x in zip(_dir,_sbj_session)]
        dir_ = pd.DataFrame(dir_, columns=['path','participant','session'])

        #------------------------------------------check if running using multiprocessing
        #----get cores
        ##if requested cores is 1, run without multiprocessing
        if ((cores == 0) or (cores == 1)):
            isMultiprocessing = False
            print(self.console['green'] + 'processing.dwell() not multiprocessing' + self.console['ENDC'])
        ##else if requested cores are less than/equal 7, and less than available cores plus 1
        elif ((cores <= 7) and (multiprocessing.cpu_count() >= cores + 1)):
            isMultiprocessing = True
            dir_p = np.array_split(dir_, cores)
            print(self.console['green'] + 'processing.dwell() multiprocessing with %s cores'%(cores) + self.console['ENDC'])
        ##else use less than half of total available cores
        else:
            isMultiprocessing = True
            cores = int(cores/2)
            dir_p = np.array_split(_dir, cores)
            print(self.console['green'] + 'processing.dwell() multiprocessing with %s cores'%(cores) + self.console['ENDC'])
            
        #------------------------------------------multiprocessing
        #if not multiprocessing
        if not isMultiprocessing:
            #----start
            output = run(dir_, cores)
            
            #----after finished 
            df_dwell, df_error = finished(output=output)
            
            #----merge
            df_dwell["participant"] = df_dwell[["participant"]].astype(np.int64)
            df = df_dwell.merge((df[['cesd_group','participant']].drop_duplicates(subset="participant", keep="first")), on='participant')
            
            #----finished
            return df, df_error
        #else multiprocessing
        else:
            #collect each pipe (this is used to build send and recieve portions of output)
            queue = multiprocessing.Queue()
            
            #----collect each thread
            process = [multiprocessing.Process(target=run,args=(dir_p[core], core, queue,)) for core in range(cores)]
            
            #start each thread
            for p in process:
                p.daemon = True
                p.start()
            
            #return queues
            #note: see https://stackoverflow.com/a/45829852
            returns = []
            for p in process:
                returns.append(queue.get())
                
            #wait for each process to finish
            for p in process:
                p.join()

            #---- finished multiprocessing
            df_dwell, df_error = finished(output=returns)
            
            #----merge
            df_dwell["participant"] = df_dwell[["participant"]].astype(np.int64)
            df = df_dwell.merge((df[['cesd_group','participant']].drop_duplicates(subset="participant",keep="first")), on='participant')
            return df, df_error
    
    def onset_diff(self, df0, merge=None, cores=1):
        """Calculate differences in onset presentation (stimulus, dotloc) using bokeh, seaborn, and pandas.

        Parameters
        ----------
        df0 : :class:`pandas.DataFrame`
            Pandas dataframe of raw data. This is used to merge variables that may be useful for analysis.
        merge : :class:`list` or `None`
            Variables to merge into returned df.
        cores : :class:`int`    
            Number of cores to use for multiprocessing.

        Returns
        -------
        df1 : :class:`pandas.DataFrame`
            Pandas dataframe.
        error : :class:`pandas.DataFrame`
            Dataframe of each participants and the amount trials included in their data.
        drop : :class:`list`
            List of participants that are 3 SD from median.
        """
        import multiprocessing
        #timestamp
        _t0 = datetime.datetime.now()
        _f = self.debug(message='t', source="timestamp")
        
        #----run
        def run(dir_=None, core=None, queue=None):
            print(self.console['green'] + 'processing.onset_diff.run(%s)'%(core) + self.console['ENDC'])
            onset = []
            #----for each subject
            for index, row in dir_.iterrows():
                _path_ = row['path']
                _subject = row['participant']
                
                #----read csv as dataframe
                df = pd.read_csv(_path_, float_precision='high', low_memory=False)
                print('subject: %s; core: %s'%(_subject, core))
                
                #----if 198 trials continue else skip
                if (df.drop_duplicates(subset="TrialNum", keep="first").shape[0] == 198):  
                    #----format column
                    df['RT'] = df['RT'].astype('float64')
                    
                    #----calculate number of samples in trial
                    df['trial_samples'] = df.groupby('TrialNum')['type'].transform(len)
                    
                    #condense to subject:trial-level
                    df = df.loc[df.drop_duplicates(subset="TrialNum", keep="first").index].reset_index(level=0, drop=True)
    
                    #----calculate scores
                    # stimulus onset
                    df['diff_stim'] = df.apply(lambda x: abs(x['Stim_onset.t'] - 1500), axis=1)
                    # dotloc onset
                    df['diff_dotloc'] = df.apply(lambda x: abs(x['DotLoc_onset.t'] - (1500 + 4500))
                    if (x['trialType'] == 'iaps') else abs(x['DotLoc_onset.t'] - abs(1500 + 3000)), axis=1)
                    
                    #----relevant data only                                    
                    #keep important columns
                    df = df[['participant', 'TrialNum', 'diff_dotloc', 'diff_stim', 'Key_Resp.rt','Key_Resp.acc','trialType']]
                    #group by trial
                    
                    #store to list
                    onset.append(df)
                    
                else:
                    print('%s; error: too few trials'%(_subject))
            
            #----add to multithreading queue
            if isMultiprocessing:
                #queue
                queue.put(onset)
                
            if not isMultiprocessing:
                return onset
        
        #--------finished
        def finished(output, isMultiprocessing, error=None):
            #----concat list of dataframes
            if isMultiprocessing:
                #flatten
                output_ =  [itm for l in output for itm in l]
                df = pd.concat(output_)
            else:
                df = pd.concat(output)
            #rename
            df = df.rename(columns={'Key_Resp.rt':'Key_Resp_rt','Key_Resp.acc':'Key_Resp_acc'})
            
            #--get median onset error
            df['m_diff_dotloc'] = df.groupby(["participant"])['diff_dotloc'].transform('median')
            df['m_diff_stim'] = df.groupby(["participant"])['diff_stim'].transform('median')
            df['m_rt'] = df.groupby(["participant"])['Key_Resp_rt'].transform('median')
            #--get accuracy
            df['accuracy'] = df.groupby(["participant"])['Key_Resp_acc'].transform('sum')    
            #--transform trial number to 0-1 for analysis
            df['TrialNum_'] = df.groupby(["participant"])['TrialNum'].transform(lambda x: x / 198)

            #----store participants with diff_dotloc or diff_stim > 500
            #drop dotloc diff time 3 SD > mean
            ##diff_dotloc
            error_std = df['diff_dotloc'].std() * 3
            drop_1 = list(df.loc[df['diff_dotloc'] > error_std].drop_duplicates(subset="participant", keep="first")['participant'])
            ##diff_stim
            error_std = df['diff_stim'].std() * 3
            drop_2 = list(df.loc[df['diff_stim'] > error_std].drop_duplicates(subset="participant", keep="first")['participant'])
            drop = list(np.unique(drop_1 + drop_2))
            
            #create new column where if onset diff greater than 500msec, then True, else False
            df['onset>500'] = np.where(df['participant'].isin(drop), True, False)
            
            #check if data came out correctly by looking at ampunt of trials and participants outputted
            error = df.groupby(['participant']).agg(['count'])
            
            #merge with df
            if merge is not None:
                df["participant"] = df[["participant"]].astype(np.int64)
                df1 = df.merge((df0[merge].drop_duplicates(subset="participant", keep="first")), on='participant')
                
            #check differences
            l_df1 = df1['participant'].unique().tolist()
            l_df = df['participant'].unique().tolist()
            missing = set(l_df1) ^ set(l_df)
            
            #----end
            print(self.console['blue']+'%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000))+self.console['ENDC'])
            return df1, error, drop
        #--------------------get list of all participants
        ##get directory
        _dir = glob.glob(os.path.join(self.config['path']['processed'] + '/data/eyetracking' + "/*.csv"))
        _sbj_session = [(Path(x).name.replace('abc', '').replace('.csv', '')).split("_", 1) for x in _dir]
        dir_ = [[z,*x] for z,x in zip(_dir,_sbj_session)]
        dir_ = pd.DataFrame(dir_, columns=['path','participant','session'])
        
        #------------------------------------------check if running using multiprocessing
        #----get cores
        ##if requested cores is 1, run without multiprocessing
        if ((cores == 0) or (cores == 1)):
            isMultiprocessing = False
            print(self.console['green'] + 'processing.onset_diff() not multiprocessing' + self.console['ENDC'])
        ##else if requested cores are less than/equal 7, and less than available cores plus 1
        elif ((cores <= 7) and (multiprocessing.cpu_count() >= cores + 1)):
            isMultiprocessing = True
            dir_p = np.array_split(dir_, cores)
            print(self.console['green'] + 'processing.onset_diff() multiprocessing with %s cores'%(cores) + self.console['ENDC'])
        ##else use less than half of total available cores
        else:
            isMultiprocessing = True
            cores = int(cores/2)
            dir_p = np.array_split(_dir, cores)
            print(self.console['green'] + 'processing.onset_diff() multiprocessing with %s cores'%(cores) + self.console['ENDC'])
            
        #------------------------------------------multiprocessing
        #if not multiprocessing
        if not isMultiprocessing:
            #----start
            output = run(dir_, cores)
            
            #----after finished 
            df_onset, df_error, drop = finished(isMultiprocessing=isMultiprocessing, output=output)
            
            return df_onset, df_error, drop
        #else multiprocessing
        else:
            #collect each pipe (this is used to build send and recieve portions of output)
            #pipes = [multiprocessing.Pipe(False) for pipe in range(cores)]
            queue = multiprocessing.Queue()
            
            #----collect each thread
            process = [multiprocessing.Process(target=run,args=(dir_p[core], core, queue,)) for core in range(cores)]
            
            #start each thread
            for p in process:
                p.daemon = True
                p.start()
            
            #return queues
            #note: see https://stackoverflow.com/a/45829852
            returns = []
            for p in process:
                #queue.get() will block #https://stackoverflow.com/a/45829852
                returns.append(queue.get())
                
            #wait for each process to finish
            for p in process:
                p.join()

            #---- finished multiprocessing
            df_onset, df_error, drop = finished(isMultiprocessing=isMultiprocessing, output=returns)
            
            return df_onset, df_error, drop
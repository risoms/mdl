#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Default settings for mdl.r33.Processing.  
| @date: Created on Sat May 1 15:12:38 2019
| @author: Semeon Risom
| @email: semeon.risom@gmail.com
| @url: https://semeon.io/d/R33-analysis
"""
# available functions
__all__ = ['Settings','config']

# required external library
__required__ = ['datetime','distutils','importlib']

# global
from pdb import set_trace as breakpoint
import os
import re

# local libraries
if __name__ == '__main__':
	from .. import settings

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

class Settings():
    """Default settings for mdl.r33.Processing"""

	# default configuration parameters
    config = config

    def __init__(self, isLibrary=False):
        """
		Initiate the mdl.r33.Settings module.

		Parameters
		----------
		is_library : :class:`bool` or `list`
			Check if required libraries are available. Default `False`.
		"""
        #check libraries
        if isLibrary:
            settings.library(__required__)

    @classmethod
    def definitions(cls, config):
        """
        Store definitions.

        Parameters
        ----------
        message : :class:`str`
            Log message.
        source : :class:`str`
            Origin of call. Either debug or timestamp.

        Returns
        -------
        config : :class:`dict`
            Returned dictionary

        Examples
        --------
        CESD Group
            in-text: m_['short']['cesd_group'] = 'CESD Group'
            title: m_['long']['cesd_group'] = 'CESD Group'
            definition: m_['def']['cesd_group'] "a binary measure of CESD score (between subjects; 'Low' (&lt16) and 'High' (≥16))"
        """
        #----prepare dictionary
        m_ = {
            'var':{},
            'short':{},
            'long':{},
            'def':{},
            'url':{},
            'cite':{},
            'img':{},
        }
        #----methods
        # task design
        name = 'task_design'
        m_['def'][name] = "Treatment stimuli include pairs of faces, each from a different actor and each expressing sad and \
        neutral emotions, from the Pictures of Facial Affect (POFA; [27]) collection and dysphoric and neutral images from the \
        International Affective Picture System (IAPS; [28]). Each POFA and IAPS scene will be equalized (12.0 cd/m2) to match \
        mean luminance distribution. Task-related screens will be matched to mean luminance as well. Each trial will begin with \
        the appearance of a central fixation cross (FC) for 1500 ms, followed by an image pair. POFA pairs will be presented \
        for 3000 ms and IAPS pairs will be presented for 4500 ms. IAPS images will be presented for a longer duration because \
        they are typically more complex than the POFA faces. Following offset of the images, a small single or double asterisk \
        probe will appear in the location of one of the images and remain on the screen until the participant indicates whether \
        they detected one or two asterisks, with a maximum duration of 10,000 msec. Latency and accuracy of each response will \
        be recorded."

        #----exclude
        _exc = len(config['metadata']['subjects']['exclude'])
        _pct = (round(len(config['metadata']['subjects']['exclude'])/len(config['metadata']['subjects']['eyetracking']), 4)*100)
        m_['def']['exclude'] = "Participants with 'Dotloc' or 'Stimulus' Onset Error median above 3SD (<i>n</i> = %s, %.1f%%) \
        were excluded from analysis \
        (see <a class='anchor' href='../../methods.html#outliers'>methods</a>)."%(_exc, _pct)

        #----stimuli
        # iaps
        name = 'iaps'
        title = 'International Affective Picture System (IAPS)'
        ref = 'Lang, P., Bradley, M., Cuthbert, B. (2008). International affective picture system (IAPS): Affective \
        ratings of pictures and instruction manual. Technical Report A-8. University of Florida, Gainesville, FL.'
        m_['var'][name] = name
        m_['short'][name] = 'IAPS'
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['img'][name] = 'img/iaps.png'
        # pofa
        name = 'pofa'
        title = 'Pictures of Facial Affect (POFA)'
        ref = 'Ekman, P., Friesen, W., (1976). Pictures of facial affect. Consulting Psychologist Press, Palo Alto.'
        m_['var'][name] = name
        m_['short'][name] = 'POFA'
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['img'][name] = 'img/pofa.png'

        #----variables
        # os
        m_['var']['os'] = 'os'
        m_['short']['os'] = 'Operating System'
        m_['long']['os'] = 'Operating System (Microsoft OS, Mac OS)'
        m_['def']['os'] = 'Microsoft OS, Mac OS'
        #stimulus
        m_['var']['trialType'] = 'trialType'
        m_['short']['trialType'] = 'Stimulus'
        m_['long']['trialType'] = 'Stimulus (IAPS, POFA)'
        m_['def']['trialType'] = '<b>%s</b>: %s<br><b>%s</b>: %s'\
        %(m_['short']['iaps'], m_['long']['iaps'], m_['short']['pofa'], m_['long']['pofa'])
        # aoi
        m_['var']['aoi'] = 'aoi'
        m_['short']['aoi'] = 'Area of Interest'
        m_['long']['aoi'] = 'Area of Interest (sad, neutral images)'
        m_['def']['aoi'] = 'sad, neutral (categorical).'
        # participant
        m_['var']['participant'] = 'participant'
        m_['short']['participant'] = 'Participant'
        m_['long']['participant'] = 'Participant'
        m_['def']['participant'] = 'Participant number (categorical).'
        # trial
        m_['var']['TrialNum'] = 'TrialNum'
        m_['short']['TrialNum'] = 'Trial'
        m_['long']['TrialNum'] = 'Trial'
        m_['def']['TrialNum'] = ': 0-197 (categorical).'
        # cesd group
        m_['var']['cesd_group'] = 'cesd_group'
        m_['short']['cesd_group'] = 'CESD Score'
        m_['long']['cesd_group'] = "CESD Score ('Low' (&lt16) and 'High' (≥16))"
        m_['def']['cesd_group'] = ": Binary measure of CESD score ('Low' (&lt16) and 'High' (≥16))"
        # diff_stim
        m_['var']['diff_stim'] = 'diff_stim'
        m_['short']['diff_stim'] = 'Stimulus Onset Error'
        m_['long']['diff_stim'] = 'Stimulus Onset Error'
        m_['def']['diff_stim'] = ": The difference in time (msec) between predicted and true 'Stimulus' onset."
        # diff_dotloc
        m_['var']['diff_dotloc'] = 'diff_dotloc'
        m_['short']['diff_dotloc'] = 'Dotloc Onset Error'
        m_['long']['diff_dotloc'] = 'Dotloc Onset Error'
        m_['def']['diff_dotloc'] = ": The difference in time (msec) between predicted and true 'Dotloc' onset."
        # dotprobe bias score
        m_['var']['dp_bias'] = 'dp_bias'
        m_['short']['dp_bias'] = 'Dotprobe Bias Score'
        m_['long']['dp_bias'] = 'Dotprobe Bias Score'
        m_['def']['dp_bias'] = ': Trial level bias score, using the weighted method. From the R itrak package.'
        # dotprobe bias score
        m_['var']['gaze_bias'] = 'gaze_bias'
        m_['short']['gaze_bias'] = 'Gaze Bias Score'
        m_['long']['gaze_bias'] = 'Gaze Bias Score'
        m_['def']['gaze_bias'] = ': Trial level bias score, using the weighted method. From the R itrak package.'
        # dwell_time
        m_['var']['dwell_time'] = 'dwell_time'
        m_['short']['dwell_time'] = 'Dwell Time'
        m_['long']['dwell_time'] = 'Dwell Time'
        m_['def']['dwell_time'] = ": The duration (msec) during a trial gaze has been within an area of interest."

        #----modelling
        #lmer
        name = 'lmer'
        title = 'Bates, Mächler, Bolker, & Walker, 2015'
        doi = 'https://doi.org/10.18637/jss.v067.i01'
        ref = 'Bates, D., Mächler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. 2015, 67(1), 48. \
        doi: %s'%(doi)
        m_['short'][name] = name
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['url'][name] = doi
        #glmer
        name = 'glmer'
        title = 'Bates, Mächler, Bolker, & Walker, 2015'
        doi = 'https://doi.org/10.18637/jss.v067.i01'
        ref = 'Bates, D., Mächler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. 2015, 67(1), 48. \
        doi: %s'%(doi)
        m_['short'][name] = name
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['url'][name] = doi
        #anova
        name = 'anova'
        title = 'Chambers, Hastie, 1992'
        ref = 'Chambers, J., Hastie, T. (1992). Statistical Models in S. Wadsworth & Brooks/Cole.'
        m_['short'][name] = name
        m_['long'][name] = title
        m_['cite'][name] = ref

    	#----assumptions
        # lmer
    	## residual normal distribution
        m_['long']['rnd'] = "Residuals are normally distributed"
        m_['def']['rnd'] = ": Residuals are drawn from a normally distributed population. Can be checked with a QQ plot. \
        Statistical tests, such as Anderson-Darling and Kolmogorov–Smirnov are also possible."
    	## independent observations
        m_['long']['rio'] = "Residuals are independent"
        m_['def']['rio'] = ": Residuals have been drawn independently of each other. This can be checked by plotting residuals \
        against covariates - especially time-varying or spatial covariates."

        # anova
        ## normal distribution
        m_['long']['nd'] = "Samples are normally distributed"
        m_['def']['nd'] = ": Samples are drawn from a normally distributed population."
    	## Homogeneity of variance
        m_['long']['hv'] = "Homogeneity of variance"
        m_['def']['hv'] = ": Amount of variance for a IV is constant across the sample."
    	## independent observations
        m_['long']['io'] = "Independent observations"
        m_['def']['io'] = ": Samples have been drawn independently of each other."

        # Estimated Marginal Means
        url = 'https://cran.r-project.org/web/packages/emmeans/vignettes/comparisons.html'
        m_['def']['emm'] = "The 'Estimated Marginal Means' table provides a list pairwise comparisons for each level and factor \
        in our model (<a class='anchor' href='%s'>emmeans package, Version 1.3.2</a>)."%(url)
    	# residuals vs fitted
        m_['def']['rvf'] = "The Residuals vs Fitted plot is used to identify residual distribution. \
        If residuals are following a visible trend on the graph, then the homogeneity assumption was violated."
    	# qq
        m_['def']['qq'] = "The Normal Q-Q plot compares the standardized residuals against the theoretical quantiles from \
        a standard normal distribution. If the model residuals are normally distributed, then the points \
        on this graph will be plotted in a generally straight line."

        #----calibration, validation
        m_['def']['calibration'] = "Symbols: square = mouse click, circle = calibration point, cross = gaze coordinates.<br>\
        To use the interactive plot, drag the mouse along the calibration point chart. Each pair of dots repersents gaze coordinates \
        recorded during the presentation of one of the calibration points."
        m_['def']['validation'] = "Symbols: circle = calibration point, cross = gaze coordinates.<br>\
        To use the interactive plot, drag the mouse along the calibration point chart. Each pair of dots repersents gaze coordinates \
        recorded during the presentation of one of the calibration points."

        #----data processing: classify, filter (processing.py)
        # hmm
        name = 'hmm'
        title = 'Pekkanen & Lappi, 2017'
        doi = 'doi: 10.1038/s41598-017-17983-x'
        ref = 'Pekkanen, J., & Lappi, O. (2017). A new and general approach to signal denoising and eye movement classification \
        based on segmented linear regression. Scientific Reports, 7(1).'
        m_['short'][name] = name
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['url'][name] = doi
        # how preprocessing was planned
        name = 'preprocessing'
        title = 'Larsson, Nystrom, & Stridh, 2013'
        doi = 'doi: 10.1109/tbme.2013.2258918'
        ref = 'Larsson, L., Nystrom, M., & Stridh, M. (2013). Detection of Saccades and Postsaccadic Oscillations in the Presence \
        of Smooth Pursuit. IEEE Transactions On Biomedical Engineering, 60(9), 2484-2493.'
        m_['short'][name] = name
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['url'][name] = doi
        # example
        m_['def']['filter'] = "As conventional in eye tracking research, eye movement data were filtered according to \
        predetermined cut-offs (e.g. Juhasz and Rayner, 2006; Kliegl, Grabner, Rolfs, and Engbert, 2004; Rayner, Reichle, Stroud, \
        Williams, and Pollatsek, 2006; Rayner et al., 2011; Schattka, Radach, and Huber, 2010). Fixations smaller than 80 ms \
        and adjacent to a larger neighbouring fixation (within 0.3° of a visual angle) were merged. Fixations shorter than \
        80 ms that were not adjacent to a larger neighbouring fixation and fixations longer than 1200 ms were excluded \
        (Juhasz et al., 2006). Trials with gross track loss were also excluded, leading to an elimination of 4.47% of the \
        data overall (3.68% for NHI and 4.80% for PWA). Trials with blinks were not excluded since a comparison of trials \
        with blinks to trials without blinks showed no significant differences in gaze durations in a previous experiment (Huck, 2016)."

        #----software
        name = 'R'
        title = 'R Core Team, 2013'
        url = 'http://www.R-project.org/'
        ref = 'Core Team, R., (2013). R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna,\
        Austria. (Version 3.2.1) [Software]. Available from URL %s.'%(url)
        m_['short'][name] = name
        m_['long'][name] = title
        m_['cite'][name] = ref
        m_['url'][name] = url

        #----remove whitespaces
        for key, value in m_['def'].items():
            m_['def'][key] = re.sub(r'\s+', ' ', value).strip()
        for key, value in m_['cite'].items():
            m_['cite'][key] = re.sub(r'\s+', ' ', value).strip()

        #create metadata variable
        config['metadata']['short'] = m_['short']
        config['metadata']['long'] = m_['long']
        config['metadata']['def'] = m_['def']
        config['metadata']['cite'] = m_['cite']
        config['metadata']['url'] = m_['url']
        config['metadata']['var'] = m_['var']
        config['metadata']['img'] = m_['img']

        return config


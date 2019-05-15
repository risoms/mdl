#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Hub for creating plots.  
| @date: Created on Sat May 1 15:12:38 2019   
| @author: Semeon Risom   
| @email: semeon.risom@gmail.com   
| @url: https://semeon.io/d/mdl
"""

# available functions
__all__ = ['bokeh_trial','bokeh_calibration','onset_diff_plot','density_plot','corr_matrix','boxplot','cooks_plot',
'residual_plot','qq_plot','logit_plot','html']

# core
from pdb import set_trace as breakpoint
from distutils import dir_util
import importlib
import datetime
import shutil
import sys
import os

# data
import pandas as pd
import numpy as np

# seaborn
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

# local libraries
from . import settings

# constants
console = settings.console
debug = settings.debug

def __font__():
	"""Add Helvetica to matplotlib."""
	from matplotlib import matplotlib_fname, rcParams
	import matplotlib.font_manager as font_manager

	directory = matplotlib_fname().replace("/matplotlibrc/", "")
	destination = f'{directory}/fonts/ttf'
	file = settings.path['home'] + "/dist/resources/Helvetica.ttf"

	#add to matplotlib font folder
	shutil.copy(file, destination)

	#add to computer font folder
	##if running osx
	if sys.platform == "darwin":
		shutil.copy(file, '/Library/Fonts/')
	##if running win32
	if sys.platform == "win32":
		shutil.copy(file, 'c:\\windows\\fonts')

	#rebuild fonts
	prop = font_manager.FontProperties(fname=file)
	prop.set_weight = 'light'
	rcParams['font.family'] = prop.get_name()
	rcParams['font.weight'] = 'light'
	font_manager._rebuild()

def bokeh_trial(config, df, stim_bounds, roi_bounds, flt):
    """Create single subject trial bokeh plots.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Pandas dataframe of participant sample data.
    stim_bounds : :class:`dict`
        Stimulus bounds on screen.
    roi_bounds : :class:`dict`
        ROI bounds on screen.
    flt : :class:`str`
        Filter type.
    """
	#----bokeh
    from bokeh.core.properties import value
    from bokeh.plotting import reset_output, figure
    from bokeh.models import HoverTool, Range1d, BoxAnnotation, ColumnDataSource, CDSView, BooleanFilter
    from bokeh.layouts import gridplot
    from bokeh.embed import components

    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    
    #metadata
    emotion = [df['left_mood'][0],df['right_mood'][0]]
    #filter xy coordinates
    flt_x = '%s_x'%(flt)
    flt_y = '%s_y'%(flt)
    
    #get display size
    xy = [int(i) for i in (df['monitorSize.px'].values[0]).split('x')]
    monitorSize = xy
    
    #subject data
    t = df['timestamp'].values
    
    #get fixations
    df['fixation_onset'] = df.loc[df.groupby('fix_num')['%s_fix_all'%(flt)].head(1).index, '%s_fix_all'%(flt)]
    df['fixation_onset'] = df.apply(lambda x: True if (x['fixation_onset'] == True) else False, axis=1)
    
    #source for syncing data
    s = ColumnDataSource(df)

    ##tools = "box_select,save,pan,box_zoom,reset"
    tools="box_select,save,reset"

    #figure 1
    #sizing_mode: ``"fixed"``, ``"stretch_both"``, ``"scale_width"``, ``"scale_height"``, ``"scale_both"``
    p1 = figure(
            output_backend="webgl",
            tools=tools,
            plot_width=1200,
            plot_height=400,
            x_range=Range1d(-100, (t[-1]+100), bounds="auto"),
            y_range=Range1d(0,(monitorSize[0]+100), bounds="auto"),
            x_axis_label = 'time (msec)', y_axis_label = 'x/y (px)',
            sizing_mode="stretch_both",
     )

    #hover
    hover = HoverTool()
    hover.tooltips = [
        ("name", "$name"),
        ("sample", "$index"),
        ("data (x,y)", "($x{(0)},$y{(0)})")
    ]
    p1.tools.append(hover)
    p1.hover.line_policy = "nearest"

    #graph
    ###-----------------------------------------------------------------x=time, y=(x or y)
    #original x
    p1.scatter(x='timestamp', y='x', color='#2965C0', alpha=0, line_width=2,
            line_dash='dashed', name='raw_x', source=s)
    p1.line(x='timestamp', y='x', color='#2965C0', alpha=0.5, line_width=2,
            legend=value('raw_x'), line_dash='dashed', name='raw_x', source=s)
    #filtered x
    p1.scatter(x='timestamp', y=flt_x, color='#265EB3', alpha=0, line_width=2,
            name=flt_x, source=s)
    p1.line(x='timestamp', y=flt_x, color='#265EB3', alpha=1, line_width=2,
            legend=value(flt_x), name=flt_x, source=s)
    #peak removed
    #p1.line(x=t, y=sg_x, color='#101f23', alpha=1, line_width=2,legend='x_peaksg', name='x_peaksg')

    #original y
    p1.scatter(x='timestamp', y='y', color='#C01F1F', alpha=0, line_width=2,
            line_dash='dashed', name='raw_y', source=s)
    p1.line(x='timestamp', y='y', color='#C01F1F', alpha=0.5, line_width=2,
            legend=value('raw_y'), line_dash='dashed', name='raw_y', source=s)
    #filtered y
    p1.scatter(x='timestamp', y=flt_y, color='#A61B1B', alpha=0, line_width=2,
            name=flt_y, source=s)
    p1.line(x='timestamp', y=flt_y, color='#A61B1B', alpha=1, line_width=2,
            legend=value(flt_y), name=flt_y, source=s)

    #task-events (stimulus onset, dotloc onset)
    ##stimulus onset
    time = df.loc[df['marker']=='Stimulus Onset']['timestamp'].iloc[0]
    box = BoxAnnotation(left=time, right=time + 10, fill_alpha=1, fill_color='#434e54', level='glyph')
    p1.add_layout(box)
    ##dotloc onset
    time = df.loc[df['marker']=='Dotloc Onset']['timestamp'].iloc[0]
    box = BoxAnnotation(left=time, right=time + 10, fill_alpha=1, fill_color='#434e54', level='glyph')
    p1.add_layout(box)

    #fixations
    for index, row in df[~df['sg_fix_all'].isin([False])].groupby('fix_num'):
        start = row.iloc[0]['timestamp']
        end = row.iloc[-1]['timestamp']
        box = BoxAnnotation(left=start, right=end,fill_alpha=0.2, fill_color='#9e9e9e', level='glyph')
        p1.add_layout(box)
    del index, row

    #legend
    p1.toolbar.logo = None
    p1.legend.orientation = "horizontal"
    p1.legend.location = "top_left"
    p1.legend.click_policy = "hide"

    ###-----------------------------------------------------------------window display
    #sizing_mode: ``"fixed"``, ``"stretch_both"``, ``"scale_width"``, ``"scale_height"``, ``"scale_both"``
    #display what participant sees
    tools = "box_select,save,pan,box_zoom,reset"
    p2 = figure(
            output_backend="webgl",
            tools=tools,
            plot_width=1200,
            plot_height=600,
            x_axis_label = 'x (px)', y_axis_label = 'y (px)',
            x_range=Range1d(0, monitorSize[0], bounds="auto"),
            y_range=Range1d(0, monitorSize[1], bounds="auto"),
            sizing_mode="stretch_both"
    )
    #hover
    hover = HoverTool()
    hover.tooltips = [
        ("name", "$name"),
        ("sample", "$index"),
        ("data (x,y)", "($x{(0)},$y{(0)})")
    ]
    p2.tools.append(hover)
    p2.hover.line_policy = "nearest"
    ###---------line plots
    #------gaze xy
    p2.cross(x=flt_x, y=flt_y, size=10, color="firebrick", alpha=1, fill_alpha=0.6,
              fill_color="firebrick", source=s, name='gaze', legend='gaze')

    #------fixation onset within and outside roi
    #get booleanfilter
    l_fix_all = [True if x !=False else False for x in s.data['fixation_onset']]
    fix_all = BooleanFilter(l_fix_all)
    view = CDSView(source=s, filters=[fix_all])
    ##draw square ##2222b2
    p2.square(x=flt_x, y=flt_y, size=10, color="#2222b2", alpha=1, fill_alpha=0.6,
              fill_color="white", source=s, view=view, name='fixation', legend=value("fixation"))
    
    #------fixation within and outside roi
    #get booleanfilter
    l_fix_false = [True if x !=False else False for x in s.data['sg_fix_all']]
    fix_false = BooleanFilter(l_fix_false)
    view = CDSView(source=s, filters=[fix_false])
    ##draw square ##2222b2
    p2.square(x=flt_x, y=flt_y, size=10, color="black", alpha=1, fill_alpha=0.6,
              fill_color="white", source=s, view=view, name='false-fixation', legend=value("false-fixation"))

    #------only fixation within roi
    #get booleanfilter
    l_fix_roi = [True if (y==True and z==True) else False for y,z in zip(s.data['fixation_onset'], s.data['dwell'])]
    fix_roi = BooleanFilter(l_fix_roi)
    view = CDSView(source=s, filters=[fix_roi])
    ##draw triangle ##198D40
    p2.triangle(x=flt_x, y=flt_y, size=10, color="#198D40", alpha=1, fill_alpha=0.6,
              fill_color="white", source=s, view=view, name='roi', legend=value("roi"))
    
    #------dwell-time gaze within roi
    l_dwell_roi = [True if x !=False else False for x in s.data['dwell']]
    dwell_roi = BooleanFilter(l_dwell_roi)
    view = CDSView(source=s, filters=[dwell_roi])
    ##draw circle ##ff9800
    p2.circle(x=flt_x, y=flt_y, size=10, color="#ff9800", alpha=1, fill_alpha=0.6,
              fill_color="white", source=s, view=view, name='dwell', legend=value("dwell"))

    #------stim bounds
    stimBounds = stim_bounds

    #------roi bounds
    roiBounds = roi_bounds

    #emotion
    left, right = emotion
    if left == 'Sad':
        left_color = '#ff0000'
        right_color = '#9e9e9e'
    else:
        right_color = '#ff0000'
        left_color = '#9e9e9e'

    #roi
    #left
    p2.add_layout(BoxAnnotation(left=roiBounds[0]['bx1'], right=roiBounds[0]['bx2'],
                                top=roiBounds[0]['by1'], bottom=roiBounds[0]['by2'],
                        fill_alpha=0.05, fill_color='blue', level='glyph'))
    #right
    p2.add_layout(BoxAnnotation(left=roiBounds[1]['bx1'], right=roiBounds[1]['bx2'],
                                top=roiBounds[1]['by1'], bottom=roiBounds[1]['by2'],
                        fill_alpha=0.05, fill_color='blue', level='glyph'))


    #--------stim bounds
    #left
    p2.add_layout(BoxAnnotation(left=stimBounds[0]['bx1'], right=stimBounds[0]['bx2'],
                                top=stimBounds[0]['by1'], bottom=stimBounds[0]['by2'],
                        fill_alpha=0.3, fill_color=left_color, level='glyph'))
    #right
    p2.add_layout(BoxAnnotation(left=stimBounds[1]['bx1'], right=stimBounds[1]['bx2'],
                                top=stimBounds[1]['by1'], bottom=stimBounds[1]['by2'],
                        fill_alpha=0.3, fill_color=right_color, level='glyph'))
    #hover
    hover = HoverTool()
    hover.tooltips = [
        ("time", "@timestamp"),
        ("sample", "$index"),
        ("data (x,y)", "($%s_x{(0)},$%s_y{(0)})"%(flt,flt))
    ]
    #p2.tools.append(hover)
    #p2.hover.line_policy = "nearest"

    #legend
    p2.toolbar.logo = None
    p2.legend.orientation = "horizontal"
    p2.legend.location = "top_left"
    p2.legend.click_policy = "hide"

    #reverse axis
    p2.x_range = Range1d(0, monitorSize[0])
    p2.y_range = Range1d(monitorSize[1], 0)

    ###-----------------------------------------------------------------slider
    #sizing_mode: ``"fixed"``, ``"stretch_both"``, ``"scale_width"``, ``"scale_height"``, ``"scale_both"``
    start = df.iloc[0]['timestamp']
    end = df.iloc[-1]['timestamp']
    # callback = CustomJS(args=dict(source=s), code="""
    #     data = source.data;
    #     t = cb_obj;
    #     f = cb_obj.value;
    #     x = data['x'];
    #     y = data['y'];
    #     source.change.emit();
    #     console.log('test');
    # """)
    # p3 = Slider(
    #         title="time",
    #         start=start,
    #         end=end,
    #         value=1, step=1,
    #         callback=callback,
    #         bar_color='red',
    #         width=1200,
    #         show_value=True,
    #         sizing_mode="stretch_both"
    # )

    ###-----------------------------------------------------------------combining plots
    #sizing_mode: ``"fixed"``, ``"stretch_both"``, ``"scale_width"``, ``"scale_height"``, ``"scale_both"``
    # grid = gridplot(children=[[p1], [p2], [p3]],
    grid = gridplot(children=[[p1], [p2]],
                    merge_tools=True,
                    toolbar_location='right',
                    sizing_mode="fixed")

    #get html
    script, div = components(grid)

    ##convert seperate plots and div to single string
    plots = (''.join(map(str, [div, '\n', script])))

    #clear cache
    reset_output()

    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return plots

def bokeh_calibration(config, df, cxy, event, monitorSize=[1920,1080]):
    """Create calibration matrix, using pandas and bokeh.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    cxy : :class:`pandas.DataFrame`
        Pandas dataframe of calibration points.
    event : :obj:`string`
        calibration, or validation.
    monitorSize : :obj:`list`
        Monitor size, in pixels.
    """
    from bokeh.plotting import reset_output, figure
    from bokeh.models import Range1d, ColumnDataSource
    from bokeh.embed import components

    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    
    #subject data
    event_t = df['event_trial'].values
    
    #source for syncing data
    s = ColumnDataSource(df)

    ##tools = "box_select,save,pan,box_zoom,reset"
    #figure 1
    #sizing_mode: ``"fixed"``, ``"stretch_both"``, ``"scale_width"``, ``"scale_height"``, ``"scale_both"``
    ##tools = "box_select,save,pan,box_zoom,reset"
    tools = "box_select,reset"
    p1 = figure(
            output_backend="webgl",
            tools=tools,
            plot_width=1200,
            plot_height=150,
            x_range=Range1d(0 - 0.1, (event_t[-1] + 0.1), bounds="auto"),
            y_range=Range1d(0,(monitorSize[0]+100), bounds="auto"),
            x_axis_label = 'calibration point', y_axis_label = 'x/y (px)',
            sizing_mode="scale_width",
     )

    #graph
    ###-----------------------------------------------------------------x=time, y=(x or y)
    #original x
    p1.scatter(x='event_trial', y='cx', color='#2965C0', alpha=0.5, line_width=2,
            line_dash='dashed', name='cx', source=s)
    # p1.line(x='event_trial', y='cx', color='#2965C0', alpha=0.5, line_width=2,
            # line_dash='dashed', name='cx', source=s,legend=value('cx'))

    #original y
    p1.scatter(x='event_trial', y='cy', color='#C01F1F', alpha=0.5, line_width=2,
            line_dash='dashed', name='cy', source=s)
    # p1.line(x='event_trial', y='cy', color='#C01F1F', alpha=0.5, line_width=2,
    #         line_dash='dashed', name='cy', source=s,legend=value('cy'))

    ###-----------------------------------------------------------------window display
    #sizing_mode: ``"fixed"``, ``"stretch_both"``, ``"scale_width"``, ``"scale_height"``, ``"scale_both"``
    ##tools = "box_select,save,pan,box_zoom,reset"
    tools="save,reset"
    p2 = figure(
        output_backend="webgl",
        tools=tools,
        plot_width=1200,
        plot_height=600,
        x_axis_label = 'x (px)', y_axis_label = 'y (px)',
        x_range=Range1d(0, monitorSize[0], bounds="auto"),
        y_range=Range1d(0, monitorSize[1], bounds="auto"),
        sizing_mode="scale_width"
    )
    
    ###---------line plots
    #----gaze xy
    # cross = p2.cross(x='gx', y='gy', size=10, color="firebrick", alpha=1, fill_alpha=0.6,
    p2.cross(x='gx', y='gy', size=10, color="firebrick", alpha=1, fill_alpha=0.6,
              fill_color="firebrick", source=s, name='gaze')
    #           fill_color="firebrick", source=s, name='gaze', legend=value("gaze"))
    
    #----circle xy
    p2.circle(x=cxy['cx'], y=cxy['cy'], size=12, color="#198D40", alpha=1, fill_alpha=0.6,
              fill_color="white", name='circle')
              #fill_color="white", source=s, name='circle', legend=value("circle"))
              
    # draw mouse click for calibration
    if event=='calibration':
        #----mouse xy
        p2.square(x='mx', y='my', size=10, color="#2222b2", alpha=1, fill_alpha=0.6,
                  fill_color="white", source=s, name='mouse')
                  #fill_color="white", source=s, name='mouse', legend=value("mouse"))
        
    #----legend
    p1.toolbar.logo = None
    p2.toolbar.logo = None

    #----reverse axis
    p2.x_range = Range1d(0, monitorSize[0])
    p2.y_range = Range1d(monitorSize[1], 0)
    
    #----grid
    #p1
    p1.grid.grid_line_alpha = 0.5
    p1.grid.grid_line_color = "white"
    
    #----font
    # p2
    ## title
    p2.axis.axis_label_text_font_style = "normal"
    ## labels
    p2.axis.axis_label_text_font_size= "11.5pt"
    p2.axis.axis_label_text_font = "Helvetica"
    p2.axis.axis_label_text_color = "#1c1d1e"
    p2.axis.major_label_text_font_size= "11.5pt"
    p2.axis.major_label_text_font = "Helvetica"
    p2.axis.major_label_text_color = "#1c1d1e"
    # p1
    ## title
    p1.axis.axis_label_text_font_style = "normal"
    ## labels
    p1.axis.axis_label_text_font_size = "9.5pt"
    p1.axis.axis_label_text_font = "Helvetica"
    p1.axis.axis_label_text_color = "#1c1d1e"
    p1.axis.major_label_text_font_size = "9.5pt"
    p1.axis.major_label_text_font = "Helvetica"
    p1.axis.major_label_text_color = "#1c1d1e"
    p1.axis.major_tick_line_color = None
    p1.axis.minor_tick_line_color = None 
    
    #----padding
    p2.min_border_top = 16
    p1.min_border_bottom = 0
    
    #----axis line
    # p2
    p2.axis.axis_line_width = 0
    p2.axis.axis_line_color = None
    p2.outline_line_color = "#1c1d1e"
    # p1
    p1.background_fill_color = "#dfe1e4"
    p1.axis.axis_line_width = 0
    p1.axis.axis_line_color = None
    p1.outline_line_color = "#1c1d1e"
    
    #----get html
    #get componants
    plot = {'top': p2, 'bottom': p1}
    script, div = components(plot)
    #combine
    div = ''.join(list(div.values()))
    plot = div + script
        
    #----clear cache
    reset_output()

    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return plot

def onset_diff_plot(config, df, meta, drop, y, clip=None):
    """Plot onset differences using pandas and seaborn.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    meta : :class:`pandas.DataFrame`
        Metadata for each chart.
    drop : :class:`pandas.DataFrame`
        Participants to be dropped.
    y : :obj:`str`
        Variable of interest.
    clip : :obj:`int`
        Clip value for single subject plot.

    Returns
    -------
    odp
        Bokeh or seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #setting clip
    clip = 200 if clip == None else clip
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    
    importlib.reload(plt); importlib.reload(sns)
    console('running onset_diff_plot(%s)'%(y), 'blue')
    html_plots = []
    
    #-----------------participant trend line
    individual = meta['individual']
    sns.set(style=config['style']['seaborn'], font_scale=1.25, font="Helvetica")
    #sns.despine(offset=10, trim=True)
    fig, ax = plt.subplots(figsize=(10,5))
    #plot
    df["%s (msec)"%(y)] = df.groupby('participant')[y].rolling(window=5).mean().reset_index(0,drop=True)
    ##if diff_dotloc and diff_stim < 500 msec
    sns.color_palette("RdBu",6)
    ax_ = sns.lineplot(x="TrialNum_", y="%s (msec)"%(y), ax=ax, legend=False, lw=1, estimator=None, palette="ch:2.5,.25",
                       hue="participant", units="participant", data=df.loc[df['onset_greater'] == False])
    ##if diff_dotloc and diff_stim > 500 msec
    ax_ = sns.lineplot(x="TrialNum_", y="%s (msec)"%(y), ax=ax, legend=False, lw=1, estimator=None, alpha=0.2,
                      hue="participant", units="participant", data=df.loc[df['onset_greater'] == True])
    #settings
    ax_.set(xlim=(0, 1), ylim=(0, clip), ylabel='| %s (msec) |'%(y), xlabel='trial')
      
    #append
    html_plots.append({"title":individual['title'],"file":"%s.png"%(individual['file']),"footnote":individual['footnote'],"anchor":"itl"})
    #tight layout
    fig.tight_layout()
    #save
    fig.savefig(individual['path'], dpi=300)
    #clear figure from memory
    plt.close(fig)
    
    #-----------------diff plot
    group = meta['group']
    #for each plot
    importlib.reload(plt); importlib.reload(sns)
    fig, ax = plt.subplots(figsize=(10,10), ncols=2, nrows=2, sharey=False)
    ax1, ax2, ax3, ax4 = ax.flatten()
    sns.set(style=config['style']['seaborn'], font_scale=1.1, font="Helvetica")
    #sns.despine(offset=10, trim=True)
    #binned
    ##iaps
    type_='iaps'
    df_1 = df.loc[df['trialType'] == type_].reset_index(level=0, drop=True)
    sns.regplot(x="TrialNum_",y=y,color="#5874a6",data=df_1,ax=ax1,
                fit_reg=True,x_bins=group['binned']['bins'],scatter_kws={"s": 40},line_kws={'color': 'red'})
    ax1.set(ylim=(0, 200), xlabel='', ylabel='| %s (msec) |'%(y), title='trial_type=%s'%(type_))
    ##pofa
    type_='pofa'
    df_1 = df.loc[df['trialType'] == type_].reset_index(level=0, drop=True)
    sns.regplot(x="TrialNum_",y=y,color="#5d9f6c",data=df_1,ax=ax2,
                fit_reg=True,x_bins=group['binned']['bins'],scatter_kws={"s": 40},line_kws={'color': 'red'})
    ax2.set(ylim=(0, 200), xlabel='', ylabel='', title='trial_type=%s'%(type_))
    #unbinned
    ##iaps
    type_='iaps'
    df_1 = df.loc[df['trialType'] == type_].reset_index(level=0, drop=True)
    sns.regplot(x="TrialNum_",y=y,color="#5874a6",data=df_1,ax=ax3,
                fit_reg=True,x_bins=group['unbinned']['bins'],scatter_kws={"s": 5},line_kws={'color': 'red'})
    ax3.set(ylim=(0, 1000), xlabel='trial', ylabel='| %s (msec) |'%(y), title='trial_type=%s'%(type_))
    ##pofa
    type_='pofa'
    df_1 = df.loc[df['trialType'] == type_].reset_index(level=0, drop=True)
    sns.regplot(x="TrialNum_",y=y,color="#5d9f6c",data=df_1,ax=ax4,
                fit_reg=True,x_bins=group['unbinned']['bins'],scatter_kws={"s": 5},line_kws={'color': 'red'})
    ax4.set(ylim=(0, 1000), xlabel='trial', ylabel='', title='trial_type=%s'%(type_))
    #append
    html_plots.append({"title":group['title'],"file":"%s.png"%(group['file']),"footnote":group['footnote'],"anchor":"gtl"})
    #tight layout
    fig.tight_layout()
    #save
    fig.savefig(group['path'], dpi=300)
    #clear figure from memory
    plt.close(fig)
    
    #--------finished
    #timestamp
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return html_plots

def density_plot(config, df, title):
    """
	Create density plot (draws kernel density estimate), using seaborn and pandas.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    title : :obj:`str`
        Chart title.

    Returns
    -------
    cm
        Bokeh or seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    
    #seaborn
    #https://seaborn.pydata.org/generated/seaborn.distplot.html
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    importlib.reload(plt); importlib.reload(sns)
    console('running density_plot()', 'blue')
    
    #remove cesd_group, trialType_ column
    df = df.drop(['trialType_','cesd_group'], axis=1)
    
    #create metadata to be used for html file
    html_plots = []
    
    #for each column
    for item in (df.columns.tolist()):
        #----plot type
        sns.set(style=config['style']['seaborn'], font_scale=1.1, font="Helvetica")
        sns.despine(offset=10, trim=True)

        #----plot
        fig, ax = plt.subplots(figsize=(10,10))
        density = sns.distplot(df[item], ax=ax, norm_hist=True,
                               #bins - number of bins for histogram
                               hist=True, bins=20,
                               #bw (bandwidth) - width of the kernels
                               kde=True, kde_kws={'clip':None,'bw':'scott','kernel':'gau'}).set(xlim=(None, None))
        ax.set(ylabel='Density')
        
        #----design
        #tight layout
        fig.tight_layout()
        
        #----save
        #check if path exists
        file = "density_%s.png"%(item)
        path = config['path']['output'] + "/analysis/html/img/density/"
        if not os.path.exists(path):
            os.makedirs(path)
        #save
        fig.savefig(path + file, dpi=300)
        
        #append 
        html_plots.append({"title":'%s for %s.'%(title, item),"file":'density/'+file,"footnote":""})
        #clear figure from memory
        plt.close(fig)
         
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return density, html_plots

def corr_matrix(config, df, path, title, method, footnote=None):
    """
	Create correlation matrix using bokeh and pandas.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    path : :obj:`str`
        The directory path to save the bokeh or plot.
    method : :obj:`str`
        Spearman or Pearsons correlation coefficient.
    title : :obj:`str`
        Chart title.
    footnote : :obj:`str`
        Chart footnote.

    Returns
    -------
    cm
        Bokeh plot.
    """
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    console('running bokeh corr_matrix()', 'blue')

    # math
    import bisect
    from math import pi
    from numpy import arange
    from itertools import chain
    from collections import OrderedDict
    
    # bokeh
    from bokeh.models import ColorBar, LinearColorMapper, TapTool, HoverTool, Range1d, ColumnDataSource
    from bokeh.models.callbacks import CustomJS
    from bokeh.plotting import reset_output, figure
    from bokeh.embed import components

    #create color palette
    matplotlib.use('Agg')
    import matplotlib.colors
    from matplotlib import cm as mpl_cmap
    
    #p-values
    if method == "pearson":
        from scipy.stats import pearsonr as cf
    elif method == "spearman":
        from scipy.stats import spearmanr as cf
    
    #calculate p-values correlation coefficent
    def get_pvalue(df):
        df = df.dropna()._get_numeric_data()
        dfcols = pd.DataFrame(columns=df.columns)
        pvalues = dfcols.transpose().join(dfcols, how='outer')
        for row in df.columns:
            for column in df.columns:
                pvalues[row][column] = round(cf(df[row], df[column])[1], 4)
        return pvalues

    #Gets bounds for quads with n features
    def get_bounds(n):
        bottom = list(chain.from_iterable(
            [[ii]*nlabels for ii in range(nlabels)]))
        top = list(chain.from_iterable(
            [[ii+1]*nlabels for ii in range(nlabels)]))
        left = list(chain.from_iterable(
            [list(range(nlabels)) for ii in range(nlabels)]))
        right = list(chain.from_iterable(
            [list(range(1, nlabels+1)) for ii in range(nlabels)]))
        corr_items = list(chain.from_iterable(
            [[ii+1]*nlabels for ii in range(nlabels)]))
        return top, bottom, left, right, corr_items
    
    #Aligns color values from palette with the correlation coefficient and p-values
    def get_colors_corr(corr_array, p_array, colors):
        c_corr = arange(-1, 1, 1/(len(colors)/2))
        corr_color = []
        p_color = []
        corr_list = []
        p_list = []
        factor_list = []
        itr = 0
        for corr, pvalue in zip(corr_array,p_array):
            ind = bisect.bisect_left(c_corr, corr)
            #colors
            ##corr_color
            if (itr)%(nlabels+1)==0:
                corr_color.append('#022f62')
            else:
                corr_color.append(colors[ind-1])
            ##pcolor
            if pvalue<=0.05:
                p_color.append("#F44336")
            else:
                p_color.append(colors[ind-1])
            #append corr and pvalues
            corr_list.append(corr)
            p_list.append(pvalue)
            factor_list.append(['[%s, %s]'%(l_labels[itr][0],l_labels[itr][1])])
            itr = itr + 1
        return corr_color, corr_list, p_color, p_list, factor_list
    
    #create seaborn plots for each possible correlation combinations
    def get_corr_plot(df, x, y):
        importlib.reload(plt); importlib.reload(sns)

        #----parameters
        #figure
        fig, ax = plt.subplots(1, 1, figsize=(10,10))
        #bounds
        plt.subplots_adjust(top=0.95, bottom=0.085, left=0.125, right=0.975, hspace=0.2, wspace=0.2)
        
        #----title
        title = "x=%s, y=%s"%(x,y)
        
        #----set style
        #pal = sns.color_palette("Set1", n_colors=2, desat=.5)
        sns.set(style=config['style']['seaborn'], font="Helvetica", font_scale=1.1)
        sns.despine(offset=10, trim=True)
        
        #----plot
        #if grouping #g = sns.lmplot(x, y, hue=groupby, data=df, palette=pal).set_title(title)
        sns.regplot(x, y, data=df, scatter=True, fit_reg=True, ci=95).set_title(title)
        
        #----add rho, p-value to plot
        #get values
        corr_r = cf(df[x],df[y])
        corr_t = "r = %.2f, p < %.2f"%(corr_r[0],corr_r[1])
        #place text 90% of max-x and 90% of max-y
        fig.text(0.85, 0.05, corr_t, size=16, horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes)

        #----save
        #check if path exists
        file = "%s.png"%(title)
        path = config['path']['output'] + "/analysis/html/img/corr/"
        if not os.path.exists(path):
            os.makedirs(path)
        #save
        fig.savefig(path + file, dpi=300)

    #reset
    reset_output()
    
    #get color map
    RdYlBu = mpl_cmap.get_cmap('RdBu', 32)
    colors_np = np.vstack(RdYlBu(np.linspace(0, 1, 32)))
    cmap = matplotlib.colors.ListedColormap(colors_np, name='RedBlue')
    colors = [matplotlib.colors.rgb2hex(cmap(x/32)[:3]) for x in range(32)]

    # calculate correlation coefficients
    #coeff
    corr_coeff = df.corr(method=method)
    #p-value
    p_value = get_pvalue(df)

    # get list and number of variables
    labels = df.columns
    nlabels = len(corr_coeff)

    #create list of labels
    ##x
    l_labels_x = labels.tolist() * nlabels
    ##y
    l_labels_y = labels.tolist() * nlabels
    ###split into chunks
    l_labels_y_split = np.hsplit(np.array(np.array_split(l_labels_y, nlabels)), nlabels)
    l_labels_y = np.concatenate(l_labels_y_split).ravel().tolist()
    ##combine
    l_labels = list(zip(l_labels_x, l_labels_y))

    #create coeff label coordinates
    num = np.arange(0, nlabels, 0.5).tolist()
    num = [x for x in num if x not in np.arange(0, nlabels).tolist()]
    ##x
    num_x = [(x - 0.025) for x in num]
    num_x = [x for x in num_x if x not in np.arange(0, nlabels).tolist()] * nlabels
    ##y
    num_y = [(x + .125) for x in num]
    num_y = [y for y in num_y if y not in np.arange(0, nlabels).tolist()] * nlabels

    ###split into chunks
    num_y_split = np.hsplit(np.array(np.array_split(num_y, nlabels)), nlabels)
    num_y = np.concatenate(num_y_split).ravel().tolist()
    ##combine
    #num_labels = list(zip(num_x, num_y))

    #plot
    tools="box_select,save,reset"
    cm = figure(tools=tools, plot_width=1200, plot_height=1200, x_range=(0, nlabels), y_range=(0, nlabels), 
                output_backend="webgl")

    #hover
    hover = HoverTool()
    hover.tooltips = [
         ("factor", "@factor"),
         ("rho", "@coeff_num"),
         ("p", "@p_num"),
    ]
    #cm.tools.append(hover)
    cm.hover.line_policy = "nearest"

    #legend
    #cm.toolbar.logo = None

    #grid
    cm.xgrid.grid_line_color = None
    cm.ygrid.grid_line_color = None
    cm.xaxis.major_label_orientation = pi/4
    cm.yaxis.major_label_orientation = pi/4

    #turn off scientific notation
    cm.left[0].formatter.use_scientific = False

    # prepare squares for plot
    top, bottom, left, right, corr_items = get_bounds(nlabels)
    color_list,corr,p_color,pvalues,factor = get_colors_corr(corr_coeff.values.flatten(),p_value.values.flatten(),colors)

    #prepare corr_coeff label for plot
    coeff_color = ["#444444"] * (nlabels * nlabels)
    coeff_color = ['#f9f9f9' if cr >= np.float64(0.74) else cof for cof, cr in zip(coeff_color, corr)]
    coeff_num = ["%.2f"%(x) for x in corr]

    #prepare pvalue for plot
    p_color = ["#444444"] * (nlabels * nlabels)
    p_color = ['#F44336' if p <= np.float64(0.05) else cof for pcol, cof, p in zip(p_color, coeff_color, pvalues)]
    p_num = ["(%.2f)"%(y) for y in pvalues]

    #data source
    source = ColumnDataSource(data=dict(left=left, right=right, top=top, bottom=bottom,
                                        x=num_x, y=num_y, coeff_num=coeff_num, coeff_color=coeff_color,
                                        p_num=p_num, factor=factor, square_color=color_list, p_color=p_color))
    #create squares
    cm.quad(top='top', bottom='bottom', left='left', right='right', 
            line_color='white', color='square_color', source=source)

    #create text
    #correlation coefficient
    cm.text(x='x', y='y', source=source, text_color="coeff_color", text='coeff_num', 
            text_font_style='normal', text_font_size = '1.5em', text_align='center',
            y_offset=-5, x_offset=1, text_line_height=1)
    #p-value
    cm.text(x='x', y='y', source=source, text_color="p_color", text='p_num', 
            text_font_style='normal', text_font_size = '1.0em', text_align='center',
            y_offset=20, x_offset=1, text_line_height=1)

    #callback
    link = CustomJS(args = dict(source = source), code="""
        console.log("second")
        obj = cb_obj
        s = source
        data = source.data
        attr = source.attributes
        d = attr.data

        //selected item
        id = source.selected['1d'].indices
        item = d.factor[id][0].replace(/[[\]]/g,'').match(/(".*?")|(\S+)/g)
        console.log('id: ' + id + ', item: ' + item)
        
        //url
        path = window.location.href
        current = path.split("/").slice(0,-1).join("/")
        url = current + '/reg.html?x='+ item[0] + 'y=' + item[1]
        window.open(url)
        //window.open(url, 'newwindow', config='height=720, width=1280')
    """)
    cm.add_tools(TapTool(callback=link))  

    #reverse y-axis
    cm.y_range = Range1d(nlabels, 0)
    #p.y_range = Range1d(monitorSize[1], 0)

    # Set ticks with labels
    ticks = [tick+0.5 for tick in list(range(nlabels))]
    tick_dict = OrderedDict([[tick, labels[ii]] for ii, tick in enumerate(ticks)])

    # Create the correct number of ticks for each axis
    cm.xaxis.ticker = ticks
    cm.yaxis.ticker = ticks

    # Override the labels
    cm.xaxis.major_label_overrides = tick_dict
    cm.yaxis.major_label_overrides = tick_dict

    #color bar
    mapper = LinearColorMapper(
        palette=colors,
        low=-1, high=1
    )
    color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
    cm.add_layout(color_bar, 'right')

    #create link for each comparison
    all_columns = [[x,y] for x in list(labels) for y in list(labels)]
    for idx, clm in enumerate(all_columns):
        get_corr_plot(df=df, x=clm[0], y=clm[1])

    #get html
    script, div = components(cm)
    
    ##convert seperate plots and div to single string
    plots = (''.join(map(str, [div, '\n', script])))

    #create html
    html(config, path=path, plots=plots, source='bokeh', title=title, footnote=footnote)

    #reset
    reset_output()

    #--------finished
    #timestamp
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return cm

def single_subject(self, df, path):
    """Create single subject scatterplot using seaborn and pandas.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    path : :obj:`str`
        The directory path to save the bokeh or seaborn plot.

    Returns
    -------
    cm
        Bokeh or seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    console('running single_subject()', 'blue')
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    importlib.reload(plt); importlib.reload(sns)
    
    #styling plot
    sns.set(style="darkgrid", font_scale=1, font="Helvetica")
    sns.set_context("paper")

    #events
    events = self.config['events']
    
    #get first pofa and iaps
    first = df.drop_duplicates('trialType', keep='first')['TrialNum'].tolist()
    
    #get display size
    xy = [int(i) for i in (df['monitorSize.px'].values[0]).split('x')]
    
    #drop x - outside coordinates
    df = df.loc[~(df['sg_x']<0)] #drop all gaze_x < 0
    df = df.loc[~(df['sg_x']>xy[0])] #drop all gaze_x > width
    
    #drop timestamp - outside coordinates
    df = df.loc[~(df['timestamp']>8000)]
    
    #drop all non fixations
    df = df.loc[~(df['sg_fix_all']==False)]
    
    #loop to draw event markers
    def xline(x, **kwargs):
        data = kwargs.pop("data")
        trialType = data['trialType'].values[0]
        TrialNum = data['TrialNum'].values[0]
        #check if first iaps or first pofa
        if TrialNum in first:
            #fixation onset
            time = events['fixation']
            plt.axvline(x=0, c='red', linewidth=2)
            ##annotation
            plt.text(s="Fixation Onset", x=(0 + 100), y=(xy[0] - 25), fontsize=12)
            #fixation offset
            time = events['fixation']
            plt.axvline(x=time, c='red', linewidth=2)
            ##annotation
            plt.text(s="Stimulus Offset", x=(time + 100), y=(xy[0] - 25), fontsize=12)
            #stimulus offset
            time = events['fixation'] + events['stimulus'][trialType]
            #line
            plt.axvline(x=time, c='red', linewidth=2)
            #annotation
            plt.text(s="Dotloc Offset", x=(time + 100), y=(xy[0] - 25), fontsize=12)
        
    #plot    
    pal = sns.color_palette("RdBu", n_colors=192)    
    sp = sns.FacetGrid(col="trialType", data=df, height=5, palette=pal, hue="TrialNum")
    sp.map(plt.scatter, "timestamp", "sg_x", alpha=0.3, s=10)
    sp.map_dataframe(xline, x="timestamp")
            
    #post
    ax = sp.axes.flatten()
    ax[0].set_ylabel("Gaze Coordinates (x)", fontdict={'fontsize':12})
    ax[0].set_title("trialType = IAPS", fontdict={'fontsize':12})
    ax[0].tick_params(labelsize=12)
    ax[1].set_title("trialType = POFA", fontdict={'fontsize':12})
    ax[1].tick_params(labelsize=12)
    
    #size
    sp.fig.set_size_inches(20,10)
    
    #save
    sp.savefig(path, dpi=300)
    
    #clear figure from memory
    plt.close()
    
    #--------finished
    #timestamp
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return plt 

def boxplot(config,df,path=None,x=None,y=None,title=None,plots=None,cat='analysis'):
    """
    Creates boxplot using seaborn and pandas.
    
    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    path : :obj:`str`
        Path to save data.
    drift : :obj:`str`
        X-axis.
    drift : :obj:`str`
        Y-axis.
    title : :obj:`str`
        Plot title.
    plots : :obj:`dict`
        Dictionary of plots metadata.
    cat : :obj:`str`
        Type of plot.
    """ 
    #----initiate fonts
    __font__()
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    console('running boxplot(%s)'%(y), 'blue')

	# start
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    importlib.reload(plt); importlib.reload(sns)
    sns.set(style=config['style']['seaborn'], font_scale=1.5, font="Helvetica")
    sns.despine(offset=10, trim=True)
    short_ = config['metadata']['short']
    #if looking at dwell time
    if cat=='bias':
        #plot
        fig, (ax1, ax2) = plt.subplots(figsize=(10,10),ncols=2,sharey=True)
        
        #design
        ##for each unique value in x-axis variable, assign color
        cat_x = df[x].unique().tolist()
        color=['b','r','g','y','o']
        pal = dict(zip(cat_x, color))
        
        #create plot
        for ax, trialType in zip([ax1,ax2],['iaps','pofa']):
            df_ = df.loc[df['trialType'].isin([trialType])]
            sns.boxplot(x=x, y='.fitted', data=df_, ax=ax, palette=pal)
            sns.swarmplot(x=x, y='.fitted', data=df_, color=".25", ax=ax)
            ax.set_title(trialType)
            ax.set_xlabel(short_[x])
            if trialType == 'pofa':
                ax.set_ylabel('')
    
    #if looking at dwell time
    if cat=='dwell':
        #plot
        fig, (ax1, ax2) = plt.subplots(figsize=(10,10),ncols=2,sharey=True)
        
        #design
        ##for each unique value in x-axis variable, assign color
        cat_x = df[x].unique().tolist()
        color=['b','r','g','y','o']
        pal = dict(zip(cat_x, color))
        
        #create plot
        for ax, trialType in zip([ax1,ax2],['iaps','pofa']):
            df_ = df.loc[df['trialType'].isin([trialType])]
            sns.boxplot(x=x, y='.fitted', data=df_, ax=ax, palette=pal)
            sns.swarmplot(x=x, y='.fitted', data=df_, color=".25", ax=ax)
            ax.set_title(trialType)
            ax.set_xlabel(short_['aoi'])
            if trialType == 'pofa':
                ax.set_ylabel('')
    
    #if looking at variables like gaze_bias, dp_bias
    elif cat=='analysis':
        #plot
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(figsize=(19.2, 10.8),ncols=4,sharey=False)
        
        #design
        ##for each unique value in x-axis variable, assign color
        cat_x = df[x].unique().tolist()
        color=['b','r','g','y','o']
        pal = dict(zip(cat_x, color))
        
        #create plot
        for ax, itm in zip([ax1,ax2,ax3,ax4],y):
            #dp_bias
            sns.boxplot(x=x, y=itm, data=df, ax=ax, palette=pal)
            sns.swarmplot(x=x, y=itm, data=df, color=".25", ax=ax)
            ax.set(xlabel=x)
            
    #if looking at variables like race, gender, os        
    elif cat=='demographics':
        #layout
        sns.set(style=config['style']['seaborn'], palette="deep", font_scale=1.1, font="Helvetica")
        sns.despine(offset=10, trim=True)
        fig, (ax1,ax2,ax3,ax4) = plt.subplots(figsize=(20, 10),ncols=4,sharey=True)
        palette = sns.color_palette(["#e74c3c", "#3f51b5", "#2ecc71","#9b59b6","#ffb400"])
        #counter
        counter = 0
        for ax, x_, in zip([ax1,ax2,ax3,ax4],x):
            ##exclude smaller race categories for display purposees
            if x_=='gender':
                df_ = df.loc[~df['gender'].isin(["other"])].drop_duplicates(subset="participant",keep="first")
            ##exclude smaller race categories for display purposes
            elif x_=='race':
                df_ = df.loc[~df['race'].isin(["American Indian or Alaska Native","Two or more races",
                "Black or African American","None of the above"])].drop_duplicates(subset="participant",keep="first")
            else:
                df_ = df.drop_duplicates(subset="participant",keep="first")
            #plot
            sns.boxplot(x=x_, y=y, palette=palette, ax=ax, data = df_)
            #remove label
            if counter!=0:
                ax.set_ylabel('')
            #counter
            counter = counter + 1
    
        #layer
        sns.despine(offset=10, trim=True)
    
    #tight layout
    fig.tight_layout()
    
    ##save
    fig.savefig(path, dpi=300)
    
    #clear from memory
    plt.close(fig) 
    
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')

def cooks_plot(config, y, model, path, df):
    """Create cooks distance plot plot using seaborn, pandas, and statsmodel.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    path : :obj:`str`
        The directory path save the seaborn plot.
    y : :obj:`str`
        The predictor variable.
    model : :obj:`dict`
        statsmodel model.

    Returns
    -------
    res
        seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    
    console('running cooks_plot(%s)'%(y), 'blue')
    #-------plot
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    importlib.reload(plt); importlib.reload(sns)

    #plot design
    sns.set(style=config['style']['seaborn'], font_scale=1.1, font="Helvetica")
    sns.despine(offset=10, trim=True)

    #plot
    fig, ax = plt.subplots(figsize=(10,10))
    
    # influence
    influence = model.get_influence()
    
    # cook's distance, from statsmodels internals
    ## c is the distance and p is p-value
    (c, p) = influence.cooks_distance
    
    #plot
    plt.stem(np.arange(len(c)), c, markerfmt=",")
    plt.xlabel('Observation Number')
    plt.ylabel('Cooks Distance')
    
    # annotations
    particpants = list(df['participant'])
    leverage_lines = np.flip(np.argsort(c), 0)[:3]
    for i in leverage_lines:
        plt.annotate(particpants[i], xy=(i, c[i]))

    #tight layout
    fig.tight_layout()
    
    #save
    fig.savefig(path, dpi=300)
    
    #clear figure from memory
    plt.close(fig)
    
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return plt
   
def residual_plot(config, y, residuals, path):
    """Create probability plot using seaborn, pandas, and rpy2.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    y : :obj:`str`
        Predictor variable.
    residuals : :class:`pandas.DataFrame`
        Pandas dataframe of residuals vs fitted, qq data, and raw data.
    path : :obj:`str`
        The directory path save the seaborn plot.

    Returns
    -------
    lmp
        seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    
    console('running residual_plot(%s)'%(y), 'blue')
    #-------plot
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    importlib.reload(plt); importlib.reload(sns)
    
    #-------plot design
    sns.set(style=config['style']['seaborn'], font_scale=1.1, font="Helvetica")
    sns.despine(offset=10, trim=True)
    #-------plot
    fig, ax = plt.subplots(figsize=(10,10))
    #residual vs fitted plot
    cmap=sns.color_palette(["#bd282f","#226db2"])
    sns.scatterplot(x=".fitted", y=".resid", data=residuals, ax=ax, hue="trialType", palette=cmap, legend=None, s=60, edgecolor=None)
    #loess smoothing curve
    sns.regplot(x=".fitted", y=".resid", data=residuals, ax=ax, lowess=True, scatter=False, color="blue")
    #horizontal line
    plt.axhline(0, zorder=1, color='black', linewidth=2.25)
    #annotations
    ##max
    max_ = residuals[residuals['.resid']==residuals['.resid'].max()]
    max_x = max_['.fitted'].iloc[0]
    max_y = max_['.resid'].iloc[0]
    max_subject = max_['participant'].iloc[0]
    plt.text(max_x, max_y, max_subject, color='black', weight='semibold')
    ##min
    min_ = residuals[residuals['.resid']==residuals['.resid'].min()]
    min_x = min_['.fitted'].iloc[0]
    min_y = min_['.resid'].iloc[0]
    min_subject = min_['participant'].iloc[0]
    plt.text(min_x, min_y, min_subject, color='black', weight='semibold')

    #-------plot design
    #label
    plt.xlabel('.fitted')
    plt.ylabel('.resid')
    #tight layout
    fig.tight_layout()
    
    #-------save
    fig.savefig(path, dpi=300)
    
    #-------clear figure from memory
    plt.close(fig)
    
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return plt

def qq_plot(config, y, residuals, path):
    """Create probability plot using seaborn, pandas, and rpy2.

    Parameters
    ----------
    config : :obj:`dict`
        Configuration data.
    y : :obj:`str`
        Predictor variable.
    residuals : :class:`pandas.DataFrame`
        Pandas dataframe of residuals vs fitted, qq data, and raw data.
    path : :obj:`str`
        The directory path save the seaborn plot.

    Returns
    -------
    lmp
        seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    console('running qq_plot(%s)'%(y), 'blue')
    #-------plot
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    importlib.reload(plt); importlib.reload(sns)

    #plot design
    sns.set(style=config['style']['seaborn'], font_scale=1.1, font="Helvetica")
    sns.despine(offset=10, trim=True)
    #plot
    fig, ax = plt.subplots(figsize=(10,10))
    #qq residuals
    cmap=sns.color_palette(["#bd282f","#226db2"])
    sns.scatterplot(x="theoretical", y=".resid", data=residuals, ax=ax, hue="trialType", palette=cmap, legend=None, s=60, edgecolor=None)
    sns.regplot(x="theoretical", y=".resid", data=residuals, ax=ax, scatter=None, color="black", ci=None)
    #label
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Sample Quantiles')
    #annotations
    ##max
    max_ = residuals[residuals['.resid']==residuals['.resid'].max()]
    max_x = max_['theoretical'].iloc[0]
    max_y = max_['.resid'].iloc[0]
    max_subject = max_['participant'].iloc[0]
    plt.text(max_x, max_y, max_subject, color='black', weight='semibold')
    ##min
    min_ = residuals[residuals['.resid']==residuals['.resid'].min()]
    min_x = min_['theoretical'].iloc[0]
    min_y = min_['.resid'].iloc[0]
    min_subject = min_['participant'].iloc[0]
    plt.text(min_x, min_y, min_subject, color='black', weight='semibold')
    
    #tight layout
    fig.tight_layout()
    
    #save
    fig.savefig(path, dpi=300)
    
    #clear figure from memory
    plt.close(fig)
    
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return plt

def logit_plot(config,df,path,param):
    """Create logistic regression plot using seaborn and pandas

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    path : :obj:`str`
        The directory path save the seaborn plot.
    param : :obj:`dict`
        x, y, groupby parameters.

    Returns
    -------
    lmp
        seaborn plot.
    """
    #----initiate fonts
    __font__()
    
    #----for timestamp
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    console('processing.logit_plot()', 'blue')
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    importlib.reload(plt); importlib.reload(sns)
    
    #plot design
    p=param
    sns.set(style=config['style']['seaborn'], font_scale=1.1, font="Helvetica")
    sns.despine(offset=10, trim=True)
    console('running logit_plot(), (y=%s, x=%s)'%(p['y'],p['x']), 'blue')

    #plot
    fig, (ax1,ax2) = plt.subplots(figsize=(19.2, 10.8), ncols=2, sharey=True)
    #iaps
    type_ = 'iaps'
    df_ = df.loc[(df['trialType_']==type_)]
    lmp = sns.regplot(x=p['x'], y=p['y'], data=df_, logistic=True, y_jitter=.02, ax=ax1, color="#5874a6")
    ax1.set(xlabel='trial type', title='trialType=%s'%(type_))
    #pofa
    type_ = 'pofa'
    df_ = df.loc[(df['trialType_']==type_)]
    lmp = sns.regplot(x=p['x'], y=p['y'], data=df_, logistic=True, y_jitter=.02, ax=ax2, color="#5d9f6c")
    ax2.set(xlabel='trial type', title='trialType=%s'%(type_))

    #tight layout
    fig.tight_layout()
    
    #save
    fig.savefig(path, dpi=300)
    
    #clear figure from memory
    plt.close(fig)
    
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return lmp

def html(config, df=None, raw_data=None, name=None, path=None, plots=None, source=None, title=None, intro=None, footnote=None, script="", **kwargs):
    """
    Create HTML output.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Pandas dataframe of analysis results data.
    raw_data : :class:`pandas.DataFrame`
        Pandas dataframe of raw data.
    name : :obj:`str`
        (py::`if source is logit`) The name of csv file created.
    path : :obj:`str`
        The directory path of the html file.
    plots : :obj:`dict`
        If generating seaborn images, the list of plots used.
    source : :obj:`str`
        The type of data being recieved.
    trial : :obj:`str`
        (If Bokeh) Trial Number.
    session : :obj:`str`
        (If Bokeh) Session Number.
    bokeh_type : :obj:`str`
        (If Bokeh) Control directory location. If trial, create trial plots.
    title : :obj:`str`
        The title of the table or figure.
    intro : :obj:`str`
        The introduction of the group of figures or tables.
    footnote : :obj:`str`
        The footnote of the table or figure.
    metadata : :obj:`dict`
        Additional data to be included.
    **kwargs : :obj:`str`, :obj:`int`, or :obj:`None`, optional
        Additional properties, relevent for specific content types. Here's a list of available properties:
            
        .. list-table::
           :class: kwargs
           :widths: 25 50
           :header-rows: 1
           
           * - Property
             - Description
           * - **short**, **long** : :obj:`str`
             - Short (aoi) and long form (Area of Interest) label of html page. This is primarily used for constructing metadata tags in html.
           * - **display** : :obj:`str`
             - (For bokeh) The type of calibration/validation display.
           * - **trial** : :obj:`str`
             - (For bokeh) The trial number for the eyetracking task.
           * - **session** : :obj:`int`
             - (For bokeh) The session number for the eyetracking task.
           * - **day** : :obj:`str`
             - (For bokeh) The day the eyetracking task was run.

    Returns
    -------
    html : :obj:`str`
        String of html code.
    """
    #----initiate fonts
    __font__()
    
    #timestamp
    date = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    _t0 = datetime.datetime.now()
    _f = debug(message='t', source="timestamp")
    console('running plot.html()', 'blue')
    
    #---copy csv, imhr, js files to each model
    if ((source == "logit") or (source == "onset") or (source == "anova")):
        #copy files
        for folder in ['css','imhr','js']:
            source_ = config['path']['output'] + "/analysis/html/" + folder + "/"
            dest_ = os.path.dirname(path) + "/" + folder + "/"
            dir_util.copy_tree(src=source_, dst=dest_)
    
    #----if creating html file from bokeh
    if ((source=='bokeh') or (source=='methods')):
        #get short and long names
        short = kwargs['short'] if 'short' in kwargs else source
        long = kwargs['long'] if 'long' in kwargs else source
        
        #if trial plot
        if (source=='bokeh'):
            display =  kwargs['display'] if 'display' in kwargs else None
            trial =  kwargs['trial'] if 'trial' in kwargs else None
            session =  kwargs['session'] if 'session' in kwargs else None
            day =  kwargs['day'] if 'day' in kwargs else None
            if ((display=='trial') or (display=='calibration') or (display=='validation')):
                parent='../'
            else:
                parent=''
        else:
            parent=''
            
        #build header
        link = []; css = []; js = []
        link.append('<title>IMHR [webgazer] %s</title>'%(long))
        link.append('<meta name="title" content="mdl[webgazer]: %s">'%(long))
        link.append('<meta name="description" content="Results from our feasibility study for in-browser eyetracking.">')
        link.append('<meta name="author" content="Semeon Risom">')
        link.append('<meta name="email" content="semeon.risom@gmail.com">')
        link.append('<meta name="robots" content="index,follow">')
        link.append('<meta name="AdsBot-Google" content="noindex">')
        link.append('<!--size-->')
        link.append('<meta name="viewport" content="width=device-width, initial-scale=1.0" charset="utf-8"/>')
        link.append('<!--no cache-->')
        link.append('<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>')
        link.append('<meta http-equiv="Pragma" content="no-cache"/>')
        link.append('<meta http-equiv="Expires" content="0"/>')
        link.append('<!--icons-->')
        link.append('<link rel="shortcut icon" href="'+parent+'imhr/favicon/favicon.ico">')
        link.append('<link rel="icon" sizes="16x16 32x32 64x64" href="'+parent+'imhr/favicon/favicon.ico">')
        link.append('<link rel="icon" type="image/png" sizes="196x196" href="'+parent+'imhr/favicon/favicon-192.png">')
        link.append('<link rel="icon" type="image/png" sizes="160x160" href="'+parent+'imhr/favicon/favicon-160.png">')
        link.append('<link rel="icon" type="image/png" sizes="96x96" href="'+parent+'imhr/favicon/favicon-96.png">')
        link.append('<link rel="icon" type="image/png" sizes="64x64" href="'+parent+'imhr/favicon/favicon-64.png">')
        link.append('<link rel="icon" type="image/png" sizes="32x32" href="'+parent+'imhr/favicon/favicon-32.png">')
        link.append('<link rel="icon" type="image/png" sizes="16x16" href="'+parent+'imhr/favicon/favicon-16.png">')
        link.append('<link rel="apple-touch-icon" href="'+parent+'imhr/favicon/favicon-57.png">')
        link.append('<link rel="apple-touch-icon" sizes="114x114" href="'+parent+'imhr/favicon/favicon-114.png">')
        link.append('<link rel="apple-touch-icon" sizes="72x72" href="'+parent+'imhr/favicon/favicon-72.png">')
        link.append('<link rel="apple-touch-icon" sizes="144x144" href="'+parent+'imhr/favicon/favicon-144.png">')
        link.append('<link rel="apple-touch-icon" sizes="60x60" href="'+parent+'imhr/favicon/favicon-60.png">')
        link.append('<link rel="apple-touch-icon" sizes="120x120" href="'+parent+'imhr/favicon/favicon-120.png">')
        link.append('<link rel="apple-touch-icon" sizes="76x76" href="'+parent+'imhr/favicon/favicon-76.png">')
        link.append('<link rel="apple-touch-icon" sizes="152x152" href="'+parent+'imhr/favicon/favicon-152.png">')
        link.append('<link rel="apple-touch-icon" sizes="180x180" href="'+parent+'imhr/favicon/favicon-180.png">')
        link.append('<meta name="msapplication-TileColor" content="#FFFFFF">')
        link.append('<meta name="msapplication-TileImage" content="'+parent+'imhr/favicon/favicon-144.png">')
        link.append('<meta name="msapplication-config" content="'+parent+'docs/favicon/browserconfig.xml">')
        css.append('<link rel="stylesheet" type="text/css" href="'+parent+'css/user.css">')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/jquery/jquery-3.2.1.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/user.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/lodash.min.js"></script>')
        css.append('<!--bootstrap-->')
        css.append('<link rel="stylesheet" type="text/css" href="'+parent+'css/bootstrap/bootstrap.css">')
        css.append('<!--bokeh-->')
        css.append('<link rel="stylesheet" type="text/css" href="'+parent+'css/bokeh/bokeh-1.0.4.min.css">')
        css.append('<link rel="stylesheet" type="text/css" href="'+parent+'css/bokeh/bokeh-widgets-1.0.4.min.css">')
        css.append('<link rel="stylesheet" type="text/css" href="'+parent+'css/bokeh/bokeh-tables-1.0.4.min.css">')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/bokeh/bokeh-1.0.4.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/bokeh/bokeh-widgets-1.0.4.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/bokeh/bokeh-tables-1.0.4.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/bokeh/bokeh-gl-1.0.4.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/bokeh/bokeh-api-1.0.4.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/popper.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="'+parent+'js/bootstrap/bootstrap.js"></script>')
        
        # finish header
        head = ('\n\t'.join(map(str, link))) + ('\n\t'.join(map(str, css))) + ('\n\t'.join(map(str, js)))
        
        #body, footer
        if source=='bokeh':
            #build body
            body = ['<div class="container" style="">',
                        '<div class="container bokeh" style="">',
                            '<div class="figure %s" trial-id="%s" session-id="%s" day-id="%s" type-id="%s">\
                            '%(display, trial, session, day, display),
                                '<div class="title"><b>Figure 1.</b> <a>%s</a></div>'%(title),
                                '<div class="date"> Last Updated: ' + '%s'%(date) + '</div>',
                                plots,
                                '<div class="footnote">%s</div>'%(footnote),
                            '</div>',
                        '</div>',
                    '</div>']
            # finish body
            body = ('\n\t'.join(map(str, body)))
            
            #build footer
            if ((display=='trial') or (display=='calibration') or (display=='validation')):
                foot = ['<script>',
                            '$(document).ready(function() {getinput();});',
                        '</script>']
                # finish footer
                foot = ('\n\t'.join(map(str, foot)))
            else:
                foot = ''
                
        elif source=='methods':
            #build body
            body = ['<div class="container" style="">',
                        '<div class="dashboard-main">',
                            '<div class="table-container">',
                                '<div class="title"><a><b>%s</b></a></div>'%(title) ,
                                plots,
                            '</div>',
                        '</div>',
                    '</div>']
            # finish body
            body = ('\n\t'.join(map(str, body)))
            #build footer
            foot = ''
        
        #build html
        html = ['<html short="%s" long="%s">'%(short, long),
                    '<head>',
                        head,
                    '</head>',
                    '<body id="body" class="%s" style="margin: 0px; background-color: #434e54 !important;">'%(display),
                        body,
                    '</body>',
                    '<footer>',
                        foot,
                    '</footer>',
                '</html>']
        # finish html
        html = ('\n'.join(map(str, html)))
        
    #all other html
    else:
        #get short and long names
        short = kwargs['short'] if 'short' in kwargs else source
        long = kwargs['long'] if 'long' in kwargs else source
        var = kwargs['var'] if 'var' in kwargs else source
        
        #build header
        link = []; css = []; js = []
        link.append('<title>IMHR [webgazer] %s</title>'%(long))
        link.append('<meta name="title" content="mdl[webgazer]: %s">'%(long))
        link.append('<meta name="description" content="Results from our feasibility study for in-browser eyetracking.">')
        link.append('<meta name="author" content="Semeon Risom">')
        link.append('<meta name="email" content="semeon.risom@gmail.com">')
        link.append('<meta name="robots" content="index,follow">')
        link.append('<meta name="AdsBot-Google" content="noindex">')
        link.append('<!--size-->')
        link.append('<meta name="viewport" content="width=device-width, initial-scale=1.0" charset="utf-8"/>')
        link.append('<!--no cache-->')
        link.append('<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>')
        link.append('<meta http-equiv="Pragma" content="no-cache"/>')
        link.append('<meta http-equiv="Expires" content="0"/>')
        link.append('<meta name="msapplication-TileColor" content="#FFFFFF">')
        link.append('<meta name="msapplication-TileImage" content="imhr/favicon/favicon-144.png">')
        link.append('<meta name="msapplication-config" content="docs/favicon/browserconfig.xml">')
        link.append('<!--icons-->')
        link.append('<link rel="shortcut icon" href="imhr/favicon/favicon.ico">')
        link.append('<link rel="icon" sizes="16x16 32x32 64x64" href="imhr/favicon/favicon.ico">')
        link.append('<link rel="icon" type="image/png" sizes="196x196" href="imhr/favicon/favicon-192.png">')
        link.append('<link rel="icon" type="image/png" sizes="160x160" href="imhr/favicon/favicon-160.png">')
        link.append('<link rel="icon" type="image/png" sizes="96x96" href="imhr/favicon/favicon-96.png">')
        link.append('<link rel="icon" type="image/png" sizes="64x64" href="imhr/favicon/favicon-64.png">')
        link.append('<link rel="icon" type="image/png" sizes="32x32" href="imhr/favicon/favicon-32.png">')
        link.append('<link rel="icon" type="image/png" sizes="16x16" href="imhr/favicon/favicon-16.png">')
        link.append('<link rel="apple-touch-icon" href="imhr/favicon/favicon-57.png">')
        link.append('<link rel="apple-touch-icon" sizes="114x114" href="imhr/favicon/favicon-114.png">')
        link.append('<link rel="apple-touch-icon" sizes="72x72" href="imhr/favicon/favicon-72.png">')
        link.append('<link rel="apple-touch-icon" sizes="144x144" href="imhr/favicon/favicon-144.png">')
        link.append('<link rel="apple-touch-icon" sizes="60x60" href="imhr/favicon/favicon-60.png">')
        link.append('<link rel="apple-touch-icon" sizes="120x120" href="imhr/favicon/favicon-120.png">')
        link.append('<link rel="apple-touch-icon" sizes="76x76" href="imhr/favicon/favicon-76.png">')
        link.append('<link rel="apple-touch-icon" sizes="152x152" href="imhr/favicon/favicon-152.png">')
        link.append('<link rel="apple-touch-icon" sizes="180x180" href="imhr/favicon/favicon-180.png">')
        js.append('<!--all-->')
        js.append('<script type="text/javascript" language="javascript" src="js/jquery/jquery-3.2.1.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/lodash.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/bootstrap/bootstrap.bundle.js"></script>')
        link.append('<!--dataTables-->')
        css.append('<link rel="stylesheet" type="text/css" href="css/bootstrap/bootstrap.min.css">')
        css.append('<link rel="stylesheet" type="text/css" href="css/datatables/dataTables.bootstrap.min.css">')
        css.append('<link rel="stylesheet" type="text/css" href="css/datatables/responsive.bootstrap.min.css">')
        css.append('<link rel="stylesheet" type="text/css" href="css/datatables/buttons.bootstrap.min.css">')
        js.append('<!--user-->')
        link.append('<link rel="stylesheet" type="text/css" href="css/user.css">')
        js.append('<!--dataTables-->')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/jquery.dataTables.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.rowsGroup.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.rowGroup.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.bootstrap.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.buttons.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/buttons.bootstrap.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/dataTables.responsive.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/responsive.bootstrap.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/buttons.html5.min.js"></script>')
        js.append('<script type="text/javascript" language="javascript" src="js/datatables/jszip.min.js"></script>')
        js.append('<!--user-->')
        js.append('<script type="text/javascript" language="javascript" src="js/user.js"></script>')
        js.append('<script>source="%s"</script>'%(source))
        # additional libraries
        if ((source == "logit") or (source == "onset") or (source == "anova")):
            link.append('<!--prism-->')
            css.append('<link rel="stylesheet" type="text/css" href="css/prism/prism.css">')
            css.append('<link rel="stylesheet" type="text/css" href="css/prism/prism-line-numbers.css">')
            css.append('<script type="text/javascript" language="javascript" src="js/prism/prism.js"></script>')
            css.append('<script type="text/javascript" language="javascript" src="js/prism/prism-r.js"></script>')
            css.append('<script type="text/javascript" language="javascript" src="js/prism/prism-python.js"></script>')
            css.append('<script type="text/javascript" language="javascript" src="js/prism/prism-line-numbers.js"></script>')
            css.append('<script type="text/javascript" language="javascript" src="js/prism/prism-normalize-whitespace.js"></script>')
        
        # finish header
        head = ('\n\t'.join(map(str, link))) + ('\n\t'.join(map(str, css))) + ('\n\t'.join(map(str, js)))
        
        #if displaying seaborn plots
        if source == "plots":
            html_plots = []
            #for each plot
            for idx, p in enumerate(plots):
                html_p = ['<div class="figure" style="max-width:800px;">',
                            #title
                            '<div class="title"><b>Figure %s.</b> %s</div>'%((idx+1), p['title']),
                            #date
                            '<div class="date"> Last Updated: ' + '%s'%(date) + '</div>',
                            #figure
                            '<a href="img\\' + p['file'] + '">\n<img class="figure" src="img\\' + p['file'] + '">\n</a>',
                            #footnote
                            '<div class="footnote">%s</div>'%(p['footnote']),
                        '</div>']
                html_plots.append(('\n\t'.join(map(str, html_p))))
                
            #build body
            ##add none as class only if there is no intro
            if intro!=None:
                intro_class = ''
            else:
                intro_class = None
                
            body = ['<div class="container" style="">',
                        '<div class="container-figure %s" style="">'%(display),
                            '<div class="intro %s">%s</div>'%(intro_class, intro),
                                (''.join(map(str, html_plots))),
                            '</div>',
                        '</div>',
                    '</div>']   
            body = ('\n\t'.join(map(str, body)))
            
            #build html
            html = ['<html>',
                    '<head>',
                        head,
                    '</head>',
                    '<body id="body">',
                        body,
                    '</body>',
                    '</html>']
            html = ('\n' .join(map(str, html)))
            
            #save
            with open(path,'w') as html_:
                html_.write(html)
                
            #--------finished
            console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
            return html
        
        #if displaying dataframe tables
        else:         
            #build body
            ##save table to html for datatable
            if ((source == "demographic") or (source == "device") or (source == "task") or (source == "summary")):
                #allow word wrapping
                if(source == "demographic") or (source == "task"):
                    wrap = "wrap"
                else:
                    wrap = "nowrap"
                # save table to csv for downloading
                ## check if paths exist
                p_ = config['path']['output'] + '/analysis/html/csv/'
                if not os.path.exists(p_):
                    os.makedirs(p_)
                df.to_csv(p_ + '%s.csv'%(name), index=False)
                #get table
                table = df.to_html(index=False, index_names=True).replace('<table border="1" class="dataframe">',
                '<table id="table" class="table '+source+' table-striped table-bordered \
                hover dt-responsive '+wrap+'" cellspacing="0" width="100%">').replace('&gt;','>').replace('&lt;','<')
            elif (source == "definitions"):
                #wordwrap
                wrap = "nowrap"
                #prevent trucating strings
                width = pd.get_option('display.max_colwidth')
                pd.set_option('display.max_colwidth', -1)
                ##save table to csv for downloading
                df.to_csv(config['path']['output'] + '/analysis/html/csv/%s.csv'%(name), index=False)
                #get table
                table = df.to_html(index=False, index_names=True).replace('<table border="1" class="dataframe">',
                '<table id="table" class="table '+source+' table-striped table-bordered \
                hover dt-responsive '+wrap+'" cellspacing="0" width="100%">')   
                #reset
                pd.set_option('display.max_colwidth', width)
            elif ((source == "logit") or (source == "onset") or (source == "anova")):
                #prevent trucating strings
                width = pd.get_option('display.max_colwidth')
                pd.set_option('display.max_colwidth', -1)
                ##save table to csv for downloading #here saving raw data for future analysis
                raw_data.to_csv(config['path']['output'] + '/analysis/html/csv/%s.csv'%(name), index=False)
                #get table
                table = df.to_html(index=True, index_names=True).replace('<table border="1" class="dataframe">',
                '<table id="table" data-file="'+ name +'" class="table '+source+' table-striped table-bordered \
                hover dt-responsive nowrap" cellspacing="0" width="100%">')
                #reset
                pd.set_option('display.max_colwidth', width)
            else:
                ##check if paths exist
                p_ = config['path']['output'] + '/analysis/html/csv/'
                if not os.path.exists(p_):
                    os.makedirs(p_)
                # save table to csv for downloading
                df.to_csv(p_ + '%s.csv'%(name), index=False)
                #get table
                table = df.to_html(index=True, index_names=True).replace('<table border="1" class="dataframe">',
                '<table id="table" data-file="'+ name +'" class="table '+source+' table-striped table-bordered \
                hover dt-responsive nowrap" cellspacing="0" width="100%">')
      
            #add images to bottom of model
            if ((source == "logit") or (source == "onset") or (source == "anova")):
                html_plots = []
                #for each plot
                if plots != None:
                    fig_num = 0
                    for idx, p in enumerate(plots):
                        if (source == "anova"):
                            #if supplimentary table
                            if (p['type'] == 'table'):
                                if 'anchor' in p:
                                    anchor = p['anchor']
                                _table = p['df']
                                #prevent trucating strings
                                width = pd.get_option('display.max_colwidth')
                                pd.set_option('display.max_colwidth', -1)
                                #convert df to html table
                                _table = _table.to_html(index=True, index_names=True).replace('<table border="1" class="dataframe">',
                                '<table id="table2" data-file="'+ name +'" class="table '+source+' table-striped table-bordered \
                                hover dt-responsive nowrap"\ cellspacing="0" width="100%">')
                                #create table
                                html_p = [
                                    '<div class="figure %s" id="%s">'%(source, anchor),
                                        '<div class="title">%s</div>'%(p['title']),
                                        '<div class="date"> Last Updated: ' + '%s'%(date) + '</div>',
                                        '<div class="dataTables_wrapper form-inline dt-bootstrap">',
                                            '<!--script-->' + '\n',
                                            _table,
                                        '</div>',
                                        '<div class="footnote">%s</div>'%(p['footnote']),
                                    '</div>']
                                html_p = ('\n\t'.join(map(str, html_p)))
                                #reset
                                pd.set_option('display.max_colwidth', width)
                            #else is plot
                            else:
                                fig_num = fig_num + 1
                                if 'anchor' in p:
                                    anchor = p['anchor']  
                                else: 
                                    anchor = ""
                                html_p = ['<div class="figure %s" id="%s">'%(source, anchor),
                                              #title
                                              '<div class="title"><b>Figure %d.</b> %s</div>'%(fig_num, p['title']),
                                              #date
                                              '<div class="date"> Last Updated: ' + '%s'%(date) + '</div>',
                                              #figure
                                              '<a class="img" href="img\\'+p['file']+'">\n<img class="img" src="img\\'+p['file']+'">\n</a>',
                                              #footnote
                                              '<div class="footnote">%s</div>'%(p['footnote']),
                                        '</div>']
                        #else is plot
                        else:
                            fig_num = fig_num + 1
                            if 'anchor' in p:
                                anchor = p['anchor']  
                            else: 
                                anchor = ""
                            html_p = ['<div class="figure %s" id="%s">'%(source, anchor),
                                        #title
                                        '<div class="title"><b>Figure %d.</b> %s</div>'%(fig_num, p['title']),
                                        #date
                                        '<div class="date"> Last Updated: ' + '%s'%(date) + '</div>',
                                        #figure
                                        '<a class="img" href="img\\'+p['file']+'">\n<img class="img" src="img\\'+p['file']+'">\n</a>',
                                        #footnote
                                        '<div class="footnote">%s</div>'%(p['footnote']),
                                    '</div>']
                        
                        #----append to html plots 
                        html_plots.append(('\n\t'.join(map(str, html_p))))
                    
                html_plots = '\n\t'.join(map(str, html_plots))
            else:
                html_plots = ""
                
            ##body
            body = ['<div class="container-large %s" style="">'%(source),
                        '<div class="container" style="">',
                            '<div class="dashboard-main">',
                                '<div class="table-container %s">'%(source),
                                    '<div class="title">'+'%s'%(title)+'</div>',
                                    '<div class="date"> Last Updated: '+'%s'%(date),
                                        '<span class="link" id="code">code</span>',
                                        '<span class="link" id="csv">csv</span>',
                                    '</div>',
                                '<div class="dataTables_wrapper form-inline dt-bootstrap">',
                                    '<!--script-->',
                                    table,
                                '</div>',
                                '<div class="footnote">' + '\n' + '%s'%(footnote) + '</div>',
                                    html_plots,
                                '</div>',
                            '</div>',
                        '</div>',
                    '</div>']
            #replace script within body, then join as string
            if ((source == "logit") or (source == "onset") or (source == "anova")):
                body = [script if x==(                '<!--script-->') else x for x in body]
            # join
            body = ('\n\t'.join(map(str, body)))

            #build footer
            if ((source == "logit") or (source == "onset") or (source == "anova")):
                foot = ['<script>',
                            '$(document).ready(function(){',
                                'getLogitTable();',
                                'additionalTable();',
                                'popover();',
                                'codeButton();',
                            '})',
                        '</script>']
            elif (source == "task"):
                foot = ['<script>',
                            '$(document).ready(function(){',
                                'getLogitTable();',
                                'popover();',
                            '})',
                        '</script>']   
            else:
                foot = ['<script>',
                            '$(document).ready(function(){',
                                'getLogitTable();',
                            '})',
                        '</script>']
            foot = ('\n\t'.join(map(str, foot)))
            
            #build html
            html = ['<html short="%s" long="%s">'%(short, long),
                    '<head>',
                        head,
                    '</head>',
                    '<body id="body">',
                        body,
                    '</body>',
                    '<foot>',
                        foot,
                    '</foot>',
                    '</html>']
            html = ('\n'.join(map(str, html)))
                
    #----save
    # check if paths exist
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    # tidy html
    #html = re.sub("\s\s+", " ", html) #multiple spaces
    # save
    with open(path,'w') as html_:
        html_.write(html)
    console('saved html file at %s'%(path), 'blue')
    
    #--------finished
    console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
    return html

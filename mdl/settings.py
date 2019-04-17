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

class settings():
    """Provide resource for creating links, anchors, calculate significant figures, user-friendly console."""
    def __init__(self, is_library=False):
        """Provide resource for creating links, anchors, calculate significant figures, user-friendly console."""
        self.config = config
        
    @classmethod
    def console(cls, message, color='blue'):
        """
        Allows user-friend console logging using ANSI escape codes.
        
        Parameters
        ----------
        message : :class:`str`
            Message to send to console.
        color : :class:`str`
            Name of color or ANSI escape event to use.
        
        Returns
        -------
        result : :class:`str`
            ANSI escape code.
            
        Examples
        --------
        >>> console(self, message, color='blue)
        >>>
        >>>
            
        Notes
        -----
        Colors are produced using ASCII Oct format. For example: '\033[40m'
        See http://jafrog.com/2013/11/23/colors-in-terminal.html
        """
        
        c_ = dict(
            black = '40m',
            red =  '41m',
            green =  '42m',
            orange = '43m',
            purple = '45m',
            blue =  '46m',
            grey =  '47m'
        )
        
        # result will be in this format: [<PREFIX>];[<COLOR>];[<TEXT DECORATION>][<MESSAGE>][<FINISHING SYMBOL>]
        result = '\033[' + c_[color] + message + '\033[0m'
        
        return print(result)
        
    @classmethod
    def link(cls, name, url):
        """
        Create popover of variable in html.
        
        Parameters
        ----------
        name : :class:`str`
            Name of variable.
        url : :class:`str`
            URL to link to.
        
        Returns
        -------
        link : :class:`str`
            HTML <a> element.
            
        Examples
        --------
        >>>
        >>>'''<a href="#boxplot" class="anchor">boxplot</a>'''
        """
        
        link = '<a href="%s" class="anchor">%s</a>'%(url, name)
        
        return link
    
    @classmethod
    def popover(cls, name, title, description, url=None, **kwargs):
        """
        Create popover of variable in html.
        
        Parameters
        ----------
        name : :class:`str`
            Local name of variable.
        title : :class:`str`
            Title of variable in popover.
        description : :class:`str`
            Description of variable in popover.
        url : :class:`str` or `str`
            URL to include. Default `None`.
        
        Other Parameters
        ----------------
        **kwargs : :class:`str`
            HTML <a> element.
            
        Returns
        -------
        link : :class:`str`
            HTML <a> element.
        
        Examples
        --------
        >>> name = "anova"
        >>> title = "Statistical Models in S"
        >>> description = "Chambers, J., Hastie, T. (1992). Statistical Models in S. Wadsworth & Brooks/Cole."
        >>>popover(name=name, title=title, description=description)
        <a tabindex="0" class="popover-anchor" link-id="anova" data-toggle="popover" data-content="Chambers, J., Hastie, T. (1992). \
        Statistical Models in S. Wadsworth & Brooks/Cole." title="" data-original-title="Statistical Models in S">Chambers, Hastie, 1992</a>
        """
        
        if url != None:
            url = '<a class="anchor" href="%s">%s</a>'%(url, url)
            description = '%s<br>%s'%(description, url)
            
        #create link
        link = '<a tabindex="0" class="popover-anchor" link-id="%s" data-toggle="popover" data-content="%s" title="" data-original-title="%s">%s</a>'\
        %(name, description, title, title)
        #format
        link = re.sub(r'\s+', ' ', link).strip()
        
        return link
    
    @classmethod
    def stn(cls, source):
        """
        Convert to scientific notation.
    
        Parameters
        ----------
        source : :class:`float`
            Original number.
    
        Returns
        -------
        output : :class:`str`
            Number in scientific notation, if (number < 0.0001) or (if number > 9999).
        """
        #convert to float
        source = float(source)
        
        #if less than 0.0001, use scientific notation
        if (source < 0.0001):
            output = '%.2E'%source
        #else if greater than 9999, use scientific notation
        elif (source > 9999):
            output = '%.2E'%source
        #else round number to 4th digit
        else:
            output = '%s'%(round(source, 4))
            
        return output
    
    @classmethod
    def library(cls, required=None):
        """
        Check if required libraries are available.
    
        Parameters
        ----------
        required : :class:`list`
            List of required libraries.
        """
        settings.console('settings.library()', 'green')
        
        #----for timestamp
        _t0 = datetime.now()
        _f = settings.debug(message='t', source="timestamp")
    
        #check libraries for missing
        
        #list of possibly missing packages to install
        if required == None:
            required = ['numpy','scipy','pandas','datetime','rpy2','pytz','seaborn','matplotlib','bokeh', 'nslr_hmm','PyGraphviz']
        
        #for geting os variables
        if platform.system() == "Windows":
            required.append('win32api')
        elif platform.system() =='Darwin':
            required.append('pyobjc')
        
        #try installing and/or importing packages
        try:
            #if pip >= 10.01
            pip_ = pkg_resources.get_distribution("pip").version
            if StrictVersion(pip_) > StrictVersion('10.0.0'):
                from pip._internal import main as _main
                #for required packages check if package exists on device
                for package in required:
                    #if missing, install
                    if importlib.util.find_spec(package) is None:
                        _main(['install',package])
                        
            #else pip < 10.01          
            else:
                #for required packages check if package exists on device
                for package in required:
                    #if missing
                    if importlib.util.find_spec(package) is None:
                        pip.main(['install',package])
                
        except Exception as e:
            return e
            #----finished
            self.console('%s finished in %s msec'%(_f,((datetime.now()-_t0).total_seconds()*1000)), 'blue')
    
    @classmethod
    def debug(cls, message, source='debug'):
        """
        Get function or class for console print.
    
        Parameters
        ----------
        message : :class:`str`
            Log message.
        source : :class:`str`
            Origin of call. Either debug or timestamp.
        
        """
        if source=='debug':
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            event = "%s, line %d, in processing.%s(), %s" % (caller.filename, caller.lineno, caller.function, message)
            print(event)
        elif source=='timestamp':
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            event = "processing.%s()" % (caller.function)
        
        return event

config = {}
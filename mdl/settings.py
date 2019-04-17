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
import inspect
from datetime import datetime
from distutils.version import StrictVersion
import importlib, pkg_resources, pip, platform

class settings():
    """Provide resource for creating links, anchors, calculate significant figures, user-friendly console."""
    def __init__(self):
        pass
    @classmethod
    def console(cls, message, color='blue'):
        """
        Allows user-friend console logging using ANSI escape codes.
        
        Attributes
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
    def stn(cls, source):
        """
        Convert to scientific notation.
    
        Attributes
        ----------
        flt : :class:`float`
            Original number.
    
        Returns
        ----------
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
    def library(cls, required):
        """Check if required libraries are available.
    
        Attributes
        ----------
        required : :class:`list`
           List of required packages.
        
        """
        settings.console('settings.library()', 'green')
        
        #----for timestamp
        _t0 = datetime.now()
        _f = settings.debug(message='t', source="timestamp")
        
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
                        
            #----finished
            settings.console('%s finished in %s msec'%(_f,((datetime.now()-_t0).total_seconds()*1000)), 'blue')
                
        except Exception as e:
            return e
        
    @classmethod
    def debug(cls, message, source='debug'):
        """
        Get function or class for console print.
    
        Attributes
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
    




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Allow mdl.eyetracking.Eyelink to initiate calibration/validation/drift correction.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/mdl
"""
# allowed imports
__all__ = ['Calibration']

# core
from pdb import set_trace as breakpoint
import os
import string
import array
from math import sin, cos, pi
from PIL import Image
import numpy as np

# local libraries
from .. import settings
from . import pylink

class Calibration(pylink.EyeLinkCustomDisplay):
	"""Allow mdl.eyetracking.Eyelink to initiate calibration/validation/drift correction."""
	def __init__(self, w, h, tracker, window):
		"""
        Initiate the mdl.eyetracking.Calibration module.

        Parameters
        ----------
        w,h : :class:`int`
            Screen width, height.
        tracker : :class:`object`
            Eyelink tracker instance.
        window :  `psychopy.visual.Window <https://www.psychopy.org/api/visual/window.html#window>`_
            PsychoPy window instance.
        """
		# import psychopy
		from psychopy import visual, event, sound

		self.visual = visual
		self.event = event
		self.sound = sound

		#---setup display
		pylink.EyeLinkCustomDisplay.__init__(self)

		#----flags
		self.is_calibration = True

		#----window
		self.window = window
		self.bg_color = self.window.color
		self.w = w
		self.h = h
		self.pylinkMinorVer = pylink.__version__.split('.')[1] # minor version 1-Mac, 11-Win/Linux

		#----check the screen units of Psychopy, forcing the screen to use 'pix'
		self.units = self.window.units
		if self.units != 'pix': self.window.setUnits('pix')

		#----mouse
		self.window.setMouseVisible(False)
		self.mouse = event.Mouse(visible=False)
		self.last_mouse_state = -1

		#----sound
		self.path = os.path.dirname(os.path.abspath(__file__)) + "\\"
		self.__target_beep__ = self.sound.Sound(self.path + "dist\\audio\\type.wav", secs=-1, loops=0)
		self.__target_beep__done__ = self.sound.Sound(self.path + "dist\\audio\\qbeep.wav", secs=-1, loops=0)
		self.__target_beep__error__ = self.sound.Sound(self.path + "dist\\audio\\error.wav", secs=-1, loops=0)

		#----color, image
		self.pal = None
		self.imgBuffInitType = 'I'
		self.img_scaling_factor = 4
		self.imagebuffer = array.array(self.imgBuffInitType)
		self.resizeImagebuffer = array.array(self.imgBuffInitType)
		self.size = (192*4, 160*4)
		self.imagebuffer = array.array(self.imgBuffInitType)
		self.resizeImagebuffer = array.array(self.imgBuffInitType)

		#----title
		self.msgHeight = self.size[1]/20.0
		self.title = visual.TextStim(win=self.window, text='', pos=(0,-self.size[1]/2-self.msgHeight), 
									units='pix', height=self.msgHeight, bold=False, color='black', 
									colorSpace='rgb', opacity=1, alignVert='center', wrapWidth=self.w)
		self.title.fontFiles = [self.path + "dist\\utils\\Helvetica.ttf"]
		self.title.font = 'Helvetica'

		#----menu
		menu = '\n'.join(['Show/Hide camera [Enter]','Switch Camera [Left, Right]',
		'Calibration [C]','Validation [V]','Continue [O]','CR [+/-]',
		'Pupil [Up/Down]','Search limit [Alt+arrows]'])
		self.menu = visual.TextStim(win=self.window, text=menu, pos=(-(self.w *.48), 0), units='pix', 
									height=38, bold=False, color='black', colorSpace='rgb', 
									opacity=1, alignHoriz='left', alignVert='center')
		self.menu.fontFiles = [self.path + "dist\\utils\\Helvetica.ttf"]
		self.menu.font = 'Helvetica'

		#----fixation
		self.line = visual.Line(win=self.window, start=(0, 0), end=(0,0), 
							lineWidth=2.0, lineColor=[0,0,0], units='pix')
		#----set circles
		self.outside = visual.Circle(win=self.window, pos=(0, 0), radius=10, fillColor=[0,0,0], 
							lineColor=[1,1,1], units='pix')
		self.inside = visual.Circle(win=self.window, pos=(0,0), radius=3, fillColor=[-1,-1,-1], 
							lineColor=[-1,-1,-1], units='pix') 

	def setup_cal_display(self):
		"""
		Shows the 'Camera Setup' screen along with menu options.

		Notes
		-----
		This function is called to setup calibration/validation display. This will be called just before we enter into 
		the calibration or validataion or drift correction mode. Any allocation per calibration or validation drift 
		correction can be done here. Also, it is normal to clear the display in this call. 

		"""
		print('setup_cal_display')
		self.window.clearBuffer()
		if self.is_calibration:
			self.menu.autoDraw = True
		self.window.flip()

	def clear_cal_display(self):
		"""Clear the 'Camera Setup' screen along with menu options."""
		print('clear_cal_display')
		self.menu.autoDraw = False
		self.title.autoDraw = False
		self.window.clearBuffer()
		self.window.color = self.bg_color
		self.window.flip()

	def exit_cal_display(self):
		"""Exit the 'Camera Setup' screen along with menu options."""
		print('exit_cal_display')
		self.window.setUnits(self.units)
		self.clear_cal_display()
		self.menu.autoDraw = False
		self.title.autoDraw = False
		#----flag
		self.is_calibration = False
    
	def record_abort_hide(self):
		"""This function is called if aborted"""
		print('record_abort_hide')

	def erase_cal_target(self):
		"""Erase the calibration/validation target."""
		print('erase_cal_target')
		self.clear_cal_display()
		#self.window.flip()
        
	def draw_cal_target(self, x, y):
		"""Draw the calibration/validation target."""
		print('draw_cal_target')
		self.clear_cal_display()
		# convert to psychopy coordinates
		x = x - (self.w / 2)
		y = -(y - (self.h / 2))

		# set calibration target position
		self.outside.pos = (x, y)
		self.inside.pos = (x, y)

		# display
		self.outside.draw()
		self.inside.draw()
		self.window.flip()

	def play_beep(self, beepid):
		""" Play a sound during calibration/drift correction."""
		if beepid == pylink.CAL_TARG_BEEP or beepid == pylink.DC_TARG_BEEP:
			self.__target_beep__.play()
		if beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
			self.__target_beep__error__.play()
		if beepid in [pylink.CAL_GOOD_BEEP, pylink.DC_GOOD_BEEP]:
			self.__target_beep__done__.play()
        
	def getColorFromIndex(self, colorindex):
		"""Return psychopy colors for elements in the camera image."""
		if colorindex   ==  pylink.CR_HAIR_COLOR:          return (1,1,1)
		elif colorindex ==  pylink.PUPIL_HAIR_COLOR:       return (1,1,1)
		elif colorindex ==  pylink.PUPIL_BOX_COLOR:        return (-1,1,-1)
		elif colorindex ==  pylink.SEARCH_LIMIT_BOX_COLOR: return (1,-1,-1)
		elif colorindex ==  pylink.MOUSE_CURSOR_COLOR:     return (1,-1,-1)
		else:                                              return (0,0,0)
        
	def draw_line(self, x1, y1, x2, y2, colorindex):
		"""Draw a line. This is used for drawing crosshairs/squares."""
		y1 = (-y1  + self.size[1]/2)* self.img_scaling_factor
		x1 = (+x1  - self.size[0]/2)* self.img_scaling_factor
		y2 = (-y2  + self.size[1]/2)* self.img_scaling_factor
		x2 = (+x2  - self.size[0]/2)* self.img_scaling_factor
		color = self.getColorFromIndex(colorindex)
		self.line.start     = (x1, y1)
		self.line.end       = (x2, y2)
		self.line.lineColor = color
		self.line.draw()

	def draw_lozenge(self, x, y, width, height, colorindex):
		"""
		Draw a lozenge to show the defined search limits (x,y) is top-left corner of the bounding box.
		"""
		width = width * self.img_scaling_factor
		height = height * self.img_scaling_factor
		y = (-y + self.size[1]/2)* self.img_scaling_factor
		x = (+x - self.size[0]/2)* self.img_scaling_factor
		color = self.getColorFromIndex(colorindex)

		if width > height:
			rad = height / 2
			if rad == 0: return #cannot draw the circle with 0 radius
			Xs1 = [rad*cos(t) + x + rad for t in np.linspace(pi/2, pi/2+pi, 72)]
			Ys1 = [rad*sin(t) + y - rad for t in np.linspace(pi/2, pi/2+pi, 72)]
			Xs2 = [rad*cos(t) + x - rad + width for t in np.linspace(pi/2+pi, pi/2+2*pi, 72)]
			Ys2 = [rad*sin(t) + y - rad for t in np.linspace(pi/2+pi, pi/2+2*pi, 72)]
		else:
			rad = width / 2
			if rad == 0: return #cannot draw sthe circle with 0 radius
			Xs1 = [rad*cos(t) + x + rad for t in np.linspace(0, pi, 72)]
			Ys1 = [rad*sin(t) + y - rad for t in np.linspace(0, pi, 72)]
			Xs2 = [rad*cos(t) + x + rad for t in np.linspace(pi, 2*pi, 72)]
			Ys2 = [rad*sin(t) + y + rad - height for t in np.linspace(pi, 2*pi, 72)]

		vertices = list(zip(Xs1+Xs2, Ys1+Ys2))
		lozenge = self.visual.ShapeStim(self.window, vertices=vertices, lineWidth=2.0, lineColor=color, closeShape=True, units='pix')
		lozenge.draw()
    
	def get_mouse_state(self):
		"""Get the current mouse position and status"""
		X, Y = self.mouse.getPos()
		mX = self.size[0]/2.0*self.img_scaling_factor + X 
		mY = self.size[1]/2.0*self.img_scaling_factor - Y
		if mX <=0: mX =  0
		if mX > self.size[0]*self.img_scaling_factor:
			mX = self.size[0]*self.img_scaling_factor
		if mY < 0: mY =  0
		if mY > self.size[1]*self.img_scaling_factor:
			mY = self.size[1]*self.img_scaling_factor
		state = self.mouse.getPressed()[0] 
		mX = mX/self.img_scaling_factor
		mY = mY/self.img_scaling_factor

		if self.pylinkMinorVer == '1':
			mX = mX *2; mY = mY*2

		return ((mX, mY), state)
    
	def get_input_key(self):
		"""
		This function will be constantly pools, update the stimuli here is you need
		dynamic calibration target.
		"""
		ky=[]
		for keycode, modifier in self.event.getKeys(modifiers=True):
			k = pylink.JUNK_KEY
			if keycode   == 'f1': k = pylink.F1_KEY
			elif keycode == 'f2': k = pylink.F2_KEY
			elif keycode == 'f3': k = pylink.F3_KEY
			elif keycode == 'f4': k = pylink.F4_KEY
			elif keycode == 'f5': k = pylink.F5_KEY
			elif keycode == 'f6': k = pylink.F6_KEY
			elif keycode == 'f7': k = pylink.F7_KEY
			elif keycode == 'f8': k = pylink.F8_KEY
			elif keycode == 'f9': k = pylink.F9_KEY
			elif keycode == 'f10': k = pylink.F10_KEY
			elif keycode == 'pageup': k = pylink.PAGE_UP
			elif keycode == 'pagedown': k = pylink.PAGE_DOWN
			elif keycode == 'up': k = pylink.CURS_UP
			elif keycode == 'down': k = pylink.CURS_DOWN
			elif keycode == 'left': k = pylink.CURS_LEFT
			elif keycode == 'right': k = pylink.CURS_RIGHT
			elif keycode == 'backspace': k = ord('\b')
			elif keycode == 'return': k = pylink.ENTER_KEY
			elif keycode == 'space': k = ord(' ')
			elif keycode == 'escape': k = pylink.ESC_KEY
			elif keycode == 'tab': k = ord('\t')
			elif keycode in string.ascii_letters: k = ord(keycode)
			elif k== pylink.JUNK_KEY: k = 0

		# plus/equal & minux signs for CR adjustment
		if keycode in ['num_add', 'equal']: k = ord('+')
		if keycode in ['num_subtract', 'minus']: k = ord('-')

		if modifier['alt']==True: mod = 256
		else: mod = 0

		ky.append(pylink.KeyInput(k, mod))

		return ky

	def exit_image_display(self):
		"""Clear the camera image."""
		print('exit_image_display')

		self.clear_cal_display()
		self.menu.autoDraw = True
		self.window.flip()

	def alert_printf(self, msg):
		"""Print error messages."""
		print("Error: %s")%(msg)

	def setup_image_display(self, width, height):
		"""Set up the camera image, for newer APIs, the size is 384 x 320 pixels."""
		print('setup_image_display')

		self.last_mouse_state = -1
		self.size = ('384', '320')
		self.menu.autoDraw = True
		self.title.autoDraw = True

	def image_title(self, text):
		print('image_title')
		"""Display or update Pupil/CR info on image screen."""
		self.title.text = text

	def draw_image_line(self, width, line, totlines, buff):
		"""Display image pixel by pixel, line by line."""
		self.size = (width, totlines)

		i = 0
		for i in range(width):
			try: self.imagebuffer.append(self.pal[buff[i]])
			except: pass

		if line == totlines:
			bufferv = self.imagebuffer.tostring()
			img = Image.frombytes("RGBX", (width, totlines), bufferv)
			imgResize = img.resize((width*self.img_scaling_factor, totlines*self.img_scaling_factor))
			imgResizeVisual = self.visual.ImageStim(self.window, image=imgResize, units='pix')
			imgResizeVisual.draw()
			self.draw_cross_hair()
			self.window.flip()
			self.imagebuffer = array.array(self.imgBuffInitType)

	def set_image_palette(self, r,g,b):
		"""Given a set of RGB colors, create a list of 24bit numbers representing the pallet.
		I.e., RGB of (1,64,127) would be saved as 82047, or the number 00000001 01000000 011111111"""

		self.imagebuffer = array.array(self.imgBuffInitType)
		self.resizeImagebuffer = array.array(self.imgBuffInitType)
		sz = len(r)
		i = 0
		self.pal = []
		while i < sz:
			rf = int(b[i])
			gf = int(g[i])
			bf = int(r[i])
			self.pal.append((rf<<16) | (gf<<8) | (bf))
			i = i + 1

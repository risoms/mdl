#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| `@purpose`: Allow imhr.eyetracking.Eyelink to initiate calibration/validation/drift correction.  
| `@date`: Created on Sat May 1 15:12:38 2019  
| `@author`: Semeon Risom  
| `@email`: semeon.risom@gmail.com  
| `@url`: https://semeon.io/d/imhr
"""
# debug
from pdb import set_trace as breakpoint

# allowed imports
__all__ = ['Calibration']

# local libraries
from .. import settings

# check if psychopy is available
try:
	# core
	import string
	import array
	import psychopy
	from math import sin, cos, pi
	from PIL import Image
	from pathlib import Path
	import numpy as np	
except ImportError as e:
	pkg = e.name
	x = {'psychopy':'psychopy','numpy':'numpy','pandas':'pandas','PIL':'Pillow'}
	pkg = x[pkg] if pkg in x else pkg
	raise Exception("No module named '%s'. Please install from PyPI before continuing."%(pkg))

if __name__ == "__main__":
	from . import pylink

class Calibration(pylink.EyeLinkCustomDisplay):
	"""Allow imhr.eyetracking.Eyelink to initiate calibration/validation/drift correction."""
	# add base class
	from . import pylink
	object.__class__ = pylink.EyeLinkCustomDisplay
	def __init__(self, w, h, tracker, window):
		"""Allow imhr.eyetracking.Eyelink to initiate calibration/validation/drift correction.

		Parameters
		----------
		w,h : :class:`int`
			Screen width, height.
		tracker : :class:`object`
			Eyelink tracker instance.
		window :  `psychopy.visual.Window <https://www.psychopy.org/api/visual/window.html#window>`__
			PsychoPy window instance.
		"""
		# inheritance
		from . import pylink
		
		# import psychopy
		from psychopy import visual, event, sound

		#----constants
		# core
		self.console = settings.console
		# psychopy
		self.visual = visual
		self.event = event
		self.sound = sound
		# pylink
		self.pylink = pylink

		#---setup display
		self.pylink.EyeLinkCustomDisplay.__init__(self)

		#----flags
		self.is_calibration = True

		#----window
		self.window = window
		self.bg_color = self.window.color
		self.w = w
		self.h = h
		self.pylinkMinorVer = self.pylink.__version__.split('.')[1] # minor version 1-Mac, 11-Win/Linux

		#----check the screen units of Psychopy, forcing the screen to use 'pix'
		self.units = self.window.units
		if self.units != 'pix': self.window.setUnits('pix')

		#----mouse
		self.window.setMouseVisible(False)
		self.mouse = event.Mouse(visible=False)
		self.last_mouse_state = -1

		#----sound
		import imhr
		self.path = Path(imhr.__file__).parent
		self.__target_beep__ = self.sound.Sound("%s/dist/audio/type.wav"%(self.path), secs=-1, loops=0)
		self.__target_beep__done__ = self.sound.Sound("%s/dist/audio/qbeep.wav"%(self.path), secs=-1, loops=0)
		self.__target_beep__error__ = self.sound.Sound("%s/dist/audio/qbeep.wav"%(self.path), secs=-1, loops=0)

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
		self.title.fontFiles = ["%s/dist/resources/Helvetica.ttf"%(self.path)]
		self.title.font = 'Helvetica'

		#----menu
		menu = '\n'.join(['Show/Hide camera [Enter]','Switch Camera [Left, Right]',
		'Calibration [C]','Validation [V]','Continue [O]','CR [+/-]',
		'Pupil [Up/Down]','Search limit [Alt+arrows]'])
		self.menu = visual.TextStim(win=self.window, text=menu, pos=(-(self.w *.48), 0), units='pix', 
									height=38, bold=False, color='black', colorSpace='rgb', 
									opacity=1, alignHoriz='left', alignVert='center')
		self.menu.fontFiles = ["%s/dist/resources/Helvetica.ttf"%(self.path)]
		self.menu.font = 'Helvetica'

		#----fixation
		self.line = visual.Line(win=self.window, start=(0, 0), end=(0,0), 
							lineWidth=2.0, lineColor=[0,0,0], units='pix')
		#----set circles
		self.outside = visual.Circle(win=self.window, pos=(0, 0), radius=10, fillColor=[0,0,0], 
							lineColor=[1,1,1], units='pix')
		self.inside = visual.Circle(win=self.window, pos=(0,0), radius=3, fillColor=[-1,-1,-1], 
							lineColor=[-1,-1,-1], units='pix') 
	
	def record_abort_hide(self):
		"""This function is called if aborted."""
		print('record_abort_hide')

	def setup_cal_display(self):
		"""
		Shows the 'Camera Setup' screen along with menu options.

		Notes
		-----
		This function is called to setup calibration/validation display. This will be
		called just before we enter into the calibration or validataion or drift correction
		mode. Any allocation per calibration or validation drift correction can be done
		here. Also, it is normal to clear the display in this call. 

		"""
		self.console('Displaying Calibration Setup.','green')
		self.window.clearBuffer()
		self.menu.autoDraw = True
		self.title.autoDraw = True
		self.setup_image_display('384','320')
		self.window.flip()

	def clear_cal_display(self):
		"""Clear the 'Camera Setup' screen along with menu options."""
		self.console('Clearing calibration dot.','orange')
		self.menu.autoDraw = False
		self.title.autoDraw = False
		self.window.clearBuffer()
		self.window.color = self.bg_color
		self.window.flip()

	def exit_cal_display(self):
		"""Exit the 'Camera Setup' screen along with menu options."""
		self.console('Exit Camera Setup screen.','green')
		self.window.setUnits(self.units)
		self.clear_cal_display()
		#----flag
		self.is_calibration = False
		
	def draw_cal_target(self, x, y):
		"""Draw the calibration/validation target."""
		self.console('Draw the calibration/validation target.','orange')
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

	def erase_cal_target(self):
		"""Erase the calibration/validation target."""
		self.console('Erase the calibration/validation target.','blue')
		self.clear_cal_display()

	def play_beep(self, beepid):
		"""Play a sound during calibration/drift correction."""
		self.console('Play a sound during calibration/drift correction.','blue')
		if beepid == self.pylink.CAL_TARG_BEEP or beepid == self.pylink.DC_TARG_BEEP:
			self.console('CAL_TARG_BEEP', 'purple')
			self.__target_beep__.play()
		elif beepid == self.pylink.CAL_ERR_BEEP or beepid == self.pylink.DC_ERR_BEEP:
			self.console('CAL_ERR_BEEP', 'purple')
			self.__target_beep__error__.play()
		elif beepid in [self.pylink.CAL_GOOD_BEEP, self.pylink.DC_GOOD_BEEP]:
			self.console('CAL_ERR_BEEP', 'purple')
			self.__target_beep__done__.play()
		
	def getColorFromIndex(self, colorindex):
		"""Return psychopy colors for elements in the camera image."""
		if colorindex   ==  self.pylink.CR_HAIR_COLOR:          return (1,1,1)
		elif colorindex ==  self.pylink.PUPIL_HAIR_COLOR:       return (1,1,1)
		elif colorindex ==  self.pylink.PUPIL_BOX_COLOR:        return (-1,1,-1)
		elif colorindex ==  self.pylink.SEARCH_LIMIT_BOX_COLOR: return (1,-1,-1)
		elif colorindex ==  self.pylink.MOUSE_CURSOR_COLOR:     return (1,-1,-1)
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
		Draw a lozenge to show the defined search limits (x,y) is top-left corner of the
		bounding box.
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
		This function will constantly pool, update the stimuli here is you need
		dynamic calibration target.
		"""
		ky=[]
		for keycode, modifier in self.event.getKeys(modifiers=True):
			k = self.pylink.JUNK_KEY
			if keycode   == 'f1': k = self.pylink.F1_KEY
			elif keycode == 'f2': k = self.pylink.F2_KEY
			elif keycode == 'f3': k = self.pylink.F3_KEY
			elif keycode == 'f4': k = self.pylink.F4_KEY
			elif keycode == 'f5': k = self.pylink.F5_KEY
			elif keycode == 'f6': k = self.pylink.F6_KEY
			elif keycode == 'f7': k = self.pylink.F7_KEY
			elif keycode == 'f8': k = self.pylink.F8_KEY
			elif keycode == 'f9': k = self.pylink.F9_KEY
			elif keycode == 'f10': k = self.pylink.F10_KEY
			elif keycode == 'pageup': k = self.pylink.PAGE_UP
			elif keycode == 'pagedown': k = self.pylink.PAGE_DOWN
			elif keycode == 'up': k = self.pylink.CURS_UP
			elif keycode == 'down': k = self.pylink.CURS_DOWN
			elif keycode == 'left': k = self.pylink.CURS_LEFT
			elif keycode == 'right': k = self.pylink.CURS_RIGHT
			elif keycode == 'backspace': k = ord('\b')
			elif keycode == 'return': k = self.pylink.ENTER_KEY
			elif keycode == 'space': k = ord(' ')
			elif keycode == 'escape': k = self.pylink.ESC_KEY
			elif keycode == 'tab': k = ord('\t')
			elif keycode in string.ascii_letters: k = ord(keycode)
			elif k== self.pylink.JUNK_KEY: k = 0

			# plus/equal & minux signs for CR adjustment
			if keycode in ['num_add', 'equal']: k = ord('+')
			if keycode in ['num_subtract', 'minus']: k = ord('-')
	
			if modifier['alt']==True: mod = 256
			else: mod = 0
	
			ky.append(self.pylink.KeyInput(k, mod))

		return ky

	def exit_image_display(self):
		"""Clear the camera image."""
		self.console('Clear the camera image and title.','blue')

		self.clear_cal_display()
		self.menu.autoDraw = True
		self.title.autoDraw = False
		self.window.flip()
		self.window.flip()

	def alert_printf(self, msg):
		"""Print error messages."""
		print("Error: %s")%(msg)

	def setup_image_display(self, width, height):
		"""Set up the camera image, for newer APIs, the size is 384 x 320 pixels."""
		self.console('Set up the camera image.','blue')
		self.last_mouse_state = -1
		self.size = ('384', '320')
		self.menu.autoDraw = True
		self.title.autoDraw = True

	def image_title(self, text):
		"""Display or update Pupil/CR info on image screen."""
		self.console('Display or update Pupil/CR info on image screen.','blue')
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

	def set_image_palette(self, r, g, b):
		"""
		Given a set of RGB colors, create a list of 24bit numbers representing the
		pallet. Example: RGB of (1,64,127) would be saved as 82047, or the number 00000001
		01000000 011111111
		"""
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

# Define custom calibration display using Psychopy
from psychopy import event, visual, sound
import pylink
import scipy
import numpy as np
import tempfile
import os

class calibration_display(pylink.EyeLinkCustomDisplay):
    '''This inherits a default class from pylink then adds psychopy stim.'''

    def __init__(self, w, h, tracker, window):
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.sres = (w, h)

        # Set up window
        self.window = window
        self.window.flip(clearBuffer=True)
        self.mouse = None

        # Define stimuli
        self.backcolor = window.color
        if sum(window.color) != 0:
            tcolout = -(window.color)
        else:
            tcolout = -1
        self.txtcol = tcolout

        self.targetout = visual.Circle(self.window, pos=(0, 0), radius=10,
                                       fillColor=[1,1,1],
                                       lineColor=[1,1,1], 
                                       units='pix')

        self.targetin = visual.Circle(self.window, pos=(0, 0), radius=3,
                                      fillColor=[-1,-1,-1],
                                      lineColor=[-1,-1,-1],
                                      units='pix')

        # Set up sounds
        #self.__target_beep__ = sound.Sound("_sound/type.wav",secs=-1,loops=0)
        #self.__target_beep__done__ = sound.Sound("_sound/qbeep.wav",secs=-1,loops=0)
        #self.__target_beep__error__ = sound.Sound("_sound/error.wav",secs=-1,loops=0)

        # Image drawing variables (used later)
        self.rgb_index_array = None
        self.imagetitlestim = None
        self.imgstim_size = None
        self.eye_image = None
        self.lineob = None
        self.loz = None

        # Define tracker
        self.setTracker(tracker)

    def setTracker(self, tracker):
        ''' Initial camera set-up for calibration '''

        self.tracker = tracker
        self.tracker_version = tracker.getTrackerVersion()
        if (self.tracker_version >= 3):
            self.tracker.sendCommand("enable_search_limits=YES")
            self.tracker.sendCommand("track_search_limits=YES")
            self.tracker.sendCommand("autothreshold_click=YES")
            self.tracker.sendCommand("autothreshold_repeat=YES")
            self.tracker.sendCommand("enable_camera_position_detect=YES")

    def setup_cal_display(self):
        """
        Sets up the initial calibration display, which contains a menu with
        instructions.
        """
        menu_screen = visual.ImageStim(self.window, name='menu_screen',
                                       image="Instructions/menu.png", mask=None,
                                       ori=0, pos=[0, 0], size=None,
                                       color=[1,1,1], colorSpace='rgb', opacity=1,
                                       flipHoriz=False, flipVert=False,
                                       texRes=128, interpolate=True, depth=-1.0)

        menu_screen.draw()
        #self.targetout.draw()
        self.window.flip()

    def exit_cal_display(self):
        """Exits calibration display."""
        
        self.clear_cal_display()

    def record_abort_hide(self):
        pass

    def clear_cal_display(self):
        self.setup_cal_display()

    def erase_cal_target(self):
        self.window.flip()

    def draw_cal_target(self, x, y):
        # Convert to psychopy coordinates
        x = x - (self.sres[0] / 2)
        y = -(y - (self.sres[1] / 2))

        # Set calibration target position
        self.targetout.pos = (x, y)
        self.targetin.pos = (x, y)

        # Display
        #self.play_beep(pylink.CAL_TARG_BEEP)
        self.targetout.draw()
        self.targetin.draw()
        self.window.flip()

    #def play_beep(self, beepid):
    #    if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
    #        self.__target_beep__.play()
    #    elif beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
    #        self.__target_beep__error__.play()
    #    else:#	CAL_GOOD_BEEP or DC_GOOD_BEEP
    #        self.__target_beep__done__.play()

    def getColorFromIndex(self, colorindex):
        if colorindex == pylink.CR_HAIR_COLOR:
            return (1, 1, 1)
        elif colorindex == pylink.PUPIL_HAIR_COLOR:
            return (1, 1, 1)
        elif colorindex == pylink.PUPIL_BOX_COLOR:
            return (-1, 1, -1)
        elif colorindex == pylink.SEARCH_LIMIT_BOX_COLOR:
            return (1, -1, -1)
        elif colorindex == pylink.MOUSE_CURSOR_COLOR:
            return (1, -1, -1)
        else:
            return (-1, -1, -1)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        pass

    def draw_lozenge(self, x, y, width, height, colorindex):
        pass

    def get_mouse_state(self):
        pass


    def get_input_key(self):
        ky = []
        v = event.getKeys()

        for key in v:
            pylink_key = None
            if len(key) == 1:
                pylink_key = ord(key)
            elif key == "escape":
                pylink_key = pylink.ESC_KEY
            elif key == "return":
                pylink_key = pylink.ENTER_KEY
            elif key == "pageup":
                pylink_key = pylink.PAGE_UP
            elif key == "pagedown":
                pylink_key = pylink.PAGE_DOWN
            elif key == "up":
                pylink_key = pylink.CURS_UP
            elif key == "down":
                pylink_key = pylink.CURS_DOWN
            elif key == "left":
                pylink_key = pylink.CURS_LEFT
            elif key == "right":
                pylink_key = pylink.CURS_RIGHT
            else:
                print('Error! :{} is not a used key.'.format(key))
                return

            ky.append(pylink.KeyInput(pylink_key, 0))

        return ky

    def exit_image_display(self):
        self.clear_cal_display()

    def alert_printf(self, msg):
        print "alert_printf %s" % msg

    def setup_image_display(self, width, height):

        self.size = (width / 2, height / 2)
        self.clear_cal_display()
        self.last_mouse_state = -1

        # Create array to hold image data later
        if self.rgb_index_array is None:
            self.rgb_index_array = np.zeros((self.size[1], self.size[0]),
                                            dtype=np.uint8)

    def image_title(self, text):
        # Display or update Pupil/CR info on image screen
        if self.imagetitlestim is None:
            self.imagetitlestim = visual.TextStim(self.window,
                                                  text=text,
                                                  pos=(0, self.window.size[
                                                      1] / 2 - 15), height=28,
                                                  color=self.txtcol,
                                                  alignHoriz='center',
                                                  alignVert='top',
                                                  wrapWidth=self.window.size[
                                                                0] * .8,
                                                  units='pix')
        else:
            self.imagetitlestim.setText(text)

    def draw_image_line(self, width, line, totlines, buff):
        # Get image info for each line of image
        for i in range(width):
            self.rgb_index_array[line - 1, i] = buff[i]

        # Once all lines are collected turn into an image to display
        if line == totlines:
            # Make image
            image = scipy.misc.toimage(self.rgb_index_array,
                                       pal=self.rgb_pallete,
                                       mode='P')
            # Resize Image
            if self.imgstim_size is None:
                maxsz = self.sres[0] / 2
                mx = 1.0
                while (mx + 1) * self.size[0] <= maxsz:
                    mx += 1.0
                self.imgstim_size = int(self.size[0] * mx), int(
                    self.size[1] * mx)
            image = image.resize(self.imgstim_size)

            # Save image as a temporay file
            tfile = os.path.join(tempfile.gettempdir(), '_eleye.png')
            image.save(tfile, 'PNG')

            # Need this for target distance to show up
            self.__img__ = image
            self.draw_cross_hair()
            self.__img__ = None

            # Create eye image
            if self.eye_image is None:
                self.eye_image = visual.ImageStim(self.window, tfile,
                                                  size=self.imgstim_size,
                                                  units='pix')
            else:
                self.eye_image.setImage(tfile)

            # Redraw the Camera Setup Mode graphics
            self.eye_image.draw()
            if self.imagetitlestim:
                self.imagetitlestim.draw()

            # Display
            self.window.flip()

    def set_image_palette(self, r, g, b):
        # This does something the other image functions need
        self.clear_cal_display()
        sz = len(r)
        self.rgb_pallete = np.zeros((sz, 3), dtype=np.uint8)
        i = 0
        while i < sz:
            self.rgb_pallete[i:] = int(r[i]), int(g[i]), int(b[i])
            i += 1

    def dummynote(self):
        # Draw Text
        visual.TextStim(self.window, text='Dummy Connection with EyeLink',
                        color=self.txtcol).draw()
        self.window.flip()

        # Wait for key press
        event.waitKeys()
        self.window.flip()
# -*- coding: utf-8 -*-
#create combinations of each pair of images: #https://stackoverflow.com/questions/12935194/combinations-between-two-lists

#logging
import logging as errorlog
import os  # handy system and path functions
from subprocess import check_output

#set up logging to file
errorlog.basicConfig(
    filename='error.log', 
    filemode='w', 
    level=errorlog.DEBUG, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logger=errorlog.getLogger(__name__)

import platform
import _winreg
def get_registry_value(key, subkey, value):
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value
    
def cpu():
    try:
        cputype = get_registry_value(
            "HKEY_LOCAL_MACHINE", 
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")
    except:
        import wmi, pythoncom
        pythoncom.CoInitialize() 
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cputype = i.Name
        pythoncom.CoUninitialize()
 
    if cputype == 'AMD Athlon(tm)':
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %.2f Ghz' % (cpuspeed / 1000.0)
    elif cputype == 'AMD Athlon(tm) Processor':
        import wmi
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %s' % cpuspeed
    else:
        pass
    return cputype
    
log_system = platform.system() +" " + platform.win32_ver()[0]#windows 7
log_cpu = cpu() #cpu
#log_video = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
log_video = check_output("wmic path win32_VideoController get VideoProcessor")
log_video = (' '.join(log_video.split())).replace("VideoProcessor ","")

errorlog.debug(log_system)
errorlog.debug(log_cpu)
errorlog.debug(log_video)

#--------------------------------------------------------------------------------------------------begin logging
try: #use _file_ in most cases
    dir = os.path.dirname(__file__)
except NameError:  #except when running python from py2exe script
    import sys
    dir = os.path.dirname(sys.argv[0])
    
while True:
    try:
        from PIL import Image
        
        #directory
        old = os.path.join(dir, 'original')
        if not os.path.exists("new"):
            os.makedirs("new")        
        
        #cmd input
        print ("Enter the length/width value of the image you wish to crop to, in pixels.")
        print ("Example '250'")
        print("")
        lw = raw_input("length/width value: ")
        lw = int(lw)
        
        print("")
        print ("Now enter the horizontal offset, in pixels. Example '10'.")
        print ("Enter 0 for centering.")
        print("")
        h_offset = raw_input("horizontal offset: ")
        h_offset = int(h_offset)

        print("")
        print ("Now enter the vertical offset, in pixels. Example '10'.")
        print ("Enter 0 for centering.")
        print("")
        v_offset = raw_input("vertical offset: ")
        v_offset = int(v_offset)
        
        im_lw = 450
        left = h_offset + ((im_lw - lw)/2)
        up = v_offset + ((im_lw - lw)/2)
        right = h_offset + ((im_lw + lw)/2)
        down = v_offset + ((im_lw + lw)/2)
        print(left,up,right,down)
        
        for img in os.listdir(old):
            im = Image.open(os.path.join(old, img))
            im = im.crop((left,up,right,down))
            
            #resize
            wpercent = (im_lw/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((im_lw, hsize), Image.ANTIALIAS)
                
            #add border
            img_w, img_h = im.size
            background = Image.new("RGB", (im_lw,im_lw), (110,110,110))
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
        
            #paste image to background    
            background.paste(im, offset)
            
            #save image
            fileName, fileExtension=os.path.splitext(img)
            background.save("new/"+fileName+".png","PNG")
        
        exit()    
    #--------------------------------------------------------------------------------------------------end logging
    except Exception as e: 
        logger.error(e, exc_info=True)
        exit()
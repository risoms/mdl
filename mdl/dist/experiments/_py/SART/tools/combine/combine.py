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
while True:
    try:
        from PIL import Image
        import itertools
        
        try: #use _file_ in most cases
            dir = os.path.dirname(__file__)
        except NameError:  #except when running python from py2exe script
            import sys
            dir = os.path.dirname(sys.argv[0])
        
        #cmd input
        print ("Enter the interpolation alpha factor (0.0-1.0) you wish to use on the images.")
        print ("If alpha is 0.0 a copy of the FACE image is returned, if alpha is 1.0 a copy of the SCENE image is returned.")
        print("")
        blend = raw_input("alpha value: ")
        blend = float(blend)
        
        #setting directories and paths
        ##new images
        print ("Now name the folder you wish to store the images.")
        print("")
        dnew = raw_input("folder: ")
        if not os.path.exists(dnew):
            os.makedirs(dnew)
        
        ##scenes
        dscenes = os.path.join(dir, 'original/scenes')
        lscenes = os.listdir(dscenes)
        lscenes = [os.path.splitext(x)[0] for x in lscenes] #stripping .png
        
        #faces
        dfaces = os.path.join(dir, 'original/faces')
        lfaces = os.listdir(dfaces)
        lfaces = [os.path.splitext(x)[0] for x in lfaces] #stripping .png
        
        # all possible combinations of two lists
        ## lcombine.__len__() = 190 faces * 100 scenes = 19000 possible combinations
        lcombine = [[x,y] for x in lfaces for y in lscenes] #as lists within lists
        lcombine2 = list(itertools.product(lscenes, lfaces)) #as tuples within lists
        
        
        #combine images
        for i in range(len(lcombine)):
            #loading
            face_image = lcombine[i][0]
            errorlog.debug("#----------------------------------------------face: "+face_image)
            print(face_image)
            face = Image.open("original/faces/"+face_image+".png")
            scene_image = lcombine[i][1]
            print(scene_image)
            errorlog.debug("#----------------------------------------------face: "+scene_image)
            scene = Image.open("original/scenes/"+scene_image+".png")
            
            #convert to RGBA
            face = face.convert("RGBA")
            scene = scene.convert("RGBA")
            
            #blend to new image and save
            new_img = Image.blend(face, scene, blend)
            new_img.save(dnew+"/"+lcombine[i][0]+"_"+lcombine[i][1]+".png","PNG")
    #--------------------------------------------------------------------------------------------------end logging
    except Exception as e: 
        logger.error(e, exc_info=True)
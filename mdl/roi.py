#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----core
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#----photoshop
from psd_tools import PSDImage
#----json
import os
import glob
#----base64
import cv2

#garbage collection
import gc

class roi():
    def __init__():
        pass
        
directory = glob.glob(os.path.join(raw_p + "*.psd"))

"""
for each image
"""
meta_all = []
for k in range(0, directory.__len__()):
    print('for each image')
    #read image
    psd = PSDImage.load(directory[k])    
    image_name = os.path.splitext(os.path.basename(directory[k]))[0]
    print(image_name)
    
    #metadata
    s1 = pd.Series(name=image_name) #blank series
    s1['filename'] = '%s.png'%(image_name)
    s1['channels'] = psd.header[0] #read channels
    s1['resolution'] = [psd.header[2], psd.header[1]] #length and width
    
    #save image
    #PSD = psd.as_PIL()
    #white background
    #PSD.save('output/%s.png'%(image_name))
    
    """
    for each layer/ROI
    """
    coord_image = [] #roi coordinates list (per)
    print('for each layer/ROI')
    for i in range(0, len(psd.layers)-1):
        """get layer"""  
        #prepare metadata
        layer = psd.layers[i]
        meta_string = layer.name
        meta = pd.DataFrame(data=(item.split("=") for item in meta_string.split(";")),columns={'key','value'})
        s2 = pd.Series(meta['value'].tolist(),meta['key'].tolist())
        
        #roi name
        s2['name'] = s2['name'].replace("roi","")
        
        #valence
        for r in (("pos", "positive"), ("neg", "negative")):
            s2['valence'] = s2['valence'].replace(*r)
        
        """save layer/ROI as image"""
        print('saving %s as image'%(s2['name']))
        PSDlayer = layer.as_PIL()
        #create blank background               
        #background = Image.new('RGB', PSD.size, (255, 255, 255))
        #paste layer and blank background
        #background.paste(PSDlayer,mask=PSDlayer.split()[3])
        #background.save('output/%s-%s-L%s.jpg'%(image_name,layerName,i))

        """search metadata string"""
        s2['human'] = None
        s2['animal'] = None
        s2['gender'] = None
        s2['behavior'] = None
        s2['body'] = None
        s2['object'] = None
        s2['age'] = None
        s2['other'] = None
        
        #human
        if meta_string.find('tag=human') != -1:
            s2['human'] = True
        else:
            s2['human'] = False
            
        #animal
        if meta_string.find('tag=fish') != -1:
            s2['animal'] = ['fish']
        elif meta_string.find('tag=giraffe') != -1:
            s2['animal'] = ['giraffe']
        elif meta_string.find('tag=flies') != -1:
            s2['animal'] = ['fly']
        elif meta_string.find('tag=bird') != -1:
            s2['animal'] = ['bird']
        elif meta_string.find('tag=dog') != -1:
            s2['animal'] = ['dog']
        else:
            s2['animal'] = []
        
        #gender
        l_gender = []
        ##female
        if (meta_string.find('tag=woman') != -1) or\
        (meta_string.find('tag=women') != -1) or\
        (meta_string.find('tag=female') != -1):
            l_gender.append('female')
        ##male
        if (meta_string.find('tag=man') != -1) or\
        (meta_string.find('tag=men') != -1) or\
        (meta_string.find('tag=male') != -1):
            l_gender.append('male')
        s2['gender'] = l_gender
        l_gender = []
        
        #behavior
        l_behavior = []
        if meta_string.find('tag=waving') != -1:
            l_behavior.append('waving')
        if meta_string.find('tag=crying') != -1:
            l_behavior.append('crying')
        if meta_string.find('tag=pickup') != -1:
            l_behavior.append('pickup')
        if meta_string.find('tag=angry') != -1:
            l_behavior.append('angry')
        if meta_string.find('tag=grief') != -1:
            l_behavior.append('grief')
        if meta_string.find('tag=happy') != -1:
            l_behavior.append('happy')
        if meta_string.find('tag=kiss') != -1:
            l_behavior.append('kiss')
        if meta_string.find('tag=sad') != -1:
            l_behavior.append('sad')
        if meta_string.find('tag=hiding') != -1:
            l_behavior.append('hiding')
        if meta_string.find('tag=injured') != -1:
            l_behavior.append('injured')
        if meta_string.find('tag=starving') != -1:
            l_behavior.append('starving')
        if meta_string.find('tag=death') != -1:
            l_behavior.append('death')
        s2['behavior'] = l_behavior
        l_behavior = []
        
        #body
        l_body = []
        if meta_string.find('tag=face') != -1:
            l_body.append('face')
        if meta_string.find('tag=arm') != -1:
            l_body.append('arm')
        if (meta_string.find('tag=hand') != -1) or (meta_string.find('tag=hands') != -1):
            l_body.append('hands')
        if (meta_string.find('tag=foot') != -1) or (meta_string.find('tag=feet') != -1):
            l_body.append('feet')
        if meta_string.find('tag=tears') != -1:
            l_body.append('tears')
        if meta_string.find('tag=bruises') != -1:
            l_body.append('bruises')
        s2['body'] = l_body
        l_body = []
        
        #object     
        l_object = []
        if meta_string.find('tag=boat') != -1:
            l_object.append('boat')
        if meta_string.find('tag=trophy') != -1:
            l_object.append('trophy')
        if meta_string.find('tag=mountains') != -1:
            l_object.append('mountains')
        if meta_string.find('tag=branches') != -1:
            l_object.append('branches')
        if meta_string.find('tag=teddybear') != -1:
            l_object.append('teddybear')
        if meta_string.find('tag=sky') != -1:
            l_object.append('sky')
        if meta_string.find('tag=outdoors') != -1:
            l_object.append('outdoors')
        if (meta_string.find('tag=cigarette') != -1) or (meta_string.find('tag=cigarettes') != -1):
            l_object.append('cigarette')
        if meta_string.find('tag=medal') != -1:
            l_object.append('medal')
        if meta_string.find('tag=oil') != -1:
            l_object.append('oil')
        if meta_string.find('tag=water') != -1:
            l_object.append('water')
        if meta_string.find('tag=trash') != -1:
            l_object.append('trash')
        if meta_string.find('tag=tubing') != -1:
            l_object.append('tubing')
        if meta_string.find('tag=ventilator') != -1:
            l_object.append('ventilator')
        if meta_string.find('tag=bandages') != -1:
            l_object.append('bandages')            
        if meta_string.find('tag=bottle') != -1:
            l_object.append('bottle')
        if meta_string.find('tag=alcohol') != -1:
            l_object.append('alcohol')
        if meta_string.find('tag=rock') != -1:
            l_object.append('rock')                   
        if meta_string.find('tag=smoke') != -1:
            l_object.append('smoke')
        if meta_string.find('tag=money') != -1:
            l_object.append('money')
        if meta_string.find('tag=drugs') != -1:
            l_object.append('drugs')
        s2['object'] = l_object
        l_object = []
        
        #age
        l_age = []
        if meta_string.find('tag=baby') != -1:
            l_age.append('baby')
        if meta_string.find('tag=child') != -1:
            l_age.append('child')
        if meta_string.find('tag=elderly') != -1:
            l_age.append('elderly')
        s2['age'] = l_age
        l_age = []
        
        #other
        l_other = []
        if meta_string.find('tag=crowd') != -1:
            l_other.append('crowd')
        if meta_string.find('tag=family') != -1:
            l_other.append('family')
        s2['other'] = l_other
        l_other = []
        
        """store table of each roi metadata"""
        roi_id = image_name+s2['name']
        meta_all.append([str(roi_id), #relational key in both metadata xy-coodinate tables (per image)
                         image_name, #image name
                         int(s2['name']), #roi name
                         (PSDlayer.size[0],PSDlayer.size[1]), #resolution
                         s2['valence'],
                         s2['human'],
                         s2['animal'],
                         s2['gender'],
                         s2['behavior'],
                         s2['body'],
                         s2['object'],
                         s2['age'],
                         s2['other'],
                         meta_string, #descriptors
                         ])
        #reset
        s2['human'] = None
        s2['animal'] = None
        s2['gender'] = None
        s2['behavior'] = None
        s2['body'] = None
        s2['object'] = None
        s2['age'] = None
        s2['other'] = None
        
        """store table of ROI coordinates"""
        print('storing %s ROI coordinates for export'%(s2['name']))
        for l in range(PSDlayer.size[0]):
            for m in range(PSDlayer.size[1]):
                r,g,b,a=PSDlayer.getpixel((l,m))
                if not r==g==b:
                    coord_image.append([str(roi_id),int(l),int(m)])
        
        """save layer/ROI as base64 string"""
        #output = BytesIO() ##convert to machine readable string
        #output = cStringIO.StringIO() ##convert to machine readable string
        #PILbackground.save(output, format="PNG")
        #PILstring = base64.b64encode(output.getvalue())
        #PILstring = "data:image/png;base64," + PILstring.decode("utf-8")
        #with open(('output/%s-%s-L%s-base64.txt'%(image_name,layerName,i)), "w") as string_file:
        #    string_file.write(PILstring)    
        #append base
        #s1['roi-%s'%(i)] = s2

    """save table of ROI coordinates"""
    print('exporting %s ROI coordinates'%(s2['name']))
    headers=['id','x','y']
    coord_image_df = pd.DataFrame(coord_image, columns=headers)
    coord_image_df.to_csv('output/%s.csv'%(image_name), index=False)
    del coord_image_df

    
    """
    for each layer: draw contours
    """
    if contours:
        #----------------------------------------------------------------------
        #---------------------------------------------------------------------identify contours
        #https://docs.opencv.org/3.4.1/dd/d49/tutorial_py_contour_features.html
        #https://docs.opencv.org/2.4.13.7/modules/imgproc/doc/structural_\
        #analysis_and_shape_descriptors.html#drawcontours
        #https://loctv.wordpress.com/2017/02/17/learn-opencv3-python-contours-convex-contours-
        #bounding-rect-min-area-rect-min-enclosing-circle-approximate-bounding-polygon/

        #images
        l_raw = [] #list of raw images
        l_box = [] #list of convex hulls images
        l_hull = [] #list of bounding boxes images
        l_poly = [] #list of approx polygon images
        #areas
        l_box_a = [] #list of approx polygon areas
        l_hull_a = [] #list of approx polygon areas
        l_poly_a = [] #list of approx polygon areas
        
        print('for each layer')
        print('draw %s contour as %s'%(image_name, draw_type))
        for i in range(0, len(psd.layers)-1):
            #-------------get layer  
            #get metadata
            layer = psd.layers[i]
            meta_string = layer.name
            meta = pd.DataFrame(data=(item.split("=") for item in meta_string.split(";")),columns={'key','value'})
            s2 = pd.Series(meta['value'].tolist(),meta['key'].tolist())
                    
            ##load image directly from PSD
            image = layer.as_PIL()
            w, h = image.size
            image = np.array(image)
            #print(image.dtype)
            
            img = "" #setting blank img for unused contours
            #-------------find contour
            # threshold the image
            ## if any pixels that have value higher than 127, assign it to 255
            ##convert to bw for countour and store original
            (thr, thr_img) = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
            # find contour in image
            ## note: if you only want to retrieve the most external contour # use cv.RETR_EXTERNAL
            cnt_img, contours, hierarchy = cv2.findContours(thr_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            #-------------draw raw
            if draw_type=='raw':
                print('draw raw for layer %s'%(s2['name']))
                # for each contour
                for ind, itm in enumerate(contours):
                    img = cv2.drawContours(image=image,contours=[],contourIdx=-1,color=(0,0,255),thickness=cv2.FILLED)
                    pass
                l_raw.append(img)
                del img, image
        
            #-------------draw approximate polygon
            if draw_type=='polygon':
                # for each contour
                print('draw approximate polygon for layer %s'%(s2['name']))
                for ind, itm in enumerate(contours):
                    cnt = contours[ind]
                    epsilon = 0.01 * cv2.arcLength(cnt, True)
                    # get approx polygons
                    appx = cv2.approxPolyDP(cnt, epsilon, True)
                    appx.shape
                    # draw approx polygons
                    img = cv2.drawContours(image=image,contours=[appx],contourIdx=-1,color=(0,0,255),thickness=cv2.FILLED)
                l_poly.append(img)
                l_poly_a.append(appx)
                del img, image
              
            #-------------draw convex hull
            if draw_type=='hull':
                # for each contour
                print('draw convex hull for layer %s'%(s2['name']))
                for ind, itm in enumerate(contours):
                    cnt = contours[ind]
                    # get convex hull
                    hull = cv2.convexHull(itm)
                    # draw hull
                    img = cv2.drawContours(image=image,contours=[hull],contourIdx=-1,color=(0,0,255), thickness=cv2.FILLED)
                l_hull.append(img)
                l_hull_a.append(hull)
                del img, image
        
            #-------------draw bounding boxes   
            if draw_type=='box': 
                # for each contour
                print('draw bounding boxes for layer %s'%(s2['name']))
                for ind, itm in enumerate(contours):
                    cnt = contours[ind]
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    #draw contours
                    img = cv2.drawContours(image=image,contours=[box],contourIdx=0, color=(0,0,255), thickness=cv2.FILLED) 
                l_box.append(img)
                l_box_a.append(box)
                del img, image
    """
    for each layer/ROI: save images and contours
    """            
    #-----------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------saving contours
    #plt.gcf().clear() #clear plots
    
    #-------------save image
    if (draw_type=='image'):
        plt.imshow(psd.as_PIL())
        plt.savefig('output\\%s_all.png'%(image_name),dpi = 300)
    
    #when saving the contours below, only one drawContours function from above can be run
    #any other drawContours function will overlay on the others if multiple functions are run
    
    #-------------save raw
    if (contours==True) and (draw_type=='raw'):
        print('save contour')
        raw_all = l_raw[0] + l_raw[1] + l_raw[2]
        plt.imshow(cv2.cvtColor(raw_all, cv2.COLOR_BGR2RGB))
        plt.savefig('output\\%s_roi.png'%(image_name),dpi = 300)
    
    
    #-------------1.) save approximate polygon
    if (contours==True) and (draw_type=='polygon'):
        print('save approximate polygon')
        poly_all = l_poly[0] + l_poly[1] + l_poly[2]
        plt.imshow(cv2.cvtColor(poly_all, cv2.COLOR_BGR2RGB))
        plt.savefig('output\\%s_poly.png'%(image_name),dpi = 300)
        #save coordiantes
        a,b,c = l_poly_a[0][:,0,:], l_poly_a[1][:,0,:], l_poly_a[2][:,0,:]
        poly_area = np.concatenate((np.hstack([a, np.tile("ROI1", a.shape[0])[None].T]), 
                                    np.hstack([b, np.tile("ROI2", b.shape[0])[None].T]), 
                                    np.hstack([c, np.tile("ROI3", c.shape[0])[None].T])
                                  ))
        df = pd.DataFrame(poly_area)
        df.columns = ['x', 'y', 'ROI'] #rename
        df = df[['ROI','x','y']] #rearrange
        df[['x', 'y']] = df[['x', 'y']].astype(int) #convert to int
        df.to_csv("output/%s_poly.csv"%(image_name), index=False)
    
    
    #-------------2.) save convex hull
    if (contours==True) and (draw_type=='hull'):
        print('save convex hull')
        hull_all = l_hull[0] + l_hull[1] + l_hull[2]
        plt.imshow(cv2.cvtColor(hull_all, cv2.COLOR_BGR2RGB))
        plt.savefig('output\\%s_hull.png'%(image_name),dpi = 300)
        #save coordiantes
        a,b,c = l_hull_a[0][:,0,:], l_hull_a[1][:,0,:], l_hull_a[2][:,0,:]
        hull_area = np.concatenate((np.hstack([a, np.tile("ROI1", a.shape[0])[None].T]), 
                                    np.hstack([b, np.tile("ROI2", b.shape[0])[None].T]), 
                                    np.hstack([c, np.tile("ROI3", c.shape[0])[None].T])
                                  ))
        df = pd.DataFrame(hull_area)
        df.columns = ['x', 'y', 'ROI'] #rename
        df = df[['ROI','x','y']] #rearrange
        df[['x', 'y']] = df[['x', 'y']].astype(int) #convert to int
        df.to_csv("output/%s_hull.csv"%(image_name), index=False)
    
    #-------------3.) save bounding boxes
    if (contours==True) and (draw_type=='box'):
        print('save bounding boxes')
        box_all = l_box[0] + l_box[1] + l_box[2]
        plt.imshow(cv2.cvtColor(box_all, cv2.COLOR_BGR2RGB))
        plt.savefig('output\\%s_box.png'%(image_name),dpi = 300)
        #save coordiantes
        a,b,c = l_box_a[0], l_box_a[1], l_box_a[2]
        box_area = np.concatenate((np.hstack([a, np.tile("ROI1", a.shape[0])[None].T]), 
                                    np.hstack([b, np.tile("ROI2", b.shape[0])[None].T]), 
                                    np.hstack([c, np.tile("ROI3", c.shape[0])[None].T])
                                  ))
        df = pd.DataFrame(box_area)
        df.columns = ['x', 'y', 'ROI'] #rename
        df = df[['ROI','x','y']] #rearrange
        df[['x', 'y']] = df[['x', 'y']].astype(int) #convert to int
        df.to_csv("output/%s_box.csv"%(image_name), index=False)
    
    #plt.close()
    
    #draw image
    #cv2.imshow('image',img)
    #k = cv2.waitKey(0)
    
    #clear memory at end of iterable
    gc.collect()
    del i,l,m,r,g,b,a
    
   
"""save table of all ROI metadata"""
print('exporting all ROI metadata')
#import shellie/joceylin/kean table to add to dataframe
original = pd.read_excel('IAPS Image Ratings and ROI labels.xlsx')
original = original[['scene_img','meanvalence','meanarousal']]
original['scene_img'] = original['scene_img'].str.replace('.png','')

#build dataframe
headers=['id','file','ROI','resolution','valence',
         'human','animal','gender','behavior','body','object','age','other','descriptors']
meta_all_df = pd.DataFrame(meta_all, columns=headers)
#meta_all_df['file'] = meta_all_df['file'].str.replace('.png','')

#combine and export
df = pd.merge(meta_all_df, original, left_on='file', right_on='scene_img')
df = df[['id','file','ROI','resolution','valence','meanvalence','meanarousal',
         'human','animal','gender','behavior','body','object','age','other','descriptors']]
df.to_csv('output/metadata.csv', index=False)

#clear unused variables #locals() #globals() #vars()
#for name in dir():
    #if not name.startswith('_'):
        #del globals()[name]

#get size of variable in memory
#from sys import getsizeof
#l_size = []
#for var, obj in locals().items():
#    size = sys.getsizeof(obj) / 1000000 #convert to MB
#    l_size.append([var,size])
#size_df = pd.DataFrame(l_size, columns=['variable','filesize (MB)'])















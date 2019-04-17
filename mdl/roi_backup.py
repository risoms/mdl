#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----core
import os
import gc
from pathlib import Path

#----data
import cv2
import pandas as pd
import numpy as np

#----photoshop
import matplotlib.pyplot as plt
from psd_tools import PSDImage

#----libraries
library = ['opencv-python','psd_tools']

#!!!remove when creating function
source = os.getcwd() + "/dist/example/raw2/"
destination = os.getcwd() + "/dist/example/"
screensize = [1920,1080]
scale = 1.0
coordinates = None
shape = 'polygon' #polygon, hull, or box
dpi = 300
save_data = True
save_contour_image = True
save_raw_image = True
level = 'both'
kwargs = {}

#----todo
"""
- Draw image on top of presentation resolution (i.e. 1920x1080)
- use this as method for properly aligning image as roi (i.e. image is in center of screen)
"""

class roi():
    def __init__(source=None, destination=None, shape='box', save_data=True, save_contour_image=True, save_raw_image=True, level='both', **kwargs):
        """Create single subject trial bokeh plots.
        
        Parameters
        ----------
        source : :class:`str`
            Source of image files.
        destination : :class:`str`
            Folder to save data.
        shape : :class:`str`
            ROI bounds. Either polygon, hull, or box. Default is box.
        save_data : :class:`bool`
            Save coordinates. Default is True.
        save_raw_image : :class:`bool`
            Save images. Default is False.
        save_contour_image : :class:`bool`
            Save generated contours as images. Default is False.
        level : :class:`str`
            Either combine output for each roi (`stimulus`) or seperate by roi (`roi`) or both (`both`). Default is `both`.
        sep : :class:`str`
            (If `source` == `psd`) How is metadata delimited, options are: `;` `,` `|` `tab` or `space` Default is `;`.
        source : :class:`str`
            Metadata source, options are from a spreadsheet or a  Default is `psd`.
        screensize : :class:`list` of `int`
            Monitor size is being presented. Default is [1920, 1080].
        scale : :class:`int`
            If image is scaled during presentation, set scale. Default is 1.
        center : :class:`list` of `int`
           Center point of image, relative to screensize. Default is [960, 540].
        dpi : :class:`int` or `None`
            Quality of exported images, refers to 'dots per inch'. Default is 300 (if `save_image`=True).
        
        Attributes
        ----------
        psd: :class:`psd_tools.api.psd_image.PSDImage`
            The loaded image file. The file should include one layer for each region of interest.
        retval, threshold : :class:`numpy.ndarray`
            Returns from `cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)`. The function 
            applies fixed-level thresholding to a multiple-channel array. 
            `retval` provides an optimal threshold only if cv2.THRESH_OTSU is passed. `threshold` is an image after applying 
            a binary threshold (cv2.THRESH_BINARY) removing all greyscale pixels < 127. The output matches the same image 
            channel as the original image.
            See <https://docs.opencv.org/4.0.1/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57>`_ and
            `<https://www.learnopencv.com/opencv-threshold-python-cpp>`_
        contours, hierarchy : :class:`numpy.ndarray`
            Returns from `cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`. This function returns 
            contours from the provided binary image (threshold). This is used here for later shape detection. `contours` are 
            the detected contours, while hierarchy containing information about the image topology.
            See <https://docs.opencv.org/4.0.1/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e07>`_
        image_contours : :class:`numpy.ndarray`
            Returns from `cv2.drawContours(image=image,contours=[polygon],contourIdx=-1,color=(0,0,255), thickness=cv2.FILLED)`.
            This draws filled contours from the image.
            
        Examples
        --------
        
        """
        pass
#------------------------------------------------------------------------------------------------------------------init start
#----source
if source is None:
    source = os.getcwd() + "/dist/example/raw/"
#----destination
if destination is None:
    destination = os.getcwd() + "/dist/example/"

#----directory
directory = [x for x in Path(source).glob("*.psd") if x.is_file()]

#----output
for folder in ['output/stim/raw','output/stim/data','output/roi/raw', 'output/roi/contours','output/roi/data']:
    p = Path('%s/%s/'%(destination, folder))
    #check if path exists
    if not os.path.exists(p):
        os.makedirs(p)

#----config
config = {
    'contours':'',
    'shape':'',
    'save':{},
}
#----parameters
# delimiter
config['delimiter'] = ';' if 'delimiter' not in kwargs else kwargs['delimiter']
# screensize
config['screensize'] = [1920, 1080] if 'screensize' not in kwargs else kwargs['screensize']
# scale
config['scale'] = 1.0 if 'scale' not in kwargs else kwargs['scale']
#center
cx = config['screensize'][0]/2
cy = config['screensize'][1]/2
config['coordinates'] = [cx, cy] if 'coordinates' not in kwargs else kwargs['coordinates']
# shape
config['shape'] = shape if shape in ['polygon','hull','box'] else 'box'
# dpi
config['dpi'] = 300 if 'dpi' not in kwargs else kwargs['dpi']
# save csv
config['save']['data'] = True if save_data else False
# save contour images
config['save']['contours'] = True if save_contour_image else False
# save raw images
config['save']['raw'] = True if save_contour_image else False
# save level
config['save']['level'] = level
#----store
l_roi_bounds = [] #square bounds
l_roi_coord = [] #exact bounds
l_error = []
#--------------------------------------------------------------------------------------------------------------------init end

#----for each image
print('for each image')
for file in directory:
    #read image
    psd = PSDImage.open(file)    
    imagename = os.path.splitext(os.path.basename(file))[0]
    
    #----metadata
    s1 = pd.Series(name=imagename) #blank series
    s1['filename'] = '%s.png'%(imagename)
    s1['channels'] = psd.channels #read channels
    s1['resolution'] = [psd.width, psd.height] #length and width
    
    #save image
    #PSD = psd.topil()
    #white background
    #PSD.save('output/%s.png'%(filename))
    print('# file: %s'%(imagename))
    #------------------------------------------------------------------------------------------------------for each layer/ROI
    for layer in psd:
        #skip if layer is main image
        if Path(layer.name).stem == imagename:
            continue
        else:
            #----store lists
            l_contours = [] #list of contours
            l_polygon = [] #list of approx polygon areas
            
            print('## roi: %s:%s'%(imagename, layer.name))
            #----prepare metadata
            metadata = pd.DataFrame(data=(item.split("=") for item in layer.name.split(config['delimiter'])),columns=['key','value'])
            metadata.set_index('key', inplace=True)
            metadata.loc['name']['value'] = metadata.loc['name']['value'].replace("roi","")
            
            #----get constants
            roiname = metadata.loc['name']['value']
            shape = config['shape']
            
            #----load image directly from PSD
            image = np.array(layer.topil())
            #print(image.dtype)
            
            #----find contour
            try:
                # threshold the image
                ## note: if any pixels that have value higher than 127, assign it to 255. convert to bw for countour and store original
                retval, threshold = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
                
                #----find contour in image
                ## note: if you only want to retrieve the most external contour # use cv.RETR_EXTERNAL
                contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                #---if contours empty raise Exception
                if not bool(contours): 
                    _err = [imagename, roiname, 'Not able to identify contours']
                    l_error.append(_err)
                    raise Exception('%s; %s; %s'%(_err[0],_err[1],_err[2]))
                
            except Exception as error:
                print(error)
                continue

            #------------------------------------------------------------------------for each layer: save images and contours
            #when saving the contours below, only one drawContours function from above can be run
            #any other drawContours function will overlay on the others if multiple functions are run
            #----approximate polygon
            if shape=='polygon':
                print('save approximate polygon')
                # for each contour
                for ind, itm in enumerate(contours):
                    cnt = contours[ind]
                    epsilon = 0.01 * cv2.arcLength(cnt, True)
                    # get approx polygons
                    polygon = cv2.approxPolyDP(cnt, epsilon, True)
                    # draw approx polygons
                    roi_contours = cv2.drawContours(image=image, contours=[polygon], contourIdx=-1 ,color=(0,0,255), thickness=cv2.FILLED)
                # combine to image
                l_contours.append(roi_contours)
                l_polygon.append(polygon)
                coordinates = l_polygon[0][:,0,:]
            
            #----bounding boxes
            elif shape=='box':
                print('save bounding boxes')
                # for each contour
                for ind, itm in enumerate(contours):
                    cnt = contours[ind]
                    rect = cv2.minAreaRect(cnt)
                    polygon = cv2.boxPoints(rect)
                    polygon = np.int0(polygon)
                    #draw contours
                    roi_contours = cv2.drawContours(image=image, contours=[polygon], contourIdx=0, color=(0,0,255), thickness=cv2.FILLED)
                # combine to image
                l_contours.append(roi_contours)
                l_polygon.append(polygon)
                coordinates = l_polygon[0]
            
            #----convex hull
            elif shape=='hull':
                print('save hull')
                # for each contour
                for ind, itm in enumerate(contours):
                    cnt = contours[ind]
                    # get convex hull
                    polygon = cv2.convexHull(itm)
                    # draw hull
                    roi_contours = cv2.drawContours(image=image,contours=[polygon],contourIdx=-1,color=(0,0,255), thickness=cv2.FILLED)
                # combine to image
                l_contours.append(roi_contours)
                l_polygon.append(polygon)
                coordinates = l_polygon[0][:,0,:]
                
            else:
                pass
                #!!!Put after creating as function return print('Please select either polygon, box, or hull shape')
            
            #----store raw data and polygons to list
            # flatten all raw data
            flat = sum(l_contours)
                
            #----store bounds as df
            bounds = pd.DataFrame(coordinates)
            bounds.columns = ['x', 'y'] #rename
            # add image, roi, and shape
            bounds['image'] = imagename
            bounds['ROI'] = roiname
            bounds['shape'] = shape
            # clean-up
            bounds = bounds[['image','ROI','shape','x','y']] #sort
            bounds[['x', 'y']] = bounds[['x', 'y']].astype(int) #convert to int
            # append to list of df
            l_roi_bounds.append(bounds)

            #----save image:roi level image bounds and coordinates
            if ((config['save']['level'] == 'both') or (config['save']['level'] == 'roi')):
                #----save roi raw image
                if config['save']['raw']:
                    #convert image from pil [nparray] > matplotlib 
                    plt.imshow(np.asarray(layer.topil()))
                    plt.savefig('%s/output/roi/raw/%s_%s.png'%(destination, imagename, roiname), dpi=dpi)
                    plt.close()
                #----save roi contour image
                if config['save']['contours']:
                    plt.imshow(cv2.cvtColor(flat, cv2.COLOR_BGR2RGB))
                    plt.savefig('%s/output/roi/contours/%s_%s_%s.png'%(destination, imagename, roiname, shape), dpi=dpi)
                    plt.close()
                #----save roi df
                if config['save']['data']:
                    #bounds
                    bounds.to_csv("%s/output/roi/data/%s_%s_bounds.csv"%(destination, imagename, roiname), index=False)
                    #coordinates
                    #coord.to_csv("%s/output/roi/data/%s_%s_bounds.csv"%(destination, imagename, roiname), index=False)
        
        #-------------save combined roi data
        if ((config['save']['level'] == 'both') or (config['save']['level'] == 'stimulus')):
            #----save all roi image
            if config['save']['raw']:
                plt.imshow(psd.topil())
                plt.savefig('%s/output/stim/raw/%s.png'%(destination, imagename), dpi=dpi)
                plt.close()
            
            #----save data
            #bounds 
            df = pd.DataFrame(l_roi_bounds)
            df.to_csv("%s/output/stim/data/%s.csv"%(destination, imagename), index=False)
            #coord
            df = pd.DataFrame(l_roi_coord)
            df.to_csv("%s/output/stim/data/%s_coord.csv"%(destination, imagename), index=False)

        #plt.gcf().clear() #clear plots
        #plt.close()
        
        #draw image
        #cv2.imshow('image',img)
        #k = cv2.waitKey(0)
        
        #clear memory at end of iterable
        gc.collect()
            
        #----save table of ROI coordinates
        # print('exporting %s ROI coordinates'%(s2['name']))
        # # create df
        # headers=['id','x','y']
        # coord_image_df = pd.DataFrame(coord_image, columns=headers)
        # coord_image_df.to_csv('%s/%s.csv'%(output['output'], filename), index=False)
        # del coord_image_df

#----error log
if bool(l_error):
    _filename = Path('%s/error.csv'%(destination))
    print("Errors found. See log %s"%(_filename))
    df = pd.DataFrame(l_error, columns=['image','roi','message'])
    df.to_csv(_filename, index=False)



#----test
# drawing image
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('image',img)



##import shellie/joceylin/kean table to add to dataframe
#original = pd.read_excel('dist/ratings_and_labels.xlsx')
#original = original[['scene_img','meanvalence','meanarousal']]
#original['scene_img'] = original['scene_img'].str.replace('.png','')
#
##build dataframe
#headers=['id','file','ROI','resolution','valence',
#         'human','animal','gender','behavior','body','object','age','other','descriptors']
#meta_all_df = pd.DataFrame(meta_all, columns=headers)
##meta_all_df['file'] = meta_all_df['file'].str.replace('.png','')
#
##combine and export
#df = pd.merge(meta_all_df, original, left_on='file', right_on='scene_img')
#df = df[['id','file','ROI','resolution','valence','meanvalence','meanarousal',
#         'human','animal','gender','behavior','body','object','age','other','descriptors']]
#df.to_csv('%s/metadata.csv'%(destination + 'metadata'), index=False)

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















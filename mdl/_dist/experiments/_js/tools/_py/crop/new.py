# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:53:01 2016

@author: sr38553
"""
#make pofa and iaps faces 768,768


from PIL import Image, ImageOps, ImageDraw, ImageEnhance, ImageChops
import os

try: #use _file_ in most cases
    dir = os.path.dirname(__file__)
except NameError:  #except when running python from py2exe script
    import sys
    dir = os.path.dirname(sys.argv[0])

##trim border from images in iapsb_old folder, and add new border
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

#setting directories
#dir = os.path.dirname(__file__)
#Pictures of Facial Affect
pofa_old = os.path.join(dir, 'pofa_old')
pofa_new = os.path.join(dir, 'pofa_new')

#International Affective Picture System
##images with border
iapsb_old = os.path.join(dir, 'iapsb_old')
iapsb_new = os.path.join(dir, 'iapsb_new')
##images without border
iaps_old = os.path.join(dir, 'iaps_old')
iaps_new = os.path.join(dir, 'iaps_new')


#Pictures of Facial Affect
#add border
for img in os.listdir(pofa_old):
    im = Image.open(os.path.join(pofa_old, img))
    img_w, img_h = im.size
    
    #add border 
    background = Image.new("RGB", (768,768), (110,110,110))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
    

    #paste image to background    
    background.paste(im, offset)
    
    #save image
    fileName, fileExtension=os.path.splitext(img)
    d=(os.path.join(pofa_new, fileName)+'.jpg')
    background.save(d, "JPEG")
    
#International Pictures of Facial Affect faces
##note: some faces already have black border - remove to keep images same size
for img in os.listdir(iapsb_old):
    im = Image.open(os.path.join(iapsb_old, img))
    #remove border
    im = trim(im)
    basewidth = 768
    
    #resize
    if float(im.size[0]) / float(im.size[1]) > 1:
        wpercent = (basewidth/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        im = im.resize((basewidth, hsize), Image.ANTIALIAS)
        
    else:
        hpercent = (basewidth/float(im.size[1]))
        wsize = int((float(im.size[0])*float(hpercent)))
        im = im.resize((wsize, basewidth), Image.ANTIALIAS)
    
    #add border
    img_w, img_h = im.size
    background = Image.new("RGB", (768,768), (110,110,110))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)

    #paste image to background    
    background.paste(im, offset)
    
    #save image
    fileName, fileExtension=os.path.splitext(img)
    d=(os.path.join(iapsb_new, fileName)+'.jpg')
    background.save(d, "JPEG")

##add border to rest of images
for img in os.listdir(iaps_old):
    im = Image.open(os.path.join(iaps_old, img))
    
    #resize
    basewidth = 768
    wpercent = (basewidth/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im = im.resize((basewidth, hsize), Image.ANTIALIAS)
    
    #add border 
    img_w, img_h = im.size
    background = Image.new("RGB", (768,768), (110,110,110))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)

    #paste image to background    
    background.paste(im, offset)
    
    #save image
    fileName, fileExtension=os.path.splitext(img)
    d=(os.path.join(iaps_new, fileName)+'.jpg')
    background.save(d, "JPEG")
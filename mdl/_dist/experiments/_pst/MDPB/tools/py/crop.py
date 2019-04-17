from PIL import Image, ImageDraw, ImageOps
import glob
import os

#built from the following examples
#http://stackoverflow.com/questions/4789894/python-pil-how-to-draw-an-ellipse-in-the-middle-of-an-image
#http://pillow.readthedocs.org/en/3.0.x/reference/Image.html?


try: #use _file_ in most cases
    dir = os.path.dirname(__file__)
except NameError:  #except when running python from py2exe script
    import sys
    dir = os.path.dirname(sys.argv[0])

#setting directories
#dir = os.path.dirname(__file__)
original = os.path.join(dir, 'old')
new = os.path.join(dir, 'crop')


#loop through all found images
for img in os.listdir(original):
    #open the image                           
    im = Image.open(os.path.join(original, img))

    #resize image, preserving aspect ratio
    img_w, img_h = im.size
    basewidth = img_w
    #wpercent = (basewidth / float(im.size[0]))
    #hsize = int((float(im.size[1]) * float(wpercent)))
    #im = im.resize((basewidth, hsize), Image.ANTIALIAS)

    #multiplier for anti-alias
    multi = 20
    
    #define image size
    w,h = (310*multi),(410*multi)

    #size of ellipse x and y-axis boundaries
    eW, eH = (310*multi), (410*multi)

    #setting elipse mask
    bound_box = (w/2 - eW/2, h/2 - eH/2, w/2 + eW/2, h/2 + eH/2) #boundary, centered
    mask = Image.new('L', (w,h), 0) #new blank image
    draw = ImageDraw.Draw(mask)
    draw.ellipse((bound_box), fill=255)

    #resize mask and put as alpha
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    im = im.convert('RGBA')

    #anti aliasing
    im.thumbnail([img_w, img_h], Image.ANTIALIAS)
    
    #add border
    background = Image.new("RGBA", (img_w, img_h), (192,192,192))
    alpha_composite = Image.alpha_composite(background, im)
    #alpha_composite.save('foo.jpg', 'JPEG', quality=80)
    
    #save image
    fileName, fileExtension=os.path.splitext(img)
    d=(os.path.join(new, fileName)+'.png')
    alpha_composite.save(d, "PNG")
   


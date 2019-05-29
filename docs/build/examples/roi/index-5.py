import sys
# add source
sys.path.insert(0, os.path.abspath('./sphinxext'))
sys.path.append('/Users/mdl-admin/Desktop/mdl')
# import package
import imhr

# create image
import matplotlib.pyplot as plt
import matplotlib.image as image
from pathlib import Path
# path
path = '%s/dist/roi/output/img/bounds/'%(Path(imhr.__file__).parent)
# draw plot
#plt.figure(figsize=(20,6), dpi=400, facecolor='#ffffff')
fig, (axes) = plt.subplots(1, 4, sharey=True)
# names
shape = 'circle'
filenames = ['2550_%s.png'%(shape),'2691_%s.png'%(shape),'4640_%s.png'%(shape),'9421_%s.png'%(shape)]
# draw and save
for idx, itm in enumerate(zip(axes, filenames)):
    ax, file, = itm
    ## load roi
    im = image.imread('%s/%s'%(path, file))
    ax.imshow(im)
    ax.grid(True)
    ax.set_facecolor('#f9f9f9')
    # labels
    if idx == 0: ax.set_ylabel('Screen Y (pixels)', fontsize=8)
    ax.set_xlabel('Screen X (pixels)', fontsize=8)
    ax.tick_params(labelsize=6, width=1, length=4)
# save
#plt.tight_layout()
plt.subplots_adjust(wspace=0.1)
plt.show()
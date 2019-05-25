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
path = '%s/dist/roi/example/'%(Path(imhr.__file__).parent)
# draw plot
#plt.figure(figsize=(20,6), dpi=400, facecolor='#ffffff')
fig, (axes) = plt.subplots(1, 2, sharey=True)
# names
files = ['photoshop_psd.png','photoshop_dicom.png']
for idx, itm in enumerate(zip(axes, files)):
    ax, file, = itm
    ## load roi
    im = image.imread('%s/%s'%(path, file))
    ax.imshow(im)
    # labels
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis('off')
# save
plt.tight_layout()
plt.subplots_adjust(wspace=0.1)
## remove frame
#plt.gca().axes.get_yaxis().set_visible(False)
#plt.gca().axes.get_xaxis().set_visible(False)
plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='off')
plt.box(False)
plt.show()
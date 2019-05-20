import matplotlib.pyplot as plt
import matplotlib.image as image
from pathlib import Path
# path
#path = '%s/imhr/dist/roi/output/img/'%(Path.cwd().parent.parent.parent)
path = Path(imhr.__file__[0])
# draw plot
plt.rcParams['axes.facecolor'] = '6e6e6e'
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(20,15), dpi=400)
size = fig.get_size_inches()*fig.dpi
## roi
im = image.imread('%s/preprocessed/AM_201.png'%(path))
ax1.imshow(im)
ax1.axis('off')
ax1.grid(True)
ax1.set_title('Region of Interest', fontsize=18)
ax1.set_ylabel('Screen Y (pixels)', fontsize=18)
ax1.set_xlabel('Screen X (pixels)', fontsize=18)
## bounds
im = image.imread('%s/bounds/AM_201.png'%(path))
ax2.imshow(im)
ax2.axis('off')
ax2.grid(True)
ax2.set_title('Rectangular Bounds', fontsize=18)
ax1.set_xlabel('Screen X (pixels)', fontsize=18)
## title
plt.title('Raw and Processed Images', fontsize=18)
plt.text(0.5, 0.5, 'Raw and Processed Images', ha='center', va='bottom', fontsize=20)
## show
plt.tight_layout()
plt.show()
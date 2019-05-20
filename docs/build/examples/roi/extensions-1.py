from pylab import *  
from pathlib import Path
import matplotlib.pyplot as plt  
import matplotlib.image as image
%matplotlib inline
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12,6))  
path = Path('%s/imhr/dist/roi/output/img/'%(Path.cwd()))  
#roi  
im = image.imread('%s/preprocessed/AM_201.png'%(path))  
ax1.imshow(im)  
ax1.axis('off')  
ax1.set_title('Region of Interest')  
#contour  
im = image.imread('%s/bounds/AM_201.png'%(path))  
ax2.imshow(im)  
ax2.axis('off')  
ax2.set_title('Rectangular Bounds')  
#show 
plt.tight_layout()  
show()  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import matplotlib.image as image
from pathlib import Path
# add source
sys.path.insert(0, os.path.abspath('./sphinxext'))
sys.path.append('/Users/mdl-admin/Desktop/mdl')
# import package
import imhr
# path
path = '%s/dist/roi/example/'%(Path(imhr.__file__).parent)
# draw plot
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(24,8), dpi=400)
## roi
im = image.imread('%s/2550_pre.png'%(path))
ax1.imshow(im)
ax1.grid(True)
ax1.set_title('Region of Interest', fontsize=16)
ax1.set_ylabel('Screen Y (pixels)', fontsize=16)
ax1.set_xlabel('Screen X (pixels)', fontsize=16)
## bounds
im = image.imread('%s/2550_roi.png'%(path))
ax2.imshow(im)
ax2.grid(True)
ax2.set_title('Rectangular Bounds', fontsize=16)
ax2.set_ylabel('Screen Y (pixels)', fontsize=16)
ax2.set_xlabel('Screen X (pixels)', fontsize=16)
## show
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.tight_layout()
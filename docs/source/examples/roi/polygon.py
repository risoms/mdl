#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# add source
sys.path.insert(0, os.path.abspath('./sphinxext'))
sys.path.append('/Users/mdl-admin/Desktop/mdl')
# import package
import imhr

import matplotlib.pyplot as plt
import matplotlib.image as image
from pathlib import Path
# path
path = '%s/dist/roi/example/'%(Path(imhr.__file__).parent)
# draw plot
fig, (ax) = plt.subplots(1, 1, sharey=True, figsize=(24,8), dpi=400)
## roi
im = image.imread('%s/2550_polygon.png'%(path))
ax.imshow(im)
ax.grid(True)
ax.set_title('Region of Interest', fontsize=16)
ax.set_ylabel('Screen Y (pixels)', fontsize=16)
ax.set_xlabel('Screen X (pixels)', fontsize=16)
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.tight_layout()
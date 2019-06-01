# create image
import matplotlib.pyplot as plt
import matplotlib.image as image
from pathlib import Path
# path
# draw plot
#plt.figure(figsize=(20,6), dpi=400, facecolor='#ffffff')
fig, ax = plt.subplots()
## load roi
im = image.imread('/Users/mdl-admin/Desktop/mdl/docs/source/examples/eyetracking/demo/img/stimulus.png')
ax.imshow(im)
# labels
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
# save
plt.tight_layout()
plt.subplots_adjust(wspace=0.1)
## remove frame
ax.axis('off')
#plt.gca().axes.get_yaxis().set_visible(False)
#plt.gca().axes.get_xaxis().set_visible(False)
plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='off')
plt.box(False)
plt.show()
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale
from skimage.transform import iradon
from skimage.transform import iradon_sart

image = imread("test_phantom_3.png", as_grey=True)
image = rescale(image, scale=0.4, mode='reflect')

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
# fig, axes = plt.subplots(2, 2, figsize=(8, 8.5), sharex=True, sharey=True)
fig, axes = plt.subplots(1, 2)
ax = axes.ravel()

ax[0].set_title("Phantom")
# ax[0].imshow(image, cmap=plt.cm.Greys_r)
ax[0].imshow(image, cmap='Greys_r')
ax[0].set_xlabel('Sudut Proyeksi (deg)')
ax[0].set_ylabel('Posisi (pixel)')

theta = np.linspace(0., 180., max(image.shape), endpoint=False)
sinogram = radon(image, theta=theta, circle=False)
# print(sinogram.shape)
# print(theta)
# print(sinogram[10])
ax[1].set_title("Sinogram")
ax[1].set_xlabel("Sudut (deg)")
ax[1].set_ylabel("Posisi (pixels)")
ax[1].imshow(sinogram,
           extent=(0, 180, 0, sinogram.shape[0]), aspect='auto', cmap='Greys_r')

# fig.tight_layout()

# reconstruction_fbp = iradon(sinogram, theta=theta, circle=False)
# reconstruction_fbp = iradon_sart(sinogram, theta=theta, relaxation=0.75)
reconstruction_fbp = iradon_sart(sinogram, theta=theta)
# error = reconstruction_fbp - image
# print('FBP rms reconstruction error: %.3g' % np.sqrt(np.mean(error**2)))

# imkwargs = dict(vmin=-0.2, vmax=0.2)

# ax[2].set_title("Rekonstruksi Citra\nFiltered Backprojection")
# ax[0].set_title("Rekonstruksi Citra\nbackproj")
# ax[0].imshow(reconstruction_fbp, cmap='Greys_r')
# ax[3].set_title("Reconstruction error\nFiltered back projection")
# ax[3].imshow(reconstruction_fbp - image, cmap=plt.cm.Greys_r, **imkwargs)
plt.show()

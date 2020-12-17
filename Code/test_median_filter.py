import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

im = np.zeros((20, 20))
im[6:-6, 4] = 1
im[6:-6, -5] = 1
im[4, 6:-6] = 1
im[-5, 6:-6] = 1
im[5:-5, 5:-5] = 1
# im[9:-9, 9:-9] = 1
im = ndimage.distance_transform_bf(im)
im_noise = im + 0.2*np.random.randn(*im.shape)

im_med = ndimage.median_filter(im_noise, 3)

plt.figure(figsize=(16, 5))

plt.subplot(141)
# plt.imshow(im, interpolation='nearest')
# plt.axis('off')
# plt.title('Citra Orisinil', fontsize=20)
# plt.subplot(142)
plt.imshow(im_noise, interpolation='nearest', vmin=0, vmax=5)
# plt.axis('off')
plt.title('Citra+Derau \nGaussian(0,2)', fontsize=20)
plt.subplot(143)
plt.imshow(im_med, interpolation='nearest', vmin=0, vmax=5)
# plt.axis('off')
plt.title('Setelah ditapis Median', fontsize=20)
# plt.subplot(144)
# plt.imshow(np.abs(im - im_med), cmap=plt.cm.hot, interpolation='nearest')
# plt.axis('off')
# plt.title('Error', fontsize=20)


# plt.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9, bottom=0, left=0,
#                     right=1)

plt.show()

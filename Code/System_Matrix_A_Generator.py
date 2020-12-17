import numpy as np
from skimage.transform import radon
from scipy.sparse import lil_matrix
from matplotlib import pyplot as plt

# %j = 3;
# %n = 2^(2*j);
j = 9
n = 81
#
# %Nang = 33;
Nang = 36;
angles = np.arange(0,Nang)*360/Nang;

#
# %tmp = radon(zeros(2^j, 2^j), angles);
tmp = radon(np.zeros((j, j)), angles, circle=True);
k = len(tmp.flatten())
#
# A = lil_matrix((k, n))
A = np.zeros((k, n))
# print(A[:,0].shape)
# plt.spy(A)
# plt.show()

for iii in range(0,j*j):
   unitvec = np.zeros((j, j)).flatten()
   unitvec[iii] = 1;

   tmp = radon(unitvec.reshape(j,j), angles, circle=True);
   # print('itaration ke-', iii, ' size=', tmp.flatten().shape)
   # A[:,iii] = lil_matrix(tmp.flatten()).todense().transpose()
   A[:,iii] = tmp.flatten().transpose()

#
# figure(1)
# clf
# spy(A)
# A
# plt.imshow(A.todense())
plt.spy(A.transpose(), markersize=0.5)
plt.show()
print(A)
# print(A[:,0])

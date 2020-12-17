import csv
import os
import sys
import numpy as np
import matplotlib.pylab as plt
from skimage.transform import iradon
from skimage.transform import iradon_sart


t_Argv = sys.argv
t_FileDir = t_Argv[1]
# t_ListFiles = os.listdir(t_FileDir)
t_SParameter = {}
# t_Measurements = np.zeros(209).reshape(11,19)
t_Measurements = np.zeros(399).reshape(21,19)

# with open(t_Argv[1], 'r') as t_File:
#     t_DataReader = csv.reader(t_File)
#     next(t_DataReader)
#
#     t_Translasi = 0
#     for t_Baris in t_DataReader:
#         print(t_Translasi)
#         t_Data = t_Baris[0].split(';')
#         # print(t_Data)
#         for i in range(1, len(t_Data)):
#             # print(t_Data[i])
#             t_Measurements[t_Translasi, i-1] = float(t_Data[i])
#         # print('test')
#         t_Translasi += 1

t_Measurements[0,:] = 1
t_Measurements[10,:] = 1
t_Measurements[20,:] = 1

#////////////////////////////////////////////////
print(t_Measurements)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
# ax1.imshow(t_Array, cmap=plt.cm.Greys_r, extent=(0, 36, 0, 1), aspect='auto')
ax1.imshow(t_Measurements, extent=(0, 18, 0, 10), aspect='auto')
ax1.set_title("Sinogram/Measurement data")

theta = np.linspace(1, 18, 19, endpoint=True)

reconstruction_fbp = iradon(t_Measurements, filter="ramp" ,interpolation="linear", circle=False, output_size=36)
# t_Relaxation = 0.01
# reconstruction_fbp = iradon_sart(t_Measurements, relaxation=t_Relaxation)
# for i in range(10):
#     reconstruction_fbp = iradon_sart(t_Measurements, image=reconstruction_fbp, relaxation=t_Relaxation)

# ax2.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
# ax2.imshow(reconstruction_fbp, extent=(0, 18, 0, 18))
ax2.imshow(reconstruction_fbp)
ax2.set_title("Reconstruction image")
ax2.set_xlabel("Projection angle (deg)")
# ax2.set_ylabel("Projection position (pixels)")
fig.tight_layout()
plt.show()

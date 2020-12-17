import csv
import os
import sys
import numpy as np
import matplotlib.pylab as plt
from skimage.transform import iradon
from skimage.transform import iradon_sart


t_Argv = sys.argv
t_FileDir = t_Argv[1]
t_ListFiles = os.listdir(t_FileDir)
t_SParameter = {}

# List nama file di directory
for t_CsvFileName in t_ListFiles:
    t_CsvFileNameSplited = t_CsvFileName.split('_')
    print(t_CsvFileNameSplited)

    # Filter nilai S-Parameter dan ambil yang real value
    if t_CsvFileNameSplited[2].upper() == 'S21' and t_CsvFileNameSplited[3] == 're.csv':
        # Buka setiap file
        print('\nOpening file : ' + t_CsvFileName)
        with open(t_FileDir + '\\' + t_CsvFileName, 'r') as t_File:
            t_DataReader = csv.reader(t_File)
            next(t_DataReader)  # Skip header

            for t_Baris in t_DataReader:
                print(t_Baris[0])
                t_FloatData = float(t_Baris[1])

                # Filter frequency
                if t_Baris[0] == '1.5':
                    t_SParameter.update({int(t_CsvFileNameSplited[0]) : t_FloatData})
                    print('Projection angle:', t_CsvFileNameSplited[0], 'Frequency:', t_Baris[0], ' Ghz', t_FloatData, ' vs ', t_FloatData * 10)

# print(sorted(t_SParameter.items()))
print('Panjang data = ', len(t_SParameter))

t_X, t_Y = zip(*sorted(t_SParameter.items()))

#t_X = np.linspace(0., 1., 10, endpoint=False)
# t_Mat = np.mat([t_X, t_Y])
#print(t_Mat.shape)
# print(t_SParameter.shape)
# t_TestArray = np.zeros(10*len(t_SParameter)).reshape(10, len(t_SParameter))
# t_Array = np.array(list(t_SParameter.values())).reshape(1,len(t_SParameter))
# t_TestArray[4:6] = t_Array
# print(t_Array.shape)
# print(t_Array)
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
# ax1.imshow(t_Array, cmap=plt.cm.Greys_r, extent=(0, 36, 0, 1), aspect='auto')
# ax1.imshow(t_TestArray, extent=(0, 36, 0, 10), aspect='auto')
# ax1.set_title("Sinogram/Measurement data")
# print(t_X)
# print(t_Y)
plt.plot(t_X, t_Y)
# theta = np.linspace(0., 35., max(t_TestArray.shape), endpoint=False)
# reconstruction_fbp = iradon(t_Array, theta=theta, circle=True)
# reconstruction_fbp = iradon_sart(t_TestArray, theta=theta)
# for i in range(10):
    # reconstruction_fbp = iradon_sart(t_TestArray, theta=theta, image=reconstruction_fbp)

# ax2.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
# ax2.imshow(reconstruction_fbp, extent=(0, 36, 0, 36))
# ax2.set_title("Reconstruction image")
# ax2.set_xlabel("Projection angle (deg)")
# ax2.set_ylabel("Projection position (pixels)")
# fig.tight_layout()
plt.show()

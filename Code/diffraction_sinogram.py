import csv
import os
import sys
import numpy as np
import matplotlib.pylab as plt
from skimage.transform import iradon
from skimage.transform import iradon_sart
import odtbrain as odt


t_Argv = sys.argv
t_FileDir = t_Argv[1]
t_ListFiles = os.listdir(t_FileDir)
t_SParameter = {}
t_Measurements = np.zeros(209).reshape(11,19)

# List nama file di directory
for t_CsvFileName in t_ListFiles:
    t_CsvFileNameSplited = t_CsvFileName.split('_')
    #print(t_CsvFileNameSplited)

    # Filter nilai S-Parameter dan ambil yang real value
    if t_CsvFileNameSplited[2].upper() == 'S21' and t_CsvFileNameSplited[3] == 're.csv':
        # Buka setiap file
        print('\nOpening file : ' + t_CsvFileName)
        with open(t_FileDir + '\\' + t_CsvFileName, 'r') as t_File:
            t_DataReader = csv.reader(t_File)
            next(t_DataReader)  # Skip header

            for t_Baris in t_DataReader:
                # print(t_Baris)
                t_FloatData = float(t_Baris[1])

                # Filter frequency
                if t_Baris[0] == '1.5':
                    # print(t_CsvFileNameSplited[0], '\t', t_CsvFileNameSplited[1], '\t', t_FloatData)
                    t_Measurements[int(t_CsvFileNameSplited[0])-1, int(int(t_CsvFileNameSplited[1])/10)] = t_FloatData
                    # t_SParameter.update({int(t_CsvFileNameSplited[0]) : t_FloatData})
                    # print('Projection angle:', t_CsvFileNameSplited[0], 'Frequency:', t_Baris[0], ' Ghz', t_FloatData, ' vs ', t_FloatData * 10)

print(t_Measurements)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 4.5))
# ax1.imshow(t_Array, cmap=plt.cm.Greys_r, extent=(0, 36, 0, 1), aspect='auto')
ax1.imshow(t_Measurements, extent=(0, 18, 0, 10), aspect='auto')
ax1.set_title("Sinogram/Measurement data")

theta = np.linspace(1, 18, 19, endpoint=True)

reconstruction_fbp = iradon(t_Measurements, filter="ramp" ,interpolation="linear", circle=False, output_size=18)
# t_Relaxation = 0.01
# reconstruction_fbp = iradon_sart(t_Measurements, relaxation=t_Relaxation)
# for i in range(10):
#     reconstruction_fbp = iradon_sart(t_Measurements, image=reconstruction_fbp, relaxation=t_Relaxation)

# ax2.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
# ax2.imshow(reconstruction_fbp, extent=(0, 18, 0, 18))

## ----------- Reconstruction by ODTBrain --------------- ##
t_Radon = odt.opt_to_ri(t_Measurements, 300, 20)
print(t_Radon)
ax3.imshow(t_Radon)
ax3.set_title("Radon by ODTBrain")
## ------------------------------------------------------ ##


ax2.imshow(reconstruction_fbp)
ax2.set_title("Reconstruction image")
ax2.set_xlabel("Projection angle (deg)")
# ax2.set_ylabel("Projection position (pixels)")
fig.tight_layout()
plt.show()

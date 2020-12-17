import csv
import os
import sys
import numpy as np
import matplotlib.pylab as plt
from skimage.transform import iradon
from skimage.transform import iradon_sart
import odtbrain as odt
from scipy import interpolate
from scipy import ndimage


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

## Interpolasi
t_Interp = 50
t_XArange = np.arange(t_Measurements.shape[0])
t_Xinter = np.linspace(0, t_Measurements.shape[0]-1, t_Interp)
t_Yinter = np.linspace(0, t_Measurements.shape[1]-1, 360)
t_InterpolatedMeasurements = np.zeros((t_Interp,360))
t_InterpolatedPosition = np.zeros((t_Interp,t_Measurements.shape[1]))
print('Xarange=', len(t_XArange), ' vs Xinter=', len(t_Xinter), ' vs Meas=', len(t_Measurements[1,:]))
for i in range(t_Measurements.shape[1]):
    print(i)
    t_InterpObject = interpolate.interp1d(t_XArange, t_Measurements[:,i], kind="cubic")
    t_InterpolatedPosition[:,i] = t_InterpObject(t_Xinter)

t_YArange = np.arange(t_Measurements.shape[1])
for s in range(t_InterpolatedPosition.shape[0]):
    t_YObjInterpolasi = interpolate.interp1d(t_YArange, t_InterpolatedPosition[s], kind="cubic")
    t_InterpolatedMeasurements[s] = t_YObjInterpolasi(t_Yinter)


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 4.5))
# ax1.imshow(t_Array, cmap=plt.cm.Greys_r, extent=(0, 36, 0, 1), aspect='auto')
# ax1.imshow(t_Measurements, extent=(0, 18, 0, 10), aspect='auto')
# ax1.imshow(t_InterpolatedMeasurements, extent=(0, 18, 0, 10), aspect='auto')
ax1.imshow(t_InterpolatedMeasurements, aspect='auto')
ax1.set_title("Interpolasi Sinogram")

theta = np.linspace(0, 180, t_InterpolatedMeasurements.shape[1], endpoint=False)

# reconstruction_fbp = iradon(t_Measurements, filter="ramp" ,interpolation="linear", circle=False, output_size=18)
# reconstruction_fbp = iradon(t_InterpolatedMeasurements, filter="ramp" ,interpolation="linear", circle=False, output_size=18)
reconstruction_fbp = iradon(t_InterpolatedMeasurements, theta=theta, filter="ramp" ,interpolation="linear", circle=False)
# t_Relaxation = 0.01
# reconstruction_fbp = iradon_sart(t_Measurements, relaxation=t_Relaxation)
# reconstruction_fbp = iradon_sart(t_InterpolatedMeasurements, relaxation=0.1)
# for i in range(10):
#     reconstruction_fbp = iradon_sart(t_Measurements, image=reconstruction_fbp, relaxation=t_Relaxation)

# ax2.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
# ax2.imshow(reconstruction_fbp, extent=(0, 18, 0, 18))

## ----------- Reconstruction by ODTBrain --------------- ##
t_Radon = odt.opt_to_ri(t_Measurements, 300, 20)
print(t_Radon)
# ax3.imshow(t_Radon)
ax3.imshow(t_Measurements)
ax3.set_title("Sinogram")
## ------------------------------------------------------ ##


ax2.imshow(ndimage.median_filter(reconstruction_fbp, size=5))
ax2.set_title("Citra Rekonstruksi")
# ax2.set_xlabel("Sudut (deg)")
# ax2.set_ylabel("Projection position (pixels)")
fig.tight_layout()
plt.show()

import csv
import sys
import numpy as np
import os
from matplotlib import pyplot as plt
import odtbrain as odt

t_Argv = sys.argv
t_FileDir = t_Argv[1]
print(t_FileDir)
t_ListFiles = os.listdir(t_FileDir)

# t_SensorPos = 250
# t_SensorPos = 250
# t_SudutProj = 361
t_SensorPos = int(t_Argv[2])
t_SudutProj = int(t_Argv[3])
sino = np.zeros(t_SudutProj*t_SensorPos, dtype=np.complex).reshape(t_SudutProj, t_SensorPos)
# sino = np.zeros(t_SudutProj*t_SensorPos).reshape(t_SudutProj, t_SensorPos)

for t_FileName in t_ListFiles:
    if t_FileName.endswith('.csv'):
        print('Processing file - ', t_FileName)
        t_FileNameSplited = t_FileName.split('_')
        t_File = open(t_FileDir + '\\' + t_FileName, 'r')
        t_Reader = csv.reader(t_File, delimiter=';')
        # next(t_Reader)
        t_Real = []
        t_Imag = []

        t_Offset = int(t_FileNameSplited[-1].split('.')[0])
        t_DetectorMax = t_Offset+150
        t_DetectorMin = t_Offset+100
        if t_DetectorMax > 250:
            t_DetectorMax = t_DetectorMax-250
        if t_DetectorMin > 250:
            t_DetectorMin = t_DetectorMin-250

        # if t_DetectorMin > t_DetectorMax:
        #     t_DetectorBuf = t_DetectorMin
        #     t_DetectorMin = t_DetectorMax
        #     t_DetectorMax = t_DetectorBuf

        next(t_Reader)
        for baris in t_Reader:
            # print('Sensor dari ', t_DetectorMin, 's/d', t_DetectorMax, ' ada ', t_DetectorMax-t_DetectorMin, ' sensor(s)')
            t_Real.append( float(baris[-2]) * np.cos(float(baris[-1]) * (np.pi/180)) )
            t_Imag.append( float(baris[-2]) * np.sin(float(baris[-1]) * (np.pi/180)) )
            # t_Complex = t_Real + 1j * t_Imag
            # print('Complex = ', t_Complex)
            # print('Real = ', np.real(t_Complex), ' vs ', np.abs(t_Complex))
            # print('Imag = ', np.imag(t_Complex), ' vs ', np.angle(t_Complex) * (180/np.pi))

        t_File.close()

        # sino[int(t_FileNameSplited[-2])] = np.array(t_Real) + 1j * np.array(t_Imag)
        sino[int((float(t_Offset))/10)-1] = np.array(t_Real) + 1j * np.array(t_Imag)

print('Ukuran sino = ', sino.reshape(t_SudutProj, t_SensorPos).shape)
print(sino)
# u_sinR = odt.sinogram_as_rytov(sino.reshape(t_SudutProj, t_SensorPos))
u_sinR = odt.sinogram_as_radon(sino.reshape(t_SudutProj, t_SensorPos))
angles = np.linspace(0, 2*np.pi, t_SudutProj, endpoint=False)
res = 2.0
nmed = 2.4
lD = 4.0
fR = odt.backpropagate_2d(u_sinR, angles, res, nmed, lD * res)
# nR = odt.odt_to_ri(fR, res, nmed)
nR = odt.opt_to_ri(fR, res, nmed)
# print(sino)
fig, axes = plt.subplots(1, 2)
axes = np.array(axes).flatten()
axes[0].imshow(20*np.log10(np.abs(u_sinR)), cmap="jet")
# axes[1].imshow(20*np.log10(np.abs(sino)), cmap="jet")
axes[1].imshow(nR.real, cmap="jet")

plt.show()

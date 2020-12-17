import csv
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from skimage.transform import radon
from skimage.transform import iradon
from skimage.transform import iradon_sart
from skimage import feature
from skimage.filters import threshold_otsu, threshold_local
from skimage.exposure import histogram
import odtbrain as odt
import radontea
from radontea import fan
# from scipy.interpolate import griddata
from scipy import interpolate
from scipy import ndimage

def GenerateSystemMatrix(jmlDetector, jmlPixel, jmlSudutProjection):
    j = jmlDetector
    n = jmlPixel

    Nang = jmlSudutProjection
    angles = np.arange(0,Nang)*360/Nang

    tmp = radon(np.zeros((j, j)), angles, circle=True)
    k = len(tmp.flatten())

    A = np.zeros((k, n))

    for iii in range(0,j*j):
       unitvec = np.zeros((j, j)).flatten()
       unitvec[iii] = 1;

       tmp = radon(unitvec.reshape(j,j), angles, circle=True);
       A[:,iii] = tmp.flatten().transpose()

    return A

if __name__ == "__main__":
    t_Argv = sys.argv
    t_FileDir = t_Argv[1]
    t_ListFiles = os.listdir(t_FileDir)

    t_Freq = t_Argv[2]

    ## pilihan method = {‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’}
    t_InterpolationMethod = t_Argv[3]

    ## Persiapan wadah untuk data
    t_SudutProj = 36
    t_SensorPos = 9
    t_PixelCount = t_SensorPos*t_SensorPos
    t_Pixel = np.zeros(t_PixelCount)
    # t_SensorPos = 2**4
    # t_SensorInterp = 9*10
    t_SensorInterp = 2**6
    # t_SudutInterp = 360
    t_SudutInterp = 2**8
    t_Sino = np.zeros((t_SudutProj,t_SensorPos), dtype=np.complex)#.reshape(t_SudutProj, t_SensorPos)
    t_SinoInterp = np.zeros((t_SudutProj,t_SensorInterp), dtype=np.complex)#.reshape(t_SudutProj, t_SensorInterp)
    t_SinoSudutInterp = np.zeros((t_SudutInterp, t_SensorInterp), dtype=np.complex)
    t_Xinter = np.linspace(0, t_SensorPos-1, t_SensorInterp)
    t_Yinter = np.linspace(0, t_SudutProj-1, t_SudutInterp)

    for t_FileName in t_ListFiles:
        print(t_FileName)
        t_FileNameSplit = t_FileName.split('_')
        t_Sudut = int(float(t_FileNameSplit[1])/10)-1
        t_Titik = int(t_FileNameSplit[-1].split('.')[0])-1
        print('Sudut=', t_Sudut, ' Titik=', t_Titik)
        t_File = open(t_FileDir + '\\' + t_FileName, 'r')
        t_ArrayLine = []
        t_LineNum = 0
        for t_Line in t_File:
            if t_LineNum > 4:
                # print('Line ke-', t_LineNum, t_Line.split(' ')[4])
                t_ArrayLine.append(t_Line.split(' '))
            t_LineNum += 1

        for t_DataLine in t_ArrayLine:
            # default 1,5 Ghz
            # t_Frequency = '1.52500000000E+09'
            if t_Freq == '1,5':
                # t_Frequency = '1.52500000000E+09'
                t_Frequency = '1.53000000000E+09'
            elif t_Freq == '3':
                t_Frequency = '3.00000000000E+09'
            elif t_Freq == '4,5':
                t_Frequency = '4.32500000000E+09'

            if t_DataLine[0] == t_Frequency:
                t_Real = float(t_DataLine[3])
                t_Imag = float(t_DataLine[4])
                # print(t_Real, t_Imag, 'j')
                t_Sino[t_Sudut, t_Titik] = t_Real + 1j*t_Imag

        t_File.close()

        ## Do Interpolasi
        t_XArange = np.arange(t_SensorPos)
        # t_XSinoInterp = np.interp(t_Xinter, t_XArange, t_Sino[t_Sudut][:])
        t_XObjInterpolasi = interpolate.interp1d(t_XArange, t_Sino[t_Sudut][:], kind=t_InterpolationMethod)
        # t_SinoInterp[t_Sudut] = t_XSinoInterp
        t_SinoInterp[t_Sudut] = t_XObjInterpolasi(t_Xinter)

    ## Do Interpolasi Sudut
    t_YArange = np.arange(t_SudutProj)
    for s in range(t_SensorInterp):
        # t_YSudutInterp = np.interp(t_Yinter, t_YArange, t_SinoInterp[:,s])
        t_YObjInterpolasi = interpolate.interp1d(t_YArange, t_SinoInterp[:,s], kind=t_InterpolationMethod)
        # t_SinoSudutInterp[:,s] = t_YSudutInterp
        t_SinoSudutInterp[:,s] = t_YObjInterpolasi(t_Yinter)

    ## Setup background
    t_RealBack = float('-1.60175172169E-02')
    t_ImagBack = float('-1.85142597885E-02')
    t_ComplexBack = t_RealBack + 1j*t_ImagBack
    # t_SinoBack = np.tile(t_ComplexBack, t_SudutProj*t_SensorInterp).reshape(t_SudutProj, t_SensorInterp)
    t_SinoBack = np.tile(t_ComplexBack, t_SudutInterp*t_SensorInterp).reshape(t_SudutInterp, t_SensorInterp)
    # print(t_SinoBack)

    ## Reconstruksi Citra
    A = GenerateSystemMatrix(t_SensorPos, t_PixelCount, t_SudutProj)

    t_Iteration = 10
    t_FlatSino = t_Sino.transpose().reshape(t_SensorPos*t_SudutProj, 1)

    for k in range(t_Iteration):
        print("Loop ke-", k)
        for i in range(t_PixelCount):
            print("Pixel ke-", i+1)
            for j in range(A.shape[0]):
                t_Pixel[i] = (t_Pixel[i] - np.dot(A[j], t_Pixel)) / np.linalg.norm(A[j])
                # print(' norm=', np.linalg.norm(A[j]), ' dot=', np.dot(A[j], t_Pixel[j]))
            # print(t_Pixel)
            # print(A[j])
            # for i in range(t_SensorPos*t_SudutProj):
                # print("Baris ke-", i, ' A_i=', A[i,:], ' Proj=', t_FlatSino[i])

    print(t_Pixel)
    Ax1 = plt.subplot(121)
    Ax2 = plt.subplot(122)
    # Ax1.imshow(np.abs(t_FlatSino))
    Ax1.imshow(t_Pixel.reshape((t_SensorPos, t_SensorPos)).real)
    Ax2.imshow(A)

    plt.tight_layout()
    plt.show()

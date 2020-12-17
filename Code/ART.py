import csv
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from skimage.transform import iradon_sart
from scipy import ndimage
from scipy import interpolate

## Main program
if __name__ == "__main__":

    # Ambil argumen dari user
    t_Argv = sys.argv
    t_FileDir = t_Argv[1]
    t_ListFiles = os.listdir(t_FileDir)

    t_Freq = t_Argv[2]  # Frekuensi yang digunakan

    ## pilihan method = {‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’}
    t_InterpolationMethod = t_Argv[3]

    ## Construct matriks untuk data
    t_SudutProj         = 36        # Jumlah sudut proyeksi
    t_SensorPos         = 9         # Sample per sudut proyeksi
    t_SensorInterp      = 9*10      # Interpolasi Sample per sudut proyeksi
    t_SudutInterp       = 360       # Interpolasi sudut proyeksi
    t_Sino              = np.zeros((t_SudutProj,t_SensorPos), dtype=np.complex)
    t_SinoInterp        = np.zeros((t_SudutProj,t_SensorInterp), dtype=np.complex)
    t_SinoSudutInterp   = np.zeros((t_SudutInterp, t_SensorInterp), dtype=np.complex)
    t_Xinter            = np.linspace(0, t_SensorPos-1, t_SensorInterp)
    t_Yinter            = np.linspace(0, t_SudutProj-1, t_SudutInterp)


    ## Untuk setiap file data hasil pengukuran
    for t_FileName in t_ListFiles:
        # proces nama file sebagai posisi dan sudut dari data
        t_FileNameSplit = t_FileName.split('_')
        t_Sudut = int(float(t_FileNameSplit[1])/10)-1
        t_Titik = int(t_FileNameSplit[-1].split('.')[0])-1

        # buka file
        t_File = open(t_FileDir + '\\' + t_FileName, 'r')
        t_ArrayLine = []
        t_LineNum = 0
        for t_Line in t_File:
            if t_LineNum > 4:
                t_ArrayLine.append(t_Line.split(' '))       # kumpulkan pada t_ArrayLine
            t_LineNum += 1

        for t_DataLine in t_ArrayLine:
            # default 1,5 Ghz
            # t_Frequency = '1.52500000000E+09'
            if t_Freq == '1,5':
                t_Frequency = '1.53000000000E+09'
            elif t_Freq == '3':
                t_Frequency = '3.00000000000E+09'
            elif t_Freq == '4,5':
                t_Frequency = '4.32500000000E+09'

            # Ambil nilai real + imajiner
            # dan tambahkan ke sinogram sebelum interpolasi
            if t_DataLine[0] == t_Frequency:
                t_Real = float(t_DataLine[3])
                t_Imag = float(t_DataLine[4])
                t_Sino[t_Sudut, t_Titik] = t_Real + 1j*t_Imag

        t_File.close()

        ## Do Interpolasi posisi
        t_XArange = np.arange(t_SensorPos)
        t_XObjInterpolasi = interpolate.interp1d(t_XArange,
                                                t_Sino[t_Sudut][:],
                                                kind=t_InterpolationMethod)
        t_SinoInterp[t_Sudut] = t_XObjInterpolasi(t_Xinter)

    ## Do Interpolasi Sudut
    t_YArange = np.arange(t_SudutProj)
    for s in range(t_SensorInterp):
        t_YObjInterpolasi = interpolate.interp1d(t_YArange,
                                                t_SinoInterp[:,s],
                                                kind=t_InterpolationMethod)
        t_SinoSudutInterp[:,s] = t_YObjInterpolasi(t_Yinter)

    ## Setup background value
    t_RealBack = float('-1.60175172169E-02')
    t_ImagBack = float('-1.85142597885E-02')
    t_ComplexBack = t_RealBack + 1j*t_ImagBack
    t_SinoBack = np.tile(t_ComplexBack,
                        t_SudutInterp*t_SensorInterp).reshape(t_SudutInterp, t_SensorInterp)

    ## Prep for Rekonstruksi Citra
    t_Theta = np.linspace(0., 360., t_SudutInterp, endpoint=False)
    t_MedianSize = 7

    ## Background corrected
    t_SinoCorrected = t_SinoSudutInterp - t_SinoBack

    ## Do rekonstruksi filtered back-projection
    t_Reconstruction = iradon_sart(np.abs(t_SinoCorrected.transpose()),
                                    theta=t_Theta, relaxation=0.01)
    ## Do iteratively
    for i in range(50):
        t_Reconstruction = iradon_sart(np.abs(t_SinoCorrected.transpose()),
                                        theta=t_Theta, relaxation=0.01)

    t_FilteredImage = ndimage.median_filter(t_ReconstructImage, size=t_MedianSize)

    fig, (ax1) = plt.subplots(1, 1)
    ax1.imshow(t_FilteredImage)
    ax1.set_xlabel('pixel')
    ax1.set_ylabel('pixel')
    plt.show()

import csv
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from skimage import feature
import odtbrain as odt
from scipy import interpolate
from scipy import ndimage

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
    t_SensorInterp = 9*10
    t_SudutInterp = 360
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

    ## Prep for Reconstruksi Citra
    t_Theta = np.linspace(0., 360., t_SudutInterp, endpoint=False)

    ## Do Fasa background corrected
    t_SinoCorrected = t_SinoSudutInterp/t_SinoBack

    ## Do backpropagate 2D
    u_sinR  = odt.sinogram_as_rytov(t_SinoCorrected)
    angles  = np.linspace(0, 2*np.pi, t_SudutInterp, endpoint=False)
    res     = 9.0
    nmed    = 2.4
    lD      = 1.0
    fR      = odt.backpropagate_2d(u_sinR, angles, res, nmed, lD * res)
    nR      = odt.odt_to_ri(fR, res, nmed)

    ## plot data
    fig, (ax1) = plt.subplots(1, 1)
    ax1.imshow(ndimage.median_filter(nR.real*-1, size=7))
    ax1.set_xlabel('pixel')
    ax1.set_ylabel('pixel')
    plt.show()

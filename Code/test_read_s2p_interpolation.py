import csv
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
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
    # t_Theta = np.linspace(0., 360., t_SudutProj, endpoint=False)
    t_Theta = np.linspace(0., 360., t_SudutInterp, endpoint=False)
    # t_SinoDeembeding = t_Sino
    # t_SinoDeembeding = t_SinoSudutInterp-t_SinoBack
    t_SinoDeembeding = t_SinoSudutInterp/t_SinoBack
    # t_SinoDeembeding = t_SinoInterp-t_SinoBack
    # t_SinoDeembeding = t_SinoInterp
    # t_Reconstruction = iradon_sart(np.abs(t_SinoInterp.transpose()) - np.abs(t_SinoBack.transpose()), theta=t_Theta, relaxation=0.1)
    # t_Reconstruction = iradon_sart(np.abs(t_Sino.transpose()), theta=t_Theta, relaxation=0.1)
    print(np.min(np.abs(t_SinoDeembeding)))
    print(np.max(np.abs(t_SinoDeembeding)))
    print(np.mean(np.abs(t_SinoDeembeding)))

    # t_Reconstruction = iradon_sart(np.abs(t_SinoDeembeding.transpose()), theta=t_Theta, relaxation=0.01)
    # t_Reconstruction = iradon_sart(np.abs(t_SinoDeembeding.transpose())*-1, theta=t_Theta, relaxation=0.01, clip=[0.02,0.04])
    # for i in range(50):
        # t_Reconstruction = iradon_sart(np.abs(t_SinoDeembeding.transpose()), theta=t_Theta, relaxation=0.01)

    # t_Reconstruction = iradon(t_SinoDeembeding.transpose(), filter="ramp" ,interpolation="cubic", circle=False, theta=t_Theta)

    # u_sinR = odt.sinogram_as_rytov(t_SinoSudutInterp / t_SinoBack)
    u_sinR = odt.sinogram_as_rytov(t_SinoDeembeding)
    angles = np.linspace(0, 2*np.pi, t_SudutInterp, endpoint=False)
    res = 9.0
    nmed = 2.4
    lD = 1.0
    fR = odt.backpropagate_2d(u_sinR, angles, res, nmed, lD * res)
    nR = odt.odt_to_ri(fR, res, nmed)


    ## Interpolasi multivariate
    # t_InterpVal = 100
    # x = np.linspace(0, t_SensorInterp-1, t_SensorInterp)
    # y = np.linspace(0, t_SensorInterp-1, t_SensorInterp)
    # X, Y = np.meshgrid(x, y)
    # px = np.random.choice(x, t_InterpVal)
    # py = np.random.choice(y, t_InterpVal)
    # print(t_Reconstruction.flatten().shape)
    # t_RecInter = griddata((px,py), t_Reconstruction.flatten(), (X,Y), method='nearest')
    # t_SinoX, t_SinoY = t_Sino.shape
    # print('sinox=', t_SinoX, ' sinoy=', t_SinoY)
    # t_SinoXNew = np.arange(0, t_SinoX*2)
    # t_SinoYNew = np.arange(0, t_SinoY*2)
    # t_ObjectInterpolasi2D = interpolate.interp2d(t_SinoX, t_SinoY, t_Sino, kind=t_InterpolationMethod)
    # t_NewSino2D = t_ObjectInterpolasi2D(t_SinoXNew, t_SinoYNew)

    plt.suptitle(t_InterpolationMethod)
    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    # ax1 = plt.subplot(212)
    # ax2 = plt.subplot(221)
    # ax3 = plt.subplot(222)
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(224)
    # fig, (ax1) = plt.subplots(1, 1, figsize=(10,5))
    # fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(10,5))
    # ax1.imshow(np.abs(t_SinoInterp))
    # ax2.contourf(t_Reconstruction)
    # ax1.imshow(np.abs(t_SinoInterp))
    # ax1.imshow(np.abs(t_SinoDeembeding.transpose()))
    # ax1.imshow(ndimage.median_filter(t_Reconstruction, size=7))
    # cs = ax1.imshow(ndimage.median_filter(t_Reconstruction, size=7), cmap=plt.cm.jet)
    # cs = ax1.imshow(np.abs(t_Sino.transpose()), cmap=plt.cm.Greys_r)
    # cs = ax1.imshow(nR.real, cmap=plt.cm.jet)
    cs = ax1.imshow(nR.real)
    ax2.imshow(t_Sino.transpose().real)
    ax3.imshow(t_SinoSudutInterp.transpose().real)
    # plt.pcolor(t_Reconstruction, cmap=plt.cm.jet, vmin=t_Reconstruction.min(), vmax=t_Reconstruction.max())
    # plt.pcolor(np.abs(nR), cmap=plt.cm.jet, vmin=np.abs(nR).min(), vmax=np.abs(nR).max())
    # cbar = fig.colorbar(cs, pad=0.02)
    # cbar.ax.set_yticklabels(['low', 'medium', 'high'])
    # ax1.imshow(feature.canny(ndimage.median_filter(t_Reconstruction, size=7)))
    # ax1.imshow(feature.canny(ndimage.median_filter(t_Reconstruction, size=7)*1000000, sigma=3))
    # ax1.set_xlim([-34, 34])
    ax1.set_xlabel('pixel', fontsize=20)
    ax1.set_ylabel('pixel', fontsize=20)
    ax2.set_xlabel('projection angle (degree)', fontsize=12)
    ax2.set_ylabel('position', fontsize=12)
    ax3.set_xlabel('projection angle (degree)', fontsize=12)
    ax3.set_ylabel('position', fontsize=12)
    # ax1.imshow(ndimage.median_filter(nR.real*100000, size=3))
    # ax1.imshow(ndimage.median_filter(t_Reconstruction, size=7)*100000)
    # ax1.imshow(nR.real*-100000)
    # block_size = 35
    # ax1.imshow(histogram(ndimage.median_filter(t_Reconstruction, size=7)*100000, block_size))
    # ax1.set_title('Sinogram')
    # ax1.set_xlabel('Sudut Proyeksi (deg)')
    # ax1.set_ylabel('Posisi')
    # ax1.imshow(np.abs(t_Sino))
    # ax2.imshow(t_Reconstruction)
    # ax3.contourf(t_Reconstruction)
    # ax2.imshow(t_Reconstruction)
    # ax3.imshow(t_Reconstruction)
    # ax3.imshow(ndimage.median_filter(t_Reconstruction, size=7))
    # ax3.contourf(ndimage.median_filter(t_Reconstruction, size=7))
    # ax3.imshow(ndimage.median_filter(nR.real, size=7))
    # ax3.imshow(feature.canny(ndimage.median_filter(nR.real*-100000, size=3), sigma=3))

    # ax1.imshow(np.abs(t_Sino), interpolation='bilinear')
    # ax1.set_title('Sinogram Freq 1,5 Ghz')
    # # ax1.imshow(t_Reconstruction)
    # ax2.imshow(np.abs(t_SinoSudutInterp))
    # ax2.set_title('Sinogram Freq 1,5 Ghz Interpolasi')

    # ax1.imshow(ndimage.median_filter(np.abs(t_Reconstruction), size=20))
    # ax1.imshow(ndimage.minimum_filter(np.abs(t_Reconstruction), size=2))
    # print(np.abs(t_Reconstruction[int(t_Reconstruction.shape[0]/2),:]))
    # ax1.plot(np.abs(t_Reconstruction[int(t_Reconstruction.shape[0]/2),:])*(10**5))
    # ax1.plot(np.abs(t_Reconstruction[int(t_Reconstruction.shape[0]/2),:]))
    # ax3.imshow(np.abs(t_Reconstruction))
    # ax3.contour(weights[::-1], levels=[-.1, .1], colors='k', linestyles='-')
    # ax3.set_title( t_Freq + ' Ghz interpolasi \'' + t_InterpolationMethod + '\'')
    # ax3.set_aspect('equal', 'box')

    # ax2.imshow(np.abs(t_SinoInterp))
    # ax2.set_title('Interpolasi receiver')
    #
    # ax3.imshow(np.abs(t_SinoSudutInterp.transpose()))
    # ax3.set_title('Interpolasi sudut & receiver')
    #
    # ax4.imshow(t_Reconstruction)
    # ax4.set_title('Interpolasi 2D')

    # plt.yscale('log')
    # plt.grid()
    plt.tight_layout()
    plt.show()

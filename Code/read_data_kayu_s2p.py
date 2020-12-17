import csv
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from skimage.transform import iradon
from skimage.transform import iradon_sart
import odtbrain as odt
import radontea
from radontea import fan

def ReadBackground(p_FileDir, p_Freq):
    t_ListFiles = os.listdir(p_FileDir)
    t_U0 = np.zeros(9, dtype=np.complex)

    for t_FileName in t_ListFiles:
        # print(t_FileName)
        t_FileNameSplit = t_FileName.split('_')
        t_Titik = int(t_FileNameSplit[-1].split('.')[0])-1
        # print('Titik = ', t_Titik)
        t_File = open(p_FileDir + '\\' + t_FileName, 'r')
        t_Reader = csv.reader(t_File, delimiter=',')
        t_ArrayLine = []
        for t_Line in t_Reader:
            print(t_Line)
            t_ArrayLine.append(t_Line)

        t_File.close()

        for t_DataLine in t_ArrayLine[3:]:
            # default 1,5 Ghz
            t_Frequency = '1.52500000000E+09'
            if p_Freq == '1,5':
                t_Frequency = '1.52500000000E+09'
            elif p_Freq == '3':
                t_Frequency = '3.00000000000E+09'
            elif p_Freq == '4,5':
                t_Frequency = '4.32500000000E+09'

            if t_DataLine[0] == t_Frequency:
                t_ValueMagnitude = 10**(float(t_DataLine[1])/10)
                # print(t_DataLine[1], 'vs MAGNITUDE = ', t_ValueMagnitude)
                t_ValueAngle = np.abs(np.deg2rad(float(t_DataLine[2])))
                # t_ValueAngle = np.deg2rad(float(t_DataLine[2]))
                # print(t_ValueAngle)
                t_Real = t_ValueMagnitude * np.cos(t_ValueAngle)
                t_Imag = t_ValueMagnitude * np.sin(t_ValueAngle)

                t_U0[t_Titik] = t_Real + 1j*t_Imag

    return t_U0



if __name__ == "__main__":
    t_Argv = sys.argv
    t_FileDir = t_Argv[1]
    t_ListFiles = os.listdir(t_FileDir)

    t_Freq = t_Argv[2]

    t_SudutProj = 72
    t_SensorPos = 9
    t_SensorInterp = 100

    t_Xinter = np.linspace(0, t_SensorPos-1, t_SensorInterp)

    t_Data = np.zeros((t_SudutProj, t_SensorPos))
    t_DataInterp = np.zeros((t_SudutProj, t_SensorInterp))
    t_Sino = np.zeros((t_SudutProj,t_SensorPos), dtype=np.complex)#.reshape(t_SudutProj, t_SensorPos)
    t_SinoInterp = np.zeros((t_SudutProj,t_SensorInterp), dtype=np.complex)#.reshape(t_SudutProj, t_SensorInterp)
    t_DataMagnitude = np.zeros((t_SudutProj, t_SensorPos))
    t_DataPhase = np.zeros((t_SudutProj, t_SensorPos))

    t_U0 = ReadBackground('Simulasi\\Pengukuran Kayu\\1,5 Ghz\\Kosong', t_Freq)

    t_DataBackground = np.zeros((t_SensorInterp,t_SudutProj), dtype=np.complex)
    # t_Data = np.tile(t_DataAmplitude, 72).reshape(9, 72)
    t_XBackArange = np.arange(t_SensorPos)
    t_XBackInterp = np.interp(t_Xinter, t_XBackArange, t_U0)

    # for x in range(t_SensorInterp):
        # t_DataBackground[x,:] = t_XBackInterp

    for t_FileName in t_ListFiles:
        print('Processing file - ', t_FileName)
        t_FileNameSplit = t_FileName.split('_')
        t_Sudut = int(float(t_FileNameSplit[1])/5)-1
        t_Titik = int(t_FileNameSplit[-1].split('.')[0])-1
        # print('Sudut = ', t_Sudut, ' Titik = ', t_Titik)
        t_File = open(t_FileDir + '\\' + t_FileName, 'r')
        t_Reader = csv.reader(t_File, delimiter=',')
        t_ArrayLine = []
        for t_Line in t_Reader:
            t_ArrayLine.append(t_Line)

        t_File.close()

        for t_DataLine in t_ArrayLine[3:]:
            # default 1,5 Ghz
            t_Frequency = '1.52500000000E+09'
            if t_Freq == '1,5':
                t_Frequency = '1.52500000000E+09'
            elif t_Freq == '3':
                t_Frequency = '3.00000000000E+09'
            elif t_Freq == '4,5':
                t_Frequency = '4.32500000000E+09'

            if t_DataLine[0] == t_Frequency:
                t_ValueMagnitude = 10**(float(t_DataLine[1])/10)
                # print(t_DataLine[1], 'vs MAGNITUDE = ', t_ValueMagnitude)
                t_ValueAngle = np.abs(np.deg2rad(float(t_DataLine[2])))
                # t_ValueAngle = float(t_DataLine[2])
                # print(t_ValueAngle)
                t_Real = t_ValueMagnitude * np.cos(t_ValueAngle)
                t_Imag = t_ValueMagnitude * np.sin(t_ValueAngle)
                # print(t_Sudut)
                # t_Data[t_Sudut][t_Titik-1] = t_ValueMagnitude
                # t_Data[t_Sudut][t_Titik] = t_Real
                t_Data[t_Sudut, t_Titik] = t_Real
                # t_Sino[t_Sudut][t_Titik] = t_Real + 1j*t_Imag
                t_Sino[t_Sudut, t_Titik] = t_Real + 1j*t_Imag
                t_DataMagnitude[t_Sudut][t_Titik] = t_ValueMagnitude
                t_DataPhase[t_Sudut][t_Titik] = t_ValueAngle
                # print(t_Sino[t_Sudut][t_Titik])

        # print(t_Data[t_Sudut][:])
        t_XArange = np.arange(t_SensorPos)
        t_XInterp = np.interp(t_Xinter, t_XArange, t_Data[t_Sudut][:])
        t_XSinoInterp = np.interp(t_Xinter, t_XArange, t_Sino[t_Sudut][:])
        # print(t_XInterp)
        t_DataInterp[t_Sudut] = t_XInterp
        t_SinoInterp[t_Sudut] = t_XSinoInterp
    # for key in sorted(t_Data):
    #     print(key , ' = ', t_Data[key])

    # print(t_Data)

    ## Interpolation
    # t_NX, t_NY = t_Data.shape
    # t_X = t_Data[0]
    # t_DataInterp

    ## Backprojection
    # t_Reconstruction = iradon_sart(t_Data)
    # t_Reconstruction = iradon(t_Data, filter="ramp" ,interpolation="linear", circle=True, output_size=73*2)
    # for i in range(20):
        # t_Reconstruction = iradon_sart(t_Data, image=t_Reconstruction)

    ## Backpropagation
    # u_sinR = odt.sinogram_as_rytov(t_SinoInterp.reshape(t_SudutProj, t_SensorInterp), u0=t_DataBackground)
    # u_sinR = odt.sinogram_as_rytov(t_SinoInterp.reshape(t_SudutProj, t_SensorInterp))
    u_sinR = odt.sinogram_as_rytov(t_SinoInterp)
    # for x_back in range(72):
    #     for y_back in range(72):
    #         if t_DataBackground[x_back,y_back] == 0. :
    #             t_DataBackground[x_back, y_back] = 1.

    # u_sinR = t_SinoInterp.reshape(t_SudutProj, t_SensorInterp)/t_DataBackground
    # u_sinR = t_SinoInterp.reshape(t_SudutProj, t_SensorInterp)
    t_Theta = np.linspace(0., 360., t_SudutProj, endpoint=False)
    # t_Reconstruction = iradon(t_DataInterp.transpose(), filter="ramp" ,interpolation="linear", circle=True, theta=t_Theta)
    # t_Reconstruction = iradon(t_DataInterp.transpose(), filter="ramp" ,interpolation="linear", circle=False, theta=t_Theta)
    # t_Reconstruction = radontea.backproject(t_DataInterp.transpose(), t_Theta)
    t_Reconstruction = radontea.fan.radon_fan(t_DataInterp.transpose(), det_size=9, det_spacing=2)
    print(t_Reconstruction.shape)
    # t_Reconstruction = iradon_sart(t_DataInterp.transpose(), theta=t_Theta, relaxation=0.01)
    # for i in range(10):
        # t_Reconstruction = iradon_sart(t_DataInterp.transpose(), image=t_Reconstruction, relaxation=0.01)
    angles = np.linspace(0, 2*np.pi, t_SudutProj, endpoint=False)
    res = 2.0
    nmed = 1.0
    lD = 2.0
    fR = odt.backpropagate_2d(u_sinR, angles, res, nmed, lD * res)
    # fR = odt.fourier_map_2d(u_sinR, angles, res, nmed, lD * res)
    # fR = odt.integrate_2d(u_sinR, angles, res, nmed, lD * res)
    nR = odt.odt_to_ri(fR, res, nmed)
    # nR = odt.opt_to_ri(fR, res, nmed)

    # fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(8, 4.5))
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # ax1.imshow(t_DataInterp.transpose(), cmap="jet")
    # ax1.imshow(np.abs(t_DataBackground), cmap="jet")
    # ax1.set_title("Projection")
    # ax1.set_xlabel("Sudut (per 5 derajat)")
    # ax1.set_ylabel("Receiver Position")
    #
    ax2.imshow(np.abs(t_Reconstruction), cmap="jet")
    ax2.set_title("Image Reconstruction")
    #
    # ax3.imshow(np.abs(u_sinR), cmap="jet")
    #
    # ax4.imshow(nR.real, cmap="jet")
    #
    # ax1.imshow(np.angle(t_SinoInterp/t_DataBackground), cmap="jet")
    # ax2.imshow(np.abs(nR), cmap="jet")

    # plot = ax2.pcolor(nR.real, cmap="jet")
    # fig.colorbar(plot)



    # plot = ax1.pcolor(t_DataMagnitude, cmap="jet")
    # fig.colorbar(plot)
    # ax1.imshow(t_DataMagnitude, cmap="jet")
    # ax2.imshow(t_DataPhase, cmap="jet")
    # ax3.imshow(t_Reconstruction, cmap="jet")
    # ax4.plot(nR.real[int(t_SudutProj/2)])

    # --------------------------------------------------------------------------
    # ax1.set_xlabel("Sudut (per 5 derajat)")
    # ax1.set_ylabel("Receiver Position")
    # ax3.imshow(20*np.log10(np.abs(t_Reconstruction)), extent=(0, 180, 0, 180))
    # ax3.imshow(t_Reconstruction, extent=(0, 360, 0, 360))
    # ax3.imshow(20*np.log10(np.abs(u_sinR)))
    # ax4.imshow(nR.real)
    # ax3.imshow(np.angle(t_Sino))
    # ax3.imshow(20*np.log10(np.abs(u_sinR)))
    # ax3.imshow(nR.real)
    # ax2.imshow(reconstruction_fbp, extent=(0, 361, 0, 361))
    # plt.plot(t_Data)
    plt.show()

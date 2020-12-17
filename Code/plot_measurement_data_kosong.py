import os
import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
    t_Argv = sys.argv
    t_FileDir = t_Argv[1]
    t_Freq = t_Argv[2]
    t_ListFiles = os.listdir(t_FileDir)

    t_DataAmplitude = []
    t_DataPhase = []

    for t_FileName in t_ListFiles:
        print(t_FileName)
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
                t_ValuePhase = np.abs(float(t_DataLine[2]))
                print('Amplitude = ', t_ValueMagnitude, '; Phase = ', t_ValuePhase)
                t_DataAmplitude.append(t_ValueMagnitude)
                t_DataPhase.append(t_ValuePhase)

    # t_Data = np.zeros((9,72))
    t_Data = np.zeros((9,36))
    # t_Data = np.tile(t_DataAmplitude, 72).reshape(9, 72)
    for x in range(9):
        for y in range(36):
            print('data ', x, 'x', y, '=', t_DataAmplitude[x])
            t_Data[x][y] = t_DataAmplitude[x]

    # plt.imshow(t_Data)
    plt.plot(10*np.log10(t_Data[:,0]))
    plt.grid(True)
    # plot = plt.pcolor(t_Data)
    # plt.colorbar(plot)
    plt.show()

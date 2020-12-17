import csv
import sys
import os
from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    t_Argv = sys.argv
    t_FileDir = t_Argv[1]
    t_ListFiles = os.listdir(t_FileDir)

    t_Freq = t_Argv[2]

    ## pilihan method = {‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’}
    t_InterpolationMethod = t_Argv[3]

    for t_FileName in t_ListFiles:
        print(t_FileName)
        t_FileNameSplit = t_FileName.split('_')
        t_Sudut = int(float(t_FileNameSplit[1])/10)-1
        t_Titik = int(t_FileNameSplit[-1].split('.')[0])-1
        print('Sudut=', t_Sudut, ' Titik=', t_Titik)
        t_File = open(t_FileDir + '\\' + t_FileName, 'r')
        # t_ArrayLine = []
        # t_LineNum = 0
        # for t_Line in t_File:
        #     if t_LineNum > 4:
        #         # print('Line ke-', t_LineNum, t_Line.split(' ')[4])
        #         t_ArrayLine.append(t_Line.split(' '))
        #     t_LineNum += 1
        #
        # for t_DataLine in t_ArrayLine:
        #     # default 1,5 Ghz
        #     # t_Frequency = '1.52500000000E+09'
        #     if t_Freq == '1,5':
        #         # t_Frequency = '1.52500000000E+09'
        #         t_Frequency = '1.53000000000E+09'
        #     elif t_Freq == '3':
        #         t_Frequency = '3.00000000000E+09'
        #     elif t_Freq == '4,5':
        #         t_Frequency = '4.32500000000E+09'
        #
        #     if t_DataLine[0] == t_Frequency:
        #         t_Real = float(t_DataLine[3])
        #         t_Imag = float(t_DataLine[4])
        #         # print(t_Real, t_Imag, 'j')
        #         t_Sino[t_Sudut, t_Titik] = t_Real + 1j*t_Imag

        t_File.close()

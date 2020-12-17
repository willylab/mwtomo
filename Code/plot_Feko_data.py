import sys
from matplotlib import pyplot as plt
import numpy as np
import csv

if __name__ == '__main__':
    t_Argv = sys.argv

    t_FileName = t_Argv[1]
    print('Plotting file -', t_FileName)

    t_File = open(t_FileName, 'r')
    t_Reader = csv.reader(t_File, delimiter=';')
    t_Data = []
    for t_Line in t_Reader:
        # print(t_Line[-2])
        t_Data.append(20*np.log10(float(t_Line[-2])))
    print(t_Reader.line_num)

    plt.plot(t_Data)
    plt.show()

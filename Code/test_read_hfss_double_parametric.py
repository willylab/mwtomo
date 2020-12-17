import csv
import sys
import numpy as np
from matplotlib import pyplot as plt


if __name__ == "__main__":
    t_Argv = sys.argv
    print("Processing file - ", t_Argv[1])
    t_File = open(t_Argv[1], 'r')
    t_Reader = csv.reader(t_File, delimiter=',')
    t_CountBaris = 0
    t_ArraySudut = []
    t_ArrayPosisi = []
    t_ArrayValue = []
    t_ArrayData = np.zeros((19, 21))
    t_Dict = {}
    # next(t_Reader)
    for t_Baris in t_Reader:
        t_CountKolom = 0
        for t_Kolom in t_Baris:
            if t_CountBaris == 0:       ## Header
                # print(t_Kolom.split("-")[1])
                t_CountSubKolom = 0
                for t_SubKolom in t_Kolom.split("-"):
                    print('test ', t_SubKolom)
                    if t_CountSubKolom == 1:
                        t_HeaderValue = t_SubKolom.strip().split(" ")
                        t_PutarXKey, t_PutarXValue = t_HeaderValue[0].split("=")
                        t_TranslasiXKey, t_TranslasiXValue = t_HeaderValue[1].split("=")
                        # t_ArrayKey.append(t_PutarXKey)
                        # t_ArrayValue.append(int(t_PutarXValue.replace('\'', '').replace('deg', '')))
                        # print(t_PutarXKey, ' = ', int(int(t_PutarXValue.replace('\'', '').replace('deg', ''))/10))
                        # print(t_TranslasiXKey, ' = ', int(int(t_TranslasiXValue.replace('\'', '').replace('mm', ''))/10)-3)
                        t_Sudut = int(int(t_PutarXValue.replace('\'', '').replace('deg', ''))/10)
                        t_Posisi = int(int(t_TranslasiXValue.replace('\'', '').replace('mm', ''))/10)-3
                        print('Sudut = ', t_Sudut, ' Posisi = ', t_Posisi)
                        # t_ArrayData[t_Sudut, t_Posisi] = 1.0
                        t_ArraySudut.append(t_Sudut)
                        t_ArrayPosisi.append(t_Posisi)
                    t_CountSubKolom += 1
            else:
                if t_CountKolom != 0:
                    print(t_CountKolom, ' = ', t_Kolom)
                    t_ArrayValue.append(float(t_Kolom))
                # t_CountSubKolom = 0
                # print('kesisni')
                # for t_SubKolom in t_Kolom.split(","):
                #     print(t_CountSubKolom)
                #     if t_CountSubKolom == 0:
                #         print('Freq = ', t_SubKolom)
                #     else:
                #         print('Value = ', t_SubKolom)
                #     t_CountSubKolom = t_CountSubKolom + 1
                #     print('testsetsets ', t_CountSubKolom)

            t_CountKolom += 1
    #     t_CountKolom = 0
    #     for t_Kolom in t_Baris:
    #         t_CountKolom += 1
    #         print(t_Kolom)
    #         if t_Count == 0:
    #             t_Key = t_Kolom.split('-')
    #             if len(t_Key) == 2:
    #                 t_ArrayKey.append(t_Kolom.split('-')[1])
    #             else:
    #                 t_ArrayKey.append(t_Kolom.split('-')[0])
    #         else:
    #             t_ArrayValue.append(t_Kolom)
        t_CountBaris += 1

    # print(t_CountBaris)
    # print(t_CountKolom)
    # print(len(t_ArraySudut), '-', len(t_ArrayPosisi), '-', len(t_ArrayValue))
    #
    # print(t_ArrayKey)
    # print(t_ArrayValue)
    # for i in range(len(t_ArrayKey)):
    #     t_SplitedKey = t_ArrayKey[i].strip().split(' ')
    #     t_PutarX = t_SplitedKey[0].split('=')
    #     t_TranslasiY = t_SplitedKey[1].split('=')
    #     print(t_PutarX[1])
    #     t_Dict[t_ArrayKey[i]] = t_ArrayValue[i]
    #
    # print("Jumlah baris = ", t_Count)
    # print("Jumlah kolom = ", t_CountKolom)
    # for k,v in t_Dict.items():
    #     print(k, '==', v)
    t_File.close()

    for i in range(len(t_ArraySudut)):
        # print('Sudut=', t_ArraySudut[i], ' Posisi=', t_ArrayPosisi[i], ' Value=', t_ArrayValue[i])
        t_ArrayData[t_ArraySudut[i], t_ArrayPosisi[i]] = t_ArrayValue[i]

    print(t_ArrayData)
    plt.imshow(t_ArrayData)
    plt.show()

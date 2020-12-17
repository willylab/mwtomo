import sys
import numpy as np

if __name__ == '__main__':
    print('Hello World')

    t_Argv = sys.argv
    t_FileName = t_Argv[1]
    t_FileDir = t_Argv[2]
    t_NamaFile = t_FileName.split("\\")[-1].split(".")[-2]
    print('Processing file -', t_NamaFile)

    t_Lines = [t_Line.rstrip('\n') for t_Line in open(t_FileName)]
    t_Found = False
    t_Count = 0
    t_Sudut = 0
    for t_Baris in t_Lines:
        if t_Baris.find("Direction of incidence: THETA =   90.00") != -1:
            t_BarisSplited = t_Baris.split(" ")
            t_Sudut = int(t_BarisSplited[-1].split(".")[0])
        if t_Baris.find("VALUES OF THE ELECTRIC FIELD STRENGTH in V/m") != -1:
            t_Found = True
            t_Count += 1
            t_Array = []
            print('----------------------')

        if t_Baris.find("VALUES OF THE MAGNETIC FIELD STRENGTH in A/m") != -1:
            t_Found = False
            print('Data sudut ke-', t_Sudut)
            # t_DataAkhir = []
            # t_FileTulis = open('Simulasi\\Feko\\Data Excel\\Silinder_Bolong_Kotak2\\'+t_NamaFile + '_' +str(t_Sudut) + '_.csv', 'w')
            t_FileTulis = open(t_FileDir + '\\' + t_NamaFile + '_' +str(t_Sudut) + '_.csv', 'w')
            for t_Data in t_Array[6:-5]:
                t_DataSplited = t_Data.replace(" ", ";")
                t_Data1 = t_DataSplited.replace(";;;", ";")
                t_DataAkhir = t_Data1.replace(";;", ";")
                # t_DataString = t_DataSplited[-5].lower()
                # print(t_DataString)
                # t_Value = float(t_DataString)
                # print(t_Value)
                # t_DataArray = t_Data2.split(";")
                # print(t_DataArray[-2], ' vs ', float(t_DataArray[-2]))
                # t_X = np.array(t_DataArray[1:])
                # t_Y = t_X.astype(np.float)
                print(t_DataAkhir[1:])
                t_FileTulis.write(t_DataAkhir[1:])
                t_FileTulis.write('\n')
            t_FileTulis.close()
            print('======================')

        if t_Found == True:
            # print(t_Baris)
            t_Array.append(t_Baris)

    print('Jumlah data = ', t_Count)

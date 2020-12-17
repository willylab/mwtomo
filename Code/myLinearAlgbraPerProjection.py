import numpy as np
import scipy.misc as im
import sys
from matplotlib import pyplot as plt

if __name__ == "__main__":
    t_Argv = sys.argv
    # A = np.random.rand(5,5)
    # A = np.ones((5,5), dtype=float)
    detectorNum = 9
    A = np.empty((detectorNum,detectorNum*detectorNum), dtype=np.uint32)
    A.fill(0)

    # A[1,1] = 23
    inc = 0
    for row in range(A.shape[0]):
        # print(inc, '\n')
        for col in range(detectorNum):
            # print('\t', inc+row+col)
            A[row,inc+col] = 1
        inc += detectorNum

    # print(A)

    # A_Origin = A
    # for proj in range(36):
    A_Rotated = im.imrotate(A, -int(t_Argv[1]))
        # A_Rotated = im.imrotate(A_Origin, (proj+1)*-10)
    for row in range(A_Rotated.shape[0]):
        for col in range(A_Rotated.shape[1]):
            if A_Rotated[row, col] != 0:
                A_Rotated[row, col] = 1
        # A = np.vstack((A, A_Rotated))

    # print(A.shape)
    # print(A_Rotated.shape)
    # A_Joint = np.vstack((A, A_Rotated))

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.imshow(A)
    for i in range(A_Rotated.shape[0]):
        for j in range(A_Rotated.shape[1]):
            text = ax1.text(j, i, A[i, j], ha="center", va="center", color="w")

    ax2.imshow(A_Rotated)
    for i in range(A_Rotated.shape[0]):
        for j in range(A_Rotated.shape[1]):
            text = ax2.text(j, i, A_Rotated[i, j], ha="center", va="center", color="w")
    fig.tight_layout()
    plt.show()

    # for i in range(36):
    #     A = im.imrotate(A, i*10)
    #     print('angle=', i*10, ' ', A)

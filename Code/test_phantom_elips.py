import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imread
import radontea
from skimage.transform import iradon
from skimage.transform import iradon_sart


if __name__ == '__main__':
    t_Image = imread("Kayu_Edited_350_pixel_Noised_3Ghz.png", as_grey=True)

    ## Generate Noise
    t_Noise = np.random.normal(0, 0.1, 350*350).reshape(350, 350)

    t_ImageNoised = t_Image+t_Noise

    A = 100
    TitikInterpolasi = 100
    # t_Angles = np.linspace(0, np.pi, A)
    t_Angles = np.linspace(0, np.pi, A)


    # t_ImagePartial = t_ImageNoised[::12, ::12]
    t_ImagePartial = t_ImageNoised[::7, ::7]
    # t_ImagePartial = t_Image
    print('SHape =', t_ImagePartial.shape)
    t_ImageInterp = np.zeros((A, TitikInterpolasi))
    # t_ImageInterp = t_ImagePartial

    ## Interpolasi Sensor Position
    t_XIndex = np.arange(t_ImagePartial.shape[1])
    t_XIndexInterp = np.linspace(0, t_ImagePartial.shape[1]-1, TitikInterpolasi)
    for t_Sudut in range(t_ImagePartial.shape[0]):
        t_XValueInterp = np.interp(t_XIndexInterp, t_XIndex, t_ImagePartial[t_Sudut])
        t_ImageInterp[t_Sudut] = t_XValueInterp

    ## Interpolasi Sudut
    t_YIndex = np.arange(t_ImageInterp.shape[0])
    t_YIndexInterp = np.linspace(0, t_ImagePartial.shape[0]-1, A)
    for t_SensorPos in range(t_ImageInterp.shape[1]):
        t_YValueInterp = np.interp(t_YIndexInterp, t_YIndex, t_ImageInterp[:,t_SensorPos])
        # print(t_YValueInterp, ' len=', len(t_YValueInterp))
        t_ImageInterp[:,t_SensorPos] = t_YValueInterp

    print(t_ImagePartial.shape)
    t_SinoPartial = radontea.radon_parallel(t_ImagePartial, t_Angles)
    t_Sino = radontea.radon_parallel(t_ImageInterp, t_Angles)
    print('Sinogram shape = ', t_Sino.shape)
    t_FilterBackProjection = radontea.backproject(t_Sino, t_Angles)
    t_SART = radontea.sart(t_Sino, t_Angles, iterations=15)

    # t_Reconstruction = iradon(t_Sino, filter="ramp" ,interpolation="linear", circle=True)#, theta=t_Angles)
    # t_Reconstruction = iradon_sart(t_Sino, theta=t_Angles, relaxation=0.01)



    fig, axes = plt.subplots(2, 2)
    ax = axes.ravel()

    ax[0].set_title("Original")
    # ax[0].imshow(image, cmap=plt.cm.Greys_r)
    # ax[0].imshow(t_ImageNoised[::7], cmap="jet")
    ax[0].imshow(t_SinoPartial[::10], cmap="jet")
    ax[1].imshow(t_Sino, cmap="jet")
    ax[2].imshow(t_FilterBackProjection, cmap="jet")
    ax[3].imshow(t_SART, cmap="jet")
    # ax[3].imshow(t_Reconstruction, cmap="jet")

    # ax[1].imshow(t_Sino, cmap="jet")
    # ax[2].imshow(t_FilterBackProjection, cmap="jet")
    # ax[3].imshow(t_SART, cmap="jet")

    plt.show()

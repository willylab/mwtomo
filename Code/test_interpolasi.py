import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def func(x,y):
    # return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2
    return np.random.rand(1000)

if __name__ == "__main__":
    # grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
    # grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
    # grid_x, grid_y = np.mgrid[0:99:100j, 0:99:100j]
    # print(grid_x.shape, ' vs ', grid_y.shape)

    t_Interp = 500

    # points = np.random.rand(1000, 2)
    pointX = np.linspace(0,99,100)
    pointY = np.linspace(0,99,100)
    X, Y = np.meshgrid(pointX, pointY)
    px = np.random.choice(pointX, t_Interp)
    py = np.random.choice(pointY, t_Interp)
    grid_x, grid_y = np.meshgrid(pointX, pointY)
    # values = func(points[:,0], points[:,1])
    values = np.random.randn(t_Interp)
    # print(pointX.shape, ' vs ', pointY.shape)
    # print(points.shape, ' vs ', values.shape)

    grid_z0 = griddata((pointX,pointY), values, (X, Y), method='nearest')
    grid_z1 = griddata((pointX,pointY), values, (X, Y), method='linear')
    grid_z2 = griddata((pointX,pointY), values, (X, Y), method='cubic')

    # grid_z0 = griddata((px,py), values, (X, Y), method='nearest')
    # grid_z1 = griddata((px,py), values, (X, Y), method='linear')
    # grid_z2 = griddata((px,py), values, (X, Y), method='cubic')

    # grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
    # grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    # grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

    plt.subplot(131)
    plt.imshow(grid_z0)
    plt.subplot(132)
    plt.imshow(grid_z1)
    plt.subplot(133)
    plt.imshow(grid_z2)
    plt.show()

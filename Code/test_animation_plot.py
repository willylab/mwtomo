import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()


def f(x, y):
    # return np.sin(x) + np.cos(y)
    return np.random.randn(120, 100)

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

im = plt.imshow(f(x, y), animated=True)


def updatefig(*args):
    global x, y
    x += np.pi / 15.
    y += np.pi / 20.
    # im.set_array(f(x, y))
    # im.set_array(np.random.randn(120,100))
    # im.set_array(np.random.triangular(-3, 0, 8, 120*100).reshape(120, 100))
    im.set_array(np.random.normal(0, 1, 120*100).reshape(120, 100))
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
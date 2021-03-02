import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib, time
from scipy import interpolate

matplotlib.interactive(True)


class Plot3d:

    def __init__(self, data, name):
        self.X = np.arange(data[0].shape[1])
        self.Y = np.arange(data[0].shape[0])
        self.X, self.Y = np.meshgrid(self.X, self.Y)

        self.data = data

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.title(name)
        self.ax.set_zlim3d(-200, 4000)

        self.index = 0
        self.hasNext = True

        heightR = np.zeros(self.X.shape)
        self.surf = self.ax.plot_surface(
            self.X, self.Y, heightR, rstride=1, cstride=1,
            cmap=cm.coolwarm, linewidth=0, antialiased=True)
        plt.draw()


    def drawNext(self):
        xnew, ynew = np.mgrid[0:3:20j, 0:6:45j]
        tck = interpolate.bisplrep(self.X, self.Y, self.data[self.index], s=0)
        znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

        self.surf.remove()
        self.surf = self.ax.plot_surface(
            xnew, ynew, znew, rstride=1, cstride=1,
            cmap=cm.coolwarm, linewidth=0, antialiased=True)
        plt.draw()  # redraw the canvas
        self.fig.canvas.flush_events()

        self.index += 1
        if self.index >= len(self.data):
            self.hasNext = False

        plt.pause(0.02)

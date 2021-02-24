import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from os import listdir
from os.path import isfile, join
from mathgl import *
from PyQt4 import QtGui,QtCore

import csv

def loadAllData():
    onlyFiles = [f for f in listdir("./logging") if isfile(join("./logging", f))]

    for file in onlyFiles:
        with open('logging/' + file, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            for row in csvReader:
                a = np.matrix(row[1:])
                a = a.astype(float)
                b = np.reshape(a, (4, 7))
                print(b)
                plt.imshow(b)
                plt.colorbar()
                plt.show()
                plotSomething(b)
                break



        break



def plotSomething(matrix):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(matrix.shape[1])
    Y = np.arange(matrix.shape[0])
    X, Y = np.meshgrid(X, Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, matrix, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    #ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


if __name__ == '__main__':
    loadAllData()
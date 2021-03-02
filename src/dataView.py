import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from os import listdir
from os.path import isfile, join
import time

#from graphical.plot3d import Plot3d
import generateFunction

import csv

from scipy import interpolate

allData = []
allForces = []
allDataName = []
allDataZero = []


def loadAllData():
    onlyFiles = [f for f in listdir("./logging") if isfile(join("./logging", f))]

    for file in onlyFiles:
        with open('logging/' + file, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            currentForce = []
            currentData = []
            firstRow = True

            for row in csvReader:
                force = float(row[0])
                a = np.matrix(row[1:])
                a = a.astype(float)
                b = np.reshape(a, (7, 4))

                if firstRow:
                    allDataZero.append(b)
                    firstRow = False
                currentForce.append(float(row[0]))
                currentData.append(b)

            allForces.append(currentForce)
            allDataName.append(file)
            allData.append(currentData)


def zeroAllData(zero, leData):
    test = np.array(zero)
    test = np.mean(test, axis=0)

    data = []
    for i in range(len(leData)):
        d = np.array(leData[i])
        a = np.array(zero[i])
        d = d - a
        data.append(d)

    return test, data


def plotSomething(m):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    for matrix in m:
        # Make data.
        X = np.arange(matrix.shape[1])
        Y = np.arange(matrix.shape[0])
        X, Y = np.meshgrid(X, Y)

        xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
        tck = interpolate.bisplrep(X, Y, matrix, s=0)
        znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

        # Plot the surface.
        # surf = ax.plot_surface(X, Y, matrix, cmap=cm.coolwarm,
        #                       linewidth=0, antialiased=False)

        # fig.clear()
        # Plot the surface.
        surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
                               linewidth=0, antialiased=True)
        plt.pause(0.05)
        time.sleep(0.5)
    plt.show()


if __name__ == '__main__':
    loadAllData()
    t, d = zeroAllData(allDataZero, allData)

    generateFunction.generateFunction(d[0], allForces[0])

#    for i in range(len(d)):
#        a = Plot3d(d[i], allDataName[i])
#        while a.hasNext:
#            a.drawNext()

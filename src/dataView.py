import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from os import listdir
from os.path import isfile, join
import time
import math

#from graphical.plot3d import Plot3d
import generateFunction

import csv

from scipy import interpolate

allData = []
allForces = []
allDataName = []
allDataPosition = []
allDataZero = []

def getPositionInFilename(fileName):
    test = fileName.split("_")
    posX = int(test[1])
    posY = int(test[2].split(".")[0])
    return posX, posY

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
            allDataPosition.append(getPositionInFilename(file))
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


def letsTrySoloFunction(leFunctions, force):
    taxelValue = np.zeros((7, 4))
    for i in range(taxelValue.shape[0]):
        for ii in range(taxelValue.shape[1]):
            a, b, c, d, e, f = leFunctions[(i, ii)]
            taxelValue[i, ii] = generateFunction.fun(force, a, b, c, d, e, f)

    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #X = np.arange(taxelValue.shape[1])
    #Y = np.arange(taxelValue.shape[0])
    #X, Y = np.meshgrid(X, Y)

    #xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
    #tck = interpolate.bisplrep(Y, X, taxelValue, s=0)
    #znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    #surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
    #                       linewidth=0, antialiased=True)
    #plt.show()

    return taxelValue

def letsTryInterpolation(lesFunctions, force, posX, posY):
    base = 4.0

    #Get the square
    x0 = base * math.floor(posX/base)
    x1 = x0 + base
    y0 = base * math.floor(posY/base)
    y1 = y0 + base

    #GetTheIndexes
    x0y0_i = allDataPosition.index((x0, y0))
    x1y0_i = allDataPosition.index((x1, y0))
    x0y1_i = allDataPosition.index((x0, y1))
    x1y1_i = allDataPosition.index((x1, y1))

    #GetTheRatios
    x0_r = (posX-x0)/(x1-x0)
    x1_r = 1.0 - x0_r
    y0_r = (posY-y0)/(y1-y0)
    y1_r = 1.0 - y0_r

    x0y0_r = x0_r * y0_r
    x1y0_r = x1_r * y0_r
    x0y1_r = x0_r * y1_r
    x1y1_r = x1_r * y1_r

    #getResultsOfEachTaxel
    x0y0_v = letsTrySoloFunction(taxelFunctions[allDataName[x0y0_i]], force)
    x1y0_v = letsTrySoloFunction(taxelFunctions[allDataName[x1y0_i]], force)
    x0y1_v = letsTrySoloFunction(taxelFunctions[allDataName[x0y1_i]], force)
    x1y1_v = letsTrySoloFunction(taxelFunctions[allDataName[x1y1_i]], force)

    #ultimateResult
    taxelValue = (x0y0_r * x0y0_v) + (x1y0_r * x1y0_v) + (x0y1_r * x0y1_v) + (x1y1_r * x1y1_v)


    #plot

    # set up a figure twice as wide as it is tall
    fig = plt.figure()

    ax = fig.add_subplot(2, 4, 1, projection='3d')
    X = np.arange(taxelValue.shape[1])
    Y = np.arange(taxelValue.shape[0])
    X, Y = np.meshgrid(X, Y)

    xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
    tck = interpolate.bisplrep(Y, X, x0y0_v, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True)
    ax.set_zlim(-100.01, 3000.01)

#----
    ax = fig.add_subplot(2, 4, 2, projection='3d')
    X = np.arange(taxelValue.shape[1])
    Y = np.arange(taxelValue.shape[0])
    X, Y = np.meshgrid(X, Y)

    xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
    tck = interpolate.bisplrep(Y, X, x0y1_v, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True)
    ax.set_zlim(-100.01, 3000.01)
#----
    ax = fig.add_subplot(2, 4, 5, projection='3d')
    X = np.arange(taxelValue.shape[1])
    Y = np.arange(taxelValue.shape[0])
    X, Y = np.meshgrid(X, Y)

    xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
    tck = interpolate.bisplrep(Y, X, x1y0_v, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)
    ax.set_zlim(-100.01, 3000.01)
#----
    ax = fig.add_subplot(2, 4, 6, projection='3d')
    X = np.arange(taxelValue.shape[1])
    Y = np.arange(taxelValue.shape[0])
    X, Y = np.meshgrid(X, Y)

    xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
    tck = interpolate.bisplrep(Y, X, x1y1_v, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)
    ax.set_zlim(-100.01, 3000.01)


    ax = fig.add_subplot(1, 2, 2, projection='3d')
    X = np.arange(taxelValue.shape[1])
    Y = np.arange(taxelValue.shape[0])
    X, Y = np.meshgrid(X, Y)

    xnew, ynew = np.mgrid[0:6:80j, 0:3:80j]
    tck = interpolate.bisplrep(Y, X, taxelValue, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)
    ax.set_zlim(-100.01, 3000.01)


    plt.show()

    pass


if __name__ == '__main__':
    loadAllData()
    t, d = zeroAllData(allDataZero, allData)

    taxelFunctions = dict()

    for i in range(len(d)):
        functions = generateFunction.generateFunction(d[i], allForces[i])
        taxelFunctions[allDataName[i]] = functions

#    for i in range(len(d)):
#        letsTrySoloFunction(taxelFunctions[allDataName[i]], 1.0)

    letsTryInterpolation(taxelFunctions, 25.12, 6.3, 20.6)

    pass
#    for i in range(len(d)):
#        a = Plot3d(d[i], allDataName[i])
#        while a.hasNext:
#            a.drawNext()

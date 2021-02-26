import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from os import listdir
from os.path import isfile, join

import csv

allData = []
allDataName = []
allDataZero = []

def loadAllData():
    onlyFiles = [f for f in listdir("./logging") if isfile(join("./logging", f))]

    for file in onlyFiles:
        with open('logging/' + file, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            currentData = []
            firstRow = True

            for row in csvReader:
                a = np.matrix(row[1:])
                a = a.astype(float)
                b = np.reshape(a, (4, 7))

                if firstRow:
                    allDataZero.append(b)
                    firstRow = False

                currentData.append(b)

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


def plotSomething(matrix):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(matrix.shape[1])
    Y = np.arange(matrix.shape[0])
    X, Y = np.meshgrid(X, Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, matrix, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)


    plt.show()


if __name__ == '__main__':
    loadAllData()
    t, d = zeroAllData(allDataZero, allData)

    pass
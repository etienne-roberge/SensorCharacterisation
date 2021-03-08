import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.optimize import least_squares, curve_fit


def fun(x, a, b, c, d, e, f):
    return a * x + b * x ** 2 + c * x ** 3 + d * x ** 4 + e * x ** 5 + f


def generateFunction(data, force):

    functionMap = dict()

    for i in range(7):
        for ii in range(4):

            t = np.array(force)
            y = data[:, i, ii]

            res_robust, _ = curve_fit(fun, t, y)

            t_test = np.linspace(t.min(), t.max(), 300)
            a, b, c, d, e, f = res_robust
            result = fun(t_test, a, b, c, d, e, f)

            #plt.plot(t, y)
            #plt.plot(t_test, result)
            #plt.show()

            functionMap[(i, ii)] = [a, b, c, d, e, f]

    return functionMap
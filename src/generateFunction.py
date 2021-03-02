import numpy as np

import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams['figure.figsize'] = (10, 6)
rcParams['legend.fontsize'] = 16
rcParams['axes.labelsize'] = 16

from scipy.optimize import least_squares, curve_fit


def fun(x, a, b, c, d, e, f):
    return a*x + b*x**2 + c * x**3 + d * x**4 + e * x**5 + f

def generateFunction(data, force):
    #x0 = np.ones(3)
    #res_lsq = least_squares(fun, x0, args=(len(force), y_train))
    #res_robust = least_squares(fun, x0, loss='soft_l1', f_scale=0.1, args=(t_train, y_train))

    t = np.array(force)
    y = data[:, 6, 2]

    x0 = np.ones(4)
    res_robust, _ = curve_fit(fun, t, y)

    t_test = np.linspace(t.min(), t.max(), 300)
    a, b, c, d, e, f = res_robust
    result = fun(t_test, a, b, c, d, e, f)
    #y_robust = generate_data(t_test, *res_robust.x)

    plt.plot(t, y)
    plt.plot(t_test, result, label='robust lsq')
    plt.show()

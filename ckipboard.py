import numpy as np

import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams['figure.figsize'] = (10, 6)
rcParams['legend.fontsize'] = 16
rcParams['axes.labelsize'] = 16

from scipy.optimize import least_squares, curve_fit


def fun(x, a, b, c, d):
    return a*x + b*x**2 + c * x**3 + d

def generate_data(t, A, sigma, omega, noise=0, n_outliers=0, random_state=0):
    y = A * np.exp(-sigma * t) * np.sin(omega * t)
    rnd = np.random.RandomState(random_state)
    error = noise * rnd.randn(t.size)
    outliers = rnd.randint(0, t.size, n_outliers)
    error[outliers] *= 35
    return y + error

def generateFunction(data, force):
    #x0 = np.ones(3)
    #res_lsq = least_squares(fun, x0, args=(len(force), y_train))
    #res_robust = least_squares(fun, x0, loss='soft_l1', f_scale=0.1, args=(t_train, y_train))

    t = np.array(force)
    y = data[:, 4, 3]

    x0 = np.ones(4)
    res_robust, _ = curve_fit(fun, t, y)

    t_test = np.linspace(t.min(), t.max(), 300)

    y_robust = generate_data(t_test, *res_robust.x)

    plt.plot(t, y)
    plt.plot(t_test, y_robust, label='robust lsq')
    plt.show()

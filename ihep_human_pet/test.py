"""
@file your_file_name.py
@detail :write your Description
@author Bo Ma
@date 2019.09.28
Email:mabo@ihep.ac.cn
Tel:010-88235869
Cell:15210606357
@version 1.0
"""

import pylab as pl
import numpy as np
from scipy.interpolate import UnivariateSpline


def make_norm_dist(x, mean, sd):
    return 1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x - mean)**2/(2*sd**2))


x = np.linspace(10, 110, 1000)
green = make_norm_dist(x, 50, 10)
pink = make_norm_dist(x, 60, 10)

blue = green + pink

# create a spline of x and blue-np.max(blue)/2
spline = UnivariateSpline(x, blue-np.max(blue)/2, s=0)
r1, r2 = spline.roots()  # find the roots

pl.plot(x, blue)
pl.axvspan(r1, r2, facecolor='g', alpha=0.5)
pl.show()

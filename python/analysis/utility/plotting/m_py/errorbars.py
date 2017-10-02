from scipy.stats import chi2, beta
from math import erf
import numpy as np

from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

def poisson_interval(points, alpha=(1 - erf(1/2**0.5))) :
    a = alpha
    k = points
    low, high = (chi2.ppf(a/2, 2*k) / 2, chi2.ppf(1-a/2, 2*(k+1)) / 2)
    low[k == 0] = 0.0
    return low, high

def efficiency_error(p, f, p_wt2, f_wt2) :
    delta_p = p_wt2**0.5
    delta_f = f_wt2**0.5
    error = ( (delta_p * f)**2 + (delta_f * p)**2 )**0.5 / (p + f)**2.0
    return error

def error_hatches(x, y, xerr, yerr, bin_width) :

    """
    Build symmetric error band "hatches" about a histogram with bin width 'bin_width'.

    x : array of bin-centers of data
    y : array of bin contents
    xerr : error in +/- x direction at data points
    yerr : error in +/- y direction at data points
    bin_width : histogram bin width
    """
    
    error_boxes = []
    for xc, yc, xe, ye in zip(x, y, xerr, yerr) :
        h = yc + ye - (yc - ye) # height of error band, from bottom edge to top edge (==2ye)
        if yc == 0 :
            continue
        rect = Rectangle( (xc, yc-ye), bin_width, h, label = 'Uncertainty',
                    edgecolor = 'none',
                    fill = False,
                    color = None,
                    zorder = 1e6)
        error_boxes.append(rect)

    pc = PatchCollection( error_boxes, label = 'Uncertainty',
                    edgecolor = 'none',
                    facecolor = None,
                    alpha = 0.0,
                    hatch = '\\\\\\\\',
                    zorder = 1e5 )
    return pc

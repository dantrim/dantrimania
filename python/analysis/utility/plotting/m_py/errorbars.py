from scipy.stats import chi2, beta
from math import erf
import numpy as np

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

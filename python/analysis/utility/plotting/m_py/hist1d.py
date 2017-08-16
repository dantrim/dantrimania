#/user/dantrim/n0234val/dantrimania/python/analysis/utility/utils
import dantrimania.python.analysis.utility.utils.plib_utils as plib
import dantrimania.python.analysis.utility.utils.root_utils as ru

plt = plib.import_pyplot()
#r = ru.import_root() 
#import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class hist1d :
    def __init__(self, name="", figsize=(8,6)) :
        self.name = name
        self.x_label = ""
        self.y_label = ""

        self.fig = plt.figure(figsize=figsize)
        self.fig_width = figsize[0]
        self.fig_height = figsize[1]

        self.nbins = 1
        self.x_low = 0
        self.x_high = 1
        self.bin_width = 1

    def set_figsize(figsize=(8,6)) :
        self.fig_width = figsize[0]
        self.fig_height = figsize[1]
        self.fig.set_figheight(figsize[0])
        self.fig.set_figwidth(figsize[1])

    def str(self) :
        return "hist1d    name = %s  x_label = %s  y_label = %s  n_bins = %d  bin_width = %.2f x_low = %.2f  x_high = %.2f" % \
                (self.name, self.x_label, self.y_label, self.nbins, self.bin_width, self.x_low, self.x_high)

class ratio_hist(hist1d) :
    def __init__(self, name = "", figsize = (8,6)) :
        hist1d.__init__(self, name, figsize)

    def str(self) :
        return "ratio_hist [%s]" % hist1d.str(self)

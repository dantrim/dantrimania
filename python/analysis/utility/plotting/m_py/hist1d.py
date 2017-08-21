#!/usr/bin/env python

import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
from matplotlib.gridspec import GridSpec
import numpy as np

class hist1d(object) :
    def __init__(self, name="", figsize=(8,6), logy = False) :
        self._name = name
        self._labels = []
        self._fig = plt.figure(figsize = figsize)
        self._do_logy = logy
        self._auto_y = True
        self._var = ""

        self._bounds = []

        self._nbins = 1
        self._bin_width = 1
        self._xlow = 0
        self._xhigh = 0

        self._ylow = 0
        self._yhigh = 0

    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, val) :
        self._name = val

    @property
    def vartoplot(self) :
        return self._var
    @vartoplot.setter
    def vartoplot(self, var) :
        self._var = var

    @property
    def autoy(self) :
        return self._auto_y
    @autoy.setter
    def autoy(self, val) :
        self._auto_y = True

    @property
    def fig(self) :
        return self._fig
    @fig.setter
    def fig(self, figobj) :
        self._fig = figobj

    @property
    def labels(self) :
        return self._labels
    @labels.setter
    def labels(self, val = ["X","Y"]) :
        self._labels = val

    @property
    def logy(self) :
        return self._do_logy
    @logy.setter
    def logy(self, val) :
        self._do_logy = val
        if val :
            self._ylow = 1e-2
        else :
            self._ylow = 0.0

    @property
    def bounds(self) :
        return self._bounds
    @bounds.setter
    def bounds(self, bounds = []) :
        if len(bounds) == 4 :
            self.autoy = False
            self.yhigh = bounds[3]
        else :
            self.autoy = True
        self.xlow = bounds[1]
        self.xhigh = bounds[2]
        self.binwidth = bounds[0]
        self.nbins = int((bounds[2] - bounds[1]) / bounds[0])

    @property
    def nbins(self) :
        return self._nbins
    @nbins.setter
    def nbins(self, n) :
        self._nbins = n

    @property
    def binwidth(self) :
        return self._bin_width
    @binwidth.setter
    def binwidth(self, width) :
        self._bin_width = width

    @property
    def xlow(self) :
        return self._xlow
    @xlow.setter
    def xlow(self, val) :
        self._xlow = val

    @property
    def xhigh(self) :
        return self._xhigh
    @xhigh.setter
    def xhigh(self, val) :
        self._xhigh = val

    @property
    def ylow(self) :
        return self._ylow
    @ylow.setter
    def ylow(self, val) :
        self._ylow = val

    @property
    def yhigh(self) :
        return self._yhigh
    @yhigh.setter
    def yhigh(self, val) :
        self._yhigh = val

class RatioCanvas(hist1d) :
    def __init__(self, name = "", figsize = (7,8), logy = False) :
        hist1d.__init__(self, name, figsize)

        self._is_ratio = True
        del self._fig
        self._fig = None
        self._upper = None
        self._lower = None

    @property
    def ratio(self) :
        return self._is_ratio

    @property
    def upper(self) :
        return self._upper
    @upper.setter
    def upper(self, pad) :
        self._upper = pad

    @property
    def lower(self) :
        return self._lower
    @lower.setter
    def lower(self, pad) :
        self._lower = pad

    def build_ratio(self, figsize = (7,8)) :
        fig = plt.figure(figsize = figsize)
        grid = GridSpec(100,100)
        upper = fig.add_subplot(grid[0:75, :])
        lower = fig.add_subplot(grid[80:100, :])
        if self.logy :
            upper.set_yscale('log')

        # axes
        upper.set_xticklabels([])
        upper.set_xlim(self.xlow, self.xhigh)
        lower.set_xlim(self.xlow, self.xhigh)
        lower.set_ylim(0.0, 2.0)

        majorticks = [0.0, 0.5, 1.0, 1.5, 2.0]
        lower.set_yticks(majorticks, minor=False)
        lower.set_yticks([], minor=True)
        #lower.set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0])

        for ax in [upper, lower] :
            ax.tick_params(axis='both', which='both', labelsize=16)
            which_grid = 'both'
            if self.logy :
                which_grid= 'major'
            ax.grid(color='k', which=which_grid, linestyle='--', lw=1, alpha=0.1)

        ax_x = upper.get_position().x0
        lower.set_xlabel(self.labels[0],
                            horizontalalignment = 'right',
                            x = 1.0,
                            fontsize = 20)

        upper.set_ylabel(self.labels[1],
                            horizontalalignment = 'right',
                            y = 1.0,
                            fontsize = 18)

        lower.set_ylabel("Data / Pred",
                            fontsize = 18)

        upper.get_yaxis().set_label_coords(-0.16, 1.0)
        lower.get_yaxis().set_label_coords(-0.16, 0.5)

        self.fig = fig
        self.upper = upper
        self.lower = lower
        

    def __str__(self) :
        return "Ratio plot  name = %s" % ( self.name )

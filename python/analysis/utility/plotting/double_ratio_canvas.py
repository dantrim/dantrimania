#!/usr/bin/env python

import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
from matplotlib.gridspec import GridSpec
import numpy as np

class double_ratio_canvas(object) :

    def __init__(self, name = "", figsize = (7, 10), logy = False) :
        self._name = name
        self._figsize = figsize
        self._logy = logy

        self._fig = None
        self._labels = []
        self._upper_pad = None
        self._middle_pad = None
        self._lower_pad = None

        self._x_bounds = []
        self._y_bounds = []

    @property
    def name(self) :
        return self._name

    @property
    def figsize(self) :
        return self._figsize
    @figsize.setter
    def figsize(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : requested figsize (%s) is incorrect size (size=%d, expect=2)' \
                % ( type(self).__name__, val, len(val) ) )
        self._figsize = figsize

    @property
    def logy(self) :
        return self._logy
    @logy.setter
    def logy(self, val) :
        self._logy = val

    @property
    def fig(self) :
        return self._fig

    @property
    def labels(self) :
        return self._labels
    @labels.setter
    def labels(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : Attempting to set labels %s that are incorrect size (size=%d, expect=2)'\
                % ( type(self).__name__, val, len(val) ) )
        self._labels = val

    @property
    def upper_pad(self) :
        return self._upper_pad

    @property
    def middle_pad(self) :
        return self._middle_pad

    @property
    def lower_pad(self) :
        return self._lower_pad

    @property
    def x_bounds(self) :
        return self._x_bounds
    @x_bounds.setter
    def x_bounds(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : Attempting to set x-axis bounds %s that are incorrect size (size=%d, expect=2)' \
                % ( type(self).__name__, val, len(val) ) )
        self._x_bounds = val

    @property
    def y_bounds(self) :
        return self._y_bounds
    @y_bounds.setter
    def y_bounds(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : Attempting to set y-axis bounds %s that are incorrect size (size=%d, expect=2)' \
                % ( type(self).__name__, val, len(val) ) )
        self._y_bounds = val


    def build(self) :

        fig = plt.figure(figsize = self.figsize)
        grid = GridSpec(100,100)
        upper = fig.add_subplot(grid[0:65, :])
        middle = fig.add_subplot(grid[66:83, :])
        lower = fig.add_subplot(grid[85:100, :])
        if self.logy :
            upper.set_yscale('log')

        # axes
        upper.set_xticklabels([])
        middle.set_xticklabels([])
        upper.set_xlim(self.x_bounds[0], self.x_bounds[1])
        middle.set_xlim(self.x_bounds[0], self.x_bounds[1])
        lower.set_xlim(self.x_bounds[0], self.x_bounds[1])

        middle.set_ylim(0.0, 2.0)
        lower.set_ylim(0.0, 2.0)

        for ax in [upper, middle, lower] :
            ax.tick_params(axis = 'both', which = 'both', labelsize = 14)
            which_grid = 'both'
            if self.logy :
                which_grid = 'major'
            ax.grid( color = 'k', which=which_grid, linestyle = '--', lw = 1, alpha = 0.1)
        ax_x = upper.get_position().x0
        lower.set_xlabel(self.labels[0],
                horizontalalignment = 'right',
                x = 1.0,
                fontsize = 20)

        upper.set_ylabel(self.labels[1],
                horizontalalignment = 'right',
                y = 1.0,
                fontsize = 18)

        middle.set_ylabel("Num / Den", fontsize = 12)
        lower.set_ylabel("Num / Den", fontsize = 12)

        upper.get_yaxis().set_label_coords(-0.16, 1.0)
        middle.get_yaxis().set_label_coords(-0.16, 0.5)
        lower.get_yaxis().set_label_coords(-0.16, 0.5)

        self._fig = fig
        self._upper_pad = upper
        self._middle_pad = middle
        self._lower_pad = lower

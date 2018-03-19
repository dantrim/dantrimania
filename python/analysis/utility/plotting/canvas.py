#!/usr/bin/env python

import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker
import numpy as np

class canvas(object) :

    def __init__(self, name = "", figsize = (7,8), logy = False) :
        self._name = name
        self._figsize = figsize
        self._logy = logy

        self._fig = None
        self._labels = []
        self._pad = None

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
        self._figsize = val

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
            raise ValueError('%s : Attempting to set labels (%s) that are incorrect size (size=%d, expect=2)' \
                % ( type(self).__name__, val, len(val)) )
        self._labels = val

    @property
    def x_bounds(self) :
        return self._x_bounds
    @x_bounds.setter
    def x_bounds(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : Attempting to set x-axis bounds (%s) that are incorrect size (size=%d, expect=2)' \
            % ( type(self).__name__, val, len(val) ) )
        self._x_bounds = val

    @property
    def y_bounds(self) :
        return self._y_bounds
    @y_bounds.setter
    def y_bounds(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : Attempting to set y-axis bounds (%s) that are incorrect size (size=%d, expect=2)' \
            % ( type(self).__name__, val, len(val) ) )
        self._y_bounds = val

    @property
    def pad(self) :
        return self._pad

    def build(self) :

        fig = plt.figure(figsize = self.figsize)
        grid = GridSpec(100,100)
        pad = fig.add_subplot(grid[0:100,:])
        if self.logy :
            pad.set_yscale('log')

        # axes configuration
        if not len(self.x_bounds) == 0 :
            pad.set_xlim(self.x_bounds[0], self.x_bounds[1])

        if not len(self.y_bounds) == 0 :
            pad.set_ylim(self.y_bounds[0], self.y_bounds[1])

        pad.tick_params(axis = 'both', which = 'both', labelsize = 16, direction = 'in',
                labelleft = True, bottom = True, top = True, right = True, left = True)
        label_locator_params = {'nbins': 10, 'steps': None, 'tick_values' : (self.x_bounds[0], self.x_bounds[-1]),
                                'integer': False, 'symmetric': False, 'prune': None, 'min_n_ticks': 2}
        pad.xaxis.set_major_locator(ticker.MaxNLocator(**label_locator_params))


        which_grid = 'both'
        if self.logy :
            which_grid = 'major'
        pad.grid(color = 'k', which = which_grid, linestyle = '--', lw = 1, alpha = 0.3)

        if len(self.labels) != 2 :
            raise ValueError('%s build : axis labels (%s) is wrong size (size=%d, expect=2)' \
            % ( type(self).__name__, self.labels, len(self.labels) ) )

        pad.set_xlabel(self.labels[0],
                horizontalalignment = 'right',
                x = 1.0,
                fontsize = 20)
        pad.set_ylabel(self.labels[1],
                horizontalalignment = 'right',
                y = 1.0,
                fontsize = 18)

        pad.get_yaxis().set_label_coords(-0.16, 1.0)
        self._fig = fig
        self._pad = pad

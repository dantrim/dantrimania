#!/usr/bin/env python

import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
from matplotlib.gridspec import GridSpec
import numpy as np

class ratio_canvas(object) :

    def __init__(self, name = "", figsize = (7,8), logy = False) :
        self._name = name
        self._figsize = figsize
        self._logy = logy

        self._fig = None
        self._labels = []
        self._rlabel = "Data / Pred"
        self._upper_pad = None
        self._lower_pad = None

        self._x_bounds = []
        self._y_bounds = []
        self._r_bounds = []

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
            raise ValueError('%s : Attempting to set labels (%s) that are incorrect size (size=%d, expect=2)' % ( type(self).__name__, val, len(val) ) )
        self._labels = val

    @property
    def rlabel(self) :
        return self._rlabel

    @rlabel.setter
    def rlabel(self, val) :
        self._rlabel = val

    @property
    def upper_pad(self) :
        return self._upper_pad

    @property
    def lower_pad(self) :
        return self._lower_pad

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
    def r_bounds(self) :
        return self._r_bounds
    @r_bounds.setter
    def r_bounds(self, val) :
        if len(val) != 2 :
            raise ValueError('%s : Attempting to set ratio y-axis bounds (%s) that are incorrect size (size=%d, expect=2)' \
            % ( type(self).__name__, val, len(val) ) )
        self._r_bounds = val

    def build(self) :

        fig = plt.figure(figsize = self.figsize)
        grid = GridSpec(100,100)
        upper_pad = fig.add_subplot(grid[0:75, :])
        lower_pad = fig.add_subplot(grid[80:100, :])#, sharex = upper_pad)

        if self.logy :
            upper_pad.set_yscale('log')

        # axes configuration
        upper_pad.set_xticklabels([])
        if not len(self.x_bounds) == 0 :
            if len(self.x_bounds) > 2 :
                raise ValueError('%s build : x-axis bounds length is wrong (length=%d, expect=2)' % ( type(self).__name__, len(self.x_bounds) ))
            upper_pad.set_xlim(self.x_bounds[0], self.x_bounds[1])
            lower_pad.set_xlim(self.x_bounds[0], self.x_bounds[1])

        if not len(self.y_bounds) == 0 :
            if len(self.y_bounds) > 2 :
                raise ValueError('%s build : y-axis bounds length is wrong (length=%d, expect=2)' % ( type(self).__name__, len(self.y_bounds) ))
            upper_pad.set_ylim(self.y_bounds[0], self.y_bounds[1])

        lower_pad.set_ylim(0.0, 2.0)
        majorticks = [0.0, 0.5, 1.0, 1.5, 2.0]
        if not len(self.r_bounds) == 0 :
            if len(self.r_bounds) > 2 :
                raise ValueError('%s build : ratio bounds length is wrong (length=%d, expect=2)' % ( type(self).__name__, len(self.r_bounds) ))
            lower_pad.set_ylim(self.r_bounds[0], self.r_bounds[1])
            step = 0.5
            delta = self.r_bounds[1] - self.r_bounds[0]
            step = float(delta / 4)
            #if self.r_bounds[1] < 2.0 :
            #    step = 0.25
            majorticks = np.arange(self.r_bounds[0], self.r_bounds[1] + step, step)
        lower_pad.set_yticks(majorticks, minor = False)
        lower_pad.set_yticks([], minor = True)

        for ax in [upper_pad, lower_pad] :
            ax.tick_params(axis = 'both', which = 'both', labelsize = 16, direction = "in",
                        labelleft=True, bottom = True, top = True, right = True, left = True)
            which_grid = 'both'
            if self.logy :
                which_grid = 'major'
            ax.grid(color = 'k', which = which_grid, linestyle = '--', lw = 1, alpha = 0.1)

        ax_x = upper_pad.get_position().x0

        if len(self.labels) != 2 :
            raise ValueError('%s build : axis labels (%s) is wrong size (size=%d, expect=2)' % ( type(self).__name__, self.labels, len(self.labels) ))

        lower_pad.set_xlabel(self.labels[0],
                horizontalalignment = 'right',
                x = 1.0,
                fontsize = 20)
        upper_pad.set_ylabel(self.labels[1],
                horizontalalignment = 'right',
                y = 1.0,
                fontsize = 18)
        lower_pad.set_ylabel(self.rlabel,
                    fontsize = 18)

        upper_pad.get_yaxis().set_label_coords(-0.16, 1.0)
        lower_pad.get_yaxis().set_label_coords(-0.16, 0.5)

        self._fig = fig
        self._upper_pad = upper_pad
        self._lower_pad = lower_pad
        

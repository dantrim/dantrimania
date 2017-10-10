#!/usr/bin/env python

import numpy as np

class plot1d(object) :

    def __init__(self, name = '', variable = '') :

        self._name = name
        self._vartoplot = variable
        self._bounds = []
        self._bin_width = 0.0
        self._x_low = 0.0
        self._x_high = 0.0
        self._binning = []

        self._labels = []

        # toggles on how to adjust the data before histogramming/plotting
        self._normalized = False
        self._absvalue = False

        # unit string describing unit of bins
        self._units = ""

    @property
    def name(self) :
        return self._name

    @property
    def vartoplot(self) :
        return self._vartoplot

    @property
    def bounds(self) :
        return self._bounds
    @bounds.setter
    def bounds(self, val) :
        if len(val) != 3 :
            raise ValueError('%s bounds : provided bounds %s has incorrect size (size=%d, expect=3)' \
            % ( type(self).__name__, val, len(val)) )

        delta_max_min = val[2] - val[1]
        if val[0] > delta_max_min :
            raise ValueError('%s bounds : provided bounds %s has bin-width wider than x-range (width=%.2f, x-range=%.2f)' \
            % ( type(self).__name__, val, val[0], delta_max_min) )

        self._bounds = val
        self._bin_width = val[0]
        self._x_low = val[1]
        self._x_high = val[2]

        self._binning = np.arange(val[1], val[2] + val[0], val[0])

    @property
    def bin_width(self) :
        return self._bin_width

    @property
    def x_low(self) :
        return self._x_low

    @property
    def x_high(self) :
        return self._x_high

    @property
    def binning(self) :
        return self._binning

    @property
    def labels(self) :
        return self._labels
    @labels.setter
    def labels(self, val) :
        if len(val) != 2 :
            raise ValueError('%s labels : Attempting to set labels %s that are incorrect size (size=%d, expect=2)' \
            % ( type(self).__name__, val, len(val) ) )
        self._labels = val

    @property
    def x_label(self) :
        return self._labels[0]

    @property
    def y_label(self) :
        return self._labels[1]

    @property
    def absvalue(self) :
        return self._absvalue
    @absvalue.setter
    def absvalue(self, val) :
        self._absvalue = val

    @property
    def normalized(self) :
        return self._normalized
    @normalized.setter
    def normalized(self, val) :
        self._normalized = val

    @property
    def units(self) :
        return self._units
    @units.setter
    def units(self, val) :
        self._units = val

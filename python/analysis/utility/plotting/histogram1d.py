#!/usr/bin/env python

import numpy as np
from bisect import bisect_left

class histogram1d(object) :
    def __init__(self, name = '', binning = []) :

        self._name = name
        self._binning = binning
        self._variable_width = False
        self._bin_width = -1
        self._x_low = -1
        self._x_high = -1
        
        self._empty = True
        self._data = np.array([]) # this is the raw data, if plotting absolute don't do that here do that in plot
        self._weights = np.array([]) # weights
        self._weights2 = np.array([]) # weights squared

        self._histogram = np.histogram([]) # histogram object
        self._raw_histogram = np.histogram([])
        self._sumw2_histogram = np.histogram([])

        # if number of bins == 3 the assumption is that:
        #  bins[0] = bin width
        #  bins[1] = low x-axis value
        #  bins[2] = high xaxis value
        # else if >= 3 the assumption is that this is a variable width
        # binning
        if not len(binning) >= 3 :
            raise ValueError('%s : provided binning not valid (length = %d and must be >=3)'
                        % ( type(self).__name__, len(binning) ))
        elif len(binning) == 3 :
            self._variable_width = False
            self._bin_width = binning[0]
            self._x_low = binning[1]
            self._x_high = binning[2]
            self._bins = np.arange(binning[1], binning[2] + binning[0], binning[0])
        else :
            self._variable_width = True
            self._x_low = binning[0]
            self._x_high = binning[-1]
            self._bins = binning
            raise ValueError('%s : variable width binning not yet supported!' % ( type(self).__name__) )

    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, val) :
        self._name = val

    @property
    def data(self) :
        return self._data

    @property
    def weights(self) :
        return self._weights

    @property
    def weights2(self) :
        return self._weights2

    @property
    def binning(self) :
        return self._binning

    @property
    def bins(self) :
        return self._bins

    def bin_centers(self) :
        return [ edge + 0.5 * self.bin_width for edge in self.bins[:-1] ]

    def nbins(self) :
        return len(self._bins) - 1

    @property
    def x_low(self) :
        return self._x_low

    @property
    def x_high(self) :
        return self._x_high

    @property
    def bin_width(self) :
        return self._bin_width

    @property
    def variable_width(self) :
        return self._variable_width

    def add_overflow(self) :
        if not self._variable_width :
            self._data = np.clip(self._data, self._x_low, self._x_high) 
        else :
            raise ValueError('%s : adding overflow for variable width binning not yet supported!'
                    % ( type(self).__name__) )

    def fill(self, input_data = None, input_weights = np.array([])) :
        self._empty = False
        self._data = np.concatenate((self._data, input_data))

        if not input_weights.any() :
            unit_weights = np.ones(len(input_data))
            self._weights = np.concatenate((self._weights, unit_weights))
            self._weights2 = np.concatenate((self._weights2, unit_weights**2))
            #self._histogram += np.histogram(self._data, bins = self.bins, weights = self._weights)

        elif len(input_weights) != len(input_data) :
            raise ValueError('%s : input weights does not have same length as input data (weights=%d, data=%d)'
                        % ( type(self).__name__, len(input_weights), len(input_data) ))
        else :
            self._weights = np.concatenate((self._weights, input_weights))
            self._weights2 = np.concatenate((self._weights2, input_weights**2))

    def clear(self) :
        self._empty = True
        self._data = np.array([])
        self._weights = np.array([])
        self._weights2 = np.array([])

    @property
    def histogram(self) :
        if self._empty :
            return np.array([])
        else :
            self._histogram, _ = np.histogram(self._data, bins = self.bins, weights = self._weights)
            self._raw_histogram, _ = np.histogram(self._data, bins = self.bins, weights = np.ones(len(self._data)))
            self._sumw2_histogram, _ = np.histogram(self._data, bins = self.bins, weights = self._weights2)
            return self._histogram

    def maximum(self) :
        return max(self.histogram)
    def minimum(self) :
        return min(self.histogram)

    def bin_from_x(self,xval) :
        #original idea from https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
        pos = bisect_left(self.bins, xval)
        return pos

    def integral(self, xvals = [0,-1], raw = False) :

        """ take the integral of the events within the histogram bounds
        note: will not take into account the overflow bin(s) unless the
        "add_overflow" method has been called!
        """

        if len(xvals) != 2 :
            raise ValueError('%s integral : requested bounds %s not correct size (need=2, provided=%d)'
                % ( type(self).__name__, xvals, len(xvals) ))

        h = self.histogram # this also resets the sumw2 and raw histograms
        if not h.any() :
            return 0.0

        if xvals == [0,-1] :
            if raw :
                return np.sum(self._raw_histogram)
            else :
                return np.sum(self._histogram)
        else :
            bin_low = self.bin_from_x(xvals[0])
            bin_high = self.bin_from_x(xvals[1])
            if raw :
                return np.sum(self._histogram[int(bin_low):int(bin_high)])
            else :
                return np.sum(self._histogram[int(bin_low):int(bin_high)])

    def integral_and_error(self, xvals = [0,-1], raw = False) :

        """ take the integral of the events within the histogram bounds
        note: will not take into account the overflow bin(s) unless the
        "add_overflow" method has been called!
        """

        if len(xvals) != 2 :
            raise ValueError('%s integral_and_error : requested bounds %s not correct size (need=2, provided=%d)'
                        % ( type(self).__name__, xvals, len(xvals) ))

        h = self.histogram # this also resets the sumw2 and raw histograms
        if not h.any() :
            return 0.0, 0.0

        if xvals == [0,-1] :
            if raw :
                return np.sum(self._raw_histogram), np.sqrt(np.sum(self._raw_histogram))
            else :
                return np.sum(self._histogram), np.sqrt(np.sum(self._sumw2_histogram)) 
        else :
            bin_low = self.bin_from_x(xvals[0])
            bin_high = self.bin_from_x(xvals[1])
            if raw :
                return np.sum(self._raw_histogram[int(bin_low):int(bin_high)]), \
                        np.sqrt(np.sum(self._raw_histogram[int(bin_low):int(bin_high)]))
            else :
                return np.sum(self._histogram[int(bin_low):int(bin_high)]), \
                            np.sqrt(np.sum(self._sumw2_histogram[int(bin_low):int(bin_high)]))

    def y_error(self) :
        """ return an array of the statistical errors
        """

        h = self.histogram # refreshes sumw2 histogram
        if not h.any() :
            return np.array([])
        return np.sqrt(self._sumw2_histogram)

    def divide(self, h_denominator = None) :
        """ divide 'this' histogram by the histogram1d object 'h_denominator',
        returns the bin contents (y-values) of the ratio of each bin
        """
        h_num = self.histogram
        h_den = h_denominator.histogram
        division = np.ones(len(h_num))

        with np.errstate(divide = 'ignore', invalid = 'ignore') :
            division = np.true_divide(h_num, h_den)
            division[division == np.inf] = 0
            division = np.nan_to_num(division)
        return division

    def mean(self) :
        """ return the mean of the data contained in this histogram
        """
        return np.mean(self.data)

    def std(self) :
        """ return the standard deviation of the data contained in this histogram
        """
        return np.std(self.data)

    def var(self) :
        """ return the variance of the data contained in this histogram
        """
        return np.var(self.data)

    def bounding_line(self) :
        """ return a set of points that define the bounding line of the
        histogram
        """

        h = self.histogram # refresh the histograms
        if not h.any() :
            return [], []

        x = []
        y = []

        for iedge, edge in enumerate(self.bins[:-1]) :
            x.append(edge)
            x.append(edge + self.bin_width)
            y.append(h[iedge])
            y.append(h[iedge])
        x.append(x[-1])
        y.append(np.min(h))

        return x, y

    def count_str(self, rmlist = [], name = '') :
        cts, err = self.integral_and_error()
        raw_cts, raw_err = self.integral_and_error(raw=True)
        name_to_use = self.name
        if name != '' :
            name_to_use = name
        elif len(rmlist) > 0 :
            for rm in rmlist :
                name_to_use = name_to_use.replace(rm,"")
        yld_str = " > {bname: <10} : {w_yield:>10} +/- {we_yield:>10} (raw: {r_yield:>10} +/- {re_yield:>10})".format(
                bname = name_to_use,
                w_yield = round(cts,2),
                we_yield = round(err,2),
                r_yield = round(raw_cts,2),
                re_yield = round(raw_err,2))
        return yld_str



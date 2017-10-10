#!/usr/bin/env python

import numpy as np
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
import operator

class histogram_stack(object) :

    def __init__(self, name = '', binning = []) :

        self._name = name

        # array of histogram objects (c.f. histogram1d)
        self._histograms = []

        self._raw_counts = {}
        self._counts = {}

        # order to stack the histograms into based on unique name
        # of each of the histogram objects
        self._order = []

        # total histogram
        self._histogram = histogram1d('hstacktotal_%s' % name, binning = binning)

    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, val) :
        self._name = val

    @property
    def size(self) :
        return len(self._histograms)

    def add(self, histo = None, skip_empty = True) :

        count = histo.integral(raw=True)
        if count > 0 :
            self._histograms.append(histo)
            self._order.append(histo.name)
            self._raw_counts[histo.name] = histo.integral_and_error(raw=True)
            self._counts[histo.name] = histo.integral_and_error(raw=False)

            self._histogram.fill(histo.data, histo.weights)

    @property
    def histograms(self) :
        return self._histograms

    @property
    def total_histo(self) :
        return self._histogram

    @property
    def order(self) :
        return self._order

    @property
    def counts(self) :
        return self._counts

    @property
    def raw_counts(self) :
        return self._raw_counts

    def print_counts(self) :
        print "stack %s counts" % self.name
        for name in self.order[::-1] : # print them out in descending order
            cts = self.counts[name][0]
            cts_e = self.counts[name][1]
            cts_raw = self.raw_counts[name][0]
            cts_raw_e = self.raw_counts[name][1]
            yld_str = " > {bname: <10} : {w_yield:>10} +/- {we_yield:>10} (raw: {r_yield:>10} +/- {re_yield:>10})".format(
                        bname = name.replace("histo_",""),
                        w_yield = round(cts,2),
                        we_yield = round(cts_e,2),
                        r_yield = round(cts_raw,2),
                        re_yield = round(cts_raw_e,2))
            #print " > %s : %10.2f +/- %.2f (raw: %10.2f +/- %.2f)" % (name.replace("histo_","").ljust(15), \
            #cts, cts_e, cts_raw, cts_raw_e)
            print yld_str

    def sort(self, reverse=False, name_list = []) :
        """sort by weighted yield
        'reverse' means the histo with the least counts is on top (so at the
        END of the list that we use to fill)
        """
        if len(name_list) == 0 :
            cts = self.counts
            self._order = sorted(cts, key = cts.__getitem__, reverse = not reverse)
            new_histos = []
            for hname in self._order :
                for h in self._histograms :
                    if h.name == hname :
                        new_histos.append(h)
                        break
            self._histograms = new_histos
                
        else :
            current_names = [h.name for h in self._histograms]
            names_ordered = []
            for n in name_list :
                for cn in current_names :
                    if n in cn :
                        if cn in names_ordered :
                            raise ValueError('%s sort : There appears to be more than \
                             one histogram associated with the name "%s"' % ( type(self).__name__, n )) 
                        names_ordered.append(cn)
                        break
            new_histos = []
            for no in names_ordered :
                for h in self._histograms :
                    if h.name == no :
                        new_histos.append(h)
                        break
            self._order = names_ordered
            self._histograms = new_histos
            
            



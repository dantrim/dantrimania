#!/usr/bin/env python

from collections import OrderedDict

class Cutflow(object) :
    def __init__(self, name = "", displayname = "") :

        self._name = name
        self._displayname = displayname
        self._n_cuts = 0
        self._cut_dict = OrderedDict()

    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, val) :
        self._name = val

    @property
    def displayname(self) :
        return self._displayname
    @displayname.setter
    def displayname(self, val) :
        self._displayname = val

    @property
    def n_cuts(self) :
        return self._n_cuts

    @property
    def cut_dict(self) :
        return self._cut_dict

    def cut_list(self) :
        return self._cut_dict.values()

    def cut_names(self) :
        return self._cut_dict.keys()

    def total_tcut(self) :
        return " && ".join(self._cut_dict.values())

    def tcut_at_idx(self, idx) :

        if idx >= self._n_cuts :
            return self.total_tcut

        cuts = []
        total_number_of_cuts = self._n_cuts
        for icut in xrange(total_number_of_cuts) :
            if icut > idx :
                break
            cuts.append(self.cut_list()[icut])
        return " && ".join(cuts)

    def add_cut(self, name = "", cut_string = "") :
        self._cut_dict[name] = cut_string
        self._n_cuts += 1


    def Print(self) :
        print " Cutflow (name=%s) : %s" % (self.name, self._cut_dict)

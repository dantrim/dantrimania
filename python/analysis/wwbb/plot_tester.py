#!/usr/bin/env python

import sys
import os
#sys.path.append(os.environ['DANTRIM_ANA'])
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d
#import plotting #.m_py.hist1d as hist1d


def main() :
    print "plot tester"

    name = "test histogram"
    figsize=(10,8)
    h = hist1d.ratio_hist(name=name, figsize=figsize)
    print h.str()




#_____
if __name__ == "__main__" :
    main()

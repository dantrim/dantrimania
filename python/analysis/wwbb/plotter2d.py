#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.utils.plib_utils as plib

plt = plib.import_pyplot()
import numpy as np


def main() :
    parser = OptionParser()
    parser.add_option("-c", "--config", default="", help="Configuration file for plotting")
    parser.add_option("-r", "--region", default="", help="Provide a region selection")
    parser.add_option("-o", "--output", default="./", help="Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("-v", "--var-list", default="", help="Provide a list of variables to plot")
    parser.add_option("--cache-dir", default="./sample_cache", help="Directory to place/look for the cached samples")
    (options, args) = parser.parse_args()

#_________________________________________________________________
if __name__ == "__main__" :
    main()

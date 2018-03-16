#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.samples.cutflow as cutflow
#import dantrimania.python.analysis.utility.plotting.m_py.errorbars as errorbars
#import dantrimania.python.analysis.utility.utils.plib_utils as plibo

def get_cutflows() :

    out = []

    # non-resonant selection
    c = cutflow.Cutflow("hhNonRes", "hhNonRes")
    c.add_cut("lepton_pt", "(l0_pt>20 && l1_pt>20)")
    out.append(c)

    return out
    

def main() :
    parser = OptionParser()
    parser.add_option("-r", "--region-name", default = "", help = "Provide a region selection by name")
    parser.add_option("-c", "--config", default = "", help = "Configuration file for plotting")
    (options, args) = parser.parse_args()
    config = options.config
    region_name = options.region_name

    if not utils.file_exists(config) :
        sys.exit()

    global loaded_samples
    global loaded_regions
    global selected_region
    global loaded_plots
    global additional_variables
    loaded_samples = []
    loaded_regions = []
    loaded_plots = []
    
    selected_region = region_name
    execfile(config, globals(), locals())

    if len(loaded_samples) == 0 :
        print "ERROR No loaded samples found in configuration"
        sys.exit()

    backgrounds, signals, data = sample_utils.categorize_samples(loaded_samples)

    available_cutflows = get_cutflows()
    available_regions = [c.name for c in available_cutflows]
    if selected_region not in available_regions :
        print "ERROR Requested region (=%s) is not in configured cutflows (= %s)" % (selected_region, available_regions)
        sys.exit()

    requested_cutflow = None
    for ac in available_cutflows :
        if ac.name == selected_region :
            requested_cutflow = ac

    if not requested_cutflow :
        print "ERROR Did not find selected region in configured cutflows"
        sys.exit()

    print "region total tcut = %s" % requested_cutflow.total_tcut()
    variables_needed_for_cutflow = sample_utils.get_variables_from_tcut(requested_cutflow.total_tcut())
    variables_needed_for_cutflow.append("eventweight")
    variables_needed_for_cutflow.append("isMC")

    # cache
    dummy_cache_selection = "(isMC==1 || isMC==0)"
    dummy_region = region.Region("dummy", "dummy")
    dummy_region.tcut = dummy_cache_selection
    cacher = sample_cacher.SampleCacher("./")
    cacher.samples = loaded_samples
    cacher.region = dummy_region
    cacher.fields = variables_needed_for_cutflow
    print str(cacher)
    cacher.cache()
    

#______________________________________________________
if __name__ == "__main__" :
    main()

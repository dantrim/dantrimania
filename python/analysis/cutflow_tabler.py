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

import numpy as np
from math import sqrt
import tabulate

def get_cutflows() :

    out = []

    trigger_cut_str = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ))"

    # non-resonant selection
    c = cutflow.Cutflow("hhNonRes", "hhNonRes")
    c.add_cut("lepton_pt", "(l0_pt>20 && l1_pt>20)")
    c.add_cut("higgs_mbb", "(mbb>100 && mbb<140)")
    out.append(c)

    # ttbar CR
    c = cutflow.Cutflow("crtt", "crtt")
    c.add_cut("trigger", "(%s)" % trigger_cut_str)
    c.add_cut("bjet", "(nBJets==2)")
    c.add_cut("mll>20", "(mll>20)")
    c.add_cut("higgs_mbb", "(mbb>100 && mbb<140)")
    c.add_cut("higgs_mt2llbb", "(mt2_llbb>100 && mt2_llbb<140)")
    c.add_cut("drll_window", "(dRll>1.5 && dRll<3.0)")
    c.add_cut("ht2", "(HT2Ratio>0.4 && HT2Ratio<0.6)")
    out.append(c)

    # wt CR
    c = cutflow.Cutflow("crwt", "crwt")
    c.add_cut("trigger", "(%s)" % trigger_cut_str)
    c.add_cut("bjet", "(nBJets==2)")
    c.add_cut("mll>20", "(mll>20)")
    c.add_cut("mbb", "(mbb>140)")
    c.add_cut("mt2_bb", "(mt2_bb>150)")
    c.add_cut("ht2", "(HT2Ratio>0.6 && HT2Ratio<0.8)")
    out.append(c)

    return out

def print_cutflow(requested_cutflow, backgrounds) :

    n_cuts = requested_cutflow.n_cuts
    cut_names = requested_cutflow.cut_names()
    cutflow_name = requested_cutflow.name

    header_row = [cutflow_name]
    for icut in xrange(n_cuts) :
        header_row += [cut_names[icut]]

    table_rows = []
    row_counts = []
    for ibkg, bkg in enumerate(backgrounds) :
        bkg_cutflow = []
        rows = []
        bkg_cutflow.append(bkg.name)
        for icut in xrange(n_cuts) :
            bkg_cut_result = bkg.cutflow_result[icut]
            cut_yield = bkg_cut_result[0]
            cut_err = bkg_cut_result[1]
            cut_result_str = "%.2f +/- %.2f" % (cut_yield, cut_err)
            bkg_cutflow.append(cut_result_str)
            rows.append(float(cut_yield))
        table_rows.append(bkg_cutflow)
        row_counts.append(rows)

    print tabulate.tabulate(table_rows, header_row, tablefmt = "rst", numalign = "right", stralign = "left", floatfmt = ".2f")

    header_row[0] = cutflow_name + " - abs eff"
    abs_efficiencies = []
    rel_efficiencies = []
    for ibkg, bkg in enumerate(backgrounds) :
        abs_eff_bkg = [bkg.name, 1]
        rel_eff_bkg = [bkg.name, 1]
        counts = row_counts[ibkg]
        for icut in xrange(n_cuts) :
            if icut == 0 : continue

            abs_num = counts[icut]
            abs_den = counts[0]
            abs_eff = abs_num / abs_den

            rel_num = counts[icut]
            rel_den = counts[icut-1]
            rel_eff = rel_num / rel_den

            abs_eff_bkg.append(abs_eff)
            rel_eff_bkg.append(rel_eff)

        abs_efficiencies.append(abs_eff_bkg)
        rel_efficiencies.append(rel_eff_bkg)

    print tabulate.tabulate(abs_efficiencies, header_row, tablefmt = "rst", numalign = "right", stralign = "left", floatfmt = ".4f")

    header_row[0] = cutflow_name + " - rel eff"
    print tabulate.tabulate(rel_efficiencies, header_row, tablefmt = "rst", numalign = "right", stralign = "left", floatfmt = ".4f")

            
            
    

def make_cutflow_table(requested_cutflow, backgrounds, signals, data) :

    n_cuts = requested_cutflow.n_cuts

    for bkg in backgrounds :
        bkg.cutflow_result = {} # { cut index : [ yield, stat_err ] }

    for icut in xrange(n_cuts) :
        print requested_cutflow.tcut_at_idx(icut)

        for bkg in backgrounds :

            bkg_yield = 0.0
            bkg_sumw2 = 0.0

            chain = bkg.chain()
            for ich, ch in enumerate(chain) :
                weights = ch["eventweight"]
                weights *= ( bkg.scalefactor * np.ones(len(weights)) )
                weights_squared = np.square(weights)

                idx_selection = sample_utils.index_selection_string(requested_cutflow.tcut_at_idx(icut), "ch", requested_cutflow.variable_list)
                set_idx = "indices = np.array( %s )" % idx_selection
                exec(set_idx)

                bkg_yield += np.sum(weights[indices])
                bkg_sumw2 += np.sum(weights_squared[indices])

            #print "bkg %s : %.2f +/- %.2f" % (bkg.name, bkg_yield, sqrt(bkg_sumw2))

            bkg.cutflow_result[icut] = [bkg_yield, sqrt(bkg_sumw2)]

    print_cutflow(requested_cutflow, backgrounds)

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

    print "backgrounds : %s" % [b.name for b in backgrounds]
    print "signals     : %s" % [s.name for s in signals]
    print "data        : %s" % data

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

    requested_cutflow.variable_list = variables_needed_for_cutflow

    make_cutflow_table(requested_cutflow, backgrounds, signals, data)

#______________________________________________________
if __name__ == "__main__" :
    main()

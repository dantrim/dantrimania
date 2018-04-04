#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.plotting.canvas as canvas
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
    isSF = "(isEE==1 || isMM==1 )"
    isDF = "(isDF==1)"
    dilepton_any = "( %s ) || ( %s ) " % ( isSF, isDF )

    # hh base
    c = cutflow.Cutflow("hhBase", "hhBase")
    c.add_cut("dilepton", "(%s)" % dilepton_any)
    c.add_cut("trigger", "(%s)" % trigger_cut_str)
    c.add_cut("2 bjets", "(nBJets==2)") 
    c.add_cut("higgs_mt2_llbb", "(mt2_llbb>100 && mt2_llbb<140)")
    c.add_cut("higgs_mbb", "(mbb>100 && mbb<140)")
    c.add_cut("HT2Ratio>0.8", "(HT2Ratio>0.8)")
    c.add_cut("dRll<0.9", "(dRll<0.9)")
    out.append(c)

    # non-resonant selection
    c = cutflow.Cutflow("hhNonRes", "hhNonRes")
    c.add_cut("dilepton", "(%s)" % dilepton_any)
    c.add_cut("trigger", "(%s)" % trigger_cut_str)
    c.add_cut("bjet", "(nBJets==2)")
    c.add_cut("mll>20", "(mll>20)")
    c.add_cut("higgs_mt2_llbb", "(mt2_llbb>100 && mt2_llbb<140)")
    c.add_cut("higgs_mbb", "(mbb>100 && mbb<140)")
    c.add_cut("ht2", "(HT2Ratio>0.8)")
    c.add_cut("drll", "(dRll<0.9)")
    c.add_cut("mt2_bb", "(mt2_bb>150)")
    out.append(c)

    # ttbar CR
    c = cutflow.Cutflow("crtt", "crtt")
    c.add_cut("dilepton", "(%s)" % dilepton_any)
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
    c.add_cut("dilepton", "(%s)" % dilepton_any)
    c.add_cut("trigger", "(%s)" % trigger_cut_str)
    c.add_cut("bjet", "(nBJets==2)")
    c.add_cut("mll>20", "(mll>20)")
    c.add_cut("mbb", "(mbb>140)")
    c.add_cut("mt2_bb", "(mt2_bb>150)")
    c.add_cut("ht2", "(HT2Ratio>0.6 && HT2Ratio<0.8)")
    out.append(c)

    # LFV - etau
    c = cutflow.Cutflow("lfv_etau", "lfv_etau")
    c.add_cut("dilepton", "(%s)" % dilepton_any)
    c.add_cut("isEM", "(isEM==1 && isME==0)")
    c.add_cut("l0_pt>45", "(l0_pt>45)")
    c.add_cut("l1_pt>15", "(l1_pt>15)")
    c.add_cut("mll_30_150", "(mll>30 && mll<150)")
    c.add_cut("one_bjet", "(nBJets==1)")
    out.append(c)

    # LFV - mutau
    c = cutflow.Cutflow("lfv_mutau", "lfv_mutau")
    c.add_cut("dilepton", "(%s)" % dilepton_any)
    c.add_cut("isME", "(isEM==0 && isME==1)")
    c.add_cut("l0_pt>45", "(l0_pt>45)")
    c.add_cut("l1_pt>15", "(l1_pt>15)")
    c.add_cut("mll_30_150", "(mll>30 && mll<150)")
    c.add_cut("one_bjet", "(nBJets==1)")
    out.append(c)

    # LFV
    c = cutflow.Cutflow("lfv_any", "lfv_any")
    c.add_cut("dilepton", "(%s)" % dilepton_any)
    c.add_cut("isDF", "(isEM==1 || isME==1)")
    c.add_cut("l0_pt>45", "(l0_pt>45)")
    c.add_cut("l1_pt>15", "(l1_pt>15)")
    c.add_cut("mll_30_150", "(mll>30 && mll<150)")
    c.add_cut("one_bjet", "(nBJets==1)")
    out.append(c)

    return out

def plot_cutflow(header_row, table_rows, plot_type = "yields") :

    region_name = header_row[0].split()[0]
    x_labels = [""]
    x_labels += header_row[1:]
    n_x = len(x_labels)

    bkg_names = []
    value_strings = []
    values = []
    errors = []
    maxy = -1
    miny = 1e9
    for row in table_rows :
        bkg_names.append(row[0])
        value_strings.append(row[1:])
        yield_and_error_list = row[1:]
        bkg_values = []
        bkg_errors = []
        for x in yield_and_error_list :

            yield_value = 0.0
            error_value = 0.0

            if "eff" not in plot_type :
                yield_string = x.strip().split()[0]
                error_string = x.strip().split()[2]

                yield_value = float(yield_string)
                error_value = float(error_string)
            else :

                yield_value = float(x)


            if yield_value > maxy : maxy = yield_value 
            if yield_value < miny : miny = yield_value 

            bkg_values.append(yield_value)
            bkg_errors.append(error_value)
        values.append(bkg_values)
        errors.append(bkg_errors)

    if plot_type == "fraction" :
        n_cuts = len(value_strings[0])
        total_yields_at_cuts = []
        fractions = []
        for icut in xrange(n_cuts) :
            total_for_cut = 0.0
            for v in values :
                total_for_cut += v[icut]
            total_yields_at_cuts.append(total_for_cut)

        for ibkg, bkg_values in enumerate(values) :
            bkg_fractions = []
            for icut, cut_value in enumerate(bkg_values) :
                bkg_fractions.append(float(cut_value) / total_yields_at_cuts[icut])
            fractions.append(bkg_fractions)

        values = fractions

        maxy = 1.2
        miny = 1e-3

    maxy = 1e1 * maxy
    miny = 1e-1 * miny

    can = canvas.canvas(name = "canvas_%s" % region_name, logy = True)
    can.x_bounds = [0, n_x-1]

    x_axis_label = "Cut"
    y_axis_label = ""
    if plot_type == "yields" :
        y_axis_label = "Yield"
    elif plot_type == "fraction" :
        y_axis_label = "Process Fraction"
    elif "eff" in plot_type :
        if "abs" in plot_type :
            y_axis_label = "Absolute Efficiency (Yield Cut i / Yield Cut 0)"
        elif "rel" in plot_type :
            y_axis_label = "Relative Efficiency (Yield Cut i / Yield Cut i-1)"

    can.labels = [x_axis_label, y_axis_label]
    can.build()
    can.pad.set_ylim(miny, maxy)
    x_tick_vals = np.arange(0, n_x+1, 1)
    can.pad.set_xticks(x_tick_vals)
    can.pad.set_xticklabels(x_labels, rotation = 65)

    xvals_i = np.arange(1, n_x)
    xvals = []
    for i in xrange(len(bkg_names)) :
        xvals.append(xvals_i)

    for i in xrange(len(values)) :
        can.pad.plot(xvals[0], values[i], linestyle = '-', marker = 'o', label = bkg_names[i])
    can.pad.legend(loc='best')

    ## save
    can.fig.savefig("cutflow_plot_%s_%s.pdf" % ( region_name, plot_type ), bbox_inches = "tight", dpi = 200)

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

    if requested_cutflow.make_plots :
        plot_cutflow(header_row, table_rows, "yields")
        plot_cutflow(header_row, table_rows, "fraction")

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
    if requested_cutflow.make_plots :
        plot_cutflow(header_row, abs_efficiencies, "abs_eff")

    header_row[0] = cutflow_name + " - rel eff"
    print tabulate.tabulate(rel_efficiencies, header_row, tablefmt = "rst", numalign = "right", stralign = "left", floatfmt = ".4f")

    if requested_cutflow.make_plots :
        plot_cutflow(header_row, rel_efficiencies, "rel_eff")

def make_cutflow_table(requested_cutflow, backgrounds, signals, data) :

    n_cuts = requested_cutflow.n_cuts

    for bkg in backgrounds :
        bkg.cutflow_result = {} # { cut index : [ yield, stat_err ] }

    for sig in signals :
        sig.cutflow_result = {}

    if data :
        data.cutflow_result = {}

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

        for sig in signals :

            sig_yield = 0.0
            sig_sumw2 = 0.0

            chain = sig.chain()
            for ich, ch in enumerate(chain) :
                weights = ch["eventweight"]
                weights *= ( bkg.scalefactor * np.ones(len(weights)) )
                weights_squared = np.square(weights)

                idx_selection = sample_utils.index_selection_string(requested_cutflow.tcut_at_idx(icut), "ch", requested_cutflow.variable_list)
                set_idx = "indices = np.array( %s )" % idx_selection
                exec(set_idx)

                sig_yield += np.sum(weights[indices])
                sig_sumw2 += np.sum(weights_squared[indices])

            sig.cutflow_result[icut] = [sig_yield, sqrt(sig_sumw2)]

        if data :

            data_yield = 0.0
            data_sumw2 = 0.0

            chain = data.chain()

            for ich, ch in enumerate(chain) :
                weights = ch["eventweight"]
                weights *= ( np.ones(len(weights)) )
                weights_squared = np.square(weights)

                idx_selection = sample_utils.index_selection_string(requested_cutflow.tcut_at_idx(icut), "ch", requested_cutflow.variable_list)
                set_idx = "indices = np.array( %s )" % idx_selection
                exec(set_idx)

                data_yield += np.sum(weights[indices])
                data_sumw2 += np.sum(weights_squared[indices])

            data.cutflow_result[icut] = [data_yield, sqrt(data_sumw2)]

            

    backgrounds += signals

    print_cutflow(requested_cutflow, backgrounds)

    if data :
        requested_cutflow.make_plots = False
        print_cutflow(requested_cutflow, [data])

def main() :
    parser = OptionParser()
    parser.add_option("-r", "--region-name", default = "", help = "Provide a region selection by name")
    parser.add_option("-c", "--config", default = "", help = "Configuration file for plotting")
    parser.add_option("-p", "--plot", default = False, action = "store_true", help = "Make cutflow plots")
    (options, args) = parser.parse_args()
    config = options.config
    region_name = options.region_name
    make_plots = options.plot

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
    requested_cutflow.make_plots = make_plots

    make_cutflow_table(requested_cutflow, backgrounds, signals, data)

#______________________________________________________
if __name__ == "__main__" :
    main()

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
import dantrimania.python.analysis.utility.plotting.m_py.errorbars as errorbars
import dantrimania.python.analysis.utility.utils.plib_utils as plib
from dantrimania.python.analysis.utility.plotting.plot1d import plot1d

# new
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
from dantrimania.python.analysis.utility.plotting.histogram_stack import histogram_stack
from dantrimania.python.analysis.utility.plotting.ratio_canvas import ratio_canvas

plt = plib.import_pyplot()
import numpy as np

def get_samples() :

    sampledir = "./wwbb_samples/"

    wt_dr = sample.Sample("WtDR", "NLO $Wt$ (DR)")
    wt_dr.scalefactor = 36.1
    wt_dr.color = "#121212"
    wt_dr.load_file("%s/wwbb_truth_nomWt_DR.h5" % sampledir)

    wt_ds = sample.Sample("WtDS", "NLO $Wt$ (DS)")
    wt_ds.scalefactor = 36.1
    wt_ds.color = "#d56061"
    wt_ds.load_file("%s/wwbb_truth_nomWt_DS.h5" % sampledir)

    mg5_wtb = sample.Sample("mg5Wtb", "MG5 LO $Wtb$")
    mg5_wtb.scalefactor = 36.1
    mg5_wtb.color = 'b'
    mg5_wtb.load_file("%s/wwbb_truth_single_res.h5" % sampledir)

    return wt_dr, wt_ds, mg5_wtb

def get_variables_from_cut(cutstr) :

    operators = ["==", ">=", "<=", ">", "<", "!=", "*", "-"]
    logics = ["&&", "||", ")", "(", "abs"]
    vars_only = cutstr
    for op in operators :
        vars_only = vars_only.replace(op, " ")
    for log in logics :
        vars_only = vars_only.replace(log, " ")
    vars_only = vars_only.split()
    out = []
    for v in vars_only :
        if v not in out and not v.isdigit() :
            try :
                flv = float(v)
            except :
                out.append(v)

    return out

def get_required_variables(variables, region) :
    out = []
    for v in variables :
        out.append(v)

    cut_vars = get_variables_from_cut(region.tcut)
    for cv in cut_vars :
        if cv not in out :
            out.append(cv)
    out.append("eventweight")
    return out

def make_dr_ds_plot(plot, region, output_dir, sel_string, dr_sample, ds_sample, wtb_sample) :

    canvas = ratio_canvas("ratio_canvas_%s" % plot.name)
    canvas.labels = plot.labels
    canvas.logy = plot.logy
    canvas.x_bounds = plot.bounds[1:]
    canvas.build()
    upper_pad = canvas.upper_pad
    lower_pad = canvas.lower_pad

    okname = plot.vartoplot.replace("abs(","").replace(")","").replace("[","").replace("]","")

    xlow = plot.x_low
    xhigh = plot.x_high
    bin_width = plot.bin_width
    binning = plot.bounds

    histos = []
    weights = []
    labels = []
    colors = []

    
    maxy = 0.0
    samples = [dr_sample, ds_sample, wtb_sample]
    for isample, sample in enumerate(samples) :

        h = histogram1d("histo_%s" % sample.name, binning = binning)

        chain = sample.chain()
        for ich, ch in enumerate(chain) :
            data = ch[plot.vartoplot]
            lumis = sample.scalefactor * np.ones(len(data))
            weights = lumis * ch["eventweight"]
            if plot.absvalue :
                data = np.absolute(data)
            h.fill(data, weights)
        labels.append(sample.displayname)
        colors.append(sample.color)
        h.add_overflow() 
        if h.maximum() > maxy : maxy = h.maximum()
        histos.append(h)

        integral, error = h.integral_and_error()
        print "Counts %s    : %.02f +/- %.02f" % ( sample.name, integral, error )

    miny = 0.0
    if plot.logy :
        miny = 1e-2
    maxy = 1.65 * maxy
    upper_pad.set_ylim(miny, maxy)

    weights = [h.weights for h in histos]
    histo_data = [h.data for h in histos]

    upper_pad.hist( histo_data,
                    weights = weights, 
                    bins = plot.binning,
                    color = colors,
                    label = labels,
                    stacked = False,
                    histtype = 'step',
                    lw = 2,
                    )

    # ratio of DR/DS
    lower_pad.set_ylabel("X / DR", horizontalalignment = 'right', y = 0.83, fontsize = 18)
    lower_pad.set_ylim([0,2])
    dr_histogram = None
    ds_histogram = None
    wtb_histogram = None
    for s in histos :
        if "DR" in s.name :
            dr_histogram = s
        elif "DS" in s.name :
            ds_histogram = s
        elif "Wtb" in s.name :
            wtb_histogram = s
    ratio_y = ds_histogram.divide(dr_histogram)
    ratio_x = np.array(dr_histogram.bin_centers())
    lower_pad.plot(ratio_x, ratio_y, linestyle = 'None', marker = 'o', markersize = 6, color = ds_sample.color, zorder=1000)
    ratio_y = wtb_histogram.divide(dr_histogram)
    lower_pad.plot(ratio_x, ratio_y, linestyle = 'None', marker = 'o', markersize = 6, color = wtb_sample.color, zorder = 1000)

    # legend
    upper_pad.legend(loc = "best", frameon = True, fontsize = 12, numpoints = 1)

    # labels
    opts = dict(transform = upper_pad.transAxes)
    opts.update( dict( va = 'top', ha = 'left' ) )
    upper_pad.text(0.05, 0.97, "ATLAS", size = 18, style = 'italic', weight = 'bold', **opts)
    upper_pad.text(0.23, 0.97, "Work In Progress", size = 18, **opts)
    upper_pad.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, 36.1 fb$^{-1}$', size = 0.75 * 18, **opts)
    upper_pad.text(0.05, 0.83, sel_string, size = 0.75 * 18, **opts)
    
    

    ########
    # save
    utils.mkdir_p(output_dir)
    save_name = output_dir + "/dr_ds_%s_%s.pdf" % (region.name, okname)
    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    canvas.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)


def main() :

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default="./", help = "Set output directory for plots")
    parser.add_option("--logy", default = False, action = "store_true", help = "Set y-axis to log scale")
    parser.add_option("-v", "--var", default = "", help = "Request a specific variable to plot")
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    do_logy = options.logy
    select_var = options.var


    # get Wt samples
    dr_sample, ds_sample, wtb_sample = get_samples()

    # define the region to use
    reg = region.Region("drds", "WW$bb$")
    reg.tcut = "l0_pt>20 && l1_pt>20 && n_bjets>=2 && bj0_pt>20 && bj1_pt>20 && met>200" #mt2_bb>100" 
    #reg.tcut = "l0_pt>20 && l1_pt>20 && n_bjets>=2 && bj0_pt>20 && bj1_pt>20 && mbb<140 && mbb>100 && mt2_llbb>90 && mt2_llbb<140"
    sel_string = '$2b + 2\\ell +$MET$>200$'

    # define variables and plot boundaries
    variables = {}
    variables["mll"] = [20, 0, 400]
    variables["met"] = [20, 200, 600]
    variables["l0_pt"] = [30, 0, 300]
    variables["l1_pt"] = [10, 0, 150]
    variables["ptll"] = [20, 0, 300]
    variables["l0_eta"] = [0.4, -3, 3]
    variables["l1_eta"] = [0.4, -3, 3]
    variables["bj0_pt"] = [40, 0, 800]
    variables["bj1_pt"] = [10, 0, 300]
    variables["bj0_eta"] = [0.4, -3, 3]
    variables["bj1_eta"] = [0.4, -3, 3]
    variables["ht2"] = [60, 0, 2000]
    variables["ht2ratio"] = [0.1, 0, 1]
    variables["dRll"] = [0.4, 0, 5]
    variables["dr_llmet"] = [0.4, 0, 5]
    variables["dr_bb"] = [0.4, 0, 5]
    variables["ptbb"] = [40, 0, 800]
    variables["dphi_llbb"] = [0.4, -3.2, 3.2]
    variables["dphi_llmet_bb"] = [0.4, -3.2, 3.2]
    variables["dphi_l0b0"] = [0.4, -3.2, 3.2]
    variables["sumpt"] = [40, 0, 800]
    variables["mt2_llbb"] = [40, 0, 800]
    variables["mbb"] = [40, 0, 1000]
    variables["mt2_bb"] = [20, 0, 600]

    # ok go
    if select_var != "" :
        if select_var not in variables.keys() :
            print "ERROR requested variable %s not initialized in variables dict" % select_var
            sys.exit()
        tmp_var = {}
        tmp_var[select_var] = variables[select_var]
        variables = tmp_var

    # cache
    cacher = sample_cacher.SampleCacher("./cache")
    cacher.samples = [dr_sample, ds_sample, wtb_sample]
    cacher.region = reg
    required_variables = get_required_variables(variables, reg)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache("truth")

    for var, bounds in variables.iteritems() :
        okname = var.replace("abs(","").replace(")","").replace("[","").replace("]","")
        p = plot1d("%s_%s" % (reg.name, okname), okname)
        p.normalized = False
        p.logy = do_logy
        if 'abs(' in var :
            p.absvalue = True
            var = var.replace("abs(","").replace(")","")
        p.bounds = bounds
        x_label = var
        y_label = "Entries / bin"
        p.labels = [x_label, y_label]
        make_dr_ds_plot(p, reg, output_dir, sel_string, dr_sample, ds_sample, wtb_sample)

if __name__ == "__main__" :
    main()

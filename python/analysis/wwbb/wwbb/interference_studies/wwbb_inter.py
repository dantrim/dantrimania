#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()

import numpy as np

def get_samples() :

    samples = []

    wwbb_sum = sample.Sample("wwbb_sum", "$WWbb$ (sum)")
    wwbb_sum.scalefactor = 36.1
    wwbb_sum.load_file("./wwbb_samples/wwbb_truth_f.h5")
    #wwbb_sum.load_file("./wwbb_samples/wwbb_truth_sum.h5")
    samples.append(wwbb_sum)

    wwbb_double_single = sample.Sample("wwbb_double_single", "$WWbb$ (single+double)")
    wwbb_double_single.scalefactor = 36.1
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_test_dub.h5")
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_double_single_res.h5")
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_nf.h5")
    wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_407326_full_dub_sing.h5")
    samples.append(wwbb_double_single)

    return samples

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

def make_plot(plot, region, samples, output_dir) :

    print 50 * "-"
    print " plotting %s" % plot.vartoplot

    xlow = plot.xlow
    xhigh = plot.xhigh
    bw = plot.binwidth
    nbins = np.arange(xlow, xhigh + bw, bw)

    nfhisto = []
    nfweights = []

    fhisto = []
    fweights = []

    for isample, sample in enumerate(samples) :

        histo = []
        weights = []

        chain = sample.chain()
        for isc, sc in enumerate(chain) :

            # get event weight
            lumis = np.ones(len(sc[plot.vartoplot]))
            lumis[:] = sample.scalefactor
            w = lumis * sc['eventweight'] 
            weights += list(w)

            if plot.absvalue :
                histo += list(np.absolute(sc[plot.vartoplot]))
            else :
                histo += list(sc[plot.vartoplot])

        if "sum" in sample.name :
            fhisto = histo
            fweights = weights
        else :
            nfhisto = histo
            nfweights = weights

    # pads
    upper = plot.upper
    lower = plot.lower

    nfhisto = np.clip(nfhisto, nbins[0], nbins[-1])
    fhisto = np.clip(fhisto, nbins[0], nbins[-1])

    fcounts = 0.0
    nfcounts = 0.0
    for label in ["full", "double+single"] :
        counts = 0.0
        if label == "full" :
            h, _ = np.histogram(fhisto, weights = fweights, bins = nbins)
            counts = sum(h)
            fcounts += counts
        else :
            h, _ = np.histogram(nfhisto, weights = nfweights, bins = nbins)
            counts = sum(h)
            nfcounts += counts
        print "Counts %s : %.2f" % ( label, counts )

    print "Ratio WWbb / (Wtb + ttbar) = %.2f" % (float(fcounts) / float(nfcounts))

    ##########################################################
    # plot double + single
    ##########################################################

    y, x, patches = upper.hist(nfhisto, bins = nbins, color = '#72cff8', weights = nfweights,
                        label = '$t\\bar{t} + Wtb$',
                        histtype = 'stepfilled',
                        lw = 1,
                        edgecolor = 'k', alpha = 1.0)

    total_nf_y = y[-1]
    total_nf_x = x
    maxy = max(y)

    y, x, patches = upper.hist(fhisto, bins = nbins, color = '#d81b39', weights = fweights,
                        label = '$WWbb$ LO',
                        histtype = 'step',
                        lw = 1,
                        ls = '--')

    total_f_y = y[-1]
    total_f_x = x

    # scale the axes to fit everything
    if max(y) > maxy : maxy = max(y)
    max_mult = 1.5
    if plot.logy :
        max_mult = 10000
    maxy = max_mult * maxy
    upper.set_ylim(plot.ylow, maxy)

    # legend
    upper.legend(loc='best', frameon = False, fontsize=12, numpoints=1)


    ##########################################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "wwbb_interf_%s_%s.pdf" % ( region.name, plot.vartoplot )

    print " >>> saving plot to : %s" % os.path.abspath(save_name)
    plot.fig.savefig(save_name, bbox_inches = 'tight', dpi=200)
    


def main() :

    print "WWbb interference"

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default="./", help="Set output directory for plots")
    parser.add_option("--logy", default=False, action="store_true", help="Set y-axis to log scale")
    parser.add_option("-v", "--var", default="", help="Request a specific variable to plot")
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    do_logy = options.logy
    select_var = options.var

    samples = get_samples()

    # region
    reg = region.Region("wwbb", "WW$bb$")
    reg.tcut = "mll>20 && l0_pt>25 && l1_pt>20 && n_bjets==2 && bj0_pt>20 && bj1_pt>20 && met>200"



    # variables
    variables = {}
    variables["mll"] = [20, 0, 400]
    variables["met"] = [10, 0, 800]
    variables["l0_pt"] = [30, 0, 600]
    variables["l1_pt"] = [10, 0, 300]
    variables["ptll"] = [40, 0, 2000]
    variables["l0_eta"] = [0.2, -3, 3]
    variables["l1_eta"] = [0.2, -3, 3]
    variables["bj0_pt"] = [40, 0, 1000]
    variables["bj1_pt"] = [10, 0, 300]
    variables["bj0_eta"] = [0.2, -3, 3]
    variables["bj1_eta"] = [0.2, -3, 3]
    variables["ht2"] = [40, 0, 2500]
    variables["ht2ratio"] = [0.1, 0, 1]
    variables["dRll"] = [0.2, 0, 5]
    variables["dr_llmet"] = [0.2, 0, 5]
    variables["dr_bb"] = [0.2, 0, 5]
    variables["ptbb"] = [30, 0, 3000]
    variables["dphi_llbb"] = [0.2, -3.2, 3.2]
    variables["dphi_llmet_bb"] = [0.2, -3.2, 3.2]
    variables["dphi_l0b0"] = [0.2, -3.2, 3.2]
    variables["sumpt"] = [40, 0, 6000]
    variables["mt2_llbb"] = [40, 0, 2000]
    variables["mt2_bb"] = [40, 0, 2000]

    if select_var != "" :
        if select_var not in variables.keys() :
            print "ERROR Requested variable %s not initialized" % select_var
            sys.exit()
        tmp_var = {}
        tmp_var[select_var] = variables[select_var]
        variables = tmp_var

    nice_names = {}
    nice_names = ["$m_{\\ell \\ell} [GeV]", "GeV"]

    # cache
    cacher = sample_cacher.SampleCacher("./cache")
    cacher.samples = samples
    cacher.region = reg
    required_variables = get_required_variables(variables.keys(), reg)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache("truth")

    for var, bounds in variables.iteritems() :
        p = hist1d.RatioCanvas(logy = do_logy)
        if "abs(" in var :
            var = var.replace("abs(","").replace(")", "")
            p.absvalue = True
        p.vartoplot = var
        p.bounds = bounds
        name = var.replace("[","").replace("]","").replace("(","").replace(")","")
        p.name = name
        y_label_unit = ""
        if var in nice_names :
            if len(nice_names[var]) == 2 :
                y_label_unit = nice_names[var][1]
        y_label_unit = str(bounds[0]) + " " + y_label_unit
        x_label = var
        y_label = "Events / %s" % y_label_unit
        if var in nice_names :
            x_label = nice_names[var][0]
        p.labels = [x_label, y_label]

        p.logy = do_logy
        p.build_ratio()

        # make the plot
        make_plot(p, reg, samples, output_dir)

#_______________________________________________________________
if __name__ == "__main__" :
    main()

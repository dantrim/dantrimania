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
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()

import numpy as np

def get_samples() :

    samples = []

    wwbb_sum = sample.Sample("wwbb_sum", "$WWbb$ (sum)")
    wwbb_sum.scalefactor = 36.1
    #wwbb_sum.load_file("./wwbb_samples/wwbb_truth_f.h5")
    #wwbb_sum.load_file("./wwbb_samples/wwbb_truth_sum.h5")
    wwbb_sum.load_file("./wwbb_samples/wwbb_truth_sum.h5")
    samples.append(wwbb_sum)

    wwbb_double_single = sample.Sample("wwbb_double_single", "$WWbb$ (single+double)")
    wwbb_double_single.scalefactor = 36.1
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_test_dub.h5")
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_double_single_res.h5")
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_nf.h5")
    #wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_407326_full_dub_sing.h5")
    wwbb_double_single.load_file("./wwbb_samples/wwbb_truth_dub_sing.h5")
    samples.append(wwbb_double_single)

    wwbb_single = sample.Sample("wwbb_single_res", "$Wtb$")
    wwbb_single.scalefactor = 36.1
    wwbb_single.load_file("./wwbb_samples/wwbb_truth_single_res.h5")

    wwbb_double = sample.Sample("wwbb_double_res", "$t\\bar{t}$")
    wwbb_double.scalefactor = 36.1
    wwbb_double.load_file("./wwbb_samples/wwbb_truth_double_res.h5")
    

    return samples, wwbb_sum, wwbb_single, wwbb_double

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

    shistos = []
    sweights = []

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
        elif "single_res" in sample.name :
            shisto = histo
            sweights = weights
        else :
            nfhisto = histo
            nfweights = weights

    # pads
    upper = plot.upper
    lower = plot.lower

    nfhisto = np.clip(nfhisto, nbins[0], nbins[-1])
    fhisto = np.clip(fhisto, nbins[0], nbins[-1])
    shisto = np.clip(shisto, nbins[0], nbins[-1])

    fcounts = 0.0
    nfcounts = 0.0
    scounts = 0.0
    for label in ["full", "double+single", "single"] :
        counts = 0.0
        if label == "full" :
            h, _ = np.histogram(fhisto, weights = fweights, bins = nbins)
            counts = sum(h)
            fcounts += counts
        elif label ==  "double+single" :
            h, _ = np.histogram(nfhisto, weights = nfweights, bins = nbins)
            counts = sum(h)
            nfcounts += counts
        elif label == "single" :
            h, _ = np.histogram(shisto, weights = sweights, bins = nbins)
            counts = sum(h)
            scounts += counts
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

    y, x, patches = upper.hist(shisto, bins = nbins, color = 'k', weights = sweights,
                        label = 'Wtb',
                        histtype = 'step',
                        lw = 1,
                        ls = '--')
    total_s_y = y[-1]
    total_s_x = x

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

def get_counts(sum_sample, single_sample, double_sample, region) :

    xlow = 0
    xhigh = 1.2
    nbins = np.arange(xlow, xhigh, 0.1)

    binning = [0.1, 0, 1.2]

    h_sum = histogram1d("histo_sum", binning = binning)
    chain_sum = sum_sample.chain()
    for ic, c in enumerate(chain_sum) :
        lumis = sum_sample.scalefactor * np.ones(len(c["ht2ratio"]))
        weights = lumis * c['eventweight']
        hist_data = c['ht2ratio']
        h_sum.fill(hist_data, weights)
    sum_counts, sum_error = h_sum.integral_and_error()

    h_single = histogram1d("histo_single", binning = binning)
    chain_single = single_sample.chain()
    for ic, c in enumerate(chain_single) :
        lumis = single_sample.scalefactor * np.ones(len(c["ht2ratio"]))
        weights = lumis * c['eventweight']
        hist_data = c['ht2ratio']
        h_single.fill(hist_data, weights)
    single_counts, single_error = h_single.integral_and_error()
    

    h_double = histogram1d("histo_double", binning = binning)
    chain_double = double_sample.chain()
    for ic, c in enumerate(chain_double) :
        lumis = double_sample.scalefactor * np.ones(len(c["ht2ratio"]))
        weights = lumis * c['eventweight']
        hist_data = c['ht2ratio']
        h_double.fill(hist_data, weights)
    double_counts, double_error = h_double.integral_and_error()

    print "WWbb  (sum)          : %.02f +/- %.02f" % ( sum_counts, sum_error )
    print "ttbar (double res)   : %.02f +/- %.02f" % ( double_counts, double_error )
    print "Wtb   (single res)   : %.02f +/- %.02f" % ( single_counts, single_error )

    # calc option 1
    option1 = ( sum_counts - double_counts )
    option1 = float(option1) / float(single_counts)
    option1 = (1.0 - option1)

    # calc option 2
    option2 = ( sum_counts - double_counts - single_counts )
    option2 = float(option2) / float(sum_counts)
    
    print 25 * '- '
    print "option1 [ 1 - (WWbb - ttbar) / Wtb ] : %.02f" % option1
    print "option2 [ WWbb - ttbar - Wtb ]       : %.02f" % option2 
    


def main() :

    print "WWbb interference"

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default="./", help="Set output directory for plots")
    parser.add_option("-c", "--counts", default=False, action = "store_true", help = "Calculate WWbb, ttbar, Wtb counts")
    parser.add_option("--logy", default=False, action="store_true", help="Set y-axis to log scale")
    parser.add_option("-v", "--var", default="", help="Request a specific variable to plot")
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    do_logy = options.logy
    select_var = options.var
    do_counts = options.counts

    samples, sum_sample, single_sample, double_sample = get_samples()
    samples.append(single_sample)

    # region
    reg = region.Region("wwbb", "WW$bb$")
#%s && nBJets==2 && mll>20 && mbb>140 && dRll>1.5 && dRll<3.0 && HT2Ratio>0.5 && mt2_bb>150
    #reg.tcut = "mll>20 && l0_pt>25 && l1_pt>20 && n_bjets==2 && bj0_pt>20 && bj1_pt>20"# && met>200"
    reg.tcut = "mll>20 && l0_pt>20 && l1_pt>10 && n_bjets==2 && bj0_pt>20 && bj1_pt>20 && met>200"# && mbb>140 && dRll>1.5 && dRll<3.0 && ht2ratio>0.5"# && met>200"

    # variables
    variables = {}
    variables["mll"] = [20, 0, 400]
    variables["met"] = [10, 0, 800]
    variables["l0_pt"] = [30, 0, 600]
    variables["l1_pt"] = [10, 0, 300]
    variables["ptll"] = [20, 0, 500]
    variables["l0_eta"] = [0.2, -3, 3]
    variables["l1_eta"] = [0.2, -3, 3]
    variables["bj0_pt"] = [40, 0, 1000]
    variables["bj1_pt"] = [10, 0, 300]
    variables["bj0_eta"] = [0.2, -3, 3]
    variables["bj1_eta"] = [0.2, -3, 3]
    variables["ht2"] = [30, 0, 1500]
    variables["ht2ratio"] = [0.1, 0, 1]
    variables["dRll"] = [0.2, 0, 5]
    variables["dr_llmet"] = [0.2, 0, 5]
    variables["dr_bb"] = [0.2, 0, 5]
    variables["ptbb"] = [20, 0, 1000]
    variables["dphi_llbb"] = [0.2, -3.2, 3.2]
    variables["dphi_llmet_bb"] = [0.2, -3.2, 3.2]
    variables["dphi_l0b0"] = [0.2, -3.2, 3.2]
    variables["sumpt"] = [40, 0, 2000]
    variables["mt2_llbb"] = [20, 0, 1000]
    variables["mt2_bb"] = [20, 0, 500]

    if not do_counts :

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

    elif do_counts :
        cacher_counts = sample_cacher.SampleCacher("./cache")
        reg.name = "%s_counts" % reg.name
        cacher_counts.region = reg
        cacher_counts.samples = [sum_sample, single_sample, double_sample]
        required_variables = get_required_variables(variables.keys(), reg)
        cacher_counts.fields = required_variables
        print str(cacher_counts)
        cacher_counts.cache("truth")

        for var, bounds in variables.iteritems() :
            if var != "ht2ratio" : continue
            get_counts(sum_sample, single_sample, double_sample, reg)


#_______________________________________________________________
if __name__ == "__main__" :
    main()

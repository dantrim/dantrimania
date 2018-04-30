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
from math import sqrt

from matplotlib.lines import Line2D
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

def draw_ratio_error_bars(h_den, h_num, pad, color) :

    yvalues = h_num.divide(h_den)
    xvalues = np.array(h_den.bin_centers())
    yvalues [ yvalues == 0 ] = -10

    err_num = np.array(h_num.y_error())
    vals_num = h_num.histogram
    err_num = np.divide(err_num, vals_num)

    err_den = np.array(h_den.y_error())
    vals_den = h_den.histogram
    err_den = np.divide(err_den, vals_den)

    ratio_errors = yvalues * np.sqrt( err_num ** 2 + err_den ** 2)

    pad.errorbar(xvalues, yvalues, yerr = ratio_errors, fmt = 'none', color = color)

def make_plot(plot, region, samples, output_dir, sel_string, sel_string2) :

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

    histos_for_errorbars = {}

    # pads
    upper = plot.upper
    lower = plot.lower


    for isample, sample in enumerate(samples) :

        histo = []
        weights = []

        h = histogram1d("histo_%d" % isample, binning = [bw, xlow, xhigh])

        chain = sample.chain()
        for isc, sc in enumerate(chain) :

            # get event weight
            lumis = np.ones(len(sc[plot.vartoplot]))
            lumis[:] = sample.scalefactor
            w = lumis * sc['eventweight'] 
            weights += list(w)

            data = sc[plot.vartoplot]

            if plot.absvalue :
                data = np.absolute(data)
            histo += list(data)

            data = np.clip(data, nbins[0],  nbins[-1])

            h.fill(data, w)

        if "sum" in sample.name :
            fhisto = histo
            fweights = weights
            fhisto = np.clip(fhisto, nbins[0], nbins[-1])
            histos_for_errorbars["fhisto"] = h
            draw_histo_errors(h, "#d81b39", upper)
        elif "single_res" in sample.name :
            shisto = histo
            sweights = weights
            shisto = np.clip(shisto, nbins[0], nbins[-1])
            histos_for_errorbars["shisto"] = h
            draw_histo_errors(h, "k", upper)
        elif "double_single" in sample.name:
            nfhisto = histo
            nfweights = weights
            nfhisto = np.clip(nfhisto, nbins[0], nbins[-1])
            histos_for_errorbars["nfhisto"] = h
            draw_histo_errors(h, "b", upper)



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

    y, x, patches = upper.hist(nfhisto, bins = nbins, color = '#73c2fb', weights = nfweights,
                        label = '$t\\bar{t} + Wtb$',
                        histtype = 'stepfilled',
                        lw = 1,
                        edgecolor = 'k', alpha = 1.0)

    total_nf_y = y
    total_nf_x = x
    maxy = max(y)

    y, x, patches = upper.hist(fhisto, bins = nbins, color = '#d81b39', weights = fweights,
                        label = '$WWbb$ LO',
                        histtype = 'step',
                        lw = 1,
                        ls = '--')

    total_f_y = y
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

    miny = 0
    max_mult = 1.5
    if plot.logy :
        max_mult = 1e2
        miny = 1e-2
    maxy = max_mult * maxy
    upper.set_ylim(miny, maxy)


    # legend
    colors = {}
    handles, labels = upper.get_legend_handles_labels()
    order = ["$WWbb$ LO", "$t\\bar{t} + Wtb$", "Wtb"]
    colororder = ["#d81b39", "#73c2fb", "k"]
    new_handles = []
    new_labels = []
    for iorder, ordername in enumerate(order) :
        for ilabel, label in enumerate(labels) :
            if ordername != label : continue
            new_labels.append(label)
            if "WWbb" in ordername :
                new_handles.append(Line2D([], [], c = colororder[iorder]))
            elif "+ Wtb" in ordername :
                new_handles.append(Line2D([], [], c = colororder[iorder]))
            elif "Wtb" in ordername and "+" not in ordername :
                new_handles.append(Line2D([], [], c = colororder[iorder], ls = '--'))

    upper.legend(handles = new_handles, labels = new_labels, loc = 'best', frameon = False, fontsize = 12, numpoints = 1)

    ##############
    # ratio
    ratio_x = [x + 0.5 * bw for x in total_f_x[:-1]]
    ratio_y = total_f_y
    ratio_y_den = total_nf_y
    for i in range(len(ratio_y)) :
        if ratio_y_den[i] == 0 :
            ratio_y[i] = -10
            continue
        ratio_y[i] = float(ratio_y[i] / ratio_y_den[i])
    lower.set_ylim([0,2])
    lower.set_ylabel("WWbb / $t \\bar{t}$ + W$t$b", horizontalalignment = 'right', y = 1.2, fontsize = 16)
    lower.plot(ratio_x, ratio_y, 'ro', zorder=1000, markersize=3)

    draw_ratio_error_bars(histos_for_errorbars['nfhisto'], histos_for_errorbars['fhisto'], lower, 'r')

    # line
    line_x = [xlow, xhigh]
    line_y = [1, 1]
    lower.plot(line_x, line_y, 'r--', zorder = 0)

    ####
    # labels
    opts = dict(transform = upper.transAxes)
    opts.update( dict( va = 'top', ha = 'left' ) )
    upper.text(0.05, 0.97, "ATLAS", size = 18, style = 'italic', weight = 'bold', **opts)
    upper.text(0.23, 0.97, "Work In Progress", size = 18, **opts)
    upper.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, 36.1 fb$^{-1}$', size = 0.75 * 18, **opts)
    upper.text(0.05, 0.83, sel_string, size = 0.75 * 18, **opts)
    if sel_string2 != "" :
        upper.text(0.05, 0.77, "+ %s" % sel_string2, size = 0.75 * 18, **opts)

    ##########################################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "wwbb_interf_%s_%s.pdf" % ( region.name, plot.vartoplot )

    print " >>> saving plot to : %s" % os.path.abspath(save_name)
    plot.fig.savefig(save_name, bbox_inches = 'tight', dpi=200)

def draw_histo_errors(histogram, color, pad) :

    yvals = histogram.histogram
    xvals = histogram.bin_centers()
    yerr = histogram.y_error()
    pad.errorbar(xvals, yvals, yerr = yerr, fmt = 'none', color = color)
    
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
    #print "adding acceptance hack"
    #double_counts = (double_counts / 0.15)
    #single_counts = (single_counts / 0.27)
    #sum_counts = (sum_counts / 0.21)
    option1 = ( sum_counts - double_counts )
    error = sqrt( sum_error * sum_error + double_error * double_error )
    option1_new = float(option1) / float(single_counts)
    error = option1_new * sqrt( (error/option1) * (error/option1) + (single_error/single_counts) * (single_error/single_counts) )
    option1 = option1_new
    option1 = (1.0 - option1)

    # calc option 2
    option2 = ( sum_counts - double_counts - single_counts )
    option2 = float(option2) / float(sum_counts)
    
    print 25 * '- '
    print "option1 [ 1 - (WWbb - ttbar) / Wtb ] : %.02f +/- %.02f" % ( option1, abs(error) )
    #print "option2 [ WWbb - ttbar - Wtb ]       : %.02f" % option2 
    


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
    reg.tcut = "l0_pt>20 && l1_pt>10 && n_bjets==2 && bj0_pt>20 && bj1_pt>20 && mbb>100 && mbb<140" #&& mt2_llbb>90 && mt2_llbb<140 && ht2ratio>0.8 && dRll<0.9 && mt2_bb>150"# && met>200"# && mbb>140 && dRll>1.5 && dRll<3.0 && ht2ratio>0.5"# && met>200"
    sel_string = "$2\\ell + 2b +$MET200 $+m_{bb}\\in(100,140)$" 
    sel_string2 = ""
    #sel_string2 = "$\\Delta R_{\\ell \ell}<1.0$"

    # variables
    variables = {}
    #variables["mll"] = [20, 0, 400]
    #variables["met"] = [10, 200, 600]
    #variables["l0_pt"] = [30, 0, 600]
    #variables["l1_pt"] = [10, 0, 300]
    #variables["ptll"] = [20, 0, 500]
    #variables["l0_eta"] = [0.2, -3, 3]
    #variables["l1_eta"] = [0.2, -3, 3]
    #variables["bj0_pt"] = [25, 0, 500]
    #variables["bj1_pt"] = [10, 0, 200]
    #variables["bj0_eta"] = [0.2, -3, 3]
    #variables["bj1_eta"] = [0.2, -3, 3]
    #variables["ht2"] = [30, 0, 1500]
    #variables["ht2ratio"] = [0.1, 0, 1]
    #variables["dRll"] = [0.2, 0, 5]
    #variables["dr_llmet"] = [0.2, 0, 5]
    #variables["dr_bb"] = [0.2, 0, 5]
    #variables["ptbb"] = [20, 0, 1000]
    #variables["dphi_llbb"] = [0.2, -3.2, 3.2]
    #variables["dphi_llmet_bb"] = [0.2, -3.2, 3.2]
    #variables["dphi_l0b0"] = [0.2, -3.2, 3.2]
    #variables["sumpt"] = [40, 0, 2000]
    #variables["mt2_llbb"] = [20, 0, 1000]
    #variables["mt2_bb"] = [20, 0, 500]
    #variables["mbb"] = [40, 0, 1000]

    #inside mbb window 
    variables["mll"] = [40, 0, 800]
    variables["met"] = [20, 200, 700]
    variables["l0_pt"] = [50, 0, 800]
    variables["l1_pt"] = [10, 0, 250]
    variables["ptll"] = [40, 0, 600]
    variables["l0_eta"] = [0.6, -3, 3]
    variables["l1_eta"] = [0.6, -3, 3]
    variables["bj0_pt"] = [50, 0, 800]
    variables["bj1_pt"] = [20, 0, 200]
    variables["bj0_eta"] = [0.5, -3, 3]
    variables["bj1_eta"] = [0.5, -3, 3]
    variables["ht2"] = [120, 0, 1200]
    variables["ht2ratio"] = [0.1, 0.0, 1]
    variables["dRll"] = [0.5, 0, 5.0]
    variables["dr_llmet"] = [0.5, 0, 5]
    variables["dr_bb"] = [0.5, 0, 6]
    variables["ptbb"] = [20, 0, 600]
    variables["dphi_llbb"] = [0.6, -3.2, 3.2]
    variables["dphi_llmet_bb"] = [0.6, -3.2, 3.2]
    variables["dphi_l0b0"] = [0.6, -3.2, 3.2]
    variables["sumpt"] = [80, 0, 2000]
    variables["mt2_llbb"] = [40, 80, 1000]
    variables["mt2_bb"] = [40, 0, 600]
    variables["mbb"] = [5, 100, 140]

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

        n_var = len(variables)
        n_at = 1

        for var, bounds in variables.iteritems() :
            print "[%02d/%02d] %s" % (n_at, n_var, var)
            n_at += 1
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
            make_plot(p, reg, samples, output_dir, sel_string, sel_string2)

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

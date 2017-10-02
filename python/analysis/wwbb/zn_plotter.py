#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.plotting.m_py.errorbars as errorbars
import dantrimania.python.analysis.utility.plotting.m_py.hist_utils as hist_utils
import dantrimania.python.analysis.utility.stats.significance as significance
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()

import numpy as np

def make_zn_plot(plot, region, backgrounds, signals, rel_unc, output_dir) :

    print 50 * "-"

    xlow = plot.xlow
    xhigh = plot.xhigh
    bw = plot.binwidth
    nbins = np.arange(xlow, xhigh + bw, bw)

    # group histos
    bkg_histos = []
    sumw2_histos = []

    weights = {}
    weights2 = []

    colors = {}
    labels = []

    for ibkg, bkg in enumerate(backgrounds) :

        # histogram data for this process
        histogram = []
        sumw2_histogram = []

        # loop over the 'chain'
        chain = bkg.chain()
        bkg_weights = []
        bkg_weights2 = []
        for ibc, bc in enumerate(chain) :

            lumis = np.ones(len(bc[plot.vartoplot]))
            lumis[:] = bkg.scalefactor
            w = lumis * bc['eventweight']
            bkg_weights += list(w)

            w2 = lumis * bc['eventweight']
            w2 = w2 ** 2
            bkg_weights2 += list(w2)

            data = bc[plot.vartoplot]
            if plot.absvalue :
                data = np.absolute(data)
            histogram += list(data)
            sumw2_histogram += list(data)

        labels.append(bkg.name)
        colors[bkg.name] = bkg.color

        bkg_histos.append(histogram)
        sumw2_histos.append(sumw2_histogram)

        weights[bkg.name] = bkg_weights
        weights2.append(bkg_weights2)

    counts_map = {}
    for ilabel, label in enumerate(labels) :
        counts_map[sum(bkg_histos[ilabel])] = label
    bkg_histos = sorted(bkg_histos, key = lambda x : sum(x), reverse = False)

    ordered_labels = []
    ordered_weights = []
    ordered_colors = []

    for bhisto in bkg_histos :
        idx = sum(bhisto)
        ordered_labels.append(counts_map[idx])
        ordered_weights.append(weights[counts_map[idx]])
        ordered_colors.append(colors[counts_map[idx]])

    labels = ordered_labels
    weights = ordered_weights
    colors = ordered_colors

    # pads
    upper = plot.upper
    middle = plot.middle
    lower = plot.lower

    #################################################################
    # upper pad

    # add overflow bin
    bkg_histos = [np.clip(b, nbins[0], nbins[-1]) for b in bkg_histos]
    for ib, b in enumerate(bkg_histos) :
        hb, _ = np.histogram(b, weights = weights[ib], bins = nbins)
        print "Counts %s : %.2f" % (labels[ib], sum(hb))
    y, x, _ = upper.hist(bkg_histos, bins = nbins,
                        color = colors,
                        weights = weights,
                        label = labels,
                        stacked = True,
                        histtype = 'stepfilled',
                        lw = 1,
                        edgecolor = 'k',
                        alpha = 1.0)

    # determine the max of the y-axis
    total_sm_y = y[-1]
    total_sm_x = x
    maxy = max(total_sm_y)
    multiplier = 1.65
    if len(signals) :
        multiplier = 1.8
    if plot.logy :
        multiplier = 1e4
        if len(signals) :
            multiplier = 1e5

    # draw MC stat uncertainty hatches
    histo_w2 = np.ones(len(nbins[:-1]))
    for iw, w in enumerate(sumw2_histos) :
        h_err, _ = np.histogram(w, bins = nbins, weights = weights2[iw])
        histo_w2 += h_err
    yerr = np.sqrt(histo_w2)
    xerr = [plot.binwidth + 0.5 for a in x]
    stat_error_hatches = errorbars.error_hatches( x, total_sm_y, xerr, yerr, plot.binwidth )
    upper.add_collection(stat_error_hatches)

    # draw total SM line
    hist_utils.draw_bounding_line(upper, total_sm_x[:-1], total_sm_y, plot.binwidth)

    # draw signal histos
    signal_labels = []
    signal_colors = []
    if len(signals) > 0  :
        signal_labels, signal_colors, signal_sy, signal_sx = hist_utils.overlay_histos(pad = upper,
                                        samples = signals,
                                        variable_name = plot.vartoplot,
                                        bins = nbins,
                                        absvalue = plot.absvalue)

    #################################################################
    # middle, signifance going right
    middle.set_ylabel("Z $\\downarrow$", fontsize = 18)
    middle.set_ylim(0, 3)

    maxz = 3
    for isample, signal in enumerate(signals) :
        sig_values_y = []
        for ix in range(len(total_sm_x)) : # loop over the bins in the histogram
            b = sum( [sm for sm in total_sm_y[ix : -1]] )
            s = sum( [bc for bc in signal_sy[isample][ix : -1]] )
            #b = sum( [sm for sm in total_sm_y[:ix+1]] )
            #s = sum( [bc for bc in signal_sy[isample][:ix+1]] )
            zn = significance.binomial_exp_z(s, b, rel_unc)
            sig_values_y.append(zn)
            if zn > maxz : maxz = zn
        middle.plot(total_sm_x + 0.5 * plot.binwidth, sig_values_y, markerfacecolor = signal.color,
                                    marker = '>',
                                    markeredgecolor = signal.color,
                                    linestyle = 'None',
                                    markersize = 4)
    if maxz > 5 :
        maxz = 5
    middle.set_ylim(0, maxz + 0.2)

    #################################################################
    # lower, signifcance going left
    lower.set_ylabel("Z $\\uparrow$", fontsize = 18)
    lower.set_ylim(0, 3)

    maxz = 3
    for isample, signal in enumerate(signals) :
        sig_values_y = []
        #print "x values = %s" % total_sm_x
        for ix in range(len(total_sm_x)) : # loop over the bins in the histogram
            #b = sum( [sm for sm in total_sm_y[ix : -1]] )
            #s = sum( [bc for bc in signal_sy[isample][ix : -1]] )
            b = sum( [sm for sm in total_sm_y[:ix+1]] )
            s = sum( [bc for bc in signal_sy[isample][:ix+1]] )
            zn = significance.binomial_exp_z(s, b, rel_unc)
            #print " x >= %.2f (s, b) = (%.2f, %.2f) -> z = %.5f" % ( total_sm_x[ix], s, b, zn )
            sig_values_y.append(zn)
            if zn > maxz : maxz = zn
        lower.plot(total_sm_x + 0.5 * plot.binwidth, sig_values_y,
                    markerfacecolor = signal.color,
                    marker = '<',
                    markeredgecolor = signal.color,
                    linestyle = 'None',
                    markersize = 4)
    if maxz > 5 :
        maxz = 5
    lower.set_ylim(0, maxz + 0.2)

    

    ## draw exclusion threshold
    for pad in [middle, lower] :
        xl = np.linspace(xlow, xhigh, 20)
        yl = np.ones(len(xl)) * 1.64
        pad.plot(xl, yl, 'r--', zorder = 0, alpha = 0.6)
    


    ####################################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "zn_plot_%s_%s.pdf" % ( region.name, plot.vartoplot)

    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    plot.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)
    print 40 * "-"

def main() :

    parser = OptionParser()
    parser.add_option("-c", "--config", default = "", help = "Configuration file for samples, regions, plots")
    parser.add_option("-r", "--region", default = "", help = "Provide a region selection")
    parser.add_option("-o", "--output", default = "./", help = "Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("-v", "--var", default = "", help = "Provide a specific variable to plot")
    parser.add_option("-e", "--error", default = 0.3, help = "Relative uncertainty on background") 
    parser.add_option("--logy", default = False, action = "store_true", help = "Set plots to have log y-axis")
    parser.add_option("--cache-dir", default = "./sample_cache", help = "Directry to place/look for the cached samples")
    (options, args) = parser.parse_args()
    config = options.config
    select_region = options.region
    output_dir = options.output
    select_var = options.var
    rel_unc = options.error
    do_logy = options.logy
    cache_dir = options.cache_dir

    print " * zn_plotter * "

    if not utils.file_exists(config) :
        sys.exit()

    global loaded_samples
    global loaded_regions
    global selected_region
    global loaded_plots
    global additional_variables
    selected_region = select_region
    loaded_samples = []
    loaded_regions = []
    loaded_plots = []
    additional_variables = []
    execfile(config, globals(), locals())

    if len(loaded_samples) == 0 :
        print "ERROR No loaded samples found in configuration"
        sys.exit()

    if not region_utils.regions_unique(loaded_regions) :
        print "ERROR Loaded regions are not unique, here are the counts:"
        for rname, count in region_utils.region_counts(loaded_regions).iteritems() :
            print " > %s : %d" % (rname, count)
        sys.exit()

    if not region_utils.has_region(loaded_regions, selected_region) :
        print "ERROR Requested region (=%s) not found in loaded regions:" % ( selected_region )
        for r in loaded_regions :
            print str(r)
        sys.exit()

    backgrounds, signals, _ = sample_utils.categorize_samples(loaded_samples)

    region_to_plot = None
    for r in loaded_regions :
        if r.name == selected_region :
            region_to_plot = r
            break

    variables_found = []
    for p in loaded_plots :
        variables_found.append(p.vartoplot)
    if select_var != "" :
        if select_var not in variables_found :
            print "ERROR Requested variable (=%s) not found in configured plots" % select_var
            sys.exit()
    tmp_plots = []
    if select_var != "" :
        for p in loaded_plots :
            if p.vartoplot == select_var :
                tmp_plots.append(p)
        loaded_plots = tmp_plots

    # cache
    cacher = sample_cacher.SampleCacher(cache_dir)
    cacher.samples = loaded_samples
    cacher.region = region_to_plot
    required_variables = sample_utils.get_required_variables(loaded_plots, region_to_plot)
    for av in additional_variables :
        if av not in required_variables :
            required_variables.append(av)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for plot in loaded_plots :
        make_zn_plot(plot, region_to_plot, backgrounds, signals, rel_unc, output_dir)

#_____________________________________________________________________________
if __name__ == "__main__" :
    main()

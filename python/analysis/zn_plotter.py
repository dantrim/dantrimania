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

# new
from dantrimania.python.analysis.utility.plotting.histogram_stack import histogram_stack
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
from dantrimania.python.analysis.utility.plotting.double_ratio_canvas import double_ratio_canvas

plt = plib.import_pyplot()
import numpy as np

##############################################################################
def make_legend(ordered_labels, pad) :

    handles, labels = pad.get_legend_handles_labels()
    new_handles = []
    new_labels = []
    for l in ordered_labels :
        for il, label in enumerate(labels) :
            if label == l :
                new_labels.append(l.replace('SIG', ''))
                new_handles.append(handles[il])

    leg_x, leg_y = 0.5, 0.85
    pad.legend(new_handles, new_labels,
            loc = (leg_x, leg_y),
            frameon = False,
            ncol = 2,
            fontsize = 12,
            numpoints = 1,
            labelspacing = 0.2,
            columnspacing = 0.4)

    return leg_x, leg_y

##############################################################################
def make_signal_legend(labels, colors, coords = [], pad = None) :

    handles, leg_labels = pad.get_legend_handles_labels()
    sig_handles = []
    sig_labels = []

    for l in labels :
        for il, ll in enumerate(leg_labels) :
            if l == ll :
                sig_handles.append(handles[il])
                sig_labels.append(l.replace('SIG',''))
    y_vals = []
    for il, l in enumerate(sig_labels) :
        y = coords[1] - 0.04 * (1.1*il+1)
        y_vals.append(y)
        pad.text(coords[0]+ 0.1, y, l,
                transform = pad.transAxes,
                fontsize = 12,
                ha = 'left')

    y_offset = 1.02
    for iy, y in enumerate(y_vals) :
        pad.plot([coords[0] + 0.007, coords[0] + 0.08],
            [y_offset * y, y_offset * y],
            '--',
            lw = 1.5,
            color = colors[iy],
            transform = pad.transAxes)

##############################################################################
def add_labels(pad, region_name = "", lumi = 36.1) : # lumi in fb

    # ATLAS label
    size = 18
    text = 'ATLAS'
    opts = dict(transform = pad.transAxes)
    opts.update( dict( va = 'top', ha = 'left') )
    pad.text(0.05, 0.97, text, size = size, style = 'italic', weight = 'bold', **opts)

    what_kind = 'Internal'
    pad.text(0.23, 0.97, what_kind, size = size, **opts)

    # lumi stuff
    pad.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, %s fb$^{-1}$' % (str(lumi)), size = 0.75 * size, **opts)

    # region
    pad.text(0.047, 0.83, region_name, size = 0.75 * size, **opts)

##############################################################################
def draw_signal_histos(pad = None, samples = [], variable = "", bins = [], binning = [], absvalue = False) :

    histograms_sig = []
    colors = []
    labels = []

    for sample in samples :
        h = histogram1d('histo_%s' % sample.name, binning = binning) 
        chain = sample.chain()
        for ic, c in enumerate(chain) :

            # get data
            hist_data = c[variable]

            # get weights
            lumis = sample.scalefactor * np.ones(len(hist_data))
            weights = lumis * c['eventweight']

            if absvalue :
                hist_data = np.absolute(hist_data)

            # fill
            h.fill(hist_data, weights)

        # overflow
        h.add_overflow()

        labels.append(sample.displayname)
        colors.append(sample.color)

        histograms_sig.append(h)

    histos = [h.data for h in histograms_sig]
    weights = [h.weights for h in histograms_sig]
    sy, sx, _ = pad.hist( histos, bins = bins,
                    color = colors,
                    weights = weights,
                    label = labels,
                    ls = '--',
                    stacked = False,
                    histtype  = 'step',
                    lw = 1.5)

    print 15 * '- '
    for isignal, histo in enumerate(histograms_sig) :
        print histo.count_str(name=samples[isignal].name)

    return labels, colors, sy, sx

        




##############################################################################
def make_zn_plot(plot, region_to_plot, bkgs, sigs, rel_unc, output_dir, lumi_val) :

    print 50 * '-'

    # canvas
    canvas = double_ratio_canvas(name = "zn_ratio_%s" % plot.name, logy = plot.logy)
    canvas.labels = plot.labels
    canvas.logy = plot.logy
    canvas.x_bounds = plot.bounds[1:]
    canvas.build()
    upper_pad = canvas.upper_pad
    middle_pad = canvas.middle_pad
    lower_pad = canvas.lower_pad

    # lets start
    xlow = plot.x_low
    xhigh = plot.x_high
    bin_width = plot.bin_width

    # histogram stack for the backgrounds
    hstack = histogram_stack("sm_stack", binning = plot.bounds)

    # group together the bkg histograms that will go into the stack
    histograms_bkg = []

    # colors for the stack (to be ordered)
    labels_bkg = {}
    colors_bkg = {}

    for ibkg, bkg in enumerate(bkgs) :

        h = histogram1d('histo_%s' % bkg.name, binning = plot.bounds)

        # loop through the bkg chain
        chain = bkg.chain()

        for ibc, bc in enumerate(chain) :

            hist_data = bc[plot.vartoplot]

            # weights
            lumis = bkg.scalefactor * np.ones(len(hist_data))
            weights = lumis * bc['eventweight']

            if plot.absvalue :
                hist_data = np.absolute(hist_data)

            # fill the histogram
            h.fill(hist_data, weights)

        labels_bkg[bkg.name] = bkg.displayname
        colors_bkg[bkg.name] = bkg.color

        # overflow
        h.add_overflow()

        # add to stack
        hstack.add(h)

    # order the stack by integral
    hstack.sort(reverse = True)

    ordered_labels_bkg = []
    ordered_colors_bkg = []

    for bkgname in hstack.order :
        name = bkgname.replace('histo_', '')
        ordered_labels_bkg.append(labels_bkg[name])
        ordered_colors_bkg.append(colors_bkg[name])

    # total SM histo
    histogram_sm = hstack.total_histo

    # y-limits
    maxy = histogram_sm.maximum()
    miny = 0.0
    if plot.logy :
        miny = 1e-2
    multiplier = 1.8
    if plot.logy :
        multiplier = 1e4
    maxy = multiplier * maxy

    upper_pad.set_ylim(miny, maxy)

    # statistical MC error band
    sm_y_error = histogram_sm.y_error()
    sm_x_error = np.zeros(len(sm_y_error))
    stat_error_band = errorbars.error_hatches(histogram_sm.bins[:-1], histogram_sm.histogram, \
            sm_x_error, sm_y_error, plot.bin_width)

    # total SM line
    sm_line = histogram_sm.bounding_line()
    upper_pad.plot(sm_line[0], sm_line[1], ls = '-', color = 'k', label = 'Total SM', lw = 2)

    ######################################
    # counts
    hstack.print_counts()

    #####################################
    # draw backgrounds
    histos = [h.data for h in hstack.histograms]
    weights = [h.weights for h in hstack.histograms]
    upper_pad.hist( histos,
                        weights = weights,
                        bins = plot.binning,
                        color = ordered_colors_bkg,
                        label = ordered_labels_bkg,
                        stacked = True,
                        histtype = 'stepfilled',
                        lw = 1,
                        edgecolor = 'k',
                        alpha = 1.0)

    #####################################
    # signals
    if len(sigs) == 0 :
        print "ERROR No signals loaded"
        sys.exit()

    signal_labels, signal_colors, signal_y, signal_x = draw_signal_histos(pad = upper_pad,
                samples = sigs,
                variable = plot.vartoplot,
                bins = histogram_sm.bins,
                binning = plot.bounds,
                absvalue = plot.absvalue)

    #####################################
    # middle pad, significance > x
    middle_pad.set_ylabel("Z $\\downarrow$ (>=)", fontsize = 18)
    middle_pad.set_ylim(0,3)

    maxz = 3
    for isignal, signal in enumerate(sigs) :
        sig_y_values = []
        for ix in range(len(histogram_sm.bins)) : # loop over the bins in the histogram
            #print "SM BINS      = %s" % histogram_sm.bins
            #print "SM BINS > 40 = %s" % histogram_sm.bins[4:-1]
            #print "SM Y         = %s" % histogram_sm.histogram
            #print "SM Y > 40    = %s" % histogram_sm.histogram[4:-1]

            b = np.sum( histogram_sm.histogram[ix:-1] ) # include background FROM ix to END
            s = np.sum( signal_y[isignal][ix:-1] ) # include signal FROM ix to END
            zn = significance.binomial_exp_z(s, b, rel_unc)
            sig_y_values.append(zn)
            if zn > maxz : maxz = zn
        xvals =  histogram_sm.bins + 0.5 * plot.bin_width
        middle_pad.plot(xvals, sig_y_values, markerfacecolor = signal.color,
                        marker = '>',
                        markeredgecolor = signal.color,
                        linestyle = 'None',
                        markersize = 4)

    if maxz > 5 :
        maxz = 5
    middle_pad.set_ylim(0, maxz + 0.2)

    ######################################
    # lower pad, signifiance < x
    lower_pad.set_ylabel("Z $\\uparrow$ (<)", fontsize = 18)
    lower_pad.set_ylim(0,3)

    maxz = 3
    for isignal, signal in enumerate(sigs) :
        sig_y_values = []
        for ix in range(len(histogram_sm.bins)) : # loop over the bins in the histogram
            #print "SM BINS          = %s" % histogram_sm.bins
            #print "SM BINS < 40     = %s" % histogram_sm.bins[ : 4]
            b = np.sum( histogram_sm.histogram[:ix]) # include background FROM BEGINNING to ix 
            s = np.sum( signal_y[isignal][:ix]) # include signal FROM BEGINNING to ix
            zn = significance.binomial_exp_z(s, b, rel_unc)
            sig_y_values.append(zn)
            if zn > maxz : maxz = zn
        xvals = histogram_sm.bins + 0.5 * plot.bin_width
        lower_pad.plot(xvals, sig_y_values, markerfacecolor = signal.color,
                        marker = '<',
                        markeredgecolor = signal.color,
                        linestyle = 'None',
                        markersize = 4)

    if maxz > 5 :
        maxz = 5
    lower_pad.set_ylim(0, maxz + 0.2)

    ######################################
    # get total Zn
    print 15 * '= '
    for isignal, signal in enumerate(sigs) :
        b = np.sum( histogram_sm.histogram ) # consider all bins
        s = np.sum( signal_y[isignal] )
        zn = significance.binomial_exp_z(s, b, rel_unc)
        print " > {bname:<10} : {zn_total:>10}".format(bname = 'Z %s' % signal.name, zn_total = round(zn,2))

    ######################################
    # draw exclusion threshold
    for pad in [middle_pad, lower_pad] :
        xl = np.linspace(xlow, xhigh, 20)
        yl = np.ones(len(xl)) * 1.64
        pad.plot(xl, yl, 'r--', zorder = 0, alpha = 0.65)

    #####################################
    # legend
    legend_order = ['Total SM']
    # the draw order of histos is reversed that of the legend order, so reverse
    legend_order += ordered_labels_bkg[::-1]
    leg_x, leg_y = make_legend(legend_order, upper_pad)

    make_signal_legend(signal_labels, signal_colors, coords = (leg_x, leg_y), pad = upper_pad)


    #####################################
    # add labels
    add_labels(upper_pad, region_name = region_to_plot.displayname, lumi = lumi_val)
    


    ######################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith('/') :
        output_dir += '/'
    save_name = output_dir + "zn_opt_%s_%s.pdf" % ( region_to_plot.name, plot.vartoplot )
    print " >>> Saving Zn plot to : %s" % os.path.abspath(save_name)
    canvas.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)

        

    

##############################################################################
def main() :

    parser = OptionParser()
    parser.add_option("-c", "--config", default = "", help = "Configuration file for samples, regions, plots")
    parser.add_option("-r", "--region", default = "", help = "Provide a region selection")
    parser.add_option("-o", "--output", default = "./", help = "Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("-v", "--var", default = "", help = "Provide a specific variable to plot")
    parser.add_option("-e", "--error", default = 0.3, help = "Relative uncertainty on background") 
    parser.add_option("--lumi", default = 36.1, help = "Set luminosity in fb-1 (default is 36.1)")
    parser.add_option("--logy", default = False, action = "store_true", help = "Set plots to have log y-axis")
    parser.add_option("--cache-dir", default = "./sample_cache", help = "Directry to place/look for the cached samples")
    (options, args) = parser.parse_args()
    config = options.config
    select_region = options.region
    output_dir = options.output
    select_var = options.var
    rel_unc = options.error
    in_logy = options.logy
    cache_dir = options.cache_dir
    in_lumi = float(options.lumi)

    print " * zn_plotter * "

    if not utils.file_exists(config) :
        sys.exit()

    global loaded_samples
    global loaded_regions
    global selected_region
    global select_lumi
    global do_logy
    global loaded_plots
    global additional_variables
    selected_region = select_region
    loaded_samples = []
    loaded_regions = []
    loaded_plots = []
    select_lumi = in_lumi
    do_logy = in_logy
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
        make_zn_plot(plot, region_to_plot, backgrounds, signals, rel_unc, output_dir, select_lumi)
#------------------------------------------------------------------------------
if __name__ == "__main__" :
    main()

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
import dantrimania.python.analysis.utility.utils.plib_utils as plib

# new
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
from dantrimania.python.analysis.utility.plotting.histogram_stack import histogram_stack
from dantrimania.python.analysis.utility.plotting.ratio_canvas import ratio_canvas

plt = plib.import_pyplot()
import numpy as np

def get_variables_from_tcut(tcut) :

    operators = ["==", ">=", "<=", ">", "<", "!=", "*", "-"]
    logics = ["&&", "||", ")", "(", "abs"]
    vars_only = tcut
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
    #vars_only = [v for v in vars_only if not v.isdigit()]

    return out

def get_required_variables(plots, region) :

    variables = []
    for p in plots :
        if p.vartoplot not in variables :
            variables.append(p.vartoplot)

    tcut = region.tcut
    selection_variables = get_variables_from_tcut(tcut)
    for sv in selection_variables :
        if sv not in variables :
            variables.append(sv)

    # we always need the eventweight, which will not show up in the tcut
    variables.append("eventweight")

    # TODO when loading systematics we need to store the weight leafs

    return variables

#############################################################################
def draw_signal_histos(pad = None, signals = [], var = "", binning = None, bins = None, absval = False) :

    histograms_signal = []
    colors_sig = [] 
    labels_sig = [] 

    for signal in signals :
        h = histogram1d("signal_histo_%s" % signal.name, binning = binning) 

        chain = signal.chain()
        for isc, sc in enumerate(chain) :
            lumis = signal.scalefactor * np.ones(len(sc[var]))
            weights = lumis * sc['eventweight']

            hist_data = sc[var]
            if absval :
                hist_data = np.absolute(hist_data)

            h.fill(hist_data, weights)

        labels_sig.append(signal.displayname)
        colors_sig.append(signal.color)

        # overflow
        h.add_overflow()

        histograms_signal.append(h)

    # draw
    histos = [h.data for h in histograms_signal]
    weights = [h.weights for h in histograms_signal]
    pad.hist(histos,
                weights = weights,
                bins = bins,
                color = colors_sig,
                label = labels_sig,
                ls = '--',
                stacked = False,
                histtype = 'step',
                lw = 1.5)
                

    print 15 * '- '
    for isignal, histo in enumerate(histograms_signal) :
        integral, error = histo.integral_and_error()
        integral_raw, error_raw = histo.integral_and_error(raw=True)
        print " > %s : %10.2f +/- %.2f (raw: %10.2f +/- %.2f)" % (signals[isignal].name.ljust(15), integral, error, integral_raw, error_raw)

    return labels_sig, colors_sig


#############################################################################
def make_stack_plot(plot, region, backgrounds, signals, data, output_dir) :

    print 50 * '*'

    # canvas
    canvas = ratio_canvas("ratio_canvas_%s" % plot.name)
    canvas.labels = plot.labels
    canvas.logy = plot.logy
    canvas.x_bounds = plot.bounds[1:]
    canvas.r_bounds = plot.bounds[1:]
    canvas.build()
    upper_pad = canvas.upper_pad
    lower_pad = canvas.lower_pad



    xlow = plot.x_low
    xhigh = plot.x_high
    bin_width = plot.bin_width
    binning = plot.bounds

    # build the histogram_stack
    hstack = histogram_stack("sm_stack", binning = binning)

    # group together the histogram objects for backgrounds
    histograms_bkg = []

    labels_bkg = {} 
    colors_bkg = {}

    for ibkg, bkg in enumerate(backgrounds) :

        h = histogram1d('histo_%s' % bkg.name, binning = binning)

        # loop through the chain and fill the histogram
        chain = bkg.chain()
        for ibc, bc in enumerate(chain) :

            # get weights
            lumis = bkg.scalefactor * np.ones(len(bc[plot.vartoplot]))
            weights = lumis * bc['eventweight']

            # get data
            hist_data = bc[plot.vartoplot]
            if plot.absvalue :
                hist_data = np.absolute(hist_data)

            # fill histogram
            h.fill(hist_data, weights)


        labels_bkg[bkg.name] = bkg.displayname
        colors_bkg[bkg.name] = bkg.color

        # overflow
        h.add_overflow()

        # add to stack
        hstack.add(h)

    # order the stack
    print "order before = %s" % hstack.order
    hstack.sort(reverse = True)
    print "order after = %s" % hstack.order

    ordered_labels_bkg = []
    ordered_colors_bkg = []
    for bkgname in hstack.order :
        name = bkgname.replace("histo_","")
        ordered_labels_bkg.append(labels_bkg[name])
        ordered_colors_bkg.append(colors_bkg[name])

    # total SM histo
    histogram_sm = hstack.total_histo

    # get y-axis maxima
    maxy = histogram_sm.maximum()
    miny = histogram_sm.minimum()

    multiplier = 1.65
    if len(signals) :
        multiplier = 1.8
    if plot.logy :
        multiplier = 1e4
        if len(signals) :
            multiplier = 1.e5
    maxy = multiplier * maxy
    upper_pad.set_ylim(miny, maxy)

    # statistical error band
    x_error = np.zeros(len(histogram_sm.y_error())) 
    stat_error_band = errorbars.error_hatches(histogram_sm.bins[:-1], histogram_sm.histogram, \
                                x_error, histogram_sm.y_error(), plot.bin_width) 

    # total sm line
    sm_line = histogram_sm.bounding_line()

    ###################################
    # counts
    hstack.print_counts()

    ##################################
    # draw backgrounds
    histos = []
    weights = []
    for name in hstack.order :
        for h in hstack.histograms :
            if name not in h.name : continue
            histos.append(h.data)
            weights.append(h.weights)
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

    # draw error band
    upper_pad.add_collection(stat_error_band)
    

    # draw total sm
    upper_pad.plot(sm_line[0], sm_line[1], ls = '-', color = 'k', label = 'Total SM', lw = 2)

    ##################################
    # data

    histogram_data = None
    if data :
        histogram_data = histogram1d("histo_data", binning = binning)
        chain = data.chain()
        for idc, dc in enumerate(chain) :
            data = dc[plot.vartoplot]
            if plot.absvalue :
                data = np.absolute(data)
            histogram_data.fill(data)

        # overflow
        histogram_data.add_overflow()

        maxd = histogram_data.maximum()
        if maxd > maxy : maxy = maxd

        data_x = histogram_data.bin_centers()
        data_y = histogram_data.histogram
        upper_pad.plot(data_x, data_y, 'ko', label = 'Data')

        # draw poisson errors
        data_err_low, data_err_high = errorbars.poisson_interval(data_y)
        data_err_low = data_y - data_err_low
        data_err_high = data_err_high - data_y
        data_err = [data_err_low, data_err_high]
        upper_pad.errorbar(data_x, data_y, yerr = data_err, fmt = 'none', color = 'k')

    #################################
    # signal
    if len(signals) > 0 :
        signal_labels, signal_colors = draw_signal_histos(pad = upper_pad,
                                        signals = signals,
                                        var = plot.vartoplot,
                                        binning = binning,
                                        bins = histogram_sm.bins[:-1],
                                        absval = plot.absvalue) 

                    


    ##################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith('/') :
        output_dir += '/'
    save_name = output_dir + "%s_%s.pdf" % ( region.name, plot.vartoplot )
    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    canvas.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)



##############################################################################
def main() :
    parser = OptionParser()
    parser.add_option("-c", "--config", default="", help="Configuration file for plotting")
    parser.add_option("-r", "--region", default="", help="Provide a region selection")
    parser.add_option("-o", "--output", default="./", help="Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("-v", "--var", default="", help="Provide as specific variable to plot")
    parser.add_option("--logy", default=False, action="store_true", help="Set plots to have log y-axis")
    parser.add_option("--skip-data", default=False, action="store_true", help="Don't include data in the plots")
    parser.add_option("--cache-dir", default="./sample_cache", help="Directory to place/look for the cached samples")
    (options, args) = parser.parse_args()
    config = options.config
    cache_dir = options.cache_dir
    do_logy = options.logy
    region = options.region
    output_dir = options.output
    select_var = options.var
    skip_data = options.skip_data

    #
    print "stack_plotter"
    print " > config:      %s" % config
    print " > cache dir:   %s" % cache_dir

    if not utils.file_exists(config) :
        sys.exit()

    global loaded_samples
    global loaded_regions
    global selected_region
    global loaded_plots#, loaded_systematics, loaded_regions
    global additional_variables
    selected_region = region
    loaded_samples = []
    loaded_regions = []
    loaded_plots = []
    additional_variables = []
    execfile(config, globals(), locals())

    if len(loaded_samples) == 0 :
        print "ERROR No loaded samples found in configuration"
        sys.exit()

    #check_selected_region(selected_region, loaded_regions)
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

    #backgrounds, signals, data = categorize_samples(loaded_samples)
    backgrounds, signals, data = sample_utils.categorize_samples(loaded_samples)

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

    if skip_data :
        del data
        data = None
            

    # cache
    cacher = sample_cacher.SampleCacher(cache_dir)
    cacher.samples = loaded_samples
    cacher.region = region_to_plot
    required_variables = get_required_variables(loaded_plots, region_to_plot)
    for av in additional_variables :
        if av not in required_variables :
            required_variables.append(av)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for p in loaded_plots :
        make_stack_plot(p, region_to_plot, backgrounds, signals, data, output_dir)

#-----------------------------------------------------------------------------
if __name__ == "__main__" :
    main()

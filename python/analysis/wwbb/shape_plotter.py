#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.utils.plib_utils as plib

plt = plib.import_pyplot()
import numpy as np

class histo :
    def __init__(self, name = "" ) :
        self.name = name
        self.color = ""
        self.label = ""

        self.y = None
        self.w = None
        self.e = None
        self.e_bars = None

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

def make_histo(pad, sample, filled = False, variable = "", bins = None, absval = False) :

    chain = sample.chain()

    h = []
    h_w2 = []

    w = []
    w2 = []

    for ic, ch in enumerate(chain) :
        lumi = np.ones(len(ch[variable]))
        lumi[:] = sample.scalefactor
        ch_w = lumi * ch['eventweight']
        w += list(ch_w)

        # sumw2
        ch_w2 = lumi * ch['eventweight']
        ch_w2 = ch_w2 ** 2
        w2 += list(ch_w2)

        # data
        if absval :
            h += list(np.absolute(ch[variable])) 
            h_w2 += list(np.absolute(ch[variable]))
        else :
            h += list(ch[variable])
            h_w2 += list(ch[variable])

    hist = histo(sample.name)
    y, bin_edges = np.histogram(h, bins = bins, weights = w, normed = 1)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    y_sumw2, _ = np.histogram(h_w2, bins = bins, weights = w2)

    y_err = np.sqrt(y_sumw2)

    histo.y = y
    histo.e = y_err
    histo.color = sample.color
    histo.label = sample.displayname

    alpha = 1.0
    histtype = 'step'
    if filled :
        alpha = 0.5
        histtype = 'stepfilled'
    hy, hx, _ = pad.hist(h,
                bins = bins,
                weights = w,
                histtype=histtype,
                color = sample.color,
                label = sample.displayname,
                alpha = alpha,
                normed = 1, 
                edgecolor=sample.color,
                lw = 1.5,
                ls = sample.linestyle)

    #bars = plt.errorbar(bin_centers, y, yerr = y_err, marker='.',
    #                        drawstyle='steps-mid', color = sample.color) 
   # pad.errorbar(bin_centers, y, yerr = y_err, marker='.',
   #                         drawstyle='steps-mid', color = sample.color) 
    #histo.e_bars = bars

    return max(hy), min(hy)

def make_shape_plot(plot, region, backgrounds, signals, output_dir) :
    print 50 * '-'
    print "make_shape_plot    %s" % plot.vartoplot

    xlow = plot.xlow
    xhigh = plot.xhigh
    bw = plot.binwidth
    nbins = np.arange(xlow, xhigh + bw, bw)
    pad = plot.pad

    background_histos = []
    signal_histos = []
    maxy = -1
    miny = 1e9

    for bkg in backgrounds :
        h_maxy, h_miny = make_histo(pad, bkg, variable = plot.vartoplot,
                                                filled = True, bins = nbins, absval = plot.absvalue)
        if h_maxy > maxy : maxy = h_maxy
        if h_miny < miny  : miny = h_miny

    for sig in signals :
        h_maxy, h_miny = make_histo(pad, sig, variable = plot.vartoplot,
                                                filled = False, bins = nbins, absval = plot.absvalue)
        if h_maxy > maxy : maxy = h_maxy
        if h_miny < miny : miny = h_miny

    f = 1.55
    low = 0.0
    if plot.logy :
        f = 100
        low = 0.01 * miny
    pad.set_ylim(low, f * maxy)

    pad.legend(loc='best', fontsize=16, frameon=False, ncol=1)

    ########################################
    # text
    pad.text(0.05, 0.95, '%s' % region.displayname, size = 18, ha='left', transform=pad.transAxes)

    #########################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "shape_%s_%s.pdf" % ( region.name, plot.vartoplot)

    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    plot.fig.savefig(save_name, bbox_inches='tight', dpi=200)
    
    

def main() :

    parser = OptionParser()
    parser.add_option("-c", "--config", default="", help="Configuration file for plotting")
    parser.add_option("-r", "--region", default="", help="Provide a region selection")
    parser.add_option("-o", "--output", default="./", help="Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("-v", "--var", default="", help="Provide a specific variable to plot")
    parser.add_option("--logy", default=False, action="store_true", help="Set the plots to have log y-axis")
    parser.add_option("--cache-dir", default="./sample_cache", help="Directory to place/look for the cached samples")

    (options, args) = parser.parse_args()
    config = options.config
    cache_dir = options.cache_dir
    do_logy = options.logy
    region = options.region
    output_dir = options.output
    select_var = options.var

    print "shape_plotter"
    print " > config:       %s" % config
    print " > cache dir:    %s" % cache_dir

    if not utils.file_exists(config) :
        print "blah"
        sys.exit()

    global loaded_samples
    global loaded_regions
    global selected_region
    global loaded_plots
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

    # check region
    if not region_utils.regions_unique(loaded_regions) :
        print "ERROR Loaded regions are not unique, here are the counts:"
        for rname, count in region_utils.region_counts(loaded_regions).iteritems() :
            print " > %s : %d" % ( rname, count )
        sys.exit()

    if not region_utils.has_region(loaded_regions, selected_region) :
        print "ERROR Requested region (=%s) not found in loaded regions:" % ( selected_region )
        for r in loaded_regions :
            print str(r)
        sys.exit()

    region_to_plot = None
    for r in loaded_regions :
        if r.name == selected_region :
            region_to_plot = r
            break

    # variables
    variables_found = []
    for p in loaded_plots :
        variables_found.append(p.vartoplot)
    if select_var != "" :
        if select_var not in variables_found :
            print "ERROR Requested variable (=%s) not found in configured plots" % select_var
            sys.exit()
        tmp_plots = []
        for p in loaded_plots :
            if p.vartoplot == select_var :
                tmp_plots.append(p)
        loaded_plots = tmp_plots

    # categorize
    backgrounds, signals, _ = sample_utils.categorize_samples(loaded_samples) 

    # cache
    cacher = sample_cacher.SampleCacher(cache_dir)
    cacher.samples = loaded_samples
    cacher.region = region_to_plot
    #required_variables = sample_utils.get_required_variables(loaded_plots, region_to_plot) 
    required_variables = get_required_variables(loaded_plots, region_to_plot)
    for av in additional_variables :
        if av not in required_variables :
            required_variables.append(av)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for plot in loaded_plots :
        make_shape_plot(plot, region_to_plot, backgrounds, signals, output_dir)
    

#____________________________________________________________
if __name__ == "__main__" :
    main()

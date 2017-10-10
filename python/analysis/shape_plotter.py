
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

#new
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
from dantrimania.python.analysis.utility.plotting.canvas import canvas

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

def draw_histo(pad, sample, filled = False, variable = '', binning = None,
            absval = False, bin_width = None) :

    h = histogram1d('histo_%s' % sample.name, binning = binning)

    # loop
    chain = sample.chain()
    for ic, c in enumerate(chain) :
    
        hist_data = c[plot.vartoplot]
    
        # get the weights
        lumis = sample.scalefactor * np.ones(len(hist_data))
        weights = lumis * c['eventweight']
    
        if plot.absvalue :
            hist_data = np.absolute(hist_data)
    
        h.fill(hist_data, weights)
    
    bin_content = h.histogram
    edges = h.bins
    bin_centers = h.bin_centers()
    total = sum(bin_content)
    
    bin_content = [ bc / total for bc in bin_content ]
    
    x = []
    y = []
    for i in range(len(bin_content)) :
        x.append(edges[i])
        x.append(edges[i] + bin_width)
        y.append(bin_content[i])
        y.append(bin_content[i])
    x.append(x[-1])
    y.append(-1000)
    
    if sample.is_signal :
        pad.plot(x, y, ls = '--', color = sample.color,
                    label = sample.displayname,
                    lw = 1.5, zorder = 1e6)
    else :
        pad.fill(x, y, color = sample.color, alpha = 0.5,
                    label = sample.displayname,
                    zorder = 0,
                    edgecolor = 'k')

    return min(bin_content), max(bin_content)

        

#############################################################################
def make_shape_plot(plot, region, bkgs, sigs, output_dir) :

    print 50 * '-'
    print 'shape_plotter    %s' % plot.vartoplot

    can = canvas("shape_canvas_%s" % plot.name)
    can.labels = plot.labels
    can.logy = plot.logy
    can.x_bounds = plot.bounds[1:]
    can.build()
    pad = can.pad
    

    xlow = plot.x_low
    xhigh = plot.x_high
    bin_width = plot.bin_width
    binning = plot.bounds

    # get the histograms
    histograms_bkg = []
    histograms_sig = []

    samples = []
    samples += bkgs
    samples += sigs

    maxy = -1
    miny = 1e9

    for sample in samples :

        hmin, hmax = draw_histo(pad, sample, filled = not sample.is_signal,
                    variable = plot.vartoplot,
                    binning = binning,
                    absval = plot.absvalue, bin_width = plot.bin_width)

        if hmin < miny : miny = hmin
        if hmax > maxy : maxy = hmax
                    

    multiplier = 1.55
    low = 0.0
    if plot.logy :
        multiplier = 1e2
        low = 0.01 * miny
    pad.set_ylim(low, maxy * multiplier)

    #handles, labels = pad.get_legend_handles_labels()
    #handles = list(set(handles))
    #labels = list(set(labels))
    #new_h = []
    #new_l = []
    #for s in samples :
    #    for il, l in enumerate(labels) :
    #        if s.displayname == l :
    #            if l not in new_l :
    #                new_l.append(l)
    #                new_h.append(handles[il])
    #handles = new_h
    #labels = new_l

    pad.legend(loc = 'best', fontsize = 16, frameon = False, ncol = 1)
    #pad.legend(handles, labels, loc = 'best', fontsize = 16, frameon = False, ncol = 1)

    ############################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith('/') :
        output_dir += '/'
    save_name = output_dir + 'shape_plot_%s_%s.pdf' % ( region.name, plot.vartoplot ) 

    print " >>> Saving shape plot to : %s" % os.path.abspath(save_name)
    can.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)

#---------------------------------------------------------------------
if __name__ == "__main__" :

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

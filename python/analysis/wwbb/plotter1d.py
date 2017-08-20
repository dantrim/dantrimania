#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher

import numpy as np


def check_config(config) :

    if config == "" :
        print "ERROR Configuration file name provided is empty"
        sys.exit()

    if not os.path.isfile(config) :
        print "ERROR Configuration file %s not found" % config
        sys.exit()

def categorize_samples(samples) :

    backgrounds = []
    signals = []
    data = None

    for s in samples :
        if not s.is_data and not s.is_signal :
            backgrounds.append(s)
        elif not s.is_data and s.is_signal :
            signals.append(s)
        elif s.is_data and not s.is_signal :
            if data :
                print "ERROR More than one of the loaded samples is categorized as Data"
                sys.exit()
            data = s

    return backgrounds, signals, data

    check_selected_region(selected_region, loaded_regions)
def check_selected_region(selected_region, loaded_regions) :
    found_region = False
    for region in loaded_regions :
        if region.name == selected_region :
            found_region = True
            break

    if not found_region :
        print "ERROR Did not find selected region (=%s) in list of loaded regions [ %s ]" % (selected_region, ','.join(loaded_regions) )
        sys.exit()

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

def make_legend(ordering, name_dict, pad) :
    handles, labels = pad.get_legend_handles_labels()
    new_handles = []
    new_labels = []
    for l in ordering :
        for il, label in enumerate(labels) :
            if label == l :
                new_labels.append(name_dict[l])
                new_handles.append(handles[il])
    pad.legend(new_handles,
                new_labels,
                loc=2,
                frameon=False,
                ncol=2,
                fontsize=14,
                numpoints=1)

def make_ratio_plot(plot, region, backgrounds, signals, data, output_dir) :

    print 50 * "-"

    print "nb -- not adding overflow, not making error bars"

    xlow = plot.xlow
    xhigh = plot.xhigh
    bw = plot.binwidth
    nbins = np.arange(xlow, xhigh + bw, bw)

    # group the histos
    bkg_histos = []

    # store color/label and index
    colors = {}
    labels = []
    weights = {}

    for ibkg, bkg in enumerate(backgrounds) :

        # 'histo' is the array of values
        histo = []

        # get the 'chain' (iterator over the datasets in the selelection file)
        chain = bkg.chain()
        b_weights = []
        for ibc, bc in enumerate(chain) :

            # get the eventweight and scale it by the lumi/scalefactor
            lumis = np.ones(len(bc[plot.vartoplot]))
            lumis[:] = bkg.scalefactor
            w = lumis * bc['eventweight']
            b_weights += list(w)

            # sumw2
            w2 = bc['eventweight'] ** 2
            w2 = lumis * w2

            # data to fill the histo
            histo += list(bc[plot.vartoplot]) # TODO see how to avoid list() calls, use numpy

        labels.append(bkg.name)
        bkg_histos.append(histo)
        colors[bkg.name] = bkg.color
        weights[bkg.name] = b_weights

    count_map = {}
    for ilabel, label in enumerate(labels) :
        count_map[sum(bkg_histos[ilabel])] = label
    bkg_histos = sorted(bkg_histos, key = lambda x : sum(x), reverse = False)

    ordered_labels = []
    ordered_weights = []
    ordered_colors = []
    for bh in bkg_histos :
        idx = sum(bh)
        ordered_labels.append(count_map[idx])
        ordered_weights.append(weights[count_map[idx]])
        ordered_colors.append(colors[count_map[idx]])

    labels = ordered_labels
    weights = ordered_weights
    colors = ordered_colors

    # pads
    upper = plot.upper
    lower = plot.lower
    y, x, patches = upper.hist(bkg_histos,
                                bins = nbins,
                                color = colors,
                                weights = weights,
                                label = labels,
                                stacked = True,
                                histtype = 'stepfilled',
                                lw = 1,
                                edgecolor = 'k',
                                alpha = 1.0)

    # total of the stack is the last array in the histgram since we stack
    total_sm_y = y[-1]
    total_sm_x = x
    maxy = max(total_sm_y)
    f = 2.0
    if plot.logy :
        f = 10000

    #########################################
    # draw total sm line
    smx = []
    smy = []
    for ix, xx in enumerate(total_sm_x[:-1]) :
        smx.append(xx)
        smx.append(xx + bw)
        smy.append(total_sm_y[ix])
        smy.append(total_sm_y[ix])
    smx.append(smx[-1])
    smy.append(-1000)
    upper.plot(smx, smy, ls='-', color='k', label='Total SM', lw=2)

        
    #########################################
    # data
    datay = None
    datax = None
    if data :
        histod = []
        chain = data.chain()
        for idc, dc in enumerate(chain) :
            histod += list(dc[plot.vartoplot])
        if max(histod) > maxy : maxy = max(histod)

        datay = np.histogram(histod, bins = nbins) [0]
        datax = [dx + 0.5 * bw for dx in total_sm_x]
        upper.plot(datax[:-1], datay, 'ko', label = 'Data')

    ########################################
    # counts
    print " Counts summary:"
    print "     Total SM = %.2f" % sum(total_sm_y)
    if data :
        print "     Data     = %.2f" % sum(datay)
        print "     Data/SM  = %.2f" % ( float(sum(datay)) / float(sum(total_sm_y)) )

    ########################################
    # ratio
    if data :
        ratio_y = np.ones(len(datay))
        ratio_x = datax
        for idata, d in enumerate(datay) :
            prediction = total_sm_y[idata]
            ratio = 1.0
            if prediction == 0 :
                ratio = -5.0
            else :
                ratio = d / prediction
            ratio_y[idata] = ratio
        lower.plot(ratio_x[:-1], ratio_y, 'ko', zorder=1000)

    # red line
    xl = np.linspace(xlow, xhigh, 20)
    yl = np.ones(len(xl))
    lower.plot(xl, yl, 'r--', zorder=0)

    #######################################
    # axes
    if plot.autoy :
        upper.set_ylim(plot.ylow, f * maxy)
    else :
        upper.set_ylim(plot.ylow, plot.yhigh)

    ######################################
    # legend
    legend_order = ["Data"]
    legend_order += ['Total SM']
    legend_order += sorted(labels, reverse=True)
    leg_names = {}
    leg_names['Data'] = 'Data'
    leg_names['Total SM'] = 'Standard Model'
    for bkg in backgrounds :
        leg_names[bkg.name] = bkg.displayname 
    make_legend(legend_order, leg_names, upper)

    ######################################
    # save
    utils.mkdir_p(output_dir) 
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "%s_%s.pdf" % ( region.name, plot.vartoplot )

    print " >>> Saving plot to : %s" % os.path.abspath(save_name) 
    plot.fig.savefig(save_name, bbox_inches='tight', dpi=200)
    print 50 * '-'


def main() :
    # grab the command line argumnets
    parser = OptionParser()
    parser.add_option("-c", "--config", default="", help="Configuration file for plotting")
    parser.add_option("-r", "--region", default="", help="Provide a region selection")
    parser.add_option("-o", "--output", default="./", help="Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("--logy", default=False, action="store_true", help="Set plots to have log y-axis")
    parser.add_option("--cache-dir", default="./sample_cache", help="Directory to place/look for the cached samples")
    (options, args) = parser.parse_args()
    config = options.config
    cache_dir = options.cache_dir
    do_logy = options.logy
    region = options.region
    output_dir = options.output

    #
    print "plotter1d"
    print " > config:      %s" % config
    print " > cache dir:   %s" % cache_dir

    check_config(config)

    global loaded_samples
    global loaded_regions
    global selected_region
    global loaded_plots#, loaded_systematics, loaded_regions
    selected_region = region
    loaded_samples = []
    loaded_regions = []
    loaded_plots = []
    execfile(config, globals(), locals())

    if len(loaded_samples) == 0 :
        print "ERROR No loaded samples found in configuration"
        sys.exit()

    backgrounds, signals, data = categorize_samples(loaded_samples)
    check_selected_region(selected_region, loaded_regions)

    for r in loaded_regions :
        print str(r)

    region_to_plot = None
    for r in loaded_regions :
        if r.name == selected_region :
            region_to_plot = r
            break

    for p in loaded_plots :
        print str(p)

    # cache
    cacher = sample_cacher.SampleCacher(cache_dir)
    cacher.samples = loaded_samples
    cacher.region = region_to_plot
    required_variables = get_required_variables(loaded_plots, region_to_plot)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for plot in loaded_plots :
        if plot.ratio :
            make_ratio_plot(plot, region_to_plot, backgrounds, signals, data, output_dir)





#________________________________________________________________________
if __name__ == "__main__" :
    main()

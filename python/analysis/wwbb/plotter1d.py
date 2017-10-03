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
plt = plib.import_pyplot()

import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches


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
                new_labels.append(name_dict[l].replace("SIG",""))
                new_handles.append(handles[il])

    leg_x, leg_y = 0.5, 0.75
    pad.legend(new_handles,
                new_labels,
                #loc=1,
                loc=(leg_x, leg_y),
                frameon=False,
                ncol=2,
                fontsize=12,
                numpoints=1,
                labelspacing=0.2,
                columnspacing=0.4)

    return leg_x, leg_y

def make_signal_legend(labels, colors, coords = [], pad = None) :

    handles, leg_labels = pad.get_legend_handles_labels()
    sig_handles = []
    sig_labels = []

    for l in labels :
        for il, ll in enumerate(leg_labels) :
            if l == ll :
                sig_handles.append(handles[il])
                sig_labels.append(l.replace("SIG",""))

    y_vals = []
    for il, l in enumerate(sig_labels) :
        y = coords[1] - 0.04 * (1.1*il+1)
        y_vals.append(y)
        pad.text(coords[0] + 0.1,  y, l,
                    transform=pad.transAxes,
                    fontsize=12,
                    ha='left')# - 0.1 * (il + 1), l)

    y_offset = 1.02
    for iy, y in enumerate(y_vals) :
        pad.plot([coords[0] + 0.007, coords[0] + 0.08], [y_offset * y, y_offset * y], '--', lw=1.5, color= colors[iy], transform=pad.transAxes)

def add_labels(pad, region_name = "") :

    # ATLAS label
    size = 18
    at_text = 'ATLAS'
    opts = dict(transform = pad.transAxes)
    opts.update( dict(va='top', ha='left') )
    pad.text(0.05, 0.97, at_text, size = size, style = 'italic', weight = 'bold',  **opts)

    what_kind = 'Internal'
    pad.text(0.23, 0.97, what_kind, size = size, **opts)

    # lumi stuff
    lumi = "36.1"
    pad.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, %s fb$^{-1}$' % ( lumi ), size = 0.75*size, **opts)

    # region
    pad.text(0.047, 0.83, region_name, size = 0.75 * size, **opts)

def make_error_bands(x, y, xerr, yerr, bw) :

    error_boxes = []
    for xc, yc, xe, ye in zip(x, y, xerr, yerr) :
        h = yc + ye - (yc - ye)
        if yc == 0 :
            continue
        rect = Rectangle((xc, yc-ye), bw, h, label = 'Uncertainty',
                            edgecolor='none',
                            fill=False,
                            color=None,
                            zorder=100000)
        error_boxes.append(rect)
    pc = PatchCollection(error_boxes, label = 'Uncertainty',
                            edgecolor='none',
                            facecolor=None,
                            alpha=0.0,
                            hatch='\\\\\\\\',
                            zorder=10000)
    return pc


def draw_signal_histos(pad = None, signals = [], var = "", bins = None, absval = False) :

    sig_histos = []
    w2_histos = []
    weights = []
    weights2 = []

    colors = []
    labels = []

    for signal in signals :
        histo = []
        w2_histo = []

        s_weights = []
        s_weights2 = []


        chain = signal.chain()
        for ic, c in enumerate(chain) :
            lumis = np.ones(len(c[var]))
            lumis[:] = signal.scalefactor
            w = lumis * c['eventweight']
            s_weights += list(w)

            w2 = lumis * c['eventweight']
            w2 = w2 ** 2
            s_weights2 += list(w2)

            if absval :
                histo += list(np.absolute(c[var]))
                w2_histo += list(np.absolute(c[var]))
            else :
                histo += list(c[var])
                w2_histo += list(c[var])

        labels.append("SIG" + signal.displayname)
        sig_histos.append(histo)
        w2_histos.append(w2_histo)
        weights.append(s_weights)
        weights2.append(s_weights2)
        colors.append(signal.color)



    sig_histos = [np.clip(s, bins[0], bins[-1]) for s in sig_histos]

    sy, sx, _ = pad.hist(sig_histos,
                            bins = bins,
                            color = colors,
                            weights = weights,
                            label = labels,
                            ls = '--',
                            stacked = False,
                            histtype = 'step',
                            lw = 1.5) 
    print 15 * '- '
    if len(signals) == 1 :
        print "Counts %s : %.2f" % ( signals[0].name, sum(list(sy)) )
    else :
        for isignal, signal_y in enumerate(sy) :
            print "Counts %s : %.2f" % ( signals[isignal].name, sum( list(signal_y) ) )


    return labels, colors

def make_ratio_plot(plot, region, backgrounds, signals, data, output_dir) :

    print 50 * "-"

    xlow = plot.xlow
    xhigh = plot.xhigh
    bw = plot.binwidth
    nbins = np.arange(xlow, xhigh + bw, bw)

    # group the histos
    bkg_histos = []
    w2_histos = []

    # store color/label and index
    colors = {}
    labels = []
    weights = {}
    weights2 = []

    for ibkg, bkg in enumerate(backgrounds) :

        # 'histo' is the array of values
        histo = []
        w2_histo = []

        # get the 'chain' (iterator over the datasets in the selelection file)
        chain = bkg.chain()
        b_weights = []
        b_weights2 = []
        for ibc, bc in enumerate(chain) :

            # get the eventweight and scale it by the lumi/scalefactor
            lumis = np.ones(len(bc[plot.vartoplot]))
            lumis[:] = bkg.scalefactor
            w = lumis * bc['eventweight']
            b_weights += list(w)

            # sumw2
            #w2 = bc['eventweight'] ** 2
            #w2 = lumis * w2
            w2 = lumis * bc['eventweight']
            w2 = w2 ** 2
            b_weights2 += list(w2)

            # data to fill the histo
            if plot.absvalue :
                histo += list(np.absolute(bc[plot.vartoplot])) # TODO see how to avoid list() calls, use numpy
                w2_histo += list(np.absolute(bc[plot.vartoplot]))
            else :
                histo += list(bc[plot.vartoplot])
                w2_histo += list(bc[plot.vartoplot])

        labels.append(bkg.name)
        bkg_histos.append(histo)
        w2_histos.append(w2_histo)
        colors[bkg.name] = bkg.color
        weights[bkg.name] = b_weights
        weights2.append(b_weights2)

        #weights2[bkg.name] = b_weights2

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

    # add overflow
    bkg_histos = [np.clip(b, nbins[0], nbins[-1]) for b in bkg_histos]
    for ib, b in enumerate(bkg_histos) :
        hb, _ = np.histogram(b, weights = weights[ib], bins = nbins)
        print "Counts %s : %.2f" % (labels[ib], sum(hb))
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
    f = 1.65
    if len(signals) :
        f = 1.8
    if plot.logy :
        f = 10000
        if len(signals) :
            f *= 10


    w2_h = np.ones(len(nbins[:-1]))
    for iw, w in enumerate(w2_histos) :
        h2y, _ = np.histogram(w, bins = nbins, weights = weights2[iw])
        w2_h += h2y
    
    yerr = np.sqrt(w2_h)
    xerr = [plot.binwidth + 0.5 for a in x]
    stat_error_hatches = make_error_bands(x,total_sm_y,xerr,yerr, plot.binwidth)
    upper.add_collection(stat_error_hatches)


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
    data_err = None
    if data :
        histod = []
        chain = data.chain()
        for idc, dc in enumerate(chain) :
            if plot.absvalue :
                histod += list(np.absolute(dc[plot.vartoplot]))
            else :
                histod += list(dc[plot.vartoplot])

        datay = np.histogram(np.clip(histod, nbins[0], nbins[-1]), bins = nbins) [0]
        if max(datay) > maxy : maxy = max(datay)
        datax = [dx + 0.5 * bw for dx in total_sm_x]
        upper.plot(datax[:-1], datay, 'ko', label = 'Data')

        # draw poisson errors
        data_err_low, data_err_high = errorbars.poisson_interval(datay)
        data_err_low = datay - data_err_low
        data_err_high = data_err_high - datay
        data_err = [data_err_low, data_err_high]
        upper.errorbar(datax[:-1], datay, yerr = [data_err_low, data_err_high], fmt='none', color='k')
        

    ########################################
    # signal
    signal_labels = []
    if len(signals) > 0 :
        signal_labels, signal_colors = draw_signal_histos(pad = upper, signals = signals, 
                                        var = plot.vartoplot, bins = nbins, absval = plot.absvalue)

    ########################################
    # counts
    print " Counts summary:"
    print "     Total SM = %.2f" % sum(total_sm_y)
    if data :
        print "     Data     = %.2f" % sum(datay)
        if sum(total_sm_y) > 0 :
            print "     Data/SM  = %.2f" % ( float(sum(datay)) / float(sum(total_sm_y)) )

    ########################################
    # ratio
    if data :
        ratio_y = np.ones(len(datay))
        ratio_x = datax
        ratio_data_err_low = np.zeros(len(datay)) 
        ratio_data_err_high = np.zeros(len(datay))
        for idata, d in enumerate(datay) :
            prediction = total_sm_y[idata]
            ratio = 1.0
            ratio_low = 0.0
            ratio_high = 0.0
            if prediction == 0 or d == 0:
                ratio = -5.0
            else :
                ratio = d / prediction
                ratio_low = data_err_low[idata] / prediction
                ratio_high = data_err_high[idata] / prediction
            ratio_y[idata] = ratio
            ratio_data_err_low[idata] = ratio_low
            ratio_data_err_high[idata] = ratio_high

        lower.plot(ratio_x[:-1], ratio_y, 'ko', zorder=1000)

        # plot the ratio data errors
        lower.errorbar(ratio_x[:-1], ratio_y, yerr = [ratio_data_err_low, ratio_data_err_high], fmt='none', color='k') 

        ratio_err = []
        for ism, sm in enumerate(total_sm_y) :
            sm_err = yerr[ism]
            rel_error = 0
            if sm != 0 :
                rel_error = float(sm_err / sm)
            ratio_err.append(rel_error)
        xerr = [plot.binwidth for a in ratio_x]

        # for the data graph were move the x-center to the center of the bin
        # so subtract off half the bin-width for the error hatches
        stat_error_band = make_error_bands([xv - 0.5 * plot.binwidth for xv in ratio_x[:-1]], np.ones(len(total_sm_y)), xerr, ratio_err, plot.binwidth) 
        lower.add_collection(stat_error_band)

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
    leg_names['Total SM'] = 'Total SM'
    for bkg in backgrounds :
        leg_names[bkg.name] = bkg.displayname 
    #legend_order += sorted(signal_labels, reverse = True)
    #for sig in signal_labels :
    #    leg_names[sig] = sig

    leg_x, leg_y = make_legend(legend_order, leg_names, upper)

    if len(signals) :
        make_signal_legend(signal_labels, signal_colors, coords = (leg_x, leg_y), pad = upper)

    ######################################
    # ATLAS text
    add_labels(upper, region_name = region.displayname)


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
    print "plotter1d"
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

    for plot in loaded_plots :
        if plot.ratio :
            make_ratio_plot(plot, region_to_plot, backgrounds, signals, data, output_dir)





#________________________________________________________________________
if __name__ == "__main__" :
    main()

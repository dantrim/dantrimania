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
    variables.append("eventweightNoPRW")
    variables.append("l0_q")
    variables.append("eventweightbtag")
    variables.append("eventweightbtagNoPRW")
    variables.append("eventweightBtagJvt")
    variables.append("eventweight_multi")
    variables.append("eventweightNoPRW_multi")
    variables.append("eventweightbtag_multi")
    variables.append("eventweightBtagJvt_multi")
    variables.append("pupw_period")

    # TODO when loading systematics we need to store the weight leafs

    return variables

#############################################################################
def make_legend(ordered_labels, pad) :

    handles, labels = pad.get_legend_handles_labels()
    new_handles = []
    new_labels = []
    for l in ordered_labels :
        for il, label in enumerate(labels) :
            if label == l :
                new_labels.append(l.replace("SIG",""))
                new_handles.append(handles[il])

    leg_x, leg_y = 0.5, 0.75
    if len(ordered_labels) > 10 :
        leg_y = 0.95 * leg_y
    pad.legend(new_handles,
                new_labels,
                loc = (leg_x, leg_y),
                frameon = False,
                ncol = 2,
                fontsize = 12,
                numpoints = 1,
                labelspacing = 0.2,
                columnspacing = 0.4)

    return leg_x, leg_y

#############################################################################
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
        pad.text(coords[0] + 0.1, y, l,
                    transform = pad.transAxes,
                    fontsize = 12,
                    ha = 'left')

    y_offset = 1.02
    for iy, y in enumerate(y_vals) :
        pad.plot([coords[0] + 0.007, coords[0] + 0.08],
                    [y_offset * y, y_offset * y],
                    '--',
                    lw = 1.5, color = colors[iy], transform = pad.transAxes)

#############################################################################
def add_labels(pad, region_name = "") :

    # ATLAS label
    size = 18
    text = 'ATLAS'
    opts = dict(transform = pad.transAxes)
    opts.update( dict(va = 'top', ha = 'left') )
    pad.text(0.05, 0.97, text, size = size, style = 'italic', weight = 'bold', **opts)

    what_kind = 'Internal'
    pad.text(0.23, 0.97, what_kind, size = size, **opts)

    # lumi stuff
    #lumi = "76.4"
    #lumi = "36.1"
    #lumi = "43.58"
    #lumi = "76.9"

    #lumi = "32.2"
    #lumi = "41.95"
    #lumi = "74.2"
    lumi = '36.2'
    pad.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, %s fb$^{-1}$' % lumi, size = 0.75 * size, **opts)

    # region
    pad.text(0.047, 0.83, region_name, size = 0.75 * size, **opts)
    #pad.text(0.047, 0.76, "mc16d", size = 0.75 * size, **opts)
    #pad.text(0.047, 0.76, "mc16a", size = 0.75 * size, **opts)
    #pad.text(0.047, 0.76, "mc16d", size = 0.75 * size, **opts)
    pad.text(0.047, 0.76, "mc16a", size = 0.75 * size, **opts)



#############################################################################
def get_wt_bjet_weights(sub_bjet_pts) :

    weights = np.ones(len(sub_bjet_pts))
    for ibj, bj in enumerate(sub_bjet_pts) :
        if bj < 140 :
            weights[ibj] = 1.0
        else :
            weights[ibj] = 0.5
#        if bj < 160 :
#            weights[ibj] = 1.0
#        elif bj>=160 and bj<200 :
#            weights[ibj] = 0.5
#        elif bj>=200 and bj<240 :
#            weights[ibj] = 0.48
#        elif bj>=240 :
#            weights[ibj] = 0.1
    return weights


def draw_signal_histos(pad = None, signals = [], var = "", binning = None, bins = None, absval = False) :

    histograms_signal = []
    colors_sig = []
    labels_sig = []

    for signal in signals :
        h = histogram1d("signal_histo_%s" % signal.name, binning = binning)

        chain = signal.chain()
        for isc, sc in enumerate(chain) :

            lumis = signal.scalefactor * np.ones(len(sc[var]))
#            weights = lumis * sc['eventweight_multi']
            weight_str = 'eventweightBtagJvt'
#            weights = lumis * sc[weight_str]
#            weights = lumis * sc['eventweight_multi']
#            weights = lumis * sc['eventweightNoPRW']
#            weights = lumis * sc['eventweightBtagJvt_multi']


            hist_data = sc[var]
            if absval :
                hist_data = np.absolute(hist_data)

            h.fill(hist_data, weights)

        labels_sig.append("SIG" + signal.displayname)
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
                lw = 1.5,
                zorder = 1e5)


    print 15 * '- '
    for isignal, histo in enumerate(histograms_signal) :
        print histo.count_str(rmlist=["signal_histo_"])
        #integral, error = histo.integral_and_error()
        #integral_raw, error_raw = histo.integral_and_error(raw=True)
        #print " > %s : %10.2f +/- %.2f (raw: %10.2f +/- %.2f)" % (signals[isignal].name.ljust(15), integral, error, integral_raw, error_raw)

    return labels_sig, colors_sig


#############################################################################
def make_stack_plots(plots, region, backgrounds, signals, data = None, output_dir = "./", suffix = "") :

    histograms_bkg = {} # histograms by variable : { plot_variable : [ list of histograms ] }
    labels_bkg = {}
    colors_bkg = {}

    n_plots = len(plots)

    for iplot, plot in enumerate(plots) :
        histos_for_plot = {}
        for bkg in backgrounds :
            h = histogram1d("histo_%s" % (bkg.name), binning = plot.bounds)
            #h = histogram1d("histo_%s_%s" % (bkg.name, plot.vartoplot), binning = plot.bounds)
#            histos_for_plot.append(h)
            histos_for_plot[bkg.name] = h
        histograms_bkg[plot.vartoplot] = histos_for_plot

    for ibkg, bkg in enumerate(backgrounds) :

        labels_bkg[bkg.name] = bkg.displayname
        colors_bkg[bkg.name] = bkg.color

        chain = bkg.chain()
        weight_str = 'eventweightBtagJvt'#_multi'

        if 'drellyan' in bkg.name.lower() : # or 'diboson' in bkg.name.lower() :
            weight_str = 'eventweightBtagJvt'
        #weight_str = 'eventweightNoPRW'
        #weight_str = 'eventweightBtagJvt'
#        weight_str = 'eventweightBtagJvt'
#        weight_str = 'eventweightNoPRW_multi'
#        weight_str = 'eventweight_multi'
#        weight_str = 'eventweightBtagJvt_multi'
        #if 'top' in region.name or 'tt' in region.name or 'wt' in region.name :
        #    weight_str += 'btag'

        for ic, c in enumerate(chain) :

            if 'S2L' in region.name and ('cr' in region.name or 'vr' in region.name) :
                cos = c["cosThetaB"]
                dpb = c["DPB_vSS"]
                if 'cr' in region.name :
                    idx = (dpb < (0.9 * np.abs(cos) + 1.6))
                elif 'vr' in region.name :
                    idx = (dpb > (0.9 * np.abs(cos) + 1.6))
                c = c[idx]

            ev_weight = c[weight_str]
            if ('_multi' not in weight_str and 'NoPRW' not in weight_str)  or 'drellyan' in bkg.name.lower() : # or 'diboson' in bkg.name.lower() :
                # since we are not combingin mc16a + mc16d, divide out the period weight
                print "INFO dividing out the PRW period weights"
                period_weights = c['pupw_period']
                ev_weight = np.divide(ev_weight, period_weights)


            for iplot, plot in enumerate(plots) :
                varname = plot.vartoplot
                plot_data = c[varname]
                #if varname == "l0_d0sig" :
                #    charge_data = c["l0_q"]
                #    plot_data = plot_data * charge_data

                lumis = bkg.scalefactor * np.ones(len(plot_data))
                weights = lumis * ev_weight #c['eventweightNoPRW']#_multi'] #NoPRW']
                if plot.absvalue :
                    plot_data = np.absolute(plot_data)

                histograms_bkg[varname][bkg.name].fill(plot_data, weights)

    # add overflow
    for plot in plots :
        for bkg in backgrounds :
            histograms_bkg[plot.vartoplot][bkg.name].add_overflow()


    histogram_stacks = {}
    ordered_labels_bkg = {}
    ordered_colors_bkg = {}

    # build the stacks
    for plot in plots :

        ordered_labels_bkg[plot.vartoplot] = []
        ordered_colors_bkg[plot.vartoplot] = []

        stack = histogram_stack("sm_stack_%s" % plot.vartoplot, binning = plot.bounds)
        for bkg in backgrounds :
            stack.add(histograms_bkg[plot.vartoplot][bkg.name])
        stack.sort(reverse = True)

        histogram_stacks[plot.vartoplot] = stack

        for bkgname in stack.order :
            name = bkgname.replace("histo_", "")
            name = name.split("_")[0]
            ordered_labels_bkg[plot.vartoplot].append(labels_bkg[name])
            ordered_colors_bkg[plot.vartoplot].append(colors_bkg[name])

    ############################
    # data
    histograms_data = {}

    if data :
        for plot in plots :
            hdata = histogram1d("histo_data_%s" % plot.vartoplot, binning = plot.bounds)
            chain = data.chain()
            for idc, dc in enumerate(chain) :

                if 'S2L' in region.name and ('cr' in region.name or 'vr' in region.name) :

                    cos = dc["cosThetaB"]
                    dpb = dc["DPB_vSS"]
                    if 'cr' in region.name :
                        idx = (dpb < (0.9 * np.abs(cos) + 1.6))
                    elif 'vr' in region.name :
                        idx = (dpb > (0.9 * np.abs(cos) + 1.6))
                    dc = dc[idx]

                plot_data = dc[plot.vartoplot]
                #if plot.vartoplot == "l0_d0sig" :
                #    print "adding CHARGE to data"
                #    charge_data = dc["l0_q"]
                #    plot_data = plot_data * charge_data

                if plot.absvalue :
                    plot_data = np.absolute(plot_data)
                hdata.fill(plot_data)
            # overflow
            hdata.add_overflow()
            histograms_data[plot.vartoplot] = hdata


    ###########################
    # start drawing
    n_plots = len(plots)

    print_yields = True
    for iplot, plot in enumerate(plots) :

        print "[%02d/%02d] %s" % (iplot+1, n_plots, plot.vartoplot)

        canvas = ratio_canvas("ratio_canvas_%s" % plot.name)
        canvas.labels = plot.labels
        canvas.logy = plot.logy
        canvas.x_bounds = plot.bounds[1:]
        canvas.build()

        upper_pad = canvas.upper_pad
        lower_pad = canvas.lower_pad

        xlow = plot.x_low
        xhigh = plot.x_high
        bin_width = plot.bin_width
        binning = plot.bounds

        ticks = list(np.arange(xlow, xhigh + bin_width, bin_width))
        if len(ticks) > 10 :
            ticks = ticks[::2]
        #if ticks[-1] != xhigh :
        #    last = ticks[-1]
        #    new_last = last + 2*bin_width
        #    xhigh = new_last
        #    plot.x_high = xhigh
        #    ticks.append(new_last)


        upper_pad.set_xticks(ticks)
        lower_pad.set_xticks(ticks)
#        lower_pad.set_xticklabels([str(x) for x in ticks])

        stack = histogram_stacks[plot.vartoplot]

        histo_total = stack.total_histo

        # get yaxis maxima
        maxy = histo_total.maximum()
        miny = 0.0
        if plot.logy :
            miny = 1e-2

        multiplier = 1.65
        if len(signals) :
            multiplier = 1.8
        if plot.logy :
            multiplier = 1e3
            if len(signals) >= 2 :
                multiplier = 1e4
        maxy = multiplier * maxy

        upper_pad.set_ylim(miny, maxy)

        # statistical error band
        sm_x_error = np.zeros(len(histo_total.y_error()))
        sm_y_error = histo_total.y_error()
        stat_error_band = errorbars.error_hatches(histo_total.bins[:-1], histo_total.histogram, \
                        sm_x_error, sm_y_error, plot.bin_width)

        # total SM line
        sm_line = histo_total.bounding_line()

        # counts
        if print_yields :
            stack.print_counts()

        # draw backgrounds
        histos = []
        weights = []
        for name in stack.order :
            for h in stack.histograms :
                if name != h.name.replace("hist_", "") : continue
                histos.append(h.data)
                weights.append(h.weights)
        upper_pad.hist( histos,
                        weights = weights,
                        bins = plot.binning,
                        color = ordered_colors_bkg[plot.vartoplot],
                        label = ordered_labels_bkg[plot.vartoplot],
                        stacked = True,
                        histtype = 'stepfilled',
                        lw = 1,
                        edgecolor = 'k',
                        alpha = 1.0)

        # print some yields
        if print_yields :
            sm_total_yield = histo_total.integral()
            print 30 * "*"
            print histo_total.count_str(name = 'Total SM')
        data_yield =  -1


        # draw error band
        upper_pad.add_collection(stat_error_band)

        # draw total SM
        upper_pad.plot(sm_line[0], sm_line[1], ls = '-', color = 'k', label = 'Total SM', lw = 2)

        # draw data points
        if data :

            hdata = histograms_data[plot.vartoplot]
            data_x = np.array(hdata.bin_centers())
            data_y = hdata.histogram
            nonzero_idx = data_y > 0
            data_y[data_y == 0.] = -5
            upper_pad.plot(data_x, data_y, 'ko', label = 'Data')

            # poisson errors
            data_err_low, data_err_high = errorbars.poisson_interval(data_y)
            data_err_low = data_y - data_err_low
            data_err_high = data_err_high - data_y
            data_err = [data_err_low, data_err_high]
            upper_pad.errorbar(data_x, data_y, yerr = data_err, fmt = 'none', color = 'k')

            data_yield = hdata.integral()



        if data_yield >= 0 and print_yields :
            print_yields = False
            print hdata.count_str(name = 'Data')
            print " > Data / SM : %5.2f" % ( data_yield / sm_total_yield )


        # ratio
        pred_y = histo_total.histogram
        ratio_y = hdata.divide(histo_total)
        ratio_y[ ratio_y == 0. ] = -1
        ratio_x = np.array(hdata.bin_centers())

        ratio_data_err_low = -1 * np.ones(len(ratio_y))
        ratio_data_err_high = -1 * np.ones(len(ratio_y))
        for idata, d in enumerate(ratio_y) :
            prediction = pred_y[idata]
            if ratio_y[idata] == 0.0 or ratio_y[idata] < 0 :
                ratio_data_err_low[idata] = 0
                ratio_data_err_high[idata] = 0
            else :
                ratio_data_err_low[idata] = data_err_low[idata] / prediction
                ratio_data_err_high[idata] = data_err_high[idata] / prediction
        lower_pad.plot(ratio_x, ratio_y, 'ko', zorder = 1000)
        yerr = [ratio_data_err_low, ratio_data_err_high]
        lower_pad.errorbar(ratio_x, ratio_y, yerr = yerr, fmt = 'none', color = 'k')

        # sm error on ratio band
        sm_ratio_error = []
        for ism, sm in enumerate(pred_y) :
            sm_y_error_ratio = sm_y_error[ism]
            relative_error = 0.0
            if sm != 0 :
                relative_error = float(sm_y_error_ratio) / float(sm)
            if ratio_y[ism] == 0 :
                relative_error = 0
            sm_ratio_error.append(relative_error)
        sm_x_error_ratio = [plot.bin_width for a in ratio_x]

        ratio_stat_error_band = errorbars.error_hatches(
                [xv - 0.5 * plot.bin_width for xv in ratio_x],
                np.ones(len(ratio_y)),
                sm_x_error_ratio,
                sm_ratio_error,
                plot.bin_width)
        lower_pad.add_collection(ratio_stat_error_band)



        # legend
        legend_order = ["Data"]
        legend_order += ["Total SM"]
        legend_order += ordered_labels_bkg[plot.vartoplot][::-1]
        leg_x, leg_y = make_legend(legend_order, upper_pad)

        # labels
        add_labels(upper_pad, region_name = region.displayname)

        # save

        utils.mkdir_p(output_dir)
        if not output_dir.endswith('/') :
            output_dir += '/'
        if suffix != "" :
            suffix = "_" + suffix
        save_name = output_dir + "%s_%s%s.png" % ( region.name, plot.vartoplot, suffix)
        print " >>> Saving plot to : %s" % os.path.abspath(save_name)
        canvas.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)



def make_stack_plot(plot, region, backgrounds, signals, data, output_dir, suffix) :

    print 50 * '*'

    # canvas
    canvas = ratio_canvas("ratio_canvas_%s" % plot.name)
    canvas.labels = plot.labels
    canvas.logy = plot.logy
    canvas.x_bounds = plot.bounds[1:]
    #canvas.r_bounds = plot.bounds[1:]
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
#            weights = lumis * bc['eventweightNoPRW']
            weights = lumis * bc['eventweight_multi']
            #weights = lumis * bc['eventweightBtagJvt_multi']

            # wt
#            if "Wt" in bkg.name :
#                wt_weights = get_wt_bjet_weights(bc['bj1_pt'])
#                weights = weights * wt_weights
                #for iw, w in enumerate(weights) :
                #    weights[iw] = w * wt_weights[iw]
                #weights = weights * wt_weights

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
    hstack.sort(reverse = True)

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
    miny = 0.0
    if plot.logy :
        miny = 1e-2

    multiplier = 1.65
    if len(signals) :
        multiplier = 1.8
    if plot.logy :
        multiplier = 1e3
        if len(signals) >= 2 :
            multiplier = 1e4
    maxy = multiplier * maxy
    #upper_pad.set_ylim(miny, maxy)

    # statistical error band
    sm_x_error = np.zeros(len(histogram_sm.y_error()))
    sm_y_error = histogram_sm.y_error()
    stat_error_band = errorbars.error_hatches(histogram_sm.bins[:-1], histogram_sm.histogram, \
                                sm_x_error, sm_y_error, plot.bin_width)

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
            #if name not in h.name : continue
            if name != h.name.replace("hist_","") : continue
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

    #################################
    # signal
    if len(signals) > 0 :
        signal_labels, signal_colors = draw_signal_histos(pad = upper_pad,
                                        signals = signals,
                                        var = plot.vartoplot,
                                        binning = binning,
                                        bins = histogram_sm.bins,
                                        absval = plot.absvalue)

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

        # counts
        print 30 * '-'
        print histogram_sm.count_str(name = 'Total SM')
        print histogram_data.count_str(name = 'Data')
        total_sm = histogram_sm.integral()
        total_data = histogram_data.integral()
        print " > Data / SM  : %5.2f" % ( total_data / total_sm )

        maxd = histogram_data.maximum()
        if maxd > maxy :
            maxy = multiplier * maxd

        data_x = np.array(histogram_data.bin_centers())
        data_y = histogram_data.histogram
        nonzero_idx = data_y > 0
        #if plot.logy :
        #    data_y[data_y == 0.] = 1e-1 * histogram_sm.minimum()
        #else :
        data_y[data_y == 0.] = -5
        #data_y = data_y[nonzero_idx]
        #data_x = data_x[nonzero_idx]
        upper_pad.plot(data_x, data_y, 'ko', label = 'Data')

        # draw poisson errors
        data_err_low, data_err_high = errorbars.poisson_interval(data_y)
        data_err_low = data_y - data_err_low
        data_err_high = data_err_high - data_y
        data_err = [data_err_low, data_err_high]
        upper_pad.errorbar(data_x, data_y, yerr = data_err, fmt = 'none', color = 'k')


        #################################
        # ratio
        pred_y = histogram_sm.histogram
        #pred_y = pred_y[nonzero_idx]

        ratio_y = histogram_data.divide(histogram_sm)
        #ratio_y = ratio_y[nonzero_idx]
        ratio_y[ ratio_y == 0. ] = -1

        ratio_x = np.array(histogram_data.bin_centers())
        #ratio_x = ratio_x[nonzero_idx]

        ratio_data_err_low = -1 * np.ones(len(ratio_y))
        ratio_data_err_high = -1 * np.ones(len(ratio_y))
        for idata, d in enumerate(ratio_y) :
            prediction = pred_y[idata]
            if ratio_y[idata] == 0.0 or ratio_y[idata] < 0:
                ratio_data_err_low[idata] = 0
                ratio_data_err_high[idata] = 0
            else :
                ratio_data_err_low[idata] = data_err_low[idata] / prediction
                ratio_data_err_high[idata] = data_err_high[idata] / prediction
        lower_pad.plot(ratio_x, ratio_y, 'ko', zorder=1000)
        yerr = [ratio_data_err_low, ratio_data_err_high]
        lower_pad.errorbar(ratio_x, ratio_y, yerr = yerr, fmt = 'none', color = 'k')

        # sm error on ratio band
        sm_ratio_error = []
        for ism, sm in enumerate(pred_y) :
            sm_y_error_ratio = sm_y_error[ism]
            relative_error = 0.0
            if sm != 0 :
                relative_error = float(sm_y_error_ratio / sm)
            if ratio_y[ism] == 0 :
                relatve_error = 0
            sm_ratio_error.append(relative_error)
        sm_x_error_ratio = [plot.bin_width for a in ratio_x]

        # for the data graph we move the x-center to the center of the bin
        # so subtract off half the bin-width for the error hatches
        ratio_stat_error_band = errorbars.error_hatches(
                [xv - 0.5 * plot.bin_width for xv in ratio_x],
                np.ones(len(ratio_y)),
                sm_x_error_ratio,
                sm_ratio_error,
                plot.bin_width)
        lower_pad.add_collection(ratio_stat_error_band)

    # now set the y-axis now that we have both data and MC taken into account
    upper_pad.set_ylim(miny, maxy)

    #################################
    # legend
    legend_order = ["Data"]
    legend_order += ['Total SM']
    # the draw order of histos is reversed that of the legend order, so reverse
    legend_order += ordered_labels_bkg[::-1]
    leg_x, leg_y = make_legend(legend_order, upper_pad)

    if len(signals) > 0 :
        make_signal_legend(signal_labels, signal_colors, coords = (leg_x, leg_y), pad = upper_pad)

    #################################
    # labels
    add_labels(upper_pad, region_name = region.displayname)




    ##################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith('/') :
        output_dir += '/'
    if suffix != "" :
        suffix = "_" + suffix
    save_name = output_dir + "%s_%s%s.pdf" % ( region.name, plot.vartoplot, suffix )
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
    parser.add_option("--suffix", default="", help = "Filename suffix for output plots")
    parser.add_option("--cache-dir", default="./sample_cache", help="Directory to place/look for the cached samples")
    (options, args) = parser.parse_args()
    config = options.config
    cache_dir = options.cache_dir
    do_logy = options.logy
    region = options.region
    output_dir = options.output
    select_var = options.var
    skip_data = options.skip_data
    suffix = options.suffix

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
        select_vars = select_var.split(",")
        for sv in select_vars :
            for p in loaded_plots :
                if p.vartoplot == sv :
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

    n_plots = len(loaded_plots)
    #for p in loaded_plots :
    #    make_stack_plots([p], region_to_plot, backgrounds, signals, data, output_dir, suffix)
    make_stack_plots(loaded_plots, region_to_plot, backgrounds, signals, data, output_dir, suffix)

#    for iplot, p in enumerate(loaded_plots) :
#        print "[%02d/%02d]" % (iplot+1, n_plots)
#        make_stack_plot(p, region_to_plot, backgrounds, signals, data, output_dir, suffix)

#-----------------------------------------------------------------------------
if __name__ == "__main__" :
    main()

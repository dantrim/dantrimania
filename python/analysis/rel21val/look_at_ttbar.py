#!/usr/bin/env python

import sys
import os

from optparse import OptionParser

import h5py

from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
from dantrimania.python.analysis.utility.plotting.canvas import canvas
from dantrimania.python.analysis.utility.plotting.ratio_canvas import ratio_canvas
from dantrimania.python.analysis.utility.plotting.plot1d import plot1d
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.plotting.m_py.errorbars as errorbars
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.samples.region_utils as region_utils

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region

import numpy as np
from math import sqrt

from matplotlib.lines import Line2D

r21_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/mc/h5/CENTRAL_410472_mc16a.h5"
r20_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0234/j_dec7_tight/mc/h5/CENTRAL_410009.h5"
r20_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0234/o_apr27_rel21val_wwbb/mc/ttbar/h5/CENTRAL_410009.h5"


#r20_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0234/o_apr27_rel21val_wwbb/mc/CENTRAL_410016.h5"
#r20_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0234/o_apr27_rel21val_wwbb/mc/CENTRAL_410015.h5"
#r21_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/mc/CENTRAL_410016_mc16a.h5"
#r21_ttbar = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/mc/CENTRAL_410015_mc16a.h5"

def get_variables() :

    var = {}
    var["dphi_met_ll"] =                    [0.05, -3.2, 3.2]
    var["l0_pt"] =                          [1, 20, 120]
    var["l1_pt"] =                          [1, 20, 120]
    var["l0_eta"] =                         [0.1, -2.8, 2.8]
    var["l1_eta"] =                         [0.1, -2.8, 2.8]
    var["mll"] =                            [1, 50, 130]
    var["pTll"] =                           [1, 0, 200]
    var["dphi_ll"] =                        [0.1, -3.5, 3.5]
    var["dRll"] =                           [0.05, 0, 5]
    var["deta_ll"] =                        [0.05, -4, 4]
    var["met"] =                            [20, 0, 400]
    var["j0_pt"] =                          [1, 0, 400]
    var["bj0_pt"] =                         [1, 0, 400]
    var["dphi_j0_l0"] =                     [0.01, -3.2, 3.2]
    var["dphi_bj0_l0"] =                    [0.01, -3.2, 3.2]
    var["dphi_j0_ll"] =                     [0.01, -3.2, 3.2]
    var["dphi_bj0_ll"] =                    [0.01, -3.2, 3.2]
    var["mbb"] =                            [1, 0, 500]
    var["dRbb"] =                           [0.05, 0, 6]
    var["dphi_bb"] =                        [0.05, -3.2, 3.2]
    var["HT2Ratio"] =                       [0.05, 0, 1]
    var["mt2_bb"] =                         [1, 0, 400]
    var["mt2_llbb"]  =                      [1, 0, 500]
    var['nBJets'] =                         [1,0,6]
    var['nJets'] =                          [1,0,8]

    var["dphi_met_ll"] =                    [0.1, -3.2, 3.2]
    var["l0_pt"] =                          [10, 20, 120]
    var["l1_pt"] =                          [10, 20, 120]
    var["l0_eta"] =                         [0.1, -2.8, 2.8]
    var["l1_eta"] =                         [0.1, -2.8, 2.8]
    var["mll"] =                            [20, 0, 600]
    var["pTll"] =                           [5, 0, 200]
    var["dphi_ll"] =                        [0.1, -3.5, 3.5]
    var["dRll"] =                           [0.1, 0, 5]
    var["deta_ll"] =                        [0.1, -4, 4]
    var["met"] =                            [20, 0, 400]
    var["j0_pt"] =                          [10, 0, 400]
    var["bj0_pt"] =                         [10, 0, 400]
    var["bj1_pt"] =                         [10, 0, 400]
    var["j0_pt"] =                         [10, 0, 400]
    var["j1_pt"] =                         [10, 0, 400]
    var["sj0_pt"] =                         [10, 0, 400]
    var["sj1_pt"] =                         [10, 0, 400]
    var["j0_eta"] =                         [0.1, -3.2, 3.2]
    var["j1_eta"] =                         [0.1, -3.2, 3.2]
    var["bj0_eta"] =                        [0.1, -3.2, 3.2]
    var["bj1_eta"] =                        [0.1, -3.2, 3.2]
    var["sj0_eta"] =                        [0.1, -3.2, 3.2]
    var["sj1_eta"] =                        [0.1, -3.2, 3.2]
    var["j0_nTracks"] =                     [1, 0, 40]
    var["j0_sumTrkPt"] =                    [10, 0, 400]
    var["bj0_nTracks"] =                    [1, 0, 40]
    var["bj0_sumTrkPt"] =                    [10, 0, 400]
    var["sj0_nTracks"] =                    [1, 0, 40]
    var["sj0_sumTrkPt"] =                    [10, 0, 400]
    var["dphi_j0_l0"] =                     [0.1, -3.2, 3.2]
    var["dphi_bj0_l0"] =                    [0.1, -3.2, 3.2]
    var["dphi_j0_ll"] =                     [0.1, -3.2, 3.2]
    var["dphi_bj0_ll"] =                    [0.1, -3.2, 3.2]
    var["dphi_ll_bb"] =                     [0.1, -3.2, 3.2]
    var["dR_ll_bb"] =                       [0.1, 0, 5]
    var["mbb"] =                            [20, 0, 500]
    var["dRbb"] =                           [0.1, 0, 6]
    var["dphi_bb"] =                        [0.1, -3.2, 3.2]
    var["HT2Ratio"] =                       [0.05, 0, 1]
    var["mt2_bb"] =                         [20, 0, 400]
    var["mt2_llbb"]  =                      [20, 0, 500]
    var['nBJets'] =                         [1,0,6]
    var['nSJets'] =                         [1,0,6]
    var['nJets'] =                          [1,0,8]

    return var

def make_residual(variablename, opts) :

    binning = [0.005, -0.6, 0.6]

    h21 = histogram1d("histo_%s_r21" % variablename, binning = binning)
    h20 = histogram1d("histo_%s_r20" % variablename, binning = binning)

    weight_str = 'eventweightbtag'
    chunksize = 100000
    max_to_read = 200000

    data_r20 = []
    data_r21 = []

    with h5py.File(r20_ttbar, 'r', libver = 'latest') as inputfile :

        print "filling R20..."

        dataset = inputfile['superNt']
        n_entries = dataset.size
        n_read = 0

        for x in range(0, dataset.size, chunksize) :
            ds = dataset[x:x+chunksize]
            n_read += ds.size
            weights = ds[weight_str.replace('btag','')]
            weights = np.divide(weights, ds['pupw_period'])
            data = ds[variablename]
            data = data * weights
            data_r20 += list(data)
#            h20.fill(data, weights)

            if n_read >= max_to_read : break

            print " > %.2f %%" % ( (float(n_read) / n_entries) * 100. )

    with h5py.File(r21_ttbar, 'r', libver = 'latest') as inputfile :

        print "filling R21..."
        dataset = inputfile['superNt']
        n_entries = dataset.size
        n_read = 0
        for x in range(0, dataset.size, chunksize) :
            ds = dataset[x:x+chunksize]
            n_read += ds.size
            weights = ds[weight_str]
            data = ds[variablename]
            data = data * weights
            data_r21 += list(data)
#            h21.fill(data, weights)

            if n_read >= max_to_read : break

            print " > %.2f %%" % ( (float(n_read) / n_entries) * 100. )

    vardict = get_variables()[variablename]

    #binning = vardict
    #hdiff = histogram1d("hdiff_%s" % variablename, binning = binning)

    min_size = min( len(data_r20), len(data_r21) )
    data_r20 = np.array( data_r20[:min_size] )
    data_r21 = np.array( data_r21[:min_size] )
    data_diff = data_r21 - data_r20


#    max_x = max(data_diff)
    max_x = 1
    max_x += 0.1

#    data_diff = h21.data[:min_size] - h20.data[:min_size]

    original_binning = binning
    binning = np.arange( binning[1], binning[2], binning[0] )
    h, _ = np.histogram(data_diff, bins = binning)
    maxy = max(h)
    maxy = 1.4 * maxy


    c = canvas("canvas_%s" % variablename)
    c.labels = [variablename, 'entries']
    c.x_bounds = [ -max_x, max_x ]
    c.y_bounds = [0, maxy ]
    c.build()
    c.pad.set_ylim(0, maxy)
    c.pad.set_xlim( -max_x, max_x )

    hdiff = histogram1d("hdiff_%s" % variablename, binning = original_binning)
    hdiff.fill(data_diff)

    hden = histogram1d("hden_%s" % variablename, binning = original_binning)
    hden.fill(data_r20)

    hdiff_x = hdiff.bin_centers()
    max_x = max(hdiff_x)

    hdiff_y = hdiff.divide(hden)
    maxy = max(hdiff_y)
    maxy = 1.2 * maxy

    c.pad.plot(hdiff_x, hdiff_y, color = 'k', label = '(R21 - R20) / R20')
    c.pad.set_ylim(0, maxy)
    c.pad.set_xlim(-max_x, max_x)

    #mean = hdiff.mean()
    #var = hdiff.var()

    #hdiff, _, _ = c.pad.hist( hdiff, bins = binning, color = 'k', label = 'R21-R20', histtype = 'step', lw = 1)
    #hdiff, _, _ = c.pad.hist( hdiff.data[~np.isnan(hdiff.data)], bins = binning, color = 'k', label = 'R21-R20', histtype = 'step', lw = 1)

    # legend
    handles, labels = c.pad.get_legend_handles_labels()
    new_handles = [Line2D([],[], c = 'k')]
    lables = ["Release 21 - Release 20"]
    c.pad.legend(handles = new_handles, labels = labels, loc = 'best', frameon = False, fontsize = 12, numpoints = 1)

    # text
    #size = 18
    #legopts = dict(transform = c.pad.transAxes)
    #legopts.update( dict( va = 'top', ha = 'left' ) )
    #c.pad.text(0.05, 0.84, 'Mean:  %.2f' % mean, size = size, **legopts)
    #c.pad.text(0.05, 0.8, '$\\sigma$ : %.2f' % var, size = size, **legopts)



    # save 
    outdir = opts.outdir
    utils.mkdir_p(outdir)
    if not outdir.endswith('/') : outdir += "/"
    save_name = outdir + "ttbar_residuals_%s.pdf" % variablename
    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    c.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)
    
        
        
def do_comp_plots(variables, options) :

    histos = []
    colors = []
    labels = []

    histo_dict = {}
    plots_dict = {}

    

    sample_files = [r20_ttbar, r21_ttbar]
    colors = ['r', 'b']
    names = ["R20", "R21"]

    chunksize = 100000
    max_to_read = 20000000000

    for variable in variables :

        h_for_var = []

        p = plot1d("ttbar_comp_r20_r21_%s" % variable)
        p.bounds = get_variables()[variable]

        for isf, sf in enumerate(sample_files) :
            h = histogram1d("histo_%s_%s" % (variable, names[isf]), binning = p.bounds)
            h_for_var.append(h)

        histo_dict[variable] = h_for_var
        plots_dict[variable] = p

    for variable in variables :

        for isf, sf in enumerate(sample_files) :

            with h5py.File(sf, 'r', libver = 'latest') as datafile :

                dataset = datafile['superNt']

                n_read = 0
                n_entries = dataset.size
                if max_to_read < n_entries : n_entries = max_to_read

                for x in range(0, dataset.size, chunksize) :
                    ds = dataset[x:x+chunksize]
                    #ds = ds[ (ds['nBJets'] == 2) & (ds['mbb'] > 140) ]
                    ds = ds[ (ds['nBJets'] == 2) & (ds['nSJets'] == 0) ]
                    n_read += ds.size

#                    weights = ds['eventweightbtag']
                    weights = None
                    if isf == 0 :
                        weights = ds['eventweight']
                        #pupw = ds['pupw']

                        #print weights[:10]
                        #print pupw[:10]
                        #weights = np.divide(weights, pupw)
                        #print weights[:10]
                    elif isf == 1 :
                        weights = ds['eventweightbtag']
                        period_weights = ds['pupw_period']
                        weights = np.divide(weights, period_weights)

                    data = ds[variable]

                    histo_dict[variable][isf].fill(data, weights)
                    print " > %s - %s : %.2f %%" % ( variable, names[isf],  (float(n_read) / n_entries)  )

                    if n_read >= max_to_read : break


            labels.append(names[isf])

    for variable in variables :
        for ih, h in enumerate(histos) :
            histo_dict[variable][ih].add_overflow()

    print_yields = True
    n_var = len(variables)

    for ivar, var in enumerate(variables) :
        histos = []
        for isf, sf in enumerate(sample_files) :
            histos.append(histo_dict[var][isf])

        yield_r20, yield_error_r20 = histos[0].integral_and_error()
        yield_r21, yield_error_r21 = histos[1].integral_and_error()
        yield_ratio = 0
        if yield_r20 != 0 :
            yield_ratio = yield_r21 / yield_r20

        rc = ratio_canvas("ratio_canvas_%s" % var)
        if options.logy :
            rc.logy = True

        rc.labels = [var, 'Entries']
        rc.rlabel = 'R21 / R20'
        rc.build()

        rc.upper_pad.hist( [h.data for h in histos],
                            weights = [h.weights for h in histos],
                            bins = plots_dict[var].binning,
                            color = colors,
                            label = labels,
                            stacked = False,
                            histtype = 'step',
                            lw = 1 )


        yerrors = []
        for ih, h in enumerate(histos) :
            yvals = h.histogram
            xvals = h.bin_centers()
            yerr = h.y_error()
            yerrors.append(yerr)
            rc.upper_pad.errorbar(xvals, yvals, yerr = yerr, fmt = 'none', color = colors[ih])

        if print_yields and yield_r20 != 0 :
            print_yields = False
            print "R20 : %.2f +/- %.2f" % (yield_r20, yield_error_r20)
            print "R21 : %.2f +/- %.2f" % (yield_r21, yield_error_r21)
            print "R21/R20 : %.2f" % (yield_r21 / yield_r20)

        maxy = -1
        miny = 0
        multiplier = 1.4
        for h in histos :
            if h.maximum() > maxy :
                maxy = h.maximum()
        if options.logy :
            miny = 1e-2
            multiplier = 1e3

        maxy = multiplier * maxy
        rc.upper_pad.set_ylim(miny, maxy)

        # legend
        handles, labels = rc.upper_pad.get_legend_handles_labels()
        new_handles = [Line2D([],[], c = colors[0]), Line2D([], [], c = colors[1])]
        #labels = ["$Wt$ Release 20", "$Wt$ Release 21"]
        labels = ["$t\\bar{t}$ Release 20", "$t\\bar{t}$ Release 21"]
        rc.upper_pad.legend(handles = new_handles, labels = labels, loc = 'best', frameon = False, fontsize = 12, numpoints = 1)

        # labels
        size = 18
        text = 'ATLAS'
        legopts = dict(transform = rc.upper_pad.transAxes)
        legopts.update( dict(va = 'top', ha = 'left') ) 
        rc.upper_pad.text(0.05, 0.97, text, size = size, style = 'italic', weight = 'bold', **legopts)
        rc.upper_pad.text(0.23, 0.97, 'Internal', size = size, **legopts)

        # error bars
        #stat_error_bands = []

        #for ih, h in enumerate(histos) :
        #    x_error = np.zeros(len(h.y_error()))
        #    y_error = h.y_error()
        #    stat_band = errorbars.error_hatches(h.bins[:-1], h.histogram, x_error, y_error, plots_dict[var].bin_width)

        #    rc.upper_pad.add_collection(stat_band)


        # lower pad
        ratio_yvalues = histos[-1].divide(histos[0])
        ratio_xvalues = np.array(histos[0].bin_centers())
        ratio_yvalues [ ratio_yvalues == 0 ] = -10
        rc.lower_pad.plot(ratio_xvalues, ratio_yvalues, 'ko', markersize = 2, zorder = 1000)

        err_num = np.array( yerrors[1] )
        num_vals = np.array(histos[1].histogram)
        err_num = np.divide(err_num, num_vals)
        err_den = np.array( yerrors[0] )
        den_vals = np.array(histos[0].histogram)
        err_den = np.divide(err_den, den_vals)

        ratio_errors = ratio_yvalues * np.sqrt( err_num ** 2 + err_den ** 2 )
        rc.lower_pad.errorbar(ratio_xvalues, ratio_yvalues, yerr = ratio_errors, fmt = 'none', color = 'k')

        # unity
        minx = get_variables()[var][1]
        maxx = get_variables()[var][2]

        x = [minx, maxx]

        y = [1.0, 1.0]
        rc.lower_pad.plot(x, y, 'r--', lw = 1)

        # save
        outdir = options.outdir
        utils.mkdir_p(outdir)
        if not outdir.endswith('/') : outdir += "/"
        process = "ttbar"
        if "Wt" in r20_ttbar : process = "wt"
        save_name = outdir + "%s_comp_%s.pdf" % (process, var)
        print " >>> [%02d/%02d] saving plot to : %s" % (ivar+1, n_var, os.path.abspath(save_name))
        rc.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)

def do_residuals(variables, opts) :

    n_vars = len(variables)

    for  ivar, var in enumerate(variables) :
        print "[%02d/%02d] %s" % (ivar+1, n_vars, var)
        make_residual(var, opts)

def main() :

    parser = OptionParser()
    parser.add_option("--residuals", help = "make residual plots between ttbar samples", action = "store_true", default = False)
    parser.add_option("--comp", help = "make comparison plots between the ttbars", action = "store_true", default = False)
    parser.add_option("-v", "--varlist", help = "provide select var (comma separated is legit)", default = "")
    parser.add_option("-o", "--outdir", help = "output directory to dump plots", default = "./")
    parser.add_option("--logy", action = 'store_true', default = False)
    (options, args) = parser.parse_args()

    variables = get_variables().keys()

    if options.varlist != "" :
        tmp = []
        varlist = options.varlist.split(",")
        for v in varlist :
            if v in variables :
                tmp.append(v)
        if len(tmp) == 0 :
            print "you requested varlist (=%s) but none of those variables are found" % options.varlist
            sys.exit()
        variables = tmp

    if options.residuals :
        do_residuals(variables, options)

    if options.comp :
        do_comp_plots(variables, options)

    print "done"

    

            
    

if __name__ == "__main__" :
    main()

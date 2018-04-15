#!/usr/bin/env python

from optparse import OptionParser
import sys
import os

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

filedir_r20 = "/data/uclhc/uci/user/dantrim/ntuples/n0234/m_apr12_rel21val/data/h5/"
filedir_r21 = "/data/uclhc/uci/user/dantrim/ntuples/n0301/data/h5/"
lumi_table = "/data/uclhc/uci/user/dantrim/n0301val/lumi_tables/lumi_table_all.txt"

class Options :
    def __init__(self) :
        print "hello"

def get_variables(region) :

    var = {}

    var["nVtx"] = {"zee" : [1, 0, 35] }
    var["avgMu"] = {"zee" : [1, 0, 40] }

    var["l0_d0"] = {"zee" : [0.001, -0.07, 0.07] }
    var["l1_d0"] = {"zee" : [0.001, -0.07, 0.07] }
    var["l0_d0sig"] = {"zee" : [0.1, -3, 3] }
    var["l1_d0sig"] = {"zee" : [0.1, -3, 3] }
    var["l0_z0sinTheta"] = {"zee" : [0.01, -0.2, 0.2] }
    var["l1_z0sinTheta"] = {"zee" : [0.01, -0.2, 0.2] }

    var["e0_clusE"] = {"zee": [1, 0, 250] }
    var["e1_clusE"] = {"zee": [1, 0, 200] }
    var["e0_clusEtaBE"] = {"zee": [0.1, -2.8, 2.8] }
    var["e1_clusEtaBE"] = {"zee": [0.1, -2.8, 2.8] }
    var["e0_trackPt"] = {"zee": [1, 0, 200] }
    var["e1_trackPt"] = {"zee": [1, 0, 150] }
    var["e0_trackEta"] = {"zee": [0.1, -2.8, 2.8] }
    var["e1_trackEta"] = {"zee": [0.1, -2.8, 2.8] }

    var["l0_etconetopo20"] = {"zee": [0.2, -5, 8] }
    var["l1_etconetopo20"] = {"zee": [0.2, -5, 8] }
    var["l0_etconetopo30"] = {"zee": [0.2, -5, 8] }
    var["l1_etconetopo30"] = {"zee": [0.2, -5, 8] }
    var["l0_ptvarcone20"] = {"zee": [0.1, 0, 5]}
    var["l1_ptvarcone20"] = {"zee": [0.1, 0, 5]}
    var["l0_ptvarcone30"] = {"zee": [0.1, 0, 10]}
    var["l1_ptvarcone30"] = {"zee": [0.1, 0, 10]}
    

    var["l0_pt"] = {"zee" : [2, 20, 120] }
    var["l1_pt"] = {"zee" : [2, 20, 120] }
    var["l0_eta"] = {"zee" : [0.1, -2.8, 2.8] }
    var["l1_eta"] = {"zee" : [0.1, -2.8, 2.8] }
    var["mll"] =   {"zee" : [1, 50, 130] }
    var["pTll"] = {"zee" : [5, 0, 200] }
    var["dphi_ll"] = {"zee" : [0.1, -3.5, 3.5] }
    var["dRll"] = {"zee" :[0.05, 0, 5] }
    var["deta_ll"] = {"zee" : [0.2, -4, 4] }

    var["met"] = {"zee" : [2, 0, 150] }
    var["metPhi"] = {"zee": [0.1, -3.5, 3.5]}
    var["metTST"] = {"zee": [2, 0, 75] }
    var["dphi_met_ll"] = {"zee": [0.1, -3.2, 3.2] }
    var["met_ele_et"] = {"zee": [2, 0, 200] }
    var["met_ele_phi"] = {"zee": [0.1, -3.2, 3.2] }
    var["met_ele_sumet"] = {"zee": [2, 0, 200] }
    var["met_jet_et"] = {"zee": [2, 0, 200] }
    var["met_jet_phi"] = {"zee": [0.1, -3.2, 3.2] }
    var["met_jet_sumet"] = {"zee": [2, 0, 200] }
    var["met_muo_et"] = {"zee": [2, 0, 200] }
    var["met_muo_phi"] = {"zee": [0.1, -3.2, 3.2] }
    var["met_muo_sumet"] = {"zee": [2, 0, 200] }
    var["met_soft_et"] = {"zee": [2, 0, 200] }
    var["met_soft_phi"] = {"zee": [0.1, -3.2, 3.2] }
    var["met_soft_sumet"] = {"zee": [2, 0, 200] }


    var["nJets"] = {"zee" : [1, 0, 15] }
    var["nBJets"] = {"zee" : [1, 0, 8] }
    var["nSJets"] = {"zee" : [1, 0, 8] }

    for v in var :
        if region not in var[v] :
            print "get_variables    ERROR variable (=%s) not defined for region (=%s)" % (v, region)
            sys.exit()

    out = {}
    for v in var :
        out[v] = var[v][region]

    return out

def get_regions() :

    regions = []

    r = region.Region("zee", "$Z\rightarrow ee$ selection")
    r.tcut = "nJets==0 && l0_pt>25 && l1_pt>20 && nLeptons==2 && nElectrons==2"
    regions.append(r)
    
    return regions

def get_samples(name, filedir, options) :

    filelist_dir = "/data/uclhc/uci/user/dantrim/n0301val/susynt-read/filelists/n0301_data/"

    runs_to_consider = []
    lines = open(options.runslist).readlines()
    for line in lines :
        if not line : continue
        line = line.strip()
        if line.startswith("#") : continue
        runs_to_consider.append(line)

    run_string = (",").join(runs_to_consider)

    colors = {}
    colors["R20"] = 'r'
    colors["R21"] = 'k'

    s = sample.Sample(name, name)
    s.is_data = True
    s.scalefactor = 1.0
    s.color = colors[name]
    s.load(filelist_dir, filedir, run_string)

    sample_lumi = 0.0

    lumi_lines = [l.strip() for l in open(lumi_table).readlines()]
    for r in runs_to_consider :
        for ll in lumi_lines :
            lr = ll.split()
            if lr[0] == r :
                sample_lumi += float(lr[1])

    s.lumi = sample_lumi

    return s, sample_lumi


#def make_comp_plot(r20sample, r21sample, vname, vbounds, opts) :
def make_comp_plot(r20sample, r21sample, variable_dict, opts) :

    # make the plot object
  #  p = plot1d("comp_r20_r21_%s_%s" % (opts.region,vname), vname)
  #  p.bounds = vbounds

  #  print "plot name = %s" % p.name
  #  print "plot var  = %s" % p.vartoplot
  #  print "plot binning = %s" % p.binning
  #  print "plot bounds = %s" % p.bounds
  #  print "bin width = %.2f" % p.bin_width
  #  print "xlow = %.2f" % p.x_low
  #  print "high = %.2f" % p.x_high

    histos = []
    colors = []
    labels = []

    histo_dict = {}
    plots_dict = {}

    samples = [r20sample, r21sample]

    for variable in variable_dict :
        h_for_var = []

        p = plot1d("comp_r20_r21_%s_%s" % (opts.region, variable), variable)
        p.bounds = variable_dict[variable]

        for s in samples :
            h = histogram1d("histo_%s_%s" % (s.name, variable), binning = p.bounds)
            h_for_var.append(h)

        histo_dict[variable] = h_for_var
        plots_dict[variable] = p

    for isample, s in enumerate(samples) :
        chain = s.chain()
        for ic, c in enumerate(chain) :
            for varname, varbounds in variable_dict.iteritems() :
                data = c[varname]
                histo_dict[varname][isample].fill(data)

        labels.append(s.name)
        colors.append(s.color)

    for varname, varbounds in variable_dict.iteritems() :

        histos = []
        for isample, sample in enumerate(samples) :
            histos.append(histo_dict[varname][isample])
        for h in histos :
            h.add_overflow()

        rc = ratio_canvas("ratio_canvas_%s" % varname)
        if opts.do_logy :
            rc.logy = True
        rc.labels = [varname, 'Entries']
        rc.rlabel = 'R21 / R20'
        rc.build()

       # print "%s : R20 = %s" % (varname, histos[0].histogram)
       # print "%s : R21 = %s" % (varname, histos[1].histogram)
       # sys.exit()

        rc.upper_pad.hist( [h.data for h in histos],
                            bins = plots_dict[varname].binning,
                            color = colors,
                            label = labels,
                            stacked = False,
                            histtype = 'step',
                            lw = 1)

        maxy = -1
        miny = 0
        multiplier = 1.4
        for h in histos :
            if h.maximum() > maxy :
                maxy = h.maximum()
        if opts.do_logy :
            miny = 1e-2
            multiplier = 1e2

        maxy = multiplier * maxy
        rc.upper_pad.set_ylim(miny, maxy)

        # legend
        handles, labels = rc.upper_pad.get_legend_handles_labels()
        new_handles = [Line2D([],[],c=s.color) for s in samples]
        labels = ["Release 20", "Release 21"]
        rc.upper_pad.legend(handles = new_handles, labels = labels, loc = 'best', frameon = False, fontsize = 12, numpoints = 1)

        # labels
        size = 18
        text = 'ATLAS'
        legopts = dict(transform = rc.upper_pad.transAxes)
        legopts.update( dict(va = 'top', ha = 'left') )
        rc.upper_pad.text(0.05, 0.97, text, size = size, style = 'italic', weight = 'bold', **legopts)
    
        rc.upper_pad.text(0.23, 0.97, 'Internal', size = size, **legopts)
    
        lumi = samples[0].lumi
        unit = "pb"
    
        if lumi > 1000. :
            lumi = lumi / 1000.
            unit = "fb"
    
        rc.upper_pad.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, %.2f %s$^{-1}$' % (lumi,unit), size = 0.75 * size, **legopts)

        # error bars
        errors =  []
        for ih, h in enumerate(histos) :
            data_x = h.bin_centers()
            data_y = h.histogram
            data_y [ data_y == 0 ] = -5
            data_err_low, data_err_high = errorbars.poisson_interval(h.histogram)
            data_err_low = data_y - data_err_low
            data_err_high = data_err_high - data_y
            data_err = [data_err_low, data_err_high]
            errors.append(data_err)
            rc.upper_pad.errorbar(data_x, data_y, yerr = data_err, fmt = 'none', color = colors[ih])

        # lower pad
        ratio_yvalues = histos[-1].divide(histos[0])
        ratio_xvalues = np.array(histos[0].bin_centers())
        ratio_yvalues [ ratio_yvalues == 0 ] = -10
        #rc.lower_pad.plot(ratio_xvalues, ratio_yvalues, fmt = 'none', color = 'k')
        rc.lower_pad.plot(ratio_xvalues, ratio_yvalues, 'ko', markersize = 2,  zorder = 1000)
        rc.lower_pad.set_ylim(0, 2)

        errors_r20 = errors[0]
        errors_r21 = errors[1]
    
        ratio_err_low = []
        ratio_err_high = []
    

        r20_values = histos[0].histogram
        r21_values = histos[1].histogram

        e20_low = np.abs(errors_r20[0])
        e21_low = np.abs(errors_r21[0])

        e20_high = np.abs(errors_r20[1])
        e21_high = np.abs(errors_r21[1])

        rel_e20_low = None
        rel_e21_low = None
        rel_e20_high = None
        rel_e21_high = None

        with np.errstate(divide='ignore', invalid='ignore') :

            rel_e20_low = np.true_divide( e20_low, r20_values )
            rel_e20_low[ ~ np.isfinite(rel_e20_low) ] = 0

            rel_e21_low = np.true_divide( e21_low, r21_values )
            rel_e21_low[ ~ np.isfinite(rel_e21_low) ] = 0

            rel_e20_high = np.true_divide( e20_high, r20_values )
            rel_e20_high[ ~ np.isfinite(rel_e20_high) ] = 0

            rel_e21_high = np.true_divide( e21_high, r21_values )
            rel_e21_high[ ~ np.isfinite(rel_e21_high) ] = 0

        e_high = ratio_yvalues * np.sqrt( np.power(rel_e20_high, 2) + np.power(rel_e21_high, 2) )
        e_low = ratio_yvalues * np.sqrt( np.power(rel_e20_low, 2) + np.power(rel_e21_low, 2) )
        ratio_err = [e_low, e_high]
        rc.lower_pad.errorbar(ratio_xvalues, ratio_yvalues, yerr = ratio_err, fmt = 'none', color = 'k')


        #for iy in range(len(ratio_yvalues)) :
    
        #    ratio_value = ratio_yvalues[iy]
    
        #    r20_value = r20_values[iy]
        #    r21_value = r21_values[iy]
    
        #    e20_low = errors_r20[0][iy]
        #    e21_low = errors_r21[0][iy]
    
        #    e20_high = errors_r20[1][iy]
        #    e21_high = errors_r21[1][iy]
    
        #    rel_e20_low = 0
        #    rel_e21_low = 0
        #    rel_e20_high = 0
        #    rel_e21_high = 0
    
        #    if r20_value != 0 :
    
        #        rel_e20_low = abs(e20_low) / r20_value
        #        rel_e20_high = abs(e20_high) / r20_value

        #    if r21_value != 0 :

        #        rel_e21_low = abs(e21_low) / r21_value
        #        rel_e21_high = abs(e21_high) / r21_value
    
        #    e_high = ratio_value * sqrt( rel_e20_high ** 2 + rel_e21_high ** 2)
        #    e_low = ratio_value * sqrt( rel_e20_low ** 2 + rel_e21_low ** 2)
        #    ratio_err_low.append(e_low)
        #    ratio_err_high.append(e_high)
    
        #ratio_err = [ratio_err_low, ratio_err_high]
        #rc.lower_pad.errorbar(ratio_xvalues, ratio_yvalues, yerr = ratio_err, fmt = 'none', color = 'k')

        line_y = [1.0, 1.0]
        line_x = [plots_dict[varname].x_low, plots_dict[varname].x_high]
        rc.lower_pad.plot(line_x, line_y, 'r-', zorder=1)

    

        ##############################
        # save
        outdir = opts.output_dir
        utils.mkdir_p(outdir)
        if not outdir.endswith('/') : outdir += "/"
        suffix = ""
        if opts.suffix != "" :
            suffix = "_" + opts.suffix
        save_name = outdir + "%s_%s.pdf" % (plots_dict[varname].name, suffix)
        print " >>> Saving plot to : %s" % os.path.abspath(save_name)
        rc.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)
                                


#    for s in samples :
#        chain = s.chain()
#        for ic, c in enumerate(chain) :
#            for varname, varbounds in variable_dict.iteritems() :
#                data = c[varname]
#
#
#        h = histogram1d("histo_%s_%s" % (s.name, vname), binning = p.bounds)
#        chain = s.chain()
#        for ic, c in enumerate(chain) :
#            data = c[vname]
#            weights = np.ones(len(data))
#            #if absval :
#            #    data = np.absolute(data)
#            h.fill(data, weights)
#
#        labels.append(s.name)
#        colors.append(s.color)
#        h.add_overflow()
#        histos.append(h)
#
#        #print "name = %s : histogram = %s" % (s.name, h.histogram)
#
#    # plotting
#    rc = ratio_canvas("ratio_canvas_%s" % vname)
#    if opts.do_logy :
#        rc.logy = True
#    rc.labels = [vname, 'Entries']
#    rc.rlabel = 'R21 / R20'
#    rc.build()
#
#    # upper pad
#
##    print "shape 0 : %s" % histos[0].histogram
#
#
#    rc.upper_pad.hist( [h.data for h in histos],
#                        weights = [h.weights for h in histos],
#                        bins = p.binning,
#                        color = colors,
#                        label = labels,
#                        stacked = False,
#                        histtype = 'step',
#                        lw = 1)
#
#    maxy = -1
#    miny = 0
#    multiplier = 1.65
#    for h in histos :
#        if h.maximum() > maxy :
#            maxy = h.maximum()
#    if opts.do_logy :
#        miny = 1e-2
#        multiplier = 1e2
#
#    maxy = multiplier * maxy
#    rc.upper_pad.set_ylim(miny, maxy)
#
#    # legend
#    handles, labels = rc.upper_pad.get_legend_handles_labels()
#    new_handles = [Line2D([], [], c = s.color) for s in samples]
#    labels = ["Release 20", "Release 21"]
#    rc.upper_pad.legend(handles = new_handles, labels = labels, loc = 'best', frameon = False, fontsize = 12, numpoints = 1)
#
#    # labels
#    size = 18
#    text = 'ATLAS'
#    legopts = dict(transform = rc.upper_pad.transAxes)
#    legopts.update( dict(va = 'top', ha = 'left') )
#    rc.upper_pad.text(0.05, 0.97, text, size = size, style = 'italic', weight = 'bold', **legopts)
#
#    rc.upper_pad.text(0.23, 0.97, 'Internal', size = size, **legopts)
#
#    lumi = samples[0].lumi
#    unit = "pb"
#
#    if lumi > 1000. :
#        lumi = lumi / 1000.
#        unit = "fb"
#
#    rc.upper_pad.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, %.2f %s$^{-1}$' % (lumi,unit), size = 0.75 * size, **legopts)
#
#    # error bars
#    errors =  []
#    for ih, h in enumerate(histos) :
#        data_x = h.bin_centers()
#        data_y = h.histogram
#        data_y [ data_y == 0 ] = -5
#        data_err_low, data_err_high = errorbars.poisson_interval(h.histogram)
#        data_err_low = data_y - data_err_low
#        data_err_high = data_err_high - data_y
#        data_err = [data_err_low, data_err_high]
#        errors.append(data_err)
#        rc.upper_pad.errorbar(data_x, data_y, yerr = data_err, fmt = 'none', color = colors[ih])
#
#    # lower pad
#    ratio_yvalues = histos[-1].divide(histos[0])
#    ratio_xvalues = np.array(histos[0].bin_centers())
#    ratio_yvalues [ ratio_yvalues == 0 ] = -10
#    #rc.lower_pad.plot(ratio_xvalues, ratio_yvalues, fmt = 'none', color = 'k')
#    rc.lower_pad.plot(ratio_xvalues, ratio_yvalues, 'ko', markersize = 2,  zorder = 1000)
#    rc.lower_pad.set_ylim(0, 2)
#
#    errors_r20 = errors[0]
#    errors_r21 = errors[1]
#
#    ratio_err_low = []
#    ratio_err_high = []
#    
#    for iy in range(len(ratio_yvalues)) :
#
#        ratio_value = ratio_yvalues[iy]
#
#        r20_value = histos[0].histogram
#        r20_value = r20_value[iy]
#
#        r21_value = histos[0].histogram
#        r21_value = r21_value[iy]
#
#        e20_low = errors_r20[0][iy]
#        e21_low = errors_r21[0][iy]
#
#        e20_high = errors_r20[1][iy]
#        e21_high = errors_r21[1][iy]
#
#        rel_e20_low = 0
#        rel_e21_low = 0
#        rel_e20_high = 0
#        rel_e21_high = 0
#
#        if r20_value != 0 :
#
#            rel_e20_low = abs(e20_low) / r20_value
#            rel_e21_low = abs(e21_low) / r21_value
#
#            rel_e20_high = abs(e20_high) / r20_value
#            rel_e21_high = abs(e21_high) / r21_value
#
#        e_high = ratio_value * sqrt( rel_e20_high ** 2 + rel_e21_high ** 2)
#        e_low = ratio_value * sqrt( rel_e20_low ** 2 + rel_e21_low ** 2)
#        ratio_err_low.append(e_low)
#        ratio_err_high.append(e_high)
#
#    ratio_err = [ratio_err_low, ratio_err_high]
#    rc.lower_pad.errorbar(ratio_xvalues, ratio_yvalues, yerr = ratio_err, fmt = 'none', color = 'k')
#
#
#        #e_low = sqrt( e20_low ** 2 + e21_low ** 2 )
#        #e_high = sqrt( e20_high ** 2 + e21_high ** 2 )
#
#    
#
#    line_y = [1.0, 1.0]
#    line_x = [p.x_low, p.x_high]
#    rc.lower_pad.plot(line_x, line_y, 'r-', zorder=1)
#
#
#    #################################
#    # save
#    outdir = opts.output_dir
#    utils.mkdir_p(outdir)
#    if not outdir.endswith("/") :
#        outdir += "/"
#    suffix = ""
#    if opts.suffix != "" :
#        sufix = "_" + opts.suffix
#    save_name = outdir + "%s_%s.pdf" % (p.name, suffix)
#    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
#    rc.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)


def main() :

    parser = OptionParser()
    parser.add_option("--runslist", help = "provide a list of runs to make plots for", default = "")
    parser.add_option("-r", "--region", help = "provide region to make plots for", default = "")
    parser.add_option("-o", "--output", help = "output directory for plots", default = "./")
    parser.add_option("--logy", default = False, action = "store_true", help = "Set plots to have log y-axis")
    parser.add_option("-v", "--var", default = "", help = "select a specific variable to plot")
    parser.add_option("--suffix", default = "", help = "filename suffix for output plots")
    (options, args) = parser.parse_args()

    opts = Options()
    opts.runslist = options.runslist
    opts.output_dir = options.output
    opts.do_logy = options.logy
    opts.select_var = options.var
    opts.suffix = options.suffix
    opts.region = options.region

    if opts.runslist == "" :
        print "ERROR Did not provide a runslist"
        sys.exit()

    if opts.region == "" :
        print "ERROR Did not provide a region"
        sys.exit()

    variables = get_variables(options.region)
    if opts.select_var != "" :
        if opts.select_var not in variables :
            print "ERROR Requested variable (=%s) not found in loaded variables" % opts.select_var
            sys.exit()

        tmp = {}
        tmp[opts.select_var] = variables[opts.select_var]
        variables = tmp

    regions = get_regions()
    loaded_region_names = [r.name for r in regions]
    if opts.region not in loaded_region_names :
        print "ERROR Requested region (=%s) not found in loaded regions: %s" % (opts.region, [r for r in loaded_region_names])
        sys.exit()

    samples_r20, lumi_r20 = get_samples("R20", filedir_r20, opts)
    samples_r21, lumi_r21 = get_samples("R21", filedir_r21, opts)

    region_to_use = None
    for r in regions :
        if r.name == opts.region :
            region_to_use = r
            break

    # cache
    variables_from_region = sample_utils.get_variables_from_tcut(region_to_use.tcut)
    for v in variables :
        if v not in variables_from_region :
            variables_from_region.append(v)
    extra_vars = ["isMC"] #, "run", "lumi_block", "year"]
    required_vars = []
    required_vars += variables_from_region
    required_vars += extra_vars

    cacher = sample_cacher.SampleCacher("./") 
    cacher.samples = [samples_r20, samples_r21]
    cacher.region = region_to_use
    cacher.fields = required_vars
    print str(cacher)
    cacher.cache()

    n_plots = len(variables)
    make_comp_plot(samples_r20, samples_r21, variables, opts)
#    for iplot, v in enumerate(variables) :
#        print 55 * "-"
#        print "[%02d/%02d] %s" % (iplot+1, n_plots, v)
#        make_comp_plot(samples_r20, samples_r21, variables, opts)
#        #make_comp_plot(samples_r20, samples_r21, v, variables[v], opts)


if __name__ == "__main__" :
    main()

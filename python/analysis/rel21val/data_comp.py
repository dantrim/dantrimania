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
filedir_r20 = "/data/uclhc/uci/user/dantrim/ntuples/n0234/n_apr22_rel21val/h5/"
filedir_r21 = "/data/uclhc/uci/user/dantrim/ntuples/n0302/data/h5/"
lumi_table = "/data/uclhc/uci/user/dantrim/n0301val/lumi_tables/lumi_table_all.txt"

class Options :
    def __init__(self) :
        print "hello"

def get_variables(region) :

    var = {}

    region_to_use = "zee"

    var["nVtx"] =                           {"zee" : [1, 0, 35] }
    var["avgMu"] =                          {"zee" : [1, 0, 40] }

    var["l0_d0"] =                          {"zee" : [0.001, -0.07, 0.07] }
    var["l1_d0"] =                          {"zee" : [0.001, -0.07, 0.07] }
    var["l0_d0sig"] =                       {"zee" : [0.1, -3, 3] }
    var["l1_d0sig"] =                       {"zee" : [0.1, -3, 3] }
    var["l0_z0sinTheta"] =                  {"zee" : [0.01, -0.2, 0.2] }
    var["l1_z0sinTheta"] =                  {"zee" : [0.01, -0.2, 0.2] }

    var["e0_clusE"] =                       {"zee": [1, 0, 250] }
    var["e1_clusE"] =                       {"zee": [1, 0, 200] }
    var["e0_clusEtaBE"] =                   {"zee": [0.1, -2.8, 2.8] }
    var["e1_clusEtaBE"] =                   {"zee": [0.1, -2.8, 2.8] }
    var["e0_trackPt"] =                     {"zee": [1, 0, 200] }
    var["e1_trackPt"] =                     {"zee": [1, 0, 150] }
    var["e0_trackEta"] =                    {"zee": [0.1, -2.8, 2.8] }
    var["e1_trackEta"] =                    {"zee": [0.1, -2.8, 2.8] }

    var["mu0_idTrackPt"] =                  {"zee": [2, 0, 200] }
    var["mu1_idTrackPt"] =                  {"zee": [2, 0, 200] }
    var["mu0_idTrackEta"] =                 {"zee": [0.1, -3, 3] }
    var["mu1_idTrackEta"] =                 {"zee": [0.1, -3, 3] }
    var["mu0_idTrackPhi"] =                 {"zee": [0.1, -3.2, 3.2] }
    var["mu1_idTrackPhi"] =                 {"zee": [0.1, -3.2, 3.2] }
    var["mu0_msTrackPt"] =                  {"zee": [2, 0, 200] }
    var["mu1_msTrackPt"] =                  {"zee": [2, 0, 200] }
    var["mu0_msTrackEta"] =                 {"zee": [0.1, -3, 3] }
    var["mu1_msTrackEta"] =                 {"zee": [0.1, -3, 3] }
    var["mu0_msTrackPhi"] =                 {"zee": [0.1, -3.2, 3.2] }
    var["mu1_msTrackPhi"] =                 {"zee": [0.1, -3.2, 3.2] }


    var["l0_etconetopo20"] =                {"zee": [0.2, -5, 8] }
    var["l1_etconetopo20"] =                {"zee": [0.2, -5, 8] }
    var["l0_etconetopo30"] =                {"zee": [0.2, -5, 8] }
    var["l1_etconetopo30"] =                {"zee": [0.2, -5, 8] }
    var["l0_ptvarcone20"] =                 {"zee": [0.1, 0.7, 5]}
    var["l1_ptvarcone20"] =                 {"zee": [0.1, 0.7, 5]}
    var["l0_ptvarcone30"] =                 {"zee": [0.1, 0.7, 10]}
    var["l1_ptvarcone30"] =                 {"zee": [0.1, 0.7, 10]}
    

    var["l0_pt"] =                          {"zee" : [2, 20, 120] }
    var["l1_pt"] =                          {"zee" : [2, 20, 120] }
    var["l0_eta"] =                         {"zee" : [0.1, -2.8, 2.8] }
    var["l1_eta"] =                         {"zee" : [0.1, -2.8, 2.8] }
    var["mll"] =                            {"zee" : [1, 50, 130] }
    var["pTll"] =                           {"zee" : [5, 0, 200] }
    var["dphi_ll"] =                        {"zee" : [0.1, -3.5, 3.5] }
    var["dRll"] =                           {"zee" :[0.05, 0, 5] }
    var["deta_ll"] =                        {"zee" : [0.2, -4, 4] }

    var["met"] =                            {"zee" : [2, 0, 150] }
    var["metPhi"] =                         {"zee": [0.1, -3.5, 3.5]}
    var["metTST"] =                         {"zee": [2, 0, 75] }
    var["dphi_met_ll"] =                    {"zee": [0.1, -3.2, 3.2] }
    var["met_ele_et"] =                     {"zee": [2, 0, 200] }
    var["met_ele_phi"] =                    {"zee": [0.1, -3.2, 3.2] }
    var["met_ele_sumet"] =                  {"zee": [2, 0, 200] }
    var["met_jet_et"] =                     {"zee": [2, 0, 200] }
    var["met_jet_phi"] =                    {"zee": [0.1, -3.2, 3.2] }
    var["met_jet_sumet"] =                  {"zee": [2, 0, 200] }
    var["met_muo_et"] =                     {"zee": [2, 0, 200] }
    var["met_muo_phi"] =                    {"zee": [0.1, -3.2, 3.2] }
    var["met_muo_sumet"] =                  {"zee": [2, 0, 200] }
    var["met_soft_et"] =                    {"zee": [2, 0, 60] }
    var["met_soft_phi"] =                   {"zee": [0.1, -3.2, 3.2] }
    var["met_soft_sumet"] =                 {"zee": [2, 0, 200] }

    var["mT_full"] =                        {"zee": [2, 0, 150] }

    var["nJets"] =                          {"zee" : [1, 0, 15] }
    var["nBJets"] =                         {"zee" : [1, 0, 8] }
    var["nSJets"] =                         {"zee" : [1, 0, 8] }

    var["j0_pt"] =                          {"zee" : [2, 0, 300] }
    var["j0_eta"] =                         {"zee" : [0.1, -3, 3] }
    var["j0_phi"] =                         {"zee" : [0.1, -3.2, 3.2] }
    var["j1_pt"] =                          {"zee" : [2, 0, 300] }
    var["j1_eta"] =                         {"zee" : [0.1, -3, 3] }
    var["j1_phi"] =                         {"zee" : [0.1, -3.2, 3.2] }
    var["sj0_pt"] =                         {"zee" : [2, 0, 300] }
    var["sj0_eta"] =                        {"zee" : [0.1, -3, 3] }
    var["sj0_phi"] =                        {"zee" : [0.1, -3.2, 3.2] }
    var["sj1_pt"] =                         {"zee" : [2, 0, 300] }
    var["sj1_eta"] =                        {"zee" : [0.1, -3, 3] }
    var["sj1_phi"] =                        {"zee" : [0.1, -3.2, 3.2] }
    var["bj0_pt"] =                         {"zee" : [2, 0, 300] }
    var["bj0_eta"] =                        {"zee" : [0.1, -3, 3] }
    var["bj0_phi"] =                        {"zee" : [0.1, -3.2, 3.2] }
    var["bj1_pt"] =                         {"zee" : [2, 0, 300] }
    var["bj1_eta"] =                        {"zee" : [0.1, -3, 3] }
    var["bj1_phi"] =                        {"zee" : [0.1, -3.2, 3.2] }

    var["j0_jvt"] =                         {"zee" : [0.05, 0, 1] }
    var["j0_nTracks"] =                     {"zee" : [1, 0, 30] }
    var["j0_mv2c10"] =                      {"zee" : [0.05, -1, 1] }
    var["j0_emfrac"] =                      {"zee" : [0.05, 0, 1] }
    var["sj0_jvt"] =                        {"zee" : [0.05, 0, 1] }
    var["sj0_nTracks"] =                    {"zee" : [1, 0, 30] }
    var["sj0_mv2c10"] =                     {"zee" : [0.05, -1, 1] }
    var["sj0_emfrac"] =                     {"zee" : [0.05, 0, 1] }
    var["bj0_jvt"] =                        {"zee" : [0.05, 0, 1] }
    var["bj0_nTracks"] =                    {"zee" : [1, 0, 30] }
    var["bj0_mv2c10"] =                     {"zee" : [0.05, -1, 1] }
    var["bj0_emfrac"] =                     {"zee" : [0.05, 0, 1] }

    var["dphi_j0_ll"] =                     {"zee" : [0.1, -3.2, 3.2] }
    var["dphi_j0_l0"] =                     {"zee" : [0.1, -3.2, 3.2] }
    var["dphi_sj0_ll"] =                    {"zee" : [0.1, -3.2, 3.2] }
    var["dphi_sj0_l0"] =                    {"zee" : [0.1, -3.2, 3.2] }
    var["dphi_bj0_ll"] =                    {"zee" : [0.1, -3.2, 3.2] }
    var["dphi_bj0_l0"] =                    {"zee" : [0.1, -3.2, 3.2] }

    var["mt2"] =                            {"zee" : [2, 0, 200] }
    var["meff"] =                           {"zee" : [5, 0, 600] }
    var["cosThetaB"] =                      {"zee" : [0.05, -1, 1] }
    var["mbb"] =                            {"zee" : [5, 0, 400] }
    var["dRbb"] =                           {"zee" : [0.05, 0, 6] }
    var["HT2Ratio"] =                       {"zee" : [0.05, 0, 1] }
    var["mt2_bb"] =                         {"zee" : [2, 0, 200] }
    var["DPB"] =                            {"zee" : [0.05, 0, 1] }
    var["GAM"] =                            {"zee" : [0.05, 0, 1] }
    var["RPT"] =                            {"zee" : [0.05, 0, 1] }


    out = {}
    for v in var :
        out[v] = var[v][region_to_use]

    return out

def get_regions() :

    regions = []

    r = region.Region("zee0j", "$ee$ selection (0J)")
    r.tcut = "nJets==0 && nLeptons==2 && nElectrons==2 && l0_pt>25 && l1_pt>20 && mll>20"
    regions.append(r)

    r = region.Region("zee", "$ee$ selection")
    r.tcut = "nLeptons==2 && nElectrons==2 && l0_pt>25 && l1_pt>20 && mll>20"
    regions.append(r)
    
    r = region.Region("zmm0j", "$\\mu \\mu$ selection (0J)")
    r.tcut = "nJets==0 && nLeptons==2 && nMuons==2 && l0_pt>25 && l1_pt>20 && mll>20"
    regions.append(r)

    r = region.Region("zmm", "$\\mu \\mu$ selection")
    r.tcut = "nLeptons==2 && nMuons==2 && l0_pt>25 && l1_pt>20 && mll>20"
    regions.append(r)

    r = region.Region("top_like", "$>=1b-$jet, $e \\mu+\\mu e$")
    r.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && l0_pt>25 && l1_pt>20 && nBJets>=1"
    regions.append(r)

    r = region.Region("dfval", "$e \\mu+\\mu e$-selection")
    r.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && l0_pt>25 && l1_pt>20"
    regions.append(r)

    r = region.Region("df_bveto", "$e\\mu + \\mu e$, b-veto")
    r.tcut = "nLeptons==2 && nLeptons==2 && nElectrons==1 && nMuons==1 && l0_pt>25 && l1_pt>25 && mll>20 && nBJets==0"
    regions.append(r)

    r = region.Region("zee_balance", "$Z\\rightarrow ee$ Balance (==1J)")
    r.tcut = "nLeptons==2 && nBJets==0 && nJets==1 && j0_pt>25 && nElectrons==2 && mll>80 && mll<100 && (dphi_j0_ll>3.0 || dphi_j0_ll<-3.0)"
    regions.append(r)

    r = region.Region("zmm_balance", "$Z\\rightarrow \\mu\\mu$ Balance (==1J)")
    r.tcut = "nLeptons==2 && nBJets==0 && nJets==1 && j0_pt>25 && nMuons==2 && mll>80 && mll<100 && (dphi_j0_ll>3.0 || dphi_j0_ll<-3.0)"
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
def make_comp_plot(r20sample, r21sample, variable_dict, region, opts) :

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
                #if varname == "l0_d0sig" :
                #    charge_data = c["l0_q"]
                #    data = data * charge_data
                #elif varname == "l1_d0sig" :
                #    charge_data = c["l1_q"]
                #    data = data * charge_data
                histo_dict[varname][isample].fill(data)

        labels.append(s.name)
        colors.append(s.color)

    print_yields = True

    n_vars_to_plot = len(variable_dict)
    var_idx = 1

    for varname, varbounds in variable_dict.iteritems() :

        histos = []
        for isample, sample in enumerate(samples) :
            histos.append(histo_dict[varname][isample])

        #for h in histos :
        #    h.add_overflow()

        yield_r20, yield_error_r20 = histos[0].integral_and_error()
        yield_r21, yield_error_r21 = histos[1].integral_and_error()
        yield_ratio = 0
        if yield_r20 != 0 :
            yield_ratio = yield_r21 / yield_r20

        rc = ratio_canvas("ratio_canvas_%s" % varname)
        if opts.do_logy :
            rc.logy = True
        #log_vars = ["jvt"]
        #for lv in log_vars :
        #    if lv in varname :
        #        opts.do_logy = True
        #        rc.logy = True
        
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

        if print_yields and yield_r20 !=0 :
            print_yields = False
            print "R20 : %.2f +/- %.2f" % (yield_r20, yield_error_r20)
            print "R21 : %.2f +/- %.2f" % (yield_r21, yield_error_r21)
            print "R21/R20 : %.2f" % (yield_r21 / yield_r20)

        maxy = -1
        miny = 0
        multiplier = 1.55
        for h in histos :
            if h.maximum() > maxy :
                maxy = h.maximum()
        if opts.do_logy :
            miny = 1e-2
            multiplier = 1e3

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

        rc.upper_pad.text(0.05, 0.84, '%s' % region.displayname, size = 0.63 * size, **legopts)
        rc.upper_pad.text(0.05, 0.79, 'R20 : %.2f' % yield_r20, size = 0.6 * size, **legopts)
        rc.upper_pad.text(0.05, 0.75, 'R21 : %.2f' % yield_r21, size = 0.6 * size, **legopts)
        rc.upper_pad.text(0.05, 0.71, '$\\rightarrow$ R21/R20 : %.2f' % (yield_ratio), size = 0.6 * size, **legopts)

        #rc.upper_pad.text(0.6, 0.71, "Lepton $d_0^{sig} \\times Q$", size = size, **legopts)

        if "mll" in varname or "d0" in varname :
            r21_mean = histos[1].mean()
            r21_std = histos[1].std()

            r20_mean = histos[0].mean()
            r20_std = histos[0].std()

            r20_mean_str = "%.4f \\pm %.4f" % (r20_mean, r20_std)
            r21_mean_str = "%.4f \\pm %.4f" % (r21_mean, r21_std)

            rc.upper_pad.text(0.5, 0.79, 'R20 : (mean, sigma) = (%.4f, %.4f)' % (r20_mean, r20_std), size = 0.4 * size, **legopts)
            rc.upper_pad.text(0.5, 0.75, 'R21 : (mean, sigma) = (%.4f, %.4f)' % (r21_mean, r21_std), size = 0.4 * size, **legopts)

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
            rel_e20_low[r20_values==0] = 0
            rel_e20_low[ ~ np.isfinite(rel_e20_low) ] = 0

            rel_e21_low = np.true_divide( e21_low, r21_values )
            rel_e21_low[r21_values==0] = 0
            rel_e21_low[ ~ np.isfinite(rel_e21_low) ] = 0

            rel_e20_high = np.true_divide( e20_high, r20_values )
            rel_e20_high[r20_values==0] = 0
            rel_e20_high[ ~ np.isfinite(rel_e20_high) ] = 0

            rel_e21_high = np.true_divide( e21_high, r21_values )
            rel_e21_high[r21_values==0] = 0
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
        print " >>> [%02d/%02d] Saving plot to : %s" % (var_idx, n_vars_to_plot, os.path.abspath(save_name))
        rc.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)

        var_idx += 1
                                


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
    extra_vars = ["isMC", "l0_q", "l1_q"] #, "run", "lumi_block", "year"]
    required_vars = []
    required_vars += variables_from_region
    required_vars += extra_vars

    cacher = sample_cacher.SampleCacher("./selection_datadata") 
    cacher.samples = [samples_r20, samples_r21]
    cacher.region = region_to_use
    cacher.fields = required_vars
    print str(cacher)
    cacher.cache()

    n_plots = len(variables)
    make_comp_plot(samples_r20, samples_r21, variables, region_to_use, opts)
#    for iplot, v in enumerate(variables) :
#        print 55 * "-"
#        print "[%02d/%02d] %s" % (iplot+1, n_plots, v)
#        make_comp_plot(samples_r20, samples_r21, variables, opts)
#        #make_comp_plot(samples_r20, samples_r21, v, variables[v], opts)


if __name__ == "__main__" :
    main()

#!/bin/env python

import ROOT as r
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
r.PyConfig.IgnoreCommandLineOptions = True

import sys, os
import glob
from math import sqrt

mc16a_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/h_apr7_rustem/mc/mc16a/"
mc16d_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/h_apr7_rustem/mc/mc16d/"
mc16e_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/h_apr7_rustem/mc/mc16e/"

ttbar_files = ["%s/CENTRAL_410472_mc16a.root" % mc16a_dir, "%s/CENTRAL_410472_mc16d.root" % mc16d_dir, "%s/CENTRAL_410472_mc16e.root" % mc16e_dir]
wt_files = ["%s/wt_mc16a.root" % mc16a_dir, "%s/wt_mc16d.root" % mc16d_dir, "%s/wt_mc16e.root" % mc16e_dir]
z_files = ["%s/zjets_mc16a.root" % mc16a_dir, "%s/zjets_mc16d.root" % mc16d_dir, "%s/zjets_mc16e.root" % mc16e_dir]
sig_files = ["/data/uclhc/uci/user/dantrim/n0307val/hh_wwbb_rustem.root"]

class Sample :
    def __init__(self, name, files) :
        self.name = name
        self.files = files
        self.tree = None
        self.load()
    def load(self) :
        c = r.TChain("superNt")
        for f in self.files :
            c.Add(f)
        self.tree = c
        print "Sample %s loaded %d entries" % (self.name, self.tree.GetEntries())

def selection_dict() :

    s = {}
    s["sr_sf"] = "nBJets>=2 && mll>20 && mll<60 && mbb>110 && mbb<140 && isSF==1"
    s["sr_df"] = "nBJets>=2 && mll>20 && mll<60 && mbb>110 && mbb<140 && isDF==1"
    s["top_cr"] = "nBJets>=2 && (mbb<110 || mbb>140) && mll>20 && mll<60 && isDF==1"
    s["z_cr"] = "nBJets>=2 && mbb>110 && mbb<140 && mll>81.2 && mll<101.2"
    return s

def get_yields(samples, region_name) :


    total_yield_array = []
    trigger = "((year==2015 && trig_tight_2015==1) || (year==2016 && trig_tight_2016==1) || (year==2017 && trig_tight_2017rand==1) || (year==2018 && trig_tight_2018==1))"

    cut = selection_dict()[region_name]
    dhh_cut = { "sr_sf" : "5.45", "sr_df" : "5.55", "top_cr" : "4.5", "z_cr" : "0" }
    for i in range(5) :
        if i == 0 : continue
        var_r = "NN_d_hh_r%d" % i
        #var_r = "NN_d_hh"
        selection_r = "%s && %s && %s>%s" % (trigger, cut, var_r, dhh_cut[region_name])
        weight_str = "eventweightNoPRW_multi * 140.5"
        tcut = "(%s) * %s" % (selection_r, weight_str)

        yield_i = 0.0
        err_i = 0.0

        for isample, sample in enumerate(samples) :
            h = r.TH1F("h_%d_%d" % (isample, i), "", 4, 0, 4)
            h.Sumw2()
            cmd = "isMC>>%s" % h.GetName()
            sample.tree.Draw(cmd, tcut, "goff")
            err = r.Double(0.0)
            integral = h.IntegralAndError(0,-1, err)
            yield_i += integral
            err_i += err * err
        err_i = sqrt(err_i)
        print "Split %d: %.5f +/- %.5f" % (i, yield_i, err_i)
        total_yield_array.append( [yield_i, err_i] )

    h_spread = r.TH1F("h_spread_%s" % region_name, "", 100, 0, -1)
    h_spread.Sumw2()
    for iy, y in enumerate(total_yield_array) :
        integral = y[0]
        h_spread.Fill(integral)
    print 35 * "- "
    print "Spread %s : %.4f +/- %.4f" % (region_name, h_spread.GetMean(), h_spread.GetStdDev())


def main() :

  #  sample_ttbar = Sample("ttbar", ttbar_files)
  #  sample_z = Sample("zjets", z_files)
  #  sample_wt = Sample("wt", wt_files)
  #  samples = [sample_ttbar, sample_wt, sample_z]
  #  #samples = [sample_wt]

    sample_sig = Sample("hh", sig_files)
    samples = [ sample_sig ]

    region_dict = selection_dict()
    n_reg = len(region_dict)
    for ireg, reg in enumerate(region_dict.keys()) :
        print 70 * "="
        print "[%02d/%02d] %s" % (ireg+1, n_reg,  reg)
        get_yields(samples, reg)

if __name__ == "__main__" :
    main()

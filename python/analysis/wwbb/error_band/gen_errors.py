#!/bin/env python

from __future__ import print_function

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)

import argparse
import os, sys
import glob
import json
from math import sqrt, ceil

import numpy as np

ntuple_dir = "/data/uclhc/uci/user/dantrim/WWbbXAnalysis/sys_ntuples/"
ttbar_a_dir = "%s/group.phys-susy.mc16_13TeV.410472.PhPy8EG_A14_ttbar_hdamp258p75_dil.WWbb2l2x.mc16a.p3703_v00_nt/" % ntuple_dir
ttbar_d_dir = "%s/group.phys-susy.mc16_13TeV.410472.PhPy8EG_A14_ttbar_hdamp258p75_dil.WWbb2l2x.mc16d.p3703_v00_nt/" % ntuple_dir
ttbar_e_dir = "%s/group.phys-susy.mc16_13TeV.410472.PhPy8EG_A14_ttbar_hdamp258p75_dil.WWbb2l2x.mc16e.p3703_v00_nt/" % ntuple_dir
ttbar_file_dirs = [ttbar_a_dir, ttbar_d_dir, ttbar_e_dir]

z_ntuple_dir = "/data/uclhc/uci/user/dantrim/WWbbXAnalysis/sys_ntuples/"
z_data_dir = "/data/uclhc/uci/user/dantrim/WWbbXAnalysis/source/wwbb2l2x/data/"
z_xsec_file = "%s/xsec_wwbb2l2x.txt" % z_data_dir
z_sumw_file = "%s/sumw_wwbb2l2x_mc16ade.txt" % z_data_dir

def variables_dict() :

    vdict = {}
    vdict["NN_d_hh"] = { "top_cr" : [1.0, -10, 10], "top_vr" : [1.0, 4.5, 11.5], "z_cr" : [1.0, -10, 10], "z_vr" : [1.0, 0, 6], "sr" : [1.0, -12, 12] }
    #vdict["NN_d_hh"] = { "top_cr" : [1.0, -10, 10], "top_vr" : [1.0, -10, 12], "z_cr" : [1.0, -10, 10], "z_vr" : [1.0, -10, 8], "sr" : [1.0, -12, 12] }
    #vdict["NN_d_hh"] = { "top_cr" : [0.5, -7, 1], "top_vr" : [0.5, -7, 1], "z_cr" : [0.5, -7, 1], "z_vr" : [0.5, -7, 1], "sr" : [0.5, -7, 1] }
    #vdict["NN_d_hh"] = { "top_cr" : [0.5, -7, 1], "top_vr" : [0.5, -7, 1], "z_cr" : [0.5, -7, 1], "z_vr" : [0.5, -7, 1], "sr" : [1, 0, 12] }
    #vdict["NN_d_hh"] = { "top_cr" : [0.5, -7, 1], "top_vr" : [0.5, -7, 1], "z_cr" : [0.5, -7, 1], "z_vr" : [0.5, -7, 1], "sr" : [0.5, 4, 9],
    #                    "crTop" : [1.0, 4.5, 11.5], "crZ" : [1.0, 0, 8], "srIncNoDhh" : [1.0, -11, 11], "srSFNoDhhCloseCut" : [1.0, 5.5, 11.5], "srDFNoDhhCloseCut" : [1.0, 5.5, 9.5] }
    vdict["NN_d_top"] = { "top_cr" : [1.0, -12, 12], "top_vr" : [1.0, -10, 12], "z_cr" : [1.0, -10, 10], "z_vr" : [1.0, -10, 8], "sr" : [2.0, -20, 12] }
    vdict["NN_d_ztt"] = { "top_cr" : [1.0, -18, 5], "top_vr" : [1.0, -10, 12], "z_cr" : [1.0, -10, 10], "z_vr" : [1.0, -10, 8], "sr" : [2.0, -20, 4] }
    vdict["NN_d_zsf"] = { "top_cr" : [1.0, -10, 10], "top_vr" : [1.0, -10, 12], "z_cr" : [1.0, -10, 10], "z_vr" : [1.0, -10, 8], "sr" : [4.0, -60, 4] }

    vdict["dRll"] = { "srIncNoDhh" : [ 0.2, 0.0, 3.6] }
    vdict["HT2Ratio"] = { "srIncNoDhh" : [0.1, 0.0, 1.0], "srIncNoMbbDhh" : [ 0.1, 0.6, 1.0] }


    # aux plots
    vdict["NN_d_hh"] = {
        "top_cr" : [1.0, 4.5, 11.5]
        ,"z_cr"  : [1.0, 0, 8]
        ,"top_vr": [1.0, 4.5, 11.5]
        ,"z_vr"  : [1.0, 0, 6]
        ,"srIncNoDhh" : [1.0, -11, 11]
        ,"srSFNoDhh" : [1.0, -11.0, 12.0]
        ,"srDFNoDhh" : [1.0, -12.0, 10.0]
        ,"srSFNoDhhCloseCut" : [1.0, 5.45, 11.45]
        ,"srDFNoDhhCloseCut" : [1.0, 5.55, 9.55]
    }
    vdict["dphi_ll"] = {
        "top_cr" : [0.2, 0, 1.8]
        ,"z_cr"  : [0.2, 0.0, 1.8]
        ,"top_vr": [0.2, 0.0, 1.8]
        ,"z_vr"  : [0.2, 0.0, 1.8]
        ,"srIncNoDhh" : [0.2, 0, 3.2]
        ,
    }
    vdict["dRll"] = {
        "top_cr" : [0.2, 0.2, 2.2]
        ,"z_cr"  : [0.4, 0, 2.8]
        ,"top_vr": [0.2, 0, 2.4]
        ,"z_vr"  : [0.4, 0.0, 3.2]
        ,"srIncNoDhh" : [0.2, 0.0, 3.6]
        ,
    }
    vdict["HT2Ratio"] = {
        "top_cr" : [0.1, 0.2, 1.0]
        ,"z_cr"  : [0.1, 0.5, 1.0]
        ,"top_vr": [0.1, 0.2, 1.0]
        ,"z_vr"  : [0.1, 0.5, 1.0]
        ,"srIncNoDhh" : [0.1, 0, 1.0]
        ,"srIncNoMbbDhh" : [0.1, 0.6, 1.0]
        ,
    }
    vdict["mt2_bb"] = {
        "top_cr" : [40, 0, 360]
        ,"z_cr"  : [20, 0, 160]
        ,"top_vr": [40, 0, 360]
        ,"z_vr"  : [20, 0, 200]
        ,"srIncNoDhh" : [30, 0, 300]
        ,
    }
    vdict["mbb"] = {
        "srIncNoMbbDhh" : [20, 20, 300]
    }
    vdict["mll"] = {
        "srIncNoMllDhh" : [5, 20, 80]
    }

    return vdict

def regions_dict() :

    rdict = {}
    #rdict["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && isDF==1"
    #rdict["sr"] = "nBJets>=2 && mll>20 && mll<60 && mbb>110 && mbb<140 && isDF==1"

    # paper plots
    #rdict["srSFNoDhhCloseCut"] = "isSF==1 && mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140 && NN_d_hh>5.45"
    #rdict["srDFNoDhhCloseCut"] = "isDF==1 && mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140 && NN_d_hh>5.55"
    #rdict["crTop"]  = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>4.5 && isDF==1"
    #rdict["crZ"]    = "nBJets>=2 && mll>81.2 && mll<101.2 && mbb>100 && mbb<140 && NN_d_hh>0"
    rdict["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>4.5 && isDF==1"
    rdict["top_vr"] = "nBJets>=2 && mll>20 && mll<60 && mbb>140 && NN_d_hh>4.5 && isSF==1"
    rdict["z_cr"]   = "nBJets>=2 && mll>81.2 && mll<101.2 && mbb>100 && mbb<140 && NN_d_hh>0"
    rdict["z_vr"]   = "nBJets>=2 && ((mll>71.2 && mll<81.2) || (mll>101.2 && mll<115)) && mbb>100 && mbb<140 && NN_d_hh>0"
    rdict["srIncNoDhh"] = "mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140"
    rdict["srSFNoDhh"] = "mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140 && isSF==1"
    rdict["srDFNoDhh"] = "mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140 && isDF==1"
    rdict["srSFNoDhhCloseCut"] = "isSF==1 && mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140 && NN_d_hh>5.45"
    rdict["srDFNoDhhCloseCut"] = "isDF==1 && mll>20 && mll<60 && nBJets>=2 && mbb>110 && mbb<140 && NN_d_hh>5.55"
    rdict["srIncNoMbbDhh"] = "mll>20 && mll<60 && nBJets>=2 && NN_d_hh>5"
    rdict["srIncNoMllDhh"] = "mbb>110 && mbb<140 && nBJets>=2 && NN_d_hh>5"
    return rdict

def uncert_types_dict() :

    udict = {}
    udict["ttbar"] = { "hs_gen" : "superNt", "frag_had" : "superNt", "radiation" : "wwbb2l2x" }
    udict["wt"] = { "ds" : "superNt", "frag_had" : "superNt" }
    udict["z"] = { "mg5" : "truth" }
    return udict

class SuperNtSample :
    def __init__(self, name = "", treename = "", variation = "", input_files = []) :
        self.name = name
        self.variation = variation
        self.files = input_files
        self.tree = None
        self.treename = treename
        self.load()

    def load(self) :
        c = r.TChain(self.treename)
        for f in self.files :
            c.Add(f)
        self.tree = c
        print("SuperNtSample {} (variation = {}) loaded chain with {} entries".format(self.name, self.variation, c.GetEntries()))

class WWbb2l2xSample :
    def __init__(self, name = "", treename = "", variation = "", input_filedirs = []) :

        if name != "ttbar" :
            print("ERROR We do not handle WWbb2l2xSample objects that are not ttbar!")
            sys.exit()
        self.name = name
        self.treename = treename
        self.variation = variation
        self.input_filedirs = input_filedirs
        self.tree = None
        self.load()

    def load(self) :
        c = r.TChain(self.treename)
        for fdir in self.input_filedirs :
            rfiles = glob.glob("%s/*.root" % fdir)
            for rf in rfiles :
                c.Add(rf)
        self.tree = c
        print("Loaded WWbb2l2xSample {} (variation = {}) with {} entries".format(self.name, self.variation, c.GetEntries()))
        

class ZHFSample :
    def __init__(self, name = "", filelist = "", color = "") :

        self.name = name
        self.color = color
        self.filelist = filelist
        self.files = self.load_files()
        print("%s loaded sample with %d files" % (self.name, len(self.files)))
        self.dsid_map = {}
        self.xsec_map = {}

    def get_sumw(self) :
        total_sumw = 0.0
        for f in self.filelist :
            rfile = r.TFile.Open(f)
            h = rfile.Get("h_sumw")
            total_sumw += h.GetBinContent(1)
        return total_sumw

    def load_files(self) :
        list_out = []
        with open(self.filelist) as infile :
            for line in infile :
                line = line.strip()
                if line.startswith("#") : continue
                list_out.append(line)
        return list_out


    def load_xsec(self, xsec_filename = "") :
        self.dsid_map = {}
        self.xsec_map = {}
        with open(xsec_filename, "r") as infile :
            for iline, line in enumerate(infile) :
                line = line.strip()
                fields = line.split()
                dsid = fields[0]
                xsec = float(fields[1])
                self.dsid_map[iline] = dsid
                self.xsec_map[dsid] = xsec


def get_superNt_bin_values(sample, h_var_bounds, args) :

    variable = h_var_bounds[0]
    n_bins = h_var_bounds[1]
    x_lo = h_var_bounds[2]
    x_hi = h_var_bounds[3]

    h = r.TH1F("h_{}_{}".format(sample.name, sample.variation), "", n_bins, x_lo, x_hi)
    h.Sumw2()

    hc = r.TH1F("hc_{}_{}".format(sample.name, sample.variation), "", n_bins, x_lo, x_hi)
    hc.Sumw2()

    if args.absval :
        variable = "abs(%s)" % variable

    cmd = "{}>>{}".format(variable, h.GetName())
    selection_str = regions_dict()[args.region]
    weight_str = "eventweightNoPRW_multi * 140.5"

    #if sample.name == "ttbar" and sample.variation == "nominal" :
    #    ttbar_sumw = 1.63520096697e+11
    #    ttbar_xsec = 87.7174095997
    #    weight_str = "nom_weight * %.2f * 1000. * 140.5 / %.2f" % (ttbar_xsec, ttbar_sumw)

    full_cut_str = "({}) * {}".format(selection_str, weight_str)

    sample.tree.Draw(cmd, full_cut_str, "goff")

    cmd = "{}>>{}".format(variable, hc.GetName())
    sample.tree.Draw(cmd, full_cut_str, "goff")

    h.Scale(1.0 / h.Integral())
    bin_vals = []
    bin_vals_norm = []
    for ibin in range(h.GetNbinsX()) :
        bin_no = ibin + 1
        bin_vals.append(hc.GetBinContent(bin_no))
        #print("SuperNt %s BIN vals: %d --> %.5f" % (sample.variation, bin_no, hc.GetBinContent(bin_no)))
        bin_vals_norm.append(h.GetBinContent(bin_no))
        
    return bin_vals_norm, bin_vals

def get_superNt_variation(process, variation_name, h_var_bounds, args) :

    json_file = "./inputs/{}_inputs".format(process) #.json".format(process)
    if process == "ttbar" and h_var_bounds[0] != "dphi_ll" : # and args.region == "z_cr" :
        json_file += "_good"
        #json_file += "_forz"
    json_file += ".json"
    
    with open(json_file, "r") as input_file :
        data = json.load(input_file)

    samples = {}
    for sample in data["samples"] :
        variation = sample["variation"]
        if not (variation == "nominal" or variation == variation_name) : continue
        treename = sample["treename"]
        filelist = sample["files"]
        s = SuperNtSample(name = process, treename = treename, variation = variation, input_files = filelist)
        samples[variation] = s

    nominal_sample = samples["nominal"]
   # if process == "ttbar" :
   #     nominal_sample = WWbb2l2xSample(name = process, treename = "wwbb", variation = "nominal", input_filedirs = ttbar_file_dirs)

    variation_sample = samples[variation_name]

    nominal_bin_values_norm, nominal_bin_values = get_superNt_bin_values(nominal_sample, h_var_bounds, args)
    variation_bin_values_norm, variation_bin_values = get_superNt_bin_values(variation_sample, h_var_bounds, args)

    deltas = []
    for ibin in range(len(nominal_bin_values_norm)) :
        nom_val = nominal_bin_values_norm[ibin]
        var_val = variation_bin_values_norm[ibin]

        delta = 0.0
        if nom_val != 0 :
            if var_val > nom_val :
                delta = var_val - nom_val
            elif var_val < nom_val :
                delta = nom_val - var_val
            delta /= nom_val
        deltas.append(delta)

    #nominal_bin_values = np.array(nominal_bin_values)
    #variation_bin_values = np.array(variation_bin_values)

    #print("nominal bin values   : {}".format(nominal_bin_values))
    #print("variation bin values : {}".format(variation_bin_values))

    #delta = np.abs(nominal_bin_values - variation_bin_values)
    #relative_delta = np.divide(delta, nominal_bin_values)

    relative_delta = np.array(deltas)

    return relative_delta, nominal_bin_values

def get_zhf_bin_values(sample, h_var_bounds, args) :

    variable = h_var_bounds[0]
    n_bins = h_var_bounds[1]
    x_lo = h_var_bounds[2]
    x_hi = h_var_bounds[3]

    if args.absval :
        variable = "abs(%s)" % variable

    filelist = sample.files
    n_files = len(filelist)

    selection_str = regions_dict()[args.region]

#    w_n = 200
#    w_xlo = -100
#    w_xhi = 100
    w_n = 5
    w_xlo = 0.5
    w_xhi = 1
#    hw = r.TH1F("h_w_%s" % sample.name, "", w_n, w_xlo, w_xhi)
    hw = r.TH1F("h_ht2r_%s" % sample.name, "", w_n, w_xlo, w_xhi)
    hw.Sumw2()
    ov_min = 0
    ov_max = 0

    h_full = r.TH1F("h_full_%s" % (sample.name), "", n_bins, x_lo, x_hi)
    h_full.Sumw2()
    hc_full = r.TH1F("hc_full_%s" % (sample.name), "", n_bins, x_lo, x_hi)
    hc_full.Sumw2()

    bin_values = np.zeros(n_bins)
    bin_values_norm = np.zeros(n_bins)
    for ifile, filename in enumerate(filelist) :
        if ifile % 6 == 0 :
            print(" > [%02d/%02d]" % (ifile+1, len(filelist)))
        rfile = r.TFile.Open(filename)
        h = r.TH1F("h_%s_%d" % (sample.name, ifile), "", n_bins, x_lo, x_hi)
        h.Sumw2()

        hc = r.TH1F("hc_%s_%d" % (sample.name, ifile), "", n_bins, x_lo, x_hi)
        hc.Sumw2()

        h_sumw = rfile.Get("h_sumw")
        sumw = h_sumw.GetBinContent(1)
        current_dsid = sample.dsid_map[ifile]
        xsec = sample.xsec_map[current_dsid]

        weight_str = "w * %.2f * 1000. * 140.5 / %.2f" % (float(xsec), float(sumw))
        #print("******** FORCING EVENT WEIGHTS |w|<10 *********")
        full_cut_str = "(%s) * %s" % (selection_str, weight_str)

        tree = rfile.Get("truth")
        cmd = "{}>>{}".format(variable, h.GetName())
        tree.Draw(cmd, full_cut_str, "goff")

        cmd = "{}>>{}".format(variable, hc.GetName())
        tree.Draw(cmd, full_cut_str, "goff")

        hw_i = r.TH1F("h_w_%s_%d" % (sample.name, ifile), "", w_n, w_xlo, w_xhi)
        hw_i.Sumw2()
        #cmd_w = "w>>%s" % hw_i.GetName()
        cmd_w = "HT2Ratio>>%s" % hw_i.GetName()
        #w_sel = "(%s && HT2Ratio>0.7 && HT2Ratio<0.8)" % selection_str
        w_sel = full_cut_str
        tree.Draw(cmd_w, w_sel, "goff")

        bin_no_max = hw_i.GetMaximumBin()
        bin_no_min = hw_i.GetMinimumBin()
        if bin_no_max > ov_max : ov_max = bin_no_max
        if bin_no_min < ov_min : ov_min = bin_no_min

        #print("%d BIN MIN %.5f  BIN MAX %.5f" % (ifile, bin_no_min, bin_no_max))

        ### TEST FULL HISTO BEFORE NORM [BEGIN]
        h_full.Add(h)
        hc_full.Add(hc)
        continue
        ### TEST FULL HISTO [END]

        hw.Add(hw_i)
        #print("HW integral: %d" % hw.GetEntries())

        if h.Integral() == 0 : continue

        h.Scale(1.0 / h.Integral())
        bin_vals = []
        bin_vals_norm = []
        for ibin in range(h.GetNbinsX()) :
            bin_no = ibin + 1
            bin_vals.append(hc.GetBinContent(bin_no))
            #print("ZHF %s BIN vals: %d -> %.5f" % (sample.name, bin_no, hc.GetBinContent(bin_no)))
            bin_vals_norm.append(h.GetBinContent(bin_no))

        bin_vals = np.array(bin_vals)
        bin_vals_norm = np.array(bin_vals_norm)
        bin_values += bin_vals
        bin_values_norm += bin_vals_norm

    #print("OVERALL MIN MAX = %.5f %.5f" % (ov_min, ov_max))

    if h_full.Integral() == 0 :
        return bin_values_norm, bin_values

    h_full.Scale(1.0 / h_full.Integral())
    bin_vals = []
    bin_vals_norm = []
    for ibin in range(h_full.GetNbinsX()) :
        bin_no = ibin + 1
        bin_vals.append(hc_full.GetBinContent(bin_no))
        bin_vals_norm.append(h_full.GetBinContent(bin_no))
    bin_values += np.array(bin_vals)
    bin_values_norm += np.array(bin_vals_norm)

    print("Saving ZHF %s weight histogram to %s" % (sample.name, hw.GetName()))
    hw.SaveAs("%s.root" % hw.GetName())

    return bin_values_norm, bin_values

def get_z_mg5_variation(uncert, variation, h_var_bounds, args) :

    sample_nom = ZHFSample("nominal", "data/list_sherpa.txt", 0)
    sample_nom.load_xsec("data/xsec_file_sherpa.txt")
    sample_alt = ZHFSample("mg5", "data/list_mg5.txt", 0)
    sample_alt.load_xsec("data/xsec_file_mg5.txt")
    samples = [sample_nom, sample_alt]

    nominal_bin_values_norm, nominal_bin_values = get_zhf_bin_values(sample_nom, h_var_bounds, args)
    variation_bin_values_norm, variation_bin_values = get_zhf_bin_values(sample_alt, h_var_bounds, args)

    print("nom bin vals  : {}".format(nominal_bin_values))
    print("var bin vals  : {}".format(variation_bin_values))

    deltas = []
    for ibin in range(len(nominal_bin_values_norm)) :
        nom_val = nominal_bin_values_norm[ibin]
        var_val = variation_bin_values_norm[ibin]
        delta = 0.0
        if nom_val != 0 :
            if var_val > nom_val :
                delta = var_val - nom_val
            elif var_val < nom_val :
                delta = nom_val - var_val
            delta /= nom_val
            #print("BIN %d  VAR VAL = %.2f  NOM VAL = %.2f : RELDELTA = %.2f" % (ibin, var_val, nom_val, delta))
        deltas.append(delta)

    relative_delta = np.array(deltas)
    return relative_delta, nominal_bin_values

def get_uncerts(uncert, h_var_bounds, args) :

    variable = h_var_bounds[0]
    n_bins = int(h_var_bounds[1])
    x_lo = h_var_bounds[2]
    x_hi = h_var_bounds[3]

    bin_errors = np.zeros(n_bins)
    bin_content = np.zeros(n_bins)

    udict = uncert_types_dict()[uncert]
    for variation, variation_type in udict.iteritems() :
        print(" -> {} : {}".format(variation, variation_type))
        if variation_type == "superNt" :
            #print("SKIPPING TTBAR UNCERTS")
            #continue
            var_bin_deltas, nom_bin_values = get_superNt_variation(uncert, variation, h_var_bounds, args)
            #bin_errors += var_bin_deltas
            bin_content += np.array(nom_bin_values)
            bin_errors += np.power(var_bin_deltas, 2)
        elif uncert == "z" and variation == "mg5" :
            var_bin_deltas, nom_bin_values = get_z_mg5_variation(uncert, variation, h_var_bounds, args)
            #bin_errors += var_bin_deltas
            bin_content += np.array(nom_bin_values)
            bin_errors += np.power(var_bin_deltas, 2)

    # symmetrize
    #bin_errors = 0.5 * np.sqrt(bin_errors)
    #print("bin errors: {}".format(bin_errors))

    return bin_errors, bin_content

def get_error_band(variable_name, args) :

    var_bounds = variables_dict()[variable_name][args.region]
    n_bins = var_bounds[2] - var_bounds[1]
    #print("n_bins = {}".format(n_bins))
    n_bins /= var_bounds[0]
    #print("n_bins /= {} = {}".format(var_bounds[0], n_bins))
    n_bins = int(round(n_bins, 2))
    #n_bins = int(ceil(n_bins))
    #print("ceiled = {}".format(n_bins))
    x_lo = var_bounds[1]
    x_hi = var_bounds[2]
    #print("FUCK face var_bounds[0] = %.2f var_bounds[1] = %.2f var_bounds[2] = %.2f  (n_bins = %.2f  x_lo = %.2f  x_hi = %.2f)" % (var_bounds[0], var_bounds[1], var_bounds[2], n_bins, x_lo, x_hi))
    #sys.exit()
    h_var_bounds = [variable_name, n_bins, x_lo, x_hi]

    bin_error = np.zeros(n_bins)
    bin_sq_deltas_by_proc = {}
    total_bin_contents = np.zeros(n_bins)
    bin_contents_by_proc = {}
    for iuncert, uncert in enumerate(args.uncerts) :
        bin_sq_deltas, nom_bin_contents  = get_uncerts(uncert, h_var_bounds, args)

        bin_contents_by_proc[uncert] = nom_bin_contents
        bin_sq_deltas_by_proc[uncert] = bin_sq_deltas

    # get totals
    for proc_name, proc_totals in bin_contents_by_proc.iteritems() :
        total_bin_contents += proc_totals

    # get fractions
    process_frac_dict = {}
    for proc_name, bc in bin_contents_by_proc.iteritems() :
        process_frac_dict[proc_name] = np.divide(bc, total_bin_contents)

    # write it out, too
    #json_name = "process_uncerts_{}_{}_paper_may7.json".format(variable_name, args.region)
    #json_name = "process_uncerts_{}_{}_paper_test.json".format(variable_name, args.region)
    json_name = "process_uncerts_{}_{}_paper_may29.json".format(variable_name, args.region)
    json_data = {}
    json_data["variable"] = variable_name
    json_data["region"] = args.region
    json_data["binning"] = { "n_bins" : n_bins, "x_lo" : x_lo, "x_hi" : x_hi, "bin_width" : var_bounds[0] }
    json_data["processes"] = []

    # get process fraction weighted errors
    bin_error_by_proc = {}
    for proc_name, bin_sq_delta in bin_sq_deltas_by_proc.iteritems() :
    
        #bin_errors = np.power(bin_deltas, 2)
        #print("process uncerts {} : {}".format(proc_name, bin_sq_delta))
        #print("process fraction {} : {}".format(proc_name, process_frac_dict[proc_name]))
        json_data["processes"].append(
            { "name" : proc_name, "errors" : list(0.5 * np.sqrt(bin_sq_delta)) }
        )
        bin_errors = 0.5 * np.sqrt(bin_sq_deltas) * process_frac_dict[proc_name]
        bin_error_by_proc[uncert] = bin_errors# * process_frac_dict[proc_name]

    with open(json_name, "w") as outfile :
        json.dump(json_data, outfile)


    for bn, be in bin_error_by_proc.iteritems() :
        bin_error += np.power(be,2)
    bin_error = np.sqrt(bin_error)
    #bin_error = 0.5 * np.sqrt(bin_error)
    print("final bin error: {}".format(bin_error))

def main() :

    parser = argparse.ArgumentParser(description = "Generate errors for plots")
    parser.add_argument("-r", "--region", required = True,
        help = "Select the region to generate the errors for"
    )
    parser.add_argument("--uncerts", nargs = "+", default = ["ttbar", "wt", "z"],
        help = "Select which uncertainties to consider"
    )
    parser.add_argument("-v", "--var", nargs = "+", default = ["NN_d_hh"],
        help = "Select which variable to consider"
    )
    parser.add_argument("--absval", action = "store_true", default = False,
        help = "Make absolute value of the variable requested"
    )
    args = parser.parse_args()

    vdict = variables_dict()
    for v in args.var :
        if v not in vdict :
            print("ERROR requested variable {0} not found in variables dict".format(v))
            sys.exit()

    rdict = regions_dict()
    if args.region not in rdict :
        print("ERROR requested region {0} not found in regions dict".format(args.region))
        sys.exit()

    n_vars = len(args.var)
    for ivar, var in enumerate(args.var) :
        print("[{0:02d}/{1:02d}] {2}".format(ivar+1, n_vars, var))
        get_error_band(var, args)

    

#__________
if __name__ == "__main__" :
    main()

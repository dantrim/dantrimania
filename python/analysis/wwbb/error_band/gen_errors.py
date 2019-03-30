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
from math import sqrt

import numpy as np

ntuple_dir = "/data/uclhc/uci/user/dantrim/WWbbXAnalysis/sys_ntuples/"

z_ntuple_dir = "/data/uclhc/uci/user/dantrim/WWbbXAnalysis/sys_ntuples/"
z_data_dir = "/data/uclhc/uci/user/dantrim/WWbbXAnalysis/source/wwbb2l2x/data/"
z_xsec_file = "%s/xsec_wwbb2l2x.txt" % z_data_dir
z_sumw_file = "%s/sumw_wwbb2l2x_mc16ade.txt" % z_data_dir

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

def variables_dict() :

    vdict = {}
    vdict["NN_d_hh"] = [1.0, -10, 10]
    return vdict

def regions_dict() :

    rdict = {}
    rdict["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && isDF==1"
    rdict["z_cr"] = "nBJets>=2 && mll>70 && mll<115 && mbb>110 && mbb<140"
    return rdict

def uncert_types_dict() :

    udict = {}
    udict["ttbar"] = { "hs_gen" : "superNt", "frag_had" : "superNt", "radiation" : "wwbb2l2x" }
    udict["wt"] = { "ds" : "superNt", "frag_had" : "superNt" }
    udict["z"] = { "mg5" : "truth" }
    return udict

def get_superNt_bin_values(sample, h_var_bounds, args) :

    variable = h_var_bounds[0]
    n_bins = h_var_bounds[1]
    x_lo = h_var_bounds[2]
    x_hi = h_var_bounds[3]

    h = r.TH1F("h_{}_{}".format(sample.name, sample.variation), "", n_bins, x_lo, x_hi)
    h.Sumw2()

    cmd = "{}>>{}".format(variable, h.GetName())
    selection_str = regions_dict()[args.region]
    weight_str = "eventweightNoPRW_multi * 140.5"
    full_cut_str = "({}) * {}".format(selection_str, weight_str)

    sample.tree.Draw(cmd, full_cut_str, "goff")
    h.Scale(1.0 / h.Integral())
    bin_vals = []
    for ibin in range(h.GetNbinsX()) :
        bin_no = ibin + 1
        bin_vals.append(h.GetBinContent(bin_no))
    return bin_vals

def get_superNt_variation(process, variation_name, h_var_bounds, args) :

    json_file = "./inputs/{}_inputs.json".format(process)
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
    variation_sample = samples[variation_name]

    nominal_bin_values = get_superNt_bin_values(nominal_sample, h_var_bounds, args)
    variation_bin_values = get_superNt_bin_values(variation_sample, h_var_bounds, args)

    deltas = []
    for ibin in range(len(nominal_bin_values)) :
        nom_val = nominal_bin_values[ibin]
        var_val = variation_bin_values[ibin]

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

    return relative_delta

def get_zhf_bin_values(sample, h_var_bounds, args) :

    variable = h_var_bounds[0]
    n_bins = h_var_bounds[1]
    x_lo = h_var_bounds[2]
    x_hi = h_var_bounds[3]

    filelist = sample.files
    n_files = len(filelist)

    selection_str = regions_dict()[args.region]

    bin_values = np.zeros(n_bins)
    for ifile, filename in enumerate(filelist) :
        if ifile % 6 == 0 :
            print(" > [%02d/%02d]" % (ifile+1, len(filelist)))
        rfile = r.TFile.Open(filename)
        h = r.TH1F("h_%s_%d" % (sample.name, ifile), "", n_bins, x_lo, x_hi)
        h.Sumw2()

        h_sumw = rfile.Get("h_sumw")
        sumw = h_sumw.GetBinContent(1)
        current_dsid = sample.dsid_map[ifile]
        xsec = sample.xsec_map[current_dsid]

        weight_str = "w * %.2f * 1000. / %.2f" % (float(xsec), float(sumw))
        full_cut_str = "(%s) * %s" % (selection_str, weight_str)

        tree = rfile.Get("truth")
        cmd = "{}>>{}".format(variable, h.GetName())
        tree.Draw(cmd, full_cut_str, "goff")

        if h.Integral() == 0 : continue

        h.Scale(1.0 / h.Integral())
        bin_vals = []
        for ibin in range(h.GetNbinsX()) :
            bin_no = ibin + 1
            bin_vals.append(h.GetBinContent(bin_no))
        bin_vals = np.array(bin_vals)
        bin_values += bin_vals
    return bin_values

def get_z_mg5_variation(uncert, variation, h_var_bounds, args) :

    sample_nom = ZHFSample("nominal", "data/list_sherpa.txt", 0)
    sample_nom.load_xsec("data/xsec_file_sherpa.txt")
    sample_alt = ZHFSample("mg5", "data/list_mg5.txt", 0)
    sample_alt.load_xsec("data/xsec_file_mg5.txt")
    samples = [sample_nom, sample_alt]

    nominal_bin_values = get_zhf_bin_values(sample_nom, h_var_bounds, args)
    variation_bin_values = get_zhf_bin_values(sample_alt, h_var_bounds, args)

    print("nom bin vals  : {}".format(nominal_bin_values))
    print("var bin vals  : {}".format(variation_bin_values))

    deltas = []
    for ibin in range(len(nominal_bin_values)) :
        nom_val = nominal_bin_values[ibin]
        var_val = variation_bin_values[ibin]
        delta = 0.0
        if nom_val != 0 :
            if var_val > nom_val :
                delta = var_val - nom_val
            elif var_val < nom_val :
                delta = nom_val - var_val
            delta /= nom_val
        deltas.append(delta)

    relative_delta = np.array(deltas)
    return relative_delta

    

def get_uncerts(uncert, h_var_bounds, args) :

    variable = h_var_bounds[0]
    n_bins = int(h_var_bounds[1])
    x_lo = h_var_bounds[2]
    x_hi = h_var_bounds[3]

    bin_errors = np.zeros(n_bins)

    udict = uncert_types_dict()[uncert]
    for variation, variation_type in udict.iteritems() :
        print(" -> {} : {}".format(variation, variation_type))
        if variation_type == "superNt" :
            var_bin_deltas = get_superNt_variation(uncert, variation, h_var_bounds, args)
            bin_errors += var_bin_deltas
            #bin_errors += np.power(var_bin_deltas, 2)
        elif uncert == "z" and variation == "mg5" :
            var_bin_deltas = get_z_mg5_variation(uncert, variation, h_var_bounds, args)
            bin_errors += var_bin_deltas
            #bin_errors += np.power(var_bin_delta, 2)

    # symmetrize
    #bin_errors = 0.5 * np.sqrt(bin_errors)
    #print("bin errors: {}".format(bin_errors))

    return bin_errors

def get_error_band(variable_name, args) :

    var_bounds = variables_dict()[variable_name]
    n_bins = var_bounds[2] - var_bounds[1]
    n_bins /= var_bounds[0]
    n_bins = int(n_bins)
    x_lo = var_bounds[1]
    x_hi = var_bounds[2]
    h_var_bounds = [variable_name, n_bins, x_lo, x_hi]

    bin_error = np.zeros(n_bins)
    bin_error_by_proc = {}
    for iuncert, uncert in enumerate(args.uncerts) :
        bin_deltas = get_uncerts(uncert, h_var_bounds, args)

        # apply here the per-bin process fraction
        #for bin, bin_frac in process_fractions :
        #    bin_deltas[bin] *= bin_frac

        bin_erors = np.power(bin_deltas, 2)
        bin_error_by_proc[uncert] = bin_errors

        #bin_error += bin_errors

    for bn, be in bin_error_by_proc.iteritems() :
        bin_error += bin
    bin_error = 0.5 * np.sqrt(bin_error)
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

#!/bin/env python

from __future__ import print_function

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)

import sys, os
import argparse
import glob

mc16a_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/mc/mc16a/output/"
mc16d_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/mc/mc16d/output/"
mc16e_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/mc/mc16e/output/"
mc_dirs = [mc16a_dir, mc16d_dir, mc16e_dir]

ttbar_dsids = ["410472"]
wt_dsids = ["410648", "410649"]


class Sample :
    def __init__(self, name = "", dsid_list = []) :
        self.name = name
        self.dsid_list = dsid_list
        self.tree = None
        self.load()

    def load(self) :
        c = r.TChain("superNt")
        files_to_add = []
        for mc in mc_dirs :
            all_files = glob.glob("%s/CENTRAL*.root" % mc)
            for dsid in self.dsid_list :
                for af in all_files :
                    if dsid in af :
                        files_to_add.append(af)
                        break
        for f in files_to_add :
            c.Add(f)
        self.tree = c
        print("Loaded sample %s with %d entries (%d files)" % (self.name, self.tree.GetEntries(), len(files_to_add)))

def region_dict() :

    rdict = {}
    rdict["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<110 || mbb>140)"
    rdict["top_vr"] = "nBJets>=2 && mll>20 && mll<60 && mbb>140"
    rdict["sr"] = "nBJets>=2 && mll>20 && mll<60 && mbb>110 && mbb<140"
    return rdict

def check_bflav(sample, args) :

    reg_names = { "top_cr" : "CR Top", "top_vr" : "VR Top", "z_cr" : "CR Z+HF", "z_vr" : "VR Z+HF", "sr" : "SR" }
    sample_names = { "top" : "t#bar{t}+Wt", "ttbar" : "t#bar{t}", "wt" : "Wt" }

    selection_str = region_dict()[args.region]
    all_sel = "{} && (isBB==1 || isCC==1 || isBC==1 || isBL==1 || isCL==1 || isLL==1)".format(selection_str)
    heavy_flavor_sel = "%s && (isBB==1 || isBC==1 || isCC==1)" % (selection_str)
    light_flavor_sel = "%s && (isBL==1 || isCL==1 || isLL==1)" % (selection_str)
    weight_str = "eventweightNoPRW_multi"
    weight_str = "1"

    flavors = ["isBB", "isCC", "isBC", "isBL", "isCL", "isLL"]
    flavor_names = ["bb", "cc", "bc", "bl", "cl", "ll"]
    flavor_colors = [r.kRed, r.kYellow, r.kCyan, r.kGreen, r.kMagenta, r.kBlack]

    frac_hf = 0.0
    frac_lf = 0.0

    flavor_histos = {}
    flavor_yields = {}

    c = r.TCanvas("c_flav_{}_{}".format(args.region, sample.name), "", 700, 800)
    c.SetTicks(1,1)
    c.cd()
    stack = r.THStack("flavor_stack_{}_{}".format(args.region, sample.name), "")

    h_all = r.TH1F("h_{}_{}_all".format(args.region, sample.name), "", 1, 1, 2)
    h_all.Sumw2()
    cmd = "isMC>>%s" % h_all.GetName()
    sample.tree.Draw(cmd, "(%s) * %s" % (all_sel, weight_str), "goff")
    err_all = r.Double(0.0)
    yield_all = h_all.IntegralAndError(0,-1, err_all)
    print("yield_all = %.3f" % yield_all)

    total_frac = 0.0
    for iflavor, flavor in enumerate(flavors) :
        cut_str = "{} && {}==1".format(selection_str, flavor)
        h = r.TH1F("h_{}_{}_{}".format(iflavor, args.region, sample.name), "", 1, 1, 2)
        #h.Sumw2()
        cmd = "isMC>>%s" % h.GetName()
        h.SetFillStyle(1001)
        h.SetFillColor(flavor_colors[iflavor])
        sample.tree.Draw(cmd, "(%s) * %s" % (cut_str, weight_str), "goff")
        h.Scale(1.0/yield_all)
        max_val = h.GetMaximum()
        print("Flavor   {0} : {1:.3f}".format(flavor, max_val))
        total_frac += h.Integral()
        flavor_histos[flavor_names[iflavor]] = h
        flavor_yields[flavor_names[iflavor]] = h.Integral()

    print("Total       : {0:.2f}".format(total_frac))

    maxy = total_frac * 1.4
    stack.SetMaximum(maxy)
    for f in flavor_names :
        flavor_histos[f].SetFillStyle(1001)
        stack.Add(flavor_histos[f])


    leg = r.TLegend(0.65, 0.67, 0.88, 0.82)
    leg.SetNColumns(2)
    for f in flavor_names :
        leg.AddEntry(flavor_histos[f], f, "f")

    stack.Draw("hist")
    c.Update()
    leg.Draw()
    c.Update()

    text = r.TLatex()
    text.SetTextFont(42)
    text.SetNDC()
    text.DrawLatex(0.13, 0.84, "#it{#bf{ATLAS}} Simulation Internal")
    text.SetTextSize(0.78 * text.GetTextSize())
    text.DrawLatex(0.13, 0.80, "Selection: {}".format(reg_names[args.region]))
    text.DrawLatex(0.13, 0.76, "Sample: {}".format(sample_names[sample.name]))
    c.Update()

    # save
    outname = "top_flav_plots/flavor_histo_{}_{}.pdf".format(args.region, sample.name)
    print("saving: {}".format(os.path.abspath(outname)))
    c.SaveAs(outname)

def main() :

    parser = argparse.ArgumentParser(description = "Check Top regions b-flavor composition")
    parser.add_argument("--split-top", action = "store_true", default = False,
        help = "Make separate plots/numbers for ttbar and wt"
    )
    parser.add_argument("-r", "--region", default = "top_cr",
        help = "Select a region"
    )
    args = parser.parse_args()

    if args.region not in region_dict() :
        print("ERROR Requested region (={})is not defined".format(args.region))
        sys.exit()

    samples = []
    if args.split_top :
        sample_ttbar = Sample(name = "ttbar", dsid_list = ttbar_dsids)
        sample_wt = Sample(name = "wt", dsid_list = wt_dsids)
        samples = [sample_ttbar, sample_wt]
    else :
        top_dsids = []
        top_dsids.extend(ttbar_dsids)
        top_dsids.extend(wt_dsids)
        sample_top = Sample(name = "top", dsid_list = top_dsids)
        samples = [sample_top]

    for isample, sample in enumerate(samples) :
        print("[{0:02d}/{1:02d}] {2}".format(isample+1, len(samples), sample.name))
        check_bflav(sample, args)

if __name__ == "__main__" :
    main()

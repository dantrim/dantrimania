#!/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)

import sys, os
import json

filename = "bbww_mc16ade.root"

def main() :

    rfile = r.TFile.Open(filename)
    tree = rfile.Get("superNt")
    n_entries = tree.GetEntries()
    print "Loaded tree with %d entries" % n_entries

    weight_str = "eventweightNoPRW_multi * hh_NLO_weight"
    trigger_str = "((year==2015 && trig_tight_2015==1) || (year==2016 && trig_tight_2016==1) || (year==2017 && trig_tight_2017rand==1) || (year==2018 && trig_tight_2018==1))"
    nbjets_str = "nBJets>=2"
    nlep_str = "nLeptons==2"
    presel_str = "%s && %s && %s" % (trigger_str, nbjets_str, nlep_str)
    cuts = [presel_str]
    n_bins = 20
    x_lo = 240
    x_hi = 1600

    h = r.TH1F("h_mhh", "", n_bins, x_lo, x_hi)
    h.Sumw2()

    cmd = "truth_mHH>>%s" % h.GetName()
    cut = "(%s) * %s" % (presel_str, weight_str)
    tree.Draw(cmd, cut, "goff")
    h.Scale(1.0 / h.Integral())
    bc_h = []
    for ibin in range(h.GetNbinsX()) :
        bin_no = ibin+1
        bc = h.GetBinContent(bin_no)
        bc_h.append(bc)
    out_histo = { "presel" : bc_h }

    with open("mhh_presel.json", "w") as outfile :
        json.dump(out_histo, outfile)
    
    #out_histos = {}
    #histos = []
    #for icut, cut_str in enumerate(full_cuts) :
    #    h = r.TH1F("h_%d" % icut, ";Truth m_{hh} [GeV];Selection Efficiency", n_bins, x_lo, x_hi)
    #    h.SetLineColor(colors[icut])
    #    h.SetLineWidth(2)
    #    h.SetMarkerStyle(20)
    #    h.SetMarkerColor(colors[icut])
    #    h.Sumw2()

    #    h_initial = r.TH1F("h_initial_%d" % icut, ";Truth m_{hh} [GeV];Selection Efficiency", n_bins, x_lo, x_hi)
    #    h_initial.Sumw2()

    #    cmd = "truth_mHH>>%s" % h.GetName()
    #    cmd_initial = "truth_mHH>>%s" % h_initial.GetName()

    #    cut = "%s * %s" % (cut_str, weight_str)
    #    cut_initial = "(1) * %s" % (weight_str)

    #    tree.Draw(cmd, cut, "goff")
    #    tree.Draw(cmd_initial, cut_initial, "goff")

    #    h.Divide(h_initial)
    #    histos.append(h)

    #    bc_h = []
    #    for ibin in range(h.GetNbinsX()) :
    #        bin_no = ibin+1
    #        bc = h.GetBinContent(bin_no)
    #        bc_h.append(bc)
    #    out_histos[h_out_names[icut]] = bc_h

    #with open("mhh_sel_eff.json", "w") as outfile :
    #    json.dump(out_histos, outfile)
    #    

    #c = r.TCanvas("c", "", 800, 600)
    #c.SetGrid(1,1)
    #c.SetTicks(1,1)
    #c.cd()

    #leg = r.TLegend(0.7, 0.12, 0.9, 0.32)
    #leg.SetBorderSize(0)
    #leg.SetFillStyle(0)

    #for ih, h in enumerate(histos) :
    #    cmd = "hist e "
    #    h.SetMinimum(0)
    #    h.SetMaximum(1.1)
    #    if ih > 0 : cmd += " same"
    #    h.Draw(cmd)
    #    c.Update()
    #    leg.AddEntry(h, cut_names[ih], "l")
    #leg.Draw()
    #c.Update()
    #c.SaveAs("truth_mhh_wwbb_selection_eff.pdf")
    #x = raw_input()

        

        


if __name__ == "__main__" :
    main()

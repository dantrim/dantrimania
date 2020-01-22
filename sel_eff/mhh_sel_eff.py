#!/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)

import sys, os
import json
from math import sqrt

filename = "bbww_mc16ade.root"

def main() :

    rfile = r.TFile.Open(filename)
    tree = rfile.Get("superNt")
    n_entries = tree.GetEntries()
    print "Loaded tree with %d entries" % n_entries

    weight_str = "eventweightNoPRW_multi * hh_NLO_weight"
    trigger_str = "((year==2015 && trig_tight_2015==1) || (year==2016 && trig_tight_2016==1) || (year==2017 && trig_tight_2017rand==1) || (year==2018 && trig_tight_2018==1))"
    mll_str = "mll>20 && mll<60"
    mbb_str = "mbb>110 && mbb<140"
    dhh0_str = "NN_d_hh>0"
    dhh1_str = "NN_d_hh>2"
    dhh2_str = "NN_d_hh>4"
    dhh3_str = "NN_d_hh>5.45"

    cuts = [trigger_str, mll_str, mbb_str, dhh0_str, dhh1_str, dhh2_str, dhh3_str]
    full_cuts = []
    seed_cut = "("
    for icut, cut_str in enumerate(cuts) :
        if icut == 0 :
            new_cut = "(%s" % cut_str
        else :
            new_cut = "%s && %s" % (seed_cut, cut_str)
        seed_cut = new_cut
        full_cuts.append( "%s)" % new_cut)
        print "cut %d: %s" % (icut, full_cuts[-1])
        

    h_out_names = ["trig", "mll", "mbb", "dhh_0", "dhh_2", "dhh_4", "dhh_545"]
    cut_names = ["Trigger", "m_{ll}", "m_{bb}", "d_{hh}>0", "d_{hh}>2", "d_{hh}>4", "d_{hh}>5.45"]
    colors = [r.kBlack, r.kMagenta, r.kRed, r.kBlue, r.kGreen, r.kCyan, r.kGreen+4]

    n_bins = 20
    x_lo = 240
    x_hi = 1400

    x_lo = 0
    x_hi = -1

    out_histos = {}
    histos = []
    for icut, cut_str in enumerate(full_cuts) :
        h = r.TH1F("h_%d" % icut, ";Truth m_{hh} [GeV];Selection Efficiency", n_bins, x_lo, x_hi)
        h.SetLineColor(colors[icut])
        h.SetLineWidth(2)
        h.SetMarkerStyle(20)
        h.SetMarkerColor(colors[icut])
        h.Sumw2()

        h_initial = r.TH1F("h_initial_%d" % icut, ";Truth m_{hh} [GeV];Selection Efficiency", n_bins, x_lo, x_hi)
        h_initial.Sumw2()

        cmd = "truth_mHH>>%s" % h.GetName()
        cmd_initial = "truth_mHH>>%s" % h_initial.GetName()

        cut = "%s * %s" % (cut_str, weight_str)
        cut_initial = "(1) * %s" % (weight_str)

        tree.Draw(cmd, cut, "goff")
        tree.Draw(cmd_initial, cut_initial, "goff")

        err_initial = r.Double(0.0)
        integral_initial = h_initial.IntegralAndError(0,-1,err_initial)
        err_cut = r.Double(0.0)
        integral_cut = h.IntegralAndError(0,-1,err_cut)
        eff_at_cut = integral_cut / integral_initial
        err_eff = eff_at_cut * sqrt( (err_initial / integral_initial)**2 + (err_cut / integral_cut)**2 )
        print "Efficiency at cut %s: %.3f +/- %.3f  (yield = %.2f +/- %.2f)" % (h_out_names[icut], eff_at_cut, err_eff, integral_cut, err_cut)

        h.Divide(h_initial)
        histos.append(h)

        bc_h = []
        for ibin in range(h.GetNbinsX()) :
            bin_no = ibin+1
            bc = h.GetBinContent(bin_no)
            bc_h.append(bc)
        out_histos[h_out_names[icut]] = bc_h

    with open("test_mhh_sel_eff.json", "w") as outfile :
        json.dump(out_histos, outfile)
        

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

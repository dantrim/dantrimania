#!/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)

import os, sys, argparse
import glob
import subprocess
from math import sqrt
import json

class Sample :
    def __init__(self, name = "", variation = "", treename = "", files = []) :
        self.name = name
        self.variation = variation
        self.files = files
        self.treename = treename
        self.tree = None
        self.load()

    def load(self) :
        ch = r.TChain(self.treename)
        for f in self.files :
            ch.Add(f)
        self.tree = ch
        print "Sample %s (variation = %s) loaded chain from %d files : %d entries total" %(self.name, self.variation, len(self.files), self.tree.GetEntries())

def get_tcut(region_name) :

    dhh_cut = ""

    cuts = {}
    #cuts["top_cr"] = "nBJets>=2 && mll<60 && (mbb>150) && NN_d_hh>4"# % dhh_cut# && isDF==1" # dantrim March 20 : the ntuples are skimmed to have )(mbb in Higgs) OR (mbb>150))
    #cuts["top_cr"] = "nBJets>=2 && mll>60 && (mbb>100 && mbb<140) && NN_d_hh>4"# % dhh_cut# && isDF==1" # dantrim March 20 : the ntuples are skimmed to have )(mbb in Higgs) OR (mbb>150))
    #cuts["top_cr"] = "nBJets>=2 && mll<60 && (mbb>140 || mbb<100) && NN_d_hh>%s" % dhh_cut# && isDF==1"
    #cuts["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>4.5 && isDF==1"
#    cuts["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>4.5 && isDF==1"
#    cuts["sr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb>100 && mbb<140) && NN_d_hh>5.5 && isDF==1"# % dhh_cut
#
#    cuts["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>4.5 && isDF==1"
#    #cuts["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb>100 && mbb<140) && NN_d_hh>4.5"
#    cuts["sr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb>100 && mbb<140) && NN_d_hh>5.5 && isDF==1"
#    #cuts["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>4 && isDF==1"
#    #cuts["sr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb>100 && mbb<140) && NN_d_hh>4 && isDF==1"
    dhh_cut = [4.5, 4.5]
    cuts["top_cr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb<100 || mbb>140) && NN_d_hh>%s && isDF==1" % str(dhh_cut[0])
    cuts["sr"] = "nBJets>=2 && mll>20 && mll<60 && (mbb>100 && mbb<140) && NN_d_hh>%s && isDF==1" % str(dhh_cut[1])
    return cuts[region_name]

def get_yields(samples = [], region_name = "") :

    total_yield = 0.0
    total_stat_uncert = 0.0

    tcut = get_tcut(region_name)
    weight_str = "eventweightNoPRW_multi"
    lumi = 140.5 # not really important for the uncertainty measurement

    for sample in samples :

        h = r.TH1F("h_%s_%s" % (region_name, sample.name), "", 4, 0, 4)
        h.Sumw2()
        sample.tree.Draw("isMC>>%s" % h.GetName(), "(%s) * %s * %s" % (tcut, weight_str, str(lumi)), "goff")
        err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1, err)
        err_sq = err * err
        total_yield += integral
        total_stat_uncert += err_sq

        rel_unc = (float(err) / float(integral)) * 100.

        print "%10s %10s (%10s) : %.3f +/- %.3f (%.3f)" % (region_name, sample.name, sample.variation, total_yield, float(err), rel_unc)

    total_stat_uncert = sqrt(total_stat_uncert)
    return total_yield, total_stat_uncert

def load_inputs(inputs) :

    all_samples = []
    all_names = []
    for input_json in inputs :
        with open(input_json, "r") as j :
            data = json.load(j)
        s_name = data["name"]
        all_names.append(s_name)
        s = data["samples"]
        for var in s :
            var_name = var["variation"]
            var_files = var["files"]
            var_treename = var["treename"]
            var_sample = Sample(s_name, var_name, var_treename, var_files)
            all_samples.append(var_sample)

    return all_samples

def get_sample_yields(samples, region_name) :


    yields_dict = {}
    for sample in samples :
        integral, stat_err = get_yields([sample], region_name)

        results = { sample.variation : [integral, stat_err] }

        if sample.name in yields_dict :
            yields_dict[sample.name].append( results )
        else :
            yields_dict[sample.name] = [ results ]

    return yields_dict

def get_list(dict_list, look_for) :

    for dl in dict_list :
        keys = dl.keys()
        if len(keys) == 1 :
            if keys[0] == look_for :
                return dl[keys[0]]
    return {}

def calculate_tf_uncertainties(sample_name, variations, sr_dict, cr_dict, args) :

    print "sr_dict = %s" % sr_dict
    print "cr_dict = %s" % cr_dict

    nominal_cr = get_list(cr_dict, "nominal")
    nominal_sr = get_list(sr_dict, "nominal")

    nom_cr_yield, nom_cr_stat = nominal_cr[0], nominal_cr[1]
    nom_sr_yield, nom_sr_stat = nominal_sr[0], nominal_sr[1]

    TF_nom = float(nom_sr_yield) / float(nom_cr_yield)
    TF_nom_stat = TF_nom * sqrt( (nom_cr_stat / nom_cr_yield) ** 2 + (nom_sr_stat / nom_sr_yield) ** 2)
    TF_nom_stat_rel = float(TF_nom_stat) / float(TF_nom)

    print "TF nom %.4f +/- %.3f" % (TF_nom, TF_nom_stat)
    for ivar, variation in enumerate(variations) :
        print "%d %s" % (ivar, variation)
        variation_cr = get_list(cr_dict, variation)
        variation_sr = get_list(sr_dict, variation)

        var_cr_yield, var_cr_stat = variation_cr[0], variation_cr[1]
        var_sr_yield, var_sr_stat = variation_sr[0], variation_sr[1]

        rel_stat_sr = float(var_sr_stat) / float(var_sr_yield)
        rel_stat_cr = float(var_cr_stat) / float(var_cr_yield)

        cr_var_frac = float(var_cr_yield) / float(nom_cr_yield)
        sr_var_frac = float(var_sr_yield) / float(nom_sr_yield)
    

        if args.dbg :
            print " %10s (%10s) CR fraction : %.3f" % (sample_name, variation, cr_var_frac)
            print " %10s (%10s) SR fraction : %.3f" % (sample_name, variation, sr_var_frac)

        TF_var = float(var_sr_yield) / float(var_cr_yield)
        TF_var_stat = TF_var * sqrt( rel_stat_sr ** 2 + rel_stat_cr ** 2 )
        #TF_var_stat = sqrt( rel_stat_sr ** 2 + rel_stat_cr ** 2 )
        #print "TF_var_stat_fix = %.4f  TF_var_stat %.4f" % (TF_var_stat_fix, TF_var_stat)
        TF_var_stat_rel = float(TF_var_stat) / float(TF_var)


        print "TF %10s : %.4f +/- %.4f (%.4f)" % (variation, TF_var, TF_var_stat, TF_var_stat_rel)

        TF_uncert_numer = abs(TF_var - TF_nom)
        TF_uncert_denom = TF_nom
        TF_uncert = TF_uncert_numer / TF_uncert_denom

        print "ADDING NOMINAL SAMPLE STAT UNCERTIANTY"
        TF_uncert_stat = TF_uncert * sqrt( TF_var_stat_rel ** 2  + TF_nom_stat_rel ** 2 )
        #TF_uncert_stat = TF_uncert * sqrt( TF_var_stat ** 2 )
        #print "TF_uncert_stat_fix = %.4f   TF_uncert_stat = %.4f" % (TF_uncert_stat_fix, TF_uncert_stat)
        #print " %10s (%10s) var_sr_stat = %.3f   var_sr_yield = %.3f  var_cr_stat = %.3f   var_cr_yield = %.3f   TF = %.3f  TF_var_stat = %.3f  TF_NOM = %.3f   DELTA_TF = %.3f  DELTA_TF_STAT_ERR = %.3f" % (sample_name, variation, var_sr_stat, var_sr_yield, var_cr_stat, var_cr_yield, TF_var, TF_var_stat, TF_nom, TF_uncert, TF_uncert_stat)

        TF_uncert_quad_sum = sqrt( TF_uncert ** 2 + TF_uncert_stat ** 2 )

        print "%10s (variation = %10s) TF uncertainty : %.5f +/- %.5f ==> %.5f" % (sample_name, variation, TF_uncert, TF_uncert_stat, TF_uncert_quad_sum)

def make_plots(samples, args) :

    var_to_plot = args.plotvar

    vardict = {}
    vardict["mbb"] = [20, 100, 400]
    vardict["NN_d_hh"] = [10, 0, 10]
    #vardict["NN_d_hh"] = [20, -10, 10]
    n_bins = vardict[var_to_plot][0]
    x_low = vardict[var_to_plot][1]
    x_high = vardict[var_to_plot][2]

    c = r.TCanvas("c", "", 700, 800)
    upper_pad = r.TPad("upper", "upper", 0., 0., 1., 1.)
    lower_pad = r.TPad("lower", "lower", 0., 0., 1., 1.)
    c.cd()

    upper_pad.SetPad(0., 1.0 - 0.75, 1.0, 1.0)
    lower_pad.SetPad(0., 0., 1.0, 0.3)
    upper_pad.SetTicks(1,1)
    lower_pad.SetTicks(1,1)
    upper_pad.SetGrid(1,1)
    lower_pad.SetGrid(1,1)

    upper_pad.SetFrameFillColor(0)
    upper_pad.SetFillColor(0)

    upper_pad.SetRightMargin(0.05)
    lower_pad.SetRightMargin(0.05)

    upper_pad.SetLeftMargin(0.14)
    lower_pad.SetLeftMargin(0.14)

    upper_pad.SetTopMargin(0.7 * upper_pad.GetTopMargin())
    upper_pad.SetBottomMargin(0.09)
    lower_pad.SetBottomMargin(0.4)


    upper_pad.Draw()
    lower_pad.Draw()
    c.Update()

    sample_names = []
    colors = [r.kBlack, r.kGreen, r.kRed, r.kBlue, r.kMagenta]
    histos = []
    histos_ratio = []
    integrals = []
    nominal_integral = 0.0

    for ir in range(2) :
        for isample, sample in enumerate(samples) :
            sample_names.append("%s - %s" % (sample.name, sample.variation))
            h = r.TH1F("h_%d_%s_%s_%d" % (isample, var_to_plot, sample.variation, ir), ";%s;a.u." % var_to_plot, n_bins, x_low, x_high)
            h.Sumw2()
            cmd = "%s>>%s" % (var_to_plot, h.GetName())
            cut = "(nBJets>=2 && mbb>150) * eventweightNoPRW_multi"
            sample.tree.Draw(cmd, cut, "goff")
            #h.Scale(1.0 / h.Integral())
            if "nom" in sample.variation :
                nominal_integral = h.Integral()
            integrals.append(h.Integral())
            h.SetLineWidth(2)
            h.SetLineColor(colors[isample])
            if ir == 0 :
                h.GetXaxis().SetTitleOffset(999)
                h.GetXaxis().SetLabelOffset(999)
                histos.append(h)
            else :
                h.GetXaxis().SetTitleSize(3 * h.GetXaxis().GetTitleSize())
                h.GetXaxis().SetLabelSize(3 * h.GetXaxis().GetLabelSize())
                #h.GetYaxis().SetLabelSize(histos[0].GetYaxis().GetLabelSize())
                h.GetYaxis().SetLabelSize(2.7 * h.GetYaxis().GetLabelSize())
                histos_ratio.append(h)

    leg = r.TLegend(0.7, 0.7, 0.87, 0.87)

    upper_pad.cd()
    for ih, h in enumerate(histos) :
        h.Scale( nominal_integral / integrals[ih] ) #integrals[ih] / nominal_integral )
        leg.AddEntry(h, sample_names[ih], "l")
        cmd = "hist e"
        if ih > 0 :
            cmd += " same"
        h.Draw(cmd)
        c.Update()

    leg.Draw()
    c.Update()

    # ratio
    lower_pad.cd()
    histo_nominal = None
    for ih, h in enumerate(histos_ratio) :
        h.Scale( nominal_integral / integrals[ih])
    for ih, h in enumerate(histos_ratio) :
        if "nom" in h.GetName() :
            histo_nominal = h
    ratios = []
    for ih, h in enumerate(histos_ratio) :
        if "nom" in h.GetName() : continue
        h.Divide(histo_nominal)
        h.GetYaxis().SetNdivisions(6)
        h.SetMaximum(2)
        h.SetMinimum(0)
        print "hr %.2f" % h.Integral()
        ratios.append(h)

    for ir, hr in enumerate(ratios) :
        cmd = "hist e"
        if ir > 0 :
            cmd += " same"
        hr.Draw(cmd)
        c.Update()

    outname = "modelling_sys_plots/sys_plot_%s_%s.pdf" % (samples[0].name, var_to_plot)
    print "saving plot to: %s" % os.path.abspath(outname)
    c.SaveAs(outname)

def main() :

    parser = argparse.ArgumentParser(description = "Calculate TF uncertainties")
    parser.add_argument("-j", "--json", nargs = "+", required = True,
        help = "Provide input JSON file configuring samples and variations"
    )
    parser.add_argument("--uncerts", action = "store_true", default = False,
        help = "Calculate TF uncertainties for each of the variations"
    )
    parser.add_argument("--plots", action = "store_true", default = False,
        help = "Make plots"
    )
    parser.add_argument("--plotvar", default = "mbb",
        help = "Select a var to plot"
    )
    parser.add_argument("-m", "--mc-campaign", default = "",
        help = "Specify a specific MC campaign to consider [defualt: all available]"
    )
    parser.add_argument("-v", "--variation", default = "",
        help = "Specify a specfic variation (must exist in input JSON file)"
    )
    parser.add_argument("--cr", required = True,
        help = "Specify which CR to calcualte TF for"
    )
    parser.add_argument("--dbg", action = "store_true", default = False,
        help = "Debug mode"
    )
    args = parser.parse_args()

    samples = load_inputs(args.json)
    variations = {}
    for s in samples :
        if s.name in variations :
            variations[s.name].append(s.variation)
        else :
            variations[s.name] = [s.variation]
    if args.uncerts :
        cr_yield_dict = get_sample_yields(samples, args.cr)
        sr_yield_dict = get_sample_yields(samples, "sr")

        for sample_name in variations :
            variations = [v for v in variations[sample_name]]
            tmp = []
            for v in variations :
                if v != "nominal" : tmp.append(v)
            variations = tmp
            print "variations = %s" % variations
            sr_dict = sr_yield_dict[sample_name]
            cr_dict = cr_yield_dict[sample_name]
        
            calculate_tf_uncertainties(sample_name, variations, sr_dict, cr_dict, args)

    if args.plots :
        make_plots(samples, args)
        
    

if __name__ == "__main__" :
    main()

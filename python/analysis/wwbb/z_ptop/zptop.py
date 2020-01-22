#!/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

import os, sys
import argparse
import glob

filelist_dir = "/data/uclhc/uci/user/dantrim/n0307val/susynt-read/filelists/zjets_and_dy_sherpa_mc16d/"
mc16a_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16a/output/"
mc16d_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16d/output/"
mc16e_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16e/output/"
mc16_dirs = [ mc16a_dir, mc16d_dir, mc16e_dir ]

class Sample :

    def __init__(self, name = "", dsid_list = []) :
        self.name = name
        self.dsid_list = dsid_list
        self.tree = None
        self.load()

    def load(self) :

        c = r.TChain("superNt")
        sample_files = []
        for mc_dir in mc16_dirs :
            all_files = glob.glob("%s/CENTRAL*.root" % mc_dir)
            for dsid in self.dsid_list :
                for af in all_files :
                    af_short = af.strip().split("/")[-1]
                    if dsid in af_short :
                        sample_files.append(af)
                        break
        for sf in sample_files :
            c.Add(sf)
        self.tree = c
        print "Sample %s loaded tree with %d entries (%d files)" % (self.name, self.tree.GetEntries(), len(sample_files))

def dsid_from_list(x) :

    x = x.strip().split("/")[-1]
    find = "13TeV."
    dsid = x.strip().split(find)[1].split(".")[0]
    return dsid

def get_mll_samples() :

    all_filelists = glob.glob("%s/*.txt" % filelist_dir)
    sf_lists = []
    for af in all_filelists :
        af_short = af.strip().split("/")[-1]
        if "Ztt" in af_short or "Ztautau" in af_short : continue
        sf_lists.append(af)


    low_mll_lists = []
    high_mll_lists = []

    for sf in sf_lists :
        sf_short = sf.strip().split("/")[-1]
        if "Mll10" in sf_short :
            low_mll_lists.append(sf)
        else :
            high_mll_lists.append(sf)

    low_mll_dsids = [ dsid_from_list(x) for x in low_mll_lists ]
    high_mll_dsids = [ dsid_from_list(x) for x in high_mll_lists ]

    print "Found %d low mll dsids" % len(low_mll_dsids)
    print "Found %d high mll dsids" % len(high_mll_dsids)

    sample_low_mll = Sample(name = "mll_low", dsid_list = low_mll_dsids)
    sample_high_mll = Sample(name = "mll_high", dsid_list = high_mll_dsids)

    return [sample_low_mll, sample_high_mll]

def get_flavor_samples() :

    all_filelists = glob.glob("%s/*.txt" % filelist_dir)
    sf_lists = []
    for af in all_filelists :
        af_short = af.strip().split("/")[-1]
        if "Ztt" in af_short or "Ztautau" in af_short : continue
        if "Mll10" in af_short : continue
        sf_lists.append(af)

    cbv_lists = []
    cvbv_lists = []
    b_lists = []
    for sf in sf_lists :
        sf_short = sf.strip().split("/")[-1]
        if "CFiltBV" in sf_short :
            cbv_lists.append(sf)
        elif "CVBV" in sf_short :
            cvbv_lists.append(sf)
        elif "BFilt" in sf_short :
            b_lists.append(sf)

    cbv_dsids = [ dsid_from_list(x) for x in cbv_lists ]
    cvbv_dsids = [ dsid_from_list(x) for x in cvbv_lists ]
    b_dsids = [ dsid_from_list(x) for x in b_lists ]

    sample_cbv = Sample(name = "flavor_cbv", dsid_list = cbv_dsids)
    sample_cvbv = Sample(name = "flavor_cvbv", dsid_list = cvbv_dsids)
    sample_b = Sample(name = "flavor_b", dsid_list = b_dsids)

    return [sample_cbv, sample_b] #sample_cvbv, sample_b]

def get_pt_samples() :

    all_filelists = glob.glob("%s/*.txt" % filelist_dir)
    sf_lists = []
    for af in all_filelists :
        af_short = af.strip().split("/")[-1]
        if "Ztt" in af_short or "Ztautau" in af_short : continue
        if "Mll10" in af_short : continue
        sf_lists.append(af)

    slices = ["0_70", "70_140", "140_280", "280_500", "500_1000", "1000_E_CMS"]
    slice_lists = []
    for pt_slice in slices :
        pt_slice_list = []
        for sf in sf_lists :
            sf_short = sf.strip().split("/")[-1]
            if pt_slice in sf_short :
                pt_slice_list.append(sf)
        slice_lists.append(pt_slice_list)

    slice_dsids = []
    for slice_list in slice_lists :
        dsid_list = [ dsid_from_list(x) for x in slice_list ]
        slice_dsids.append(dsid_list)

    samples = []
    for idsid, dsid_list in enumerate(slice_dsids) :
        sample = Sample(name = "pt_%s" % slices[idsid], dsid_list = dsid_list)
        samples.append(sample)
    return samples

def make_mll_plot(samples, args) :

    selection_str = "nBJets>=2 && mll>20"
    weight_str = "eventweightNoPRW_multi"
    full_cut_str = "(%s) * %s" % (selection_str, weight_str)

    c = r.TCanvas("c", "", 700, 800)
    c.SetLeftMargin(1.2 * c.GetLeftMargin())
    c.SetTicks(1,1)
    c.SetGrid(1,1)
    c.cd()

    histos = []
    names = []
    nice_names = { "mll_low" : "Z, m_{ll} < 40 GeV", "mll_high" : "Z, m_{ll} > 40 GeV" }

    colors = [r.kRed, r.kBlack]

    histos = []
    maxy_vals = []
    for isample, sample in enumerate(samples) :
        h = r.TH1F("h_{}_{}".format(isample, sample.name), ";p_{top};a.u.", 20, 0, 1)
        h.Sumw2()
        h.SetLineWidth(2)
        h.SetLineColor(colors[isample])

        cmd = "NN_p_top>>%s" % h.GetName()
        sample.tree.Draw(cmd, full_cut_str, "goff")
        print "Sample %s : entries %d" % (sample.name, h.GetEntries())
        if h.Integral() == 0 : continue

        h.Scale(1.0 / h.Integral())
        maxy_vals.append(h.GetMaximum())
        histos.append(h)

    leg = r.TLegend(0.6, 0.8, 0.88, 0.88)

    maxy = max(maxy_vals) * 1.25
    for ihist, hist in enumerate(histos) :
        hist.SetMaximum(maxy)
        cmd = "hist e"
        if ihist > 0 :
            cmd += " same"
        hist.Draw(cmd)
        c.Update()
        leg.AddEntry(hist, nice_names[samples[ihist].name], "l")

    leg.Draw()
    c.Update()

    # save
    outname = "zptop_plots/zptop_mll.pdf"
    print "Saving: %s" % os.path.abspath(outname)
    c.SaveAs(outname)


    

def make_flavor_plot(samples, args) :

    selection_str = "nBJets>=2 && mll>20"
    weight_str = "eventweightNoPRW_multi"
    full_cut_str = "(%s) * %s" % (selection_str, weight_str)

    c = r.TCanvas("c", "", 700, 800)
    c.SetLeftMargin(1.2 * c.GetRightMargin())
    c.SetTicks(1,1)
    c.SetGrid(1,1)
    c.cd()

    histos = []
    names = []
    nice_names = { "flavor_cbv" : "C-Filter", "flavor_cvbv" : "Veto", "flavor_b" : "B-Filter" }

    colors = [r.kRed, r.kBlue, r.kBlack]
    for isample, sample in enumerate(samples) :
        h = r.TH1F("h_{}_{}".format(isample, sample.name), ";p_{top};a.u.", 20, 0, 1)
        h.Sumw2()
        h.SetLineWidth(2)
        h.SetLineColor(colors[isample])

        cmd = "NN_p_top>>%s" % h.GetName()
        sample.tree.Draw(cmd, full_cut_str, "goff")
        h.Scale(1.0 / h.Integral())
        histos.append(h)

    leg = r.TLegend(0.7, 0.8, 0.88, 0.88)

    for ihist, hist in enumerate(histos) :
        hist.SetMaximum(0.17)
        cmd = "hist e"
        if ihist > 0 :
            cmd += " same"
        hist.Draw(cmd)
        c.Update()
        leg.AddEntry(hist, nice_names[samples[ihist].name], "l")

    leg.Draw()
    c.Update()

    # save
    outname = "zptop_plots/zptop_flavor.pdf"
    print "Saving: %s" % os.path.abspath(outname)
    c.SaveAs(outname)

def make_pt_plot(samples, args) :

    selection_str = "nBJets>=2 && mll>20"
    weight_str = "eventweightNoPRW_multi"
    full_cut_str = "(%s) * %s" % (selection_str, weight_str)

    c = r.TCanvas("c", "", 700, 800)
    c.SetLeftMargin( 1.2 * c.GetRightMargin())
    c.SetTicks(1,1)
    c.SetGrid(1,1)
    c.cd()

    names = ["0_70", "70_140", "140_280", "280_500", "500_1000", "1000_E_CMS"]
    nice_names = ["Z p_{T} slice %s" % x.replace("_","-") for x in names]
    colors = [r.kBlack, r.kRed, r.kGreen, r.kBlue, r.kMagenta, r.kCyan]

    var_to_plot = "NN_p_top"
    var_name = "p_{top}"
    n_bins = 20
    x_low = 0
    x_high = 1

    #var_to_plot = "NN_d_hh"
    #var_name = "d_{hh}"
    #n_bins = 20
    #x_low = -10
    #x_high = 10

    histos = []
    maxy_vals = []
    for isample, sample in enumerate(samples) :
        h = r.TH1F("h_{}_{}".format(isample, sample.name), ";%s;a.u." % var_name, n_bins, x_low, x_high)
        h.Sumw2()
        h.SetLineWidth(2)
        h.SetLineColor(colors[isample])
        h.SetMinimum(0)
        cmd = "%s>>%s" % (var_to_plot, h.GetName())
        sample.tree.Draw(cmd, full_cut_str, "goff")
        if h.Integral() == 0 : continue
        h.Scale(1.0 / h.Integral())
        maxy_vals.append(h.GetMaximum())
        histos.append(h)

    if "top" in var_to_plot :
        leg = r.TLegend(0.4, 0.65, 0.83, 0.88)
    elif "hh" in var_to_plot :
        leg = r.TLegend(0.45, 0.65, 0.88, 0.88)
    maxy = max(maxy_vals) * 1.25

    for ihist, hist in enumerate(histos) :
        hist.SetMaximum(maxy)
        hist.SetMinimum(0)
        cmd = "hist e"
        if ihist > 0 :
            cmd += " same"
        hist.Draw(cmd)
        c.Update()
        leg.AddEntry(hist, nice_names[ihist], "l")

    leg.Draw()
    c.Update()

    # save
    outname = "zptop_plots/zptop_pt_%s.pdf" % var_to_plot
    print "Saving: %s" % os.path.abspath(outname)
    c.SaveAs(outname)

    

def main() :

    parser = argparse.ArgumentParser(description = "Plot Z-SF samples in p_top")
    parser.add_argument("--mll", action = "store_true", default = False,
        help = "Plot low mll vs high  mll"
    )
    parser.add_argument("--pt", action = "store_true", default = False,
        help = "Plot pT slices"
    )
    parser.add_argument("--flavor", action = "store_true", default = False,
        help = "Plot in flavor slices"
    )
    args = parser.parse_args()

    samples = []
    if args.mll :
        samples = get_mll_samples()
        make_mll_plot(samples, args)
    if args.flavor :
        samples = get_flavor_samples()
        make_flavor_plot(samples, args)
    if args.pt :
        samples = get_pt_samples()
        make_pt_plot(samples, args)



if __name__ == "__main__" :
    main()

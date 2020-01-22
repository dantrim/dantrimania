#!/bin/env python

import os, sys, argparse
import glob
import subprocess
from math import sqrt

import ROOT as r
r.gROOT.SetBatch(True)
r.PyConfig.IgnoreCommandLineOptions = True

files_ttbar = ["/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16a/output_410472/"]#,
                #"/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16d/output_410472/",
                #"/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16e/output_410472/"]
    

files_WtDR = ["/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16a/output/CENTRAL_410648_mc16a.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16a/output/CENTRAL_410649_mc16a.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16d/output/CENTRAL_410648_mc16d.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16d/output/CENTRAL_410649_mc16d.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16e/output/CENTRAL_410648_mc16e.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16e/output/CENTRAL_410649_mc16e.root"
            ]
files_WtDS = ["/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16a/output/CENTRAL_410656_mc16a.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16a/output/CENTRAL_410657_mc16a.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16d/output/CENTRAL_410656_mc16d.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16d/output/CENTRAL_410657_mc16d.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16e/output/CENTRAL_410656_mc16e.root",
              "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/mc16e/output/CENTRAL_410657_mc16e.root"
            ]

class Sample :
    def __init__(self, name = "", files = []) :
        self.name = name
        self.files = files
        self.tree = None
        self.load()

    def load(self) :
        ch = r.TChain("superNt")
        if "ttbar" in self.name.lower() :
            files_to_add = []
            for fdir in self.files :
                infiles = glob.glob("%s/CENTRAL*.root" % fdir)
                for f in infiles :
                    files_to_add.append(f)
            for f in files_to_add :
                ch.Add(f)
        else :
            for f in self.files :
                ch.Add(f)
        self.tree = ch
        print "Sample %s loaded chain from %d files : %d entries total" %(self.name, len(self.files), self.tree.GetEntries())

def get_tcut(region_name) :

    dhh_cut = "4"

    cuts = {}
    cuts["top_cr"] = "nBJets>=2 && mll<60 && (mbb>140 || mbb<100) && NN_d_hh>%s" % dhh_cut# && isDF==1"
    cuts["sr"] = "nBJets>=2 && mll<60 && (mbb>100 && mbb<140) && NN_d_hh>%s" % dhh_cut
    return cuts[region_name]

def get_yields(samples = [], region_name = "") :

    total_yield = 0.0
    total_stat_uncert = 0.0

    tcut = get_tcut(region_name)
    weight_str = "eventweightNoPRW_multi"
    lumi = 140.5

    for sample in samples :

        h = r.TH1F("h_%s_%s" % (region_name, sample.name), "", 4, 0, 4)
        sample.tree.Draw("isMC>>%s" % h.GetName(), "(%s) * %s * %s" % (tcut, weight_str, str(lumi)), "goff")
        err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1, err)
        err_sq = err * err
        total_yield += integral
        total_stat_uncert += err_sq

        rel_unc = (float(err) / float(integral)) * 100.

        print "%s %s : %.3f +/- %.3f (%.3f)" % (region_name, sample.name, total_yield, float(err), rel_unc)

    total_stat_uncert = sqrt(total_stat_uncert)
    return total_yield, total_stat_uncert


def calculate_tf_uncerts(sample_dr, sample_ds, sample_tt, args) :

    dr_samples = [sample_dr]
    ds_samples = [sample_ds]
    if sample_tt :
        dr_samples.append(sample_tt)
        ds_samples.append(sample_tt)

    cr_yield_dr, cr_err_dr = get_yields(dr_samples, "top_cr")
    cr_yield_ds, cr_err_ds = get_yields(ds_samples, "top_cr")

    sr_yield_dr, sr_err_dr = get_yields(dr_samples, "sr")
    sr_yield_ds, sr_err_ds = get_yields(ds_samples, "sr")

    cr_frac = float(cr_yield_ds) / float(cr_yield_dr)
    sr_frac = float(sr_yield_ds) / float(sr_yield_dr)
    print "CR fraction: %.3f" % cr_frac
    print "SR fraction: %.3f" % sr_frac

    tf_dr = sr_yield_dr / cr_yield_dr
    tf_ds = sr_yield_ds / cr_yield_ds

    tf_dr_unc = tf_dr * sqrt((sr_err_dr / sr_yield_dr)**2 + (cr_err_dr / cr_yield_dr)**2)
    tf_ds_unc = tf_ds * sqrt((sr_err_ds / sr_yield_ds)**2 + (cr_err_ds / cr_yield_ds)**2)

    print 60 * "-"
    print " TF DR = %.3f +/- %.3f (rel unc = %.3f %%)" % (tf_dr, tf_dr_unc, abs(tf_dr_unc/tf_dr) * 100.)
    print " TF DS = %.3f +/- %.3f (rel unc = %.3f %%)" % (tf_ds, tf_ds_unc, abs(tf_ds_unc/tf_ds) * 100.)


    tf_num_unc = sqrt( (tf_dr_unc)**2 + (tf_ds_unc)**2 )
    tf_den_unc = tf_dr_unc

    delta_tf_num = tf_ds - tf_dr
    delta_tf_den = tf_dr
    delta_tf = delta_tf_num / delta_tf_den


    print "A = %.5f  B = %.5f, DEN = %.5f" % ( (tf_ds - tf_dr), delta_tf_num, tf_dr )
    print "DELTA TF = (%.3f - %.3f) / %.3f = %.3f / %.3f = %.5f" % (tf_ds, tf_dr, tf_dr, (tf_ds - tf_dr), tf_dr, (tf_ds - tf_dr) / tf_dr)


    #print "delta_tf_num_unc = %.5f  delta_tf_num = %.5f" % (tf_num_unc, delta_tf_num)
    #print "delta_tf_den_unc = %.5f  delta_tf_den = %.5f" % (tf_den_unc, delta_tf_den)

    
    delta_tf_unc = abs(delta_tf) * sqrt( (tf_num_unc / delta_tf_num)**2 + (tf_den_unc / delta_tf_den)**2 )
    quad_sum = sqrt( delta_tf**2 + delta_tf_unc**2 )

    print "TF uncert: %.4f +/- %.4f (rel unc = %.2f%%) ===> %.3f" % (abs(delta_tf), delta_tf_unc, abs(delta_tf_unc/delta_tf) * 100., quad_sum)


def main() :

    parser = argparse.ArgumentParser(description = "Compare DR and DS top background estimates")
    parser.add_argument("--plots", default = False, action = "store_true",
        help = "Make plots"
    )
    parser.add_argument("--var", default = "",
        help = "Select specific variable to plot"
    )
    parser.add_argument("--uncerts", default = False, action = "store_true",
        help = "Calculate TF uncertainties"
    )
    parser.add_argument("--ttbar", default = False, action = "store_true",
        help = "Include ttbar"
    )

    args = parser.parse_args()

    sample_ttbar = None #Sample("ttbar", files_ttbar)
    if args.ttbar :
        sample_ttbar = Sample("ttbar", files_ttbar)
    sample_wtDR = Sample("wtDR", files_WtDR)
    sample_wtDS = Sample("wtDS", files_WtDS)

    if args.uncerts :
        calculate_tf_uncerts(sample_wtDR, sample_wtDS, sample_ttbar, args)
    

if __name__ == "__main__" :
    main()

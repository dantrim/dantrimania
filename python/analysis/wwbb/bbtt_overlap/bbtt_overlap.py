#!/bin/env python

import sys, os, argparse

import h5py
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

from overlay_nn import Sample, chunk_generator, valid_idx

file_bbtt = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/bbtt_signal/bbtautau_dilep_combined.h5"
file_bbww = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/mc/bbww_dilep_combined.h5"

def variable_dict() :

    v = {}
    v["l0_pt"] = [ [10, 0, 300], "Leading lepton $p_{T}$ [GeV]" ]
    v["l1_pt"] = [ [10, 0, 300], "Sub-leading lepton $p_{T}$ [GeV]" ]
    v["mll"] = [ [5, 0, 100], "$m_{\\ell \\ell}$ [GeV]" ]
    v["NN_d_hh"] = [ [2, -30, 30], "$d_{hh}$" ]
    return v

def get_sample_data(sample, varname) :

    data = []
    w = []
    total_read = 0
    with h5py.File(sample.filename, "r", libver = "latest") as sample_file :
        dataset = sample_file["superNt"]
        for chunk in chunk_generator(dataset) :
            total_read += chunk.size
            print("Reading (%s) %d" % (sample.name, total_read))
            idx = (chunk["l0_pt"]>10) & (chunk["l1_pt"]>10) & (chunk["nBJets"]>=2) & (chunk["NN_d_hh"]>0)
            chunk = chunk[idx]
            var_data = chunk[varname]
            weights = chunk["eventweightNoPRW_multi"]
            data.extend(var_data)
            w.extend(weights)
    return data, w

def make_plots(samples, args) :

    var_dict = variable_dict()
    n_vars = len(var_dict)
    for iv, v in enumerate(var_dict) :
        if args.var :
            if v not in args.var : continue
        print("[%03d/%03d] Plotting %s" % (iv+1, n_vars, v))

        x_bounds = var_dict[v][0]
        x_label = var_dict[v][1]

        bin_width = x_bounds[0]
        x_low = x_bounds[1]
        x_high = x_bounds[2]
        bin_edges = np.arange(x_low - bin_width, x_high + 2 * bin_width, bin_width)
        bin_centers = bin_edges + 0.5 * bin_width
        bin_centers = bin_centers[:-1]

        histo_data = []
        weight_data = []
        labels = [s.name for s in samples]
        for sample in samples :
            data, w = get_sample_data(sample, v)
            histo_data.append(data)
            weight_data.append(w)

        fig = plt.figure(figsize = (7,8))
        grid = GridSpec(100, 100)
        upper_pad = fig.add_subplot(grid[0:40,:])
        #middle_pad = fig.add_subplot(grid[52:73,:], sharex = upper_pad)
        #lower_pad = fig.add_subplot(grid[75:100,:], sharex = upper_pad)
        middle_pad = fig.add_subplot(grid[42:60,:], sharex = upper_pad)
        lower_pad =  fig.add_subplot(grid[62:80,:], sharex = upper_pad)
        br_pad = fig.add_subplot(grid[82:100,:], sharex = upper_pad)

        for pad in [upper_pad, middle_pad, lower_pad] :
            pad.set_xlim([x_low, x_high])
            pad.tick_params(axis = 'both', which = 'both', labelsize = 16, direction = 'in',
                labelleft = True, bottom = True, top = True, left = True)
            pad.grid(color = 'k', which = 'both', linestyle = '-', lw = 1, alpha = 0.1)

        upper_pad.set_xlabel("")
        middle_pad.set_xlabel("")
        upper_pad.get_xaxis().set_visible(False)
        upper_pad.set_ylabel("a.u.", horizontalalignment = "right", y = 1.0)
        middle_pad.set_ylabel("Ratio")
        lower_pad.set_ylabel("Fraction")
        lower_pad.set_xlabel(x_label, horizontalalignment = "right", x = 1.0)

        histograms = []
        totals = []
        maxys = []
        for ihist, hist in enumerate(histo_data) :
            y, _ = np.histogram(hist, weights = weight_data[ihist], bins = bin_edges)
            integral = np.sum(y)
            maxy = max(y)
            maxy /= integral
            maxys.append(maxy)
            y /= integral
            integral = np.sum(y)
            totals.append(integral)
            histograms.append(y)

        maxy = max(maxys)
        maxy = 1.2 * maxy

        for ih, h in enumerate(histograms) :
            upper_pad.step(bin_centers, h, where = "mid", label = samples[ih].name)
        upper_pad.legend(loc = "best", frameon = False)


        # save
        outname = "%s/bbtt_comp_%s.png" % (args.outdir, v)
        print("Saving figure to %s" % (os.path.abspath(outname)))
        fig.savefig(outname, bbox_inches = "tight", dpi = 200)

def main() :

    parser = argparse.ArgumentParser(description = "Make plots comparing stuff to stuff")
    parser.add_argument("-o", "--output", default = "./",
        help = "Output directory for any output"
    )
    parser.add_argument("-v", "--var", nargs = "+",
        help = "Select a variable to plot"
    )
    args = parser.parse_args()

    sample_bbtt = Sample("bbtt", file_bbtt, "")
    sample_bbww = Sample("bbww", file_bbww, "")
    samples = [sample_bbtt, sample_bbww]

    make_plots(samples, args)

if __name__ == "__main__" :
    main()

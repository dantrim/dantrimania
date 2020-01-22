#!/bin/env python

from __future__ import print_function

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
import matplotlib
matplotlib.use("pdf")

import sys, os
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

data_file = "mhh_sel_eff.json"

class Histo :
    def __init__(self, cut_name = "", bin_content = None) :
        self.cut_name = cut_name
        self.bin_content = bin_content
    def __str__(self) :
        return "Histo %s : %s" % (self.cut_name, self.bin_content)

def nice_cut_names(cut_name) :

    v = {}
    #v["trig"] = "Trigger"
    #v["mll"] = "$m_{\\ell\ell}$"
    #v["mbb"] = "$m_{bb}$"
    #v["dhh_0"] = "$d_{HH} > 0$"
    #v["dhh_2"] = "$d_{HH} > 2$"
    #v["dhh_4"] = "$d_{HH} > 4$"
    #v["dhh_545"] = "$d_{HH} > 5.45$"
    v["trig"] = "Trigger"
    v["mll"] = r"\textit{m}$_{\mbox{\tiny{\textit{ll}}}} \le$ 60 GeV"
    v["mbb"] = r"\textit{m}$_{\mbox{\tiny{\textit{bb}}}} \in$ (110,140) GeV"
    v["dhh_0"] = r"\textit{d}$_{\mbox{\tiny{\textit{HH}}}}\ge$ 0"
    v["dhh_2"] = r"\textit{d}$_{\mbox{\tiny{\textit{HH}}}}\ge$ 2"
    v["dhh_4"] = r"\textit{d}$_{\mbox{\tiny{\textit{HH}}}}\ge$ 4"
    v["dhh_545"] = r"\textit{d}$_{\mbox{\tiny{\textit{HH}}}}\ge$ 5.45"
    return v[cut_name]

def get_cut_color(cut_name) :

    c = {}
    c["trig"] = "k"
    c["mll"] = "#016fb9"
    c["mbb"] = "#ff9505"
    c["dhh_0"] = "#ec4e20"
    c["dhh_2"] = "g"
    c["dhh_4"] = "b"
    c["dhh_545"] = "r"
    return c[cut_name]

def cut_order() :

    return ["trig", "mll", "mbb", "dhh_0", "dhh_2", "dhh_4", "dhh_545"]

def get_plot_data() :

    with open(data_file, "r") as infile :
        json_data = json.load(infile)

    histos = {}
    for cut_name, data in json_data.items() :
        h = Histo(cut_name, data)
        histos[cut_name] = h
    return histos

def get_mhh_data() :

    with open("mhh_presel.json", "r") as infile :
        json_data = json.load(infile)
    histos = {}
    for cut_name, data in json_data.items() :
        h = Histo(cut_name, data)
        histos[cut_name] = h
    return histos

def make_plot() :

    plot_data = get_plot_data()

    n_bins = 20
    x_lo = 240
    x_hi = 1600
    bin_width = int((x_hi - x_lo) / n_bins)

    fig, ax = plt.subplots(1,1)
    
    ax.tick_params(axis = 'both', which = 'both', labelsize = 10, direction = 'in',
        labelleft = True, bottom = True, top = True, left = True, right = True)
    #ax.grid(color = 'k', which = 'both', linestyle = '-', lw = 1, alpha = 0.1)

    ax.tick_params(which = "major", length = 7, zorder = 1e9)
    ax.tick_params(which = "minor", length = 4, zorder = 1e9)
    
    ax.set_xlabel(r"Truth \textit{m}$_{\mbox{\normalsize{\textit{HH}}}}$ [GeV]", horizontalalignment = 'right', x = 1,
        fontsize = 15)
    ax.set_ylabel('Selection Efficiency', horizontalalignment = 'right', y = 1,
        fontsize = 15)

    bin_edges = np.arange(x_lo - bin_width, x_hi + 2 * bin_width, bin_width)
    bin_centers = bin_edges + 0.5 * bin_width
    bin_centers = bin_centers[:-1]

    for icut, cut in enumerate(cut_order()) :
        h = plot_data[cut]
        data = h.bin_content
        x_vals = []
        y_vals = []
        for ie, e in enumerate(bin_edges[1:-2]) :
            x_vals.append(e)
            x_vals.append(e + bin_width)
            if data[ie] > 1.0 :
                data[ie] = 0.98 * data[ie]
            y_vals.append(data[ie])
            y_vals.append(data[ie])
        ax.plot(x_vals, y_vals, label = "Req. \#%d: %s" % (icut+1, nice_cut_names(cut)),
                color = get_cut_color(cut))

    ##
    ## draw the bare mHH distribution
    ##
    mhh_histo = get_mhh_data()
    h_mhh = mhh_histo["presel"]
    data_mhh = h_mhh.bin_content
    x_vals = []
    y_vals = []
    for ie, e in enumerate(bin_edges[1:-2]) :
        x_vals.append(e)
        x_vals.append(e + bin_width)
        if data_mhh[ie] > 1.0 :
            data_mhh[ie] = 0.98 * data_mhh[ie]
        y_val = 2.4 * data_mhh[ie]
        y_vals.append(y_val)
        y_vals.append(y_val)
    #ax.fill(x_vals, y_vals, color = "grey")
    ax.fill_between(x_vals, y_vals, [0 for a in y_vals], color = "grey", alpha = 0.3, edgecolor = "k")

    maxy = 1.5
    ax.set_ylim([0,maxy])
    ax.set_xlim([x_lo, x_hi])
    ax.legend(loc = "lower right", ncol = 1,
        fontsize = 8, frameon = False)

    xticks = [x_lo, 400, 600, 800, 1000, 1200, 1400, 1600]
    ax.set_xticks(xticks)

    # unity line
    ax.plot([x_lo, x_hi], [1.0, 1.0], 'k--', lw = 1, alpha = 0.5)
    ax.tick_params(axis = "x", pad = 5)

    # labels
    size = 16
    text = r"\textit{\textbf{ATLAS}}"
    x_atlas = 0.04
    y_atlas = 0.96
    x_type_offset = 0.25
    y_type = 0.96
    
    x_lumi = 0.04
    y_lumi = 0.88
    
    x_region = 0.042
    y_region = 0.80
#172     opts = dict(transform = ax.transAxes)
#173     opts.update( dict(va = 'top', ha = 'left') )
#174     #ax.text(x_atlas, y_atlas, text, size = size, style = 'italic', weight = 'bold', **opts)
#175     ax.text(x_atlas, y_atlas, text, size = size, **opts)
#176
#177     what_kind = 'Simulation Preliminary'
#178     ax.text(x_atlas + 0.7 * x_type_offset, y_type, what_kind, size = size, **opts)
#179
#180     energy_text = r"$\sqrt{s}$ = 13 TeV"
#181     ax.text(x_atlas, 0.94 * y_type, energy_text, size = 0.80 * size, **opts)
#182
#183     #sel_text = r"Selection: at least 2 \textit{b}-tagged jets"
#184     sel_text = r"\textit{HH} $\rightarrow$ \textit{bbl}$\nu$\textit{l}$\nu$ pre-selection"
#185     ax.text(x_atlas, 0.88 * y_type, sel_text, size = 0.80 * size, **opts)
    
    opts = dict(transform = ax.transAxes)
    opts.update( dict(va = 'top', ha = 'left') )
    #ax.text(x_atlas, y_atlas, text, size = size, style = 'italic', weight = 'bold', **opts)
    ax.text(x_atlas, y_atlas, text, size = size, **opts)
    
    what_kind = 'Simulation'# Preliminary'
    ax.text(x_atlas + 0.65 * x_type_offset, y_type, what_kind, size = size, **opts)

    energy_text = r"$\sqrt{s}$ = 13 TeV"
    ax.text(x_atlas, 0.93 * y_atlas, energy_text, size = 0.83 * size, **opts)

    sel_text = r"\textit{HH} $\rightarrow$ \textit{bbl}$\nu$\textit{l}$\nu$ pre-selection"
    ax.text(x_atlas, 0.86 * y_atlas, sel_text, size = 0.83 * size, **opts)
#180     sel_text = r"Selection: at least 2 \textit{b}-tagged jets"
#181     #ax.text(x_atlas, 0.94 * y_type, sel_text, size = 0.7 * size, **opts)


    x_tick_loc = ax.get_xticks()
    x_tick_lab = ["%d" % int(x) for x in x_tick_loc]
    ax.set_xticks(x_tick_loc)
    ax.set_xticklabels(x_tick_lab)

    y_tick_loc = ax.get_yticks()
    y_tick_lab = ["%.1f" % x for x in y_tick_loc]
    ax.set_yticks(y_tick_loc)
    ax.set_yticklabels(y_tick_lab)

    ax.set_ylim([0,1.3])

    #save
    fig.show()
    #x = input()
    fig.savefig("mhh_sel_eff_nice_jul30.pdf", bbox_inches = "tight", dpi = 200)

def main() :
    make_plot()

if __name__ == "__main__" :
    main()

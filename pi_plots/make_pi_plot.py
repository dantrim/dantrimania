#!/bin/env python

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

data_dir = "./wwbb_pi_plot_data"


def get_plot_data(var_name) :

    path = "%s/pi_plot_data_%s.json" % (data_dir, var_name)
    with open(path, "r") as infile :
        jdata = json.load(infile)
    return jdata

def nice_process_names(p) :

    v = {}
    v["hh"] = r"\textit{HH}"# \\rightarrow b\\bar{b}\\ell\\nu\\ell\\nu$"
    v["top"] = "Top"
    v["zll"] = r"\textit{Z}-\textit{ll}"
    v["ztt"] = r"\textit{Z}-$\tau\tau$"
    return v[p]

def nice_var_names(p) :

    v = {}
    v["NN_d_hh"] = "$d_{HH}$"
    v["NN_d_top"] = "$d_{Top}$"
    v["NN_d_zsf"] = "$d_{Z-\ell\ell}$"
    v["NN_d_ztt"] = "$d_{Z-\\tau\\tau}$"
    v["NN_p_hh"] = "$p_{HH}$"
    v["NN_p_top"] = "$p_{Top}$"
    v["NN_p_zsf"] = "$p_{Z-\ell\ell}$"
    v["NN_p_ztt"] = "$p_{Z-\\tau\\tau}$"

    v["NN_d_hh"] = r"\textit{d}$_{\mbox{\small{\textit{HH}}}}$"
    v["NN_d_top"] = r"\textit{d}$_{\mbox{\small{\textit{Top}}}}$"
    v["NN_d_zsf"] = r"\textit{d}$_{\mbox{\small{\textit{Z-SF}}}}$"
    v["NN_d_ztt"] = r"\textit{d}$_{\mbox{\small{\textit{Z-}}}\tau\tau}$"
    v["NN_p_hh"] = r"\textit{p}$_{\mbox{\small{\textit{HH}}}}$"
    v["NN_p_top"] = r"\textit{p}$_{\mbox{\small{\textit{Top}}}}$"
    v["NN_p_zsf"] = r"\textit{p}$_{\mbox{\small{\textit{Z-ll}}}}$"
    v["NN_p_ztt"] = r"\textit{p}$_{\mbox{\small{\textit{Z-}}}\tau\tau}$"
    return v[p]

def get_bin_width(p) :

    v = {}
    v["NN_d_hh"] = 1
    v["NN_d_top"] = 1
    v["NN_d_zsf"] = 2
    v["NN_d_ztt"] = 1
    v["NN_p_hh"] = 0.1 
    v["NN_p_top"] = 0.1 
    v["NN_p_zsf"] = 0.1 
    v["NN_p_ztt"] = 0.1 
    return v[p]

def x_tick_skip(var) :

    v = {}
    v["NN_d_hh"]  = 4
    v["NN_d_top"] = 4 
    v["NN_d_zsf"] = 2 
    v["NN_d_ztt"] = 2 
    v["NN_p_hh"]  = 2 
    v["NN_p_top"] = 2 
    v["NN_p_zsf"] = 2 
    v["NN_p_ztt"] = 2 
    return v[var]

def process_color(p) :

    c = {}
    c["hh"] = "#000000"
    c["top"] = "#016fb9"
    c["zll"] = "#ff9505"
    c["ztt"] = "#ec4e20"
    return c[p]

def make_plot(var_name, args) :

    plot_data = get_plot_data(var_name)
    x_bounds = plot_data["x_bounds"]
    sample_data = plot_data["sample_data"]

    fig, ax = plt.subplots(1,1, figsize = (7,7))
    if args.logy :
        ax.set_yscale("log")
    ax.tick_params(axis = 'both', which = 'both', labelsize = 12, direction = 'in',
        labelleft = True, bottom = True, top = True, left = True, right = True)
    #ax.grid(color = 'k', which = 'both', linestyle = '-', lw = 1, alpha = 0.1)

    ax.tick_params(which = "major", length = 10, zorder = 1e9)
    ax.tick_params(which = "minor", length = 5, zorder = 1e9)
    
    ax.set_xlabel(nice_var_names(var_name), horizontalalignment = 'right', x = 1,
        fontsize = 15)
    ax.set_ylabel('a.u.', horizontalalignment = 'right', y = 1,
        fontsize = 15)

    n_bins = x_bounds[0]
    x_lo = x_bounds[1]
    x_hi = x_bounds[2]
    bin_width = get_bin_width(var_name)
    
    bin_edges = np.arange(x_lo - bin_width, x_hi + 2 * bin_width, bin_width)
    bin_centers = bin_edges + 0.5 * bin_width
    bin_centers = bin_centers[:-1]

    max_y = -99
    min_y = 0
    if args.logy :
        min_y = 1e-3
    sample_order = ["hh", "top", "zll", "ztt"]
    for isample, so in enumerate(sample_order) :
        for sample in sample_data :
            if sample != so : continue
            data = sample_data[sample]
            x_vals = []
            y_vals = []
            for ie, e in enumerate(bin_edges[1:-2]) :
            #for idata, d in enumerate(data) :
                x_vals.append(e)
                x_vals.append(e + bin_width)
                #x_vals.append(bin_centers[idata] - 0.5 * bin_width)
                #x_vals.append(bin_centers[idata] + 0.5 * bin_width)
                y_vals.append(data[ie])
                y_vals.append(data[ie])
                #y_vals.append(d)
                #y_vals.append(d)
            if so == "hh" :
                ax.plot(x_vals, y_vals, label = nice_process_names(so), color = process_color(so), zorder = 1e9)
            else :
                ax.plot(x_vals, y_vals, label = nice_process_names(so), color = process_color(so), zorder = 1e8)
            if max(y_vals) > max_y : max_y = max(y_vals)
    max_y = 1.3 * max_y
    if args.logy :
        max_y = 10
        #max_y = 1e2 * max_y




    ax.legend(loc = "upper right",frameon = False, fontsize = 16)

    # labels

    size = 18
    text = r"\textbf{\textit{ATLAS}}"
    x_atlas = 0.04
    y_atlas = 0.95
    x_type_offset = 0.25
    y_type = 0.95
    
    x_lumi = 0.04
    y_lumi = 0.88
    
    x_region = 0.042
    y_region = 0.80
     
    opts = dict(transform = ax.transAxes)
    opts.update( dict(va = 'top', ha = 'left') )
    #ax.text(x_atlas, y_atlas, text, size = size, style = 'italic', weight = 'bold', **opts)
    ax.text(x_atlas, y_atlas, text, size = size, **opts)
    
    what_kind = 'Simulation'# Preliminary'
    ax.text(x_atlas + 0.7 * x_type_offset, y_type, what_kind, size = size, **opts)

    energy_text = r"$\sqrt{s}$ = 13 TeV"
    ax.text(x_atlas, 0.94 * y_type, energy_text, size = 0.80 * size, **opts)

    #sel_text = r"Selection: at least 2 \textit{b}-tagged jets"
    sel_text = r"\textit{HH} $\rightarrow$ \textit{bbl}$\nu$\textit{l}$\nu$ pre-selection"
    ax.text(x_atlas, 0.88 * y_type, sel_text, size = 0.80 * size, **opts)


    x_tick_loc = ax.get_xticks()
    x_tick_labs = ["%s" % x for x in ax.get_xticks()]
    if "_p_" in var_name :
        x_tick_labs = ["%.1f" % x for x in x_tick_loc]
    ax.set_xticks(x_tick_loc)
    ax.set_xticklabels(x_tick_labs)

    y_tick_loc = ax.get_yticks()
    y_tick_labs = ["%.2f" % float(y) for y in ax.get_yticks()]
    if args.logy :
        y_tick_labs = ["{:.2e}".format(x) for x in ax.get_yticks()]
        y_tick_labs = [r"10$^{\mbox{%s}}$" % str(int(x.split("e")[-1].replace("+",""))) for x in y_tick_labs]
        ax.set_yticklabels(y_tick_labs)

    ax.set_yticks(y_tick_loc)
    ax.set_yticklabels(y_tick_labs)

    ax.set_xlim([x_lo, x_hi])
    #ax.set_ylim([min_y, max_y])
    #ax.set_xticks(["%.1f" % x for x in bin_edges[1:-1:x_tick_skip(var_name)]])
    ax.set_ylim([1e-3, max_y])

    # save
    #fig.savefig("test.pdf", bbox_inches = "tight", dpi = 200)
    fig.savefig("jul30_pi_plots/pi_plot_%s.pdf" % var_name, bbox_inches = "tight", dpi = 200)
    
    

def main() :

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--var", default = ["NN_d_hh"], nargs = "+",
        help = "Provide var to plot"
    )
    parser.add_argument("--logy", default = False, action = "store_true",
        help = "Make log y axis"
    )
    args = parser.parse_args()

    n_var = len(args.var)
    for iv, v in enumerate(args.var) :
        print("[%02d/%02d] %s" % (iv+1, n_var, v))
        make_plot(v, args)

    

    
if __name__ == "__main__" :
    main()

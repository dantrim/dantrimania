#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.utils.plib_utils as plib
import dantrimania.python.analysis.utility.plotting.m_py.scatterplot_matrix as scatterplot_matrix
from matplotlib.gridspec import GridSpec

plt = plib.import_pyplot()
import numpy as np
from matplotlib.colors import LogNorm
import matplotlib

def get_requested_variables(varlist) :

    out = []
    v = varlist.split(",")
    for var in v :
        if ":" in var :
            vc = var.split(":")
            if vc[0] not in out :
                out.append(vc[0])
            if vc[1] not in out :
                out.append(vc[1])
        else :
            if var not in out :
                out.append(var)

    return out

def get_requested_samples(samplelist) :
    out = []
    for s in samplelist.split(",") :
        out.append(s)
    return out

def get_variable_pairs(varlist) :
    out = []
    for s in varlist.split(",") :
        if ":" in s :
            s = s.split(":")
            pair = [s[0], s[1]]
            out.append(pair)
    return out

def make_heat_plot(sample, varpair, output_dir, region) :

    var_x = varpair[0]
    var_y = varpair[1]

    data_x = []
    data_y = []

    chain = sample.chain()
    for ich, ch in enumerate(chain) :
        data_x += list(ch[var_x])
        data_y += list(ch[var_y])


    fig = plt.figure(figsize = (8,8) )
    grid = GridSpec(100,100)
    pad = fig.add_subplot(grid[0:100,:])

    pad.set_title("%s vs %s for %s" % (var_x, var_y, sample.displayname) )
    pad.set_xlabel(var_x)
    pad.set_ylabel(var_y)

    bin_numbers = 60
    if sample.is_signal :
        bin_numbers = 30
    cmap = matplotlib.cm.jet
    cmap = matplotlib.cm.BuPu
    #cmap = matplotlib.cm.Blues
    h, x, y, p = pad.hist2d(data_x, data_y, cmap = cmap, bins = bin_numbers, cmin=1)#, norm=LogNorm())
    fig.colorbar(p)

    ##########################################
    # save name
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "dim2_%s_%s_v_%s_%s.pdf" % (region.name, var_x, var_y, sample.name)
    plt.savefig(save_name, bbox_tight = 'inches', dpi = 200)


def make_scatter_matrix(sample, varlist, region_to_plot, output_dir) :

    variables = varlist.split(",")
    data_dict = {}
    for v in variables :
        data_dict[v] = []

    chain = sample.chain()
    for ic, ch in enumerate(chain) :
        for il, variable in enumerate(variables) :
            data_dict[variable] += list(ch[variable])

    m = len(data_dict.keys())
    n = len(data_dict[variables[0]])
    data_array = np.ndarray(shape = (m,n), dtype=float)
    labels = []
    for ivar, var in enumerate(variables) :
        data_array[ivar] = data_dict[var]
        labels.append(var)

    fig, axes = plt.subplots(nrows=len(variables), ncols=len(variables))
    for iv, ivar in enumerate(variables) :
        for jv, jvar in enumerate(variables) :
            if jv > iv : continue
            data_x = data_dict[ivar]
            data_y = data_dict[jvar]
            if iv < (len(variables) - 1) :
                axes[iv][jv].set_xticklabels([])
            if jv > 0 :
                axes[iv][jv].set_yticklabels([])
            h, x, y, p = axes[iv][jv].hist2d(data_x, data_y, cmap = 'jet', bins = 60, cmin = 1)
            

    #import pandas as pd
    #from pandas.plotting import scatter_matrix
    #df = pd.DataFrame(data_array.T, columns = labels)
    #scatter_matrix(df, alpha=0.2, figsize=(8,8), diagonal='kde')
    #import seaborn as sns
    
    #print data_array.shape
    #sys.exit()
    #fig, axes = scatterplot_matrix.scatter_plot_matrix(data_array, labels = labels)
    #print fig

    print "saving figure"
    plt.savefig("test_scatter_matrix.png", bbox_tight='inches')#, dpi=200)
             
    

    


def main() :
    parser = OptionParser()
    parser.add_option("-c", "--config", default="", help="Configuration file for plotting")
    parser.add_option("-r", "--region", default="", help="Provide a region selection")
    parser.add_option("-o", "--output", default="./", help="Provide an output directory for plots (will make it if it does not exist)")
    parser.add_option("-s", "--sample", default="", help="Provide the name(s) of a background sample to make the plots for")
    parser.add_option("-v", "--var-list", default="", help="Provide a list of variables to plot")
    parser.add_option("--cache-dir", default="./sample_cache", help="Directory to place/look for the cached samples")
    (options, args) = parser.parse_args()
    config = options.config
    cache_dir = options.cache_dir
    region = options.region
    output_dir = options.output
    samplelist = options.sample
    varlist = options.var_list

    if not utils.file_exists(config) :
        sys.exit()

    global loaded_samples
    global loaded_regions
    global selected_region
    global loaded_plots
    selected_region = region
    loaded_samples = []
    loaded_regions = []
    loaded_plots = []
    execfile(config, globals(), locals())

    if len(loaded_samples) == 0 :
        print "ERROR No loaded samples found in configuration"
        sys.exit()

    # check region
    if not region_utils.regions_unique(loaded_regions) :
        print "ERROR Loaded regions are not unique, here are the counts:"
        for rname, count in region_utils.region_counts(loaded_regions).iteritems() :
            print " > %s : %d" % (rname, count)
        sys.exit()

    if not region_utils.has_region(loaded_regions, selected_region) :
        print "ERROR Requested region (=%s) not found in loaded regions:" % ( selected_region )
        for r in loaded_regions :
            print str(r)
        sys.exit()

    region_to_plot = None
    for r in loaded_regions :
        if r.name == selected_region :
            region_to_plot = r
            break

    requested_variables = get_requested_variables(varlist)
    requested_variables += sample_utils.get_required_variables(loaded_plots, region_to_plot)

    requested_samples = get_requested_samples(samplelist)
    samples_all_found = True
    loaded_sample_names = [s.name for s in loaded_samples]
    for rs in requested_samples :
        if rs not in loaded_sample_names :
            samples_all_found = False
            print " > Did not find requested sample %s in loaded sample list" % rs
    if not samples_all_found :
        sys.exit()
    requested_samples = [s for s in loaded_samples if s.name in requested_samples]

    # cache
    cacher = sample_cacher.SampleCacher(cache_dir)
    cacher.samples = requested_samples
    cacher.region = region_to_plot
    cacher.fields = requested_variables
    print str(cacher)
    cacher.cache()
    
    if ":" in varlist :
        varpairs = get_variable_pairs(varlist)
        for vp in varpairs :
            for sample in requested_samples :
                make_heat_plot(sample, vp, output_dir, region_to_plot)
    else :
        for sample in requested_samples :
            make_scatter_matrix(sample, varlist, region_to_plot, output_dir)
    

#_________________________________________________________________
if __name__ == "__main__" :
    main()

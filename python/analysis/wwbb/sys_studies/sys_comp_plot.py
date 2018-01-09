#!/usr/env/python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.samples.region_utils as region_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
from math import sqrt

import numpy as np

def get_variables_from_cut(cutstr) :

    operators = ["==", ">=", "<=", ">", "<", "!=", "*", "-"]
    logics = ["&&", "||", ")", "(", "abs"]
    vars_only = cutstr
    for op in operators :
        vars_only = vars_only.replace(op, " ")
    for log in logics :
        vars_only = vars_only.replace(log, " ")
    vars_only = vars_only.split()
    out = []
    for v in vars_only :
        if v not in out and not v.isdigit() :
            try :
                flv = float(v)
            except :
                out.append(v)

    return out

def get_required_variables(variables, region) :

    out = []

    for v in variables :
        out.append(v)

    cut_vars = get_variables_from_cut(region.tcut)
    for cv in cut_vars :
        if cv not in out :
            out.append(cv)

    out.append("eventweight")
    return out

def get_samples(nominal_file = "", up_file = "", down_file = "") :

    if nominal_file == "" :
        print "get_samples    provided nominal file is empty"
        sys.exit()

    if up_file == "" :
        print "get_samples    provided up file is empty"
        sys.exit()

    do_down = True
    if down_file == "" :
        print "get_samples    treating as one-sided systematic"
        do_down = False

    samples = []

    nom = sample.Sample("nominal", "Nominal")
    nom.scalefactor = 36.1
    nom.load_file(nominal_file)
    samples.append(nom)

    up = sample.Sample("up", "$+1 \\sigma$")
    up.scalefactor = 36.1
    up.load_file(up_file)
    samples.append(up)

    if do_down :
        dn = sample.Sample("dn", "$-1 \\sigma$")
        dn.scalefactor = 36.1
        dn.load_file(down_file)
        samples.append(dn)

    return samples

def make_sys_plot(plot, region, samples, output_dir, symmetrize) :

    print 50 * "-"
    print " plotting %s" % plot.vartoplot

    xlow = plot.xlow
    xhigh = plot.xhigh
    binwidth = plot.binwidth
    nbins = np.arange(xlow, xhigh + binwidth, binwidth)

    nom_histo = []
    nom_weights = []

    up_histo = []
    up_weights = []

    down_histo = []
    down_weights = []

    for isample, sample in enumerate(samples) :

        histo = []
        weights = []
        chain = sample.chain()

        for ic, c in enumerate(chain) :
            # data
            data = c[plot.vartoplot]
            lumis = np.ones(len(data))
            lumis[:] = sample.scalefactor
            w = lumis * c['eventweight']
            weights += list(w)

            if plot.absvalue :
                histo += list(np.absolute(data))
            else :
                histo += list(data)


        histo = np.clip(histo, nbins[0], nbins[-1])

        if isample == 0 :
            nom_histo = histo
            nom_weights = weights
        elif isample == 1 :
            up_histo = histo
            up_weights = weights
        elif isample == 2 :
            down_histo = histo
            down_weights = weights


    # pads

    upper = plot.upper
    lower = plot.lower
#    lower.set_ylim(0.7, 1.3)

    # styles
    linewidth = 1.5
    hatch = ""
    color_up = "blue"
    color_dn = "red"
    edge_color_up = "blue"
    edge_color_dn = "red"
    alpha = 0.5

    # plot nominal
    h_nom, range_nom = np.histogram(nom_histo, bins = nbins, weights = nom_weights)
    xvals_nom = []
    yvals_nom = []
    for xval in h_nom :
        xvals_nom.append(xval)
        xvals_nom.append(xval)
    for i in xrange(len(nbins)-1) :
        yvals_nom.append(nbins[i])
        yvals_nom.append(nbins[i] + binwidth)
    tmp = xvals_nom
    xvals_nom = yvals_nom
    yvals_nom = tmp
    upper.step(xvals_nom, yvals_nom, "k-", lw=linewidth)

    # plot upper variation
    h_up, range_up = np.histogram(up_histo, bins = nbins, weights = up_weights)
    xvals_up = [] 
    yvals_up = []
    for xval in h_up :
        xvals_up.append(xval)
        xvals_up.append(xval)
    for i in xrange(len(nbins)-1) :
        yvals_up.append(nbins[i])
        yvals_up.append(nbins[i] + binwidth)
    tmp = xvals_up
    xvals_up = yvals_up
    yvals_up = tmp

    # plot down variation
    xvals_dn = []
    yvals_dn = []
    if len(samples) == 3 :
        h_dn, range_dn = np.histogram(down_histo, bins = nbins, weights = down_weights)
        for xval in h_dn :
            xvals_dn.append(xval)
            xvals_dn.append(xval)
        for i in xrange(len(nbins)-1) :
            yvals_dn.append(nbins[i])
            yvals_dn.append(nbins[i] + binwidth)
        tmp = xvals_dn
        xvals_dn = yvals_dn
        yvals_dn = tmp


    if symmetrize :
        new_yvals_up = []
        new_yvals_dn = []
        for i in xrange(len(yvals_nom)) :
            nom_val = yvals_nom[i]
            ehigh = yvals_up[i]
            elow = yvals_nom[i]
            if len(samples) == 3 :
                elow = yvals_dn[i]
            delta_ehigh = ehigh - nom_val
            delta_elow = nom_val - elow
            if nom_val == 0.0 :
                rel_delta_high = nom_val
                rel_delta_low = nom_val
            else :
                rel_delta_high = abs( float(delta_ehigh) / float(nom_val) )
                rel_delta_low = abs( float(delta_elow) / float(nom_val) )
            rel_delta_sym = 0.5 * (rel_delta_high + rel_delta_low)


            new_yvals_up.append( yvals_nom[i] + rel_delta_sym * yvals_nom[i] )
            new_yvals_dn.append( yvals_nom[i] - rel_delta_sym * yvals_nom[i] )
            #yvals_up = [(y + rel_delta_sym * y) for y in yvals_nom]
            #yvals_dn = [(y - rel_delta_sym * y) for y in yvals_nom]
        yvals_up = new_yvals_up
        yvals_dn = new_yvals_dn

    #if not symmetrize :
    upper.fill_between(xvals_up, yvals_nom, yvals_up, lw = linewidth, hatch = hatch,
                alpha = alpha, facecolor = color_up, edgecolor = edge_color_up) 
    upper.fill_between(xvals_up, yvals_nom, yvals_up, lw = linewidth, hatch = hatch,
                alpha = 1.0, facecolor = "None", edgecolor = edge_color_up) 
    

    if len(samples) == 3 :
        #if not symmetrize :
        upper.fill_between(xvals_dn, yvals_nom, yvals_dn, lw = linewidth, hatch = hatch,
               alpha = alpha, facecolor = color_dn, edgecolor = edge_color_dn) 
        upper.fill_between(xvals_dn, yvals_nom, yvals_dn, lw = linewidth, hatch = hatch,
                    alpha = 1.0, facecolor = "None", edgecolor = edge_color_dn) 
           
        
    # ratio up variation
    ratio_up = []
    for i in xrange(len(yvals_up)) :
        nom_val = yvals_nom[i]
        up_val = yvals_up[i]
        if nom_val != 0.0 :
            ratio_up.append( float(up_val) / float(nom_val) )
        else :
            ratio_up.append(1.0)
    lower.step(xvals_nom, ratio_up, color_up, lw = linewidth)

    if len(samples) == 3 :
        # ratio down variation
        ratio_down = []
        for i in xrange(len(yvals_dn)) :
            nom_val = yvals_nom[i]
            dn_val = yvals_dn[i]
            if nom_val != 0.0 :
                ratio_down.append( float(dn_val) / float(nom_val) )
            else :
                ratio_down.append(1.0)
        lower.step(xvals_nom, ratio_down, color_dn, lw = linewidth)


    ######################################################
    # save
    utils.mkdir_p(output_dir)
    save_name = output_dir + "/sys_comp_%s_%s.pdf" % ( region.name, plot.vartoplot )
    print " >>> saving plot to : %s" % os.path.abspath(save_name)
    plot.fig.savefig(save_name, bbox_inches = "tight", dpi = 200)


    


def main() :

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default = "./", help = "Set output directory for plots")
    parser.add_option("-n", "--nom", default = "", help = "Provide input file for NOMINAL sample")
    parser.add_option("-u", "--up", default = "", help = "Provide input file for UP sample")
    parser.add_option("-d", "--dn", default = "", help = "Provide input file for DN sample")
    parser.add_option("--logy", default = False, action = "store_true", help = "Set y-axis to log scale")
    parser.add_option("--sym", default = False, action = "store_true", help = "Symmetrize the y errors")
    parser.add_option("-v", "--var", default = "", help = "Request a specific variable to plot")
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    do_logy = options.logy
    nom_file = options.nom
    up_file = options.up
    dn_file = options.dn
    request_var = options.var
    sym = options.sym

    samples = get_samples(nom_file, up_file, dn_file) # [NOM, UP, DN] if 2-sided, [NOM, UP] if 1-sided

    # region
    reg = region.Region("wwbb", "WW$bb$")
    #reg.tcut = "l0_pt>20 && l1_pt>10 && nBJets==2 && mbb>100 && mbb<140 && mt2_llbb>100 && mt2_llbb<140 && dRll<0.9"
    reg.tcut = "l0_pt>20 && l1_pt>10 && nBJets>=2"

    variables = {}
    variables["met"] = [30, 0, 300]
    variables["mll"] = [20, 0, 400]
    variables["mbb"] = [20, 0, 400]
    variables["bj0_pt"] = [20, 20, 400]
    variables["bj1_pt"] = [10, 20, 200]
    variables["j0_pt"] = [20, 20, 400]
    variables["j1_pt"] = [10, 20, 200]
    variables["sj0_pt"] = [20, 20, 400]
    variables["sj1_pt"] = [10, 20, 200]
    variables["nBJets"] = [1, 4, 10]
    variables["nJets"] = [1, 0, 10]
    variables["nSJets"] = [1, 0, 10]
    variables["HT2Ratio"] = [0.2, 0, 1.0]
    variables["HT2"] = [50, 0, 750]
    variables["MT_1_scaled"] = [50, 0, 600]
    variables["dRll"] = [0.5, 0, 5]
    variables["mt2_bb"] = [25, 0, 300]

    if request_var != "" :
        if request_var not in variables.keys() :
            print "ERROR requested variable %s not in initialized varialbes list %s" % (request_var, variables.keys())
            sys.exit()
        tmp_var = {}
        tmp_var[request_var] = variables[request_var]
        variables = tmp_var

    nice_names = {}
    nice_names["mll"] = ["$m_{\ell \ell}$ [GeV]", "GeV"]
    nice_names["mbb"] = ["$m_{bb}$ [GeV]", "GeV"]

    # cache
    cacher = sample_cacher.SampleCacher("./cache_np3")
    cacher.samples = samples
    cacher.region = reg
    required_variables = get_required_variables(variables.keys(), reg)
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for var, bounds in variables.iteritems() :
        p = hist1d.RatioCanvas(logy = do_logy)
        if "abs(" in var :
            var = var.replace("abs(","").replace(")","")
            p.absvalue = True
        p.vartoplot = var
        p.bounds = bounds
        name = var.replace("[","").replace("]","").replace("(","").replace(")","")
        p.name = name
        y_label_unit = ""
        if var in nice_names :
            if len(nice_names[var]) == 2 :
                y_label_unit = nice_names[var][1]
        y_label_unit = str(bounds[0]) + " " + y_label_unit
        x_label = var
        y_label = "Events / %s" % y_label_unit
        if var in nice_names :
            x_label = nice_names[var][0]
        p.labels = [x_label, y_label]
        p.logy = do_logy
        p.build_ratio()

        make_sys_plot(p, reg, samples, output_dir, sym)
        
    



#_______________________________________
if __name__ == "__main__" :
    main()

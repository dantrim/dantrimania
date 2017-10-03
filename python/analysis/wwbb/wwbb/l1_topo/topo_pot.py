#!/usr/bin/env python

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
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()

import numpy as np

def get_samples() :

    filedir = "/data/uclhc/uci/user/dantrim/TruthAnalysis/dihiggs_ntuples/h5/"

    samples = []

    hh = sample.Sample("hh", "SM $hh$")
    hh.scalefactor = 1
    hh.is_signal = True
    hh.load_file(filedir + "wwbb_truth_390532.h5")
    samples.append(hh)
    

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

def main() :
    print " * l1topo pot * "

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default="./", help = "Set output directory for plots")
    parser.add_option("-v", "--var", default = "", help = "Request a specific variable to plot")
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    select_var = options.var

    samples = get_samples()

    reg = region.Region("wwbb", "WW$bb$")
    reg.tcut = "mll>20 && n_bjets==2 && bj0_pt>20 && bj1_pt>20"

    variables = {}
    variables["l0_pt"] = [10, 0, 500]
    variables["l1_pt"] = [10, 0, 300]

    if select_var != "" :
        if select_var not in variables :
            print "ERROR Requested variable %s not initialized" % select_var
            sys.exit()
        tmp_var = {}
        tmp_var[select_var] = variables[select_var]
        variables = tmp_var

    # cache
    cacher = sample_cacher.SampleCacher("./cache")
    cacher.samples = samples
    cacher.region = reg
    required_variables = get_required_variables(variables.keys(), reg) 
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache("truth")

    for var, bounds in variables.iteritems() :
        p = hist1d.

    
    

    

#______________________________________________________
if __name__ == "__main__" :
    main()

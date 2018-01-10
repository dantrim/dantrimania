#!/usr/bin/env/python
import sys

import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
import numpy as np

def get_masses(infile) :
    masses = []
    lines = open(infile).readlines()
    for line in lines :
        if "#" in line : continue
        x = line.strip()
        x = x.split()
        mass = x[0]
        masses.append(int(mass))
    return masses

def get_s95(infile, masses) :

    out = {}

    lines = open(infile).readlines()
    for m in masses :
        for line in lines :
            if "#" in line : continue 
            x = line.strip()
            x = x.split()
            if int(x[0]) != m : continue
            mass = m
            vis_xsec = float(x[1])
            s95 = float(x[2])
            s95_p1 = float(x[3])
            s95_m1 = float(x[4])
            out[m] = [vis_xsec, s95, s95_p1, s95_m1]
    return out

def get_acceptance(infile, masses) :

    lines = open(infile).readlines()
    out = {}
    for m in masses :
        for line in lines :
            if "#" in line : continue
            x = line.strip()
            x = x.split()
            if int(x[0]) != m : continue
            acc = float(x[1])
            num = float(x[5])
            out[m] = [acc, num]
    return out

def get_reco(infile, masses) :

    lines = open(infile).readlines()
    out = {}
    for line in lines :
        for m in masses :
            if "#" in line : continue
            x = line.strip()
            x = x.split()
            if int(x[0]) != m : continue
            reco_yield = float(x[1])
            reco_yield_err = float(x[2])
            out[m] = [reco_yield, reco_yield_err]
    return out

def get_limit(s95list, acc_list, reco_list) :

    vis_xsec = s95list[0]
    truth_pass = acc_list[1]
    acceptance = acc_list[0]
    reco_yield = reco_list[0]

    # out[m] = [vis_xsec, s95, s95_p1, s95_m1]
    print "DOING DN"
    vis_xsec = (float(s95list[1]) - float(s95list[3])) / 36.06
    efficiency = -1.0
    if float(truth_pass) > 0.0 :
        efficiency = float(reco_yield) / float(truth_pass)
    numerator = vis_xsec * ( 1.0 / 1000.0) # convert from [fb] to [pb]
    denominator = efficiency * acceptance

    if float(denominator) > 0.0 :
        return ( float(numerator) / float(denominator))
    else :
        return -1.0

def main() :

    acceptance_file = "hh_acceptance_tables_36.1.txt"
    reco_yield_file = "jan10_wwbb_reco_counts_sig.txt"
    s95_file = "sig95_exp_limits_36.1.txt"

    masses = get_masses(s95_file)

    # out[m] = [vis_xsec, s95, s95_p1, s95_m1]
    s95_dict = get_s95(s95_file, masses)

    # { mass : acceptance }
    acc_dict = get_acceptance(acceptance_file, masses)

    # { mass : [yield, yield_err] }
    reco_dict = get_reco(reco_yield_file, masses)

    xvals = masses

    xsec_limits = {}
    for m in masses :
        limit = get_limit(s95_dict[m], acc_dict[m], reco_dict[m])
        xsec_limits[m] = limit

    yvals = []
    for m in masses :
        yvals.append(xsec_limits[m])

    print xvals
    print yvals

    


if __name__ == "__main__" :
    main()

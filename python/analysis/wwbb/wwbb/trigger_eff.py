#!/usr/bin/env python

from optparse import OptionParser
import os
import sys
from math import sqrt

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.samples.sample_utils as sample_utils
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.samples.sample_cacher as sample_cacher
import dantrimania.python.analysis.utility.utils.plib_utils as plib
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
plt = plib.import_pyplot()

import numpy as np
import matplotlib

def load_samples() :

    out = []

    filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
    h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/c_aug16/mc/h5/" 

    ttbar = sample.Sample("ttbar", "$t\\bar{t}$")
    ttbar.scalefactor = 1
    ttbar.load(filelist_dir + "ttbar", h5_dir_mc)
    #out.append(ttbar)

    hhSM = sample.Sample("hhSM", "$hh$ SM")
    hhSM.is_signal = True
    hhSM.scalefactor = 1
    hhSM.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '342053')
    out.append(hhSM)

    return out

def trigger_variables() :

    out = []
    # dilepton
    out.append('trig_pass2015')
    out.append('trig_pass2016update')
    # single 15
    out.append('trig_e60_lhmedium')
    out.append('trig_e120_lhloose')
    out.append('trig_mu20_iloose_L1MU15')
    out.append('trig_mu40')
    out.append('trig_mu60_0eta105_msonly')
    # single 16
    out.append('trig_e60_lhmedium_nod0')
    out.append('trig_e140_lhloose_nod0')
    out.append('trig_mu26_ivarmedium')
    out.append('trig_mu50')

    return out
    
def get_counts(sample, idx_sel_str) :

    chunks = sample.chain()
    count = 0.0
    sumw2 = 0.0
    for ic, chain in enumerate(chunks) :
        set_idx = "indices = np.array( %s )" % idx_sel_str
        exec(set_idx)
        ds = chain[indices] # apply the selection to the dataset

        w = ds['eventweight']
        h, _ = np.histogram(ds['l0_pt'], weights = w)
        hsw, _ = np.histogram(ds['l0_pt'], weights = w**2)
        count += sum(h)
        sumw2 += sum(hsw)

        if not sample.is_signal :
            if count > 1000 :
                break

    return count, sqrt(sumw2)
        

def calculate_efficiency(lead_pt_cut, sub_lead_pt_cut, trig_type, sample, initial_region, varlist) :

    print "[%s,%s]" % (lead_pt_cut, sub_lead_pt_cut)
    base_selection = "%s && l0_pt>%s && l1_pt>%s" % (initial_region.tcut, lead_pt_cut, sub_lead_pt_cut)
    #base_selection = "%s" % initial_region.tcut
    #print "initial_region tcut = %s" % base_selection

    trig_dilepton_2015 = "trig_pass2015==1"
    trig_dilepton_2016 = "trig_pass2016update==1"

    trig_single_2015 = "(trig_e60_lhmedium==1 || trig_mu20_iloose_L1MU15)"
    trig_single_2016 = "(trig_e60_lhmedium_nod0==1 || trig_mu26_ivarmedium==1)"

    trigger_selection = ""
    if trig_type == 'dilepton' :
        trigger_selection = "( year==2015 && %s ) || ( year==2016 && %s )" % ( trig_dilepton_2015, trig_dilepton_2016 )
    elif trig_type == 'dilepton_or_single' :
        t15 = "( year==2015 && ( %s || %s ) )" % ( trig_dilepton_2015, trig_single_2015 )
        t16 = "( year==2016 && ( %s || %s ) )" % ( trig_dilepton_2016, trig_single_2016 )
        trigger_selection = "( %s || %s )" % ( t15, t16 )

    initial_sel_idx_str = sample_utils.index_selection_string(base_selection, 'chain', varlist)

    initial_counts, initial_error = get_counts(sample, initial_sel_idx_str)

    selection_with_trigger = "%s && ( %s )" % ( base_selection, trigger_selection )
    trigger_sel_idx_str = sample_utils.index_selection_string(selection_with_trigger, 'chain', varlist)
    trigger_sel_idx_str = trigger_sel_idx_str.replace("']_nod0", "_nod0']")
    trigger_counts, trigger_error = get_counts(sample, trigger_sel_idx_str)

    eff = float(trigger_counts) / float(initial_counts)
    return eff * 100

def make_plot(sample, region, type, data, minz = 0, lead_pts = [], sub_pts= [], output_dir = "./") :

    
    fig, ax = plt.subplots()

    masked_array = np.ma.masked_where(data.T == 0, data.T)
    cmap = matplotlib.cm.PuRd
    if sample.is_signal :
        cmap = matplotlib.cm.BuPu
    im = ax.pcolor(masked_array, cmap = cmap)
    fig.colorbar(im)

    xlabels = [int(p) for p in lead_pts]
    ylabels = [int(p) for p in sub_pts]
    xlabels.append(xlabels[-1] + 5)
    ylabels.append(ylabels[-1] + 5)
    xlabels = [str(l) for l in xlabels]
    ylabels = [str(l) for l in ylabels]
    ax.xaxis.set(ticks=np.arange(0, len(lead_pts)+1), ticklabels = xlabels) 
    ax.yaxis.set(ticks=np.arange(0, len(sub_pts)+1), ticklabels = ylabels)

    for irow, row in enumerate(data) :
        for jcol, col in enumerate(row) :
            if col > 0 :
                ax.text(irow + 0.35 ,jcol + 0.4 , "%.2f" % col, fontsize=4)

    ###############################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "trig_eff_vPT_%s_%s_%s.pdf" % ( type, sample.name, region.name )

    print " >>> Saving plot to : %s" % (os.path.abspath(save_name) ) 
    plt.savefig(save_name, bbox_tight = 'inches')

def make_trigger_eff(sample, initial_region, output_dir, varlist) :

    lead_pt_cuts = [str(pt) for pt in range(25,80,5)]
    sub_lead_pt_cuts = [str(pt) for pt in range(20,80,5)]

    efficiency_map = {}
    minz = {}
    minz['dilepton'] = 99999
    minz['dilepton_or_single'] = 999999
    for ilpt, lpt in enumerate(lead_pt_cuts) :
        for ispt, spt in enumerate(sub_lead_pt_cuts) :
            key = "%s_%s" % ( lpt, spt )
            efficiency_map[key] = {}
            for trig_type in ['dilepton', 'dilepton_or_single'] :
                if spt >= lpt :
                    efficiency_map[key][trig_type] = 0
                else :
                    efficiency_map[key][trig_type] = calculate_efficiency(lpt, spt, trig_type, sample, initial_region, varlist)

    bounds = [ min(lead_pt_cuts), max(lead_pt_cuts),  min(sub_lead_pt_cuts), max(sub_lead_pt_cuts) ]
    bounds = [ float(f) for f in bounds ]
    print "bounds ", bounds
    for trig_type in ['dilepton'] : #, 'dilepton_or_single'] :
        data_array = np.ndarray(shape = ( len(lead_pt_cuts), len(sub_lead_pt_cuts) ) , dtype = float)
        for pt in efficiency_map :
            lpt = pt.split("_")[0]
            spt = pt.split("_")[1]
            l_idx = lead_pt_cuts.index(lpt)
            s_idx = sub_lead_pt_cuts.index(spt)
            eff = efficiency_map["%s_%s" % ( lpt, spt )][trig_type]
            eff_or = efficiency_map["%s_%s" % ( lpt, spt)]['dilepton_or_single']
            if eff < minz[trig_type] : minz[trig_type] = eff
            if eff == 0 :
                data_array[l_idx][s_idx] = 0
            else :
                data_array[l_idx][s_idx] = float(eff_or) /  float(eff)
        make_plot(sample, initial_region, trig_type, data_array, minz[trig_type], lead_pt_cuts, sub_lead_pt_cuts, output_dir)

def calculate_efficiency_a_b_pt(selection_den, selection_num, sample, varlist) :

    den_idx_str = sample_utils.index_selection_string(selection_den, 'chain', varlist)
    den_idx_str = den_idx_str.replace("']_nod0", "_nod0']")
    num_idx_str = sample_utils.index_selection_string(selection_num, 'chain', varlist)
    num_idx_str = num_idx_str.replace("']_nod0", "_nod0']")

    den_counts, den_error = get_counts(sample, den_idx_str)
    num_counts, num_error = get_counts(sample, num_idx_str)

    print "den_counts = %.2f   num_counts = %.2f" % (den_counts, num_counts)

    error_ratio = num_counts / den_counts
    error_ratio = error_ratio * sqrt( (num_error / num_counts) ** 2  + (den_error / den_counts) ** 2 )

    eff = float(num_counts) / float(den_counts)
    return eff * 100, error_ratio * 100

def make_di_give_si_eff(sample, region, output_dir, varlist) :

    # calculate the efficiency to pass the dilepton triggers after requiring the
    # single lepton triggers with lead pT cut > X

    lead_pt_cuts = [str(pt) for pt in range(25, 100, 5)]

    trig_single_2015 = "(trig_e60_lhmedium==1 || trig_mu20_iloose_L1MU15==1)"
    trig_single_2016 = "(trig_e60_lhmedium_nod0==1 || trig_mu26_ivarmedium==1)"
    single_lepton_triggers = "( %s || %s )" % (trig_single_2015, trig_single_2016)

    trig_dilepton_2015 = "trig_pass2015==1"
    trig_dilepton_2016 = "trig_pass2016update==1"
    dilepton_triggers =  "( year==2015 && %s ) || ( year==2016 && %s )" % ( trig_dilepton_2015, trig_dilepton_2016 )

    t15 = "( year==2015 && ( %s || %s ) )" % ( trig_dilepton_2015, trig_single_2015 )
    t16 = "( year==2016 && ( %s || %s ) )" % ( trig_dilepton_2016, trig_single_2016 )
    dil_and_single_triggers = "( %s || %s )" % ( t15, t16 ) 


    efficiency_map = {}
    error_map = {}
    for ilpt, lpt in enumerate(lead_pt_cuts) :
        #denominator = "l0_pt > %s && ( %s )" % (lpt, single_lepton_triggers)
        denominator = "l0_pt > %s && ( %s )" % (lpt, dilepton_triggers) #single_lepton_triggers)
        numerator = "l0_pt > %s && ( %s )" % ( lpt, dil_and_single_triggers )
        efficiency_map[lpt], error_map[lpt] = calculate_efficiency_a_b_pt(denominator, numerator, sample, varlist)

    fig, ax = plt.subplots()
    x = []
    y  = []
    e = []
    for pt, eff in efficiency_map.iteritems() :
        x.append(float(pt))
        y.append(eff)
        e.append(error_map[pt])
    ax.plot(x,y,'bo')
    #ax.errorbar(x,y,e, fmt='o', color='b')
    ax.set_title("Efficiency (Single OR Dilepton) / (Dilepton) $ee$ channel")
    ax.set_xlabel("Lead lepton $p_{T}$ GeV", ha = 'right', x = 1.0)
    ax.set_ylabel("$\\epsilon$(Dilepton $\\cup$ Single | Dilepton) %", ha = 'right', y = 1.0)
    #ax.set_ylabel("$\\epsilon$(Single | Dilepton) %", ha = 'right', y = 1.0)
    ax.set_ylim(0.9*min(y), 130)
    xl = np.linspace(min(x), max(x), 20)
    yl = np.ones(len(xl)) * 100.
    ax.plot(xl,yl, 'k--', lw = 1)
    
    ax.text(0.07,0.9, sample.displayname, transform =ax.transAxes, ha='left', weight='bold')

    ######################################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "trig_eff_di_giv_si_vPT_%s_%s_eeOR.pdf" % ( sample.name, region.name )
    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    plt.savefig(save_name, bbox_tight = 'inches')
    

def main() :

    parser = OptionParser()
    parser.add_option("-o", "--output", default="./", help="Output directory for plots")
    parser.add_option("--di-give-si", action="store_true", default=False, help="Make the eff(Dilepton | Single) plots")
    (options, args) = parser.parse_args()
    output_dir = options.output
    di_give_si = options.di_give_si

    samples = load_samples()

    r = region.Region("wwbbpre_trig", "WW$bb$-pre (pre-trigger)")
    r.tcut = "mll>20 && nElectrons==2"
    #r.tcut = "nBJets>=2 && mll>20"
    required_variables = ['nBJets', 'mll', 'nElectrons', 'nMuons', 'l0_pt', 'l1_pt', 'year', 'eventweight']

    required_variables += trigger_variables()

    cache_dir = "./selection/"
    cacher = sample_cacher.SampleCacher(cache_dir)
    cacher.samples = samples
    cacher.region = r
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for sample in samples :
        if not di_give_si :
            make_trigger_eff(sample, r, output_dir, required_variables)
        elif di_give_si :
            make_di_give_si_eff(sample, r, output_dir, required_variables)

    

    



#___________________________________________________
if __name__ == "__main__" :
    main()

#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

from math import sqrt

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
    hh.color = '#fa0f00'
    hh.load_file(filedir + "wwbb_truth_342053.h5")
    samples.append(hh)

    x600 = sample.Sample("x600", "X 600 GeV")
    x600.scalefactor = 1
    x600.is_signal = True
    x600.color = '#ffb900'
    x600.load_file(filedir + "wwbb_truth_343772.h5")
    samples.append(x600)

    x800 = sample.Sample("x800", "X 800 GeV")
    x800.scalefactor = 1
    x800.is_signal = True
    x800.color = '#0cf4ea' 
    x800.load_file(filedir + "wwbb_truth_343775.h5")
    samples.append(x800)

    x1000 = sample.Sample("x1000", "X 1000 GeV")
    x1000.scalefactor = 1
    x1000.is_signal = True
    x1000.color = '#ff5900'
    x1000.load_file(filedir + "wwbb_truth_343777.h5")
    samples.append(x1000)

    tt = sample.Sample("ttbar", "$t\\bar{t}$")
    tt.scalefactor = 1
    tt.is_signal = False
    tt.color = '#1066bd' 
    tt.load_file(filedir + "wwbb_truth_410009.h5")
    samples.append(tt)

    return samples
    

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
        if "abs(" in v :
            v = v.replace("abs(","").replace(")","")
        out.append(v)

    cut_vars = get_variables_from_cut(region.tcut)
    for cv in cut_vars :
        if cv not in out :
            out.append(cv)

    out.append("eventweight")
    return out

def find_index(value, edges) :
    for idx, val in enumerate(edges) :
        if val == value :
            return idx

def draw_histo(pad, sample, filled = False, variable = "", bins = None, absval = False, scaling = "1.0") :

    chain = sample.chain()

    histogram = []
    sumw2_histogram = []

    weights = []
    weights2 = []

    scaling = float(scaling)

    for ic, ch in enumerate(chain) :
        lumi = np.ones(len(ch['eventweight']))
        lumi[:] = sample.scalefactor
        ch_weights = lumi * ch['eventweight']
        ch_weights = ch_weights * scaling
        weights += list(ch_weights)

        

        # calculate sumw2
        ch_weights2 = lumi * ch['eventweight']
        ch_weights2 = ch_weights2 * scaling
        ch_weights2 = ch_weights2 ** 2
        weights2 += list(ch_weights2)

        data = ch[variable]
        if absval :
            data = np.absolute(data)

        histogram += list(data)
        sumw2_histogram += list(data)

    bin_content, bin_edges = np.histogram(histogram, bins = bins,
                                weights = weights)#,normed = 1)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    total = sum(bin_content)

    #print "bin content %s" % bin_content
    print "Counts %s : %.2f" % ( sample.name, total ) 

    sumw2_bin_content, _ =  np.histogram(sumw2_histogram, bins = bins, weights = weights2)
    bin_error = np.sqrt(sumw2_bin_content)

    bin_content = [bc / total for bc in bin_content]
    bin_width = bins[1] - bins[0]

    alpha = 1.0
    histtype = 'step'
    zorder = 1e6
    if filled :
        alpha = 0.5
        histtype = 'stepfilled'
        zorder = 0

    x = []
    y = []
    for i in range(len(bin_content)) :
        x.append(bin_edges[i])
        x.append(bin_edges[i] + bin_width)
        y.append(bin_content[i])
        y.append(bin_content[i])

    x.append(x[-1])
    y.append(-1000)
    if not filled :
        pad.plot(x, y, ls='--', color = sample.color,
                        label = sample.displayname,
                        lw=1.5, zorder = zorder)
    else :
        pad.fill(x, y, color = sample.color, alpha = alpha,
                            label = sample.displayname,
                            zorder = zorder,
                            edgecolor = 'k')
    

    return max(bin_content), min(bin_content)

    

def make_plot(plot, reg, samples, output_dir, trigeff) :

    print 30 * '-'
    print " > plotting %s" % plot.vartoplot

    xlow = plot.xlow
    xhigh = plot.xhigh
    bw = plot.binwidth
    nbins = np.arange(xlow, xhigh + bw, bw)
    pad = plot.pad

    maxy = -1
    miny = 1e9

    for s in samples :
        filled = not s.is_signal
        h_maxy, h_miny = draw_histo(pad, s, variable = plot.vartoplot, filled = filled,
                    bins = nbins, absval = plot.absvalue, scaling = trigeff)
        if h_maxy > maxy : maxy = h_maxy
        if h_miny < miny : miny = h_miny

    if plot.vartoplot == "met" :
        labels = [0, 50, 100, 150, 200, 250, 300, 350, 400]
        pad.set_xticklabels(labels)

    multiplier = 1.55
    low = 0.0
    if plot.logy :
        multiplier = 1e2
        low = 0.01 * miny
    pad.set_ylim(low, maxy * multiplier)

    pad.legend(loc = 'best', fontsize = 16, frameon = False, ncol = 1)

    ######################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "l1topo_eff_%s_%s.pdf" % ( reg.name, plot.vartoplot )

    print " >>> Saving plot to : %s" % os.path.abspath(save_name)
    plot.fig.savefig(save_name, bbox_inches = 'tight', dpi = 200)

def make_truth_plots(output_dir, select_var, do_logy, trigeff) :
    
    samples = get_samples()

    reg = region.Region("wwbb", "WW$bb$")
    reg.tcut = "n_bjets==2"# && dphi_llmet<1.75 && dphi_llmet>-1.75"# && l0_pt>10 && l1_pt>10"
    #reg.tcut = "mll>20 && n_bjets==2 && bj0_pt>20 && bj1_pt>20 && l0_pt>25 && l1_pt>20 && l0_eta<2.4 && l0_eta>-2.4 && l1_eta<2.4 && l1_eta>-2.4"

    variables = {}
    variables["l0_pt"] = [5, 0, 200]
    variables["l1_pt"] = [5, 0, 120]
    variables["abs(dphi_llmet)"] = [0.1, 0, 3.2]
    variables["dr_llmet"] = [ 0.5, 0, 5 ]
    variables["abs(dphi_ll)"] = [ 0.1, 0, 3.2]
    variables["dRll"] = [0.5, 0, 5]
    variables["met"] = [0.02, 0, 0.4]
    variables["mll"] = [10, 0, 400]
    variables["j0_pt"] = [10, 0, 400]
    variables["bj0_pt"] = [10, 0, 400]
    variables["sj0_pt"] = [10, 0, 400]
    variables["j1_pt"] = [10, 0, 400]

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
        p = hist1d.Canvas(logy = do_logy)
        if "abs(" in var :
            var = var.replace("abs(", "").replace(")", "")
            p.absvalue = True
        p.vartoplot = var
        p.bounds = bounds
        name = var.replace("[","").replace("]","").replace("(","").replace(")","") 
        p.name = name
        y_label_unit = ""
        x_label = var
        y_label = "a.u."
        p.labels = [x_label, y_label]

        p.logy = do_logy
        p.build_canvas(logy = p.logy)

        make_plot(p, reg, samples, output_dir, trigeff)


############################################################################
# trigger eff

def get_reco_samples() :

    samples = []

    filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/" 
    h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/mc/h5/" # these samples already have the pT cuts applied

    lumi_factor = 36.06

    ttbar = sample.Sample("ttbar", "$t\\bar{t}$")
    ttbar.scalefactor = lumi_factor
    ttbar.fillstyle = 0
    ttbar.linestyle = '-'
    ttbar.color = 'r'
    ttbar.load(filelist_dir + "ttbar", h5_dir_mc)
    samples.append(ttbar)

    hh = sample.Sample("hh", "SM $hh$")
    hh.scalefactor = lumi_factor
    hh.fillstyle = 0
    hh.linestyle = '-'
    hh.color = 'b'
    hh.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '342053')
    samples.append(hh)

    dsids = ['343772', '343775', '343777']
    massx = [600, 800, 1000]
    for idsid, dsid in enumerate(dsids) :
        x = sample.Sample('x%d' % massx[idsid], 'X %d GeV' % massx[idsid])
        x.scalefactor = lumi_factor
        x.load(filelist_dir + 'wwbb_susy2', h5_dir_mc, dsid_select = '%s' % dsids[idsid])
        samples.append(x)

    return samples

def trigger_variables() :

    out = []
    out.append('trig_pass2015')
    out.append('trig_pass2016update')
    out.append('trig_e60_lhmedium')
    out.append('trig_e120_lhloose')
    out.append('trig_mu20_iloose_L1MU15')
    out.append('trig_mu40')
    out.append('trig_mu60_0eta105_msonly')
    out.append('trig_e60_lhmedium_nod0')
    out.append('trig_e140_lhloose_nod0')
    out.append('trig_mu26_ivarmedium')
    out.append('trig_mu50')

    return out

def trigger_sel_string() :

    sel = "( year==2015 && ( (trig_e60_lhmedium==1 || trig_mu20_iloose_L1MU15) || trig_pass2015==1   ) ) || "
    sel += "( year==2016 && ( (trig_e60_lhmedium_nod0==1 || trig_mu26_ivarmedium==1) || trig_pass2016update==1) )"
    return sel

def get_counts(sample, idx_str) :

    chunks = sample.chain()
    count = 0.0
    sumw2 = 0.0
    for ic, chain in enumerate(chunks) :
        set_idx = "indices = np.array( %s )" % idx_str
        exec(set_idx)
        ds = chain[indices] # apply the selection to the dataset object
        w = ds['eventweight']
        h, _ = np.histogram(ds['l0_pt'], weights = w)
        hw2, _ = np.histogram(ds['l0_pt'], weights = w**2)
        count += sum(h)
        sumw2 += sum(hw2)

    return count, sqrt(sumw2)

def error(a, b, ae, be) :
    """
    error for estimate of a/b with error ae on a, and error be on b
    """

    return (a/b) * sqrt( (ae/a)**2 + (be/b)**2 )

def calculate_efficiency(sample, region, varlist) :

    base_selection = region.tcut

    sel_with_pt = base_selection + " && l0_pt>25 && l1_pt>20"
    sel_with_pt_and_trigger = sel_with_pt + " && %s" % trigger_sel_string()

    base_selection_idx_str = sample_utils.index_selection_string(base_selection, 'chain', varlist)
    sel_with_pt_idx_str = sample_utils.index_selection_string(sel_with_pt, 'chain', varlist)
    sel_with_pt_and_trigger_idx_str = sample_utils.index_selection_string(sel_with_pt_and_trigger, 'chain', varlist)
    sel_with_pt_and_trigger_idx_str = sel_with_pt_and_trigger_idx_str.replace("']_nod0", "_nod0']")

    initial_counts, initial_error = get_counts(sample, base_selection_idx_str)

    pt_counts, pt_error = get_counts(sample, sel_with_pt_idx_str)

    pt_trig_counts, pt_trig_error = get_counts(sample, sel_with_pt_and_trigger_idx_str)

    print 30 * '-'
    print " Process : %s "% sample.name
    print "  Initial counts   : %.4f +/- %.4f" % (initial_counts, initial_error)
    print "  pT counts        : %.4f +/- %.4f" % (pt_counts, pt_error)
    print "  pT + trig counts : %.4f +/- %.4f" % (pt_trig_counts, pt_trig_error)

    print 15 * '- '
    print " >>> pT/initial       : %.4f +/- %.4f" % ( pt_counts / initial_counts, error(pt_counts, initial_counts, pt_error, initial_error) )
    print " >>> trig/initial      : %.4f +/- %.4f" % ( pt_trig_counts / initial_counts, error(pt_trig_counts, initial_counts, pt_trig_error, initial_error) )
    print " >>> trig/pT           : %.4f +/- %.4f" % ( pt_trig_counts / pt_counts, error(pt_trig_counts, pt_counts, pt_trig_error, pt_error) )
    

def calculate_trigger_eff() :

    samples = get_reco_samples()

    r = region.Region("trig_test", "trig test")
    r.tcut = "mll>20 && nLeptons==2 && nBJets==2 && bj0_pt>20 && bj1_pt>20"
    required_variables = ['mll', 'nLeptons', 'nBJets', 'bj0_pt', 'bj1_pt', 'year', 'l0_pt', 'l1_pt', 'eventweight', 'l0_eta', 'l1_eta', 'nMuons', 'nElectrons']
    required_variables += trigger_variables()

    cacher = sample_cacher.SampleCacher('./cache')
    cacher.samples = samples
    cacher.region = r
    cacher.fields = required_variables
    print str(cacher)
    cacher.cache()

    for sample in samples :
        calculate_efficiency(sample, r, required_variables)


###############################################################################
# summary plot

def make_summary_plot() :

    from matplotlib.gridspec import GridSpec

    pt_eff = {}

    topo_eff = {}

    topo_eff['pt'] = {}
    topo_eff['pt']['hh'] = 62
    topo_eff['pt']['600'] = 70
    topo_eff['pt']['800'] = 77.5
    topo_eff['pt']['1000'] = 81
    topo_eff['pt']['tt'] = 69

    topo_eff['drll2'] = {}
    topo_eff['drll2']['hh'] = 88
    topo_eff['drll2']['600'] = 94
    topo_eff['drll2']['800'] = 98
    topo_eff['drll2']['1000'] = 99
    topo_eff['drll2']['tt'] = 36

    topo_eff['drll25'] = {}
    topo_eff['drll25']['hh'] = 93
    topo_eff['drll25']['600'] = 98
    topo_eff['drll25']['800'] = 99
    topo_eff['drll25']['1000'] = 100
    topo_eff['drll25']['tt'] = 56

    topo_eff['dr_metll2'] = {}
    topo_eff['dr_metll2']['hh'] = 70
    topo_eff['dr_metll2']['600'] = 84
    topo_eff['dr_metll2']['800'] = 88.3
    topo_eff['dr_metll2']['1000'] = 91.2
    topo_eff['dr_metll2']['tt'] = 32

    topo_eff['dr_metll25'] = {}
    topo_eff['dr_metll25']['hh'] = 83
    topo_eff['dr_metll25']['600'] = 92.5
    topo_eff['dr_metll25']['800'] = 95
    topo_eff['dr_metll25']['1000'] = 96
    topo_eff['dr_metll25']['tt'] = 52

    topo_eff['dphi_ll25'] = {}
    topo_eff['dphi_ll25']['hh'] = 77
    topo_eff['dphi_ll25']['600'] = 87
    topo_eff['dphi_ll25']['800'] = 93
    topo_eff['dphi_ll25']['1000'] = 97
    topo_eff['dphi_ll25']['tt'] = 31

    topo_eff['dphi_ll75'] = {}
    topo_eff['dphi_ll75']['hh'] = 88
    topo_eff['dphi_ll75']['600'] = 93
    topo_eff['dphi_ll75']['800'] = 97
    topo_eff['dphi_ll75']['1000'] = 99
    topo_eff['dphi_ll75']['tt'] = 46

    topo_eff['dphi_metll25'] = {}
    topo_eff['dphi_metll25']['hh'] = 66
    topo_eff['dphi_metll25']['600'] = 84
    topo_eff['dphi_metll25']['800'] = 90
    topo_eff['dphi_metll25']['1000'] = 93
    topo_eff['dphi_metll25']['tt'] = 29

    topo_eff['dphi_metll75'] = {}
    topo_eff['dphi_metll75']['hh'] = 79
    topo_eff['dphi_metll75']['600'] = 92
    topo_eff['dphi_metll75']['800'] = 93
    topo_eff['dphi_metll75']['1000'] = 95
    topo_eff['dphi_metll75']['tt'] = 44

    fig = plt.figure(figsize = (14,8))
    grid = GridSpec(100,100)
    upper = fig.add_subplot(grid[0:48,:])
    lower = fig.add_subplot(grid[51:100,:])

    variables = ['pt', 'drll2', 'drll25', 'dr_metll2', 'dr_metll25', 'dphi_ll25', 'dphi_ll75', 'dphi_metll25', 'dphi_metll75']
    nice_names = {}
    nice_names['pt'] = 'Lep Triggers'
    nice_names['drll2'] = '$\\Delta R_{\\ell\\ell} < 2$'
    nice_names['drll25'] = '$\\Delta R_{\\ell\\ell} < 2.5$'
    nice_names['dr_metll2'] = '$\\Delta R_{\\ell\\ell,MET} < 2$'
    nice_names['dr_metll25'] = '$\\Delta R_{\\ell\ell,MET} < 2.5$'
    nice_names['dphi_ll25'] = '$|\\Delta \\phi_{\\ell\\ell}| < 1.25$'
    nice_names['dphi_ll75'] = '$|\\Delta \\phi_{\\ell\\ell}| < 1.75$'
    nice_names['dphi_metll25'] = '$|\\Delta \\phi_{\\ell\\ell,MET}| < 1.25$'
    nice_names['dphi_metll75'] = '$|\\Delta \\phi_{\\ell\\ell,MET}| < 1.75$'


    # set the labels
    ticks = []
    for i in range(10) :
        ticks.append(i+0.5)
    labels = []
    upper.set_xticklabels(labels)
    upper.set_xticks(ticks)
    for var in variables :
        labels.append(nice_names[var])
    lower.set_xticklabels(labels)
    for l in lower.get_xmajorticklabels() :
        l.set_rotation(30)
    lower.set_xticks(ticks)

    # bounding lines
    for t in ticks :
        xvals = [t-0.5, t-0.5]
        yvals = [0, 100]
        upper.plot(xvals, yvals, linestyle = '--', alpha = 0.5, color = 'k')
        yvals = [0.97, 2.0]
        lower.plot(xvals, yvals, linestyle = '--', alpha = 0.5, color = 'k')

    xvals = [ticks[0] - 0.5, ticks[-1] - 0.5]
    yvals = [1.0, 1.0]
    lower.plot(xvals, yvals, linestyle = '-', alpha = 0.5, color = 'r')

    for ax in [upper, lower] :
        ax.tick_params(axis='both', which='both', labelsize=11)
        which_grid = 'both'
        ax.grid(color='k', which=which_grid, linestyle='--', lw=1, alpha=0.1)

    offsets = {}
    offsets['hh'] = -0.3
    offsets['600'] = -0.15
    offsets['800'] = 0
    offsets['1000'] = 0.15
    offsets['tt'] = 0.3

    bkgs = ['hh', '600', '800', '1000', 'tt']

    ##################################################################
    # upper pad

    colors = ['r', 'b', 'g', 'm', 'k']
    for ibkg, bkg in enumerate(bkgs) :
        xvals = []
        yvals = []
        for ivar, var in enumerate(variables) :
            xvals.append( ticks[ivar] + offsets[bkg] )
            yvals.append( topo_eff[var][bkg] )
        marker = 'o'
        if bkg == 'tt' :
            marker = 'X'
        upper.plot(xvals, yvals, marker = marker, linestyle = 'none', color = colors[ibkg], label = bkg)

    upper.set_ylabel("Efficiency", fontsize = 14)
    upper.legend(loc = 'best', frameon = True, ncol = 1)

    ##################################################################
    # lower pad

    #signals = [b for b in bkgs if b != 'tt']
    signals = bkgs
    for isig, sig in enumerate(signals) :
        xvals = []
        yvals = []
        for ivar, var in enumerate(variables) :
            #if var == 'pt' : continue
            xvals.append( ticks[ivar] + offsets[sig] )
            s_factor = topo_eff[var][sig] - topo_eff['pt'][sig]
            b_factor = topo_eff[var]['tt'] - topo_eff['pt']['tt']
            s_factor = s_factor / 100.0
            b_factor = b_factor / 100.0
            s_factor = 1.0 + s_factor
            b_factor = 1.0 + b_factor
            s_o_b_diff = (s_factor / b_factor)
            print "s_factor = %.2f   b_factor = %.2f   s/b factor = %.2f" % ( s_factor, b_factor, s_o_b_diff )
            yvals.append( s_o_b_diff )
        marker = 'o'
        if sig == 'tt' :
            marker = 'X'
        lower.plot(xvals, yvals, marker = marker, linestyle = 'none', color = colors[isig], label = sig) 

    lower.set_ylabel("$\\Delta$ S/B", fontsize = 14)
    fig.savefig("topo_test.pdf", bbox_tight = 'inches', dpi = 200)

def main() :
    print " * l1topo pot * "

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default="./", help = "Set output directory for plots")
    parser.add_option("--logy", default=False, action="store_true", help="Set the plots to have log y-axis")
    parser.add_option("-v", "--var", default = "", help = "Request a specific variable to plot")
    parser.add_option("--eff", default = False, action='store_true', help = "Calculate pseudo trigger efficiency")
    parser.add_option("--trigeff", default="1.0", help = 'Set trigger efficiency to apply to plots, counts')
    parser.add_option("--summary", default = False, action = 'store_true', help = 'Make summary plot')
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    select_var = options.var
    do_logy = options.logy
    do_eff = options.eff
    trigeff = options.trigeff
    do_summary = options.summary

    if do_summary and do_eff :
        print "ERROR Cannot make summary plot and trig eff at the same time"
        sys.exit()

    if do_eff :
        calculate_trigger_eff()

    elif do_summary :
        make_summary_plot()

    else :
        make_truth_plots(output_dir, select_var, do_logy, trigeff)

#______________________________________________________
if __name__ == "__main__" :
    main()

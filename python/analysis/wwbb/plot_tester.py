#!/usr/bin/env python

import sys
import os
import glob
import h5py

import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()
from matplotlib.gridspec import GridSpec

import pandas as pd
import numpy as np

class Sample :
    def __init__(self, name = "", color = "", filelist = []) :
        self.files = filelist
        self.name = name
        self.color = color
        self.entries = 0
        self.n_in_chain = 0
        #self.df = None
        #self.chain = self.build_chain(filelist)

    def get_entries(self) :
        return self.entries

    def get_chain_size(self) :
        return self.n_in_chain

    def pd_chain(self) :
        self.entries = 0
        chunksize = 100000
        for file in self.files :
            with h5py.File(file, 'r') as h5_file :
                ds = h5_file['superNt']
                self.entries += ds.size
                for x in range(0, ds.size, chunksize) :
                    yield pd.read_hdf(file, 'superNt', start=x, stop=x+chunksize, chunksize=chunksize, iterator=True)

    def chain(self):
        chunksize = 10000
        self.entries = 0
        for file in self.files:
            with h5py.File(file,'r') as h5_file:
                ds = h5_file['superNt']
                self.entries += ds.size
                for x in range(0,ds.size, chunksize):
                    yield ds[x:x+chunksize]

    def var_chain(self, var) :
        chunksize = 100000
        self.entries = 0
        for file in self.files:
            with h5py.File(file,'r') as h5_file:
                ds = h5_file['superNt']
                self.entries += ds.size
                for x in range(0,ds.size, chunksize):
                    yield ds[x:x+chunksize,'HT2Ratio', 'nBJets', 'mll', 'eventweight', 'l0_pt']

    def df(self, pytables_iter = None, key = 'superNt') :
        if pytables_iter == None :
            return None
        return pd.DataFrame(pytables_iter.store[key])

def get_combined_dataframe(hfiles) :

    print " > get_combined_dataframe"

    combined = None
    for ifile, hfile in enumerate(hfiles) :
        print "   -> %s" % hfile
        if ifile == 0 :
            combined = pd.read_hdf(hfile, "superNt") 
            print "df size [%d] = %d  (combined = %d)" % (ifile, len(combined), len(combined))
        else :
            df = pd.read_hdf(hfile, "superNt")
            combined = pd.concat([combined, df])
            print "df size [%d] = %d  (combined = %d)" % (ifile, len(df), len(combined))
    return combined

def get_sample(name, txt_files, h5dir) :

    all_files = glob.glob(h5dir + "*.h5")

    dids = []
    for txt in txt_files :
        is_data = False
        did = ""
        first_split = "mc15_13TeV."
        if "data15" in txt or "data16" in txt :
            is_data = True
            if "data15" in txt :
                first_split = "data15_13TeV."
            elif "data16" in txt :
                first_split = "data16_13TeV."
        did = txt.split(first_split)[1]
        did = did.split(".")[0]
        if is_data :
            did = did[2:] # remove first 00
        dids.append(did)

    sample_files = []
    for did in dids :
        for f in all_files :
            if did in f :
                sample_files.append(f)
                break

    print "samples for %s = %d" % (name, len(sample_files))

    def h5_chain(file_list):
        for file in file_list:
            with h5py.File(file,'r') as h5_file:
                ds = h5_file['superNt']
                for x in range(0,ds.size, 1000):
                    yield ds[x:x+1000]

    colors = {}
    colors['ttbar'] = "#f6f5f0"
    colors['Ztt'] = "#fecf90"
    colors['Zll'] = "#d1b7a5"
    colors['Wt'] = "#698bae"
    colors['Diboson'] = "#785e6f"
    colors['Wjets'] = "#daadbb"
    colors['ttV'] = "#b3e6fd"
    colors['Data'] = 'k'
    #colors['ttbar'] = "#698bae"
    #colors['Ztt'] = "#fecf90"
    #colors['Wt'] = "#264350"
    #colors['Data'] = 'k'

    s = Sample(name, color=colors[name], filelist = sample_files)


    #s.chain = h5_chain(s.files)
    #for x in s.chain() :
    #    #print x
    #    print "length before = %d" % len(x)
    #    x = x[ (x['nBJets']>=2) & (x['l0_pt']>150)]
    #    print "length after = %d" % len(x)
    #
    #    #print x[x['nBJets']>=2]['nBJets'][:40]
    #    #print x['nBJets'][:40]
    #    sys.exit()

    return s

def get_samples() :
    out = []

    filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
    samples = ["ttbar", "Wt"]

    ttbar_txt_files = glob.glob(filelist_dir + "ttbar/*.txt")
    wt_txt_files = glob.glob(filelist_dir + "Wt/*.txt")
    ztt_txt_files = glob.glob(filelist_dir + "zjets_sherpa_tt/*.txt")
    zll_txt_files = glob.glob(filelist_dir + "zjets_sherpa_ll/*.txt")
    diboson_txt_files = glob.glob(filelist_dir + "diboson_sherpa_llvv/*.txt")
    wjets_txt_files = glob.glob(filelist_dir + "wjets_sherpa/*.txt")
    ttv_txt_files = glob.glob(filelist_dir + "ttV/*.txt")
    data_txt_files = glob.glob(filelist_dir + "data_n0234/*.txt")

    h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/c_aug16/mc/h5/"
    h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/c_aug16/data/h5/"

    ttbar_sample = get_sample("ttbar", ttbar_txt_files, h5_dir_mc)
    wt_sample = get_sample("Wt", wt_txt_files, h5_dir_mc)
    ztt_sample = get_sample("Ztt", ztt_txt_files, h5_dir_mc)
    zll_sample = get_sample("Zll", zll_txt_files, h5_dir_mc)
    diboson_sample = get_sample("Diboson", diboson_txt_files, h5_dir_mc)
    wjets_sample = get_sample("Wjets", wjets_txt_files, h5_dir_mc)
    ttv_sample = get_sample("ttV", ttv_txt_files, h5_dir_mc)
    data_sample = get_sample("Data", data_txt_files, h5_dir_data)

    return (ttbar_sample, wt_sample, ztt_sample, zll_sample, diboson_sample, wjets_sample, ttv_sample), (), data_sample

def replace_operators(cut) :
    operators =["==", ">=", "<=", ">", "<", "!="]
    for op in operators :
        cut = cut.replace(op, "']%s"%op)
    cut = cut.replace("']']", "']")
    return cut

def get_cut_np(data, selection_str) :

    cut = selection_str.replace(" && ", ") & (data['")
    cut = replace_operators(cut)
    cut = "(data['" + cut
    cut = cut + ")"
    turn = "data = data[%s]" % cut
    exec(turn)
    return data

def make_legend(ordering, name_dict, pad) :
    handles, labels = pad.get_legend_handles_labels()
    new_handles = []
    new_labels = []
    for l in ordering :
        for il, label in enumerate(labels) :
            if label == l :
                new_labels.append(name_dict[l])
                new_handles.append(handles[il])
    pad.legend(new_handles,
                    new_labels,
                    loc=2, 
                    frameon=False,
                    ncol=2,
                    fontsize=14,
                    numpoints=1)

def make_test_stack(bkgs, signals, data) : #, hist) :

    vars = ["HT2Ratio", "nBJets", "dRll", "MT_1_scaled", "mt2_llbb"]
    nice_vars = ["H$_{T2}^{R}$", "# $b-$jets", "$\\DeltaR_{\\ell\ell}$", "M$_{T1}$", "$m_{T2}^{\\ell\\ellbb}$"]
    ivar = 0
    bw = [0.05, 1, 0.1, 40, 10]
    high = [1.0, 5, 1.5, 1500,200]
    low = [0.0, 0.0, 0.0, 0.0,0]
    selection = "nBJets==2 && mll>20"

    #tmp_bkgs = []
    #tmp_sigs = []
    #for bkg in bkgs :
    #    tmp_bkgs.append(get_cut_np(bkg, selection))
    #bkgs = tmp_bkgs
    #for signal in signals :
    #    tmp_sigs.append(get_cut_np(signal, selection))
    #signals = tmp_sigs
    #data = get_cut_np(data, selection) 

    fig = plt.figure(figsize=(7,8))
    ##fig, (upper, lower) = plt.subplots(figsize=(8,6), nrows=2, ncols=1)
    ##fig.set_figheight()
    #upper = fig.add_axes([0.15,0.4,0.85,0.85])
    #lower = fig.add_axes([0.15,0.15,0.85,0.5])


    grid = GridSpec(100,100)#, height_ratios=[100,100])
    #grid = GridSpec(2,1, height_ratios=[100,100])
    #upper = fig.add_subplot(grid[0,0:75])
    #lower = fig.add_subplot(grid[0,80:100])#, sharex=upper)
    upper = fig.add_subplot(grid[0:75, :])
    lower = fig.add_subplot(grid[80:100, :])#, sharex=upper)
    #upper = hist.fig.add_axes([0.1,0.4,0.9,0.9])
    #lower = hist.fig.add_axes([0.1,0.1,0.9,0.25])

    do_logy = True#False
    if do_logy :
        upper.set_yscale('log')
    nbins = np.arange(low[ivar], high[ivar] + bw[ivar], bw[ivar])

    bkg_histos = []
    #colors = ['#9fb6d9', 'blue', 'green']
    colors = {}
    labels = []

    weights = {}
    for ibkg, bkg in enumerate(bkgs) :

        print "make stack sample %s" % bkg.name

        histo = []
        #chain = bkg.chain()
        chain = bkg.var_chain(vars[ivar])
        b_weights = [] 
        #n_bc = bkg.get_chain_size()
        for ibc, bc in enumerate(chain) :

            #print "  -> %d " % ibc

            bc = get_cut_np(bc, selection)

            lumis = np.ones(len(bc[vars[ivar]]))
            lumis[:] = 36.0
            w = lumis * bc['eventweight']
            w2 = bc['eventweight'] ** 2
            w2 = lumis * w2

            b_weights += list(w)

            bvar = list(bc[vars[ivar]]) # TODO see how to avoid this list() calls and use strictly numpy arrays
            histo += bvar
            #hist += np.histogram(bvar, bins = nbins, weights = w)[0]

        print "  -> %.2f" % sum(histo)
        labels.append(bkg.name)
        bkg_histos.append(histo)
        colors[bkg.name] = bkg.color
        #weights.append(b_weights)
        weights[bkg.name] = b_weights


    count_map = {}
    for ilabel, label in enumerate(labels) :
        count_map[sum(bkg_histos[ilabel])] = label
    bkg_histos = sorted(bkg_histos, key = lambda x : sum(x), reverse = False)
    ordered_labels = []
    ordered_weights = []
    ordered_colors = []
    for bh in bkg_histos :
        ordered_labels.append(count_map[sum(bh)])
        ordered_weights.append(weights[count_map[sum(bh)]])
        ordered_colors.append(colors[count_map[sum(bh)]])
        
    labels = ordered_labels
    weights = ordered_weights
    colors = ordered_colors


    for ibh, bh in enumerate(bkg_histos) :
        print " hist[%d] len x = %d  len w = %d"%(ibh, len(bh), len(weights[ibh]))
    y, x, patches = upper.hist(bkg_histos,
                            bins = nbins,
                            color = colors,
                            weights = weights,
                            label = labels,
                            stacked = True,
                            histtype='stepfilled',
                            lw=1,
                            edgecolor = 'k',
                            alpha=1.0) 

    # total of the stack is the last array in the histogram since we stack
    total_sm_y = y[-1]
    total_sm_x = x
    maxy = max(total_sm_y)
    f = 1.6
    if do_logy :
        f = 1000

    ##################################
    # draw total SM line
    smx = []
    smy = []
    for ix, xx in enumerate(total_sm_x[:-1]) :
        smx.append(xx)
        smx.append(xx + bw[ivar])
        smy.append(total_sm_y[ix])
        smy.append(total_sm_y[ix])
    smx.append(smx[-1])
    smy.append(-1000)
    upper.plot(smx, smy, ls="-", color='k', label = 'Total SM', lw=2)

    ##################################
    # data
    histod = []
    data_chain = data.var_chain(vars[ivar])
    print "make stack sample %s" % data.name
    for idc, dc in enumerate(data_chain) :
        #print "  -> %d " % idc
        dc = get_cut_np(dc, selection)
        dvar = list(dc[vars[ivar]])
        histod += dvar
    if max(histod) > maxy : maxy = max(histod)
    datay = np.histogram(histod, bins = nbins)[0]
    print "  -> %.2f" % sum(datay)
    datax = [ dx + 0.5 * bw[ivar] for dx in total_sm_x ]
    #print "datay = ", datay
    #print "datax = ", datax
    #print "len datay = %d  len datax = %d" % (len(datay), len(datax))
    #sys.exit()
    upper.plot(datax[:-1], datay, 'ko', label = 'Data')

    #########################################
    # table
    print "Total SM = %.2f" % sum(total_sm_y)
    print "Data     = %.2f" % sum(datay)
    print "Data/SM  = %.2f" % ( float(sum(datay)) / float(sum(total_sm_y)) )


    #######################################
    # ratio
    ratio_y = np.ones(len(datay))
    ratio_x = datax
    for idata, d in enumerate(datay) :
        prediction = total_sm_y[idata]
        ratio = 1.0
        if prediction == 0 :
            ratio = -5.0
        else :
            ratio = d / prediction 
        ratio_y[idata] = ratio
    lower.plot(ratio_x[:-1], ratio_y, 'ko')

    # red line
    xl = np.linspace(low[ivar], high[ivar], 20)
    yl = np.ones(len(xl))
    lower.plot(xl,yl, 'r--')
    

    # axes
    print "setting maxy to %.2f" % (f * maxy)
    upper.set_ylim(0.0, f * maxy) 
    lower.set_ylim(0.0, 2)
    upper.set_xlim(0.0, 1)
    upper.set_xticklabels([])
    lower.set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0])
    lower.set_xlim(0.0, 1.0)

    for ax in [upper, lower] :
        ax.tick_params(axis='both', which='both', labelsize=16)
        which_grid = 'both'
        if do_logy :
            which_grid = 'major'
        ax.grid(color='k', which=which_grid, linestyle='--', lw=1, alpha=0.5)

    print "upper ylabel = ", upper.get_position()
    ax_x = upper.get_position().x0;
    lower.set_xlabel(nice_vars[ivar],
                            horizontalalignment = 'right',
                            x = 1.0, fontsize = 20)
    #lower.set_title("Data / Pred",
    #                fontsize=16,
    #                position = (-0.15,0.65),
    #                rotation=90)
    lower.set_ylabel("Data / Pred",
                            fontsize = 18)
    upper.get_yaxis().set_label_coords(-0.16, 1.0) 
    lower.get_yaxis().set_label_coords(-0.16, 0.5)

    upper.set_ylabel("Entries / %.2f" % bw[ivar],
                        horizontalalignment = 'right',
                        y = 1.0, fontsize = 18)


    legend_order = ['Data']
    legend_order += ['Total SM']
    legend_order += sorted(labels, reverse=True)
    leg_names = {}
    leg_names['Data'] = 'Data'
    leg_names['Total SM'] = 'Standard Model'
    leg_names['ttbar'] = '$\\bar{t}t$'
    leg_names['Ztt'] = '$Z\\rightarrow\\tau\\tau$'
    leg_names['Zll'] = '$Z\\rightarrow ee/\\mu\\mu$'
    leg_names['Diboson'] = '$VV\\rightarrow \\ell\\ell\\nu\\nu$'
    leg_names['Wt'] = '$Wt$'
    leg_names['ttV'] = '$\\bar{t}t+V$'
    leg_names['Wjets'] = '$W+jets$'
    make_legend(legend_order, leg_names, upper)
    #upper.legend(loc=2, frameon=False, ncol=2, fontsize=16, numpoints=1)


    fig.savefig("np_test.png", bbox_inches='tight')#, dpi=200)
    #hist.fig.savefig("np_test.png")#, dpi=200)

    
        

        
    

def main() :
    print "plot tester"

    name = "test histogram"
    #figsize=(10,8)
    #h = hist1d.ratio_hist(name=name, figsize=figsize)
    #print h.str()

    bkg, signals, data = get_samples()

    make_test_stack(bkg, signals, data) #, h)




#_____
if __name__ == "__main__" :
    main()

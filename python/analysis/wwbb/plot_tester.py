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

verbose = False

class Sample :
    def __init__(self, name = "", color = "", filelist = []) :
        self.files = filelist
        self.name = name
        self.color = color
        self.entries = 0
        self.n_in_chain = 0
        self.selection_ref = None
        self.do_load_check = True
        #self.df = None
        #self.chain = self.build_chain(filelist)

        self.selection_file = ""
        self.selection_group = ""

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

    def var_chain2(self) :
        chunksize = 100000
        self.entries = 0
        for file in self.files:
            with h5py.File(file,'r') as h5_file:
                ds = h5_file['superNt']
                selected_dataset = None
                if not self.selection_ref :
                    print "   Applying selection to %s" % self.name
                    print "      counts before = %d" % len(ds)
                    indices = ((ds['nBJets']>=2) & (ds['mll']>20))
                    if not indices.any() :
                        continue
                    ref = ds.regionref[np.array(indices)]
                    selected_dataset = ds[ref]
                    print "      counts after = %d" % len(selected_dataset)
                    self.selection_ref = ref
                    del ref
                else  :
                    selected_dataset = ds[self.selection_ref]
                for x in range(0, selected_dataset.size, chunksize) :
                    yield selected_dataset[x:x+chunksize]

    def load_dataset(self, name, ds) :
        print "     -> load_dataset  %s" % name
        for x in range(0, ds.size, 100000) :
            yield ds[x:x+100000]

    def sel_chain(self) :
        chunksize = 100000
        self.entries = 0
        with h5py.File(self.selection_file, 'r') as f :
            process_group = f[self.selection_group]
            #print "sel_chain process_group = %s" % str(process_group.name)
            #print process_group
            for dsname in process_group :
                ds = process_group[dsname]
                for x in range(0, ds.size, chunksize) :
                    yield ds[x:x+chunksize]
            


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

    #print "samples for %s = %d" % (name, len(sample_files))

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
    colors['DY'] = "#ffd787"
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
    dy_txt_files = glob.glob(filelist_dir + "drellyan_sherpa/*.txt")
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
    dy_sample = get_sample("DY", dy_txt_files, h5_dir_mc)
    data_sample = get_sample("Data", data_txt_files, h5_dir_data)

    #print "OMITTING TTBAR FOR TESTING PURPOSES"
    #return (wt_sample, ztt_sample, ttv_sample), (), data_sample
    return (ttbar_sample, wt_sample, ztt_sample, zll_sample, diboson_sample, wjets_sample, ttv_sample, dy_sample), (), data_sample

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

def make_test_stack(selection, var, vars, bkgs, signals, data) : #, hist) :

    print 50 * '-'
    print "make_test_stack    var = %s" % var
    #vars = ["HT2Ratio", "nBJets", "dRll", "MT_1_scaled", "mt2_llbb"]
    nice_vars = ["H$_{T2}^{R}$", "# $b-$jets", "$\\Delta R_{\\ell \\ell}$", "M$_{T1}$", "$m_{T2}^{\\ell \\ell bb}$"]
    nice_vars.append("$m_{bb}$")
    ivar = vars.index(var)
    #ivar = 0
    bw = [0.05, 1, 0.1, 40, 10, 20]
    high = [1.0, 5, 5.0, 1500,600, 1000]
    low = [0.0, 0.0, 0.0, 0.0,0, 0.0]

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

    do_logy = False
    if do_logy :
        upper.set_yscale('log')
    nbins = np.arange(low[ivar], high[ivar] + bw[ivar], bw[ivar])

    bkg_histos = []
    #colors = ['#9fb6d9', 'blue', 'green']
    colors = {}
    labels = []

    weights = {}
    for ibkg, bkg in enumerate(bkgs) :

        #print "make stack sample %s" % bkg.name

        histo = []
        #chain = bkg.chain()


        do_var2 = True
        chain = None
        if do_var2 :
            #chain = bkg.var_chain2()
            chain = bkg.sel_chain()
        else :
            chain = bkg.var_chain(vars[ivar])

        #chain = bkg.var_chain(vars[ivar])
        b_weights = [] 
        #n_bc = bkg.get_chain_size()
        for ibc, bc in enumerate(chain) :

            #print "  -> %d " % ibc

            if not do_var2 :
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

        #print "  -> %.2f" % sum(histo)
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


    #for ibh, bh in enumerate(bkg_histos) :
    #    print " hist[%d] len x = %d  len w = %d"%(ibh, len(bh), len(weights[ibh]))
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
    f = 2.0
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
    data_chain = None
    if do_var2 :
        data_chain = data.sel_chain()
    else :
        data_chain = data.var_chain(vars[ivar])
    #print "make stack sample %s" % data.name
    for idc, dc in enumerate(data_chain) :
        #print "  -> %d " % idc
        dc = get_cut_np(dc, selection)
        dvar = list(dc[vars[ivar]])
        histod += dvar
    if max(histod) > maxy : maxy = max(histod)
    datay = np.histogram(histod, bins = nbins)[0]
    #print "  -> %.2f" % sum(datay)
    datax = [ dx + 0.5 * bw[ivar] for dx in total_sm_x ]
    #print "datay = ", datay
    #print "datax = ", datax
    #print "len datay = %d  len datax = %d" % (len(datay), len(datax))
    #sys.exit()
    upper.plot(datax[:-1], datay, 'ko', label = 'Data')

    #########################################
    # table
    print " Counts summary:"
    print "     Total SM = %.2f" % sum(total_sm_y)
    print "     Data     = %.2f" % sum(datay)
    print "     Data/SM  = %.2f" % ( float(sum(datay)) / float(sum(total_sm_y)) )


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
    lower.plot(ratio_x[:-1], ratio_y, 'ko', zorder=1000)

    # red line
    xl = np.linspace(low[ivar], high[ivar], 20)
    yl = np.ones(len(xl))
    lower.plot(xl,yl, 'r--', zorder=0)
    

    # axes
    #print "setting maxy to %.2f" % (f * maxy)
    upper.set_ylim(0.0, f * maxy) 
    lower.set_ylim(0.0, 2)
    upper.set_xlim(0.0, high[ivar])
    upper.set_xticklabels([])
    #lower.set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0])
    lower.set_xlim(0.0, high[ivar])

    for ax in [upper, lower] :
        ax.tick_params(axis='both', which='both', labelsize=16)
        which_grid = 'both'
        if do_logy :
            which_grid = 'major'
        ax.grid(color='k', which=which_grid, linestyle='--', lw=1, alpha=0.1)

    #print "upper ylabel = ", upper.get_position()
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
    leg_names['DY'] = 'Drell-Yan'
    make_legend(legend_order, leg_names, upper)
    #upper.legend(loc=2, frameon=False, ncol=2, fontsize=16, numpoints=1)


    save_name = "./test_plots/np_test_%s.pdf" % vars[ivar]
    print "Saving plot to : %s" % save_name
    fig.savefig(save_name,  bbox_inches='tight', dpi=200)
    #hist.fig.savefig("np_test.png")#, dpi=200)

def check_selected_sample(list_name, sample, selection_str, selection_name, relevant_variables) :

    # check file and see if 

    name = selection_name.split()
    name = '_'.join(name)

    group_name = "%s" % name
    cut_attr = selection_str


    group_pattern = "/%s/%s/" % (name, sample.name)

    sub_file_no = 0
    for file in sample.files :
        with h5py.File(file, 'r') as f :
            # input dataset
            input_dset = f['superNt']
        
    
def add_selection(group, sample, cut_str, relevant_columns) :

    sel_var = ["'%s'" % var for var in relevant_columns]
    sel_var_str = ','.join(sel_var)
    #print "sel_var_str = ", sel_var_str
    sub_file_no = 0
    for file in sample.files :
        #print "     -> %d "% sub_file_no
        with h5py.File(file, 'r') as sample_file :
            #print sel_var_str
            #sys.exit()
            set_ds = "ds = sample_file['superNt'][ %s ]" % sel_var_str
            exec(set_ds)
            #ds = sample_file['superNt'][col for col in relevant_columns]
            #ds = sample_file['superNt']['nBJets', 'HT2Ratio', 'mll']
            indices = np.array( (ds['nBJets']>=2) & (ds['mll']>20) & (ds['l0_pt']>45) )
            selected_dataset = ds[indices]
            sub_dataset_name = "dataset_%d" % sub_file_no
            out_ds = group.create_dataset(sub_dataset_name, shape=selected_dataset.shape, dtype=selected_dataset.dtype)
            out_ds[:] = selected_dataset
            sub_file_no += 1


def check_selected(samples, selection_str, selection_name, relevant_variables) :

    selection_filename = "test_selection_list.hdf5"
    if not os.path.isfile(selection_filename) :
        with h5py.File(selection_filename, 'w') as selection_file :
            name = '_'.join(selection_name.split())
            selection_group = selection_file.create_group(name)
            selection_group.attrs['cut_string'] = selection_str

            for sample in samples :
                print "check_selected   > %s " % sample.name
                process_group = selection_group.create_group(sample.name)
                #add_selection_file(selection_filename, sample, selection_str, selection_name)
                add_selection(process_group, sample, selection_str, relevant_variables)
                sample.selection_file = selection_filename
                sample.selection_group = "/%s/%s/" % ( str(selection_group.name), sample.name ) 
        return selection_filename

    elif os.path.isfile(selection_filename) :

        print "Found selection file %s" % selection_filename
        # check the current file for
        #  1) make sure that the selection definintion is the same
        #  2) make sure that each of our samples is in there
        # if (1) fails, don't try to be smart -- just exit
        # if (2) fails (and (1) succeeds), just add the dataset for the sample to the file
        # TODO CHECK THAT ALL OF THE RELEVANT VARIABLES ARE IN THE FOUND FILE -- IF NOT EITHER
        # START A FRESH OR JUST ADD THAT FIELD

        with h5py.File(selection_filename, 'a') as selection_file :
            name = '_'.join(selection_name.split())
            for top_level in selection_file :
                print "looking for top level -> %s "% top_level
                if str(top_level) == name :
                    print "  %s in file!" % name
                    selection_group = selection_file["%s" % name]
                    cut_definition = selection_group.attrs['cut_string']
                    if cut_definition != selection_str :
                        print "ERROR Cut definition for %s in selection file %s does not match!" % (name, selection_file)
                        print "ERROR Expected selection: %s" % selection_str
                        print "ERROR Selection in file : %s" % cut_definition
                        sys.exit() 
                else :
                    print "ERROR Did not find top level group for selection definition (%s) (name=%s)in file %s" % (selection_str, name, selection_filename)
                    sys.exit()

            print "Top level and selection seem ok!"

            selection_group = selection_file["%s" % name]
            print "Looking for selection group %s" % selection_group.name
            group_keys = [ str(g) for g in selection_group.keys() ]
            for sample in samples :
                process_group_name = sample.name
                if process_group_name in group_keys :
                    print "loading   > %s (found in pre-existing group)" % sample.name
                    sample.selection_file = selection_filename
                    sample.selection_group = "/%s/%s/" % ( str(selection_group.name), sample.name ) 
                else :
                    print "loading   > %s did not find in pre-existing group, adding it now" % sample.name
                    process_group = selection_group.create_group(sample.name)
                    add_selection(process_group, sample, selection_str, relevant_variables)
                    sample.selection_file = selection_filename
                    sample.selection_group = "/%s/%s/" % ( str(selection_group.name), sample.name )
        return selection_filename
                         
                        
                    


    #for sample in samples :
    #    check_selected_sample(selection_filename, sample, selection_str, selection_name)
    #
    #def chain_check(self, region) :
    #    chunksize = 10000
    #    if self.do_load_check :
    #        self.do_load_check = False

    #        selection_filename = "test_selection_list.hdf5"
    #        group_pattern = "/%s/%s/" % ( region, self.name )
    #        if os.path.isfile(selection_filename) :

    #            # walk across the stored datasets
    #            with h5py.File(selection_filename, 'r') as f :
    #                for ds in f[group_pattern] :
    #                    for x in range(0,ds.size, chunksize):
    #                        yield ds[x:x+chunksize]
    #        else :
    #            try :
    #                sub_file_number = 0
    #                with h5py.File(selection_filename, 'w-') as f :
    #                    group = f.create_group(group_pattern)
    #                    dataset_name = "sub_data_%03d" % sub_file_number
    #                    
    #                    sub_file_number += 1
    #            except IOError :
    #                print "A selection file of the name %s already exists, cannot continue with writing it" % selection_filename
    #                sys.exit()
                
                
                    
        

        
    

def main() :
    print "plot tester"

    

    name = "test histogram"
    #figsize=(10,8)
    #h = hist1d.ratio_hist(name=name, figsize=figsize)
    #print h.str()

    bkg, signals, data = get_samples()
    selection_name = "wwbb test"
    selection = "nBJets>=2 && mll>20 && l0_pt>45" 
    all_samples = []
    for b in bkg :
        all_samples.append(b)
    for s in signals :
        all_samples.append(s)
    all_samples.append(data)
    vars = ["HT2Ratio", "nBJets", "dRll", "MT_1_scaled", "mt2_llbb", "mbb"]
    vars.append("mll")
    vars.append("eventweight")
    vars.append("l0_pt")
    selection_file = check_selected( all_samples, selection, selection_name, vars) 

    for v in vars[:6] :
        make_test_stack(selection, v, vars, bkg, signals, data) #, h)




#_____
if __name__ == "__main__" :
    main()

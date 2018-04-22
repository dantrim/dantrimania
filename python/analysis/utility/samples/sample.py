#!/usr/bin/env python

import os
import sys
import glob

import h5py

default_colors = {}
default_colors['ttbar'] = "#f6f5f0"
default_colors['Ztt'] = "#fecf90"
default_colors['Zll'] = "#d1b7a5"
default_colors['Wt'] = "#698bae"
default_colors['Diboson'] = "#785e6f"
default_colors['Wjets'] = "#daadbb"
default_colors['DY'] = "#ffd787"
default_colors['ttV'] = "#b3e6fd"
default_colors['Data'] = 'k'

class Sample(object) :
    def __init__(self, name, displayname) :
        self._name = name
        self._displayname = displayname
        self._scalefactor = 1.0
        self._filestyle = 0
        self._linestyle = '-'
        self._color = '' 
        self._loaded = False
        self._is_data = False
        self._is_signal = False

        # loaded properties
        self._h5_dir = ""
        self._filelist_dir = ""
        self._loaded_dsids = [] # integers
        self._loaded_h5_files = []
        self._selection_file = "" # this is the file that is used to build the chain that we plot from
        self._selection_group = "" # path within selection HDF5 file to the sample's dataset


    # simple name 
    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, name = "") :
        self._name = name

    # displayname
    @property
    def displayname(self) :
        return self._displayname
    @displayname.setter
    def displayname(self, name = "") :
        self._displayname = name

    # scale factor
    @property
    def scalefactor(self) :
        return self._scalefactor
    @scalefactor.setter
    def scalefactor(self, val = 1.0) :
        self._scalefactor = val

    # color
    @property
    def color(self) :
        if not self._color == "" :
            return self._color
        else :
            try :
                return default_colors[self._name]
            except KeyError :
                print "KeyError    Default color for sample %s not defined, returning 'blue'"
                return 'blue'
    @color.setter
    def color(self, color_str = "") :
        self._color = color_str

    @property
    def is_data(self) :
        return self._is_data
    @is_data.setter
    def is_data(self, val) :
        self._is_data = val

    @property
    def is_signal(self) :
        return self._is_signal
    @is_signal.setter
    def is_signal(self, val) :
        self._is_signal = val

    @property
    def h5_files(self) :
        return self._loaded_h5_files
    @h5_files.setter
    def h5_files(self, h5_filelist) :
        self._loaded_h5_files = h5_filelist

    @property
    def dsids(self) :
        return self._loaded_dsids
    @dsids.setter
    def dsids(self, dsid_list) :
        for d in dsid_list :
            self._loaded_dsids.append(int(d))

    @property
    def h5dir(self) :
        return self._h5_dir
    @h5dir.setter
    def h5dir(self, val = "") :
        self._h5_dir = val

    @property
    def filelistdir(self) :
        return self._filelist_dir
    @filelistdir.setter
    def filelistdir(self, val = "") :
        self._filelist_dir = val

    def load_file(self, filename) :

        if not filename.endswith(".h5") :
            print "ERROR [samples %s load] Input file does not have '.h5' extension" % filename
            sys.exit()

        self._loaded_h5_files.append(filename)

    # load the sample
    def load(self, filelist_directory, h5_dir, dsid_select = "", tags = [] ) :

        if not h5_dir.endswith("/") :
            h5_dir += "/"
        if not os.path.isdir(h5_dir) :
            print "ERROR [sample %s load] H5 sample directory '%s' not found" % (self.name, h5_dir)
            sys.exit()

        if not filelist_directory.endswith("/") :
            filelist_directory += "/"
        if not os.path.isdir(filelist_directory) :
            print "ERROR [sample %s load] Filelist directory '%s' not found" % (self.name, filelist_directory)

        all_files = glob.glob(h5_dir + "*.h5")
        if len(all_files) == 0 :
            print "ERROR [sample load] H5 directory '%s' has no *.h5 files" % (h5_dir)
            sys.exit()

        filelists = glob.glob(filelist_directory + "*.txt")
        if len(filelists) == 0 :
            print "ERROR [sample %s load] No text filelists found in directory '%s'" % (self.name, filelist_directory)
            sys.exit()

        sample_dsids = []
        is_data = False
        for txt in filelists :
            dsid = ""

            first_split = "mc15_13TeV."
            if "mc16_13TeV." in txt :
                first_split = "mc16_13TeV."

            if "data15" in txt or "data16" in txt or "data17" in txt :
                is_data = True
                if "data15" in txt :
                    first_split = "data15_13TeV."
                elif "data16" in txt :
                    first_split = "data16_13TeV."
                elif "data17" in txt :
                    first_split = "data17_13TeV."

            dsid = txt.split(first_split)[1]
            dsid = dsid.split(".")[0]
            if is_data :
                dsid = dsid[2:] # remove first 00 from run number

            if dsid_select == "" :
                sample_dsids.append(dsid)
            else :
                dsids_to_select = dsid_select.split(",")
                for d in dsids_to_select :
                    if int(d) == int(dsid) :
                        sample_dsids.append(dsid)
                #if int(dsid_select) == int(dsid) :
                #    sample_dsids.append(dsid)
            

        sample_files = []

        if not is_data and len(tags) > 0 :
            for tag in tags :
                for dsid in sample_dsids :
                    for f in all_files :
                        if dsid in f and tag in f :
                            sample_files.append(f)

        else :
            for dsid in sample_dsids :
                for f in all_files :
                    if dsid in f :
                        sample_files.append(f)
                        break

        if len(sample_files) == 0 :
            print "ERROR [sample %s load] No loaded sample files (filelist = %s, H5 dir = %s)" % ( self._name, filelist_directory, h5_dir )
            sys.exit()

        if len(sample_files) != len(sample_dsids) :

            #if len(sample_files) == 2 and "mc16" in sample_files[0] :
            #    mc16a_versions = []
            #    mc16d_versions = []
            #    for sf in sample_files :
            #        if "mc16a" in sf : mc16a_versions.append(sf)
            #        elif "mc16d" in sf : mc16d_versions.append(sf)

            #    samples_ok = True
            #    if len(mc16a_versions) != 1 :
            #        samples_ok = False
            #        print "WARNING [samples %s load] There is not ==1 MC16A version of the file found (# found=%d)" % (self._name, len(mc16a_versions))
            #    if len(mc16d_versions) != 1 :
            #        samples_ok = False
            #        print "WARNING [samples %s load] There is not ==1 MC16D version of the file found (# found=%d)" % (self._name, len(mc16d_versions))

            #    if not samples_ok :
            #        sys.exit()

            print "WARNING [samples %s load] Number of files found (=%d) not equal to number of sample dsids (=%d)" % ( self._name, len(sample_files), len(sample_dsids) )
            n_f = len(sample_files)
            n_d = len(sample_dsids)
            #choice = raw_input(" >>> Print files and dsids and EXIT? [y/n] ")
            #if choice.lower() == 'y' :
            #    print "Loaded files:"
            #    for i, f in enumerate(sample_files) :
            #        print "[%03d/%03d] %s" % (i+1, n_f, f)
            #    print "Loaded dsids:"
            #    for i, d in enumerate(sample_dsids) :
            #        print "[%03d/%03d] %s" % (i+1, n_d, d)
            #    sys.exit()

        for d in sample_dsids :
            self._loaded_dsids.append(int(d))
        for f in sample_files :
            self._loaded_h5_files.append(f)
        self.h5dir = h5_dir
        self.filelistdir = filelist_directory

    def __str__(self) :
        out = "Sample    name = %s  displayname = %s  [from=(filelistdir=%s, h5dir=%s)]" % ( self.name, self.displayname, self.filelistdir, self.h5dir )
        return out

    @property
    def selection_file(self) :
        return self._selection_file
    @selection_file.setter
    def selection_file(self, val) :
        self._selection_file = val

    @property
    def selection_group(self) :
        return self._selection_group
    @selection_group.setter
    def selection_group(self, val) :
        self._selection_group = val

    def chain(self) :
        chunksize = 100000
        self.entries = 0
        with h5py.File(self.selection_file, 'r') as f :
            process_group = f[self.selection_group]
            for dsname in process_group :
                ds = process_group[dsname]
                for x in range(0, ds.size, chunksize) :
                    yield ds[x:x+chunksize]

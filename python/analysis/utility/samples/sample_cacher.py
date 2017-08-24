#!/usr/bin/env python

import os
import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.utils.utils as utils

import h5py
import numpy as np

class SampleCacher(object) :
    def __init__(self, cache_dir = "") :
        self._name = ""
        self.outdir = cache_dir
        self._selection_cut_str = ""
        self._selection_name = "" 
        self._sample_names = []
        self._samples_to_cache = [] 
        self._variables_to_keep = []
        self._fields = []

    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, val) :
        self._name = val

    @property
    def outdir(self) :
        return self._output_dir
    @outdir.setter
    def outdir(self, directory) :
        print "SampleCacher setting output directory to %s" % directory
        utils.mkdir_p(directory)
        self._output_dir = directory

    @property
    def samples(self) :
        return self._samples_to_cache
    @samples.setter
    def samples(self, input_samples ) :
        for s in input_samples :
            self._samples_to_cache.append(s)
            self._sample_names.append(s.name)

    @property
    def region(self) :
        return self._selection_name
    @region.setter
    def region(self, region) :
        self._selection_name = region.name
        self._selection_cut_str = region.tcut
        self.name = "selection_file_%s.hdf5" % region.name

    @property
    def selection(self) :
        return self._selection_name
    @selection.setter
    def selection(self, name) :
        self._selection_name = name

    @property
    def selectionstr(self) :
        return self._selection_cut_str
    @selectionstr.setter
    def selectionstr(self, tcut_str = "") :
        self._selection_cut_str = tcut_str

    @property
    def fields(self) :
        return self._fields
    @fields.setter
    def fields(self, fields_list) :
        fields_list = list(set(fields_list)) # remove duplicates
        self._fields = fields_list

    def __iter__(self) :
        """ iterate over the loaded samples """
        for s in self._samples_to_cache :
            yield s

    def __str__(self) :
        out = " *** SampleCacher ***\n"
        out += " > Samples:        %s\n" % ( ' , '.join(self._sample_names) )
        out += " > Selection:      (name=%s, cut=%s)\n" % ( self.selection, self.selectionstr )
        out += " > Cache dir:      %s\n" % ( self.outdir )
        out += " > Selection file: %s\n" % ( self.name )
        out += " > Fields:         %s" % ( self.fields )
        return out

    def find_var_idxs(self, tcut_str, sub) :
        start = 0
        while True :
            start = tcut_str.find(sub, start)
            if start == -1 : return
            yield start
            start += len(sub)

    def index_selection_string(self) :
        tcut = self.selectionstr
        tcut = tcut.replace("&&", " & ")
        tcut = tcut.replace("||", " | ")
        fields_order = []
        var_strings = []

        var_str_map = {}
        logic = ["&", "|"]
        for var in self.fields :
            if var in tcut :
                new_str = "(ds['%s']" % var
                var_strings.append(new_str)
                tcut = tcut.replace(var, "(ds['%s']" % var)
                occurrences = self.find_var_idxs(tcut, new_str) 
                #print tcut
                #print "  -> occurrences of %s = " % (new_str)
                #for occ in occurrences :
                #    print "       ", occ
                #var_str_map[new_str] = occurrences

                for idx in occurrences :
                    sub = ""
                    for i, c in enumerate(tcut[idx:]) :
                        if c in logic :
                            break
                        sub += c
                    substr_to_replace = sub
                    substr = substr_to_replace + ") "
                    tcut = tcut.replace(substr_to_replace, substr)

#        #print "before ", tcut
#        for vs, idxs in var_str_map.iteritems() :
#            print "vs = %s  idx = %s" % (vs, idxs)
#            for idx in idxs :
#                print idx
#                sub = ""
#                for i, c in enumerate(tcut[idx:]) :
#                    #print "  > C %s" % c
#                    if c in logic :
#                        break
#                    sub += c
#                substr_to_replace = sub
#                #print "SUB = %s"%sub
#                substr = substr_to_replace + ") "
#                #for l in logic :
#                #    substr = substr.replace(")%s" % l, ") %s" % l)
#                tcut = tcut.replace(substr_to_replace, substr)
        for l in logic :
            tcut = tcut.replace(")%s" % l, ") %s" % l)
                

        #tcut += ")"
        #print "after ", tcut

        #for i, vs in enumerate(var_strings) :
        #    idx = tcut.index(vs)
        #    sub = ""
        #    for i, c in enumerate(tcut[idx:]) :
        #        if c in logic :
        #            break
        #        sub += c
        #        
        #    substr_to_replace = sub
        #    substr = substr_to_replace +  ") "

        #    for l in logic :
        #        substr = substr.replace(")%s" % l, ") %s" % l)
        #    #for l in logic :
        #    #    substr = substr.replace("  )%s" % l, ") %s" % l)
        #    #for l in logic :
        #    #    substr = substr.replace(" ) %s" % l, ")  %s" % l)
        #    
        #    tcut = tcut.replace(substr_to_replace, substr)
        #    #if vs == var_strings[-1] :
        #    #    tcut += ")"

        return tcut
        

    def add_process_to_cache(self, process_group, sample) :
        relevant_vars = self.fields
        relevant_vars = list(set(relevant_vars))
        field_select_str = ",".join("'%s'" % v for v in relevant_vars)
        sub_file_no = 0
        for file in sample.h5_files :
            with h5py.File(file, 'r') as sample_file :
                set_ds = "ds = sample_file['superNt'][ %s ]" % field_select_str
                exec(set_ds)
                #print "len before %d "% len(ds)
                indices_select_str = self.index_selection_string()
                #print indices_select_str
                set_idx = "indices = np.array( %s )" % indices_select_str
                exec(set_idx)
                selected_dataset = ds[indices]
                #print "len after %d" % len(selected_dataset)
                sub_dataset_name = "dataset_%d" % sub_file_no
                out_ds = process_group.create_dataset(sub_dataset_name, shape=selected_dataset.shape, dtype=selected_dataset.dtype)
                out_ds[:] = selected_dataset
                sub_file_no += 1
                

    def cache(self) :
        """ main cache functionality here """

        output_directory = self.outdir
        if not output_directory.endswith("/") :
            output_directory += "/"
        full_filename = output_directory + "%s" % self.name

        if not os.path.isfile(full_filename) :
            with h5py.File(full_filename, 'w') as selection_file :
                name = self.selection
                selection_group = selection_file.create_group(name)
                selection_group.attrs['cut_string'] = self.selectionstr

                for sample in self.samples :
                    print "Caching %s" % sample.name
                    process_group = selection_group.create_group(sample.name)
                    self.add_process_to_cache(process_group, sample)
                    sample.selection_file = full_filename
                    sample.selection_group = "/%s/%s/" % ( str(selection_group.name), sample.name )
            return full_filename

        elif os.path.isfile(full_filename) :
            print "Found pre-cached selection file %s" % full_filename
            # check the current file for
            # 1) make sure that the selection definition is the same
            # 2) make sure that each of our samples is in  there
            # if (1) fails, don't try to be smart, just exit
            # if (2) fails (and (1) succeeds), just add the dataset
            # TODO add check for all the relevant variables
            with h5py.File(full_filename, 'a') as selection_file :
                name = self.selection
                print " > Looking for top level -> %s " % name
                found_top_level = False
                for top_level in selection_file :
                    if str(top_level) == name :
                        found_top_level = True
                        print"  %s in file!" % name
                        selection_group = selection_file["%s" % name]
                        cut_definition = selection_group.attrs['cut_string']
                        if cut_definition != self.selectionstr :
                            print "ERROR Cut definition for %s in selection file %s does not match!" % ( name, full_filename )
                            print "ERROR Expected selection : %s" % self.selectionstr
                            print "ERROR Selection in file  : %s" % cut_definition
                            sys.exit()

                if not found_top_level :
                    print "ERROR Did not find top level group %s for selection %s in file %s" % (self.selectionstr, full_filename)
                    sys.exit()

                print "Top level and selection seem ok! (n.b. did not check variable content)"

                selection_group = selection_file["%s" % name]
                print "Looking for selection group %s" % str(selection_group.name)
                group_keys = [str(g) for g in selection_group.keys()]
                for sample in self.samples :
                    process_group_name = sample.name
                    if process_group_name in group_keys :
                        print "Loading   > %s (from pre-existing group)" % sample.name
                        sample.selection_file = full_filename
                        sample.selection_group = "/%s/%s/" % ( str(selection_group.name), sample.name )
                    else :
                        print "Loading   > %s did not find in pre-existing group, adding it now" % sample.name
                        process_group = selection_group.create_group(sample.name)
                        self.add_process_to_cache(process_group, sample)
                        sample.selection_file = full_filename
                        sample.selection_group = "/%s/%s/" % ( str(selection_group.name), sample.name )
            return full_filename

#!/bin/env python

import os
import sys
import glob
import subprocess
from optparse import OptionParser

xrd_scope = "root://${ATLAS_XROOTD_CACHE}/"

analysis_release = "AnalysisBase,21.2.19,slc6"

out_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0301/mc/h5_test/"
log_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0301/mc/h5_test/"

def get_outfilename(filename) :

    out = filename.split("/")[-1]
    out = out.replace(".root", ".h5")

    return out

def get_number(fname) :

    if "mc16" in fname :
        f = fname.split("/")[-1]
        number = f.split("_")[1]
        return int(number)
    elif "Main" in fname :
        f = fname.split("/")[-1]
        number = f.split("_")[4]
        return int(number)

def main() :

    parser = OptionParser("condor conversion")
    parser.add_option("-i", "--input", help = "input dir", default = "")
    parser.add_option("-t", "--tag", help = "wildcard for file selection", default = "")
    parser.add_option("--dsid-start", help ="minimum dsid to consider", default = "")
    (options, args) = parser.parse_args()

    if options.input == "" :
        print "did not provide input files"
        sys.exit()

    files_to_convert = glob.glob("%s/*.root" % options.input)

    if options.tag != "" :
        tags = options.tag.split(",")
        tmp = []
        for f in files_to_convert :

            keep_file = True
            for tag in tags :
                if tag not in f :
                    keep_file = False

            if keep_file :
                tmp.append(f)
        files_to_convert = tmp

    if options.dsid_start != "" :
        tmp = []
        for f in files_to_convert :
            number = get_number(f)
            if number < int(options.dsid_start) : continue
            tmp.append(f)
        files_to_convert = tmp

    for f in files_to_convert :
        print f
    print 55 * '-'


    xrd_files = []
    for f in files_to_convert :
        f = os.path.abspath(f)
        f = xrd_scope + f
        xrd_files.append(f)

    n_files_to_convert = len(xrd_files)


    for isample, sample in enumerate(xrd_files) :
        script_name = "submit_condor_h5_converter.condor"
        exec_name = "run_h5_converter.sh"
        build_condor_script(script_name, exec_name)
        build_job_executable(exec_name, analysis_release)

        outfilename = get_outfilename(sample)

        descriptor = outfilename.replace(".h5", "")
        descriptor = "h5conversion_" + descriptor


        run_cmd = "ARGS="
        run_cmd += '"'
        run_cmd += ' %s ' % sample
        run_cmd += ' %s ' % outfilename
        run_cmd += '"'
        run_cmd += ' condor_submit %s ' % script_name
        run_cmd += ' -append "output = %s%s.out" ' % (log_dir, descriptor)
        run_cmd += ' -append "log = %s%s.log" ' % (log_dir, descriptor)
        run_cmd += ' -append "error = %s%s.err" ' % (log_dir, descriptor)

        print run_cmd
        subprocess.call(run_cmd, shell = True)

def build_condor_script(script_name, exec_name) :

    f = open(script_name, 'w')
    script = """universe = vanilla
+local=true
+site_local=false
+sdsc=false
+uc=false
executable = %s
arguments = $ENV(ARGS)
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
use_x509userproxy = True
notification = Never
queue
""" % (exec_name)

    f.write(script)
    f.close()

def build_job_executable(exec_name, release) :

    f = open(exec_name, 'w')
    script = """#!/bin/bash
infilename=${1}
outfilename=${2}
while (( "$#" )); do
    shift
done

echo "hostname:"
hostname
echo "whoami:"
whoami

echo "infilename = ${infilename}"
echo "outfilename = ${outfilename}"

work_dir=${PWD}
echo "work_dir: ${work_dir}"

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

lsetup fax
lsetup "asetup %s"


echo "calling: ttree2hdf5 ${infilename} -o ${outfilename}"
ttree2hdf5 ${infilename} -o ${outfilename}


""" % release

    f.write(script)
    f.close()

if __name__ == "__main__" :
    main()

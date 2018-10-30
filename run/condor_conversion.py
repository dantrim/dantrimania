#!/bin/env python

import os
import sys
import glob
import subprocess
import argparse

xrd_scope = 'root://${ATLAS_XROOTD_CACHE}/'
analysis_release = 'AnalysisBase,21.2.49'
out_dir = '/data/uclhc/uci/user/dantrim/ntuples/n0304/a_oct28/data/h5/'

def get_outfilename(filename) :

    '''
    Takes a path to a ROOT file, strips the path,
    and returns a string with the ".root" suffix
    replace with ".h5"

    Args:
        filename : full path to ROOT file
    Returns:
        string
    '''

    out = filename.split('/')[-1]
    out = out.replace('.root', '.h5')
    return out

def get_number(filename) :

    '''
    From an input filename, get the run number or
    DSID (if data or MC, resp). This assumes a specific
    file format: <syst>_<number>_mc16X.root, e.g.
        [MC] CENTRAL_410472_mc16a.root
        [DATA] CENTRAL_physics_Main_2016_310634.root

    Args:
        filename : string, full path to data file
    Returns:
        string
    '''

    if 'mc16' in filename :
        f = filename.split('/')[-1]
        number = f.split('_')[1]
        return int(number)
    elif 'Main' in filename :
        f = filename.split('/')[-1]
        number = f.split('_')[4]
        return int(number)
    else :
        print 'ERROR Failed to get DSID/run number associated with input "%s"' % filename
        sys.exit()

def build_condor_file(condor_filename, exec_name, xrd_files) :

    with open(condor_filename, 'w') as f :
        f.write('universe = vanilla\n')
        f.write('+local = true\n')
        f.write('+site_local = false\n')
        f.write('+sdsc = false\n')
        f.write('+uc = false\n')
        f.write('executable = %s\n' % exec_name)
        f.write('should_transfer_files = YES\n')
        f.write('when_to_transfer_output = ON_EXIT\n')
        f.write('use_x509userproxy = True\n')
        f.write('notification = Never\n')

        for ifile, xfile in enumerate(xrd_files) :

            log_base = '.'.join(xfile.split('/')[-1].split('.')[:-1])
            f.write('\n')
            arg_string = ' %s %s ' % (xfile, get_outfilename(xfile))
            f.write('arguments = %s\n' % arg_string)
            f.write('output = log_%s.out\n' % log_base)
            f.write('log = log_%s.log\n' % log_base)
            f.write('error = log_%s.err\n' % log_base)
            f.write('queue\n')

def build_executable(exec_name) :

    with open(exec_name, 'w') as f :
        f.write('#!/bin/bash\n\n\n')
        f.write('echo "----------- %s ------------"\n' % exec_name)
        f.write('hostname\n')
        f.write('echo "start: `date`"\n')
        f.write('input_filename=${1}\n')
        f.write('output_filename=${2}\n')
        f.write('while (( "$#" )); do\n')
        f.write('   shift\n')
        f.write('done\n')
        f.write('echo "input_filename   : ${input_filename}"\n')
        f.write('echo "output_filename  : ${output_filename}"\n')
        f.write('export PATH=/data/uclhc/uci/user/dantrim/n0303val/dantrimania/scripts/:${PATH}\n')
        f.write('export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase\n')
        f.write('source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh\n')
        f.write('lsetup fax\n')
        f.write('source /home/dantrim/dantrim_setup_scripts/setup_h5.sh\n')
        f.write('lsetup "root 6.04.16-x86_64-slc6-gcc49-opt --skipConfirm"\n')
        f.write('lsetup "lcgenv -p LCG_86 x86_64-slc6-gcc49-opt Python"\n')
        f.write('echo "type h5converter:"\n')
        f.write('type h5converter\n')
        f.write('echo "calling h5converter"\n')
        f.write('h5converter ${input_filename}\n')
        f.write('echo "done"\n')

def main() :

    global out_dir

    parser = argparse.ArgumentParser(description = 'Submit HDF5 conversion jobs to the CONDOR batch queue')
    parser.add_argument('-i', '--input', required = True,
        help = 'Provide input directory of .root files to be converted')
    parser.add_argument('-t', '--tag', default = '',
        help = 'Provide a wildcard for file selection (can be comma-separated-list)')
    parser.add_argument('--number-start', default = '',
        help = 'Provide a minimum run number to consider')
    args = parser.parse_args()

    pwd = str(os.getcwd())
    out_dir = os.path.abspath(out_dir)
    if pwd != out_dir :
        print 'ERROR You must call this script in the set output directory (=%s) (current_dir=%s)' % (out_dir, pwd)
        sys.exit()

    files_to_convert = glob.glob('%s/*.root' % args.input)
    if args.tag != '' :
        tags = args.tag.split(',')
        tmp = []
        for f in files_to_convert :
            keep_file = False
            for tag in tags :
                if tag in f :
                    keep_file = True
            if keep_file :
                tmp.append(f)
        files_to_convert = tmp

    if args.number_start != '' :
        tmp = []
        for f in files_to_convert :
            n = get_number(f)
            if int(n) < int(args.number_start) : continue
            tmp.append(f)
        files_to_convert = tmp

    xrd_files = []
    for f in files_to_convert :
        f = os.path.abspath(f)
        f = xrd_scope + f
        xrd_files.append(f)
    n_to_convert = len(xrd_files)

    condor_filename = 'h5_convert.condor'
    exec_name = 'run_h5_conversion.sh'
    build_condor_file(condor_filename, exec_name, xrd_files)
    build_executable(exec_name)

    cmd = 'condor_submit %s' % condor_filename

    subprocess.call(cmd, shell = True)

#____________________________
if __name__ == '__main__' :
    main()


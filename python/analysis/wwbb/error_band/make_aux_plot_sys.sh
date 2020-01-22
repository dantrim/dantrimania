#!/bin/bash

#for region in top_cr z_cr top_vr z_vr srIncNoDhh; do
#    echo " >>> ${region} <<< "
#    python gen_errors.py -r ${region} -v NN_d_hh > /dev/null &
#    python gen_errors.py -r ${region} -v HT2Ratio > /dev/null &
#    python gen_errors.py -r ${region} -v mt2_bb > /dev/null &
#    python gen_errors.py -r ${region} -v dRll > /dev/null &
#    python gen_errors.py -r ${region} -v dphi_ll --absval > /dev/null &
#    #python gen_errors.py -r ${region} -v NN_d_hh HT2Ratio mt2_bb dRll
#done
#
##for region in srSFNoDhh srDFNoDhh srSFNoDhhCloseCut srDFNoDhhCloseCut; do
##    echo " >>> ${region} <<< "
##    python gen_errors.py -r ${region} -v NN_d_hh
##done
#python gen_errors.py -r srSFNoDhh -v NN_d_hh > /dev/null &
#python gen_errors.py -r srDFNoDhh -v NN_d_hh > /dev/null &
#python gen_errors.py -r srSFNoDhhCloseCut -v NN_d_hh > /dev/null &
#python gen_errors.py -r srDFNoDhhCloseCut -v NN_d_hh > /dev/null &

python gen_errors.py -r srIncNoMbbDhh -v mbb > /dev/null &
python gen_errors.py -r srIncNoMllDhh -v mll > /dev/null &

#for region in top_cr z_cr top_vr z_vr srIncNoDhh; do
#    echo " >>> ${region} <<< "
#    #python gen_errors.py -r ${region} -v NN_d_hh
#    #python gen_errors.py -r ${region} -v HT2Ratio
#    #python gen_errors.py -r ${region} -v dRll
#    #python gen_errors.py -r ${region} -v mt2_bb
#    python gen_errors.py -r ${region} -v dphi_ll --absval
#done

#python gen_errors.py -r z_cr -v HT2Ratio #dRll
#python gen_errors.py -r top_vr -v mt2_bb dRll
#python gen_errors.py -r z_vr -v HT2Ratio
#python gen_errors.py -r srIncNoMbbDhh -v HT2Ratio mbb
#python gen_errors.py -r srSFNoDhh -v NN_d_hh > /dev/null &
#python gen_errors.py -r srDFNoDhh -v NN_d_hh > /dev/null &
#python gen_errors.py -r srSFNoDhhCloseCut -v NN_d_hh > /dev/null & 
#python gen_errors.py -r srDFNoDhhCloseCut -v NN_d_hh > /dev/null &
#python gen_errors.py -r srIncNoMllDhh -v mll


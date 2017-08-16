#!/bin/bash

export DANTRIM_ANA=${PWD}/..
export PYTHONPATH=${DANTRIM_ANA}:${PYTHONPATH}
export ON_BRICK="0"

hname=$( hostname )
if [[ $hname = "uclhc-1.ps.uci.edu" ]]; then 
    echo "Setting up python for the brick"
    export ON_BRICK="1"
    lsetup "lcgenv -p LCG_86 x86_64-slc6-gcc49-opt Python"
fi


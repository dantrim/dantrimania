import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d

##################################################################################
# additional variables / common variables
##################################################################################
additional_variables = ['nBJets', 'MT_1_scaled', 'mt2_llbb', 'mbb',
                        'l0_pt', 'l1_pt', 'HT2Ratio', 'dRll', 'dRbb', 'mt2_bb',
                        'nBLMJets', 'nBLSJets', 'nSJets']

##################################################################################
# sample definition
##################################################################################
filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.06
#lumi_factor = 100

# backgrounds
ttbar = sample.Sample("ttbar", "$t\\bar{t} \\times 1.03$")
ttbar.scalefactor = lumi_factor * 1.03
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#f6f5f0"
ttbar.load(filelist_dir + "ttbar", h5_dir_mc) 
loaded_samples.append(ttbar)

wt = sample.Sample("Wt", "$Wt$")# \\times 0.83$")
#wt = sample.Sample("WtHPP", "$Wt$ (H++)")# \\times 0.83$")
#wt = sample.Sample("WtAMC", "$Wt$ (aMC@NLO)")# \\times 0.83$")
wt.scalefactor = lumi_factor# * 0.83
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#698bae" 
#wt.load(filelist_dir + "WtAMC", h5_dir_mc)
#wt.load(filelist_dir + "WtHPP", h5_dir_mc)
wt.load(filelist_dir + "Wt", h5_dir_mc)
loaded_samples.append(wt)

ztt = sample.Sample("Ztt", "$Z \\rightarrow \\tau \\tau$")
ztt.scalefactor = lumi_factor
ztt.fillstyle = 0
ztt.linestyle = '-'
ztt.color = "#fecf90" 
ztt.load(filelist_dir + "zjets_sherpa_tt", h5_dir_mc)
loaded_samples.append(ztt)

zll = sample.Sample("Zll", "$Z \\rightarrow \\ell \ell$")
zll.scalefactor = lumi_factor
zll.fillstyle = 0
zll.linestyle = '-'
zll.color = "#d1b7a5" 
zll.load(filelist_dir + "zjets_sherpa_ll", h5_dir_mc)
loaded_samples.append(zll)

dib = sample.Sample("Diboson", "$VV \\rightarrow \\ell \\ell \\nu \\nu$")
dib.scalefactor = lumi_factor
dib.fillstyle = 0
dib.linestyle = '-'
dib.color = "#785e6f" 
dib.load(filelist_dir + "diboson_sherpa", h5_dir_mc)
loaded_samples.append(dib)

wjets = sample.Sample("Wjets", "$W + jets$")
wjets.scalefactor = lumi_factor
wjets.fillstyle = 0
wjets.linestyle = '-'
wjets.color = "#daadbb" 
wjets.load(filelist_dir + "wjets_sherpa", h5_dir_mc)
loaded_samples.append(wjets)

ttv = sample.Sample("ttV", "$t\\bar{t} + V$")
ttv.scalefactor = lumi_factor
ttv.fillstyle = 0
ttv.linestyle = '-'
ttv.color = "#b3e6fd" 
ttv.load(filelist_dir + "ttV", h5_dir_mc)
loaded_samples.append(ttv)

# drell-yan samples are contained in the Z+jets filelists
#dy = sample.Sample("DY", "Drell-Yan")
#dy.scalefactor = lumi_factor
#dy.fillstyle = 0
#dy.linestyle = '-'
#dy.color = "#ffd787" 
#dy.load(filelist_dir + "drellyan_sherpa", h5_dir_mc)
#loaded_samples.append(dy)

higgs = sample.Sample("higgs", "Higgs")
higgs.scalefactor = lumi_factor
higgs.fillstyle = 0
higgs.linestyle = '-'
higgs.color = '#b1f574'
higgs.load(filelist_dir + "higgs", h5_dir_mc)
loaded_samples.append(higgs)

# data
data = sample.Sample("data", "Data")
data.is_data = True
data.scalefactor = 1.0
data.fillstyle = 0
data.linestyle = '-'
data.color = 'k'
data.load(filelist_dir + "data_n0234", h5_dir_data)
loaded_samples.append(data)

##signals
#hh0 = sample.Sample("hhSM", "$hh$ SM ($\\sigma \\times$ 100)")
#hh0.is_signal = True
#hh0.scalefactor = lumi_factor * 0.06 * 100
#hh0.fillstyle = 0
#hh0.linestyle = '--'
#hh0.color = 'r'
#hh0.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '342053')
#loaded_samples.append(hh0)
#
#hh1 = sample.Sample("hh800", "X $800$ GeV ($\\sigma \\times$ 20)")
#hh1.is_signal = True
#hh1.scalefactor = lumi_factor * 20
#hh1.fillstyle = 0
#hh1.linestyle = '--'
#hh1.color = 'b'
#hh1.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '343775')
#loaded_samples.append(hh1)
#
#hh2 = sample.Sample("hh1000", "X $1000$ GeV ($\\sigma \\times$ 20)")
#hh2.is_signal = True
#hh2.scalefactor = lumi_factor * 20
#hh2.fillstyle = 0
#hh2.linestyle = '--'
#hh2.color = '#9cfd9d'
#hh2.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = "343777")
#loaded_samples.append(hh2)



#############################################################
# region definitions
#############################################################
logy_regions = []

isSFOS = "((( nMuons == 2 && l0_pt > 25 && l1_pt > 20 ) || ( nElectrons == 2 && l0_pt > 25 && l1_pt > 20 ))"# && mll < 81.2 && mll > 101.2)"#  && (l0_q * l1_q) < 0)"

isEE = "nElectrons==2"
isMM = "nMuons==2"
isSF = "nElectrons==2 ||  nMuons==2"
isDF = "(nElectrons==1 && nMuons==1)"
#isDFOS = "(nLeptons == 2 && nElectrons == 1 && nMuons == 1 && l0_pt > 25 && l1_pt > 20)" # && (l0_q * l1_q) < 0"
trigger = "(( year == 2015 && trig_pass2015 == 1 ) || ( year == 2016 && trig_pass2016update == 1 ))"

r = region.Region("wttest", "WWbb - CR$_{Wt}$")
r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && HT2Ratio>0.7 && dRll>1.2 " % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && dRll>1.2 && bj1_pt>40" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && dRll>0.9" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && dRll<0.9" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && HT2Ratio>0.8" % ( trigger, isDF, isSF )
loaded_regions.append(r)

r = region.Region("wtvrtest", "WWbb - VR$_{Wt}$")
r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && dRll<1.2" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && dRll>1.2" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb>80 && mbb<140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && dRll>0.9" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 &&  HT2Ratio>0.7 && HT2Ratio<0.8 && dRll>0.9" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && HT2Ratio<0.8 && dRll>0.9" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140) && HT2Ratio>0.7 && HT2Ratio<0.8 && dRll>0.9" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && (mbb>80 && mbb<140) && (mt2_llbb>80 && mt2_llbb<140) && dRll>0.9" % ( trigger, isDF, isSF )
loaded_regions.append(r)

r = region.Region("wtshape", "WWbb - $Wt$ shape")
r.tcut = "%s && (%s || %s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>200 && dRll>1.2" % ( trigger, isDF, isSF )
#r.tcut = "%s && (%s || %s) && nBJets==2  && mll>20 && l0_pt>25 && l1_pt>20 && mt2_bb>150 && (mbb<80 || mbb>140) && (mt2_llbb<80 || mt2_llbb>140)" % ( trigger, isDF, isSF )
loaded_regions.append(r)


r = region.Region("wwbbpre_wtbls", "WW$bb$-pre (BLS)")
#r.tcut = "%s && nBJets==1 && nBLSJets==2 && nSJets==1 && mll>20 && l0_pt>25 && l1_pt>20 && met>75 && HT2Ratio_bls<0.5 && HT2Ratio_bls>0.2 && dRll<0.9 && mt2_bb_bls>30" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && nBJets==1 && nBLSJets==2 && nSJets==1 && mll>20 && l0_pt>25 && l1_pt>20 && met>75 && HT2Ratio_bls<0.5 && mbb_bls>40 && mbb_bls<100 && dRll<0.9" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && nBJets==1 && nBLSJets==2 && nSJets==1 && mll>20 && l0_pt>25 && l1_pt>20 && met>75 && dphi_ll>-0.5 && dphi_ll<0.5 && mbb_bls>40 && mbb_bls<100 && dRll<0.9" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && (l_flav==2 || l_flav==3) && nBJets==1 && nBLSJets==2 && nSJets==1 && mll>20 && l0_pt>25 && l1_pt>20 && HT2Ratio_bls>0.6 && HT2Ratio_bls<0.8 && dRll<0.9  && mt2_llbb_bls>80" % ( trigger )#,)isSF, isDF) #, trigger)
r.tcut = "%s && (%s && nBJets==1 && nBLSJets==2 && nSJets==1 && mll>20 && l0_pt>25 && l1_pt>20 && (dphi_met_ll>1.5 || dphi_met_ll<-1.5)" % ( trigger, isDF )

loaded_regions.append(r)

r = region.Region("wwbbpre_wtblm", "WW$bb$-pre (BLM)")
#r.tcut = "%s && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && HT2Ratio_bls>0.8 && dRll<0.9 && mt2_bb_blm>120 && mt2_bb_blm<150 && (dphi_met_ll<-0.5 || dphi_met_ll>0.5)" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && met>75 && HT2Ratio_blm<0.5 && HT2Ratio_blm>0.2 && dRll<0.9 && mt2_bb_blm>30" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20" % ( trigger )#,)isSF, isDF) #, trigger)
r.tcut = "%s && isDF==1 && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && dRll<0.9 && HT2Ratio_blm<0.8" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && isDF==1 && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && dRll<0.9 && HT2Ratio_blm<0.8 && HT2Ratio_blm>0.5" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && isDF==1 && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && dRll<0.9 && met>75  && HT2Ratio_blm<0.8 && HT2Ratio_blm>0.5" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && dRll<0.9 && met>75 && HT2Ratio_blm>0.2 && HT2Ratio_blm<0.8" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "%s && (l_flav==2 || l_flav==3) && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && HT2Ratio_blm>0.8 && dRll<0.9" % ( trigger )#,)isSF, isDF) #, trigger)
loaded_regions.append(r)

###################################################################
# ttbar regions
r = region.Region("wwbb_crtt", "WW$bb$ - CR$_{t\\bar{t}}$")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && dRll<2.0 && HT2Ratio<0.8 && HT2Ratio>0.2" % ( trigger )
loaded_regions.append(r)

r = region.Region("wwbb_vrtt1", "WW$bb$ - VR$_{t\\bar{t}}^{H_{T2}^{R}}$")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && dRll<2.0 && HT2Ratio>0.8" % ( trigger )
loaded_regions.append(r)

r = region.Region("wwbb_vrtt2", "WW$bb$ - VR$_{t\\bar{t}}^{\\Delta R_{\\ell \\ell}}$")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll<0.9 && HT2Ratio<0.8 && HT2Ratio>0.2" % ( trigger )
loaded_regions.append(r)


#auto blind
if "sr" in selected_region.lower() :
    del data
    data = None

#############################################################
# plots
#############################################################
variables = {}
##variables["HT2Ratio"] = { "wwbbpre_wtbls" : [0.005, 0.98, 1.0] } # if a 4th argument is given, override automatic setting of y-max
##variables["HT2Ratio"] =     { "wwbbpre_wtbls" : [0.05, 0.0, 1.0] , "vrht2ratio" : [0.03, 0.2, 0.8] , "vrtt0" : [0.05, 0.0, 1.0] }
##variables["HT2Ratio_bls"] =     { "wwbbpre_wtbls" : [0.02, 0.2, 0.4] , "vrht2ratio" : [0.01, 0.8, 1.0] , "vrtt0" : [0.05, 0.0, 1.0] }
#variables["HT2Ratio_bls"] =     { "wwbbpre_wtbls" : [0.05, 0.0, 1.0] , "vrht2ratio" : [0.01, 0.8, 1.0] , "vrtt0" : [0.05, 0.0, 1.0] }
#variables["nBJets"] =           { "wwbbpre_wtbls" : [1, 0, 6]        , "vrht2ratio" : [1, 0, 6]       , "vrtt0" : [1, 0, 5] }
#variables["dRll"] =             { "wwbbpre_wtbls" : [0.2, 0, 5]      , "vrht2ratio" : [0.05, 0.9, 2.0]    , "vrtt0" : [0.03, 0, 0.9] }
##variables["dRll"] =            { "wwbbpre_wtbls" : [0.1, 0, 5]      , "vrht2ratio" : [0.05, 0.0, 0.9]    , "vrtt0" : [0.03, 0, 0.9] }
#variables["MT_1_scaled_bls"] =  { "wwbbpre_wtbls" : [40, 0, 1500]    , "vrht2ratio" : [40, 0, 1500]    , "vrtt0" : [40, 0, 1500] }
#variables["mt2_llbb_bls"] =     { "wwbbpre_wtbls" : [10, 60, 400]    , "vrht2ratio" : [2, 90, 140]     , "vrtt0" : [2, 90, 140] }
#variables["dRbb_bls"] =         { "wwbbpre_wtbls" : [0.1, 0, 6]      , "vrht2ratio" : [0.1, 0, 6]      , "vrtt0" : [0.1, 0, 6] }
#variables["l0_pt"] =            { "wwbbpre_wtbls" : [10, 0, 300]     , "vrht2ratio" : [10, 0, 300]     , "vrtt0" : [10, 0, 300] }
#variables["l1_pt"] =            { "wwbbpre_wtbls" : [10, 0, 200]     , "vrht2ratio" : [10, 0, 200]     , "vrtt0" : [10, 0, 200] }
#variables["mbb_bls"] =          { "wwbbpre_wtbls" : [10, 0, 600]     , "vrht2ratio" : [2, 100,140]     , "vrtt0" : [2, 100, 140] }
#variables["mt2_bb_bls"] =       { "wwbbpre_wtbls" : [10, 0, 250] }
#variables["nBLSJets"] =         { "wwbbpre_wtbls" : [1, 0, 6] }
#variables["nBLMJets"] =         { "wwbbpre_wtbls" : [1, 0, 6] }
#variables["mll"] =              { "wwbbpre_wtbls" : [10, 20, 500] }
#variables["abs(dphi_ll)"] =     { "wwbbpre_wtbls" : [0.1, 0, 3.2] }
##variables["abs(dphi_ll)"] =     { "wwbbpre_wtbls" : [0.1, 0, 3.2] }
#variables["abs(dphi_met_ll)"] = { "wwbbpre_wtbls" : [0.1, 0, 3.2] }
#variables["abs(dphi_bj0_ll)"] = { "wwbbpre_wtbls" : [0.1, 0, 3.2] }
#variables["abs(dphi_bj0_l0)"] = { "wwbbpre_wtbls" : [0.1, 0, 3.2] }
#variables["met"] =              { "wwbbpre_wtbls" : [10, 0, 400] }

#variables["HT2Ratio"] =         { "wttest" : [0.05, 0.0, 1.0],      "wtvrtest" : [0.06, 0.7, 1] }
variables["HT2Ratio"] =         { "wttest" : [0.03, 0.7, 1.0],      "wtvrtest" : [0.06, 0.7, 1] }
variables["nBJets"] =           { "wttest" : [1, 0, 5],             "wtvrtest" : [1, 0, 5] }
variables["dRll"] =             { "wttest" : [0.5, 0, 5] ,          "wtvrtest" : [0.12, 0, 1.2] }
variables["MT_1_scaled"] =      { "wttest" : [80, 0, 1500],         "wtvrtest" : [100, 0, 1500] }
variables["mt2_llbb"] =         { "wttest" : [40, 0, 800],          "wtvrtest" : [40, 0, 500] }
variables["dRbb"] =             { "wttest" : [0.5, 0, 5],           "wtvrtest" : [0.5, 0, 5] }
variables["l0_pt"] =            { "wttest" : [20, 0, 400],          "wtvrtest" : [40, 0, 400] }
variables["l1_pt"] =            { "wttest" : [9, 0, 180],            "wtvrtest" : [18, 0, 180] }
variables["mbb"] =              { "wttest" : [40, 0, 600],          "wtvrtest" : [80, 0, 600] }
variables["mt2_bb"] =           { "wttest" : [40, 0, 600],          "wtvrtest" : [40, 0, 500] }
variables["mll"] =              { "wttest" : [40, 0, 500],          "wtvrtest" : [10, 0, 200] }
variables["abs(dphi_ll)"] =     { "wttest" : [0.4, 0, 3.2],         "wtvrtest" : [0.4, 0, 3.2] }
variables["abs(dphi_bb)"] =     { "wttest" : [0.4, 0, 3.2],         "wtvrtest" : [0.4, 0, 3.2] }
variables["abs(dphi_met_ll)"] = { "wttest" : [0.4, 0, 3.2],         "wtvrtest" : [0.4, 0, 3.2] }
variables["abs(dphi_bj0_ll)"] = { "wttest" : [0.4, 0, 3.2],         "wtvrtest" : [0.4, 0, 3.2] }
variables["abs(dphi_bj0_l0)"] = { "wttest" : [0.4, 0, 3.2],         "wtvrtest" : [0.4, 0, 3.2] }
variables["met"] =              { "wttest" : [30, 0, 600],          "wtvrtest" : [40, 0, 400] }
variables["bj0_pt"] =           { "wttest" : [20, 0, 400],          "wtvrtest" : [20, 0, 400] }
variables["bj1_pt"] =           { "wttest" : [15, 0, 300],          "wtvrtest" : [15, 0, 300] }
variables["avgMuDataSF"] =      { "wttest" : [1, 0, 45] }

#variables["HT2Ratio"] =         { "wwbb_crtt" : [0.03, 0.2, 0.8] }
#variables["nBJets"] =           { "wwbb_crtt" : [1, 0, 5] }
#variables["dRll"] =             { "wwbb_crtt" : [0.055, 0.9, 2] }
#variables["MT_1_scaled"] =      { "wwbb_crtt" : [20, 0, 600] }
#variables["mt2_llbb"] =         { "wwbb_crtt" : [5, 90, 140] }
#variables["dRbb"] =             { "wwbb_crtt" : [0.5, 0, 5] }
#variables["l0_pt"] =            { "wwbb_crtt" : [10, 0, 200] }
#variables["l1_pt"] =            { "wwbb_crtt" : [5, 0, 100] }
#variables["mbb"] =              { "wwbb_crtt" : [2, 100, 140] }
#variables["mt2_bb"] =           { "wwbb_crtt" : [10, 0, 150] }
#variables["mll"] =              { "wwbb_crtt" : [8, 0, 160] }
#variables["abs(dphi_ll)"] =     { "wwbb_crtt" : [0.4, 0, 3.2] }
#variables["abs(dphi_bb)"] =     { "wwbb_crtt" : [0.4, 0, 3.2] }
#variables["abs(dphi_met_ll)"] = { "wwbb_crtt" : [0.4, 0, 3.2] }
#variables["abs(dphi_bj0_ll)"] = { "wwbb_crtt" : [0.4, 0, 3.2] }
#variables["abs(dphi_bj0_l0)"] = { "wwbb_crtt" : [0.4, 0, 3.2] }
#variables["met"] =              { "wwbb_crtt" : [10, 0, 200] }

#variables["HT2Ratio"] =         { "wwbb_vrtt2" : [0.03, 0.2, 0.8] }
#variables["nBJets"] =           { "wwbb_vrtt2" : [1, 0, 5] }
#variables["dRll"] =             { "wwbb_vrtt2" : [0.045, 0.0, 0.9] }
#variables["MT_1_scaled"] =      { "wwbb_vrtt2" : [20, 0, 600] }
#variables["mt2_llbb"] =         { "wwbb_vrtt2" : [5, 90, 140] }
#variables["dRbb"] =             { "wwbb_vrtt2" : [0.5, 0, 5] }
#variables["l0_pt"] =            { "wwbb_vrtt2" : [10, 0, 200] }
#variables["l1_pt"] =            { "wwbb_vrtt2" : [5, 0, 100] }
#variables["mbb"] =              { "wwbb_vrtt2" : [2, 100, 140] }
#variables["mt2_bb"] =           { "wwbb_vrtt2" : [10, 0, 150] }
#variables["mll"] =              { "wwbb_vrtt2" : [8, 0, 160] }
#variables["abs(dphi_ll)"] =     { "wwbb_vrtt2" : [0.4, 0, 3.2] }
#variables["abs(dphi_bb)"] =     { "wwbb_vrtt2" : [0.4, 0, 3.2] }
#variables["abs(dphi_met_ll)"] = { "wwbb_vrtt2" : [0.4, 0, 3.2] }
#variables["abs(dphi_bj0_ll)"] = { "wwbb_vrtt2" : [0.4, 0, 3.2] }
#variables["abs(dphi_bj0_l0)"] = { "wwbb_vrtt2" : [0.4, 0, 3.2] }
#variables["met"] =              { "wwbb_vrtt2" : [10, 0, 200] }

nice_names = {}
nice_names["HT2Ratio_bls"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["MT_1_scaled_bls"] = ["M$_{T1}$", "GeV"]
nice_names["mt2_llbb_bls"] = ["$m_{T2}^{\\ell \\ell bb}$", "GeV"]
nice_names["l0_pt"] = ["Lead lepton $p_{T}$", "GeV"]
nice_names["l1_pt"] = ["Sub-lead lepton $p_{T}$", "GeV"]
nice_names["mt2_bb_bls"] = ["$m_{T2}^{bb}", "GeV"]
nice_names["HT2Ratio_bls"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["MT_1_scaled_bls"] = ["M$_{T1}$", "GeV"]
nice_names["mt2_llbb_bls"] = ["$m_{T2}^{\\ell \\ell bb}$", "GeV"]
nice_names["l0_pt"] = ["Lead lepton $p_{T}$", "GeV"]
nice_names["l1_pt"] = ["Sub-lead lepton $p_{T}$", "GeV"]
nice_names["mt2_bb_bls"] = ["$m_{T2}^{bb}$", "GeV"]

# load the plots 
for var, bounds in variables.iteritems() :
    if selected_region not in bounds :
        print "ERROR selected region (=%s) is not defined in configured variables" % ( selected_region )
        sys.exit()
    logy = False
    if selected_region in logy_regions or do_logy :
        logy = True
    p = hist1d.RatioCanvas(logy = logy)
    if "abs(" in var :
        var = var.replace("abs(", "").replace(")","")
        p.absvalue = True
    p.vartoplot = var
    p.bounds = bounds[selected_region]
    name = var.replace("[","").replace("]","").replace("(","").replace(")","")
    p.name = name
    y_label_unit = ""
    if var in nice_names :
        if len(nice_names[var]) == 2 :
            y_label_unit = nice_names[var][1]
    y_label_unit = str(bounds[selected_region][0]) + " " + y_label_unit
    x_label = var
    y_label = "Events / %s" % y_label_unit
    if var in nice_names :
        x_label = nice_names[var][0]
    p.labels = [x_label, y_label]

    if selected_region in logy_regions or do_logy :
        p.logy = True

    p.build_ratio()

    loaded_plots.append(p)

    

import sys

from dantrimania.python.analysis.utility.plotting.plot1d import plot1d
import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region

##############################################################################
# additional variables
##############################################################################

##################################################################################
# sample definition
##################################################################################
filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/j_dec7_tight/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/j_dec7_tight/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/k_jan6_bsys/mc/h5_central/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/k_jan6_bsys/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.06
#lumi_factor = 100

# backgrounds
#ttbar = sample.Sample("ttbar", "$t\\bar{t}$")# \\times 0.96$")
ttbar = sample.Sample("ttbar", "$t\\bar{t} \\times 0.96$")
#ttbar = sample.Sample("ttbar", "$t\\bar{t}$ (PP8)")# \\times 0.97$")
ttbar.scalefactor = lumi_factor# * 0.96# * 1.10# * 0.92
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#f6f5f0"
ttbar.load(filelist_dir + "ttbar", h5_dir_mc) 
#ttbar.load(filelist_dir + "ttbar_pp8", h5_dir_mc) 
loaded_samples.append(ttbar)

#wt = sample.Sample("WtAMC", "$Wt$ (AMC)")# \\times 0.94$")
wt = sample.Sample("Wt", "$Wt \\times 1.13$")# \\times 0.76$ (nom)")
#wt = sample.Sample("Wt", "$Wt$")# \\times 1.13$")# \\times 0.76$ (nom)")
wt.scalefactor = lumi_factor #* 1.13
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#698bae" #wt.load(filelist_dir + "Wt", h5_dir_mc)
wt.load(filelist_dir + "Wt", h5_dir_mc)
#wt.load(filelist_dir + "WtAMC", h5_dir_mc)
loaded_samples.append(wt)
###wtDS = sample.Sample("WtDS", "$Wt$ (DS)")
###wtDS.scalefactor = lumi_factor
###wtDS.fillstyle = 0
###wtDS.linestyle = '-'
###wtDS.color = "#698bae"
###wtDS.load(filelist_dir + "singletop_DS", h5_dir_mc)
###loaded_samples.append(wtDS)
##
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
##
##wjets = sample.Sample("Wjets", "$W + jets$")
##wjets.scalefactor = lumi_factor
##wjets.fillstyle = 0
##wjets.linestyle = '-'
##wjets.color = "#daadbb" 
##wjets.load(filelist_dir + "wjets_sherpa", h5_dir_mc)
##loaded_samples.append(wjets)
##
ttv = sample.Sample("ttV", "$t\\bar{t} + V$")
ttv.scalefactor = lumi_factor
ttv.fillstyle = 0
ttv.linestyle = '-'
ttv.color = "#b3e6fd" 
ttv.load(filelist_dir + "ttV", h5_dir_mc)
loaded_samples.append(ttv)
##
### drell-yan samples are contained in the Z+jets filelists
###dy = sample.Sample("DY", "Drell-Yan")
###dy.scalefactor = lumi_factor
###dy.fillstyle = 0
###dy.linestyle = '-'
###dy.color = "#ffd787" 
###dy.load(filelist_dir + "drellyan_sherpa", h5_dir_mc)
###loaded_samples.append(dy)
##
### data
data = sample.Sample("data", "Data")
data.is_data = True
data.scalefactor = 1.0
data.fillstyle = 0
data.linestyle = '-'
data.color = 'k'
data.load(filelist_dir + "data_n0234", h5_dir_data)
#loaded_samples.append(data)

#signals
#hh0 = sample.Sample("hhSM", "$hh$ SM")
#hh0.is_signal = True
#hh0.scalefactor = lumi_factor * 0.06# * 100
#hh0.fillstyle = 0
#hh0.linestyle = '--'
#hh0.color = '#fa0f00'
#hh0.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '342053')
#loaded_samples.append(hh0)
#
#hh3 = sample.Sample("hh600", "X $600$ GeV")
#hh3.is_signal = True
#hh3.scale_factor = lumi_factor * 20
#hh3.fillstyle = 0
#hh3.linestyle = "--"
#hh3.color = '#ff5900'
#hh3.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = "343772")
#loaded_samples.append(hh3)
#
#hh1 = sample.Sample("hh800", "X $800$ GeV")
#hh1.is_signal = True
#hh1.scalefactor = lumi_factor * 20
#hh1.fillstyle = 0
#hh1.linestyle = '--'
#hh1.color = '#ffb900'
#hh1.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '343775')
#loaded_samples.append(hh1)
#
signal_mass = 1000
dsid_dict = {}
masses="""343764.260
343766.300
343769.400
343771.500
343772.600
343773.700
343774.750
343775.800
343776.900
343777.1000
343778.1100
343779.1200
343780.1300
343781.1400
343782.1500
343783.1600
343784.1800
343785.2000
343786.2250
343787.2500
343788.2750
343789.3000
"""
for f in masses.split() :
    x = f.split(".")
    mass = x[1]
    dsid = x[0]
    dsid_dict[int(mass)] = dsid

hh2 = sample.Sample("hh%d"%signal_mass, "X $%d$ GeV" % signal_mass)
hh2.is_signal = True
hh2.scalefactor = lumi_factor #* 20
hh2.fillstyle = 0
hh2.linestyle = '--'
hh2.color = '#0cf4ea'
hh2.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = dsid_dict[signal_mass])
loaded_samples.append(hh2)

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
trigger_single = "(( year == 2015 && ( (trig_pass2015==1) || (trig_e60_lhmedium==1 || trig_mu20_iloose_L1MU15))) || ( year == 2016 && ( (trig_pass2016update==1) || (trig_e60_lhmedium_nod0==1 || trig_mu26_ivarmedium==1))))"
trigger = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ))"

r = region.Region("wwbbpre", "WW$bb$ pre-selection")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20" % (trigger)
loaded_regions.append(r)

r = region.Region("wwbbpre2", "WW$bb$-pre")
#r.tcut = "%s && nBJets==1 && nBLSJets==2 && nSJets==1 && mll>20 && l0_pt>25 && l1_pt>20 && mbb_bls>80 && mbb_bls<140" % ( trigger )#,)isSF, isDF) #, trigger)
#r.tcut = "nBJets==2 && mll>20"
r.tcut = "nBJets==2 && mll>20 && mt2_bb>200"
#r.tcut = "nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20"
#r.tcut = "(%s) && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20" % (trigger_single)
#r.tcut = "(%s) && nBJets==2 && mll>20" % (trigger_single)
#r.tcut = "%s && nBJets==2 && mll>20" % trigger
#r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20" % trigger
loaded_regions.append(r)

## CR ttbar
r = region.Region("crtt", "CR-$t\\bar{t}$")
r.tcut = "%s && nBJets==2 && mll>20  && mbb>100 && mbb<140 && mt2_llbb>100 && mt2_llbb<140 && dRll>1.5 && dRll<3.0 && HT2Ratio>0.4 && HT2Ratio<0.6" % ( trigger )
#r.tcut = "%s && nBJets==2 && mll>20  && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && dRll<1.5 && HT2Ratio>0.6 && HT2Ratio<0.8" % ( trigger )

#r.tcut = "%s && nBJets==2 && mll>20  && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll<0.9 && HT2Ratio>0.6 && HT2Ratio<0.8" % ( trigger )
#r.tcut = "%s && nBJets==2 && mll>20  && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && dRll<2.0 && HT2Ratio<0.8 && HT2Ratio>0.2 && mt2_bb>50" % ( trigger )
#r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && dRll<2.0 && HT2Ratio<0.8 && HT2Ratio>0.2" % ( trigger )
loaded_regions.append(r)

r = region.Region("vrtt", "VR-$t\\bar{t}$")
r.tcut = "%s && nBJets==2 && mll>20  && mbb>100 && mbb<140 && mt2_llbb>100 && mt2_llbb<140 && dRll>0.9 && dRll<1.5 && HT2Ratio>0.6 && HT2Ratio<0.8" % ( trigger )
loaded_regions.append(r)

r = region.Region("vrdrll", "VR$_{Top}^{dRll}$")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll<0.9 && HT2Ratio<0.8 && HT2Ratio>0.2" % ( trigger )
loaded_regions.append(r)

r = region.Region("vrht2ratio", "VR$_{Top}^{HT2Ratio}$")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && dRll<2.0 && HT2Ratio>0.8" % ( trigger )
loaded_regions.append(r)


#r = region.Region("srlike", "SR")
#r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll<0.9 && HT2Ratio>0.8 && mt2_bb>150" % ( trigger )
#loaded_regions.append(r)

r = region.Region("crwt", "CR-$Wt$")
r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>150 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>120 && HT2Ratio>0.8 && dRll<1.5" % (trigger)
loaded_regions.append(r)

r = region.Region("vrwt", "VR-$Wt$")
r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>120 && HT2Ratio>0.8 && dRll<1.5" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && dRll<2.0 && HT2Ratio>0.5 && mt2_bb>150" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && dRll<0.9 && mt2_bb>150" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && dRll>0.9 && mbb>100 && mbb<140 && mt2_bb>150" % ( trigger )
#r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && mt2_bb>150 && HT2Ratio>0.7 && dRll>0.9" % ( trigger ) 
#r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>140 && mt2_llbb>140 && HT2Ratio>0.7 && mt2_bb>150 && dRll<1.2" % ( trigger )
#r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>140 && (mt2_llbb<90 || mt2_llbb>140) && HT2Ratio>0.7 && mt2_bb>150 && dRll<1.2" % ( trigger )
loaded_regions.append(r)

r = region.Region("sr_test", "SR-Test")
lower=0.8 *  signal_mass 
upper=1.1 * signal_mass 
r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>100 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9 && MT_1_scaled>%.2f && MT_1_scaled<%.2f" % (trigger, lower, upper)
#r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>90 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9 && mt2_bb>130 && met>200" % ( trigger )
loaded_regions.append(r)

#r = region.Region("sr_test", "SR-Test")
#r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>100 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9 && mt2_bb>150" % (trigger)
#loaded_regions.append(r)

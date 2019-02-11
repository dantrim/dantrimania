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
filelist_dir = "/data/uclhc/uci/user/dantrim/n0301val/susynt-read/filelists/"
filelist_dir_data = "/data/uclhc/uci/user/dantrim/n0302val/susynt-read/filelists/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
filelist_dir_data = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/data/h5/"


h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/r_aug_27_nn/mc/h5/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/t_sep9_nn/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/r_aug_27_nn/data/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/t_sep9_nn/data/h5/"
h5_dir_sig = "/data/uclhc/uci/user/dantrim/n0234val/my_reco_hh/"
h5_dir_sig = h5_dir_mc

filelist_dir = "/data/uclhc/uci/user/dantrim/n0306val/susynt-read/filelists/"
filelist_dir_data = "/data/uclhc/uci/user/dantrim/n0306val/susynt-read/filelists/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0304/a_oct28/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0304/a_oct28/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0304/b_nov11/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0304/b_nov11/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0304/c_nov12/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0304/c_nov12/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/mc/mc16a_nom/h5_test/"
h5_dir_mc = '/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/mc/mc16a_sys/h5/'
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/mc/mc16a_nom/h5_test/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0306/b_dec12/mc/mc16a/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/b_dec12/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.24
lumi_factor = 138.6
#lumi_factor = 36.24
#lumi_factor = 80.0
#lumi_factor = 78.5
#lumi_factor = 43.6

#tags = ["mc16a"]#, "mc16d"] #, "mc16d"]
#tags = ['mc16a', 'mc16d', 'mc16e']
tags = ['mc16a']
#tags = ["mc16a"]
#tags = ["mc16a", "mc16d"]

which_data = '1516'
sf_vals_tt = { '1516' : 1.00, '151617' : 1.00 }
sf_vals_wt = { '1516' : 1.00, '151617' : 1.00 }
sf_vals_tt = { '1516' : 1.00, '151617' : 1.00 }
sf_vals_wt = { '1516' : 1.00, '151617' : 1.00 }
#sf_vals_tt = { '1516' : 1.02, '151617' : 1.00 }
#sf_vals_wt = { '1516' : 0.40, '151617' : 1.00 }
#sf_vals_tt = { '1516' : 1.02, '151617' : 1.00 }
#sf_vals_wt = { '1516' : 0.40, '151617' : 0.41 }

# backgrounds
#top = sample.Sample("topDS", "Top (DS)")
#top.scalefactor = lumi_factor * 0.93
#top.fillstyle = 0
#top.linestyle = '-'
#top.color = "#0057FF"
#top.load(filelist_dir + "topDS_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(top)


ttbar = sample.Sample("ttbar", "$t\\bar{t}$") # \\times 0.95$")
#ttbar = sample.Sample("ttbar", "$t\\bar{t} \\times %s$" % str(sf_vals_tt[which_data]))
ttbar.scalefactor = lumi_factor #* 0.93 #* sf_vals_tt[which_data]
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#0057FF"
#ttbar.color = "#3f88c5"
ttbar.load(filelist_dir + "ttbar_mc16a", h5_dir_mc, tags = tags)
loaded_samples.append(ttbar)

#wt = sample.Sample("WtDRFull", "$Wt$ (DR)") #  \\times 0.35$")
##wt = sample.Sample("WtPP8Dil", "$Wt  \\times %s$" % str(sf_vals_wt[which_data]))
#wt.scalefactor = lumi_factor #* 0.35 #* sf_vals_wt[which_data]
#wt.fillstyle = 0
#wt.linestyle = '-'
#wt.color = "#008AFF"
##wt.color = "#e94f37"
#wt.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = ['mc16a', 'mc16d', 'mc16e'])
##wt.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(wt)

#wt = sample.Sample("WtDS", "$Wt$ (DS)")# \\times 0.45$")
wt = sample.Sample("WtDSFull", "$Wt$ (DS)")# \\times 0.45$")
wt.scalefactor = lumi_factor# * 0.45
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#e94f37"
#wt.load(filelist_dir + "WtDS_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])#, tags = tags)
wt.load(filelist_dir + "WtDS_mc16a", h5_dir_mc, tags = ['mc16a', 'mc16d', 'mc16e'])#, tags = tags)
loaded_samples.append(wt)

zjets = sample.Sample("Zjets", "$Z$+jets")
zjets.scalefactor = lumi_factor
zjets.fillstyle = 0
zjets.linestyle = '-'
zjets.color = "#FF0000"
#zjets.color = "#6e8387"
zjets.load(filelist_dir + "zjets_sherpa_mc16a", h5_dir_mc, tags = tags)
loaded_samples.append(zjets)

#zee = sample.Sample("Zee", "$Z\\rightarrow ee$")
#zee.scalefactor = lumi_factor
#zee.color = "#CAD2C5"
#zee.load(filelist_dir + "zjets_ee", h5_dir_mc, tags = tags)
#loaded_samples.append(zee)
#
#zmm = sample.Sample("Zmm", "$Z\\rightarrow \\mu\\mu$")
#zmm.scalefactor = lumi_factor
#zmm.color = "#52796F"
#zmm.load(filelist_dir + "zjets_mm", h5_dir_mc, tags = tags)
#loaded_samples.append(zmm)
#
#ztt = sample.Sample("Ztt", "$Z\\rightarrow \\tau\\tau$")
#ztt.scalefactor = lumi_factor
#ztt.color = "#2F3E46"
#ztt.load(filelist_dir + "zjets_tt", h5_dir_mc, tags = tags)
#loaded_samples.append(ztt)
#
#dee = sample.Sample("DYee", "$DY (ee)$")
#dee.scalefactor = lumi_factor
#dee.color = "#83B5D1"
#dee.load(filelist_dir + "drellyan_ee", h5_dir_mc, tags = tags)
#loaded_samples.append(dee)
#
#dmm = sample.Sample("DYmm", "$DY (\\mu\\mu)$")
#dmm.scalefactor = lumi_factor
#dmm.color = "#726E97"
#dmm.load(filelist_dir + "drellyan_mm", h5_dir_mc, tags = tags)
#loaded_samples.append(dmm)
#
#dtt = sample.Sample("DYtt", "$DY (\\tau\\tau)$")
#dtt.scalefactor = lumi_factor
#dtt.color = "#673C45"
#dtt.load(filelist_dir + "drellyan_tt", h5_dir_mc, tags = tags)
#loaded_samples.append(dtt)

higgs = sample.Sample("higgs", "Single-higgs")
higgs.scalefactor = lumi_factor
higgs.fillstyle = 0
higgs.linestyle = '-'
higgs.color = 'b'
higgs.load(filelist_dir + "single_higgs_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(higgs)
#
#
#
##zee = sample.Sample("zee", "$Z\\rightarrow ee$")
##zee.scalefactor = lumi_factor
##zee.fillstyle = 0
##zee.linestyle = '-'
##zee.color = '#354F52'
##zee.load(filelist_dir + 'zjets_sherpa_zee_mc16a', h5_dir_mc, tags = tags)
##loaded_samples.append(zee)
##
##zmm = sample.Sample("zmm", "$Z\\rightarrow \\mu\\mu$")
##zmm.scalefactor = lumi_factor
##zmm.fillstyle = 0
##zmm.linestyle = '-'
##zmm.color = '#52796F'
##zmm.load(filelist_dir + 'zjets_sherpa_zmm_mc16a', h5_dir_mc, tags = tags)
##loaded_samples.append(zmm)
##
##ztt = sample.Sample("ztt", "$Z\\rightarrow \\tau\\tau$")
##ztt.scalefactor = lumi_factor
##ztt.fillstyle = 0
##ztt.linestyle = '-'
##ztt.color = '#84A98C'
##ztt.load(filelist_dir + 'zjets_sherpa_ztt_mc16a', h5_dir_mc, tags = tags)
##loaded_samples.append(ztt)
#
dib = sample.Sample("Diboson", "$VV$")
dib.scalefactor = lumi_factor
dib.fillstyle = 0
dib.linestyle = '-'
dib.color = "#f6f7eb"
dib.load(filelist_dir + "diboson_sherpa_mc16a", h5_dir_mc, tags = tags)
loaded_samples.append(dib)
#
#wjets = sample.Sample("Wjets", "$W + jets$")
#wjets.scalefactor = lumi_factor
#wjets.fillstyle = 0
#wjets.linestyle = '-'
#wjets.color = "#726e97"
#wjets.load(filelist_dir + "wjets_sherpa_mc16a", h5_dir_mc, tags = tags)
##loaded_samples.append(wjets)
#
ttv = sample.Sample("ttV", "$t\\bar{t} + V$")
ttv.scalefactor = lumi_factor
ttv.fillstyle = 0
ttv.linestyle = '-'
ttv.color = "#353531"
ttv.load(filelist_dir + "ttV_mc16a", h5_dir_mc, tags = tags)
loaded_samples.append(ttv)

dy = sample.Sample("DY", "Drell-Yan")
dy.scalefactor = lumi_factor
dy.fillstyle = 0
dy.linestyle = '-'
dy.color = "#FF5959"
#dy.color = "#ff9505"
dy.load(filelist_dir + "drellyan_sherpa_mc16a", h5_dir_mc, tags = tags)
loaded_samples.append(dy)
#
##dyee = sample.Sample('dyee', 'DY$\\rightarrow ee$')
##dyee.scalefactor = lumi_factor
##dyee.fillstyle = 0
##dyee.linestyle = '-'
##dyee.color = '#6E8387'
##dyee.load(filelist_dir + 'drellyan_zee_sherpa_mc16a', h5_dir_mc, tags = tags)
##loaded_samples.append(dyee)
##
##dymm = sample.Sample('dymm', 'DY$\\rightarrow \\mu\\mu$')
##dymm.scalefactor = lumi_factor
##dymm.fillstyle = 0
##dymm.linestyle = '-'
##dymm.color = '#A4B8C4'
##dymm.load(filelist_dir + 'drellyan_zmm_sherpa_mc16a', h5_dir_mc, tags = tags)
##loaded_samples.append(dymm)
##
##dytt = sample.Sample('dytt', 'DY$\\rightarrow \\tau\\tau$')
##dytt.scalefactor = lumi_factor
##dytt.fillstyle = 0
##dytt.linestyle = '-'
##dytt.color = '#C8D3D5'
##dytt.load(filelist_dir + 'drellyan_ztt_sherpa_mc16a', h5_dir_mc, tags = tags)
##loaded_samples.append(dytt)
#
##signals
##hh0 = sample.Sample("hhSM", "$hh$ SM ($\\times 20$)")
##hh0.is_signal = True
##hh0.scalefactor = lumi_factor * 20 # 0.06# * 100
##hh0.fillstyle = 0
##hh0.linestyle = '--'
##hh0.color = '#fa0f00'
##hh0.load(filelist_dir + "custom_wwbb", h5_dir_sig, dsid_select = '123456')
##loaded_samples.append(hh0)
#
#hh = sample.Sample("hhSM", "SM $hh$ (arbitrary $\\sigma$)")
#hh.is_signal = True
#hh.scalefactor = lumi_factor * 5000#* 350
#hh.fillstyle = 0
#hh.linestyle = '--'
#hh.color = 'r'
#hh.load(filelist_dir + "wwbb_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(hh)

## data
data = sample.Sample("data15161718REAL", "Data ('15+'16+'17)")
#data = sample.Sample("data15161718DUMMY", "Data ('15+'16+'17)")
#data = sample.Sample("data1516REAL", "Data ('15+'16+'17)")

data.is_data = True
data.scalefactor = 1.0
data.fillstyle = 0
data.linestyle = '-'
data.color = 'k'
#data.load(filelist_dir + "ttV_mc16a", h5_dir_mc, tags = tags)
#data.load(filelist_dir_data + "n0306_data1516", h5_dir_data)
data.load(filelist_dir_data + "n0306_data15161718", h5_dir_data)
#print 'LOADING DATA AS Wt SAMPLE'
#print 'LOADING DATA AS Wt SAMPLE'
#print 'LOADING DATA AS Wt SAMPLE'
#print 'LOADING DATA AS Wt SAMPLE'
#data.load(filelist_dir + "wwbb2L_mc16a", h5_dir_mc, tags = tags)
#data.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = tags)
loaded_samples.append(data)
#if "sr_" not in selected_region.lower() :
#    loaded_samples.append(data)
#
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
trigger = "(( year == 2015 && trig_tight_2015dil == 1 ) || ( year == 2016 && trig_tight_2016dil == 1 ))"

#trigger = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ) || ( year == 2017 && trig_tight_2017rand == 1))"
#trigger = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ))"

#trigger1516 = "(( year == 2015 && trig_2015 == 1 ) || ( year == 2016 && trig_2016 == 1 ))"
#trigger151617 = "(( year == 2015 && trig_2015dil == 1 ) || ( year == 2016 && trig_2016dil == 1 ) || ( year == 2017 && trig_2017dilrand == 1) )"
#trigger17 = "(year == 2017 && trig_2017dilrand == 1)"
trigger1516 = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ))"
#trigger1516dil = "(( year == 2015 && trig_tight_2015dil == 1 ) || ( year == 2016 && trig_tight_2016dil == 1 ))"
trigger15161718 = "( ( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ) || ( year == 2017 && trig_tight_2017rand == 1 ) || ( year == 2018 && trig_tight_2018 == 1 ))" 
trigger151617 = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ) || ( year == 2017 && trig_tight_2017rand == 1) )"
trigger17 = "( year == 2017 && trig_tight_2017rand == 1 )"
if '15161718' in loaded_samples[len(loaded_samples)-1].name :
    trigger = trigger15161718
elif '151617' in loaded_samples[len(loaded_samples)-1].name :
    trigger = trigger151617
elif '1516' in loaded_samples[len(loaded_samples)-1].name :
    trigger = trigger1516
elif '17' in loaded_samples[len(loaded_samples)-1].name :
    trigger = trigger17
else :
    print 'FAILED TO LOAD TRIGGER STRING'
    sys.exit()

#trigger = trigger1516dil
trigger = trigger15161718

#trigger = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ))"


r = region.Region("wwbbpre", "WW$bb$ pre-selection")
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20" % (trigger)
loaded_regions.append(r)

## CR ttbar
r = region.Region("crtt", "Top CR")
r.tcut = "%s && nBJets==2 && mll>20  && mbb>100 && mbb<140 && mt2_llbb>100 && mt2_llbb<140 && dRll>1.5 && dRll<3.0 && HT2Ratio>0.4 && HT2Ratio<0.6" % ( trigger )
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

r = region.Region("crwt", "CR-$Wt$")
r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>150 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
loaded_regions.append(r)

r = region.Region("vrwt", "VR-$Wt$")
r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>120 && HT2Ratio>0.8 && dRll<1.5" % (trigger)
loaded_regions.append(r)

r = region.Region("sr_test", "SR N-1")
#r.tcut = "%s && nBJets>=2 && mbb>110 && mbb<140" % trigger
r.tcut = "nBJets>=2 && mbb>110 && mbb<140" # && mt2_bb>65 && NN_d_hh>6.2"
#r.tcut = "%s && nBJets>=2 && mbb>110 && mbb<140 && NN_d_hh>6.2 && mt2_bb>65" % trigger
loaded_regions.append(r)

r = region.Region("sr_nm1", "SR N-1")
r.tcut = "%s && nBJets>=2 && mbb>110 && mbb<140 && mt2_bb>50" % trigger
loaded_regions.append(r)

## NN REG
r = region.Region("nn_pre", "NN-Pre")
#r.tcut = "nBJets>=2 && l1_pt>20"
r.tcut = "%s && nBJets>=2" % (trigger)
loaded_regions.append(r)

r = region.Region("nn_preMBB2", "$m_{bb} \\in [100,140]$")
r.tcut = "nBJets>=2 && mbb>100 && mbb<140"
loaded_regions.append(r)

r = region.Region("nn_crtt", "Top CR")
#r.tcut = "nBJets>=2 && mbb>140 && NN_d_tt>1.5"
r.tcut = "nBJets>=2 && mbb>140 && NN_d_tt>1.5"
r.tcut = "nBJets>=2 && mbb>140 && NN_d_hh>4 && NN_d_hh<6"
r.tcut = "nBJets>=2 && mbb>140 && NN_d_hh>4"
#r.tcut = "%s && nBJets>=2 && mbb>140 && NN_d_tt>1.5" % (trigger)
loaded_regions.append(r)


r = region.Region("nn_crwt", "NN CR-$Wt$")
r.tcut = "nBJets>=2 && NN_d_tt<2.5 && NN_d_wt>2.2"
#r.tcut = "%s && nBJets>=2 && NN_d_tt<2.5 && NN_d_wt>2.2" % trigger# && isDF==1" % trigger
loaded_regions.append(r)

r = region.Region("nn_crz", "NN CR-$Z$")
r.tcut = "%s && nBJets>=1 && NN_d_zjets>0 && NN_d_tt<-5" % trigger # &&  NN_d_zjets>5 && NN_d_hh<6 && NN_d_wt<0 && NN_d_tt<1.5" % trigger
loaded_regions.append(r)

r = region.Region("nn_vrgen", "NN VR")
r.tcut = "%s && nBJets>=2 && mbb>100 && mbb<140 && NN_d_hh<6.5 && NN_d_hh>0 && mt2_bb>30" % trigger
loaded_regions.append(r)

r = region.Region("check_wt", "Wt target")
r.tcut = "%s && nBJets>=2 && NN_d_wt>1" % trigger
loaded_regions.append(r)

#auto blind
if "sr" in selected_region.lower() :
    del data
    data = None

#############################################################
# plots
#############################################################
variables = {}

# nn input features
variables["met"]            = { "nn_preMBB2" : [30, 0, 600]    , "nn_pre" : [50, 0, 1000]    , "nn_crtt" : [15, 0, 300]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [20, 0, 400]    }
variables["mbb"]            = { "nn_preMBB2" : [120, 0, 2400],  "nn_crtt" : [60, 140, 1360], "nn_crwt" : [60, 140, 1200] }
variables["metPhi"]         = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] ,  "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["mll"]            = { "nn_preMBB2" : [60, 0, 1200]    , "nn_pre" : [60, 0, 1200]    , "nn_crtt" : [40, 0, 800]    , "nn_crwt" : [40, 0, 800]     ,"nn_crz" : [20, 0, 600]    }
variables["dRll"]           = { "nn_preMBB2" : [0.3, 0, 6]      , "nn_pre" : [0.3, 0, 6]      ,  "nn_crtt" : [0.3, 0, 6]     , "nn_crwt" : [0.2, 0, 5]      ,"nn_crz" : [0.2, 0, 5]     }
variables["pTll"]           = { "nn_preMBB2" : [30, 0, 600]    , "nn_pre" : [50, 0, 1000]    , "nn_crtt" : [12, 0, 240]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [20, 0, 400]    }
variables["dphi_ll"]        = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["dphi_bb"]        = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["dphi_met_ll"]    = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["met_pTll"]       = { "nn_preMBB2" : [40, 0, 800]    , "nn_pre" : [60, 0, 1200]    , "nn_crtt" : [18, 0, 360]    , "nn_crwt" : [50, 0, 1000]     ,"nn_crz" : [20, 0, 600]    }
variables["nJets"]          = { "nn_preMBB2" : [1, 0, 20]       , "nn_pre" : [1, 0, 20]       , "nn_crtt" : [1, 0, 20]      , "nn_crwt" : [1, 0, 12]       ,"nn_crz" : [1, 0, 12]      }      
variables["nSJets"]         = { "nn_preMBB2" : [1, 0, 20]       , "nn_pre" : [1, 0, 20]       , "nn_crtt" : [1, 0, 20]      , "nn_crwt" : [1, 0, 12]       ,"nn_crz" : [1, 0, 12]      }
variables["nBJets"]         = { "nn_preMBB2" : [1, 0, 10]       , "nn_pre" : [1, 0, 10]       , "nn_crtt" : [1, 0, 10]       , "nn_crwt" : [1, 0, 6]        ,"nn_crz" : [1, 0, 6]       }
variables["HT2"]            = { "nn_preMBB2" : [60, 0, 1500]    , "nn_pre" : [60, 0, 1500]    , "nn_crtt" : [30, 0, 600]    , "nn_crwt" : [75, 0, 1500]     ,"nn_crz" : [30, 0, 900]    }
variables["HT2Ratio"]       = { "nn_preMBB2" : [0.05, 0, 1]     , "nn_pre" : [0.05, 0, 1]     , "nn_crtt" : [0.05, 0, 1]    , "nn_crwt" : [0.05, 0, 1]     ,"nn_crz" : [0.05, 0, 1]    }
variables["l0_pt"]          = { "nn_preMBB2" : [30, 0, 600]    , "nn_pre" : [50, 0, 1000]    , "nn_crtt" : [15, 0, 300]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [10, 0, 350]    }
variables["l1_pt"]          = { "nn_preMBB2" : [15, 0, 330]     , "nn_pre" : [30, 0, 600]     , "nn_crtt" : [10, 0, 250]    , "nn_crwt" : [10, 0, 250]     ,"nn_crz" : [10, 0, 250]    }
variables["l0_phi"]         = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["l1_phi"]         = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["j0_pt"]          = { "nn_preMBB2" : [60, 0, 1200]    , "nn_pre" : [60, 0, 1200]    , "nn_crtt" : [30, 0, 600]    , "nn_crwt" : [50, 0, 1000]     ,"nn_crz" : [20, 0, 500]    }
variables["j1_pt"]          = { "nn_preMBB2" : [40, 0, 800]     , "nn_pre" : [40, 0, 800]     , "nn_crtt" : [20, 0, 400]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [10, 0, 250]    }
variables["j0_phi"]         = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["j1_phi"]         = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["bj0_pt"]         = { "nn_preMBB2" : [30, 0, 600]    , "nn_pre" : [60, 0, 1200]    , "nn_crtt" : [20, 0, 400]    , "nn_crwt" : [50, 0, 1000]     ,"nn_crz" : [20, 0, 400]    }
variables["bj1_pt"]         = { "nn_preMBB2" : [10, 0, 200]     , "nn_pre" : [40, 0, 800]     , "nn_crtt" : [20, 0, 400]    , "nn_crwt" : [20, 0, 400]     ,"nn_crz" : [10, 0, 200]    }
variables["bj0_phi"]        = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["bj1_phi"]        = { "nn_preMBB2" : [0.4, -3.2, 3.2] , "nn_pre" : [0.4, -3.2, 3.2] , "nn_crtt" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
variables["mt2_bb"]         = { "nn_crtt" : [10, 0, 160], "nn_crwt" : [10, 0, 300],  "nn_pre" : [10, 0, 450], "nn_preMBB2" : [20, 0, 340] }
#variables["NN_p_hh"]        = { "nn_pre" : [0.05, 0, 1], "nn_crtt" : [0.05, 0, 1], "nn_crwt" : [0.005, 0, 0.1], "nn_crz" : [0.05, 0, 1]}
#variables["NN_p_tt"]        = { "nn_pre" : [0.05, 0, 1], "nn_crtt" : [0.05, 0, 1], "nn_crwt" : [0.005, 0, 0.1], "nn_crz" : [0.05, 0, 1]}
#variables["NN_p_wt"]        = { "nn_pre" : [0.05, 0, 1], "nn_crtt" : [0.05, 0, 1], "nn_crwt" : [0.005, 0.9, 1], "nn_crz" : [0.05, 0, 1]}
#variables["NN_p_zjets"]     = { "nn_pre" : [0.05, 0, 1], "nn_crtt" : [0.05, 0, 1], "nn_crwt" : [0.001, 0, 0.05], "nn_crz" : [0.05, 0, 1]}
variables["NN_d_hh"]        = { "nn_preMBB2" : [2, -40, 12], "nn_crtt" : [2, -40, 0], "nn_crwt" : [2, -50, 0], "nn_crz" : [2, -20, 30]}
variables["NN_d_tt"]        = { "nn_preMBB2" : [2, -15, 6], "nn_crtt" : [0.2, 1.4, 4] , "nn_crwt" : [0.5, -12, 0] , "nn_crz" : [1, -15, 5] }
#variables["NN_d_wt"]        = { "nn_pre" : [2, -25, 20], "nn_crtt" : [0.25, -5, 0], "nn_crwt" : [0.5, 0, 10], "nn_crz" : [2, -40, 10]}
#variables["NN_d_zjets"]     = { "nn_pre" : [2, -30, 10], "nn_crtt" : [2, -30, 0], "nn_crwt" : [2, -50, -8], "nn_crz" : [1, -15, 10]}
#variables["MT_1_scaled"] = { "nn_crtt" : [40, 160, 1000] }

#tmp = {}
#tmp["NN_d_hh"] = { "sr_test" : [2, -30, 20] }
##tmp["NN_d_hh"] = { "sr_nm1" : [2, -20, 12] }
##tmp["HT2Ratio"] = { "sr_nm1" : [0.05, 0, 1] }
##tmp["mt2_bb"] = { "sr_nm1" : [10, 0, 200] }
#variables = tmp

#tmp = {}
##tmp['NN_d_hh'] = { "nn_crz" : [1,-50,50] }
#tmp['NN_d_hh'] = { "sr_test" : [1,-50,50] }
#variables = tmp

#ptt = "nn_score_0/nn_score_1"
#pwt = "nn_score_0/nn_score_2"
#variables[ptt] = { "nn_pre" : [0.2, 0, 5] }
#variables[pwt] = { "nn_pre" : [0.2, 0, 5] }

nice_names = {}
nice_names["MT_1_scaled"] = [ "$M_{T1}$" ]
nice_names["NN_p_hh"]    = ["$p_{hh}$"]
nice_names["NN_p_tt"]    = ["$p_{t\\bar{t}}$"]
nice_names["NN_p_wt"]    = ["$p_{Wt}$"]
nice_names["NN_p_zjets"] = ["$p_{Z+jets}$"]
nice_names["NN_d_hh"]    = ["$d_{hh}$"]
nice_names["NN_d_tt"]    = ["$d_{tt}$"]
nice_names["NN_d_wt"]    = ["$d_{Wt}$"]
nice_names["NN_d_zjets"] = ["$d_{Z+jets}$"]
nice_names["met"]        = ["Missing Transverse Momentum [GeV]"]
nice_names["metPhi"]     = ["$\\phi$ of Missing Transverse Momentum"]
nice_names["mll"]        = ["$m_{\\ell \\ell}$ [GeV]"]
nice_names["dRll"]       = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["pTll"]       = ["$p_{T}^{\\ell \ell}$ [GeV]"]
nice_names["dphi_ll"]    = ["$\\Delta \\phi_{\\ell \ell}$"]
nice_names["dphi_bb"]    = ["$\\Delta \\phi_{bb}$"]
nice_names["dphi_met_ll"]= ["$\\Delta \\phi(\\vec{E}_{T}^{miss}, \\vec{p}_{T}^{\\ell \\ell})$"]
nice_names["met_pTll"]   = ["$\\vec{E}_{T}^{miss} + \\vec{p}_{T}^{\\ell \\ell}$ [GeV]"]
nice_names["nJets"]      = ["Jet Multiplicity" ]
nice_names["nSJets"]     = ["Non b-tagged Jet Multiplicity"]
nice_names["nBJets"]     = ["b-tagged Jet Multiplicity"]
nice_names["HT2"]        = ["$H_{T2}$ [GeV]"]
nice_names["HT2Ratio"]   = ["$H_{T2}^{R}$"]
nice_names["l0_pt"]      = ["Leading lepton $p_{T}$ [GeV]"]
nice_names["l1_pt"]      = ["Sub-leading lepton $p_{T}$ [GeV]"]
nice_names["l0_phi"]     = ["Leading lepton $\\phi$"]
nice_names["l1_phi"]     = ["Sub-leading lepton $\\phi$" ]
nice_names["j0_pt"]      = ["Leading jet $p_{T}$ [GeV]"]
nice_names["j1_pt"]      = ["Sub-leading jet $p_{T}$ [GeV]"]
nice_names["j0_phi"]     = ["Leading jet $\\phi$"]
nice_names["j1_phi"]     = ["Sub-leading jet $\\phi$"]
nice_names["bj0_pt"]     = ["Leading $b$-tagged jet $p_{T}$ [GeV]"]
nice_names["bj1_pt"]     = ["Sub-leading $b$-tagged jet $p_{T}$ [GeV]"]
nice_names["bj0_phi"]    = ["Leading $b$-tagged jet $\\phi$"]
nice_names["bj1_phi"]    = ["Sub-leading $b$-tagged jet $\\phi$"]
nice_names["mbb"]        = ["$m_{bb}$ [GeV]"]


for var, bounds in variables.iteritems() :

    if selected_region not in bounds :
        print "ERROR selected region (=%s) is not defined in configured variables" % ( selected_region )
        sys.exit()
    logy = False
    if selected_region in logy_regions or do_logy :
        logy = True

    name_var = var.replace('abs(','').replace(')','').replace('[','').replace(']','')
    p = plot1d('%s_%s' % (selected_region, name_var), name_var)
    p.normalized = False
    p.logy = logy
    if 'abs(' in var :
        p.absvalue = True
        var = var.replace('abs(', '').replace(')','')
    p.bounds = bounds[selected_region]
    if var in nice_names :
        if len(nice_names[var]) == 2 :
            p.units = nice_names[var][1]
    x_label = var
    y_label = 'Events / %s' % str(bounds[selected_region][0])
    if p.units != '' :
        y_label += ' %s' % str(p.units) 
    if var in nice_names :
        x_label = nice_names[var][0]
        if p.units != '' :
            x_label += ' [%s]' % str(p.units)
    p.labels = [x_label, y_label]
    loaded_plots.append(p)

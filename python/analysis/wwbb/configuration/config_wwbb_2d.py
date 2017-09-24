import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d

##################################################################################
# sample definition
##################################################################################
filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.06

# backgrounds
ttbar = sample.Sample("ttbar", "$t\\bar{t}$")
ttbar.scalefactor = lumi_factor 
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#bc5c61"
#ttbar.color = "#f6f5f0"
ttbar.load(filelist_dir + "ttbar", h5_dir_mc) 
loaded_samples.append(ttbar)

wt = sample.Sample("Wt", "$Wt$")
wt.scalefactor = lumi_factor
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#698bae" 
wt.load(filelist_dir + "Wt", h5_dir_mc)
loaded_samples.append(wt)
#
#ztt = sample.Sample("Ztt", "$Z \\rightarrow \\tau \\tau$")
#ztt.scalefactor = lumi_factor
#ztt.fillstyle = 0
#ztt.linestyle = '-'
#ztt.color = "#fecf90" 
#ztt.load(filelist_dir + "zjets_sherpa_tt", h5_dir_mc)
#loaded_samples.append(ztt)
#
#zll = sample.Sample("Zll", "$Z \\rightarrow \\ell \ell$")
#zll.scalefactor = lumi_factor
#zll.fillstyle = 0
#zll.linestyle = '-'
#zll.color = "#d1b7a5" 
#zll.load(filelist_dir + "zjets_sherpa_ll", h5_dir_mc)
#loaded_samples.append(zll)
#
#dib = sample.Sample("Diboson", "$VV \\rightarrow \\ell \\ell \\nu \\nu$")
#dib.scalefactor = lumi_factor
#dib.fillstyle = 0
#dib.linestyle = '-'
#dib.color = "#785e6f" 
#dib.load(filelist_dir + "diboson_sherpa_llvv", h5_dir_mc)
#loaded_samples.append(dib)
#
#wjets = sample.Sample("Wjets", "$W + jets$")
#wjets.scalefactor = lumi_factor
#wjets.fillstyle = 0
#wjets.linestyle = '-'
#wjets.color = "#daadbb" 
#wjets.load(filelist_dir + "wjets_sherpa", h5_dir_mc)
#loaded_samples.append(wjets)
#
#ttv = sample.Sample("ttV", "$t\\bar{t} + V$")
#ttv.scalefactor = lumi_factor
#ttv.fillstyle = 0
#ttv.linestyle = '-'
#ttv.color = "#b3e6fd" 
#ttv.load(filelist_dir + "ttV", h5_dir_mc)
#loaded_samples.append(ttv)
#
#dy = sample.Sample("DY", "Drell-Yan")
#dy.scalefactor = lumi_factor
#dy.fillstyle = 0
#dy.linestyle = '-'
#dy.color = "#ffd787" 
#dy.load(filelist_dir + "drellyan_sherpa", h5_dir_mc)
#loaded_samples.append(dy)
#
## data
#data = sample.Sample("data", "Data")
#data.is_data = True
#data.scalefactor = 1.0
#data.fillstyle = 0
#data.linestyle = '-'
#data.color = 'k'
#data.load(filelist_dir + "data_n0234", h5_dir_data)
#loaded_samples.append(data)

#signals
hh0 = sample.Sample("hhSM", "$hh$ SM")
hh0.is_signal = True
hh0.scalefactor = lumi_factor * 0.06 * 100
hh0.fillstyle = 0
hh0.linestyle = '--'
hh0.color = 'r'
hh0.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '342053')
loaded_samples.append(hh0)

hh1 = sample.Sample("hh800", "X $800$ GeV")
hh1.is_signal = True
hh1.scalefactor = lumi_factor * 20
hh1.fillstyle = 0
hh1.linestyle = '--'
hh1.color = 'b'
hh1.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '343775')
loaded_samples.append(hh1)

hh2 = sample.Sample("hh1000", "X $1000$ GeV")
hh2.is_signal = True
hh2.scalefactor = lumi_factor * 20
hh2.fillstyle = 0
hh2.linestyle = '--'
hh2.color = '#9cfd9d'
hh2.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = "343777")
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

r = region.Region("wwbbpre", "WW$bb$-pre")
r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>80 && mbb<140" % ( trigger )#,)isSF, isDF) #, trigger)
loaded_regions.append(r)

r = region.Region("wwbbpre_wtblm", "WW$bb$-pre (BLM)")
r.tcut = "%s && nBJets==1 && nBLMJets==2 && nSJets>=1 && mll>20 && l0_pt>25 && l1_pt>20 && mbb_blm>80 && mbb_blm<140" % ( trigger )#,)isSF, isDF) #, trigger)
loaded_regions.append(r)


#############################################################
# plots
#############################################################
variables = {}
#variables["HT2Ratio"] = { "wwbbpre" : [0.005, 0.98, 1.0] } # if a 4th argument is given, override automatic setting of y-max
variables["HT2Ratio_blm"] =     { "wwbbpre" : [0.05, 0.0, 1.0] } # if a 4th argument is given, override automatic setting of y-max
variables["nBJets"] =           { "wwbbpre" : [1, 0, 12] }
variables["nBLMJets"] =         { "wwbbpre" : [1, 0, 12] }
variables["dRll"] =             { "wwbbpre" : [0.1, 0, 5] }
variables["MT_1_scaled_blm"] =  { "wwbbpre" : [40, 0, 1500] }
variables["mt2_llbb_blm"] =     { "wwbbpre" : [10, 60, 400] }
variables["dRbb_blm"] =         { "wwbbpre" : [0.1, 0, 6] }
variables["l0_pt"] =            { "wwbbpre" : [10, 0, 300] }
variables["l1_pt"] =            { "wwbbpre" : [10, 0, 200] }


nice_names = {}
nice_names["HT2Ratio_blm"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["nBJets_blm"] = ["# $b-$jets (BLM)"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["MT_1_scaled_blm"] = ["M$_{T1}$", "GeV"]
nice_names["mt2_llbb_blm"] = ["$m_{T2}^{\\ell \\ell bb}$", "GeV"]
nice_names["l0_pt"] = ["Lead lepton $p_{T}$", "GeV"]
nice_names["l1_pt"] = ["Sub-lead lepton $p_{T}$", "GeV"]

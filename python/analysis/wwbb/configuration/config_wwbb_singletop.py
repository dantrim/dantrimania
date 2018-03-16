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

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.06
#lumi_factor = 100

# backgrounds
#ttbar = sample.Sample("ttbar", "$t\\bar{t}$")# \\times 0.97$")
##ttbar = sample.Sample("ttbar", "$t\\bar{t}$ (PP8)")# \\times 0.97$")
#ttbar.scalefactor = lumi_factor# * 0.97# * 1.10# * 0.92
#ttbar.fillstyle = 0
#ttbar.linestyle = '-'
#ttbar.color = "#f6f5f0"
#ttbar.load(filelist_dir + "ttbar", h5_dir_mc) 
##ttbar.load(filelist_dir + "ttbar_pp8", h5_dir_mc) 
#loaded_samples.append(ttbar)

#wt = sample.Sample("Wt", "$Wt$ (AMC)")# \\times 1.32$")
wt = sample.Sample("Wt", "$Wt$")
wt.scalefactor = lumi_factor# * 1.13
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#698bae" 
wt.load(filelist_dir + "Wt", h5_dir_mc)
#wt.load(filelist_dir + "WtAMC", h5_dir_mc)
loaded_samples.append(wt)

wtDS = sample.Sample("WtDS", "$Wt$ (DS)")
wtDS.scalefactor = lumi_factor
wtDS.fillstyle = 0
wtDS.linestyle = '-'
wtDS.color = "#698bad"
wtDS.load(filelist_dir + "singletop_DS", h5_dir_mc)
loaded_samples.append(wtDS)

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
#dib.load(filelist_dir + "diboson_sherpa", h5_dir_mc)
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
## drell-yan samples are contained in the Z+jets filelists
##dy = sample.Sample("DY", "Drell-Yan")
##dy.scalefactor = lumi_factor
##dy.fillstyle = 0
##dy.linestyle = '-'
##dy.color = "#ffd787" 
##dy.load(filelist_dir + "drellyan_sherpa", h5_dir_mc)
##loaded_samples.append(dy)
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
#
##signals
#hh0 = sample.Sample("hhSM", "$hh$ SM")
#hh0.is_signal = True
#hh0.scalefactor = lumi_factor * 0.06 * 100
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
#hh2 = sample.Sample("hh1000", "X $1000$ GeV")
#hh2.is_signal = True
#hh2.scalefactor = lumi_factor * 20
#hh2.fillstyle = 0
#hh2.linestyle = '--'
#hh2.color = '#0cf4ea'
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
trigger_single = "(( year == 2015 && ( (trig_pass2015==1) || (trig_e60_lhmedium==1 || trig_mu20_iloose_L1MU15))) || ( year == 2016 && ( (trig_pass2016update==1) || (trig_e60_lhmedium_nod0==1 || trig_mu26_ivarmedium==1))))"
trigger = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ))"

r = region.Region("crwtST", "CR-$Wt$ (ST)")
r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && HT2Ratio>0.5 && dRll>1.5 && dRll<3.0 && mt2_bb>80" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && dRll>1.5 && dRll<3.0 && HT2Ratio>0.5 && mt2_bb>150" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>160 && dRll<1.5 && HT2Ratio>0.5 && mt2_bb>150" % (trigger)
loaded_regions.append(r)

r = region.Region("srST", "SR-Test (ST)")
r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>90 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9" % ( trigger )
loaded_regions.append(r)

#auto blind
#if "sr" in selected_region.lower() :
#    if data :
#        del data
#        data = None

#############################################################
# plots
#############################################################
variables = {}

variables["HT2Ratio"] =     { "crwtST" : [0.1, 0.0, 1.0], "srST" : [0.1, 0.0, 1.0] }# , "vrht2ratio" : [0.01, 0.8, 1.0] , "vrtt0" : [0.05, 0.0, 1.0] }
variables["nBJets"] =       { "crwtST" : [1, 0, 6]      , "srST" : [1, 0, 6]       }#, "vrht2ratio" : [1, 0, 6]       , "vrtt0" : [1, 0, 5] }
variables["dRll"] =         { "crwtST" : [0.5, 0, 5]    , "srST" : [0.5, 0, 5]     }# , "vrht2ratio" : [0.05, 0.9, 2.0]    , "vrtt0" : [0.03, 0, 0.9] }
variables["MT_1_scaled"] =  { "crwtST" : [200, 0, 1600] , "srST" : [200, 0, 1600]  }# , "vrht2ratio" : [40, 0, 1500]    , "vrtt0" : [40, 0, 1500] }
variables["mt2_llbb"] =     { "crwtST" : [20, 60, 400]  , "srST" : [20, 60, 400]   }# , "vrht2ratio" : [2, 90, 140]     , "vrtt0" : [2, 90, 140] }
variables["dRbb"] =         { "crwtST" : [0.5, 0, 6]    , "srST" : [0.5, 0, 6]     }# , "vrht2ratio" : [0.1, 0, 6]      , "vrtt0" : [0.1, 0, 6] }
variables["l0_pt"] =        { "crwtST" : [20, 0, 300]   , "srST" : [20, 0, 300]    }# , "vrht2ratio" : [10, 0, 300]     , "vrtt0" : [10, 0, 300] }
variables["l1_pt"] =        { "crwtST" : [20, 0, 200]   , "srST" : [20, 0, 200]    }# , "vrht2ratio" : [10, 0, 200]     , "vrtt0" : [10, 0, 200] }
variables["mbb"] =          { "crwtST" : [40, 0, 600]   , "srST" : [40, 0, 600]    }# , "vrht2ratio" : [2, 100,140]     , "vrtt0" : [2, 100, 140] }
variables["bj0_pt"] =       { "crwtST" : [50, 0, 400]   , "srST" : [50, 0, 400]    }
variables["bj1_pt"] =       { "crwtST" : [50, 0, 400]   , "srST" : [50, 0, 400]    }
variables["mt2_bb"] =       { "crwtST" : [20, 0, 400]   , "srST" : [20, 0, 400]    }


nice_names = {}
nice_names["HT2Ratio"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["MT_1_scaled"] = ["M$_{T1}$ (scaled)", "GeV"]
nice_names["mt2_llbb"] = ["$m_{T2}^{\\ell \\ell bb}$", "GeV"]
nice_names["l0_pt"] = ["Lead lepton $p_{T}$", "GeV"]
nice_names["l1_pt"] = ["Sub-lead lepton $p_{T}$", "GeV"]
nice_names["mt2_bb"] = ["$m_{T2}^{bb}$", "GeV"]
nice_names["mbb"] = ["$m_{bb}$", "GeV"]
nice_names["bj0_pt"] = ["Lead $b-$jet $p_{T}$", "GeV"]
nice_names["bj1_pt"] = ["Sub-lead $b-$jet $p_{T}$", "GeV"]


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
            x_label += ' %s' % str(p.units)
    p.labels = [x_label, y_label]
    loaded_plots.append(p)

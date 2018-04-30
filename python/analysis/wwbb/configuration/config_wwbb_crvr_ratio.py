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

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.2

# backgrounds
ttbar = sample.Sample("ttbar", "$t\\bar{t}")# \\times 0.96$")
ttbar.scalefactor = lumi_factor #* 0.96
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#3f88c5"
ttbar.load(filelist_dir + "ttbar", h5_dir_mc, tags = ["mc16a"]) 
loaded_samples.append(ttbar)

wt = sample.Sample("Wt", "$Wt$") # \\times 0.50$")
wt.scalefactor = lumi_factor #* 0.50
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#e94f37"
wt.load(filelist_dir + "singletop", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(wt)

ztt = sample.Sample("Ztt", "$Z \\rightarrow \\tau \\tau$")
ztt.scalefactor = lumi_factor
ztt.fillstyle = 0
ztt.linestyle = '-'
ztt.color = "#44bba4"
ztt.load(filelist_dir + "zjets_tt", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(ztt)

zee = sample.Sample("Zee", "$Z \\rightarrow e e$")
zee.scalefactor = lumi_factor
zee.fillstyle = 0
zee.linestyle = '-'
zee.color = "#52796f"
zee.load(filelist_dir + "zjets_ee", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(zee)

zmm = sample.Sample("Zmm", "$Z \\rightarrow \\mu \\mu$")
zmm.scalefactor = lumi_factor
zmm.fillstyle = 0
zmm.linestyle = '-'
zmm.color = "#84a98c"
zmm.load(filelist_dir + "zjets_mm", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(zmm)

dib = sample.Sample("Diboson", "$VV$")
dib.scalefactor = lumi_factor
dib.fillstyle = 0
dib.linestyle = '-'
dib.color = "#f6f7eb"
dib.load(filelist_dir + "diboson", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(dib)

wjets = sample.Sample("Wjets", "$W + jets$")
wjets.scalefactor = lumi_factor
wjets.fillstyle = 0
wjets.linestyle = '-'
wjets.color = "#726e97"
wjets.load(filelist_dir + "wjets", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(wjets)

ttv = sample.Sample("ttV", "$t\\bar{t} + V$")
ttv.scalefactor = lumi_factor
ttv.fillstyle = 0
ttv.linestyle = '-'
ttv.color = "#353531"
ttv.load(filelist_dir + "ttV", h5_dir_mc, tags = ["mc16a"] )
loaded_samples.append(ttv)

dy = sample.Sample("DY", "Drell-Yan")
dy.scalefactor = lumi_factor
dy.fillstyle = 0
dy.linestyle = '-'
dy.color = "#ff9505"
dy.load(filelist_dir + "drellyan", h5_dir_mc, tags = ["mc16a"])
loaded_samples.append(dy)

## data
data = sample.Sample("data1516", "Data")
data.is_data = True
data.scalefactor = 1.0
data.fillstyle = 0
data.linestyle = '-'
data.color = 'k'
data.load(filelist_dir_data + "n0302_data1516", h5_dir_data)
loaded_samples.append(data)

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
#signal_mass = 1000
#dsid_dict = {}
#masses="""343764.260
#343766.300
#343769.400
#343771.500
#343772.600
#343773.700
#343774.750
#343775.800
#343776.900
#343777.1000
#343778.1100
#343779.1200
#343780.1300
#343781.1400
#343782.1500
#343783.1600
#343784.1800
#343785.2000
#343786.2250
#343787.2500
#343788.2750
#343789.3000
#"""
#for f in masses.split() :
#    x = f.split(".")
#    mass = x[1]
#    dsid = x[0]
#    dsid_dict[int(mass)] = dsid
#
#hh2 = sample.Sample("hh%d"%signal_mass, "X $%d$ GeV" % signal_mass)
#hh2.is_signal = True
#hh2.scalefactor = lumi_factor #* 20
#hh2.fillstyle = 0
#hh2.linestyle = '--'
#hh2.color = '#0cf4ea'
#hh2.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = dsid_dict[signal_mass])
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
trigger = "(( year == 2015 && trig_tight_2015dil == 1 ) || ( year == 2016 && trig_tight_2016dil == 1 ))"

#trigger = "(( year == 2015 && trig_tight_2015 == 1 ) || ( year == 2016 && trig_tight_2016 == 1 ) || ( year == 2017 && trig_tight_2017rand == 1))"

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
#r.tcut = "%s && nBJets==2 && mll>20" % trigger #&& mbb>140 && mt2_bb>100 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20" % trigger #&& mbb>140 && mt2_bb>100 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>100 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>150 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
#r.tcut = "%s && nBJets==2 && mll>20 && mbb>140 && mt2_bb>150 && HT2Ratio>0.6 && HT2Ratio<0.8" % (trigger)
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

#r = region.Region("sr_test", "SR-Test")
#lower=0.8 *  signal_mass 
#upper=1.1 * signal_mass 
#r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>100 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9 && MT_1_scaled>%.2f && MT_1_scaled<%.2f" % (trigger, lower, upper)
##r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>90 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9 && mt2_bb>130 && met>200" % ( trigger )
#loaded_regions.append(r)

#r = region.Region("sr_test", "SR-Test")
#r.tcut = "%s && nBJets==2 && (mbb>100 && mbb<140) && (mt2_llbb>100 && mt2_llbb<140) && HT2Ratio>0.8 && dRll<0.9 && mt2_bb>150" % (trigger)
#loaded_regions.append(r)

#auto blind
if "sr" in selected_region.lower() :
    del data
    data = None

#############################################################
# plots
#############################################################
variables = {}
variables["HT2Ratio"] =     { "crwt" : [0.04, 0.0, 1.0]}# , "crwt" : [0.01, 0.8, 1.0] , "vrtt0" : [0.05, 0.0, 1.0] }
variables["nBJets"] =       { "crwt" : [1, 0, 6]       }#, "crwt" : [1, 0, 6]       , "vrtt0" : [1, 0, 5] }
variables["dRll"] =         { "crwt" : [0.5, 0, 5]     }# , "crwt" : [0.05, 0.9, 2.0]    , "vrtt0" : [0.03, 0, 0.9] }
variables["MT_1_scaled"] =  { "crwt" : [60, 0, 1500]   }# , "crwt" : [40, 0, 1500]    , "vrtt0" : [40, 0, 1500] }
variables["mt2_llbb"] =     { "crwt" : [10, 60, 400]   }# , "crwt" : [2, 90, 140]     , "vrtt0" : [2, 90, 140] }
variables["dRbb"] =         { "crwt" : [0.5, 0, 6]     }# , "crwt" : [0.1, 0, 6]      , "vrtt0" : [0.1, 0, 6] }
variables["l0_pt"] =        { "crwt" : [10, 0, 300]    }# , "crwt" : [10, 0, 300]     , "vrtt0" : [10, 0, 300] }
variables["l1_pt"] =        { "crwt" : [10, 0, 200]    }# , "crwt" : [10, 0, 200]     , "vrtt0" : [10, 0, 200] }
variables["mbb"] =          { "crwt" : [40, 0, 600]    }# , "crwt" : [2, 100,140]     , "vrtt0" : [2, 100, 140] }
variables["bj0_pt"] =       { "crwt" : [20, 0, 400] }
variables["bj1_pt"] =       { "crwt" : [20, 0, 400] }
variables["mt2_bb"] =       { "crwt" : [20, 0, 400] }

variables["pTll"] =         { "crtt" : [10, 0, 210], "crwt" : [10, 0, 210], "vrtt" : [10, 0, 210], "vrwt" : [20, 0, 220] }

variables["HT2Ratio"] =     { "crtt" : [0.02, 0.38, 0.62], "vrtt" : [0.02, 0.58, 0.82],
                              "crwt" : [0.05, 0.55, 0.85], "vrwt" : [0.04, 0.76, 1.04], "sr_test" : [0.1, 0, 1]  }
variables["nBJets"] =       { "crtt" : [1, 0, 6]         , "vrtt" : [1, 0, 6]         ,
                              "crwt" : [1, 0, 6]         , "vrwt" : [1, 0, 6]         , "sr_test" : [1, 0, 10]  }
variables["dRll"] =         { "crtt" : [0.1, 1.4, 3.1]   , "vrtt" : [0.1, 0.8, 1.6]   ,
                              "crwt" : [0.5, 0, 5]       , "vrwt" : [0.2, 0, 1.6]     , "sr_test" : [0.2, 0, 10]  }
variables["MT_1_scaled"] =  { "crtt" : [35, 100, 800]    , "vrtt" : [20, 100, 680]    ,
                              "crwt" : [60, 200, 1200]   , "vrwt" : [60, 200, 1200]   , "sr_test" : [20, 0, 5000]  }
variables["mt2_llbb"] =     { "crtt" : [5, 90, 150]      , "vrtt" : [5, 90, 150]      ,
                              "crwt" : [50, 140, 1000]   , "vrwt" : [50, 115, 800]    , "sr_test" : [20, 0, 5000]  }
variables["dRbb"] =         { "crtt" : [0.5, 0, 6]       , "vrtt" : [0.5, 0, 6]       ,
                              "crwt" : [0.5, 0, 6]       , "vrwt" : [0.5, 0, 6]       , "sr_test" : [0.1, 0, 10]  }
variables["l0_pt"] =        { "crtt" : [10, 0, 220]      , "vrtt" : [10, 0, 240]      ,
                              "crwt" : [30, 0, 300]      , "vrwt" : [30, 0, 300]      , "sr_test" : [10, 0, 5000]  }
variables["l1_pt"] =        { "crtt" : [10, 0, 100]      , "vrtt" : [10, 0, 120]      ,
                              "crwt" : [20, 0, 200]      , "vrwt" : [10, 0, 120]      , "sr_test" : [10, 0, 5000]  }
variables["mbb"] =          { "crtt" : [5, 90, 150]      , "vrtt" : [5, 90, 150]      ,
                              "crwt" : [60, 140, 800]    , "vrwt" : [50, 115, 640]    , "sr_test" : [10, 0, 5000]  }
variables["bj0_pt"] =       { "crtt" : [10, 20, 180]     , "vrtt" : [10, 20, 250]     ,
                              "crwt" : [40, 20, 500]     , "vrwt" : [40, 20, 620]     , "sr_test" : [10, 0, 5000]  }
variables["bj1_pt"] =       { "crtt" : [8, 20, 100]      , "vrtt" : [5, 20, 130]      ,
                              "crwt" : [20, 20, 300]     , "vrwt" : [20, 20, 200]     , "sr_test" : [10, 0, 5000]  }
variables["mt2_bb"] =       { "crtt" : [5, 0, 100]       , "vrtt" : [8, 0, 160]       ,
                              "crwt" : [15, 150, 300]    , "vrwt" : [20, 110, 310]    , "sr_test" : [10, 0, 5000]  }
variables["met"] =          { "crtt" : [10, 0, 180]      , "vrtt" : [10, 0, 260]      ,
                              "crwt" : [30, 0, 500]      , "vrwt" : [30, 0, 500]      , "sr_test" : [10, 0, 5000]  }

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
nice_names["dRbb"] = ["$\\Delta R_{bb}$"]
nice_names["met"] = ["Missing Transverse Momentum", "GeV"]


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

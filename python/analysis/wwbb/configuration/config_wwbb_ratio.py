import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d

##################################################################################
# sample definition
##################################################################################
filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/c_aug16/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/c_aug16/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.06

# backgrounds
ttbar = sample.Sample("ttbar", "$t\\bar{t}$")
ttbar.scalefactor = lumi_factor 
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#f6f5f0"
ttbar.load(filelist_dir + "ttbar", h5_dir_mc) 
loaded_samples.append(ttbar)

wt = sample.Sample("Wt", "$Wt$")
wt.scalefactor = lumi_factor
wt.fillstyle = 0
wt.linestyle = '-'
wt.color = "#698bae" 
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

r = region.Region("wwbbpre", "WW$bb$-pre")
#r.tcut = "nBJets>=2 && mll>20 && l0_pt>45"
#r.tcut = "(( %s ) || ( %s )) && %s && nBJets>=2 && mll>20 && mbb>80 && mbb<140" % (isSFOS, isDFOS, trigger)
#r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && (mbb<80 || mbb>140) && HT2Ratio>0.98 && MT_1_scaled>800" % ( trigger )#,)isSF, isDF) #, trigger)
r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>80 && mbb<140" % ( trigger )#,)isSF, isDF) #, trigger)
loaded_regions.append(r)

# CR ttbar
r = region.Region("crtt0", "CR-$t\\bar{t}$ 0")
r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll>0.9 && HT2Ratio<0.8" % ( trigger )
loaded_regions.append(r)

r = region.Region("crtt1", "CR-$t\\bar{t}$ 1$")
#r = region.Region("crtt1", "CR-$t\\bar{t}$ 1 (-$H_{T2}^{R} \\in m_{T2}^{\\ell \\ell bb})$")
r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && (mbb<100 || mbb>140) && (mt2_llbb>90 && mt2_llbb<140) && dRll<0.9 && HT2Ratio>0.8" % ( trigger )
#r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && (mbb<100 || mbb>140) && (mt2_llbb>90 && mt2_llbb<140) && dRll<0.9" % ( trigger )
#r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && (mbb<100 || mbb>140) && (mt2_llbb<90 || mt2_llbb>140) && dRll<0.9 && HT2Ratio>0.8" % ( trigger )
loaded_regions.append(r)

r = region.Region("vrtt0", "VR-$t\\bar{t}$ 0$")
r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>100 && mbb<140 && mt2_llbb>90 && mt2_llbb<140 && dRll<0.9 && HT2Ratio<0.8" % ( trigger )
loaded_regions.append(r)

#############################################################
# plots
#############################################################
variables = {}
#variables["HT2Ratio"] = { "wwbbpre" : [0.005, 0.98, 1.0] } # if a 4th argument is given, override automatic setting of y-max
variables["HT2Ratio"] =     { "wwbbpre" : [0.05, 0.0, 1.0] , "crtt0" : [0.05, 0.0, 0.8] , "vrtt0" : [0.05, 0.0, 1.0] }
variables["nBJets"] =       { "wwbbpre" : [1, 0, 12]       , "crtt0" : [1, 0, 12]       , "vrtt0" : [1, 0, 5] }
variables["dRll"] =         { "wwbbpre" : [0.1, 0, 5]      , "crtt0" : [0.1, 0.9, 5]    , "vrtt0" : [0.03, 0, 0.9] }
variables["MT_1_scaled"] =  { "wwbbpre" : [40, 0, 1500]    , "crtt0" : [40, 0, 1500]    , "vrtt0" : [40, 0, 1500] }
variables["mt2_llbb"] =     { "wwbbpre" : [10, 60, 400]    , "crtt0" : [2, 90, 140]     , "vrtt0" : [2, 90, 140] }
variables["dRbb"] =         { "wwbbpre" : [0.1, 0, 6]      , "crtt0" : [0.1, 0, 6]      , "vrtt0" : [0.1, 0, 6] }
variables["l0_pt"] =        { "wwbbpre" : [10, 0, 300]     , "crtt0" : [10, 0, 300]     , "vrtt0" : [10, 0, 300] }
variables["l1_pt"] =        { "wwbbpre" : [10, 0, 200]     , "crtt0" : [10, 0, 200]     , "vrtt0" : [10, 0, 200] }
variables["mbb"] =          { "wwbbpre" : [40, 0, 600]     , "crtt0" : [2, 100,140]     , "vrtt0" : [2, 100, 140] }


nice_names = {}
nice_names["HT2Ratio"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["MT_1_scaled"] = ["M$_{T1}$", "GeV"]
nice_names["mt2_llbb"] = ["$m_{T2}^{\\ell \\ell bb}$", "GeV"]
nice_names["l0_pt"] = ["Lead lepton $p_{T}$", "GeV"]
nice_names["l1_pt"] = ["Sub-lead lepton $p_{T}$", "GeV"]

# load the plots 
for var, bounds in variables.iteritems() :
    if selected_region not in bounds :
        print "ERROR selected region (=%s) is not defined in configured variables" % ( selected_region )
        sys.exit()
    logy = False
    if selected_region in logy_regions or do_logy :
        logy = True
    p = hist1d.RatioCanvas(logy = logy)
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

    

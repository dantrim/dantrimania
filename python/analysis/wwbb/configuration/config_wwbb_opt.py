import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d

##################################################################################
# additional variables / common variables
##################################################################################
aadditional_variables = ['nBJets', 'MT_1_scaled', 'mt2_llbb', 'mbb',
                        'l0_pt', 'l1_pt', 'HT2Ratio', 'dRll', 'dRbb', 'mt2_bb',
                        'nBLMJets', 'nBLSJets', 'nSJets']
for a in aadditional_variables :
    additional_variables.append(a)

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
hh0.color = '#fa0f00'
hh0.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '342053')
loaded_samples.append(hh0)

hh3 = sample.Sample("hh600", "X $600$ GeV")
hh3.is_signal = True
hh3.scale_factor = lumi_factor * 20
hh3.fillstyle = 0
hh3.linestyle = "--"
hh3.color = '#ff5900'
hh3.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = "343772")
loaded_samples.append(hh3)

hh1 = sample.Sample("hh800", "X $800$ GeV")
hh1.is_signal = True
hh1.scalefactor = lumi_factor * 20
hh1.fillstyle = 0
hh1.linestyle = '--'
hh1.color = '#ffb900'
hh1.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '343775')
loaded_samples.append(hh1)

hh2 = sample.Sample("hh1000", "X $1000$ GeV")
hh2.is_signal = True
hh2.scalefactor = lumi_factor * 20
hh2.fillstyle = 0
hh2.linestyle = '--'
hh2.color = '#0cf4ea'
hh2.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = "343777")
loaded_samples.append(hh2)

hh4 = sample.Sample("hh1200", "X $1200$ GeV")
hh4.is_signal = True
hh4.scalefactor = lumi_factor * 20
hh4.fillstyle = 0
hh4.linestyle = '--'
hh4.color = '#002cff'
hh4.load(filelist_dir + "wwbb_susy2", h5_dir_mc, dsid_select = '343779')
loaded_samples.append(hh4)

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
r.tcut = "%s && nBJets==2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>80 && mbb<140 && mt2_llbb>80 && mt2_llbb<140 && HT2Ratio>0.7 && dRll<1.0" % ( trigger )#,)isSF, isDF) #, trigger)
loaded_regions.append(r)

#############################################################
# plots
#############################################################
variables = {}
#variables["HT2Ratio"] = { "wwbbpre" : [0.005, 0.98, 1.0] } # if a 4th argument is given, override automatic setting of y-max
variables["HT2Ratio"] =         { "wwbbpre" : [0.05, 0.0, 1.0] } # if a 4th argument is given, override automatic setting of y-max
variables["nBJets"] =           { "wwbbpre" : [1, 0, 5] }
variables["dRll"] =             { "wwbbpre" : [0.1, 0, 5] }
variables["abs(dphi_ll)"] =     { "wwbbpre" : [0.1, 0, 3.2] }
variables["abs(dphi_bb)"] =     { "wwbbpre" : [0.1, 0, 3.2] }
variables["MT_1_scaled"] =      { "wwbbpre" : [40, 0, 1500] }
variables["MT_1"] =             { "wwbbpre" : [40, 0, 1500] }
variables["mt2_llbb"] =         { "wwbbpre" : [10, 60, 400] }
variables["mbb"] =              { "wwbbpre" : [10, 60, 400] }
variables["dRbb"] =             { "wwbbpre" : [0.1, 0, 4] }
variables["l0_pt"] =            { "wwbbpre" : [10, 0, 300] }
variables["l1_pt"] =            { "wwbbpre" : [10, 0, 200] }
variables["mt2_bb"] =           { "wwbbpre" : [20, 0, 600] }
variables["abs(dphi_met_ll)"] = { "wwbbpre" : [0.1, 0, 3.2] }
variables["met"] =              { "wwbbpre" : [10, 0, 400] }
variables["abs(dphi_j0_l0)"] =  { "wwbbpre" : [0.1, 0, 3.2] }
variables["abs(dphi_j0_ll)"] =  { "wwbbpre" : [0.1, 0, 3.2] }
variables["abs(dphi_bj0_l0)"] = { "wwbbpre" : [0.1, 0, 3.2] }
variables["abs(dphi_bj0_ll)"] = { "wwbbpre" : [0.1, 0, 3.2] }


nice_names = {}
nice_names["HT2Ratio"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["dRbb"] = ["$\\Delta R_{bb}$"]
nice_names["MT_1_scaled"] = ["M$_{T1}$ (scaled) [GeV]", "GeV"]
nice_names["MT_1"] = ["M$_{T1}$ [GeV]", "GeV"]
nice_names["mt2_llbb"] = ["$m_{T2}^{\\ell \\ell bb}$ [GeV]", "GeV"]
nice_names["mt2_bb"] = ["$m_{T2}^{bb}$ [GeV]", "GeV"]
nice_names["mbb"] = ["$m_{bb}$ [GeV]", "GeV"]
nice_names["dphi_ll"] = ["$|\\Delta \\phi_{\\ell \\ell}$|"]
nice_names["dphi_bb"] = ["$|\\Delta \\phi_{bb}|$"]
nice_names["dphi_met_ll"] = ["$|\\Delta \\phi_{E_{T}^{miss}, \\ell \\ell}|$"]
nice_names["l0_pt"] = ["Lead lepton $p_{T}$ [GeV]", "GeV"]
nice_names["l1_pt"] = ["Sub-lead lepton $p_{T}$ [GeV]", "GeV"]
nice_names["met"] = ["$E_T^{miss}$ [GeV]", "GeV"]

# load the plots 
for var, bounds in variables.iteritems() :
    if selected_region not in bounds :
        print "ERROR selected region (=%s) is not defined in configured variables" % ( selected_region )
        sys.exit()
    logy = False
    if selected_region in logy_regions or do_logy :
        logy = True
    p = hist1d.DoubleRatioCanvas(logy = logy)
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

    p.build()

    loaded_plots.append(p)

    

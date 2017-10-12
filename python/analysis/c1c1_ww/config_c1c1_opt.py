import sys

import dantrimania.python.analysis.utility.samples.sample as sample
import dantrimania.python.analysis.utility.samples.region as region
from dantrimania.python.analysis.utility.plotting.plot1d import plot1d

##################################################################################
# additional variables / common variables
##################################################################################
#aadditional_variables = ['nBJets', 'nSJets', 'nJets', 'mt2', 'mll', 'dphi_ll',
#            'l0_pt', 'l1_pt', 'MDR', 'GAM', 'RPT', 'SHATR', 'DPB', 'dRll',
#            'dphi_met_ll', 'met', 'pTll', 'met_pTll', 'MT_HWW', 'cosThetaB']
#for a in aadditional_variables :
#    additional_variables.append(a)

##################################################################################
# sample definition
##################################################################################
filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/f_sep28_c1c1ww/mc/h5_2/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/e_aug31/data/h5/"

#loaded_samples = []
#loaded_signals = []

#lumi_factor = 36.06
lumi_factor = select_lumi

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

ztt = sample.Sample("Ztt", "$Z \\rightarrow \\tau \\tau$")
ztt.scalefactor = lumi_factor
ztt.fillstyle = 0
ztt.linestyle = '-'
ztt.color = "#fecf90" 
ztt.load(filelist_dir + "zjets_sherpa_tt", h5_dir_mc)
loaded_samples.append(ztt)

#zll = sample.Sample("Zll", "$Z \\rightarrow \\ell \ell$")
#zll.scalefactor = lumi_factor
#zll.fillstyle = 0
#zll.linestyle = '-'
#zll.color = "#d1b7a5" 
#zll.load(filelist_dir + "zjets_sherpa_ll", h5_dir_mc)
#loaded_samples.append(zll)

dib = sample.Sample("Diboson", "$VV \\rightarrow \\ell \\ell \\nu \\nu$")
dib.scalefactor = lumi_factor
dib.fillstyle = 0
dib.linestyle = '-'
dib.color = "#785e6f" 
dib.load(filelist_dir + "diboson_sherpa_llvv", h5_dir_mc)
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
c0 = sample.Sample("c1c1ww_100_1", "(100,1)")
c0.is_signal = True
c0.scalefactor = lumi_factor
c0.fillstyle = 0
c0.linestyle = '--'
c0.color = '#fa0f00'
c0.load(filelist_dir + "c1c1_ww", h5_dir_mc, dsid_select = '393650')
loaded_samples.append(c0)

c1 = sample.Sample("c1c1ww_100_25", "(100,25)")
c1.is_signal = True
c1.scalefactor = lumi_factor
c1.fillstyle = 0
c1.linestyle = '--'
c1.color = '#ff5900' 
c1.load(filelist_dir + "c1c1_ww", h5_dir_mc, dsid_select = '393652')
loaded_samples.append(c1)

c2 = sample.Sample("c1c1ww_100_50", "(100,50)")
c2.is_signal = True
c2.scalefactor = lumi_factor
c2.fillstyle = 0
c2.linestyle = '--'
c2.color = '#ffb900' 
c2.load(filelist_dir + "c1c1_ww",  h5_dir_mc, dsid_select = '393653')
loaded_samples.append(c2)

c3 = sample.Sample("c1c1ww_100_75", "(100,75)")
c3.is_signal = True
c3.scalefactor = lumi_factor
c3.fillstyle = 0
c3.linestyle = '--'
c3.color = '#0cf4ea' 
c3.load(filelist_dir + "c1c1_ww", h5_dir_mc, dsid_select = '393654')
loaded_samples.append(c3)

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

r = region.Region("c1c1pre", "$\\tilde{\\chi}_{1}^{\\pm} \\tilde{\\chi}_{1}^{\\mp}$-pre")
r.tcut = "%s && %s && mll>20 && l0_pt>25 && l1_pt>20 && nJets==1 && nSJets==1 && sj0_pt>100  && DPB>2" % ( isDF, trigger )
loaded_regions.append(r)

#############################################################
# plots
#############################################################
variables = {}
#variables["HT2Ratio"] = { "c1c1pre" : [0.005, 0.98, 1.0] } # if a 4th argument is given, override automatic setting of y-max
variables["dRll"] =             { "c1c1pre" : [0.1, 0, 5] }
variables["abs(dphi_ll)"] =     { "c1c1pre" : [0.1, 0, 3.2] }
variables["l0_pt"] =            { "c1c1pre" : [10, 0, 300] }
variables["l1_pt"] =            { "c1c1pre" : [10, 0, 200] }
variables["abs(dphi_met_ll)"] = { "c1c1pre" : [0.1, 0, 3.2] }
variables["met"] =              { "c1c1pre" : [10, 0, 400] }
variables['l0_pt'] =            { 'c1c1pre' : [20, 0, 400] }
variables['l1_pt'] =            { 'c1c1pre' : [20, 0, 400] }
variables['mll'] =              { 'c1c1pre' : [20, 0, 600] }
variables['mt2'] =              { 'c1c1pre' : [10, 0, 400] }
variables['MDR'] =              { 'c1c1pre' : [10, 0, 400] }
variables['GAM'] =              { 'c1c1pre' : [0.1, 0, 1] }
variables['RPT2'] =             { 'c1c1pre' : [0.1, 0, 1] }
variables['RPT'] =              { 'c1c1pre' : [0.01, 0, 0.1] }
variables['DPB'] =              { 'c1c1pre' : [0.1, 0, 3.2] }
variables['SHATR'] =            { 'c1c1pre' : [20, 0, 500] }
variables['met'] =              { 'c1c1pre' : [20, 0, 500] }
variables['abs(dphi_met_ll)'] = { 'c1c1pre' : [0.1, 0, 3.2] }
variables['abs(cosThetaB)'] =   { 'c1c1pre' : [0.1, 0, 1] }
variables['MT_HWW'] =           { 'c1c1pre' : [10, 0, 500] }
variables['R2'] =               { 'c1c1pre' : [0.1, 0, 1] }
variables['R1'] =               { 'c1c1pre' : [0.1, 0, 1] }
variables['meff'] =             { 'c1c1pre' : [20, 0, 600] }


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

for var, bounds in variables.iteritems() :
    if selected_region not in bounds :
        print "ERROR selected region (=%s) is not defined in configured variables" % ( selected_region )
        sys.exit()
    logy = False
    if selected_region in logy_regions or do_logy :
        logy = True

    name_var = var.replace('abs(','').replace(')','').replace('[','').replace(']','')
    p = plot1d('%s_%s' % (selected_region, name_var), name_var)
    p.logy = logy
    if 'abs(' in var :
        p.absvalue = True
        var = var.replace('abs(','').replace(')','')
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

    p.labels = [x_label, y_label]
    loaded_plots.append(p)

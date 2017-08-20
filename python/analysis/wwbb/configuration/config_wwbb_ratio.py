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

lumi_factor = 36.0

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

dy = sample.Sample("DY", "Drell-Yan")
dy.scalefactor = lumi_factor
dy.fillstyle = 0
dy.linestyle = '-'
dy.color = "#ffd787" 
dy.load(filelist_dir + "drellyan_sherpa", h5_dir_mc)
loaded_samples.append(dy)

# data
data = sample.Sample("data", "Data")
data.is_data = True
data.scale_factor = 1.0
data.fillstyle = 0
data.linestyle = '-'
data.color = 'k'
data.load(filelist_dir + "data_n0234", h5_dir_data)
loaded_samples.append(data)



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
r.tcut = "%s && nBJets>=2 && mll>20 && l0_pt>25 && l1_pt>20 && mbb>80 && mbb<140" % ( trigger )#,)isSF, isDF) #, trigger)
loaded_regions.append(r)

#############################################################
# plots
#############################################################
variables = {}
variables["HT2Ratio"] = { "wwbbpre" : [0.05, 0, 1] } # if a 4th argument is given, override automatic setting of y-max
variables["nBJets"] = { "wwbbpre" : [1, 0, 12] }
variables["dRll"] = { "wwbbpre" : [0.1, 0, 5] }
variables["MT_1_scaled"] = { "wwbbpre" : [40, 0, 1500] }
variables["mt2_llbb"] = { "wwbbpre" : [10, 0, 600] }


nice_names = {}
nice_names["HT2Ratio"] = ["$H_{T2}^{R}$"]
nice_names["nBJets"] = ["# $b-$jets"]
nice_names["dRll"] = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["MT_1_scaled"] = ["M$_{T1}$", "GeV"]
nice_names["mt2_llbb"] = ["$m_{T2}^{\\ell \\ell bb}$", "GeV"]

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

    

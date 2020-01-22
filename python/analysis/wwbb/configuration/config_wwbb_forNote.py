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
#filelist_dir = "/data/uclhc/uci/user/dantrim/n0301val/susynt-read/filelists/"
#filelist_dir_data = "/data/uclhc/uci/user/dantrim/n0302val/susynt-read/filelists/"
#filelist_dir = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
#filelist_dir_data = "/data/uclhc/uci/user/dantrim/n0234val/filelists/"
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/mc/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0302/b_apr25/data/h5/"
#
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/r_aug_27_nn/mc/h5/"
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0234/t_sep9_nn/mc/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/r_aug_27_nn/data/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0234/t_sep9_nn/data/h5/"
#h5_dir_sig = "/data/uclhc/uci/user/dantrim/n0234val/my_reco_hh/"
#h5_dir_sig = h5_dir_mc
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0304/a_oct28/mc/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0304/a_oct28/data/h5/"
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0304/b_nov11/mc/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0304/b_nov11/data/h5/"
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0304/c_nov12/mc/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0304/c_nov12/data/h5/"
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/mc/mc16a_nom/h5_test/"
#h5_dir_mc = '/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/mc/mc16a_sys/h5/'
##h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/mc/mc16a_nom/h5_test/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/a_dec2/data/h5/"
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0306/b_dec12/mc/mc16a/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/b_dec12/data/h5/"
#
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0306/c_dec20/mc/h5/"
#h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0306/c_dec20/data/h5/"
##h5_dir_mc_top = "/data/uclhc/uci/user/dantrim/ntuples/n0306/d_jan15/mc/h5/"


filelist_dir = "/data/uclhc/uci/user/dantrim/n0307val/susynt-read/filelists/"
filelist_dir_data = "/data/uclhc/uci/user/dantrim/n0307val/susynt-read/filelists/"
h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/mc/h5/"
#h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0307/b_feb18/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0307/a_feb10/data/h5/"

h5_dir_mc = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/mc/h5/"
h5_dir_data = "/data/uclhc/uci/user/dantrim/ntuples/n0307/d_feb21/data/h5/"

#loaded_samples = []
#loaded_signals = []

lumi_factor = 36.24
lumi_factor = 136
lumi_factor = 140.48 # joakim
#lumi_factor = 36.24
#lumi_factor = 80.0
#lumi_factor = 78.5
#lumi_factor = 43.6

tags = ["mc16a", "mc16d", "mc16e"]

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

top_sf =  0.85 #0.87  #0.9 #1.0 #0.94 #0.97 #0.97# 1.#0.64 #0.87 #0.88#0.905#0.93 #0.91 #0.97 #0.98 #0.98
z_sf = 1.35 #1.31#1.30#27#2 #1.3

ttbar = sample.Sample("ttbarFull", "$t\\bar{t} \\times %s$" % top_sf)
#ttbar = sample.Sample("ttbar", "$t\\bar{t} \\times$" % str(sf_vals_tt[which_data]))
ttbar.scalefactor = lumi_factor * top_sf #* 0.646#* 0.5533 #* 0.93 #* sf_vals_tt[which_data]
ttbar.fillstyle = 0
ttbar.linestyle = '-'
ttbar.color = "#057390"
#ttbar.color = "#0057FF"
ttbar.load(filelist_dir + "ttbar_mc16a", h5_dir_mc, tags = tags)#["mc16a"],"mc16d", "mc16e"])#, "mc16d", "mc16e"])
#ttbar.load(filelist_dir + "ttbar_mc16a", h5_dir_mc, tags = ["mc16a" ,"mc16d", "mc16e"])#, "mc16d", "mc16e"])
loaded_samples.append(ttbar)

#ttbar = sample.Sample("ttbar", "$t\\bar{t} \\times %s$" % str(top_sf))
##ttbar = sample.Sample("ttbar", "$t\\bar{t} \\times %s$" % str(sf_vals_tt[which_data]))
#ttbar.scalefactor = lumi_factor * top_sf #* 0.93 #* sf_vals_tt[which_data]
#ttbar.fillstyle = 0
#ttbar.linestyle = '-'
#ttbar.color = "#0057FF"
##ttbar.color = "#3f88c5"
#ttbar.load(filelist_dir + "ttbar_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(ttbar)

useDS = False

if not useDS :
    wt = sample.Sample("WtDRFull", "$Wt$ (DR) $\\times %s$" % top_sf)
    #wt = sample.Sample("WtPP8Dil", "$Wt  \\times %s$" % str(sf_vals_wt[which_data]))
    wt.scalefactor = lumi_factor * top_sf #* 0.35 #* sf_vals_wt[which_data]
    wt.fillstyle = 0
    wt.linestyle = '-'
    wt.color = "#78b166"
    #wt.color = "#008AFF"
    #wt.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = ['mc16a', 'mc16d', 'mc16e'])
    wt.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])
    loaded_samples.append(wt)

    #wt = sample.Sample("WtDR", "$Wt$ (DR) $\\times %s$" % str(top_sf))
    ##wt = sample.Sample("WtPP8Dil", "$Wt  \\times %s$" % str(sf_vals_wt[which_data]))
    #wt.scalefactor = lumi_factor * top_sf #* 0.35 #* sf_vals_wt[which_data]
    #wt.fillstyle = 0
    #wt.linestyle = '-'
    #wt.color = "#008AFF"
    ##wt.color = "#e94f37"
    ##wt.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = ['mc16a', 'mc16d', 'mc16e'])
    #wt.load(filelist_dir + "WtPP8_mc16a", h5_dir_mc, tags = tags)
    #loaded_samples.append(wt)

else :
    wt = sample.Sample("WtDSFull", "$Wt$ (DS) $\\times %s$" % top_sf)
    wt.scalefactor = lumi_factor * top_sf
    wt.fillstyle = 0
    wt.linestyle = '-'
    wt.color = "#78b166"
    wt.load(filelist_dir + "WtDS_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])
    loaded_samples.append(wt)

#stop = sample.Sample("STFull", "Single Top")
#stop.scalefactor = lumi_factor
#stop.fillstyle = 0
#stop.linestyle = '-'
#stop.color = 'b'
#stop.load(filelist_dir + "single_top_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])
#loaded_samples.append(stop)

#zjets = sample.Sample("Zjets", "$Z$+jets $\\times %s$" % z_sf)
#zjets.scalefactor = lumi_factor * z_sf
#zjets.fillstyle = 0
#zjets.linestyle = '-'
#zjets.color = "#FF0000"
##zjets.color = "#6e8387"
#zjets.load(filelist_dir + "zjets_sherpa_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(zjets)

zjets = sample.Sample("ZjetsFull", "$Z$+jets $\\times %s$" % z_sf)
zjets.scalefactor = lumi_factor * z_sf
zjets.fillstyle = 0
zjets.linestyle = '-'
zjets.color = "#fc8f1e"
#zjets.color = "#FF0000"
zjets.load(filelist_dir + "zjets_sherpa_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])
loaded_samples.append(zjets)

#zee = sample.Sample("Zee", "$Z\\rightarrow ee$")
#zee.scalefactor = lumi_factor * z_sf
#zee.color = "#CAD2C5"
#zee.load(filelist_dir + "zjets_ee", h5_dir_mc, tags = tags)
#loaded_samples.append(zee)
#
#zmm = sample.Sample("Zmm", "$Z\\rightarrow \\mu\\mu$")
#zmm.scalefactor = lumi_factor * z_sf
#zmm.color = "#52796F"
#zmm.load(filelist_dir + "zjets_mm", h5_dir_mc, tags = tags)
#loaded_samples.append(zmm)
#
#ztt = sample.Sample("Ztt", "$Z\\rightarrow \\tau\\tau$")
#ztt.scalefactor = lumi_factor * z_sf
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

#higgs = sample.Sample("higgs", "Single-higgs")
#higgs.scalefactor = lumi_factor
#higgs.fillstyle = 0
#higgs.linestyle = '-'
#higgs.color = 'b'
#higgs.load(filelist_dir + "single_higgs_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(higgs)

higgs = sample.Sample("higgsCorr2Full", "Single-higgs")
higgs.scalefactor = lumi_factor
higgs.fillstyle = 0
higgs.linestyle = '-'
higgs.color = '#d93b3b'
#higgs.color = '#7F557D'
#higgs.load(filelist_dir + "single_higgs_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])
#loaded_samples.append(higgs)

tth = sample.Sample("ttHFull", "$t\\bar{t} +H$")
tth.scalefactor = lumi_factor
tth.fillstyle = 0
tth.linestyle = '-'
tth.color = '#d93b3b'
#tth.load(filelist_dir + "ttH_dilep_mc16a", h5_dir_mc, tags = tags) #['mc16a', 'mc16d', 'mc16e'])
#loaded_samples.append(tth)

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

dib = sample.Sample("DibosonFull", "$VV$")
dib.scalefactor = lumi_factor
dib.fillstyle = 0
dib.linestyle = '-'
dib.color = "#f6f7eb"
dib.load(filelist_dir + "diboson_sherpa_mc16a", h5_dir_mc, tags = tags) #["mc16a", "mc16d", "mc16e"])
loaded_samples.append(dib)
#dib = sample.Sample("Diboson", "$VV$")
#dib.scalefactor = lumi_factor
#dib.fillstyle = 0
#dib.linestyle = '-'
#dib.color = "#f6f7eb"
#dib.load(filelist_dir + "diboson_sherpa_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(dib)

wjets = sample.Sample("WjetsFull", "$W + jets$")
wjets.scalefactor = lumi_factor
wjets.fillstyle = 0
wjets.linestyle = '-'
wjets.color = "#726e97"
#wjets.load(filelist_dir + "wjets_sherpa_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(wjets)

ttv = sample.Sample("ttVFull", "$t\\bar{t} + V$")
ttv.scalefactor = lumi_factor
ttv.fillstyle = 0
ttv.linestyle = '-'
ttv.color = "#353531"
ttv.load(filelist_dir + "ttV_mc16a", h5_dir_mc, tags = tags) #["mc16a", "mc16d", "mc16e"])
loaded_samples.append(ttv)

#ttv = sample.Sample("ttV", "$t\\bar{t} + V$")
#ttv.scalefactor = lumi_factor
#ttv.fillstyle = 0
#ttv.linestyle = '-'
#ttv.color = "#353531"
#ttv.load(filelist_dir + "ttV_mc16a", h5_dir_mc, tags = tags)

dy = sample.Sample("DYFull", "Drell-Yan")
dy.scalefactor = lumi_factor * z_sf
dy.fillstyle = 0
dy.linestyle = '-'
dy.color = "#f7b94c"
#dy.color = "#FF5959"
dy.load(filelist_dir + "drellyan_sherpa_mc16a", h5_dir_mc, tags = tags) #["mc16a", "mc16d", "mc16e"])
loaded_samples.append(dy)

#dy = sample.Sample("DY", "Drell-Yan")
#dy.scalefactor = lumi_factor
#dy.fillstyle = 0
#dy.linestyle = '-'
#dy.color = "#FF5959"
#dy.load(filelist_dir + "drellyan_sherpa_mc16a", h5_dir_mc, tags = tags)
#loaded_samples.append(dy)

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
#hh = sample.Sample("hhSMFull", "SM $hh$ (arbitrary $\\sigma$)")
#hh.is_signal = True
#hh.scalefactor = lumi_factor * 5000#* 350
#hh.fillstyle = 0
#hh.linestyle = '--'
#hh.color = 'r'
##hh.load(filelist_dir + "wwbb_mc16a", h5_dir_mc, tags = tags)
#sig_file_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0306/f_jan21/wwbb_signal/"
#hh.load('/data/uclhc/uci/user/dantrim/n0306val/susynt-read/filelists_mwt2/wwbb_mc16a', sig_file_dir, tags = ["mc16a", "mc16d", "mc16e"])
##loaded_samples.append(hh)

## data
data = sample.Sample("data15161718REAL", "Data ('15+'16+'17)")
#data = sample.Sample("data15161718DUMMY", "Data ('15+'16+'17)")
#data = sample.Sample("data1516REAL", "Data ('15+'16+'17)")
data.is_data = True
data.scalefactor = 1.0
data.fillstyle = 0
data.linestyle = '-'
data.color = 'k'
#data.load(filelist_dir_data + "n0306_data1516", h5_dir_data)
data.load(filelist_dir_data + "n0307_data15161718", h5_dir_data)
#print 'LOADING DATA AS Wt SAMPLE'
#print 'LOADING DATA AS Wt SAMPLE'
#print 'LOADING DATA AS Wt SAMPLE'
#print 'LOADING DATA AS Wt SAMPLE'
#data.load(filelist_dir + "ttV_mc16a", h5_dir_mc, tags = tags)
#data.load(filelist_dir + "wwbb_mc16a", h5_dir_mc, tags = tags)
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

r = region.Region("sr_test", "SR N-1")
#r.tcut = "%s && nBJets>=2 && mbb>110 && mbb<140" % trigger
r.tcut = "nBJets>=2 && mbb>110 && mbb<140 && (mll<71.2 || mll>111.2)" # && mt2_bb>65 && NN_d_hh>6.2"
#r.tcut = "%s && nBJets>=2 && mbb>110 && mbb<140 && NN_d_hh>6.2 && mt2_bb>65" % trigger
loaded_regions.append(r)

r = region.Region("sr_nm1", "SR N-1")
r.tcut = "%s && nBJets>=2 && mbb>110 && mbb<140 && mt2_bb>50" % trigger
loaded_regions.append(r)

r = region.Region("crztest", "CR-Z")
r.tcut = "nBJets>=2 && mll>20" # && mll>72 && mll<111"
loaded_regions.append(r)

r = region.Region("vrztest", "VR-Z")
r.tcut = "nBJets>=2 && mll>20" # && mll>72 && mll<111"
loaded_regions.append(r)


r = region.Region("crtoptest", "CR-Top")
r.tcut = "nBJets>=2"
loaded_regions.append(r)

r = region.Region("vrtoptest", "VR-Top")
r.tcut = "nBJets>=2"
loaded_regions.append(r)

r = region.Region("mllpre", "SR")
r.tcut = "nBJets>=2 && mll>20 && mbb>110 && mbb<140"
loaded_regions.append(r)

r = region.Region("mllOutMbb", "Check")
r.tcut = "nBJets>=2 && mll>20 && (mbb<110 || mbb>140)"
loaded_regions.append(r)

r = region.Region("presel", "$m_{bb} \in [100,140]$")
r.tcut = "nBJets>=2 && mll>20 && mbb>100 && mbb<140"
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
#variables["met"]            = { "crtoptest" : [60, 0, 600]    ,  "crztest" :  [50, 0, 1000]    , "crtop" : [30, 0, 600]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [20, 0, 400]    }
#variables["mbb"]            = { "crtoptest" : [5, 100, 140],     "crztest" :  [120, 0, 2400],  "crtop" : [45, 100, 1000], "nn_crwt" : [60, 140, 1200] }
#variables["metPhi"]         = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] ,  "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["mll"]            = { "crtoptest" : [5, 20, 80]    , "crztest" : [5, 70, 115]    , "crtop" : [8, 0, 160]    , "nn_crwt" : [40, 0, 800]     ,"nn_crz" : [20, 0, 600]    }
#variables["dRll"]           = { "crtoptest" : [0.15, 0, 3]      , "crztest" : [0.3, 0, 6]      ,  "crtop" : [0.15, 0, 3]     , "nn_crwt" : [0.2, 0, 5]      ,"nn_crz" : [0.2, 0, 5]     }
#variables["pTll"]           = { "crtoptest" : [15, 0, 300]    ,  "crztest" :  [50, 0, 1000]    , "crtop" : [20, 0, 400]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [20, 0, 400]    }
#variables["dphi_ll"]        = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["dphi_bb"]        = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
##variables["dphi_met_ll"]    = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["met_pTll"]       = { "crtoptest" : [30, 0, 600]    ,  "crztest" :  [60, 0, 1200]    , "crtop" : [40, 0, 800]    , "nn_crwt" : [50, 0, 1000]     ,"nn_crz" : [20, 0, 600]    }
#variables["nJets"]          = { "crtoptest" : [1, 0, 20]       , "crztest" : [1, 0, 20]       , "crtop" : [1, 0, 20]      , "nn_crwt" : [1, 0, 12]       ,"nn_crz" : [1, 0, 12]      }      
#variables["nSJets"]         = { "crtoptest" : [1, 0, 20]       , "crztest" : [1, 0, 20]       , "crtop" : [1, 0, 10]      , "nn_crwt" : [1, 0, 12]       ,"nn_crz" : [1, 0, 12]      }
#variables["nBJets"]         = { "crtoptest" : [1, 0, 10]       , "crztest" : [1, 0, 10]       , "crtop" : [1, 0, 10]       , "nn_crwt" : [1, 0, 6]        ,"nn_crz" : [1, 0, 6]       }
#variables["HT2"]            = { "crtoptest" : [45, 0, 900]    , "crztest" : [60, 0, 1500]    , "crtop" : [100, 0, 2000]    , "nn_crwt" : [75, 0, 1500]     ,"nn_crz" : [30, 0, 900]    }
#variables["HT2Ratio"]       = { "crtoptest" : [0.02, 0.6, 1]     , "crztest" : [0.05, 0, 1]     , "crtop" : [0.025, 0.5, 1]    , "nn_crwt" : [0.05, 0, 1]     ,"nn_crz" : [0.05, 0, 1]    }
#variables["l0_pt"]          = { "crtoptest" : [10, 0, 200]    ,  "crztest" :  [50, 0, 1000]    , "crtop" : [20, 0, 400]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [10, 0, 350]    }
#variables["l1_pt"]          = { "crtoptest" : [6, 0, 120]     , "crztest" : [30, 0, 600]     , "crtop" : [10, 0, 200]    , "nn_crwt" : [10, 0, 250]     ,"nn_crz" : [10, 0, 250]    }
#variables["l0_phi"]         = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["l1_phi"]         = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["j0_pt"]          = { "crtoptest" : [40, 0, 800]    , "crztest" : [60, 0, 1200]    , "crtop" : [40, 0, 800]    , "nn_crwt" : [50, 0, 1000]     ,"nn_crz" : [20, 0, 500]    }
#variables["j1_pt"]          = { "crtoptest" : [20, 0, 320]     , "crztest" : [40, 0, 800]     , "crtop" : [60, 0, 600]    , "nn_crwt" : [30, 0, 600]     ,"nn_crz" : [10, 0, 250]    }
#variables["j0_phi"]         = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["j1_phi"]         = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["bj0_pt"]         = { "crtoptest" : [20, 0, 340]    ,  "crztest" :  [60, 0, 1200]    , "crtop" : [30, 0, 600]    , "nn_crwt" : [50, 0, 1000]     ,"nn_crz" : [20, 0, 400]    }
#variables["bj1_pt"]         = { "crtoptest" : [10, 0, 200]     , "crztest" : [40, 0, 800]     , "crtop" : [20, 0, 400]    , "nn_crwt" : [20, 0, 400]     ,"nn_crz" : [10, 0, 200]    }
#variables["bj0_phi"]        = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["bj1_phi"]        = { "crtoptest" : [0.4, -3.2, 3.2] , "crztest" : [0.4, -3.2, 3.2] , "crtop" : [0.4, -3.2, 3.2], "nn_crwt" : [0.4, -3.2, 3.2] ,"nn_crz" : [0.2, -3.2, 3.2]}
#variables["mt2_bb"]         = {  "crtoptest" : [20, 0, 240],     "crztest" : [10, 0, 450],     "crtop" : [15, 0, 300], "nn_crwt" : [10, 0, 300] }
#variables["NN_d_hh"]        = { "crtoptest" : [0.1, 2.5, 4],     "crztest" : [1, 4, 16],        "crtop" : [1, 0, 20], "nn_crwt" : [2, -50, 0], "nn_crz" : [2, -20, 30]}

#variables["met"]                    = { "crtoptest" : [25, 0, 500]    ,    "vrtoptest" : [100, 0, 1000]    ,    "crztest" :  [25, 0, 500],    "vrztest" :  [25, 0, 500]}
#variables["mbb"]                    = { "crtoptest" : [50, 100, 1200],       "vrtoptest" : [50, 0, 1000],       "crztest" :  [100, 0, 2000],  "vrztest" :  [60, 0, 1200]}
#variables["abs(metPhi)"]            = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
#variables["mll"]                    = { "crtoptest" : [5, 20, 60]    ,     "vrtoptest" : [5, 20, 60]    ,     "crztest" : [5, 70, 115],     "vrztest" : [5, 70, 115]}
#variables["dRll"]                   = { "crtoptest" : [0.25, 0, 3.5]      ,  "vrtoptest" : [0.15, 0, 3]      ,  "crztest" : [0.3, 0, 6],      "vrztest" : [0.15, 0, 2.4]}
#variables["pTll"]                   = { "crtoptest" : [25, 0, 500]    ,    "vrtoptest" : [25, 0, 500]    ,    "crztest" :  [50, 0, 1000],   "vrztest" :  [50, 0, 800]}
#variables["abs(dphi_ll)"]           = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.1, 0, 2]} 
#variables["abs(dphi_bb)"]           = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.16, 0, 3.2]}
#variables["abs(dphi_met_ll)"]       = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.16, 0, 3.2]}
#variables["met_pTll"]               = { "crtoptest" : [40, 0, 800]    ,    "vrtoptest" : [40, 0, 800]    ,    "crztest" :  [30, 0, 900],    "vrztest" :  [50, 0, 1000]}
#variables["nJets"]                  = { "crtoptest" : [1, 0, 20]       ,   "vrtoptest" : [1, 0, 20]       ,   "crztest" : [1, 0, 20],       "vrztest" : [1, 0, 20]}    
#variables["nSJets"]                 = { "crtoptest" : [1, 0, 20]       ,   "vrtoptest" : [1, 0, 20]       ,   "crztest" : [1, 0, 20],       "vrztest" : [1, 0, 20]}   
#variables["nBJets"]                 = { "crtoptest" : [1, 0, 10]       ,   "vrtoptest" : [1, 0, 10]       ,   "crztest" : [1, 0, 10],       "vrztest" : [1, 0, 10]}   
#variables["HT2"]                    = { "crtoptest" : [80, 0, 1600]    ,    "vrtoptest" : [90, 0, 1800]    ,    "crztest" : [80, 0, 1600],    "vrztest" : [75, 100, 1600]}
#variables["HT2Ratio"]               = { "crtoptest" : [0.1, 0., 1]  ,    "vrtoptest" : [0.05, 0.2, 1]  ,    "crztest" : [0.05, 0.2, 1],   "vrztest" : [0.05, 0.4, 1]}
#variables["l0_pt"]                  = { "crtoptest" : [15, 0, 300]    ,    "vrtoptest" : [25, 0, 500]    ,    "crztest" :  [50, 0, 1000],   "vrztest" :  [30, 0, 600]} 
#variables["l1_pt"]                  = { "crtoptest" : [5, 0, 120]     ,    "vrtoptest" : [9, 0, 180]     ,    "crztest" : [20, 0, 400],     "vrztest" : [14, 0, 280]}
#variables["abs(l0_phi)"]            = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
#variables["abs(l1_phi)"]            = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
#variables["j0_pt"]                  = { "crtoptest" : [40, 0, 800]    ,    "vrtoptest" : [60, 0, 1200]    ,    "crztest" : [60, 0, 1200],    "vrztest" : [50, 0, 1000]}
#variables["j1_pt"]                  = { "crtoptest" : [30, 0, 600]     ,   "vrtoptest" : [25, 0, 500]     ,   "crztest" : [40, 0, 800],     "vrztest" : [25, 0, 550]} 
#variables["abs(j0_phi)"]            = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
#variables["abs(j1_phi)"]            = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.16, 0, 3.2]}
#variables["bj0_pt"]                 = { "crtoptest" : [40, 0, 800]    ,   "vrtoptest" : [40, 0, 800]    ,   "crztest" :  [60, 0, 1200],   "vrztest" :  [60, 0, 1200]}
#variables["bj1_pt"]                 = { "crtoptest" : [25, 0, 500]     ,   "vrtoptest" : [20, 0, 400]     ,   "crztest" : [40, 0, 800],     "vrztest" : [20, 0, 400]}
#variables["abs(bj0_phi)"]           = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.16, 0, 3.2]}
#variables["abs(bj1_phi)"]           = { "crtoptest" : [0.16, 0, 3.2] ,   "vrtoptest" : [0.16, 0, 3.2] ,   "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.16, 0, 3.2]}
#variables["mt2_bb"]                 = { "crtoptest" : [20, 0, 280],        "vrtoptest" : [20, 0, 400],        "crztest" : [10, 0, 200],     "vrztest" : [15, 0, 300]}
#variables["NN_d_hh"]                = { "crtoptest" : [0.2, 1, 3],        "vrtoptest" : [1, 3, 12],        "crztest" : [1, 2, 16],       "vrztest" : [1, 2, 12]}  
#variables["dRbb"]                   = { "crtoptest" : [0.5, 0, 6],         "vrtoptest" : [0.4, 0, 5.2],         "crztest" : [0.5, 0, 6],      "vrztest" : [0.5, 0, 6]}   
#variables["abs(deta_ll)"]           = { "crtoptest" : [0.2, 0, 2.6],        "vrtoptest" : [0.1, 0, 2],        "crztest" : [0.1, 0, 2],      "vrztest" : [0.1, 0, 2]}   
#variables["abs(dphi_WW_bb)"]        = { "crtoptest" : [0.16, 0, 3.2],       "vrtoptest" : [0.2, 0, 3.2],       "crztest" : [0.16, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]50

# definitions as of Jan 21
variables["met"]                    = { "presel": [60, 0, 600], "crtoptest" : [50, 0, 500]    ,    "vrtoptest" : [100, 0, 800]    ,    "crztest" :  [40, 0, 340],    "vrztest" :  [40, 0, 440]}
variables["mbb"]                    = { "presel": [5,100, 140], "crtoptest" : [20, 0, 600],       "vrtoptest" : [400, 0, 1800],       "crztest" :  [5, 100, 160],  "vrztest" :  [5, 100, 160]}
variables["abs(metPhi)"]            = { "presel": [0.16, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["mll"]                    = { "presel": [60, 0, 1200], "crtoptest" : [5, 20, 60]    ,     "vrtoptest" : [5, 20, 60]    ,     "crztest" : [1, 80, 102],     "vrztest" : [5, 70, 115]}
variables["dRll"]                   = { "presel": [0.3, 0, 6], "crtoptest" : [0.25, 0, 3.25]      ,  "vrtoptest" : [0.3, 0, 3]      ,  "crztest" : [0.25, 0, 3],      "vrztest" : [0.4, 0, 4]}
variables["pTll"]                   = { "presel": [60, 0, 600], "crtoptest" : [50, 0, 450]    ,    "vrtoptest" : [50, 0, 600]    ,    "crztest" :  [100, 0, 1000],   "vrztest" :  [60, 0, 720]}
variables["abs(dphi_ll)"]           = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.16, 0, 2.4] ,   "vrtoptest" : [0.32, 0, 2.24] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.2, 0, 3]} 
variables["abs(dphi_bb)"]           = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["abs(dphi_met_ll)"]       = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["met_pTll"]               = { "presel": [80, 0, 800], "crtoptest" : [100, 0, 700]    ,    "vrtoptest" : [100, 0, 900]    ,    "crztest" :  [50, 0, 900],    "vrztest" :  [100, 0, 900]}
variables["nJets"]                  = { "presel": [1, 2, 12], "crtoptest" : [1, 2, 12]       ,   "vrtoptest" : [1, 2, 12]       ,   "crztest" : [2, 2, 12],       "vrztest" : [1, 2, 12]}    
variables["nSJets"]                 = { "presel": [1, 0, 12], "crtoptest" : [1, 0, 8]       ,   "vrtoptest" : [1, 0, 10]       ,   "crztest" : [1, 0, 10],       "vrztest" : [1, 0, 8]}   
variables["nBJets"]                 = { "presel": [1, 2, 6], "crtoptest" : [1, 2, 5]       ,   "vrtoptest" : [1, 2, 5]       ,   "crztest" : [1, 2, 5],       "vrztest" : [1, 2, 5]}   
variables["HT2"]                    = { "presel": [100, 0, 2000], "crtoptest" : [100, 200, 1200]    ,    "vrtoptest" : [200, 100, 2000]    ,    "crztest" : [100, 100, 1800],    "vrztest" : [100, 100, 1400]}
variables["HT2Ratio"]               = { "presel": [0.05, 0, 1], "crtoptest" : [0.1, 0.2, 1]  ,    "vrtoptest" : [0.1, 0.2, 1]  ,    "crztest" : [0.1, 0.5, 1],   "vrztest" : [0.05, 0.5, 1]}
variables["l0_pt"]                  = { "presel": [60, 0, 600], "crtoptest" : [40, 20, 440]    ,    "vrtoptest" : [50, 0, 500]    ,    "crztest" :  [70, 0, 770],   "vrztest" :  [60, 0, 600]} 
variables["l1_pt"]                  = { "presel": [15, 0, 330], "crtoptest" : [10, 10, 130]     ,    "vrtoptest" : [25, 0, 225]     ,    "crztest" : [30, 0, 300],     "vrztest" : [20, 0, 200]}
variables["abs(l0_phi)"]            = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["abs(l1_phi)"]            = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["j0_pt"]                  = { "presel": [120, 0, 1200], "crtoptest" : [120, 0, 1200]    ,    "vrtoptest" : [120, 0, 1200]    ,    "crztest" : [90, 0, 900],    "vrztest" : [100, 0, 1100]}
variables["j1_pt"]                  = { "presel": [80, 0, 800], "crtoptest" : [60, 0, 720]     ,   "vrtoptest" : [100, 0, 900]     ,   "crztest" : [60, 0, 600],     "vrztest" : [50, 0, 550]} 
variables["abs(j0_phi)"]            = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["abs(j1_phi)"]            = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["bj0_pt"]                 = { "presel": [60, 0, 600], "crtoptest" : [100, 0, 800]    ,   "vrtoptest" : [100, 0, 1000]    ,   "crztest" :  [30, 0, 600],   "vrztest" :  [60, 0, 600]}
variables["bj1_pt"]                 = { "presel": [20, 0, 200], "crtoptest" : [50, 0, 450]     ,   "vrtoptest" : [50, 0, 550]     ,   "crztest" : [20, 20, 240],     "vrztest" : [20, 20, 220]}
variables["abs(bj0_phi)"]           = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["abs(bj1_phi)"]           = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2] ,   "vrtoptest" : [0.32, 0, 3.2] ,   "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}
variables["mt2_bb"]                 = { "presel": [40, 0, 400], "crtoptest" : [40, 0, 320],        "vrtoptest" : [40, 0, 480],        "crztest" : [40, 0, 280],     "vrztest" : [30, 0, 300]}
#variables["NN_d_hh"]               = { "presel": [100, 0, 1500], "crtoptest" : [1, -15, 15],        "vrtoptest" : [1, 5, 12],        "crztest" : [1, 2, 16],       "vrztest" : [1, 2, 12]}  
variables["NN_d_hh"]                = { "presel": [2, -20, 20], "crtoptest" : [0.2, 3.7, 5.2],        "vrtoptest" : [2, 5, 16],        "crztest" : [1, 0, 10],       "vrztest" : [1, 0, 10]}  
variables["dRbb"]                   = { "presel": [0.25, 0, 5], "crtoptest" : [0.5, 0.5, 4.5],         "vrtoptest" : [0.4, 0.4, 4.8],         "crztest" : [0.5, 0, 4.5],      "vrztest" : [0.5, 0, 4]}   
variables["abs(deta_ll)"]           = { "presel": [0.2, 0, 4], "crtoptest" : [0.2, 0, 2.2],        "vrtoptest" : [0.2, 0, 2],        "crztest" : [0.2, 0, 2],      "vrztest" : [0.2, 0, 2.4]}   
variables["abs(dphi_WW_bb)"]        = { "presel": [0.32, 0, 3.2], "crtoptest" : [0.32, 0, 3.2],       "vrtoptest" : [0.4, 0, 3.2],       "crztest" : [0.32, 0, 3.2],   "vrztest" : [0.32, 0, 3.2]}

#tmp = {}
##tmp["NN_d_hh"] = { "mllpre" : [1, -12, 12] }
#tmp["mll"] = { "mllOutMbb" : [4, 20, 60] }
#tmp["l1_pt"] = { "mllOutMbb" : [20, 0, 160] }
#tmp["l0_pt"] = { "mllOutMbb" : [50, 0, 500] }
#tmp["NN_d_hh"] = { "mllOutMbb" : [2, -10, 10] }
##tmp["abs(l0_eta)"] = { "mllOutMbb" : [0.4, 0, 2.4] }
##tmp["abs(l1_eta)"] = { "mllOutMbb" : [0.4, 0, 2.4] }
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
nice_names["metPhi"]     = ["|$\\phi$| of Missing Transverse Momentum"]
nice_names["mll"]        = ["$m_{\\ell \\ell}$ [GeV]"]
nice_names["dRll"]       = ["$\\Delta R_{\\ell \\ell}$"]
nice_names["pTll"]       = ["$p_{T}^{\\ell \ell}$ [GeV]"]
nice_names["dphi_ll"]    = ["|$\\Delta \\phi_{\\ell \ell}$|"]
nice_names["dphi_bb"]    = ["|$\\Delta \\phi_{bb}$|"]
nice_names["dphi_met_ll"]= ["|$\\Delta \\phi(\\vec{E}_{T}^{miss}, \\vec{p}_{T}^{\\ell \\ell})$|"]
nice_names["met_pTll"]   = ["|$\\vec{E}_{T}^{miss} + \\vec{p}_{T}^{\\ell \\ell}$| [GeV]"]
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
nice_names["mt2_bb"]     = ["$m_{t2}^{bb}$ [GeV]"]
nice_names["deta_ll"]    = ["|$\\Delta \\eta_{\\ell \\ell}$|"]
nice_names["dphi_WW_bb"] = ["|$\\Delta \\phi( \\vec{WW}, \\vec{bb} )$|"]
nice_names["l0_eta"]     = ["Leading lepton |$\\eta$|"]
nice_names["l1_eta"]     = ["Sub-leading lepton |$\\eta$|"]


plot_var_loaded = []
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

    if var in plot_var_loaded: continue
    plot_var_loaded.append(var)

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

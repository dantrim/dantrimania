# stuff to handle loading of ROOT, etc

def import_root(ignore_all=False) :
    import ROOT as r
    r.PyConfig.IgnoreCommandLineOptions = True
    r.TFile.__init__._creates = False
    r.TCanvas.__init__._creates = False
    r.TPad.__init__._creates = False
    r.TH1F.__init__._creates = False
    r.TH2F.__init__._creates = False
    r.TGraph.__init__._creates = False
    r.TGraph2D.__init__._creates = False
    r.TGraphErrors.__init__._creates = False
    r.TGraphAsymmErrors.__init__._creates = False
    r.TLine.__init__._creates = False
    r.TLatex.__init__._creates = False

    if ignore_all :
        r.gROOT.ProcessLine("gErrorIgnoreLevel = 3001;")
    return r

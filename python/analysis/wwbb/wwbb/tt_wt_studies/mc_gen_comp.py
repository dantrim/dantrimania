#!/usr/bin/env python

from optparse import OptionParser
import os
import sys

import dantrimania.python.analysis.utility.plotting.m_py.hist1d as hist1d
import dantrimania.python.analysis.utility.utils.utils as utils
import dantrimania.python.analysis.utility.utils.plib_utils as plib
plt = plib.import_pyplot()

import numpy as np

class Plot :
    def __init__(self, name = "") :
        self.name = name
        self.nbins = []
        self.datay = []
        self.datax = []
        self.predx = []
        self.predy = []

    def __str__(self) :
        return "Plot variable = %s %s data = %s pred = %s" % (self.name, self.nbins, self.datay, self.predy)

def make_float_list(liststr) :

    return list(float(x) for x in liststr.replace("[","").replace("]","").replace(",","").split())

def load_file(infile) :

    out_plots = []
    lines = open(infile).readlines()
    for iline, line in enumerate(lines) :
        if not line : continue
        line = line.strip()
        if "XXX" not in line :
            print "ERROR Input file has line that does not start with 'XXX'"
            sys.exit()
        line = line.split("XXX")[1].strip()
        if line.split()[0] == 'var' :
            var = line.strip().replace("XXX","").strip().split('var')[1].strip()
            lbins = lines[iline+1]. strip().replace("XXX","").strip().split('bins')[1]
            ldatay = lines[iline+2].strip().replace("XXX","").strip().split('datay')[1]
            ldatax = lines[iline+3].strip().replace("XXX","").strip().split('datax')[1]
            lpredy = lines[iline+4].strip().replace("XXX","").strip().split('predy')[1]
            lpredx = lines[iline+5].strip().replace("XXX","").strip().split('predx')[1]

            #lbins = list(float(x) for x in lbins.replace("[","").replace("]","").split())
            bins = make_float_list(lbins)
            datay = make_float_list(ldatay)
            datax = make_float_list(ldatax)
            predy = make_float_list(lpredy)
            predx = make_float_list(lpredx)


            p = Plot(var)
            p.nbins = bins
            p.datay = datay
            p.datax = datax
            p.predy = predy
            p.predx = predx
            out_plots.append(p)

    return out_plots
            

def load_data(infiles) :

    out = []
    for f in infiles :
        out.append(load_file(f))
    #variables_a = load_file(file_a)
    #variables_b = load_file(file_b)

    l0 = len(out[0])
    for x in out[1:] :
        if len(x) != l0 :
            print "ERROR number of variable mismatch"
            sys.exit()
    return out

def get_var(varname, varlist) :

    if varlist == None :
        return None

    for v in varlist :
        if v.name == varname :
            return v
    print "ERROR Did not find var '%s' in varlist" % varname
    sys.exit()

def make_ab_plot(varname, avar, bvar, cvar, dvar, do_logy, output_dir, aname, bname, cname, dname) :

    datax = avar.datax
    datay = avar.datay
    bins = avar.nbins
    bw = bins[1] - bins[0]
    xlow = bins[0]
    xhigh = bins[-1]

    p = hist1d.DoubleRatioCanvas(logy = do_logy)
    p.vartoplot = avar.name
    p.bounds = [bw, xlow, xhigh]
    name = avar.name
    y_label = "Events"
    x_label = avar.name
    p.labels = [x_label, y_label]
    p.logy = do_logy
    p.build()

    # pads
    upper = p.upper
    middle = p.middle
    lower = p.lower

    #####################################################
    # draw data
    upper.plot(datax[:-1], datay, 'ko', label = 'Data', zorder=10000)

    # draw sample A
    ax = []
    ay = []
    for ix, x in enumerate(avar.predx[:-1]) :
        ax.append(x)
        ax.append(x+bw)
        ay.append(avar.predy[ix])
        ay.append(avar.predy[ix])
    upper.plot(ax, ay, color = 'r', label = "A = %s" % aname)
    #upper.hist(avar.predx[:-1], avar.predy, color = 'r', label = 'A')

    # draw sample B
    bx = []
    by = []
    for ix, x in enumerate(bvar.predx[:-1]) :
        bx.append(x)
        bx.append(x+bw)
        by.append(bvar.predy[ix])
        by.append(bvar.predy[ix])
    upper.plot(bx, by, color = 'b', label = "B = %s" % bname)

    # draw sample C
    if cvar :
        cx = []
        cy = []
        for ix, x in enumerate(cvar.predx[:-1]) :
            cx.append(x)
            cx.append(x+bw)
            cy.append(cvar.predy[ix])
            cy.append(cvar.predy[ix])
        upper.plot(cx, cy, color = 'g', label = "C = %s" % cname)

    if dvar :
        dx = []
        dy = []
        for ix, x in enumerate(dvar.predx[:-1]) :
            dx.append(x)
            dx.append(x+bw)
            dy.append(dvar.predy[ix])
            dy.append(dvar.predy[ix])
        upper.plot(dx, dy, color = 'm', label = "D = %s" % dname)

    ####################################################
    # data/X ratios
    middle.set_ylabel("Data / X", fontsize = 12)
    middle.set_yticks([0,0.5,1,1.5,2,2.5,3], minor = True)
    middle.set_ylim(0.0, 3.0)

    aratiox = datax
    aratioy = np.ones(len(datay))
    for idata, d in enumerate(datay) :
        pred = avar.predy[idata]
        ratio = 1.0
        if pred == 0 or d == 0:
            ratio = -5
        else :
            ratio = d / pred
        aratioy[idata] = ratio

    bratiox = datax
    bratioy = np.ones(len(datay))
    for idata, d in enumerate(datay) :
        pred = bvar.predy[idata]
        ratio = 1.0
        if pred == 0 or d == 0 :
            ratio = -5
        else :
            ratio = d / pred
        bratioy[idata] = ratio

    ashift = 0.2
    bshift = -0.2
    if cvar :
        ashift = 0.2
        bshift = 0.0
        cshift = -0.2
    if dvar :
        ashift = 0.2
        bshift = 0.1
        cshift = -0.1
        dshift = -0.2
    aratiox = [x - bw * ashift for x in aratiox]
    bratiox = [x - bw * bshift for x in bratiox]

    middle.plot(aratiox[:-1], aratioy,'ro', markersize = 4)
    middle.plot(bratiox[:-1], bratioy,'bo', markersize = 4)

    if cvar :
        cratiox = datax
        cratioy = np.ones(len(datay))
        for idata, d in enumerate(datay) :
            pred = cvar.predy[idata]
            ratio = 1.0
            if pred == 0 or d == 0 :
                ratio = -5
            else :
                ratio = d / pred
            cratioy[idata] = ratio
        cratiox = [x - bw * cshift for x in cratiox]
        middle.plot(cratiox[:-1], cratioy, 'go', markersize = 4)

    if dvar :
        dratiox = datax
        dratioy = np.ones(len(datay))
        for idata, d in enumerate(datay) :
            pred = dvar.predy[idata]
            ratio = 1.0
            if pred == 0 or d == 0 :
                ratio = -5
            else :
                ratio = d / pred
            dratioy[idata] = ratio
        dratiox = [x - bw * dshift for x in dratiox]
        middle.plot(dratiox[:-1], dratioy, 'mo', markersize = 4)

    # redline
    xl = np.linspace(xlow, xhigh, 20)
    yl = np.ones(len(xl))
    middle.plot(xl, yl, 'r--', zorder=0)
    
    
    ####################################################
    # A/B ratios
    lower.set_ylabel("X / A", fontsize = 12)
    lower.set_yticks([0,0.5,1,1.5,2], minor = True)
    lower.set_ylim(0.0, 2.0)
    #lower.set_ylabel("%s / %s" % ( aname, bname ), fontsize = 12)

    ratiox = datax
    ratioy = np.ones(len(datay))
    bshift = 0.0
    cshift = -0.1
    if cvar :
        bshift = 0.1
    if dvar :
        bshift = 0.1
        cshift = 0.0
        dshift = -0.1

    for i, d in enumerate(datay) :
        data_a = avar.predy[i]
        data_b = bvar.predy[i]
        ratio = 1.0
        if data_b == 0 or data_a == 0 :
            ratio = -5
        else :
            ratio = data_b / data_a
        ratioy[i] = ratio
    ratiox = [x - bw * bshift for x in ratiox]
    lower.plot(ratiox[:-1], ratioy, 'bo', markersize = 5)

    if cvar :
        ratiox = datax
        ratioy = np.ones(len(datay))
        for i, d in enumerate(datay) :
            data_a = avar.predy[i]
            data_c = cvar.predy[i]
            ratio = 1.0
            if data_c == 0 or data_a == 0 :
                ratio = -5
            else :
                ratio = data_c / data_a
            ratioy[i] = ratio
        ratiox = [x - bw * cshift for x in ratiox]
        lower.plot(ratiox[:-1], ratioy, 'go', markersize = 5)

    if dvar :
        ratiox = datax
        ratioy = np.ones(len(datay))
        for i, d in enumerate(datay) :
            data_a = avar.predy[i]
            data_d = dvar.predy[i]
            ratio = 1.0
            if data_d == 0 or data_a == 0 :
                ratio = -5
            else :
                ratio = data_d / data_a
            ratioy[i] = ratio
        ratiox = [x - bw * dshift for x in ratiox]
        lower.plot(ratiox[:-1], ratioy, 'mo', markersize = 5)

    # redline
    lower.plot(xl, yl, 'r--', zorder=0)

    ####################################################
    # legend
    upper.legend(loc='best', frameon = False, fontsize = 12, numpoints = 1)

    #####################################################
    # save
    utils.mkdir_p(output_dir)
    if not output_dir.endswith("/") :
        output_dir += "/"
    save_name = output_dir + "mc_comp_%s.pdf" % ( p.vartoplot )
    p.fig.savefig(save_name, bbox_inches = 'tight', dpi=200)
    p.fig.clf()
    
    

def main() :
    print "mc_gen_comp"

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", default="./", help = "Set output directory for plots") 
    parser.add_option("--logy", default=False, action="store_true", help = "Set y-axis to log scale in plots")
    parser.add_option("-v", "--var", default="", help = "Request specific variable to plot")
    parser.add_option("-a", "--in-a", default="", help = "Data file for sample 'A' (will take A/B)")
    parser.add_option("-b", "--in-b", default="", help = "Data file for sample 'B' (will take A/B)")
    parser.add_option("-c", "--in-c", default="", help = "Data file for sample 'C'")
    parser.add_option("-d", "--in-d", default="", help = "Data file for sample 'D'")
    parser.add_option("--aname", default="A", help = "Name for sample A")
    parser.add_option("--bname", default="B", help = "Name for sample B")
    parser.add_option("--cname", default="C", help = "Name for sample C")
    parser.add_option("--dname", default="D", help = "Name for sample D")
    (options, args) = parser.parse_args()
    output_dir = options.outputdir
    do_logy = options.logy
    select_var = options.var
    file_a = options.in_a
    file_b = options.in_b
    file_c = options.in_c
    file_d = options.in_d
    name_a = options.aname
    name_b = options.bname
    name_c = options.cname
    name_d = options.dname

    if file_a == "" :
        print "ERROR You did not provide a file for sample 'A'"
        sys.exit()
    if file_b == "" :
        print "ERROR You did not provide a file for sample 'B'"
        sys.exit()
    if file_d != "" and file_c == "" :
        print "ERROR You have provided a 'D' sample but no 'C' sample"
        sys.exit()


    avar = None
    bvar = None
    cvar = None
    dvar = None
    
    vars = load_data([file_a, file_b, file_c, file_d])
    avar = vars[0]
    bvar = vars[1]
    if file_c != "" :
        cvar = vars[2]

    if file_d != "" :
        dvar = vars[3]


    n_total = len(avar)
    for iv, v in enumerate(avar) :
        print "[%02d/%02d] %s" % (iv+1, n_total, v.name) 
        make_ab_plot(v, avar = get_var(v.name, avar),
                        bvar = get_var(v.name, bvar),
                        cvar = get_var(v.name, cvar),
                        dvar = get_var(v.name, dvar),
                        do_logy = do_logy, output_dir = output_dir,
                        aname = name_a,
                        bname = name_b,
                        cname = name_c,
                        dname = name_d)
    


#____________________________________________________________________________
if __name__ == "__main__" :
    main()

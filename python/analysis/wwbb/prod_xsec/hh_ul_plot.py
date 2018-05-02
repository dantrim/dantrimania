#!/usr/bin/env python

from scipy.interpolate import spline
import numpy as np
import matplotlib.pyplot as plt
import sys

class LimitPoint :
    def __init__(self, mass = 0) :
        self.mass = mass
        self.exp = 0.0 # pb
        self.exp_up = 0.0 # pb
        self.exp_dn = 0.0 # pb

    def __str__(self) :
        return "LimitPoint %d (%.4f, +%.4f, -%.4f)" % (self.mass, self.exp, self.exp_up, self.exp_dn)

def get_color(name) :

    colors = {}

    colors["NonRes_2L_Nom"] = "k"
    colors["NonRes_2L_1s"] = "#6dcef9"
    #colors["NonRes_2L_1s"] = "#014d87"
    colors["NonRes_1L_Nom"] = "k"
    colors["NonRes_1L_1s"] = "#bfd1d4"

    colors["Res_2L_Nom"] = "k"
    colors["Res_2L_1s"] = "#00ff00"
    colors["Res_1L_Nom"] = "k"
    colors["Res_1L_1s"] = "#85a88d"

    return colors[name]

def get_name(name) :

    names = {}

    names["NonRes_2L"] = "Non-resonant (2$\\ell$)"
    names["NonRes_1L"] = "Non-resonant (1$\\ell$)"
    names["Res_2L"] = "Resonant (2$\\ell$)"
    names["Res_1L"] = "Resonant (1$\\ell$)"

    return names[name]

def plot_sm_value(pad, limit, xbounds = [260, 1000], furthest_x = 500, name = "") :

    nom = limit.exp
    up = limit.exp_up
    dn = limit.exp_dn

    minx = xbounds[0]
    maxx = xbounds[1]

    xvals = np.arange(minx, maxx, 10)
    xvals = [x for x in xvals if x <= furthest_x]

    yvals = [nom for x in xvals]
    yvals_up = [up for x in xvals]
    yvals_dn = [dn for x in xvals]

    # draw nominal line

    nom_color = get_color("%s_Nom" % name)
    pad.plot(xvals, yvals, '%s--' % nom_color, lw = 1)

    # draw +/-1 sigma band around the nominal
    color_1s = get_color("%s_1s" % name)
    pad.fill_between(xvals, yvals, yvals_up, alpha = 0.6,
        facecolor = color_1s, edgecolor = 'none', label = get_name(name))

    pad.fill_between(xvals, yvals_dn, yvals, alpha = 0.6,
        facecolor = color_1s, edgecolor = 'none')

    # draw text of limit val
    nom = yvals[0]
    up = yvals_up[0] - yvals[0]
    dn = yvals[0] - yvals_dn[0]
    pad.text(furthest_x + 10, 0.5 * (nom + yvals_dn[0]), '$%.2f^{+%.2f}_{-%.2f}$' % (nom, up, dn), alpha = 0.86,
                color = 'grey', zorder = 1000)


def plot_resonant_value(pad, limits, name = "") :
    
    xvals = [l.mass for l in limits]
    yvals = [l.exp for l in limits]
    yvals_up = [l.exp_up for l in limits]
    yvals_dn = [l.exp_dn for l in limits]

    nom_color = get_color("%s_Nom" % name)
    color_1s = get_color("%s_1s" % name)

    pad.plot(xvals, yvals, '%so--' % nom_color, lw = 1, markersize = 0)

    # draw +/-1 sigma band around the nominal
    pad.fill_between(xvals, yvals, yvals_up, alpha = 0.6,
        facecolor = color_1s, edgecolor = 'none', label = get_name(name))
    pad.fill_between(xvals, yvals_dn, yvals, alpha = 0.6,
        facecolor = color_1s, edgecolor = 'none')
    

def plot_1L_stuff(pad, xbounds = [], furthest_x = 500) :

    # non-resonant 
    yval = 8.20 # pb
    yval_up = yval + 3.21
    yval_dn = yval - 2.29


    lp = LimitPoint(0)
    lp.exp = yval
    lp.exp_up = yval_up
    lp.exp_dn = yval_dn

    plot_sm_value(pad, lp, xbounds = xbounds, furthest_x = furthest_x, name = "NonRes_1L")


    xvals = [500, 600, 800, 900, 1000]
    yvals = [3.4, 1.2, 0.5, 0.41, 0.4]
    yvals_up = [5.0, 1.8, 0.71, 0.62, 0.56]
    yvals_dn = [2.3, 0.88, 0.38, 0.3, 0.28]

    nom_color = get_color("Res_1L_Nom")
    color_1s = get_color("Res_1L_1s")

    pad.plot(xvals, yvals, '%s--' % nom_color, lw = 1, alpha = 0.6, zorder = 0)

    pad.fill_between(xvals, yvals, yvals_up, alpha = 0.5, facecolor = color_1s,
        edgecolor = 'none', zorder = 0)

    pad.fill_between(xvals, yvals_dn, yvals, alpha = 0.5, facecolor = color_1s,
        edgecolor = 'none', zorder = 0)

def main() :

    points_file = sys.argv[1]
    lines = [l.strip() for l in open(points_file).readlines()]

    limits = []

    for line in lines :
        if line.startswith("#") : continue
        if not line : continue
        cols = line.split()

        mass = int(cols[0])
        lp = LimitPoint(mass)
        lp.exp = float(cols[1])
        lp.exp_up = float(cols[2])
        lp.exp_dn = float(cols[3])

        print lp

        limits.append(lp)

    resonant_limits = limits[1:]

    # get rid of undefined points
    resonant_limits = [r for r in resonant_limits if r.exp > 0]
    sm_limit = limits[0]

    xvals = [rl.mass for rl in resonant_limits]
    yvals_nominal = [rl.exp for rl in resonant_limits]
    yvals_up = [rl.exp_up for rl in resonant_limits]
    yvals_dn = [rl.exp_dn for rl in resonant_limits]

    minx = min(xvals)
    maxx = max(xvals)

    all_ys = [y for y in yvals_nominal]
    all_ys += [y for y in yvals_up]
    all_ys += [y for y in yvals_dn]
    maxy = max(all_ys)
    miny = min(all_ys)



    # start plotting
    ax = plt.subplot()
    ax.set_ylabel("95% CL limit on $\\sigma(pp\\rightarrow X \\rightarrow hh)$ [pb]",
        horizontalalignment = 'right', y = 1.0, fontsize = 20)
    ax.set_xlabel("Resonance mass, $m_{X}$ [GeV]", horizontalalignment = 'right',
        fontsize = 16, x = 1.0)
    ax.tick_params(axis = 'both', which = 'both', labelsize = 16, direction = 'in',
        labelleft = True, bottom = True, top = True, right = True, left = True)
    ax.set_yscale('log')
    ax.set_ylim(0.1*miny, 10 *maxy)
    ax.grid(color = 'k', which = 'major', linestyle = '--', lw = 1, alpha = 0.2, zorder = 0)

    furthest_x = 700
    plot_sm_value(ax, sm_limit, xbounds = [minx, maxx], name = "NonRes_2L", furthest_x = furthest_x)
    plot_1L_stuff(ax, xbounds = [minx, maxx], furthest_x = furthest_x)

    plot_resonant_value(ax, resonant_limits, name = "Res_2L")


    ## legend
    import matplotlib.patches as mpatches
    import matplotlib.lines as mlines

    leg_handles = []
    leg_labels = []

    # 2L non-resonant handles
    patch_non_res_2L = mpatches.Patch(color = get_color("NonRes_2L_1s"))
    line_non_res_2L = mlines.Line2D([], [], color = get_color("NonRes_2L_Nom"), ls = '--')
    leg_handles.append( (patch_non_res_2L, line_non_res_2L) )
    leg_labels.append( '2$\\ell$ Expected (Non-resonant)' )

    # 2L resonant handles
    patch_res_2L = mpatches.Patch(color = get_color("Res_2L_1s"))
    line_res_2L = mlines.Line2D([],[], color = get_color("Res_2L_Nom"), ls = '--')
    leg_handles.append( (patch_res_2L, line_res_2L) )
    leg_labels.append( '2$\\ell$ Expected (Resonant)' )

    # 1L non-resonant handles
    patch_non_res_1L = mpatches.Patch(color = get_color("NonRes_1L_1s"))
    line_non_res_1L = mlines.Line2D([],[], color = get_color("NonRes_1L_Nom"), ls = '--')
    leg_handles.append( (patch_non_res_1L, line_non_res_1L) )
    leg_labels.append( '1$\\ell$ Expected (Non-resonant)')

    # 1L resonant handles
    patch_res_1L = mpatches.Patch(color = get_color("Res_1L_1s"))
    line_res_1L = mlines.Line2D([], [], color = get_color("Res_1L_Nom"), ls = '--')
    leg_handles.append( (patch_res_1L, line_res_1L) )
    leg_labels.append( '1$\\ell$ Expected (Resonant)')


    ax.legend(leg_handles, leg_labels, loc='best', frameon = False, numpoints = 1)
    

    # labels
    size = 18
    opts = dict(transform = ax.transAxes)
    opts.update( dict(va = 'top', ha = 'left') )
    ax.text(0.05, 0.97, 'ATLAS', size = size, style = 'italic', weight = 'bold', **opts)
    ax.text(0.23, 0.97, "Internal", size = size, **opts)
    ax.text(0.047, 0.9, '$\\sqrt{s} = 13$ TeV, 36.1 fb$^{-1}$', size = 0.75 * size, **opts)

    # SM line
    xvals = [minx, furthest_x]
    yvals = [0.038 for x in xvals]
    ax.plot(xvals, yvals, ls = '--', color = 'k', lw = 1.2)
    ax.text(furthest_x+10, 0.03, 'SM ($0.038$ pb) 1610.07922')


    plt.show()

    

if __name__ == "__main__" :
    main()

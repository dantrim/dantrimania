#!/bin/env python

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
import matplotlib
matplotlib.use("pdf")

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import patches
import numpy as np
import os, sys, argparse
import glob
import scipy.interpolate as interpolate
from scipy.interpolate import spline

class LambdaPoint :
    def __init__(self, lambda_val) :
        self.lambda_val = lambda_val
        self.exp = -1
        self.exp_1s_up = -1
        self.exp_2s_up = -1
        self.exp_1s_dn = -1
        self.exp_2s_dn = -1
        self.obs = -1

    def __str__(self) :
        return "LambdaPoint %.2f : [-2s -1s med +1s +2s | obs] = [%.2f %.2f %.2f %.2f %.2f | %.2f]" % (self.lambda_val, self.exp_2s_dn, self.exp_1s_dn, self.exp, self.exp_1s_up, self.exp_2s_up, self.obs)

def get_lambda_vals_from_dirs(results_dirs) :

    out = []
    for rd in results_dirs :
        lv = rd.strip().split("/")
        lv = [l for l in lv if l]
        lv = lv[-1].split("_")[-1]

        if "neg" in lv :
            lv = lv.replace("neg","")
            lv = -1.0 * float(lv)
        elif "pos" in lv :
            lv = lv.replace("pos","")
            lv = 1.0 * float(lv)

        out.append(lv)
    return out

def mu_to_xsec(mu, args) :

    if not args.bbll :
        den = 0.248 * 0.066979
        xsec_times_filt = 0.008524
        num = mu * xsec_times_filt
        ul = num / den
        return ul

    elif args.bbll :
        bbww_xsec_eff = 0.0085228131
        bbtt_xsec_eff = 0.00808722
        bbzz_xsec_eff = 0.00652987
        
        bbww_den = 0.0166
        bbtt_den = 0.00539
        bbzz_den = 0.000424
        den = bbww_den + bbtt_den + bbzz_den
        
        bbll_xsec_sum = bbww_xsec_eff * bbww_den + bbtt_xsec_eff * bbtt_den + bbzz_xsec_eff * bbzz_den
        mu = float(mu)
        #print("mu_to_xsec: input mu = {}, bbll_xsec_sun = {}".format(mu, bbll_xsec_sum))
        ul = mu * bbll_xsec_sum
        ul /= den
        return ul

    return -1

def get_points(lambda_vals, results_dirs, args) :

    lambda_points = []

    for lvi in lambda_vals :
        lv_str = str(int(abs(lvi)))
        if lvi < 0 :
            lv_str = "neg%s" % lv_str
        elif lvi >= 0 :
            lv_str = "pos%s" % lv_str
        for result in results_dirs :
            #print("result = %s" % result.split("/")[-2].split("_")[-1])
            rval = result.split("/")[-2].split("_")[-1]
            if lv_str != rval : continue
            limit_log_file = glob.glob("{}/UL_*.log".format(result))
            if not limit_log_file :
                print("ERROR Did not find expected limit log file for result {}".format(result))
                sys.exit()
            if len(limit_log_file) > 1 :
                print("ERROR Found more than one limit log file for result {}".format(result))
                sys.exit()
            limit_log_file = limit_log_file[0]

            lines = open(limit_log_file, "r").readlines()
            is_sm = lv_str == "pos1"
            for iline, line in enumerate(lines) :
                line = line.strip()
                if "expected limit (median)" not in line : continue
                obs = float(lines[iline-1].strip().split(":")[-1].split("+")[0])
                exp = float(line.strip().split()[-1])
                exp_1s_up = float(lines[iline+2].strip().split()[-1])
                exp_1s_dn = float(lines[iline+1].strip().split()[-1])
                exp_2s_up = float(lines[iline+4].strip().split()[-1])
                exp_2s_dn = float(lines[iline+3].strip().split()[-1])

                obs = mu_to_xsec(obs, args)
                exp = mu_to_xsec(exp, args)
                exp_1s_up = mu_to_xsec(exp_1s_up, args)
                exp_1s_dn = mu_to_xsec(exp_1s_dn, args)
                exp_2s_up = mu_to_xsec(exp_2s_up, args)
                exp_2s_dn = mu_to_xsec(exp_2s_dn, args)

                lp = LambdaPoint(lvi)
                lp.exp = exp
                lp.exp_1s_up = exp_1s_up
                lp.exp_2s_up = exp_2s_up
                lp.exp_1s_dn = exp_1s_dn
                lp.exp_2s_dn = exp_2s_dn
                lp.obs = obs

                lambda_points.append(lp)
                if args.dbg :
                    print(lp)
                break

#    for lp in lambda_points :
#        print("LVI2 %.2f" % lp.lambda_val)

    return lambda_points

def get_theory_points(args) :

    xsec_correction_factor = 0.929 # take us from 33.4 fb to 31.05 fb

    theory_points = []
    with open("sm_theory_band_values.txt", "r") as sm_file :
        for line in sm_file :
            line = line.strip()
            fields = line.split()
            x_val = float(fields[0])
            y_val = float(fields[1]) * xsec_correction_factor
            y_dn  = float(fields[2]) * xsec_correction_factor
            y_up  = float(fields[3]) * xsec_correction_factor

            lp = LambdaPoint(x_val)
            lp.exp = y_val
            lp.exp_1s_up = y_up
            lp.exp_1s_dn = y_dn
            theory_points.append(lp)
    return theory_points

def smooth_lambda_scan(lambda_scan_points, is_exp) :

    x_lo = -20
    x_hi = 20
    n_x_points = 205

    smooth_output = []

    x_range_input = sorted([l.lambda_val for l in lambda_scan_points])
    x_range_smooth = np.linspace(x_lo, x_hi, n_x_points)

    exp_smooth = spline(x_range_input, [l.exp for l in lambda_scan_points], x_range_smooth)
    obs_smooth = spline(x_range_input, [l.obs for l in lambda_scan_points], x_range_smooth)
    exp_1s_up_smooth = spline(x_range_input, [l.exp_1s_up for l in lambda_scan_points], x_range_smooth)
    exp_1s_dn_smooth = spline(x_range_input, [l.exp_1s_dn for l in lambda_scan_points], x_range_smooth)

    if is_exp :
        exp_2s_up_smooth = spline(x_range_input, [l.exp_2s_up for l in lambda_scan_points], x_range_smooth)
        exp_2s_dn_smooth = spline(x_range_input, [l.exp_2s_dn for l in lambda_scan_points], x_range_smooth)

    for i, x in enumerate(x_range_smooth) :
        lps = LambdaPoint(x)
        lps.exp = exp_smooth[i]
        lps.obs = obs_smooth[i]
        lps.exp_1s_up = exp_1s_up_smooth[i]
        lps.exp_1s_dn = exp_1s_dn_smooth[i]
        if is_exp :
            lps.exp_2s_up = exp_2s_up_smooth[i]
            lps.exp_2s_dn = exp_2s_dn_smooth[i]
        smooth_output.append(lps)
    return smooth_output

def make_lambda_scan_plot(lambda_vals, results_dirs, args) :

    lambda_scan_points = get_points(lambda_vals, results_dirs, args)
    theory_points = get_theory_points(args)
    if args.smooth :
        lambda_scan_points = smooth_lambda_scan(lambda_scan_points, is_exp = True)
        theory_points = smooth_lambda_scan(theory_points, is_exp = False)

    ##
    ## take into account the different relative xsec that we compare to
    ##

    factors = {}
    for ith, thx in enumerate(theory_points) :
        thx_val = thx.lambda_val
        found_it = False
        for i, x in enumerate(lambda_scan_points) :
            x_val = x.lambda_val
            if x_val == thx_val :
                found_it = True
                factor = thx.exp / 0.03105 # relative to SM value
                factors[x_val] = factor
                break
        if not found_it :
            print("ERROR Did not find xsec factor for theory point at x-value of %.2f" % thx_val)
            sys.exit()

    for lp in lambda_scan_points :
        #if lp.lambda_val == 0.0 : continue
        xsec_factor = factors[lp.lambda_val]
        before = lp.exp
        lp.exp *= xsec_factor
        after = lp.exp
        lp.obs *= xsec_factor
        lp.exp_1s_up *= xsec_factor
        lp.exp_1s_dn *= xsec_factor
        lp.exp_2s_up *= xsec_factor
        lp.exp_2s_dn *= xsec_factor

    ##
    ## start plotting
    ##

    theory_color = "#9825fb"
    exp_2s_color = "#fffd38"
    exp_1s_color = "#29fd2f"

    fig, ax = plt.subplots(1,1)#, figsize = (6,6))
    ax.set_yscale("log")

    y_lo = 8e-3
    y_hi = 60
    ax.set_ylim([y_lo, y_hi])

#dhh_text = "$d_{\\mbox{\\textit{\\normalsize{HH}}}}$"

    plt.minorticks_on()
    #ax.set_xlabel(r"$\kappa_{\lambda} = \lambda_{\small{  \mbox{\textit{HHH}}   }}$ / $\lambda_{\small{ \mbox{\textit{SM}}  }}$",
    #ax.set_xlabel("$\\kappa_{\\lambda} = \\lambda_{\\small{HHH}}$ / $\\lambda_{SM}$",
    #ax.set_xlabel(r"$\kappa_{\lambda} = \lambda_{\textit{\normalsize{HHH}}}$ / $\lambda_{\textit{\normalsize{SM}}}$",
    ax.set_xlabel(r"$\kappa_{\lambda}$",
        horizontalalignment = "right", x = 1.0, size = 17)
    ax.set_ylabel(r"95\% CL upper limit on $\sigma ( \mbox{\textit{gg}} \rightarrow \mbox{\textit{HH}} )$ [pb]",
#$\sigma_{\mbox{\normalsize{ggF}}}(\mbox{\textit{pp}} \rightarrow \mbox{\textit{HH}})$ [pb]",
    #ax.set_ylabel(r"95\% CL upper limit on $\sigma_{\mbox{\normalsize{ggF}}}(\mbox{\textit{pp}} \rightarrow \mbox{\textit{HH}})$ [pb]",
    #ax.set_ylabel("95% CL upper limit on $\\sigma_{ggF}(pp \\rightarrow HH)$ [pb]",
        horizontalalignment = "right", y = 1.0, size = 15)

    ax.tick_params(axis = 'both', which = 'both', labelsize = 12, direction = 'in',
        labelleft = True, bottom = True, top = True, left = True, right = True)
    #ax.grid(color = 'k', which = 'major', linestyle = '-', lw = 1, alpha = 0.1)
    ax.tick_params(which = "major", length = 7, zorder = 1e9)
    ax.tick_params(which = "minor", length = 4, zorder = 1e9)

    # plot expected values
    x_vals = [l.lambda_val for l in lambda_scan_points]

    # observed
    y_obs = [l.obs for l in lambda_scan_points]
    ax.plot(x_vals, y_obs, "k-", markersize = 2, label = "Observed")# 95% CL limit")


    # median expected
    y_vals = [l.exp for l in lambda_scan_points]
    ax.plot(x_vals, y_vals, "k--",
        markersize = 2, label = "Expected")# 95% CL limit") # \\rightarrow b\\bar{b}\\ell\\nu\\ell\\nu$ (Expected)")

    # 1 and 2 sigma bands
    y_vals_2s_up = [l.exp_2s_up for l in lambda_scan_points]
    y_vals_2s_dn = [l.exp_2s_dn for l in lambda_scan_points]
    ax.fill_between(x_vals, y_vals_2s_up, y_vals_2s_dn, color = exp_2s_color, linewidth = 0, zorder = 1)

    y_vals_1s_up = [l.exp_1s_up for l in lambda_scan_points]
    y_vals_1s_dn = [l.exp_1s_dn for l in lambda_scan_points]
    ax.fill_between(x_vals, y_vals_1s_up, y_vals_1s_dn, color = exp_1s_color, linewidth = 0, zorder = 1, alpha = 0.75)


    # theory band
    y_vals_th = np.array([l.exp for l in theory_points])
    ax.plot(x_vals, y_vals_th, color = theory_color, zorder = 1)

    y_vals_th_up = np.array([l.exp_1s_up for l in theory_points])
    y_vals_th_dn = np.array([l.exp_1s_dn for l in theory_points])
    ax.fill_between(x_vals, y_vals_th + y_vals_th_up, y_vals_th - y_vals_th_dn, color = theory_color, linewidth = 0, alpha = 0.75, zorder = 1)

    # draw vertical line for the SM kappa lambda scenario
    ax.plot([1,1], [y_lo, y_hi], color = "k", linestyle = "--", zorder = 1, alpha = 0.5, linewidth = 1)
    ax.text(1.5, 0.52*y_hi, "SM ($\\kappa_{\\lambda} =$ 1)")

#1101     r_tick_loc = lower_pad.get_yticks()
#1102     r_tick_labs = ["%s" % x for x in lower_pad.get_yticks() ]
#1103     lower_pad.set_yticks(r_tick_loc)
#1104     lower_pad.set_yticklabels(r_tick_labs)

    x_tick_loc = ax.get_xticks()
    x_tick_lab = ["%d" % int(x) for x in x_tick_loc]
    ax.set_xticks(x_tick_loc)
    ax.set_xticklabels(x_tick_lab)

#1090     upper_pad.set_yticklabels(y_tick_labs)
#1091     if args.logy :
#1092         #print "FOOBS %s" % ["{:.0e}".format(x) for x in upper_pad.get_yticks()]
#1093         #upper_pad.yaxis.set_major_formatter(ScalarFormatter())
#1094         #upper_pad.yaxis.set_major_formatter(OOMFormatter(9, "%1.1f"))
#1095         #upper_pad.ticklabel_format(axis = "y", style = "scientific", scilimits=(2,2))
#1096         y_tick_labs = ["{:.2e}".format(x) for x in upper_pad.get_yticks()]
#1097         y_tick_labs = [r"10$^{\mbox{%s}}$" % str(int(x.split("e")[-1].replace("+",""))) for x in y_tick_labs]
#1098         upper_pad.set_yticklabels(y_tick_labs)
    y_tick_loc = ax.get_yticks()
    y_tick_lab = ["{:.2e}".format(x) for x in ax.get_yticks()]
    y_tick_lab = [r"10$^{\mbox{%s}}$" % str(int(x.split("e")[-1].replace("+",""))) for x in y_tick_lab]
    ax.set_yticklabels(y_tick_lab)

    ax.set_xlim([-21,21])



    # legend
    u1_patch = patches.Patch(color = "#29fd2f", label = "Expected $\\pm$1$\\sigma$")
    u2_patch = patches.Patch(color = "#fffd38", label = "Expected $\\pm$2$\\sigma$")
    theory_line = mlines.Line2D([],[], color = theory_color)
    theory_patch = patches.Patch(color = theory_color, alpha = 0.6, linewidth = 0)
    
    
    new_handles = []
    new_labels = []
    handles, labels = ax.get_legend_handles_labels()
    new_handles.append(handles[0])
    new_labels.append(labels[0])
    obs_handle = None
    obs_label = None
    for ih, h in enumerate(handles) :
        if "expected" in labels[ih].lower() :
            obs_handle = h
            obs_label = labels[ih]
    new_handles.append(obs_handle)
    new_labels.append(obs_label)

    new_handles.append(u1_patch)
    new_labels.append("$\\pm$1$\\sigma$")
    new_handles.append(u2_patch)
    new_labels.append("$\\pm$2$\\sigma$")
    new_handles.append((theory_line, theory_patch))
    new_labels.append("Theory prediction")
    ax.legend(handles = new_handles, labels = new_labels, loc = "lower left", frameon = False)

    # ATLAS text
    opts = dict( transform = ax.transAxes )
    opts.update( dict(va = 'top', ha = 'left') )
    #ax.text(0.035, 0.97, "ATLAS", size = 18, style = "italic", weight = "bold", **opts)
    ax.text(0.035, 0.97, r"\textit{\textbf{ATLAS}}", size = 18, **opts)
#    ax.text(0.23, 0.97, "Internal", size = 18, **opts)
    ax.text(0.035, 0.9, "$\\sqrt{s} =$ 13 TeV, 139 fb$^{-1}$", size = 0.75 * 18, **opts)

    # save
    #fig.show()
    #x = input()
    #fig.savefig("lambda_scan_jul30.pdf", bbox_inches = "tight", dpi = 200)

    olines = []
    olines.append("#LAMBDA\tMINUS2 MINUS1 EXP PLUS1 PLUS2 OBS\n")
    for lp in lambda_scan_points :
        line = "%.4f %.4f %.4f %.4f %.4f %.4f %.4f\n" % (lp.lambda_val
                    ,lp.exp_2s_dn
                    ,lp.exp_1s_dn
                    ,lp.exp
                    ,lp.exp_1s_up
                    ,lp.exp_2s_up
                    ,lp.obs
            )
        olines.append(line)

    with open("exp_lambda_scan.txt", "w") as ofile :
        for iline in olines :
            ofile.write(iline)
    thlines = []
    thlines.append("#LAMBDA\tMINUS1 EXP PLUS1\n")
    for tp in theory_points :
        line = "%.4f %.4f %.4f %.4f\n" % (tp.lambda_val, tp.exp_1s_dn, tp.exp, tp.exp_1s_up)
        thlines.append(line)
    with open("th_lambda_scan.txt", "w") as ofile :
        for iline in thlines :
            ofile.write(iline)
        
    

def main() :

    parser = argparse.ArgumentParser(description = "Make a kappa lambda scan plot from a set of limit logs")
    parser.add_argument("-t", "--table-dir", required = True,
        help = "Provide a path to the directory of limits"
    )
    parser.add_argument("--format", default = "hhSRNN_lambda_",
        help = "Expected format for directory of each limit result stored in the provided table dir"
    )
    parser.add_argument("--bbll", action = "store_true", default = False,
        help = "Consider the combined bbll interpretation"
    )
    parser.add_argument("-d", "--dbg", action = "store_true", default = False,
        help = "Turn on verbose mode"
    )
    parser.add_argument("--smooth", action = "store_true", default = False,
        help = "Smooth the curves"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.table_dir) :
        print("ERROR Provided table dir ({}) is not found".format(args.table_dir))
        sys.exit()

    results = glob.glob("{}/{}*/".format(args.table_dir, args.format))
    print("Found {} scans in provided table dir".format(len(results)))

    lambda_vals = list(set(get_lambda_vals_from_dirs(results)))
    lambda_vals = sorted(lambda_vals)
    print("Found {} lambda vals".format(len(lambda_vals)))
    if args.dbg :
        print(" -> %s" % lambda_vals)

    make_lambda_scan_plot(lambda_vals, results, args)

    
if __name__ == "__main__" :
    main()

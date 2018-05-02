#!/usr/bin/env python

acceptances = "hh_acceptance_tables_36.1.txt"
reco_counts = "may2_wwbb_reco_counts_sig.txt"
sig95_counts = "sig95_exp_limits_36.1.txt"

class SignalPoint :

    def __init__(self, mass = 0) :
        self.mass = mass
        self.n95 = 0
        self.n95_up = 0
        self.n95_dn = 0

        self.acceptance = 0
        self.n_reco = 0
        self.n_truth = 0

        self.efficiency = 0

    def denominator(self) :

        br_ww = 0.21
        br_bb = 0.57
        br = 2 * br_ww * br_bb
        den = br * float(self.efficiency) * float(self.acceptance)

        return den

    def numerator(self, sys = 0) :

        number = self.n95
        if sys > 0 :
            number = self.n95 + self.n95_up
        elif sys < 0 :
            number = self.n95 - self.n95_dn

        return float(number) / 36.1

def main() :

    hh_sigs = []

    
    lines = [l.strip() for l in open(sig95_counts).readlines()]
    for line in lines :
        if line.startswith('#') : continue
        if not line : continue
        line = line.split()

        s = SignalPoint(int(line[0]))

        s.vis_xsec = float(line[1])
        s.n95 = float(line[2])
        s.n95_up = float(line[3])
        s.n95_dn = float(line[4])

        print "Signal Point : %d  vis_xsec %.2f  ( %.2f  %.2f  %.2f ) " % (s.mass, s.vis_xsec, s.n95, s.n95_up, s.n95_dn)
    
        hh_sigs.append(s)

    lines = [l.strip() for l in open(reco_counts).readlines()]
    for line in lines :
        if not line : continue
        if line.startswith('#') : continue
        l = line.split()
        mass = int(l[0])
        for hh in hh_sigs :
            if hh.mass != mass : continue
            hh.n_reco = float(l[1])

    lines = [l.strip() for l in open(acceptances).readlines()]
    for line in lines :
        if not line : continue
        if line.startswith('#') : continue
        l = line.split()
        mass = int(l[0])
        for hh in hh_sigs :
            if hh.mass != mass : continue
            hh.acceptance = float(l[1])
            hh.n_truth = float(l[5])

    for hh in hh_sigs :
        if float(hh.n_truth) != 0. :
            hh.efficiency = float(hh.n_reco) / float(hh.n_truth)
        else :
            hh.efficiency = -1

    ofilename = "ul_xsec_plot_points.txt"
    ofile = open(ofilename, 'w')
    header = "#SIG EXP EXPUP EXPDN\n"
    ofile.write(header)
    for hh in hh_sigs :
        den = float(hh.denominator())
        num = float(hh.numerator(0))
        num_up = float(hh.numerator(1))
        num_dn = float(hh.numerator(-1))

        val = 0.
        val_up = 0.
        val_dn = 0.
        if den != 0. :
            val = num / den
            val_up = num_up / den
            val_dn = num_dn / den

            val *= 1e-3
            val_up *= 1e-3
            val_dn *= 1e-3
        else :
            val = -1
            val_up = -1
            val_dn = -1
        
        line = "%d  %.4f  %.4f  %.4f" % (int(hh.mass), val, val_up, val_dn)
        ofile.write(line + "\n")

    

    

if __name__ == "__main__" :

    main()

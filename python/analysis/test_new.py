
#import dantrimania.python.analysis.utility.plotting.histogram1d as histogram1d
from dantrimania.python.analysis.utility.plotting.histogram1d import histogram1d
from dantrimania.python.analysis.utility.plotting.histogram_stack import histogram_stack
from dantrimania.python.analysis.utility.plotting.ratio_canvas import ratio_canvas
from dantrimania.python.analysis.utility.plotting.canvas import canvas
from dantrimania.python.analysis.utility.plotting.plot1d import plot1d

import numpy as np

def main() :

    bins = [1, 0, 5]
    h = histogram1d("test_histo", binning = bins)
    h2 = histogram1d("test_histo2", binning = bins)

    #test_data_0 = np.array([1,2,2,3,3,3,3.2])
    test_data_0 = np.array([1,2,3])
    w0 = 1 * np.ones(len(test_data_0))
    #w0[1] = 4
    h.fill(test_data_0, w0)
    test_data_1 = np.array([1,4,4,2,2])
    w1 = 0.5 * np.ones(len(test_data_1))
    h2.fill(test_data_1, w1)
    #h.add_overflow()
    #h2.add_overflow()

    #print "data : %s" % h.data
    #print "weights : %s" % h.weights
    #print "weights2 : %s" % h.weights2
    #print "sum wweights2 : %.2f" % np.sum(h.weights2)
    #print "bins : %s" % h.bins
    #print "nbins : %s" % h.nbins()
    #print "histogram : %s" % h.histogram
    ##integral_bounds = [-3, 4.0]
    #integral_bounds = [0,-1]
    #raw = False
    #print "integral bounds = %s" % integral_bounds
    #print "integral : %.2f" % h.integral(integral_bounds, raw = raw)
    #integral, error = h.integral_and_error(integral_bounds, raw = raw)
    #print "integral and error : %.2f +/- %.2f" % ( integral, error )
    #print "bins : %s" % h.bins
    #print "bin centers : %s" % [ "%.2f" % x for x in h.bin_centers() ]

    print "H Y-ERROR        : %s" % h.y_error()
    print "H2 Y-ERROR       : %s" % h2.y_error()

    stack = histogram_stack("hstack", binning = bins)
    stack.add(h)
    stack.add(h2)
    print stack.counts
    print "stack order %s" % stack.order
    stack.sort()
    stack.print_counts()
    print "stack order after sort %s" % stack.order

    print "STACK Y-ERROR    : %s" % stack.total_histo.y_error()
    print "STACK BINNING    : %s" % stack.total_histo.binning

    print 45 * '-'
    htotal = stack.total_histo
    print "htotal bin content : %s" % htotal.histogram
    print "htotal integral : %.2f +/- %.2f" % ( htotal.integral_and_error()[0], htotal.integral_and_error()[1])


    print "htotal maximum = ", htotal.maximum()
    print "htotal minimum = ", htotal.minimum()

    print 45 * '-'
    rc = ratio_canvas("test_ratio_canvas")
    print "logy = ", rc.logy

    rc.labels = ['x value', 'y value']
    rc.rlabel = 'Hello / Dolly'
    rc.build()
    rc.fig.savefig("test_rc.pdf", bbox_inches='tight')

    print 45 * '-'
    c = canvas("test_canvas") 
    c.labels = ['x value', 'y value']
    c.x_bounds = [0.0, 5.0]
    c.y_bounds = [0.0, 10]
    c.build()
    xvals = [0, 1,2,3,4]
    yvals = [0, 2, 4, 6, 8]
    c.pad.plot(xvals, yvals, 'ro')
    c.fig.savefig("test_canvas.pdf", bbox_inches='tight')

    # test divide
    print 45 * '-'
    hdivide = h.divide(h2)
    print "numberator = ", h.histogram
    print "dneome     = ", h2.histogram
    print "divided    = ", hdivide

    print 45 * '-'
    bins = [1, 0, 10]
    hm = histogram1d("mean_histo", binning = bins)
    mean_data = np.array([5,0,10,10,10])
    w = np.ones(len(mean_data))
    hm.fill(mean_data, w)
    print "mean data : %s" % hm.histogram
    print "mean      : %.2f" % hm.mean()
    print "std       : %.2f" % hm.std()
    print "var       : %.2f" % hm.var()

    print 45 * '-'
    p = plot1d('test_plot', 'l0_pt')
    p.bounds = [10, 0, 200]
    p.units = "GeV"
    print "plot name = %s" % p.name
    print "variable  = %s" % p.vartoplot
    print "binning   = %s" % p.binning
    print "bounds    = %s" % p.bounds
    print "bin width = %.2f" % p.bin_width
    print "xlow      = %.2f" % p.x_low
    print "xhigh     = %.2f" % p.x_high
    print "units     = %s" % p.units

if __name__ == "__main__" :
    main()

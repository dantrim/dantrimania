#!/usr/bin/env python
import numpy as np

def overlay_histos( pad = None, samples = [], variable_name = "",
                        bins = [], absvalue = False) :

    """
    Draws un-filled histograms for each of the samples in 'samples' for
    the variable 'variable_name'
    """

    sample_histos = []
    sumw2_histos = []
    weights = []
    weights2 = []

    colors = []
    labels = []

    for sample in samples :
        histogram = []
        sumw2_histogram = []

        sample_weights = []
        sample_weights2 = []

        chain = sample.chain()
        for ic, c in enumerate(chain) :
            data = c[variable_name]
            lumis = np.ones(len(data))
            lumis[:] = sample.scalefactor
            w = lumis * c['eventweight']
            sample_weights += list(w)

            w2 = lumis * c['eventweight']
            w2 = w2 ** 2
            sample_weights2 += list(w2)

            if absvalue :
                data = np.absolute(data)
            histogram += list(data)
            sumw2_histogram += list(data)

        labels.append(sample.displayname)
        colors.append(sample.color)

        sample_histos.append(histogram)
        sumw2_histos.append(sumw2_histogram)
        weights.append(sample_weights)
        weights2.append(sample_weights2)

    # add overflow
    sample_histos = [np.clip(s, bins[0], bins[-1]) for s in sample_histos]
    sy, sx, _ = pad.hist( sample_histos, bins = bins,
                            color = colors,
                            weights = weights,
                            label = labels,
                            ls = '--',
                            stacked = False,
                            histtype = 'step',
                            lw = 1.5)

    return labels, colors, sy, sx

def draw_bounding_line( pad = None, xvals = None, yvals = None, bin_width = None,
                        linestyle = '-',
                        linecolor = 'k',
                        label = 'Total SM',
                        linewidth = 2) :
    """
    Draw a bounding line on a histogram

    pad : pad to draw on
    xvals : array of values containing x-values of the left-edges of the histogram
                bins
    yvals : bin content of each of the histogram bins
    bin_width : histogram bin width (assumes fixed bin width)
    linestyle : style of the line to use for the bounding line
    label : label for the line object
    linewidth : width of the line to use for the bounding line
    """

    x = []
    y = []
    n_points = len(xvals)
    for i in xrange(n_points) :
        x.append(xvals[i])
        x.append(xvals[i] + bin_width)
        y.append(yvals[i])
        y.append(yvals[i])

    # add line for right most edge 
    x.append(x[-1])
    miny = min(yvals)
    y.append(1e-3 * miny)
    pad.plot( x, y, ls = linestyle, color = linecolor, label = label, lw = linewidth )

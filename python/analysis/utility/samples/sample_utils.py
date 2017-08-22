#!/usr/bin/env python

def categorize_samples(samples) :
    """ provided an input list of sample objects, break them into
        separate list of backgrounds, signal, and data """

    backgrounds = []
    signals = []
    data = None
    for s in samples :
        if not s.is_data and not s.is_signal :
            backgrounds.append(s)
        elif not s.is_data and s.is_signal :
            signals.append(s)
        elif s.is_data and not s.is_signal :
            if data :
                print "ERROR More than one of the loaded samples is categorized as Data"
                sys.exit()
            data = s

    return backgrounds, signals, data

def get_variables_from_tcut(tcut) :

    operators = ["==", ">=", "<=", ">", "<", "!=", "*", "-"]
    logics = ["&&", "||", ")", "(", "abs"]
    vars_only = tcut
    for op in operators :
        vars_only = vars_only.replace(op, " ")
    for log in logics :
        vars_only = vars_only.replace(log, " ")
    vars_only = vars_only.split()
    out = []
    for v in vars_only :
        if v not in out and not v.isdigit() :
            try :
                flv = float(v)
            except :
                out.append(v)
    return out

def get_required_variables(plots, region) :
    variables = []
    for p in plots :
        if p.vartoplot not in variables :
            variables.append(p.vartoplot)

    tcut = region.tcut
    selection_variables = get_variables_from_tcut(tcut)
    for sv in selection_variables :
        if sv not in variables :
            variables.append(sv)

    # always append eventweight
    variables.append('eventweight')

    return variables

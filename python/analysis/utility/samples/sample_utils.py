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

def find_occurrences(string, substr) :
    start = 0
    while True :
        start = string.find(substr, start)
        if start == -1 : return
        yield start
        start += len(substr)

def index_selection_string(selection_str, chain_name, varlist) :
    tcut = selection_str
    tcut = tcut.replace("&&", " & ")
    tcut = tcut.replace("||", " | ")
    var_strings = []
    var_str_map = {}

    logic = ['&', '|']
    for var in varlist :
        if var in tcut :
            new_str = "(%s['%s']" % ( chain_name, var ) 
            var_strings.append(new_str)
            tcut = tcut.replace(var, new_str)
            occurrences = find_occurrences(tcut, new_str)
            for idx in occurrences :
                sub = ""
                for i, c in enumerate(tcut[idx:]) :
                    if c in logic :
                        break
                    sub += c
                substr_to_replace = sub
                substr = substr_to_replace + ") "
                tcut = tcut.replace(substr_to_replace, substr)

    for l in logic :
        tcut = tcut.replace(")%s" % l, ") %s" % l)

    return tcut

class SimpleSample :
    def __init__(self, name = "", filename = "", color = "") :
        self.name = name
        self.filename = filename
        self.color = color

def chunk_generator(h5_dataset, chunksize = 100000) :
    for x in range(0, h5_dataset.size, chunksize) :
        yield h5_dataset[x:x+chunksize]

def get_valid_idx(input_array) :
    lo = input_array > -np.inf
    hi = input_array < np.inf
    return lo & hi

#!/usr/bin/env python

import os
import errno
import sys

def mkdir_p(path) :
    try :
        os.makedirs(path)
    except OSError as exc :
        if exc.errno == errno.EEXIST and os.path.isdir(path) :
            pass
        else :
            raise

def file_exists(filename) :
    if filename == "" :
        print "BAD FILE Filename is empty"
        return False
    if not os.path.isfile(filename) :
        print "BAD FILE File '%s' not found" % filename
        return False
    return True

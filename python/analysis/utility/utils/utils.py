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

#!/usr/bin/env python

import sys, os
from argparse import ArgumentError

autoDetectEnabled = True
FAN_MODE_FILENAME = 'fan_mode' # name of control file
FAN_MODE_FULLPATH = '' # Custom path should be provided here and autoDetectEnabled set to false

# lists all possible fan_mode control files
def listFanModeFiles():
    searchResults = []
    
    for root, dirs, files in os.walk('/sys/devices/'):
        if FAN_MODE_FILENAME in files:
            searchResults.append(os.path.join(root, FAN_MODE_FILENAME))
            
    return searchResults

def autoDetect():
    global FAN_MODE_FULLPATH
    
    modes = listFanModeFiles()

    if(len(modes) == 1): # auto detect only possible if we know the one file to use. else up to user to define.
        FAN_MODE_FULLPATH = modes[0]
        print 'Auto detected file_mode path:' + FAN_MODE_FULLPATH
    else:
        Exception('Could not auto detect file_mode path. Please disable autodetect and specify fan_mode file.')


if(autoDetectEnabled):
    autoDetect()

if(len(FAN_MODE_FULLPATH) > 1):
    f = open(FAN_MODE_FULLPATH, 'w')
    
    try:
        mode = sys.argv[1] # retrieve mode argument
        
        if(not mode.isdigit()):
            raise TypeError('Second argument must be numerical.')
        
        f.write(mode)
    except IndexError:
        raise ArgumentError('No second argument to use as fan mode')
else:
    raise Exception('Invalid fan mode file provided. Please see documentation.')
#!/usr/bin/env python

import sys

FAN_MODE_FILE = '/sys/devices/pci0000:00/0000:00:1f.0/PNP0C09:00/VPC2004:00/fan_mode' #TODO find a way to auto detect this
#FAN_MODE_FILE = '/home/alex/pythonTest99.txt'

f = open(FAN_MODE_FILE, 'w')

mode = sys.argv[1] # retrieve the mode argument

if(not mode.isdigit()):
    raise TypeError('Second argument must be numerical.')

f.write(mode) 
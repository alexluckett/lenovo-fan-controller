# LenovoFanControl
Fan control indicator for Ubuntu's Unity desktop.

Provided as-is without support, guarantees or warranty. Use entirely at your own risk.
Developed for a Lenovo z570 running Ubuntu 14.10 w/ Unity. May work on other Lenovo Ideapad systems - see the 'Set up' section.

## Setup
`'FAN_MODE_FILE'` in fileWriter may need to be altered to point to the location of your fan_mode file. This can be found by running the following command in a terminal:

`find /sys/devices -name "fan_mode"`

Copy and paste the file path into the `'FAN_MODE_FILE'` variable and then run fanControl.py.

Later versions of this software will have autodetection functionality.
 
## Requirements
* Python (developed using v2.7)
* Desktop environment w/ support for Appindicators (e.g Unity)
* gksudo package (if not present: `sudo apt-get install gksu`)

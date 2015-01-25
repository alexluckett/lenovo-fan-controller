#!/usr/bin/env python
# Lenovo Ideapad Fan control indicator for the Unity desktop

# Provided as-is without support, guarantees or warranty. Use entirely at your own risk.
# Developed for a Lenovo z570 running Ubuntu 14.10 w/ Unity. May work on other Lenovo Ideapad systems 
# although FAN_MODE_FILE in fileWriter may need to be altered to point to the location of your fan_mode file.

from gi.repository import Gtk
from gi.repository import AppIndicator3 as Appindicator
import subprocess, os

iconName = "stock_weather-fog"

def setFanSpeed(widget, modeNumber):
	modeNumber = modeNumber[0]
	
	if modeNumber in getFanSpeeds():
		filePath = '%s/fileWriter.py' % getCurrentPath()
		
		# run the fileWriter process as root, passing in the current mode as an argument
		subprocess.call(['gksudo', 'python', filePath, str(modeNumber)]) 
		
		print modeNumber,': ' + getFanSpeeds()[modeNumber], 'applied'
	else:
		raise ValueError('Invalid fan mode entered: %s' % modeNumber)

def getFanSpeeds():
	return {0:'Silent Mode', 1:'Standard Mode', 2:'Dust Cleaning', 4:'Thermal Dissipation'}

def getCurrentPath():
	return os.path.dirname(os.path.abspath(__file__)) # retrieve the full path of this file
	
def displayAbout(widget):
	global iconName
	
	about = Gtk.AboutDialog()
	about.set_title('About Fan Control for Lenovo')
	about.set_program_name('Lenovo Ideapad Fan Control')
	about.set_version('v0.1 alpha')
	about.set_comments('THIS IS UNSUPPORTED SOFTWARE, USE ENTIRELY AT YOUR OWN RISK.')
	about.set_website_label('http://github.com/alexluckett/LenovoFanControl')
	about.set_website('http://github.com/alexluckett/LenovoFanControl')
	
	iconTheme = Gtk.IconTheme.get_default()
	icon = iconTheme.load_icon(iconName, 64, Gtk.IconLookupFlags.FORCE_SVG) # get 64x64 SVG icon
	
	if(icon): # only apply if present
		about.set_logo(icon)
		
	about.run()
	about.destroy()
	
def addMenuEntry(text, parent, function, *args):
	entry = Gtk.MenuItem(text)
	parent.append(entry)
	
	if(function is not None): # if function is present, connect to entry
		if(len(args) == 0):
			entry.connect("activate", function)
		else:
			entry.connect("activate", function, args)
		
	entry.show()
	
def addDivider(parent):
	dividerEntry = Gtk.SeparatorMenuItem()
	parent.append(dividerEntry)
	dividerEntry.show()
	
def terminate(widget):
	Gtk.main_quit()
	
def main():
	global iconName
	
	indicator = Appindicator.Indicator.new (
					"Lenovo Fan Control",
					iconName, # temporarily using this until I make my own
					Appindicator.IndicatorCategory.APPLICATION_STATUS
				)
	
	indicator.set_status (Appindicator.IndicatorStatus.ACTIVE)
	
	menu = Gtk.Menu()
	
	# fan speed entries
	for key in getFanSpeeds():
 		text = '%s - %s' %(key, getFanSpeeds()[key]) # Text = 'ModeNo - Text'
		addMenuEntry(text, menu, setFanSpeed, key)
		
	addDivider(menu) # divider entry
	addMenuEntry('About', menu, displayAbout) # about menu item
	addMenuEntry('Quit', menu, terminate) # terminate menu item
	
	# apply menu to indicator
	indicator.set_menu(menu)
	
	Gtk.main()

if __name__ == "__main__":
	main()
else:
	print 'Please run fancontrol.py directly'
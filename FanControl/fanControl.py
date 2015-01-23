#!/usr/bin/env python
# Lenovo Ideapad Fan control indicator for the Unity desktop

# Provided as-is without support, guarantees or warranty. Use entirely at your own risk.
# Developed for a Lenovo z570 running Ubuntu 14.10 w/ Unity. May work on other Lenovo Ideapad systems 
# although FAN_MODE_FILE in fileWriter may need to be altered to point to the location of your fan_mode file.

from gi.repository import Gtk
from gi.repository import AppIndicator3 as Appindicator
import subprocess, os

def setFanSpeed(widget, modeNumber):
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
	about = Gtk.AboutDialog()
	about.set_title('About Fan Control for Lenovo')
	about.set_program_name('Lenovo Ideapad Fan Control')
	about.set_version('v0.1 alpha')
	about.set_comments('THIS IS UNSUPPORTED SOFTWARE, USE ENTIRELY AT YOUR OWN RISK.')
	about.set_website_label('http://github.com/alexluckett/LenovoFanControl')
	about.set_website('http://github.com/alexluckett/LenovoFanControl')
	
	about.run()
	about.destroy()
	
def terminate(widget):
	Gtk.main_quit()
	
def main():
	indicator = Appindicator.Indicator.new (
							"Lenovo Fan Control",
							"stock_weather-fog", # temporarily using this until I make my own
							Appindicator.IndicatorCategory.APPLICATION_STATUS
						)
	
	indicator.set_status (Appindicator.IndicatorStatus.ACTIVE)
	
	menu = Gtk.Menu()
	
	# fan speed entries
	for key in getFanSpeeds():
		text = '%s - %s' %(key, getFanSpeeds()[key])
		entry = Gtk.MenuItem(text)
		
		menu.append(entry)
		entry.connect("activate", setFanSpeed, key)
		
		entry.show()
		
	# divider entry
	dividerEntry = Gtk.SeparatorMenuItem()
	menu.append(dividerEntry)
	dividerEntry.show()
	
	# about menu item
	aboutEntry = Gtk.MenuItem('About')
	menu.append(aboutEntry)
	aboutEntry.connect("activate", displayAbout)
	aboutEntry.show()
	
	# terminate menu item
	quitEntry = Gtk.MenuItem('Quit')
	menu.append(quitEntry)
	quitEntry.connect("activate", terminate)
	quitEntry.show()
	
	# apply menu to indicator
	indicator.set_menu(menu)
	
	Gtk.main()

if __name__ == "__main__":
	main()
else:
	print 'Please run fancontrol.py directly'
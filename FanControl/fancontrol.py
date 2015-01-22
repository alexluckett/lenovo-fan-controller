#!/usr/bin/env python
# Fan control indicator for the Unity desktop - Ubuntu 14.10

#from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import AppIndicator3 as Appindicator

currentFanMode = 0

def setFanSpeed(widget, modeNumber):
	if modeNumber in getFanSpeeds():
		#global currentFanMode
		file = '' #TODO file path
		writeToFile(file, modeNumber)
		
		print modeNumber,': ' + getFanSpeeds()[modeNumber], 'applied'
	else:
		print 'Invalid fan mode entered: %s' % modeNumber

def getFanSpeeds():
	return {0:'Silent Mode', 1:'Standard Mode', 2:'Dust Cleaning', 4:'Thermal Dissipation'}

# TODO implement
def writeToFile(file, content):
	return 

def displayAbout(widget):
	about = Gtk.AboutDialog()
	about.set_title('About Fan Control for Lenovo')
	about.set_program_name('Lenovo z570 Fan Control')
	about.set_version('v0.1 alpha')
	about.set_comments('THIS IS UNSUPPORTED SOFTWARE, USE ENTIRELY AT YOUR OWN RISK.')
	about.set_website_label('http://github.com/alexluckett/LenovoFanControlGUI')
	about.set_website('http://github.com/alexluckett/LenovoFanControl')
	
	about.run()
	about.destroy()

if __name__ == "__main__":
	indicator = Appindicator.Indicator.new (
										"example-simple-client",
										"stock_weather-fog", # temporarily using this until I make my own
										Appindicator.IndicatorCategory.APPLICATION_STATUS)
	
	indicator.set_status (Appindicator.IndicatorStatus.ACTIVE)
	
	menu = Gtk.Menu()
	
	# fan speeds
	for key in getFanSpeeds():
		text = '%s - %s' %(key, getFanSpeeds()[key])
		entry = Gtk.MenuItem(text)
		
		menu.append(entry)
		entry.connect("activate", setFanSpeed, key)
		
		entry.show()
		
	# misc options
	dividerEntry = Gtk.MenuItem('')
	menu.append(dividerEntry)
	dividerEntry.show()
	
	aboutEntry = Gtk.MenuItem('About')
	menu.append(aboutEntry)
	aboutEntry.connect("activate", displayAbout)
		
	aboutEntry.show()
		
	indicator.set_menu(menu)
	
	Gtk.main()
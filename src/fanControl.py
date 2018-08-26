#!/usr/bin/env python
# Lenovo Ideapad Fan control indicator for the Unity desktop

# Provided as-is without support, guarantees or warranty. Use entirely at your own risk.
# Developed for a Lenovo z570 running Ubuntu 14.10 w/ Unity. May work on other Lenovo Ideapad systems 
# although FAN_MODE_FILE in fileWriter may need to be altered to point to the location of your fan_mode file.

from gi.repository import Gtk
from gi.repository import AppIndicator3 as Appindicator
import subprocess, os

class FanController():
	def setFanSpeed(self, widget, modeNumber):
		modeNumber = modeNumber[0]
		
		if modeNumber in self.getFanSpeeds():
			filePath = '{path}/fileWriter.py'.format(path=self.getCurrentPath())
			
			try:
				# run the fileWriter process as root, passing in the current mode as an argument
				subprocess.check_output(['gksudo', 'python', filePath, str(modeNumber)])
				
				print modeNumber,': ' + self.getFanSpeeds()[modeNumber] + ' applied'
			except CalledProcessError:
				displayErrorMessage('Unable to write to fan mode file. Invalid file or autodetection failed. Please see documentation.')
			
		else:
			raise ValueError('Invalid fan mode entered: {mode}'.format(mode=modeNumber))
	
	def getFanSpeeds(self):
		return {
			0:'Silent Mode',
			1:'Standard Mode',
			2:'Dust Cleaning',
			4:'Thermal Dissipation'
		}
		
	def getCurrentPath(self):
		return os.path.dirname(os.path.abspath(__file__)) # retrieve the full path of this file

class UserInterface():
	iconName = "stock_weather-fog" 
	
	def __init__(self, fanController):
		self.fanController = fanController
	
	def showIndicator(self):		
		indicator = Appindicator.Indicator.new (
					"Lenovo Fan Control",
					UserInterface.iconName, # temporarily using this until I make my own
					Appindicator.IndicatorCategory.APPLICATION_STATUS
				)
	
		indicator.set_status (Appindicator.IndicatorStatus.ACTIVE)
		
		menu = Gtk.Menu()
	
		fanSpeeds = self.fanController.getFanSpeeds()
		# fan speed entries
		for key in fanSpeeds:
	 		text = '{text}'.format(text = fanSpeeds[key]) # Text = 'ModeNo - Text'
			self.__addMenuEntry(text, menu, self.fanController.setFanSpeed, key)
		
		self.__addDivider(menu) # divider entry
		self.__addMenuEntry('About', menu, self.__displayAbout) # about menu item
		self.__addMenuEntry('Quit', menu, self.terminate) # terminate menu item
		
		# apply menu to indicator
		indicator.set_menu(menu)
		
		Gtk.main()
		
	def __displayAbout(self, widget):
		about = Gtk.AboutDialog()
		about.set_title('About Fan Control for Lenovo')
		about.set_program_name('Lenovo Ideapad Fan Control')
		about.set_version('v0.1 alpha')
		about.set_comments('THIS IS UNSUPPORTED SOFTWARE, USE ENTIRELY AT YOUR OWN RISK.')
		about.set_website_label('http://github.com/alexluckett/LenovoFanControl')
		about.set_website('http://github.com/alexluckett/LenovoFanControl')
		
		iconTheme = Gtk.IconTheme.get_default()
		icon = iconTheme.load_icon(UserInterface.iconName, 64, Gtk.IconLookupFlags.FORCE_SVG) # get 64x64 SVG icon
		
		if(icon): # only apply if present
			about.set_logo(icon)
			
		about.run()
		about.destroy()
		
	def __displayErrorMessage(text):
		error = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, text)
		error.set_title('Lenovo Ideapad Fan Control Error')
		error.run()
		error.destroy()
		
	def __addMenuEntry(self, text, parent, function, *args):
		entry = Gtk.MenuItem(text)
		parent.append(entry)
		
		if(function is not None): # if function is present, connect to entry
			if(len(args) == 0):
				entry.connect("activate", function)
			else:
				entry.connect("activate", function, args)
			
		entry.show()
		
	def __addDivider(self, parent):
		dividerEntry = Gtk.SeparatorMenuItem()
		parent.append(dividerEntry)
		dividerEntry.show()
		
	def terminate(self, widget):
		Gtk.main_quit()
	
def main():
		ui = UserInterface(FanController())
		ui.showIndicator()

if __name__ == "__main__":
	main()
else:
	print 'Please run fancontrol.py directly'
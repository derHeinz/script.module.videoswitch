# -*- coding: utf-8 -*-

import sys
import subprocess
import xbmcaddon
import xbmc
import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addonpath = addon.getAddonInfo('path')

def translate(text):
	return addon.getLocalizedString(text).encode("utf-8")

def showOptions(main=None):
	headings = ["to HDMI", "to LVDS", "to VGA", "restart"]
	handlers = [main.toHDMI, main.toLVDS, main.toVGA, main.restart]

	index = xbmcgui.Dialog().select(addonname, headings)
	if index >= 0:
		handlers[index]()

class main():

	def __init__(self):
		arg = self.getArg()
		showOptions(self)
		
	def getArg(self):
		return sys.argv[-1]
		
	def toHDMI(self):
		res = "1280x720"
		#self._exec(["xrandr", "--output", "HDMI-1", "--mode", res])
		#self._exec(["xrandr", "--output", "HDMI-1", "--primary"])
		#self._exec(["xrandr", "--output", "LVDS-1", "--off"])
		#self._exec(["xrandr", "--output", "VGA-1", "--off"])
		#self._exec(["xrandr", "--output", "HDMI-1", "--auto"])
		#self._exec(["xrandr", "--output", "HDMI-1", "--mode", res])
		#self.restart()
		self._toMode("HDMI-1", "LVDS-1", "HDMI-1", res)

	def toLVDS(self):
		#self._exec(["xrandr", "--output", "LVDS-1", "--primary"])
		#self._exec(["xrandr", "--output", "LVDS-1", "--auto"])
		#self._exec(["xrandr", "--output", "HDMI-1", "--off"])
		#self._exec(["xrandr", "--output", "VGA-1", "--off"])
		#self._exec(["xrandr", "--output", "LVDS-1", "--auto"])
		#self.restart()
		self._toMode("LVDS-1", "VGA-1", "HDMI-1")

	def toVGA(self):
		res = "1024x786"
		self._toMode("VGA-1", "LVDS-1", "HDMI-1", res)
		
	def _toMode(self, main, off_1, off_2, res=None):
		if res is not None:
			self._exec(["xrandr", "--output", main, "--mode", res])
		self._exec(["xrandr", "--output", main, "--primary"])
		self._exec(["xrandr", "--output", off_1, "--off"])
		self._exec(["xrandr", "--output", off_2, "--off"])
		self._exec(["xrandr", "--output", main, "--auto"])
		if res is not None:
			self._exec(["xrandr", "--output", main, "--mode", res])
		self.restart()
		
	def restart(self):
		self._exec(["systemctl", "restart", "kodi"])
		
	def back(self):
		pass
		
	def _exec(self, cmds):
		try:
			subprocess.check_call(cmds)
			xbmc.log('script.video.switch: Executing {0}'.format(cmds), xbmc.LOGNOTICE)
			return True
		except subprocess.CalledProcessError as cpe:
			xbmc.log('script.video.switch: Error {1} running {0}'.format(cpe, cmds), xbmc.LOGERROR)
			return False
		
		

main()
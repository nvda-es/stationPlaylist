# Station Playlist Studio
# An app module and global plugin package for NVDA
# Copyright 2011, 2013, Geoff Shang, Joseph Lee and others, released under GPL.
# The primary function of this appModule is to provide meaningful feedback to users of SplStudio
# by allowing speaking of items which cannot be easily found.
# Version 0.01 - 7 April 2011:
# Initial release: Jamie's focus hack plus auto-announcement of status items.
# Additional work done by Joseph Lee and other contributors.
# For SPL Studio Controller, focus movement and other utilities, see the global plugin version of this app module.

# Because of different interfaces between 4.x and 5.x, we need to come up with a way to handle both.
# Minimum version: SPL 4.33, NvDA 2013.3.

import controlTypes
from controlTypes import ROLE_GROUPING
import appModuleHandler
import api
import ui
import gui
import wx
import winUser
from ctypes import windll
from NVDAObjects.IAccessible import IAccessible
import tones
from functools import wraps
import addonHandler
addonHandler.initTranslation()

# The finally function for the toggle scripts in this module (source: Tyler Spivey's code).
def finally_(func, final):
	"""Calls final after func, even if it fails."""
	def wrap(f):
		@wraps(f)
		def new(*args, **kwargs):
			try:
				func(*args, **kwargs)
			finally:
				final()
		return new
	return wrap(final)

# Try both 4.x and 5.x interfaces.
user32 = windll.user32
SPLWin = user32.FindWindowA("SPLStudio", None)

# Use IPC tags to decide what to do for 4.x and 5.x (may look similar to global plugin version).
SPLMinVersion = 500 # Check the version string against this. If it is less, use a different procedure for some routines.

class AppModule(appModuleHandler.AppModule):

	# Translators: Script category for Station Playlist commands in input gestures dialog.
	scriptCategory = _("Station Playlist Studio")

	# Some useful variables:
	beepAnnounce = False # Play beeps instead of announcing toggles.
	SPLCurVersion = winUser.sendMessage(SPLWin, 1024, 0, 2) # The version test variable.

	# GS: The following was written by James Teh <jamie@NVAccess.org
	#It gets around a problem where double focus events are fired when moving around the playlist.
	#Hopefully it will be possible to remove this when it is fixed in Studio.>
	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "TListView" and obj.role in (controlTypes.ROLE_CHECKBOX, controlTypes.ROLE_LISTITEM) and controlTypes.STATE_FOCUSED not in obj.states:
			# These lists seem to fire a focus event on the previously focused item before firing focus on the new item.
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False
		# Radio button group names are not recognized as grouping, so work around this.
		if obj.windowClassName == "TRadioGroup": obj.role = ROLE_GROUPING

	# Check the following variable for end of track announcement.
	SPLEndOfTrackTime = "00:05" # Should be adjustable by the user in the end. Also find a way to announce this even if SPL Studio is minimized.

	# Automatically announce mic, line in, etc changes
	# These items are static text items whose name changes.
	# Note: There are two status bars, hence the need to exclude Up time so it doesn't announce every minute.
	# Unfortunately, Window handles and WindowControlIDs seem to change, so can't be used.
	# Bonus: if the user sets beep announce to on, beeps will be heard instead of announcements.
	# Bonus 2: announce when the track is about to end.
	def event_nameChange(self, obj, nextHandler):
		# Do not let NvDA get name for None object when SPL window is maximized.
		if obj.name == None: return
		else:
			if obj.windowClassName == "TStatusBar" and not obj.name.startswith("  Up time:"):
				# Special handling for Play Status
				if obj.IAccessibleChildID == 1:
					# Strip off "  Play status: " for brevity
					ui.message(obj.name[15:])
				else:
					# Even with beeps enabled, be sure to announce scheduled time.
					if self.beepAnnounce and obj.name.startswith("Scheduled for"): ui.message(obj.name)
					elif self.beepAnnounce:
						# User wishes to hear beeps instead of words. The beeps are power on and off sounds from PAC Mate Omni.
						import nvwave, os.path # The wave playback and path manipulator.
						beep = obj.name.split(" ")
						stat = beep[len(beep)-1]
						wavDir, wavFile = os.path.dirname(__file__), ""
						# Play a wave file based on on/off status.
						if stat == "Off": wavFile = wavDir + "\SPL_off.wav"
						elif stat == "On": wavFile = wavDir+"\SPL_on.wav"
						nvwave.playWaveFile(wavFile)
					else:
						ui.message(obj.name)
			# Monitor the end of track time and announce it.
			elif obj.windowClassName == "TStaticText" and obj.name == self.SPLEndOfTrackTime and obj.simpleParent.name == "Remaining Time": tones.beep(440, 200) # SPL 4.x.
			elif obj.windowClassName == "TStaticText" and obj.name == self.SPLEndOfTrackTime and obj.simplePrevious != None and obj.simplePrevious.name == "Remaining Time": tones.beep(440, 200) # SPL 5.x.
			# Clean this mess with a more elegant solution.
		nextHandler()

# JL's additions

	# Various status scripts.
	# To save keyboard commands, layered commands will be used.
	# Most were borrowed from JFW and Window-Eyes layer scripts.

	# Set up the layer script environment.
	def getScript(self, gesture):
		if not self.SPLAssistant: return appModuleHandler.AppModule.getScript(self, gesture)
		script = appModuleHandler.AppModule.getScript(self, gesture)
		if not script: script = finally_(self.script_error, self.finish)
		return finally_(script, self.finish)

	def finish(self):
		self.SPLAssistant = False
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)

	def script_error(self, gesture):
		tones.beep(120, 100)

	# Let us meet the scripts themselves.

	def script_sayRemainingTime(self, gesture):
		fgWindow, remainingTime = api.getForegroundObject(), ""
		# For Studio 5.x: While Studio is on focus, the playback window with remaining time info is right next door. Parse the window title.
		# For Studio 4.x: this information is part of the main window. Fetch one of the objects.
		if self.SPLCurVersion >= SPLMinVersion: # See if we're running 5.00 or later.
			timeWindowStr = fgWindow.parent.next.name.split(" ")
			# We want the first part only, the time itself.
			remainingTime = timeWindowStr[0]
		else: # SPL 4.x.
			remainingTime = fgWindow.children[17].firstChild.name
		ui.message(remainingTime)
	# Translators: Input help mode message for a command in Station Playlist Studio.
	script_sayRemainingTime.__doc__=_("Announces the remaining track time.")

	# Set the end of track alarm time between 1 and 9 seconds.

	def script_setEndOfTrackTime(self, gesture):
		# Borrowed from NVDA core cursorManager.py.
		timeVal = self.SPLEndOfTrackTime[-1]
		timeMSG = "Enter end of track alarm time in seconds (currently {curAlarmSec})".format(curAlarmSec = timeVal)
		dlg = wx.TextEntryDialog(gui.mainFrame,
		timeMSG,
		"End of track alarm", defaultValue=timeVal)
		def callback(result):
			if result == wx.ID_OK:
				# Check if the value is indeed between 1 and 9.
				if not dlg.GetValue().isdigit() or int(dlg.GetValue()) < 1 or int(dlg.GetValue()) > 9: wx.CallAfter(gui.messageBox, "Incorrect value entered.", "Error",wx.OK|wx.ICON_ERROR)
				else: self.SPLEndOfTrackTime = self.SPLEndOfTrackTime.replace(self.SPLEndOfTrackTime[-1], dlg.GetValue()) # Quite a complicated replacement expression, but it works in this case.
		gui.runScriptModalDialog(dlg, callback)
	script_setEndOfTrackTime.__doc__="sets end of track alarm (default is 5 seconds)."

	# Toggle whether beeps should be heard instead of toggle announcements.

	def script_toggleBeepAnnounce(self, gesture):
		if not self.beepAnnounce:
			self.beepAnnounce = True
			# Translators: Reported when toggle announcement is set to beeps in SPL Studio.
			ui.message(_("Toggle announcement beeps"))
		else:
			self.beepAnnounce = False
			# Translators: Reported when toggle announcement is set to words in SPL Studio.
			ui.message(_("Toggle announcement words"))
	# Translators: Input help mode message for a command in Station Playlist Studio.
	script_toggleBeepAnnounce.__doc__=_("Toggles option change announcements between words and beeps.")

	# The layer commands themselves.
	# First layer (SPL Assistant): basic status such as playback, automation, etc.
	SPLAssistant = False

	# The children constants for fetching status information from the SPL Studio window.
	SPLElapsedTime = 3 # Elapsed time of the current track.
	SPLPlayStatus = 5 # Play status, mic, etc.
	SPL4PlayStatus = 0 # Play status for Studio 4.x.
	SPLHourTrackDuration = 17 # For track duration for the given hour marker.
	SPLHourSelectedDuration = 18 # In case the user selects one or more tracks in a given hour.

	# The SPL Assistant layer driver.

	def script_SPLAssistantToggle(self, gesture):
		if self.SPLAssistant:
			self.script_error(gesture)
			return
		self.bindGestures(self.__SPLAssistantGestures)
		self.SPLAssistant = True
		tones.beep(512, 10)
	# Translators: Input help mode message for a layer command in Station Playlist Studio.
	script_SPLAssistantToggle.__doc__=_("The SPL Assistant layer command. See the add-on guide for more information on available commands.")

	# Whichever layer we use, get the appropriate children from the foreground window.
	def getStatusChild(self, childIndex):
		childObj = api.getForegroundObject().children[childIndex]
		return childObj

	# Basic status such as playback and mic.
	# For all these methods, assign the correct child ID based on SPL Studio version.

	def script_sayPlayStatus(self, gesture):
		obj = self.getStatusChild(self.SPLPlayStatus).children[0] if self.SPLCurVersion >= SPLMinVersion else self.getStatusChild(self.SPL4PlayStatus).children[0]
		ui.message(obj.name)

	def script_sayAutomationStatus(self, gesture):
		obj = self.getStatusChild(self.SPLPlayStatus).children[1] if self.SPLCurVersion >= SPLMinVersion else self.getStatusChild(self.SPL4PlayStatus).children[1]
		ui.message(obj.name)

	def script_sayMicStatus(self, gesture):
		obj = self.getStatusChild(self.SPLPlayStatus).children[2] if self.SPLCurVersion >= SPLMinVersion else self.getStatusChild(self.SPL4PlayStatus).children[2]
		ui.message(obj.name)

	def script_sayLineInStatus(self, gesture):
		obj = self.getStatusChild(self.SPLPlayStatus).children[3] if self.SPLCurVersion >= SPLMinVersion else self.getStatusChild(self.SPL4PlayStatus).children[3]
		ui.message(obj.name)

	def script_sayHourTrackDuration(self, gesture):
		obj = self.getStatusChild(self.SPLHourTrackDuration).firstChild
		ui.message(obj.name)

	def script_sayHourSelectedTrackDuration(self, gesture):
		obj = self.getStatusChild(self.SPLHourSelectedDuration).firstChild
		ui.message(obj.name)


	__SPLAssistantGestures={
		"kb:p":"sayPlayStatus",
		"kb:a":"sayAutomationStatus",
		"kb:m":"sayMicStatus",
		"kb:l":"sayLineInStatus",
		"kb:h":"sayHourTrackDuration",
		"kb:shift+h":"sayHourSelectedTrackDuration"
	}

	__gestures={
		"kb:control+alt+t":"sayRemainingTime",
		"kb:control+nvda+1":"toggleBeepAnnounce",
		"kb:control+nvda+2":"setEndOfTrackTime",
		"kb:control+nvda+`":"SPLAssistantToggle"
	}

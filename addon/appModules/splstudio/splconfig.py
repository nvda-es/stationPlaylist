# SPL Studio Configuration Manager
# An app module and global plugin package for NVDA
# Copyright 2015 Joseph Lee and others, released under GPL.
# Provides the configuration management package for SPL Studio app module.
# For miscellaneous dialogs and tool, see SPLMisc module.

import os
from cStringIO import StringIO
from configobj import ConfigObj
from validate import Validator
import weakref
import globalVars
import ui
import api
import gui
import wx
from winUser import user32
import tones

# Configuration management
SPLIni = os.path.join(globalVars.appArgs.configPath, "splstudio.ini")
SPLProfiles = os.path.join(globalVars.appArgs.configPath, "addons", "stationPlaylist", "profiles")
confspec = ConfigObj(StringIO("""
BeepAnnounce = boolean(default=false)
SayEndOfTrack = boolean(default=true)
EndOfTrackTime = integer(min=1, max=59, default=5)
SaySongRamp = boolean(default=true)
SongRampTime = integer(min=1, max=9, default=5)
BrailleTimer = option("off", "intro", "outro", "both", default="off")
MicAlarm = integer(min=0, default="0")
LibraryScanAnnounce = option("off", "ending", "progress", "numbers", default="off")
TrackDial = boolean(default=false)
UseScreenColumnOrder = boolean(default=true)
ColumnOrder = string(default="Artist,Title,Duration,Intro,Category,Filename")
IncludedColumns = string(default="Artist,Title,Duration,Intro,Category,Filename")
SayScheduledFor = boolean(default=true)
SayListenerCount = boolean(default=true)
SayPlayingCartName = boolean(default=true)
"""), encoding="UTF-8", list_values=False)
confspec.newlines = "\r\n"
SPLConfig = None
# A pool of broadcast profiles.
SPLConfigPool = []

# The following settings can be changed in profiles:
_mutatableSettings=("SayEndOfTrack","EndOfTrackTime","SaySongRamp","SongRampTime","MicAlarm")

# Display an error dialog when configuration validation fails.
def runConfigErrorDialog(errorText, errorType):
	wx.CallAfter(gui.messageBox, errorText, errorType, wx.OK|wx.ICON_ERROR)

# Reset settings to defaults.
# This will be called when validation fails or when the user asks for it.
def resetConfig(defaults, activeConfig, intentional=False):
	for setting in activeConfig:
		activeConfig[setting] = defaults[setting]
	activeConfig.write()
	if intentional:
		# Translators: A dialog message shown when settings were reset to defaults.
		wx.CallAfter(gui.messageBox, _("Successfully applied default add-on settings."),
		# Translators: Title of the reset config dialog.
		_("Reset configuration"), wx.OK|wx.ICON_INFORMATION)

# In case one or more profiles had config issues, look up the error message from the following map.
_configErrors ={
	"completeReset":"All settings reset to defaults",
	"partialReset":"Some settings reset to defaults",
	"columnOrderReset":"Column announcement order reset to defaults",
	"partialAndColumnOrderReset":"Some settings, including column announcement order reset to defaults"
}

# To be run in app module constructor.
# With the load function below, load the config upon request.
# 6.0: The below init function is really a vehicle that traverses through config profiles in a loop.
# Prompt the config error dialog only once.
_configLoadStatus = {} # Key = filename, value is pass or no pass.

def initConfig():
	# Load the default config from a list of profiles.
	global SPLConfig, SPLConfigPool, _configLoadStatus, SPLActiveProfile
	if SPLConfigPool is None: SPLConfigPool = []
	if SPLActiveProfile is None: SPLActiveProfile = "Normal profile"
	SPLConfigPool.append(unlockConfig(SPLIni, profileName=SPLActiveProfile, prefill=True))
	try:
		profiles = filter(lambda fn: os.path.splitext(fn)[-1] == ".ini", os.listdir(SPLProfiles))
		for profile in profiles:
			SPLConfigPool.append(unlockConfig(os.path.join(SPLProfiles, profile), profileName=os.path.splitext(profile)[0]))
	except WindowsError:
		pass
	SPLConfig = SPLConfigPool[0]
	if len(_configLoadStatus):
		# Translators: Standard error title for configuration error.
		title = _("Studio add-on Configuration error")
		messages = []
		messages.append("One or more broadcast profiles had issues:\n\n")
		for profile in _configLoadStatus:
			error = _configErrors[_configLoadStatus[profile]]
			messages.append("{profileName}: {errorMessage}".format(profileName = profile, errorMessage = error))
		_configLoadStatus.clear()
		runConfigErrorDialog("\n".join(messages), title)

# 6.0: Unlock (load) profiles from files.
def unlockConfig(path, profileName=None, prefill=False):
	global _configLoadStatus # To be mutated only during unlock routine.
	SPLConfigCheckpoint = ConfigObj(path, configspec = confspec, encoding="UTF-8")
	# 5.2 and later: check to make sure all values are correct.
	val = Validator()
	configTest = SPLConfigCheckpoint.validate(val, copy=prefill)
	if configTest != True:
		# Hack: have a dummy config obj handy just for storing default values.
		SPLDefaults = ConfigObj(None, configspec = confspec, encoding="UTF-8")
		SPLDefaults.validate(val, copy=True)
		# Translators: Standard error title for configuration error.
		title = _("Studio add-on Configuration error")
		if not configTest:
			# Case 1: restore settings to defaults when 5.x config validation has failed on all values.
			resetConfig(SPLDefaults, SPLConfigCheckpoint)
			_configLoadStatus[profileName] = "completeReset"
		elif isinstance(configTest, dict):
			# Case 2: For 5.x and later, attempt to reconstruct the failed values.
			for setting in configTest:
				if not configTest[setting]:
					SPLConfigCheckpoint[setting] = SPLDefaults[setting]
			SPLConfigCheckpoint.write()
			_configLoadStatus[profileName] = "partialReset"
	_extraInitSteps(SPLConfigCheckpoint, profileName=profileName)
	SPLConfigCheckpoint.name = profileName
	return SPLConfigCheckpoint

# Extra initialization steps such as converting value types.
def _extraInitSteps(conf, profileName=None):
	global _configLoadStatus
	columnOrder = conf["ColumnOrder"].split(",")
	# Catch suttle errors.
	fields = ["Artist","Title","Duration","Intro","Category","Filename"]
	invalidFields = 0
	for field in fields:
		if field not in columnOrder: invalidFields+=1
	if invalidFields or len(columnOrder) != 6:
		if profileName in _configLoadStatus and _configLoadStatus[profileName] == "partialReset":
			_configLoadStatus[profileName] = "partialAndColumnOrderReset"
		else:
			_configLoadStatus[profileName] = "columnOrderReset"
		columnOrder = fields
	conf["ColumnOrder"] = columnOrder
	conf["IncludedColumns"] = set(conf["IncludedColumns"].split(","))

# Perform some extra work before writing the config file.
def _preSave(conf):
	conf["ColumnOrder"] = ",".join(conf["ColumnOrder"])
	conf["IncludedColumns"] = ",".join(conf["IncludedColumns"])

	# Save configuration database.
def saveConfig():
	# Save all config profiles.
	global SPLConfig, SPLConfigPool, SPLActiveProfile
	# Apply any global settings changed in profiles to normal configuration.
	if SPLConfigPool.index(SPLConfig) > 0:
		for setting in SPLConfig:
			if setting not in _mutatableSettings:
				SPLConfigPool[0][setting] = SPLConfig[setting]
	for configuration in SPLConfigPool:
		if configuration is not None:
			_preSave(configuration)
			configuration.write()
	SPLConfig = None
	SPLConfigPool = None
	SPLActiveProfile = None

# Switch between profiles.
SPLActiveProfile = None
SPLPrevProfile = None
SPLSwitchProfile = None

# Called from within the app module.
def instantProfileSwitch():
	global SPLPrevProfile, SPLConfig, SPLActiveProfile
	if _configDialogOpened:
		ui.message("Add-on settings dialog is open, cannot switch profiles")
		return
	if SPLSwitchProfile is None:
		ui.message("No instant switch profile is defined")
	else:
		if SPLPrevProfile is None:
			if SPLActiveProfile == SPLSwitchProfile:
				ui.message("You are already in the instant switch profile")
				return
			# Switch to the given profile.
			switchProfileIndex = [profile.name for profile in SPLConfigPool].index(SPLSwitchProfile)
			SPLPrevProfile = SPLConfigPool.index(SPLConfig)
			SPLConfig = SPLConfigPool[switchProfileIndex]
			ui.message("Switching profiles")
		else:
			SPLConfig = SPLConfigPool[SPLPrevProfile]
			SPLActiveProfile = SPLConfig.name
			SPLPrevProfile = None
			ui.message("Returning to previous profile")

# Configuration dialog.
_configDialogOpened = False

class SPLConfigDialog(gui.SettingsDialog):
	# Translators: This is the label for the StationPlaylist Studio configuration dialog.
	title = _("Studio Add-on Settings")

	def makeSettings(self, settingsSizer):

		# Broadcast profile controls were inspired by Config Profiles dialog in NVDA Core.
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in SPL add-on dialog to select a broadcast profile.
		label = wx.StaticText(self, wx.ID_ANY, label=_("Broadcast &profile:"))
		self.profiles = wx.Choice(self, wx.ID_ANY, choices=[profile.name for profile in SPLConfigPool])
		self.profiles.Bind(wx.EVT_CHOICE, self.onProfileSelection)
		try:
			self.profiles.SetSelection(SPLConfigPool.index(SPLConfig))
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.profiles)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		# Profile controls code credit: NV Access (except copy button).
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to create a new broadcast profile.
		item = newButton = wx.Button(self, label=_("&New"))
		item.Bind(wx.EVT_BUTTON, self.onNew)
		sizer.Add(item)
		# Translators: The label of a button to copy a broadcast profile.
		item = copyButton = wx.Button(self, label=_("Cop&y"))
		item.Bind(wx.EVT_BUTTON, self.onCopy)
		sizer.Add(item)
		# Translators: The label of a button to rename a broadcast profile.
		item = self.renameButton = wx.Button(self, label=_("&Rename"))
		item.Bind(wx.EVT_BUTTON, self.onRename)
		sizer.Add(item)
		# Translators: The label of a button to delete a broadcast profile.
		item = self.deleteButton = wx.Button(self, label=_("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		# Translators: The label of a button to toggle instant profile switching on and off.
		if SPLPrevProfile is None and SPLSwitchProfile is None: switchLabel = "Enable instant profile switching"
		else: switchLabel = "Disable instant profile switching"
		item = self.instantSwitchButton = wx.Button(self, label=switchLabel)
		item.Bind(wx.EVT_BUTTON, self.onInstantSwitch)
		self.switchProfile = SPLSwitchProfile
		sizer.Add(item)
		if SPLConfigPool.index(SPLConfig) == 0:
			self.renameButton.Disable()
			self.deleteButton.Disable()
			self.instantSwitchButton.Disable()
		settingsSizer.Add(sizer)

	# Translators: the label for a setting in SPL add-on settings to set status announcement between words and beeps.
		self.beepAnnounceCheckbox=wx.CheckBox(self,wx.NewId(),label=_("&Beep for status announcements"))
		self.beepAnnounceCheckbox.SetValue(SPLConfig["BeepAnnounce"])
		settingsSizer.Add(self.beepAnnounceCheckbox, border=10,flag=wx.TOP)

		self.outroSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Check box hiding method comes from Alberto Buffolino's Columns Review add-on.
		# Translators: Label for a check box in SPL add-on settings to notify when end of track (outro) is approaching.
		self.outroCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Notify when end of track is approaching"))
		self.outroCheckBox.SetValue(SPLConfig["SayEndOfTrack"])
		self.outroCheckBox.Bind(wx.EVT_CHECKBOX, self.onOutroCheck)
		self.outroSizer.Add(self.outroCheckBox, border=10,flag=wx.BOTTOM)

		# Translators: The label for a setting in SPL Add-on settings to specify end of track (outro) alarm.
		self.outroAlarmLabel = wx.StaticText(self, wx.ID_ANY, label=_("&End of track alarm in seconds"))
		self.outroSizer.Add(self.outroAlarmLabel)
		self.endOfTrackAlarm = wx.SpinCtrl(self, wx.ID_ANY, min=1, max=59)
		self.endOfTrackAlarm.SetValue(long(SPLConfig["EndOfTrackTime"]))
		self.outroSizer.Add(self.endOfTrackAlarm)
		self.onOutroCheck(None)
		settingsSizer.Add(self.outroSizer, border=10, flag=wx.BOTTOM)

		self.introSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for a check box in SPL add-on settings to notify when end of intro is approaching.
		self.introCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Notify when end of introduction is approaching"))
		self.introCheckBox.SetValue(SPLConfig["SaySongRamp"])
		self.introCheckBox.Bind(wx.EVT_CHECKBOX, self.onIntroCheck)
		self.introSizer.Add(self.introCheckBox, border=10,flag=wx.BOTTOM)

		# Translators: The label for a setting in SPL Add-on settings to specify track intro alarm.
		self.introAlarmLabel = wx.StaticText(self, wx.ID_ANY, label=_("&Track intro alarm in seconds"))
		self.introSizer.Add(self.introAlarmLabel)
		self.songRampAlarm = wx.SpinCtrl(self, wx.ID_ANY, min=1, max=9)
		self.songRampAlarm.SetValue(long(SPLConfig["SongRampTime"]))
		self.introSizer.Add(self.songRampAlarm)
		self.onIntroCheck(None)
		settingsSizer.Add(self.introSizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in SPL add-on dialog to control braille timer.
		label = wx.StaticText(self, wx.ID_ANY, label=_("&Braille timer:"))
		self.brailleTimerValues=[("off",_("off")),
		# Translators: One of the braille timer settings.
		("outro",_("track ending")),
		# Translators: One of the braille timer settings.
		("intro",_("track intro")),
		# Translators: One of the braille timer settings.
		("both",_("track intro and ending"))]
		self.brailleTimerList = wx.Choice(self, wx.ID_ANY, choices=[x[1] for x in self.brailleTimerValues])
		brailleTimerCurValue=SPLConfig["BrailleTimer"]
		selection = (x for x,y in enumerate(self.brailleTimerValues) if y[0]==brailleTimerCurValue).next()  
		try:
			self.brailleTimerList.SetSelection(selection)
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.brailleTimerList)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The label for a setting in SPL Add-on settings to change microphone alarm setting.
		label = wx.StaticText(self, wx.ID_ANY, label=_("&Microphone alarm in seconds"))
		sizer.Add(label)
		self.micAlarm = wx.TextCtrl(self, wx.ID_ANY)
		self.micAlarm.SetValue(str(SPLConfig["MicAlarm"]))
		sizer.Add(self.micAlarm)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in SPL add-on dialog to control library scan announcement.
		label = wx.StaticText(self, wx.ID_ANY, label=_("&Library scan announcement:"))
		self.libScanValues=[("off",_("off")),
		# Translators: One of the library scan announcement settings.
		("ending",_("start and end only")),
		# Translators: One of the library scan announcement settings.
		("progress",_("scan progress")),
		# Translators: One of the library scan announcement settings.
		("numbers",_("scan count"))]
		self.libScanList = wx.Choice(self, wx.ID_ANY, choices=[x[1] for x in self.libScanValues])
		libScanCurValue=SPLConfig["LibraryScanAnnounce"]
		selection = (x for x,y in enumerate(self.libScanValues) if y[0]==libScanCurValue).next()  
		try:
			self.libScanList.SetSelection(selection)
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.libScanList)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		# Translators: the label for a setting in SPL add-on settings to toggle track dial mode on and off.
		self.trackDialCheckbox=wx.CheckBox(self,wx.NewId(),label=_("&Track Dial mode"))
		self.trackDialCheckbox.SetValue(SPLConfig["TrackDial"])
		settingsSizer.Add(self.trackDialCheckbox, border=10,flag=wx.BOTTOM)

		# Translators: the label for a setting in SPL add-on settings to toggle custom column announcement.
		self.columnOrderCheckbox=wx.CheckBox(self,wx.NewId(),label=_("Announce columns in the &order shown on screen"))
		self.columnOrderCheckbox.SetValue(SPLConfig["UseScreenColumnOrder"])
		self.columnOrder = SPLConfig["ColumnOrder"]
		self.includedColumns = SPLConfig["IncludedColumns"]
		settingsSizer.Add(self.columnOrderCheckbox, border=10,flag=wx.BOTTOM)
		# Translators: The label of a button to manage column announcements.
		item = manageColumnsButton = wx.Button(self, label=_("&Manage track column announcements..."))
		item.Bind(wx.EVT_BUTTON, self.onManageColumns)
		settingsSizer.Add(item)

		# Translators: the label for a setting in SPL add-on settings to announce scheduled time.
		self.scheduledForCheckbox=wx.CheckBox(self,wx.NewId(),label=_("Announce &scheduled time for the selected track"))
		self.scheduledForCheckbox.SetValue(SPLConfig["SayScheduledFor"])
		settingsSizer.Add(self.scheduledForCheckbox, border=10,flag=wx.BOTTOM)

		# Translators: the label for a setting in SPL add-on settings to announce listener count.
		self.listenerCountCheckbox=wx.CheckBox(self,wx.NewId(),label=_("Announce &listener count"))
		self.listenerCountCheckbox.SetValue(SPLConfig["SayListenerCount"])
		settingsSizer.Add(self.listenerCountCheckbox, border=10,flag=wx.BOTTOM)

		# Translators: the label for a setting in SPL add-on settings to announce currently playing cart.
		self.cartNameCheckbox=wx.CheckBox(self,wx.NewId(),label=_("&Announce name of the currently playing cart"))
		self.cartNameCheckbox.SetValue(SPLConfig["SayPlayingCartName"])
		settingsSizer.Add(self.cartNameCheckbox, border=10,flag=wx.BOTTOM)

		# Translators: The label for a button in SPL add-on configuration dialog to reset settings to defaults.
		self.resetConfigButton = wx.Button(self, wx.ID_ANY, label=_("Reset settings"))
		self.resetConfigButton.Bind(wx.EVT_BUTTON,self.onResetConfig)
		settingsSizer.Add(self.resetConfigButton)

	def postInit(self):
		global _configDialogOpened
		_configDialogOpened = True
		self.profiles.SetFocus()

	def onOk(self, evt):
		if not self.micAlarm.Value.isdigit():
			gui.messageBox(
				# Translators: Message to report wrong value for microphone alarm.
				_("Incorrect microphone alarm value entered."),
				# Translators: The title of the message box
				_("Error"), wx.OK|wx.ICON_ERROR,self)
			self.micAlarm.SetFocus()
			return
		global SPLConfig, SPLActiveProfile, _configDialogOpened, SPLSwitchProfile
		selectedProfile = self.profiles.GetSelection()
		SPLConfig = SPLConfigPool[selectedProfile]
		SPLConfig["BeepAnnounce"] = self.beepAnnounceCheckbox.Value
		SPLConfig["SayEndOfTrack"] = self.outroCheckBox.Value
		SPLConfig["EndOfTrackTime"] = self.endOfTrackAlarm.Value
		SPLConfig["SaySongRamp"] = self.introCheckBox.Value
		SPLConfig["SongRampTime"] = self.songRampAlarm.Value
		SPLConfig["BrailleTimer"] = self.brailleTimerValues[self.brailleTimerList.GetSelection()][0]
		SPLConfig["MicAlarm"] = self.micAlarm.Value
		SPLConfig["LibraryScanAnnounce"] = self.libScanValues[self.libScanList.GetSelection()][0]
		SPLConfig["TrackDial"] = self.trackDialCheckbox.Value
		SPLConfig["UseScreenColumnOrder"] = self.columnOrderCheckbox.Value
		SPLConfig["ColumnOrder"] = self.columnOrder
		SPLConfig["IncludedColumns"] = self.includedColumns
		SPLConfig["SayScheduledFor"] = self.scheduledForCheckbox.Value
		SPLConfig["SayListenerCount"] = self.listenerCountCheckbox.Value
		SPLConfig["SayPlayingCartName"] = self.cartNameCheckbox.Value
		SPLActiveProfile = SPLConfigPool[selectedProfile].name
		SPLSwitchProfile = self.switchProfile
		_configDialogOpened = False
		super(SPLConfigDialog,  self).onOk(evt)

	def onCancel(self, evt):
		global _configDialogOpened
		_configDialogOpened = False
		super(SPLConfigDialog,  self).onCancel(evt)

	# Check events for outro and intro alarms, respectively.
	def onOutroCheck(self, evt):
		if not self.outroCheckBox.IsChecked():
			self.outroSizer.Hide(self.outroAlarmLabel)
			self.outroSizer.Hide(self.endOfTrackAlarm)
		else:
			self.outroSizer.Show(self.outroAlarmLabel)
			self.outroSizer.Show(self.endOfTrackAlarm)
		self.Fit()

	def onIntroCheck(self, evt):
		if not self.introCheckBox.IsChecked():
			self.introSizer.Hide(self.introAlarmLabel)
			self.introSizer.Hide(self.songRampAlarm)
		else:
			self.introSizer.Show(self.introAlarmLabel)
			self.introSizer.Show(self.songRampAlarm)
		self.Fit()

	# Load settings from profiles.
	def onProfileSelection(self, evt):
		import tones
		tones.beep(500, 100)
		# Don't rely on SPLConfig here, as we don't want to interupt the show.
		selection = self.profiles.GetSelection()
		if selection == 0:
			self.renameButton.Disable()
			self.deleteButton.Disable()
			self.instantSwitchButton.Disable()
		else:
			self.renameButton.Enable()
			self.deleteButton.Enable()
			if SPLConfigPool[selection].name != self.switchProfile:
				self.instantSwitchButton.Label = "Enable instant profile switching"
			else:
				self.instantSwitchButton.Label = "Disable instant profile switching"
			self.instantSwitchButton.Enable()
		selectedProfile = SPLConfigPool[selection]
		self.outroCheckBox.SetValue(selectedProfile["SayEndOfTrack"])
		self.endOfTrackAlarm.SetValue(long(selectedProfile["EndOfTrackTime"]))
		self.onOutroCheck(None)
		self.introCheckBox.SetValue(selectedProfile["SaySongRamp"])
		self.songRampAlarm.SetValue(long(selectedProfile["SongRampTime"]))
		self.onIntroCheck(None)
		self.micAlarm.SetValue(str(selectedProfile["MicAlarm"]))

	# Profile controls.
	# Rename and delete events come from GUI/config profiles dialog from NVDA core.
	def onNew(self, evt):
		self.Disable()
		NewProfileDialog(self).Show()

	def onCopy(self, evt):
		self.Disable()
		NewProfileDialog(self, copy=True).Show()

	def onRename(self, evt):
		global SPLConfigPool
		index = self.profiles.Selection
		oldName = SPLConfigPool[index].name
		# Translators: The label of a field to enter a new name for a broadcast profile.
		with wx.TextEntryDialog(self, _("New name:"),
				# Translators: The title of the dialog to rename a profile.
				_("Rename Profile"), defaultValue=oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			newName = api.filterFileName(d.Value)
		if oldName == newName: return
		newNamePath = newName + ".ini"
		newProfile = os.path.join(SPLProfiles, newNamePath)
		if oldName.lower() != newName.lower() and os.path.isfile(newProfile):
			# Translators: An error displayed when renaming a configuration profile
			# and a profile with the new name already exists.
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		oldNamePath = oldName + ".ini"
		oldProfile = os.path.join(SPLProfiles, oldNamePath)
		os.rename(oldProfile, newProfile)
		SPLConfigPool[index].name = newName
		SPLConfigPool[index].filename = newProfile
		self.profiles.SetString(index, newName)
		self.profiles.Selection = index
		self.profiles.SetFocus()

	def onDelete(self, evt):
		index = self.profiles.Selection
		if gui.messageBox(
			# Translators: The confirmation prompt displayed when the user requests to delete a broadcast profile.
			_("Are you sure you want to delete this profile? This cannot be undone."),
			# Translators: The title of the confirmation dialog for deletion of a profile.
			_("Confirm Deletion"),
			wx.YES | wx.NO | wx.ICON_QUESTION, self
		) == wx.NO:
			return
		global SPLConfigPool
		name = SPLConfigPool[index].name
		path = SPLConfigPool[index].filename
		del SPLConfigPool[index]
		try:
			os.remove(path)
		except WindowsError:
			pass
		self.profiles.Delete(index)
		self.profiles.SetString(0, SPLConfigPool[0].name)
		self.profiles.Selection = 0
		self.onProfileSelection(None)
		self.profiles.SetFocus()

	def onInstantSwitch(self, evt):
		import tones
		selection = self.profiles.GetSelection()
		selectedName = SPLConfigPool[selection].name
		if self.switchProfile is None or (selectedName != self.switchProfile):
			self.instantSwitchButton.Label = "Disable instant profile switching"
			self.switchProfile = selectedName
			tones.beep(1000, 500)
		else:
			self.instantSwitchButton.Label = "Enable instant profile switching"
			self.switchProfile = None
			tones.beep(500, 500)

	# Manage column announcements.
	def onManageColumns(self, evt):
		self.Disable()
		ColumnAnnouncementsDialog(self).Show()

	# Reset settings to defaults.
	# This affects the currently selected profile.
	def onResetConfig(self, evt):
		if gui.messageBox(
		# Translators: A message to warn about resetting SPL config settings to factory defaults.
		_("Are you sure you wish to reset SPL add-on settings to defaults?"),
		# Translators: The title of the warning dialog.
		_("Warning"),wx.YES_NO|wx.NO_DEFAULT|wx.ICON_WARNING,self
		)==wx.YES:
			val = Validator()
			SPLDefaults = ConfigObj(None, configspec = confspec, encoding="UTF-8")
			SPLDefaults.validate(val, copy=True)
			# Reset the selected config only.
			global SPLConfig
			SPLConfig = SPLConfigPool[self.profiles.GetSelection()]
			resetConfig(SPLDefaults, SPLConfig, intentional=True)
			self.Destroy()


# Open the above dialog upon request.
def onConfigDialog(evt):
	# 5.2: Guard against alarm dialogs.
	if _alarmDialogOpened:
		# Translators: Presented when an alarm dialog is opened.
		wx.CallAfter(gui.messageBox, _("An alarm dialog is already opened. Please close the alarm dialog first."), _("Error"), wx.OK|wx.ICON_ERROR)
	else: gui.mainFrame._popupSettingsDialog(SPLConfigDialog)

# Helper dialogs for add-on settings dialog.

# New broadcast profile dialog: Modification of new config profile dialog from NvDA Core.
class NewProfileDialog(wx.Dialog):

	def __init__(self, parent, copy=False):
		self.copy = copy
		if not self.copy:
			# Translators: The title of the dialog to create a new broadcast profile.
			dialogTitle = _("New Profile")
		else:
			# Translators: The title of the dialog to copy a broadcast profile.
			dialogTitle = _("Copy Profile")
		super(NewProfileDialog, self).__init__(parent, title=dialogTitle)
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the name of a new broadcast profile.
		sizer.Add(wx.StaticText(self, label=_("Profile name:")))
		item = self.profileName = wx.TextCtrl(self)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in SPL add-on dialog to select a base  profile for copying.
		label = wx.StaticText(self, wx.ID_ANY, label=_("&Base profile:"))
		self.baseProfiles = wx.Choice(self, wx.ID_ANY, choices=[profile.name for profile in SPLConfigPool])
		try:
			self.baseProfiles.SetSelection(SPLConfigPool.index(SPLConfig))
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.baseProfiles)
		if not self.copy:
			sizer.Hide(label)
			sizer.Hide(self.baseProfiles)
		mainSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.profileName.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		global SPLConfigPool
		profileNames = [profile.name for profile in SPLConfigPool]
		name = api.filterFileName(self.profileName.Value)
		if not name:
			return
		if name in profileNames:
			# Translators: An error displayed when the user attempts to create a profile which already exists.
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		namePath = name + ".ini"
		if not os.path.exists(SPLProfiles):
			os.mkdir(SPLProfiles)
		newProfile = os.path.join(SPLProfiles, namePath)
		if self.copy:
			import shutil
			baseProfile = SPLConfigPool[self.baseProfiles.GetSelection()]
			shutil.copy2(baseProfile.filename, newProfile)
		SPLConfigPool.append(unlockConfig(newProfile, profileName=name))
		parent = self.Parent
		parent.profiles.Append(name)
		parent.profiles.Selection = parent.profiles.Count - 1
		parent.onProfileSelection(None)
		parent.profiles.SetFocus()
		parent.Enable()
		self.Destroy()
		return

	def onCancel(self, evt):
		self.Parent.Enable()
		self.Destroy()

# Column announcement manager.
# Select which track columns should be announced and in which order.
class ColumnAnnouncementsDialog(wx.Dialog):

	def __init__(self, parent):
		super(ColumnAnnouncementsDialog, self).__init__(parent, title="Manage column announcements")

		# WX's CheckListBox isn't user friendly.
		# Therefore use checkboxes laid out across the top.
		self.checkedColumns = []
		for column in ("Artist", "Title", "Duration", "Intro", "Category", "Filename"):
			checkedColumn=wx.CheckBox(self,wx.NewId(),label=column)
			checkedColumn.SetValue(column in SPLConfig["IncludedColumns"])
			self.checkedColumns.append(checkedColumn)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		# First, a help text.
		label = wx.StaticText(self, wx.ID_ANY, label=_("Select columns to be announced"))
		mainSizer.Add(label,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		for checkedColumn in self.checkedColumns:
			sizer.Add(checkedColumn)
		mainSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in SPL add-on dialog to select a base  profile for copying.
		label = wx.StaticText(self, wx.ID_ANY, label=_("Column &order:"))
		# WXPython Phoenix contains RearrangeList to allow item orders to be changed automatically.
		# Because WXPython Classic doesn't include this, work around by using a variant of list box and move up/down buttons.
		self.trackColumns= wx.ListBox(self, wx.ID_ANY, choices=parent.columnOrder)
		self.trackColumns.Bind(wx.EVT_LISTBOX,self.onColumnSelection)
		try:
			self.trackColumns.SetSelection(0)
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.trackColumns)
		mainSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a button in SPL add-on configuration dialog to reset settings to defaults.
		self.upButton = wx.Button(self, wx.ID_ANY, label=_("Move &up"))
		self.upButton.Bind(wx.EVT_BUTTON,self.onMoveUp)
		self.upButton.Disable()
		sizer.Add(self.upButton)
				# Translators: The label for a button in SPL add-on configuration dialog to reset settings to defaults.
		self.dnButton = wx.Button(self, wx.ID_ANY, label=_("Move &down"))
		self.dnButton.Bind(wx.EVT_BUTTON,self.onMoveDown)
		sizer.Add(self.dnButton)
		mainSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.checkedColumns[0].SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		parent = self.Parent
		parent.columnOrder = self.trackColumns.GetItems()
		for checkbox in self.checkedColumns:
			action = parent.includedColumns.add if checkbox.Value else parent.includedColumns.remove
			action(checkbox.Label)
		parent.profiles.SetFocus()
		parent.Enable()
		self.Destroy()
		return

	def onCancel(self, evt):
		self.Parent.Enable()
		self.Destroy()

	def onColumnSelection(self, evt):
		selIndex = self.trackColumns.GetSelection()
		self.upButton.Disable() if selIndex == 0 else self.upButton.Enable()
		self.dnButton.Disable() if selIndex == self.trackColumns.GetCount()-1 else self.dnButton.Enable()

	def onMoveUp(self, evt):
		tones.beep(1000, 200)
		selIndex = self.trackColumns.GetSelection()
		if selIndex > 0:
			selItem = self.trackColumns.GetString(selIndex)
			self.trackColumns.Delete(selIndex)
			self.trackColumns.Insert(selItem, selIndex-1)
			self.trackColumns.Select(selIndex-1)
			self.onColumnSelection(None)

	def onMoveDown(self, evt):
		tones.beep(500, 200)
		selIndex = self.trackColumns.GetSelection()
		if selIndex < self.trackColumns.GetCount()-1:
			selItem = self.trackColumns.GetString(selIndex)
			self.trackColumns.Delete(selIndex)
			self.trackColumns.Insert(selItem, selIndex+1)
			self.trackColumns.Select(selIndex+1)
			self.onColumnSelection(None)

# Additional configuration dialogs

# A common alarm dialog
# Based on NVDA core's find dialog code (implemented by the author of this add-on).
# Only one instance can be active at a given moment (code borrowed from GUI's exit dialog routine).
_alarmDialogOpened = False

# A common alarm error dialog.
def _alarmError():
	# Translators: Text of the dialog when another alarm dialog is open.
	gui.messageBox(_("Another alarm dialog is open."),_("Error"),style=wx.OK | wx.ICON_ERROR)

class SPLAlarmDialog(wx.Dialog):
	"""A dialog providing common alarm settings.
	This dialog contains a number entry field for alarm duration and a check box to enable or disable the alarm.
	"""

	# The following comes from exit dialog class from GUI package (credit: NV Access and Zahari from Bulgaria).
	_instance = None

	def __new__(cls, parent, *args, **kwargs):
		# Make this a singleton and prompt an error dialog if it isn't.
		if _alarmDialogOpened:
			raise RuntimeError("An instance of alarm dialog is opened")
		inst = cls._instance() if cls._instance else None
		if not inst:
			return super(cls, cls).__new__(cls, parent, *args, **kwargs)
		return inst

	def __init__(self, parent, setting, toggleSetting, title, alarmPrompt, alarmToggleLabel, min, max):
		inst = SPLAlarmDialog._instance() if SPLAlarmDialog._instance else None
		if inst:
			return
		# Use a weakref so the instance can die.
		SPLAlarmDialog._instance = weakref.ref(self)

		# Now the actual alarm dialog code.
		super(SPLAlarmDialog, self).__init__(parent, wx.ID_ANY, title)
		self.setting = setting
		self.toggleSetting = toggleSetting
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		alarmSizer = wx.BoxSizer(wx.HORIZONTAL)
		alarmMessage = wx.StaticText(self, wx.ID_ANY, label=alarmPrompt)
		alarmSizer.Add(alarmMessage)
		self.alarmEntry = wx.SpinCtrl(self, wx.ID_ANY, min=min, max=max)
		self.alarmEntry.SetValue(SPLConfig[setting])
		alarmSizer.Add(self.alarmEntry)
		mainSizer.Add(alarmSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)

		self.toggleCheckBox=wx.CheckBox(self,wx.NewId(),label=alarmToggleLabel)
		self.toggleCheckBox.SetValue(SPLConfig[toggleSetting])
		mainSizer.Add(self.toggleCheckBox,border=10,flag=wx.BOTTOM)

		mainSizer.AddSizer(self.CreateButtonSizer(wx.OK|wx.CANCEL))
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)
		self.alarmEntry.SetFocus()

	def onOk(self, evt):
		global _alarmDialogOpened
		# Optimization: don't bother if Studio is dead and if the same value has been entered.
		if user32.FindWindowA("SPLStudio", None):
			newVal = self.alarmEntry.GetValue()
			newToggle = self.toggleCheckBox.GetValue()
			if SPLConfig[self.setting] != newVal: SPLConfig[self.setting] = newVal
			elif SPLConfig[self.toggleSetting] != newToggle: SPLConfig[self.toggleSetting] = newToggle
		self.Destroy()
		_alarmDialogOpened = False

	def onCancel(self, evt):
		self.Destroy()
		global _alarmDialogOpened
		_alarmDialogOpened = False


# SPL Studio Configuration Manager
# An app module and global plugin package for NVDA
# Copyright 2015-2016 Joseph Lee and others, released under GPL.
# Provides the configuration management package for SPL Studio app module.
# For miscellaneous dialogs and tool, see SPLMisc module.
# For UI surrounding this module, see splconfui module.

import os
from cStringIO import StringIO
from configobj import ConfigObj
from validate import Validator
import time
import datetime
import cPickle
import globalVars
import ui
import api
import gui
import wx
import splupdate
from splmisc import SPLCountdownTimer, _metadataAnnouncer

# Configuration management
SPLIni = os.path.join(globalVars.appArgs.configPath, "splstudio.ini")
SPLProfiles = os.path.join(globalVars.appArgs.configPath, "addons", "stationPlaylist", "profiles")
# New (7.0) style config.
confspec7 = ConfigObj(StringIO("""
[General]
BeepAnnounce = boolean(default=false)
MessageVerbosity = option("beginner", "advanced", default="beginner")
BrailleTimer = option("off", "intro", "outro", "both", default="off")
AlarmAnnounce = option("beep", "message", "both", default="beep")
TrackCommentAnnounce = option("off", "beep", "message", "both", default="off")
LibraryScanAnnounce = option("off", "ending", "progress", "numbers", default="off")
TrackDial = boolean(default=false)
CategorySounds = boolean(default=false)
TopBottomAnnounce = boolean(default=true)
MetadataReminder = option("off", "startup", "instant", default="off")
TimeHourAnnounce = boolean(default=true)
ExploreColumns = string_list(default=list("Artist","Title","Duration","Intro","Category","Filename","Year","Album","Genre","Time Scheduled"))
[IntroOutroAlarms]
SayEndOfTrack = boolean(default=true)
EndOfTrackTime = integer(min=1, max=59, default=5)
SaySongRamp = boolean(default=true)
SongRampTime = integer(min=1, max=9, default=5)
[MicrophoneAlarm]
MicAlarm = integer(min=0, max=7200, default="0")
MicAlarmInterval = integer(min=0, max=60, default=0)
[MetadataStreaming]
MetadataEnabled = bool_list(default=list(false,false,false,false,false))
[ColumnAnnouncement]
UseScreenColumnOrder = boolean(default=true)
ColumnOrder = string_list(default=list("Artist","Title","Duration","Intro","Outro","Category","Year","Album","Genre","Mood","Energy","Tempo","BPM","Gender","Rating","Filename","Time Scheduled"))
IncludedColumns = string_list(default=list("Artist","Title","Duration","Intro","Outro","Category","Year","Album","Genre","Mood","Energy","Tempo","BPM","Gender","Rating","Filename","Time Scheduled"))
[SayStatus]
SayScheduledFor = boolean(default=true)
SayListenerCount = boolean(default=true)
SayPlayingCartName = boolean(default=true)
SayPlayingTrackName = option("auto", "background", "off", default="auto")
[Advanced]
SPLConPassthrough = boolean(default=false)
CompatibilityLayer = option("off", "jfw", "wineyes", default="off")
ProfileTriggerThreshold = integer(min=5, max=60, default=15)
[Update]
AutoUpdateCheck = boolean(default=true)
[Startup]
AudioDuckingReminder = boolean(default=true)
WelcomeDialog = boolean(default=true)
"""), encoding="UTF-8", list_values=False)
confspec7.newlines = "\r\n"
SPLConfig = None
# A pool of broadcast profiles.
SPLConfigPool = []
# The following settings can be changed in profiles:
_mutatableSettings7=("IntroOutroAlarms", "MicrophoneAlarm", "MetadataStreaming", "ColumnAnnouncement")
# 7.0: Profile-specific confspec (might be removed once a more optimal way to validate sections is found).
# Dictionary comprehension is better here.
confspecprofiles = {sect:key for sect, key in confspec7.iteritems() if sect in _mutatableSettings7}

# Default config spec container.
# To be moved to a different place in 8.0.
_SPLDefaults7 = ConfigObj(None, configspec = confspec7, encoding="UTF-8")
_val = Validator()
_SPLDefaults7.validate(_val, copy=True)

# Display an error dialog when configuration validation fails.
def runConfigErrorDialog(errorText, errorType):
	wx.CallAfter(gui.messageBox, errorText, errorType, wx.OK|wx.ICON_ERROR)

# Reset settings to defaults.
# This will be called when validation fails or when the user asks for it.
# 6.0: The below function resets a single profile. A sister function will reset all of them.
# 7.0: This calls copy profile function with default dictionary as the source profile.
def resetConfig(defaults, activeConfig):
	# The only time everything should be copied is when resetting normal profile.
	copyProfile(defaults, activeConfig, complete=activeConfig.filename == SPLIni)

# Reset all profiles upon request.
def resetAllConfig():
	for profile in SPLConfigPool:
		# Retrieve the profile path, as ConfigObj.reset nullifies it.
		profilePath = profile.filename
		profile.reset()
		profile.filename = profilePath
		# 7.0: Without writing the profile, we end up with inconsistencies between profile cache and actual profile.
		profile.write()
		resetConfig(_SPLDefaults7, profile)
		# Convert certain settings to a different format.
		profile["ColumnAnnouncement"]["IncludedColumns"] = set(_SPLDefaults7["ColumnAnnouncement"]["IncludedColumns"])

# In case one or more profiles had config issues, look up the error message from the following map.
_configErrors ={
	"fileReset":"Settings reset to defaults due to configuration file coruption",
	"completeReset":"All settings reset to defaults",
	"partialReset":"Some settings reset to defaults",
	"columnOrderReset":"Column announcement order reset to defaults",
	"partialAndColumnOrderReset":"Some settings, including column announcement order reset to defaults",
	"noInstantProfile":"Cannot find instant profile"
}

# To be run in app module constructor.
# With the load function below, load the config upon request.
# The below init function is really a vehicle that traverses through config profiles in a loop.
# Prompt the config error dialog only once.
_configLoadStatus = {} # Key = filename, value is pass or no pass.
# Track comments map.
trackComments = {}

def initConfig():
	# Load the default config from a list of profiles.
	global SPLConfig, SPLConfigPool, _configLoadStatus, SPLActiveProfile, SPLSwitchProfile, trackComments
	if SPLConfigPool is None: SPLConfigPool = []
	# Translators: The name of the default (normal) profile.
	if SPLActiveProfile is None: SPLActiveProfile = _("Normal profile")
	SPLConfigPool.append(unlockConfig(SPLIni, profileName=SPLActiveProfile, prefill=True))
	try:
		profiles = filter(lambda fn: os.path.splitext(fn)[-1] == ".ini", os.listdir(SPLProfiles))
		for profile in profiles:
			SPLConfigPool.append(unlockConfig(os.path.join(SPLProfiles, profile), profileName=os.path.splitext(profile)[0]))
	except WindowsError:
		pass
	# 7.0: Store the config as a dictionary.
	# This opens up many possibilities, including config caching, loading specific sections only and others (the latter saves memory).
	SPLConfig = dict(SPLConfigPool[0])
	SPLConfig["ActiveIndex"] = 0 # Holds settings from normal profile.
	# Locate instant profile.
	if "InstantProfile" in SPLConfig:
		try:
			SPLSwitchProfile = SPLConfigPool[getProfileIndexByName(SPLConfig["InstantProfile"])].name
		except ValueError:
			_configLoadStatus[SPLConfigPool[0].name] = "noInstantProfile"
		# 7.1: The config module knows the fate of the instant profile.
		del SPLConfig["InstantProfile"]
	# LTS: Load track comments if they exist.
	# This must be a separate file (another pickle file).
	try:
		trackComments = cPickle.load(file(os.path.join(globalVars.appArgs.configPath, "spltrackcomments.pickle"), "r"))
	except IOError:
		pass
	if len(_configLoadStatus):
		# Translators: Standard error title for configuration error.
		title = _("Studio add-on Configuration error")
		messages = []
		# 6.1: Display just the error message if the only corrupt profile is the normal profile.
		if len(_configLoadStatus) == 1 and SPLActiveProfile in _configLoadStatus:
			# Translators: Error message shown when add-on configuration had issues.
			messages.append("Your add-on configuration had following issues:\n\n")
			messages.append(_configErrors[_configLoadStatus[SPLActiveProfile]])
		else:
			# Translators: Error message shown when add-on configuration had issues.
			messages.append("One or more broadcast profiles had issues:\n\n")
			for profile in _configLoadStatus:
				error = _configErrors[_configLoadStatus[profile]]
				messages.append("{profileName}: {errorMessage}".format(profileName = profile, errorMessage = error))
		_configLoadStatus.clear()
		runConfigErrorDialog("\n".join(messages), title)
	# Fire up profile triggers.
	initProfileTriggers()
	# Let the update check begin.
	splupdate.initialize()
	# 7.1: Make sure encoder settings map isn't corrupted.
	try:
		streamLabels = ConfigObj(os.path.join(globalVars.appArgs.configPath, "splStreamLabels.ini"))
	except:
		open(os.path.join(globalVars.appArgs.configPath, "splStreamLabels.ini"), "w").close()
		# Translators: Message displayed if errors were found in encoder configuration file.
		runConfigErrorDialog(_("Your encoder settings had errors and were reset to defaults. If you have stream labels configured for various encoders, please add them again."),
		# Translators: Title of the encoder settings error dialog.
		_("Encoder settings error"))

# Unlock (load) profiles from files.
# LTS: Allow new profile settings to be overridden by a parent profile.
def unlockConfig(path, profileName=None, prefill=False, parent=None):
	# LTS: Suppose this is one of the steps taken when copying settings when instantiating a new profile.
	# If so, go through same procedure as though config passes validation tests, as all values from parent are in the right format.
	if parent is not None:
		SPLConfigCheckpoint = ConfigObj(parent, encoding="UTF-8")
		SPLConfigCheckpoint.filename = path
		SPLConfigCheckpoint.name = profileName
		_cacheConfig(SPLConfigCheckpoint)
		return SPLConfigCheckpoint
	# For the rest.
	global _configLoadStatus # To be mutated only during unlock routine.
	# Optimization: Profiles other than normal profile contains profile-specific sections only.
	# This speeds up profile loading routine significantly as there is no need to call a function to strip global settings.
	# 7.0: What if profiles have parsing errors?
	# If so, reset everything back to factory defaults.
	try:
		SPLConfigCheckpoint = ConfigObj(path, configspec = confspec7 if prefill else confspecprofiles, encoding="UTF-8")
	except:
		open(path, "w").close()
		SPLConfigCheckpoint = ConfigObj(path, configspec = confspec7 if prefill else confspecprofiles, encoding="UTF-8")
		_configLoadStatus[profileName] = "fileReset"
	# 5.2 and later: check to make sure all values are correct.
	# 7.0: Make sure errors are displayed as config keys are now sections and may need to go through subkeys.
	configTest = SPLConfigCheckpoint.validate(_val, copy=prefill, preserve_errors=True)
	if configTest != True:
		if not configTest:
			# Case 1: restore settings to defaults when 5.x config validation has failed on all values.
			# 6.0: In case this is a user profile, apply base configuration.
			resetConfig(_SPLDefaults7, SPLConfigCheckpoint)
			_configLoadStatus[profileName] = "completeReset"
		elif isinstance(configTest, dict):
			# Case 2: For 5.x and later, attempt to reconstruct the failed values.
			# 6.0: Cherry-pick global settings only.
			# 7.0: Go through failed sections.
			for setting in configTest.keys():
				if isinstance(configTest[setting], dict):
					for failedKey in configTest[setting].keys():
						# 7.0 optimization: just reload from defaults dictionary, as broadcast profiles contain profile-specific settings only.
						SPLConfigCheckpoint[setting][failedKey] = _SPLDefaults7[setting][failedKey]
			# 7.0: Disqualified from being cached this time.
			SPLConfigCheckpoint.write()
			_configLoadStatus[profileName] = "partialReset"
	_extraInitSteps(SPLConfigCheckpoint, profileName=profileName)
	SPLConfigCheckpoint.name = profileName
	# 7.0 optimization: Store an online backup.
	# This online backup is used to prolong SSD life (no need to save a config if it is same as this copy).
	_cacheConfig(SPLConfigCheckpoint)
	return SPLConfigCheckpoint

# Extra initialization steps such as converting value types.
def _extraInitSteps(conf, profileName=None):
	global _configLoadStatus
	columnOrder = conf["ColumnAnnouncement"]["ColumnOrder"]
	# Catch suttle errors.
	fields = _SPLDefaults7["ColumnAnnouncement"]["ColumnOrder"]
	invalidFields = 0
	for field in fields:
		if field not in columnOrder: invalidFields+=1
	if invalidFields or len(columnOrder) != 17:
		if profileName in _configLoadStatus and _configLoadStatus[profileName] == "partialReset":
			_configLoadStatus[profileName] = "partialAndColumnOrderReset"
		else:
			_configLoadStatus[profileName] = "columnOrderReset"
	conf["ColumnAnnouncement"]["ColumnOrder"] = fields
	conf["ColumnAnnouncement"]["IncludedColumns"] = set(conf["ColumnAnnouncement"]["IncludedColumns"])
	# Artist and Title must be present at all times (quite redundant, but just in case).
	conf["ColumnAnnouncement"]["IncludedColumns"].add("Artist")
	conf["ColumnAnnouncement"]["IncludedColumns"].add("Title")
	# Perform a similar check for metadata streaming.
	if len(conf["MetadataStreaming"]["MetadataEnabled"]) != 5:
		if profileName in _configLoadStatus and _configLoadStatus[profileName] == "partialReset":
			_configLoadStatus[profileName] = "partialAndMetadataReset"
		else:
			_configLoadStatus[profileName] = "metadataReset"
		conf["MetadataStreaming"]["MetadataEnabled"] = [False, False, False, False, False]

# Cache a copy of the loaded config.
# This comes in handy when saving configuration to disk. For the most part, no change occurs to config.
# This helps prolong life of a solid-state drive (preventing unnecessary writes).
_SPLCache = {}

def _cacheConfig(conf):
	global _SPLCache
	if _SPLCache is None: _SPLCache = {}
	key = None if conf.filename == SPLIni else conf.name
	_SPLCache[key] = {}
	# Take care of global flags in caching normal profile.
	# 7.2: If there are any old keys, tell the add-on this config must be saved.
	pre70count = 0
	for setting in conf.keys():
		if isinstance(conf[setting], dict): _SPLCache[key][setting] = dict(conf[setting])
		else:
			# 7.2: Remove old-style config, also prevent these keys from being cached and tell config routine these must be gone when saving.
			if setting != "InstantProfile":
				del conf[setting]
				pre70count+=1
	if pre70count: _SPLCache[key]["___pre70keys___"] = True
	# Column inclusion only.
	_SPLCache[key]["ColumnAnnouncement"]["IncludedColumns"] = list(conf["ColumnAnnouncement"]["IncludedColumns"])

# Record profile triggers.
# Each record (profile name) consists of seven fields organized as a list:
# A bit vector specifying which days should this profile be active, the first five fields needed for constructing a datetime.datetime object used to look up when to trigger this profile, and an integer specifying the duration in minutes.
profileTriggers = {} # Using a pickle is quite elegant.
profileTriggers2 = {} # For caching purposes.
# Profile triggers pickle.
SPLTriggersFile = os.path.join(globalVars.appArgs.configPath, "spltriggers.pickle")
# Trigger timer.
triggerTimer = None

# Prepare the triggers dictionary and other runtime support.
def initProfileTriggers():
	global profileTriggers, profileTriggers2, SPLTriggerProfile, triggerTimer
	try:
		profileTriggers = cPickle.load(file(SPLTriggersFile, "r"))
	except IOError:
		profileTriggers = {}
	# Cache profile triggers, used to compare the runtime dictionary against the cache.
	profileTriggers2 = dict(profileTriggers)
	# Is the triggers dictionary and the config pool in sync?
	if len(profileTriggers):
		nonexistent = []
		for profile in profileTriggers.keys():
			try:
				getProfileIndexByName(profile)
			except ValueError:
				nonexistent.append(profile)
				del profileTriggers[profile]
		if len(nonexistent):
			# Translators: Message presented indicating missing time-based profiles.
			wx.CallAfter(gui.messageBox, _("Could not locate the following time-based profile(s):\n{profiles}").format(profiles = ", ".join(nonexistent)),
			# Translators: The title of a dialog shown when some time-based profiles doesn't exist.
			_("Time-based profiles missing"), wx.OK|wx.ICON_ERROR)
	triggerStart()

# Locate time-based profiles if any.
# A 3-tuple will be returned, containing the next trigger time (for time delta calculation), the profile name for this trigger time and whether an immediate switch is necessary.
def nextTimedProfile(current=None):
	if current is None: current = datetime.datetime.now()
	# No need to proceed if no timed profiles are defined.
	if not len(profileTriggers): return None
	possibleTriggers = []
	for profile in profileTriggers.keys():
		shouldBeSwitched = False
		entry = list(profileTriggers[profile])
		# Construct the comparison datetime (see the profile triggers spec).
		triggerTime = datetime.datetime(entry[1], entry[2], entry[3], entry[4], entry[5])
		# Hopefully the trigger should be ready before the show, but sometimes it isn't.
		if current > triggerTime:
			profileTriggers[profile] = setNextTimedProfile(profile, entry[0], datetime.time(entry[4], entry[5]), date=current, duration=entry[6])
			if (current-triggerTime).seconds < entry[6]*60:
				shouldBeSwitched = True
		possibleTriggers.append((triggerTime, profile, shouldBeSwitched))
	return min(possibleTriggers) if len(possibleTriggers) else None

# Some helpers used in locating next air date/time.

# Set the next timed profile.
# Bits indicate the trigger days vector, hhmm is time, with the optional date being a specific date otherwise current date.
def setNextTimedProfile(profile, bits, switchTime, date=None, duration=0):
	if date is None: date = datetime.datetime.now()
	dayIndex = date.weekday()
	triggerCandidate = 64 >> dayIndex
	currentTime = datetime.time(date.hour, date.minute, date.second, date.microsecond)
	# Case 1: Show hasn't begun.
	if (bits & triggerCandidate) and currentTime < switchTime:
		delta = 0
	else:
		# Case 2: This is a weekly show.
		if bits == triggerCandidate:
			delta = 7
		else:
			import math
			# Scan the bit vector until finding the correct date and calculate the resulting delta (dayIndex modulo 7).
			# Take away the current trigger bit as this is invoked once the show air date has passed.
			days = bits-triggerCandidate if bits & triggerCandidate else bits
			currentDay = int(math.log(triggerCandidate, 2))
			nextDay = int(math.log(days, 2))
			# Hoping the resulting vector will have some bits set to 1...
			if triggerCandidate > days:
				delta = currentDay-nextDay
			else:
				triggerBit = -1
				for bit in xrange(currentDay-1, -1, -1):
					if 2 ** bit & days:
						triggerBit = bit
						break
				if triggerBit > -1:
					delta = currentDay-triggerBit
				else:
					delta = 7-(nextDay-currentDay)
	date += datetime.timedelta(delta)
	return [bits, date.year, date.month, date.day, switchTime.hour, switchTime.minute, duration]

# Find if another profile is occupying the specified time slot.
def duplicateExists(map, profile, bits, hour, min, duration):
	if len(map) == 0 or (len(map) == 1 and profile in map): return False
	# Convert hours and minutes to an integer for faster comparison.
	start1 = (hour*60) + min
	end1 = start1+duration
	# A possible duplicate may exist simply because of bits.
	for item in filter(lambda p: p != profile, map.keys()):
		if map[item][0] == bits:
			entry = map[item]
			start2 = (entry[4] * 60) + entry[5]
			end2 = start2+entry[6]
			if start1 <= start2 <= end1 or start2 <= start1 <= end2:
				return True
	return False

# Start the trigger timer based on above information.
# Can be restarted if needed.
def triggerStart(restart=False):
	global SPLTriggerProfile, triggerTimer
	# Restart the timer when called from triggers dialog in order to prevent multiple timers from running.
	if triggerTimer is not None and triggerTimer.IsRunning() and restart:
		triggerTimer.Stop()
		triggerTimer = None
	queuedProfile = nextTimedProfile()
	if queuedProfile is not None:
		try:
			SPLTriggerProfile = queuedProfile[1]
		except ValueError:
			SPLTriggerProfile = None
		# We are in the midst of a show, so switch now.
		if queuedProfile[2]:
			triggerProfileSwitch()
		else:
			switchAfter = (queuedProfile[0] - datetime.datetime.now())
			if switchAfter.days == 0 and switchAfter.seconds <= 3600:
				time.sleep((switchAfter.microseconds+1000) / 1000000.0)
				triggerTimer = SPLCountdownTimer(switchAfter.seconds, triggerProfileSwitch, SPLConfig["Advanced"]["ProfileTriggerThreshold"])
				triggerTimer.Start()

# Dump profile triggers pickle away.
def saveProfileTriggers():
	global triggerTimer, profileTriggers, profileTriggers2
	if triggerTimer is not None and triggerTimer.IsRunning():
		triggerTimer.Stop()
		triggerTimer = None
	# Unless it is a daily show, profile triggers would not have been modified.
	# This trick is employed in order to reduce unnecessary disk writes.
	if profileTriggers != profileTriggers2:
		cPickle.dump(profileTriggers, file(SPLTriggersFile, "wb"))
	profileTriggers = None
	profileTriggers2 = None

# Instant profile switch helpers.
# A number of helper functions assisting instant switch profile routine and others, including sorting and locating the needed profile upon request.

# Fetch the profile index with a given name.
def getProfileIndexByName(name):
	# LTS: Traverse config pool if the name isn't normal profile nor it is the name of the last profile.
	if name == _("Normal profile"):
		return 0
		elif name == SPLConfigPool[-1].name:
			return -1
	try:
		return [profile.name for profile in SPLConfigPool].index(name)
	except ValueError:
		raise ValueError("The specified profile does not exist")

# And:
def getProfileByName(name):
	return SPLConfigPool[getProfileIndexByName(name)]

# Copy settings across profiles.
# Setting complete flag controls whether profile-specific settings are applied (true otherwise, only set when resetting profiles).
def copyProfile(sourceProfile, targetProfile, complete=False):
	for section in sourceProfile.keys() if complete else _mutatableSettings7:
		targetProfile[section] = dict(sourceProfile[section])

# Merge sections when switching profiles.
# This is also employed by the routine which saves changes to a profile when user selects a different profile from add-on settings dialog.
# Profiles refer to indecies.
# Active refers to whether this is a runtime switch (false if saving profiles).
def mergeSections(profile, active=True):
	global SPLConfig, SPLConfigPool
	copyProfile(SPLConfigPool[profile], SPLConfig)
	if active: SPLConfig["ActiveIndex"] = profile

# A reverse of the above.
def applySections(profile, key=None):
	global SPLConfig, SPLConfigPool
	if key is None:
		copyProfile(SPLConfig, SPLConfigPool[profile])
	else:
		# A slash (/) will denote section/key hierarchy.
		tree, leaf = key.split("/")
		if tree in SPLConfig:
			if leaf == "": # Section only.
				SPLConfigPool[profile][tree] = dict(SPLConfig[tree])
			else:
				SPLConfigPool[profile][tree][leaf] = SPLConfig[tree][leaf]

# Last but not least...
# Module level version of get profile flags function.
# Optional keyword arguments are to be added when called from dialogs such as add-on settings.
# A crucial kwarg is contained, and if so, profile flags set will be returned.
def getProfileFlags(name, active=None, instant=None, triggers=None, contained=False):
	flags = set()
	if active is None: active = SPLActiveProfile
	if instant is None: instant = SPLSwitchProfile
	if triggers is None: triggers = profileTriggers
	if name == active:
		# Translators: A flag indicating the currently active broadcast profile.
		flags.add(_("active"))
	if name == instant:
		# Translators: A flag indicating the broadcast profile is an instant switch profile.
		flags.add(_("instant switch"))
	if name in triggers:
		# Translators: A flag indicating the time-based triggers profile.
		flags.add(_("time-based"))
	if not contained:
		return name if len(flags) == 0 else "{0} <{1}>".format(name, ", ".join(flags))
	else: return flags

# Is the config pool itself sorted?
# This check is performed when displaying broadcast profiles.
def isConfigPoolSorted():
		profileNames = [profile.name for profile in SPLConfigPool][1:]
		for pos in xrange(len(profileNames)-1):
			if profileNames[pos] > profileNames[pos+1]:
				return False
		return True


# Perform some extra work before writing the config file.
def _preSave(conf):
	# Perform global setting processing only for the normal profile.
	# 7.0: if this is a second pass, index 0 may not be normal profile at all.
	# Use profile path instead.
	if conf.filename == SPLIni:
		# Cache instant profile for later use.
		if SPLSwitchProfile is not None:
			conf["InstantProfile"] = SPLSwitchProfile
			# 7.0: Also update the runtime dictionary.
			SPLConfig["InstantProfile"] = SPLSwitchProfile
		else:
			try:
				del conf["InstantProfile"]
			except KeyError:
				pass
	# For other profiles, remove global settings before writing to disk.
	else:
		# 6.1: Make sure column inclusion aren't same as default values.
		if len(conf["ColumnAnnouncement"]["IncludedColumns"]) == 17:
			del conf["ColumnAnnouncement"]["IncludedColumns"]
		for setting in conf.keys():
			for key in conf[setting].keys():
				try:
					if conf[setting][key] == _SPLDefaults7[setting][key]:
						del conf[setting][key]
				except KeyError:
					pass
			if setting in conf and not len(conf[setting]):
				del conf[setting]

# Check if the profile should be written to disk.
# For the most part, no setting will be modified.
def shouldSave(profile):
	tree = None if profile.filename == SPLIni else profile.name
	# One downside of caching: new profiles are not recognized as such.
	# 7.2 only: Also save if pre-7.0 keys were found.
	# 8.0: Streamline the whole process by comparing values alone instead of walking the entire dictionary.
	# The old loop will be kept in 7.x/LTS for compatibility and to reduce risks associated with accidental saving/discard.
	if "___new___" in _SPLCache[tree] or "___pre70keys___" in _SPLCache[tree]: return True
	for section in profile.keys():
		if isinstance(profile[section], dict):
			for key in profile[section]:
				if profile[section][key] != _SPLCache[tree][section][key]:
					return True # Setting modified.
	return False


# Save configuration database.
def saveConfig():
	# Save all config profiles.
	global SPLConfig, SPLConfigPool, SPLActiveProfile, SPLPrevProfile, SPLSwitchProfile, _SPLCache
	# 7.0: Turn off auto update check timer.
	if splupdate._SPLUpdateT is not None and splupdate._SPLUpdateT.IsRunning(): splupdate._SPLUpdateT.Stop()
	splupdate._SPLUpdateT = None
	# Close profile triggers dictionary.
	saveProfileTriggers()
	# Dump track comments.
	cPickle.dump(trackComments, file(os.path.join(globalVars.appArgs.configPath, "spltrackcomments.pickle"), "wb"))
	# Save update check state.
	splupdate.terminate()
	# Save profile-specific settings to appropriate dictionary if this is the case.
	activeIndex = SPLConfig["ActiveIndex"]
	del SPLConfig["ActiveIndex"]
	if activeIndex > 0:
		applySections(activeIndex)
	# 7.0: Save normal profile first.
	# Temporarily merge normal profile.
	mergeSections(0)
	# 6.1: Transform column inclusion data structure (for normal profile) now.
	# 7.0: This will be repeated for broadcast profiles later.
	SPLConfigPool[0]["ColumnAnnouncement"]["IncludedColumns"] = list(SPLConfigPool[0]["ColumnAnnouncement"]["IncludedColumns"])
	_preSave(SPLConfigPool[0])
	# Global flags, be gone.
	del SPLConfig["ColumnExpRange"]
	# Disk write optimization check please.
	if shouldSave(SPLConfigPool[0]):
		SPLConfigPool[0].write()
	del SPLConfigPool[0]
	# Now save broadcast profiles.
	for configuration in SPLConfigPool:
		if configuration is not None:
			configuration["ColumnAnnouncement"]["IncludedColumns"] = list(configuration["ColumnAnnouncement"]["IncludedColumns"])
			# 7.0: See if profiles themselves must be saved.
			# This must be done now, otherwise changes to broadcast profiles (cached) will not be saved as presave removes them.
			if shouldSave(configuration):
				_preSave(configuration)
				configuration.write()
	SPLConfig.clear()
	SPLConfig = None
	SPLConfigPool = None
	SPLActiveProfile = None
	SPLPrevProfile = None
	SPLSwitchProfile = None
	_SPLCache.clear()
	_SPLCache = None


# Switch between profiles.
SPLActiveProfile = None
SPLPrevProfile = None
SPLSwitchProfile = None
SPLTriggerProfile = None

# A general-purpose profile switcher.
# Allows the add-on to switch between profiles as a result of manual intervention or through profile trigger timer.
# Instant profile switching is just a special case of this function.
def switchProfile(prevProfile, newProfile):
	global SPLConfig, SPLActiveProfile, SPLPrevProfile
	from splconfui import _configDialogOpened
	if _configDialogOpened:
		# Translators: Presented when trying to switch to an instant switch profile when add-on settings dialog is active.
		ui.message(_("Add-on settings dialog is open, cannot switch profiles"))
		return
	mergeSections(newProfile)
	SPLActiveProfile = SPLConfigPool[newProfile].name
	SPLConfig["ActiveIndex"] = newProfile
	if prevProfile is not None:
		# Translators: Presented when switch to instant switch profile was successful.
		ui.message(_("Switching to {newProfileName}").format(newProfileName = SPLActiveProfile))
		# Pause automatic update checking.
		if SPLConfig["Update"]["AutoUpdateCheck"]:
			if splupdate._SPLUpdateT is not None and splupdate._SPLUpdateT.IsRunning: splupdate._SPLUpdateT.Stop()
	else:
		# Translators: Presented when switching from instant switch profile to a previous profile.
		ui.message(_("Returning to {previousProfile}").format(previousProfile = SPLActiveProfile))
		# Resume auto update checker if told to do so.
		if SPLConfig["Update"]["AutoUpdateCheck"]: updateInit()
	SPLPrevProfile = prevProfile
	# Use the module-level metadata reminder method if told to do so now.
	if SPLConfig["General"]["MetadataReminder"] in ("startup", "instant"):
		_metadataAnnouncer(reminder=True)

# Called from within the app module.
def instantProfileSwitch():
	global SPLConfig, SPLActiveProfile
	if SPLSwitchProfile is None:
		# Translators: Presented when trying to switch to an instant switch profile when the instant switch profile is not defined.
		ui.message(_("No instant switch profile is defined"))
	else:
		if SPLPrevProfile is None:
			if SPLActiveProfile == SPLSwitchProfile:
				# Translators: Presented when trying to switch to an instant switch profile when one is already using the instant switch profile.
				ui.message(_("You are already in the instant switch profile"))
				return
			# Switch to the given profile.
			switchProfileIndex = getProfileIndexByName(SPLSwitchProfile)
			# 6.1: Do to referencing nature of Python, use the profile index function to locate the index for the soon to be deactivated profile.
			# 7.0: Store the profile name instead in order to prevent profile index mangling if profiles are deleted.
			# Pass in the prev profile, which will be None for instant profile switch.
			# 7.0: Now activate "activeProfile" argument which controls the behavior of the function below.
			switchProfile(SPLActiveProfile, switchProfileIndex)
		else:
			switchProfile(None, getProfileIndexByName(SPLPrevProfile))

# The triggers version of the above function.
_SPLTriggerEndTimer = None
# Record if time-based profile is active or not.
_triggerProfileActive = False

def triggerProfileSwitch():
	global triggerTimer, _SPLTriggerEndTimer, _triggerProfileActive
	if SPLTriggerProfile is None and _triggerProfileActive:
		raise RuntimeError("Trigger profile flag cannot be active when the trigger profile itself isn't defined")
	if SPLPrevProfile is None:
		if SPLActiveProfile == SPLTriggerProfile:
			# Translators: Presented when trying to switch to an instant switch profile when one is already using the instant switch profile.
			ui.message(_("A profile trigger is already active"))
			return
		# Switch to the given profile.
		triggerProfileIndex = getProfileIndexByName(SPLTriggerProfile)
		# Pass in the prev profile, which will be None for instant profile switch.
		switchProfile(SPLActiveProfile, triggerProfileIndex)
		# Set the global trigger flag to inform various subsystems such as add-on settings dialog.
		_triggerProfileActive = True
		# Set the next trigger date and time.
		triggerSettings = profileTriggers[SPLTriggerProfile]
		# Set next trigger if no duration is specified.
		if triggerSettings[6] == 0:
			profileTriggers[SPLTriggerProfile] = setNextTimedProfile(SPLTriggerProfile, triggerSettings[0], datetime.time(triggerSettings[4], triggerSettings[5]))
		else:
			_SPLTriggerEndTimer = wx.PyTimer(triggerProfileSwitch)
			_SPLTriggerEndTimer.Start(triggerSettings[6] * 60 * 1000, True)
	else:
		switchProfile(None, getProfileIndexByName(SPLPrevProfile))
		_triggerProfileActive = False
		# Stop the ending timer.
		if _SPLTriggerEndTimer is not None and _SPLTriggerEndTimer.IsRunning():
			_SPLTriggerEndTimer.Stop()
			_SPLTriggerEndTimer = None


# Automatic update checker.

# The function below is called as part of the update check timer.
# Its only job is to call the update check function (splupdate) with the auto check enabled.
# The update checker will not be engaged if an instant switch profile is active or it is not time to check for it yet (check will be done every 24 hours).
def autoUpdateCheck():
	splupdate.updateCheck(auto=True, continuous=SPLConfig["Update"]["AutoUpdateCheck"])

# The timer itself.
# A bit simpler than NVDA Core's auto update checker.
def updateInit():
	currentTime = time.time()
	nextCheck = splupdate.SPLAddonCheck+86400.0
	if splupdate.SPLAddonCheck < currentTime < nextCheck:
		interval = int(nextCheck - currentTime)
	elif splupdate.SPLAddonCheck < nextCheck < currentTime:
		interval = 86400
		# Call the update check now.
		splupdate.updateCheck(auto=True) # No repeat here.
	splupdate._SPLUpdateT = wx.PyTimer(autoUpdateCheck)
	splupdate._SPLUpdateT.Start(interval * 1000, True)


# Let SPL track item know if it needs to build description pieces.
# To be renamed and used in other places in 7.0.
def _shouldBuildDescriptionPieces():
	return (not SPLConfig["ColumnAnnouncement"]["UseScreenColumnOrder"]
	and (SPLConfig["ColumnAnnouncement"]["ColumnOrder"] != _SPLDefaults7["ColumnAnnouncement"]["ColumnOrder"]
	or len(SPLConfig["ColumnAnnouncement"]["IncludedColumns"]) != 17))


# Additional configuration dialogs
# See splconfui module for basic configuration dialogs.

# A common alarm dialog
# Based on NVDA core's find dialog code (implemented by the author of this add-on).
# Extended in 2016 to handle microphone alarms.
# Only one instance can be active at a given moment (code borrowed from GUI's exit dialog routine).
_alarmDialogOpened = False

# A common alarm error dialog.
def _alarmError():
	# Translators: Text of the dialog when another alarm dialog is open.
	gui.messageBox(_("Another alarm dialog is open."),_("Error"),style=wx.OK | wx.ICON_ERROR)

class SPLAlarmDialog(wx.Dialog):
	"""A dialog providing common alarm settings.
	This dialog contains a number entry field for alarm duration and a check box to enable or disable the alarm.
	For one particular case, it consists of two number entry fields.
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

	def __init__(self, parent, level=0):
		inst = SPLAlarmDialog._instance() if SPLAlarmDialog._instance else None
		if inst:
			return
		# Use a weakref so the instance can die.
		import weakref
		SPLAlarmDialog._instance = weakref.ref(self)

		# Now the actual alarm dialog code.
		# 8.0: Apart from level 0 (all settings shown), levels change title.
		titles = (_("Alarms Center"), _("End of track alarm"), _("Song intro alarm"), _("Microphone alarm"))
		super(SPLAlarmDialog, self).__init__(parent, wx.ID_ANY, titles[level])
		self.level = level
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		if level in (0, 1):
			timeVal = SPLConfig["IntroOutroAlarms"]["EndOfTrackTime"]
			alarmSizer = wx.BoxSizer(wx.HORIZONTAL)
			alarmMessage = wx.StaticText(self, wx.ID_ANY, label=_("Enter &end of track alarm time in seconds (currently {curAlarmSec})").format(curAlarmSec = timeVal))
			alarmSizer.Add(alarmMessage)
			self.outroAlarmEntry = wx.SpinCtrl(self, wx.ID_ANY, min=1, max=59)
			self.outroAlarmEntry.SetValue(timeVal)
			self.outroAlarmEntry.SetSelection(-1, -1)
			alarmSizer.Add(self.outroAlarmEntry)
			mainSizer.Add(alarmSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
			self.outroToggleCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Notify when end of track is approaching"))
			self.outroToggleCheckBox.SetValue(SPLConfig["IntroOutroAlarms"]["SayEndOfTrack"])
			mainSizer.Add(self.outroToggleCheckBox,border=10,flag=wx.BOTTOM)

		if level in (0, 2):
			rampVal = SPLConfig["IntroOutroAlarms"]["SongRampTime"]
			alarmSizer = wx.BoxSizer(wx.HORIZONTAL)
			alarmMessage = wx.StaticText(self, wx.ID_ANY, label=_("Enter song &intro alarm time in seconds (currently {curRampSec})").format(curRampSec = rampVal))
			alarmSizer.Add(alarmMessage)
			self.introAlarmEntry = wx.SpinCtrl(self, wx.ID_ANY, min=1, max=9)
			self.introAlarmEntry.SetValue(rampVal)
			self.introAlarmEntry.SetSelection(-1, -1)
			alarmSizer.Add(self.introAlarmEntry)
			mainSizer.Add(alarmSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
			self.introToggleCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Notify when end of introduction is approaching"))
			self.introToggleCheckBox.SetValue(SPLConfig["IntroOutroAlarms"]["SaySongRamp"])
			mainSizer.Add(self.introToggleCheckBox,border=10,flag=wx.BOTTOM)

		if level in (0, 3):
			micAlarm = SPLConfig["MicrophoneAlarm"]["MicAlarm"]
			micAlarmInterval = SPLConfig["MicrophoneAlarm"]["MicAlarmInterval"]
			if micAlarm:
				# Translators: A dialog message to set microphone active alarm (curAlarmSec is the current mic monitoring alarm in seconds).
				timeMSG = _("Enter microphone alarm time in seconds (currently {curAlarmSec}, 0 disables the alarm)").format(curAlarmSec = micAlarm)
			else:
				# Translators: A dialog message when microphone alarm is disabled (set to 0).
				timeMSG = _("Enter microphone alarm time in seconds (currently disabled, 0 disables the alarm)")
			alarmSizer = wx.BoxSizer(wx.VERTICAL)
			alarmMessage = wx.StaticText(self, wx.ID_ANY, label=timeMSG)
			alarmSizer.Add(alarmMessage)
			self.micAlarmEntry = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=7200)
			self.micAlarmEntry.SetValue(micAlarm)
			self.micAlarmEntry.SetSelection(-1, -1)
			alarmSizer.Add(self.micAlarmEntry)
			alarmMessage = wx.StaticText(self, wx.ID_ANY, label=_("Microphone alarm interval"))
			alarmSizer.Add(alarmMessage)
			self.micIntervalEntry = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=60)
			self.micIntervalEntry.SetValue(micAlarmInterval)
			self.micIntervalEntry.SetSelection(-1, -1)
			alarmSizer.Add(self.micIntervalEntry)
			mainSizer.Add(alarmSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)

		mainSizer.AddSizer(self.CreateButtonSizer(wx.OK|wx.CANCEL))
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)
		if level in (0, 1): self.outroAlarmEntry.SetFocus()
		elif level == 2: self.introAlarmEntry.SetFocus()
		elif level == 3: self.micAlarmEntry.SetFocus()

	def onOk(self, evt):
		global SPLConfig, _alarmDialogOpened
		# Optimization: don't bother if Studio is dead and if the same value has been entered.
		import winUser
		if winUser.user32.FindWindowA("SPLStudio", None):
			# Gather settings to be applied in section/key format.
			settings = []
			if self.level in (0, 1):
				SPLConfig["IntroOutroAlarms"]["EndOfTrackTime"] = self.outroAlarmEntry.GetValue()
				settings.append("IntroOutroAlarms/EndOfTrackTime")
				SPLConfig["IntroOutroAlarms"]["SayEndOfTrack"] = self.outroToggleCheckBox.GetValue()
				settings.append("IntroOutroAlarms/SayEndOfTrack")
			elif self.level in (0, 2):
				SPLConfig["IntroOutroAlarms"]["SongRampTime"] = self.introAlarmEntry.GetValue()
				settings.append("IntroOutroAlarms/SongRampTime")
				SPLConfig["IntroOutroAlarms"]["SaySongRamp"] = self.introToggleCheckBox.GetValue()
				settings.append("IntroOutroAlarms/SaySongRamp")
			elif self.level in (0, 3):
				SPLConfig["MicrophoneAlarm"]["MicAlarm"] = self.micAlarmEntry.GetValue()
				settings.append("MicrophoneAlarm/MicAlarm")
				SPLConfig["MicrophoneAlarm"]["MicAlarmInterval"] = self.micIntervalEntry.GetValue()
				settings.append("MicrophoneAlarm/MicAlarmInterval")
			# Apply alarm settings only.
			for setting in settings:
				applySections(SPLConfig["ActiveIndex"], key=setting)
		self.Destroy()
		_alarmDialogOpened = False

	def onCancel(self, evt):
		self.Destroy()
		global _alarmDialogOpened
		_alarmDialogOpened = False


# Startup dialogs.

# Audio ducking reminder (NVDA 2016.1 and later).
class AudioDuckingReminder(wx.Dialog):
	"""A dialog to remind users to turn off audio ducking (NVDA 2016.1 and later).
	"""

	def __init__(self, parent):
		# Translators: Title of a dialog displayed when the add-on starts reminding broadcasters to disable audio ducking.
		super(AudioDuckingReminder, self).__init__(parent, title=_("SPL Studio and audio ducking"))

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: A message displayed if audio ducking should be disabled.
		label = wx.StaticText(self, wx.ID_ANY, label=_("NVDA 2016.1 and later allows NVDA to decrease volume of background audio including that of Studio. In order to not disrupt the listening experience of your listeners, please disable audio ducking by opening synthesizer dialog in NVDA and selecting 'no ducking' from audio ducking mode combo box or press NVDA+Shift+D."))
		mainSizer.Add(label,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: A checkbox to turn off audio ducking reminder message.
		self.audioDuckingReminder=wx.CheckBox(self,wx.NewId(),label=_("Do not show this message again"))
		self.audioDuckingReminder.SetValue(not SPLConfig["Startup"]["AudioDuckingReminder"])
		sizer.Add(self.audioDuckingReminder, border=10,flag=wx.TOP)
		mainSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		mainSizer.Add(self.CreateButtonSizer(wx.OK))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.audioDuckingReminder.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		global SPLConfig
		if self.audioDuckingReminder.Value:
			SPLConfig["Startup"]["AudioDuckingReminder"] = not self.audioDuckingReminder.Value
		self.Destroy()

# Welcome dialog (emulating NvDA Core)
class WelcomeDialog(wx.Dialog):

	# Translators: A message giving basic information about the add-on.
	welcomeMessage=_("""Welcome to StationPlaylist Studio add-on for NVDA,
your companion to broadcasting with SPL Studio using NVDA screen reader.

Highlights of StationPlaylist Studio add-on include:
* Layer commands for obtaining status information.
* Various ways to examine track columns.
* Various ways to find tracks.
* Cart Explorer to learn cart assignments.
* Comprehensive settings and documentation.
* Check for add-on updates automatically or manually.
* Completely free, open-source and community-driven.
* And much more.

Visit www.stationplaylist.com for details on StationPlaylist Studio.
Visit StationPlaylist entry on NVDA Community Add-ons page (addons.nvda-project.org) for more information on the add-on and to read the documentation.
Want to see this dialog again? Just press Alt+NVDA+F1 while using Studio to return to this dialog.
Have something to say about the add-on? Press Control+NVDA+hyphen (-) to send a feedback to the developer of this add-on using your default email program.

Thank you.""")

	def __init__(self, parent):
		# Translators: Title of a dialog displayed when the add-on starts presenting basic information, similar to NVDA's own welcome dialog.
		super(WelcomeDialog, self).__init__(parent, title=_("Welcome to StationPlaylist Studio add-on"))

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(self, wx.ID_ANY, label=self.welcomeMessage)
		mainSizer.Add(label,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: A checkbox to show welcome dialog.
		self.showWelcomeDialog=wx.CheckBox(self,wx.NewId(),label=_("Show welcome dialog when I start Studio"))
		self.showWelcomeDialog.SetValue(SPLConfig["Startup"]["WelcomeDialog"])
		sizer.Add(self.showWelcomeDialog, border=10,flag=wx.TOP)
		mainSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		mainSizer.Add(self.CreateButtonSizer(wx.OK))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.showWelcomeDialog.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		global SPLConfig
		SPLConfig["Startup"]["WelcomeDialog"] = self.showWelcomeDialog.Value
		self.Destroy()

# And to open the above dialog and any other dialogs.
def showStartupDialogs():
	if SPLConfig["Startup"]["WelcomeDialog"]:
		gui.mainFrame.prePopup()
		WelcomeDialog(gui.mainFrame).Show()
		gui.mainFrame.postPopup()
	try:
		import audioDucking
		if SPLConfig["Startup"]["AudioDuckingReminder"] and audioDucking.isAudioDuckingSupported():
			gui.mainFrame.prePopup()
			AudioDuckingReminder(gui.mainFrame).Show()
			gui.mainFrame.postPopup()
	except ImportError:
		pass


# Message verbosity pool.
# To be moved to its own module in add-on 7.0.
# This is a multimap, consisting of category, value and message.
# Most of the categories are same as confspec keys, hence the below message function is invoked when settings are changed.
def message(category, value):
	verbosityLevels = ("beginner", "advanced")
	ui.message(messagePool[category][value][verbosityLevels.index(SPLConfig["General"]["MessageVerbosity"])])

messagePool={
	"BeepAnnounce":
		{True:
			# Translators: Reported when status announcement is set to beeps in SPL Studio.
			(_("Status announcement beeps"),
			# Translators: Reported when status announcement is set to beeps in SPL Studio.
			_("Beeps")),
		False:
			# Translators: Reported when status announcement is set to beeps in SPL Studio.
			(_("Status announcement words"),
			# Translators: Reported when status announcement is set to beeps in SPL Studio.
			_("Words"))},
	"BrailleTimer":
		{"off":
			# Translators: A setting in braille timer options.
			(_("Braille timer off"), _("Off")),
		"outro":
			# Translators: A setting in braille timer options.
			(_("Braille track endings"),
						# Translators: A setting in braille timer options.
			_("Outro")),
		"intro":
			# Translators: A setting in braille timer options.
			(_("Braille intro endings"),
						# Translators: A setting in braille timer options.
			_("Intro")),
		"both":
			# Translators: A setting in braille timer options.
			(_("Braille intro and track endings"),
						# Translators: A setting in braille timer options.
			_("Both"))},
	"LibraryScanAnnounce":
		{"off":
			# Translators: A setting in library scan announcement options.
			(_("Do not announce library scans"), _("Off")),
		"ending":
			# Translators: A setting in library scan announcement options.
			(_("Announce start and end of a library scan"),
			_("Start and end only")),
		"progress":
			# Translators: A setting in library scan announcement options.
			(_("Announce the progress of a library scan"),
			_("Scan progress")),
		"numbers":
			# Translators: A setting in library scan announcement options.
			(_("Announce progress and item count of a library scan"),
			_("Scan count"))}}

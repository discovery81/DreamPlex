# -*- coding: utf-8 -*-
"""
DreamPlex Plugin by DonDavici, 2012
and jbleyel 2021

Original -> https://github.com/oe-alliance/DreamPlex
Fork -> https://github.com/oe-alliance/DreamPlex

Some of the code is from other plugins:
all credits to the coders :-)

DreamPlex Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

DreamPlex Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
"""
#===============================================================================
# IMPORT
#===============================================================================
import copy
from Screens.MessageBox import MessageBox

from Tools import Notifications
from Components.config import config, configfile

from .DPH_Singleton import Singleton

from .__common__ import printl2 as printl, getSkinDebugMode

#===========================================================================
#
#===========================================================================


def getDefaultCineElementsList():
	printl("", "DP_ViewFactory::", "S")

	elementsList = ["pagination", "total", "backdrop", "poster", "writer", "resolution", "cast", "audio", "info",
	                "aspect", "codec", "rated", "title", "grandparentTitle", "tag", "shortDescription", "subtitles", "director",
	                "genre", "year", "duration", "rating_stars", "sound", "soundchannels", "pagination", "total", "leafCount", "unviewedLeafCount", "viewedLeafCount",
	                "videoCodec", "bitrate", "videoFrameRate", "audioChannels", "aspectRatio",
	                "videoResolution", "audioCodec", "file", "childCount", "studio"]

	printl("", "DP_ViewFactory::", "C")
	return elementsList

#===========================================================================
#
#===========================================================================


def getDefaultDirectoryElementsList():
	printl("", "DP_ViewFactory::getDefaultDirectoryElementsList", "S")

	elementsList = ["pagination", "total", "title", "tag", "shortDescription"]

	printl("", "DP_ViewFactory::getDefaultDirectoryElementsList", "C")
	return elementsList

#===========================================================================
#
#===========================================================================


def getNoneDirectoryElements():
	printl("", "DP_ViewFactory::getNoneDirectoryElements", "S")

	directoryElementsList = getDefaultDirectoryElementsList()
	cineElementsList = getDefaultCineElementsList()

	noneDirectoryElements = []
	for element in cineElementsList:
		if element not in directoryElementsList:
			noneDirectoryElements.append(element)

	return noneDirectoryElements

	printl("", "DP_ViewFactory::getNoneDirectoryElements", "C")
#===========================================================================
#
#===========================================================================


def getDefaultSettingsList():
	printl("", "DP_ViewFactory::getDefaultSettingsList", "S")

	settingsList = ["itemsPerPage", "apiLevel", "screen", "backdropVideos", "name", "backdropVideoHeight", "backdropVideoWidth", "posterHeight", "posterWidth", "backdropHeight", "backdropWidth", "miniTv", "type"]

	printl("", "DP_ViewFactory::getDefaultSettingsList", "C")
	return settingsList

#===============================================================================
#
#===============================================================================


def getViews(libraryName):
	"""
	@return: availableViewList
	"""
	printl("", "DP_ViewFactory::getViews", "S")

	if libraryName == "movies":
		availableViewList = getViewsFromSkinParams("movieView")

	elif libraryName == "mixed":
		availableViewList = getViewsFromSkinParams("mixedView")

	elif libraryName == "shows":
		availableViewList = getViewsFromSkinParams("showView")

	elif libraryName == "music":
		availableViewList = getViewsFromSkinParams("musicView")

	else:
		availableViewList = ()

	printl("", "DP_ViewFactory::getViews", "C")
	return availableViewList

#===========================================================================
#
#===========================================================================


def getViewsFromSkinParams(myType):
	printl("", "DP_ViewFactory::getViewsFromSkinParams", "S")

	tree = Singleton().getSkinParamsInstance()

	availableViewList = []

	if myType == "movieView":
		myFile = "DP_ViewMovies"
		defaultParams = getMovieViewDefaults()

	elif myType == "mixedView":
		myFile = "DP_ViewMixed"
		defaultParams = getMovieViewDefaults()
		# todo maybe we extend for our own definition
		# we rewrite to movieView because we use it for now as reference
		myType = "movieView"

	elif myType == "showView":
		myFile = "DP_ViewShows"
		defaultParams = getShowViewDefaults()

	elif myType == "musicView":
		myFile = "DP_ViewMusic"
		defaultParams = getMusicViewDefaults()

	else:
		raise Exception

	for view in tree.findall(myType):
		# lets copy params to new alterable variable
		currentParams = copy.deepcopy(defaultParams)
		#printl("currentParams: " + str(currentParams), __name__, "D")

		useMe, subViewDict = getSubViewParams(view)
		if useMe:
			currentParams["subViews"] = subViewDict

		name = str(view.get("name"))
		printl("viewMe:" + str(view), "DP_ViewFactory::getViewsFromSkinParams", "D")

		# settings
		settings = defaultParams["settings"]
		for setting in settings:
			printl("setting:" + str(setting), "DP_ViewFactory::getViewsFromSkinParams", "D")
			#check if there are params that we have to override
			value = view.get(setting, None)
			printl("value: " + str(value), "DP_ViewFactory::getViewsFromSkinParams", "D")

			# check if this value is mandatory
			# if we are mandatory we stop here
			if defaultParams["settings"][setting] == "mandatory" and value is None:
				skinDebugMode = translateValues(getSkinDebugMode())
				if config.plugins.dreamplex.skin.value != "default" and not skinDebugMode:
					config.plugins.dreamplex.skin.value = "default"
					config.plugins.dreamplex.skin.save()
					configfile.save()
					Notifications.AddNotification(MessageBox, "DreamPlex crashed due to a skin error!\nSwitching back to default in settings.\n", type=MessageBox.TYPE_INFO, timeout=10)
				else:
					printl("this value: " + str(value) + "is misssing ....", "DP_ViewFactory::getViewsFromSkinParams", "D")
					raise Exception
			else:
				currentParams["settings"][setting] = translateValues(value)

		view = (name, myFile, currentParams)

		availableViewList.append(view)

	#printl("availableViewList: " + str(availableViewList), __name__, "D")
	printl("", "DP_ViewFactory::getViewsFromSkinParams", "C")
	return availableViewList

#===========================================================================
#
#===========================================================================


def getSubViewParams(tree):
	printl("", "DP_ViewFactory::getSubViewParams", "S")

	useMe = False
	myDict = {}

	for view in tree.findall("subView"):
		useMe = True
		subViewName = view.get("name", None)
		myDictParams = {}

		if subViewName is not None: # we do this for compatibility with oe16 with python 2.7
			for element in view.findall("element"):
				name = element.get("name")
				myDictParams[name] = {}

				params = element.attrib
				#printl("params: " + str(params), __name__, "D")

				for key, value in params.items():
					translatedValue = translateValues(value)

					if key != "name":
						myDictParams[name][key] = translatedValue

		myDict[subViewName] = myDictParams

	printl("", "DP_ViewFactory::getSubViewParams", "C")
	return useMe, myDict

#===========================================================================
#
#===========================================================================


def getMovieViewDefaults():
	printl("", "DP_ViewFactory::getMovieViewDefaults", "S")
	params = {}

	params["settings"] = {}
	settingsList = getDefaultSettingsList()
	# mandatory items have to be defined or a assert error will come
	for setting in settingsList:
		params["settings"][setting] = "mandatory"

	params["elements"] = {}
	elementsList = getDefaultCineElementsList()

	# init elements
	for element in elementsList:
		params["elements"][element] = {}
		params["elements"][element]["visible"] = True

	# override default True
	params["elements"]["grandparentTitle"]["visible"] = False
	params["elements"]["childCount"]["visible"] = False
	params["elements"]["leafCount"]["visible"] = False
	params["elements"]["unviewedLeafCount"]["visible"] = False
	params["elements"]["viewedLeafCount"]["visible"] = False
	params["elements"]["videoCodec"]["visible"] = False
	params["elements"]["bitrate"]["visible"] = False
	params["elements"]["videoFrameRate"]["visible"] = False
	params["elements"]["audioChannels"]["visible"] = False
	params["elements"]["aspectRatio"]["visible"] = False
	params["elements"]["videoResolution"]["visible"] = False
	params["elements"]["audioCodec"]["visible"] = False
	params["elements"]["file"]["visible"] = False

	# add addional params in elements
	# params["elements"]["backdrop"]["height"]                       = "315"
	# params["elements"]["backdrop"]["width"]                        = "560"
	#params["elements"]["backdrop"]["postfix"]                      = "_backdrop_v2.jpg"

	# params["elements"]["poster"]["height"]                         = "268"
	# params["elements"]["poster"]["width"]                          = "195"
	#params["elements"]["poster"]["postfix"]                        = "_poster_v2.jpg"

	printl("", "DP_ViewFactory::getMovieViewDefaults", "C")
	return params

#===========================================================================
#
#===========================================================================


def getShowViewDefaults():
	printl("", "DP_ViewFactory::getShowViewDefaults", "S")
	params = {}

	params["settings"] = {}
	settingsList = getDefaultSettingsList()
	# mandatory items have to be defined or a assert error will come
	for setting in settingsList:
		params["settings"][setting] = "mandatory"

	params["elements"] = {}
	elementsList = getDefaultCineElementsList()

	# init elements
	for element in elementsList:
		params["elements"][element] = {}
		params["elements"][element]["visible"] = True

	# override default True
	params["elements"]["subtitles"]["visible"] = False
	params["elements"]["audio"]["visible"] = False
	params["elements"]["videoCodec"]["visible"] = False
	params["elements"]["bitrate"]["visible"] = False
	params["elements"]["videoFrameRate"]["visible"] = False
	params["elements"]["audioChannels"]["visible"] = False
	params["elements"]["aspectRatio"]["visible"] = False
	params["elements"]["videoResolution"]["visible"] = False
	params["elements"]["audioCodec"]["visible"] = False
	params["elements"]["file"]["visible"] = False
	params["elements"]["director"]["visible"] = False
	params["elements"]["writer"]["visible"] = False
	params["elements"]["cast"]["visible"] = False
	params["elements"]["codec"]["visible"] = False
	params["elements"]["aspect"]["visible"] = False
	params["elements"]["resolution"]["visible"] = False
	params["elements"]["rated"]["visible"] = False
	params["elements"]["sound"]["visible"] = False
	params["elements"]["soundchannels"]["visible"] = False

	# add addional params in elements
	# params["elements"]["backdrop"]["height"]                       = "315"
	# params["elements"]["backdrop"]["width"]                        = "560"
	#params["elements"]["backdrop"]["postfix"]                      = "_backdrop_v2.jpg"

	# params["elements"]["poster"]["height"]                         = "268"
	# params["elements"]["poster"]["width"]                          = "195"
	#params["elements"]["poster"]["postfix"]                        = "_poster_v2.jpg"

	printl("", "DP_ViewFactory::getShowViewDefaults", "C")
	return params

#===========================================================================
#
#===========================================================================


def getMusicViewDefaults():
	printl("", "DP_ViewFactory::getMusicViewDefaults", "S")
	params = {}

	params["settings"] = {}
	settingsList = getDefaultSettingsList()
	# mandatory items have to be defined or a assert error will come
	for setting in settingsList:
		params["settings"][setting] = "mandatory"

	params["elements"] = {}
	elementsList = getDefaultCineElementsList()

	# init elements
	for element in elementsList:
		params["elements"][element] = {}
		params["elements"][element]["visible"] = True

	# override default True
	params["elements"]["subtitles"]["visible"] = False
	params["elements"]["audio"]["visible"] = False
	params["elements"]["year"]["visible"] = False
	params["elements"]["duration"]["visible"] = False
	params["elements"]["childCount"]["visible"] = False
	params["elements"]["writer"]["visible"] = False
	params["elements"]["director"]["visible"] = False
	params["elements"]["cast"]["visible"] = False
	params["elements"]["leafCount"]["visible"] = False
	params["elements"]["unviewedLeafCount"]["visible"] = False
	params["elements"]["viewedLeafCount"]["visible"] = False
	params["elements"]["videoCodec"]["visible"] = False
	params["elements"]["bitrate"]["visible"] = False
	params["elements"]["videoFrameRate"]["visible"] = False
	params["elements"]["audioChannels"]["visible"] = False
	params["elements"]["aspectRatio"]["visible"] = False
	params["elements"]["videoResolution"]["visible"] = False
	params["elements"]["audioCodec"]["visible"] = False
	params["elements"]["file"]["visible"] = False
	params["elements"]["genre"]["visible"] = False
	params["elements"]["studio"]["visible"] = False

	# add addional params in elements
	# params["elements"]["backdrop"]["height"]                       = "315"
	# params["elements"]["backdrop"]["width"]                        = "560"
	#params["elements"]["backdrop"]["postfix"]                      = "_backdrop_v2.jpg"

	# params["elements"]["poster"]["height"]                         = "268"
	# params["elements"]["poster"]["width"]                          = "195"
	#params["elements"]["poster"]["postfix"]                        = "_poster_v2.jpg"

	printl("", "DP_ViewFactory::getMusicViewDefaults", "C")
	return params

#===========================================================================
#
#===========================================================================


def translateValues(value):
	#printl("", "DP_ViewFactory::translateValues", "S")

	# translate xml value to real true or false
	if value == "true" or value == "True":
		value = True

	if value == "false" or value == "False":
		value = False

	#printl("", "DP_ViewFactory::translateValues", "C")
	return value

#===========================================================================
#
#===========================================================================


def getGuiElements():
	printl("", "DP_ViewFactory::getGuiElements", "S")

	tree = Singleton().getSkinParamsInstance()

	guiElements = {}
	for guiElement in tree.findall('guiElement'):
		name = str(guiElement.get('name'))
		path = str(guiElement.get('path'))
		guiElements[name] = path

	printl("guiElements: " + str(guiElements), "DP_ViewFactory::getGuiElements", "D")
	printl("", "DP_ViewFactory::getGuiElements", "C")
	return guiElements

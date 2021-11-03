# -*- coding: utf-8 -*-
"""
DreamPlex Plugin by DonDavici, 2012

https://github.com/DonDavici/DreamPlex

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
from .__common__ import printl2 as printl

#===============================================================================
# GLOBAL
#===============================================================================
gPlugins = []

#===============================================================================
#
#===============================================================================


def registerPlugin(plugin):
	printl("", "__plugin__::registerPlugin", "S")

	ps = []
	if type(plugin) is list:
		ps = plugin
	else:
		ps.append(plugin)
	for p in ps:
		if p not in gPlugins:
			printl("registered: name=" + str(p.name) + " where=" + str(p.where), "__plugin__::registerPlugin", "D")
			gPlugins.append(p)

	printl("", "__plugin__::registerPlugin", "C")

#===============================================================================
#
#===============================================================================


def getPlugins(where=None):
	printl("", "__plugin__::getPlugins", "S")

	if where is None:
		printl("", "__plugin__::getPlugins", "C")
		return gPlugins
	else:
		plist = []
		for plugin in gPlugins:
			if plugin.where == where:
				plist.append(plugin)

		plist.sort(key=lambda x: x.weight)
		printl(str(plist), "__plugin__::getPlugins", "D")

		printl("", "__plugin__::getPlugins", "C")
		return plist

#===============================================================================
#
#===============================================================================


def getPlugin(pid, where):
	printl("", "__plugin__::getPlugin", "S")

	for plugin in gPlugins:
		if plugin.pid == pid and plugin.where == where:

			printl("plugin found ... " + str(plugin), "__plugin__::getPlugin", "D")
			printl("", "__plugin__::getPlugin", "C")
			return plugin

	printl("", "__plugin__::getPlugin", "C")
	return None

#===============================================================================
#
#===============================================================================


class Plugin(object):
	# constants
	MENU_SERVER = 1
	MENU_MAIN = 2
	MENU_PICTURES = 3
	MENU_MUSIC = 4
	MENU_MOVIES = 5
	MENU_TVSHOWS = 6
	MENU_SYSTEM = 7
	MENU_FILTER = 8
	MENU_CHANNELS = 9
	MENU_MIXED = 10
	MENU_SERVERFILTER = 11

	pid = None
	name = None
	desc = None
	start = None
	fnc = None
	where = None

	#===========================================================================
	#
	#===========================================================================
	def __init__(self, pid, name=None, desc=None, start=None, where=None, fnc=None):
		printl("", self, "S")

		self.pid = pid
		self.name = name
		if desc is None:
			self.desc = self.name
		else:
			self.desc = desc
		self.start = start
		self.fnc = fnc
		self.where = where

		printl("", self, "C")

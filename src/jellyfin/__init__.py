# -*- coding: utf-8 -*-
"""
Presence of this file is what makes DreamPlex's ServiceLoader-style scan
(_discoverServerBackends() in src/__init__.py) treat "jellyfin" as a server
backend to import - importing it is the self-registration step itself.
"""
from .JellyfinSettings import JellyfinSettings, JellyfinSettingsFactory
from .. import registerServerBackend


def _jellyfinLogSanitizer(string: str, steps: list, obfuscate: bool) -> str:
	# Check for X-MediaBrowser-Token in the string
	offset = string.find("X-MediaBrowser-Token")
	if not offset == -1:
		steps[0] = 8
		start = offset + 20
		end = start + steps[0]
		new_string = string[0:start] + "********" + string[end:]
		string = new_string

	# Check for X-Emby-Authorization in the string
	offset = string.find("X-Emby-Authorization")
	if not offset == -1:
		# Find the DeviceId part and obfuscate it
		device_id_offset = string.find("DeviceId=", offset)
		if not device_id_offset == -1:
			steps[0] = 8
			start = device_id_offset + 10
			end = string.find('"', start)
			if end != -1:
				new_string = string[0:start] + "********" + string[end-8:]
				string = new_string

	return string


registerServerBackend(JellyfinSettings, JellyfinSettingsFactory, logSanitizer=_jellyfinLogSanitizer)

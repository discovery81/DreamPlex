# Release notes

🇮🇹 *Queste note sono disponibili anche [in italiano](RELEASENOTES.it.md).*

---

## 3.1.0

### ✨ New

- Jellyfin support: network discovery, authentication (username/password or
  API key), quality profiles, immediate audio/subtitle track override
- Unified XML configuration for all settings and servers, replacing the
  previous three separate storage locations
- Next episode prompt with a configurable countdown, in the style of the
  major streaming apps
- New optional "Carousel" skin (HD and FHD): vertical sidebar menu with
  number-key shortcuts, and a rotating "hero" banner on the server menu -
  poster, plot, a countdown to the next suggestion, playable with OK or the
  blue key

### ⬆️ Upgrading from 3.0

- The existing configuration migrates automatically on first start - servers,
  global settings, Home Users, path mappings; nothing to re-enter
- Installing over the previous version clears the cache and downloaded media
  (posters/backdrops need re-syncing); back up first if in doubt:
  `tar czf /tmp/dreamplex-backup.tar.gz /hdd/dreamplex /etc/enigma2/settings`
- Replaces the official feed's split packages automatically

### 🐛 Fixed

- The plugin failed to start outright, in several different ways depending on
  the image: a self-import loop, two Python 2 leftovers, a crash from logging
  too early, an `UnboundLocalError` in Jellyfin's settings, and a Twisted
  import that collided with enigma2's own reactor
- A newly created server was never actually saved, and cancelling one crashed
  instead of discarding it
- Autoplay skipped the last episode of a list, and never started with only
  two episodes
- The plugin wouldn't compile at all due to a stray indentation error
- Assorted `NameError`/`ModuleNotFoundError` crashes from Python 2 leftovers
- A server could be saved unintentionally right after a successful remote
  login, even when dismissing the following confirmation with Cancel/Exit
  instead of actually confirming
- The remote's STOP key (closes the plugin), and the server menu's
  sync/cache and switch-user buttons, worked but were never shown on screen
  or in the Help legend - in some skins the switch-user button was missing
  entirely
- Changing the skin used to require a full GUI restart; now leaving and
  re-entering the plugin is enough, with an on-screen reminder after saving
- Jellyfin poster/backdrop images could silently fail to download for
  content never cached before
- Switching skins from Settings only ever offered "default" - every other
  installed skin was silently ignored

### 🔒 Security

- Certificate verification restored for the plex.tv connections
- Backdrop rendering no longer runs through a shell
- Cache files are rejected unless written by the plugin itself

### ⚡ Responsiveness

- Jellyfin and Plex discovery no longer freeze the box while scanning the
  network
- The Wake on Lan wait no longer blocks the interface

### 🔧 Under the hood

- Python compatibility from 3.8 to 3.14
- Packaging fixes: missing subpackages, trimmed dependencies, no more stale
  bytecode shipped or left behind by upgrades
- Bare `except:` clauses replaced throughout
- Added static analysis config and a few regression-test scripts
- A handful of dead, unimplemented remote-control key handlers removed

### 🌍 Translations

- Jellyfin strings are now extracted and translatable
- Catalogue grows to 539 strings; Italian is complete

---

## 1.06
- fixed #56: theme stops playing on leave

## 1.05
- fixed direct play location check for windows server
- added some code to prevent misconfiguration in direct play ( slashes and backslashes)
- fixed order (plex defaults are untouched now :-)
- fixed newest and recently added in tv shows
- fixed gs when option live tv is enabled
- fixed streamed mode (buffer drained)
- fixed update function
- fixed media selection if more than one version is available
- fixed yellow button toggle name direct local mode
- added font details to xml for skinners
- several clean ups

## 1.04a (bugfix release)
- fixed gs in tvshow section

## 1.04
- fixed direct local with UNC path
- fixed direct local for plex on windows
- new choicebox if there is more than one version of the media in plex
- new function show location of file => menu key
- new views (long list and backdroplist) thx to tobi79ac for skinning :-) => blue key
- complete new mapping handler for direct local
- new show seen/unseen count for tvshows
- several bugfixes
- new update location => bintray

## 1.03
- UI tweaks
- added Help
- added About
- fixed when live tv stop is disabled

## 1.02
- added update function
- fixed naviagtion in tvshows
- removed buffer settings (didnt work)
- fixed quality issue playback mode "transcoded"
- options show up only when needed according to other options
- direct local mode is now also available for plex on windows
- added logrotator to have log even after greenscreen
- several bugfixes and tweaks

## 1.01
- added fastScroll feature
- fixed onDeck and recentlyViewed in TvShows
- added option: stop live tv on startup
- added option: summerize Sections
- impletmented media menu
- new feature media menu => mark as watched, unwachted and refresh library section
- small skin tweaks
- little bugfixes

## 1.00
- new hd skin (big thx to IPMAN)
- removed sd and xd skin for now
- tons of bugfixes
- another tons of bugfixes

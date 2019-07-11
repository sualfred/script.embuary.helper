#!/usr/bin/python
# coding: utf-8

########################

import xbmc
import xbmcgui
import random

from resources.lib.utils import split
from resources.lib.helper import *
from resources.lib.image import *
from resources.lib.kodi_monitor import KodiMonitor

########################

MONITOR = KodiMonitor()
KODIVERSION = get_kodiversion()

########################

log('Service started', force=True)

widget_refresh = 0
get_backgrounds = 200
set_background = 10
master_lock = None
has_reloaded = False

while not MONITOR.abortRequested():

	# Blur listitem fanart
	if visible('Skin.HasSetting(BlurEnabled)'):
		image_filter()

	# Focus monitor to split merged info labels by the default / seperator to properties
	if visible('Skin.HasSetting(FocusMonitor) + Window.IsMedia'):
		split({'value': xbmc.getInfoLabel('ListItem.Genre'), 'property': 'ListItem.Genre', 'separator': ' / '})
		split({'value': xbmc.getInfoLabel('ListItem.Country'), 'property': 'ListItem.Country', 'separator': ' / '})
		split({'value': xbmc.getInfoLabel('ListItem.Studio'), 'property': 'ListItem.Studio', 'separator': ' / '})
		split({'value': xbmc.getInfoLabel('ListItem.Director'), 'property': 'ListItem.Director', 'separator': ' / '})

	# Workaround for login screen bug
	if not has_reloaded:
		if visible('System.HasLoginScreen + Skin.HasSetting(ReloadOnLogin)'):
			log('System has login screen enabled. Reload the skin to load all strings correctly.')
			execute('ReloadSkin()')
			has_reloaded = True

	# Master lock reload logic for widgets
	if visible('System.HasLocks'):
		if master_lock is None:
			master_lock = True if visible('System.IsMaster') else False
			log('Master mode: %s' % master_lock)

		if master_lock == True and not visible('System.IsMaster'):
			log('Left master mode. Reload skin.')
			master_lock = False
			execute('ReloadSkin()')

		elif master_lock == False and visible('System.IsMaster'):
			log('Entered master mode. Reload skin.')
			master_lock = True
			execute('ReloadSkin()')

	elif master_lock is not None:
		master_lock = None

	# Grab fanarts
	if get_backgrounds >= 200:
		log('Start new fanart grabber process')
		fanarts = grabfanart()
		get_backgrounds = 0

	else:
		get_backgrounds += 1

	# Set fanart property
	if set_background >=10 and fanarts:
		winprop('EmbuaryBackground', random.choice(fanarts))
		set_background = 0

	else:
		set_background += 1

	# Refresh widgets
	if widget_refresh >= 600:
		reload_widgets(instant=True)
		widget_refresh = 0

	else:
		widget_refresh += 1

	MONITOR.waitForAbort(1)

del MONITOR

log('Service stopped', force=True)
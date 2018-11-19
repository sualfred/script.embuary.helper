#!/usr/bin/python

from resources.lib.utils import log, grabfanart, ADDON_ID
from resources.lib.kodi_monitor import KodiMonitor
import xbmc
import xbmcgui
import xbmcaddon
import time
import random

WIN = xbmcgui.Window(10000)
ADDON = xbmcaddon.Addon(ADDON_ID)
MONITOR = KodiMonitor(win=WIN, addon=ADDON)

task_interval = 300
cache_interval = 150
bg_task_interval = 200
bg_interval = 10

log('Service started')

while not MONITOR.abortRequested():

	# Grab fanarts
	if bg_task_interval >= 200:
		log("Start new fanart grabber process")
		fanarts = grabfanart()
		bg_task_interval = 0
	else:
		bg_task_interval += 10

	# Set fanart property
	if fanarts and bg_interval >=10:
		random.shuffle(fanarts)
		WIN.setProperty("EmbuaryBackground", fanarts[0])
		bg_interval = 0
	else:
		bg_interval += 10

	# Refresh widgets
	if task_interval >= 300:
		log("Update widget reload property")
		WIN.setProperty("EmbuaryWidgetUpdate", time.strftime("%Y%m%d%H%M%S", time.gmtime()))
		task_interval = 0
	else:
		task_interval += 10

	# Refresh cache
	if cache_interval >= 150:
		log("Update cache reload property")
		WIN.setProperty("EmbuaryCacheTime", time.strftime("%Y%m%d%H%M%S", time.gmtime()))
		cache_interval = 0
	else:
		cache_interval += 10

	MONITOR.waitForAbort(10)

del MONITOR
del WIN
del ADDON
log('Service stopped')
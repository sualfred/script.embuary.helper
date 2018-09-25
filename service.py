#!/usr/bin/python

from resources.lib.utils import log, ADDON_ID
from resources.lib.kodi_monitor import KodiMonitor
import xbmc
import xbmcgui
import xbmcaddon
import time

TASK_INTERVAL = 520
WIN = xbmcgui.Window(10000)
ADDON = xbmcaddon.Addon(ADDON_ID)
MONITOR = KodiMonitor(win=WIN, addon=ADDON)
log('Service started')

while not MONITOR.abortRequested():

    if TASK_INTERVAL >= 300:
        log("Update widget reload property")
        WIN.setProperty("EmbuaryWidgetUpdate", time.strftime("%Y%m%d%H%M%S", time.gmtime()))
        TASK_INTERVAL = 0
    else:
        TASK_INTERVAL += 10

    MONITOR.waitForAbort(10)

del MONITOR
del WIN
del ADDON
log('Service stopped')
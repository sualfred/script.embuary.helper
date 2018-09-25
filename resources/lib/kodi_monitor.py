#!/usr/bin/python

from resources.lib.utils import log
import xbmc
import time

class KodiMonitor(xbmc.Monitor):
    update_widgets_busy = False
    last_mediatype = ""

    def __init__(self, **kwargs):
        xbmc.Monitor.__init__(self)
        self.win = kwargs.get("win")
        self.addon = kwargs.get("addon")

    def onDatabaseUpdated(self, database):
        log("Kodi_Monitor: %s database updated" % database)
        self.refresh_widgets()

    def onNotification(self, sender, method, data):
        try:
            if method == "VideoLibrary.OnUpdate" or method == "AudioLibrary.OnUpdate" or method == "Player.OnStop" or method == "Player.OnPlay":
                log("Kodi_Monitor: sender %s - method: %s  - data: %s" % (sender, method, data))
                self.refresh_widgets()

        except Exception as exc:
            log("Exception in KodiMonitor: %s" % exc)

    def refresh_widgets(self):
        log("Refreshing widgets")
        timestr = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        self.win.setProperty("EmbuaryWidgetUpdate", timestr)
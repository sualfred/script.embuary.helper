#!/usr/bin/python

from resources.lib.utils import log
import xbmc
import time

class KodiMonitor(xbmc.Monitor):

    def __init__(self, **kwargs):
        xbmc.Monitor.__init__(self)
        self.win = kwargs.get("win")
        self.addon = kwargs.get("addon")

    def onDatabaseUpdated(self, database):
        log("Kodi_Monitor: %s database updated" % database)
        self.refresh_widgets()

    def onNotification(self, sender, method, data):

        #log("Kodi_Monitor: sender %s - method: %s  - data: %s" % (sender, method, data))

        if method == "Player.OnPlay":
            xbmc.sleep(6000)
            self.refresh_widgets()

        if method == "Player.OnStop":
            self.refresh_widgets()

            # let's wait for the player so we don't clear it by mistake
            xbmc.sleep(1000)
            if xbmc.getCondVisibility("Skin.HasSetting(EmbuaryHelperClearPlaylist) + !Player.HasMedia + !Window.IsVisible(busydialog)"):
                xbmc.executebuiltin("Playlist.Clear")
                log("Playlist cleared")

        if method == "VideoLibrary.OnUpdate" or method == "AudioLibrary.OnUpdate":
            self.refresh_widgets()

    def refresh_widgets(self):
        log("Refreshing widgets")
        timestr = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        self.win.setProperty("EmbuaryWidgetUpdate", timestr)
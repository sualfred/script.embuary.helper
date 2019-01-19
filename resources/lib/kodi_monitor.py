#!/usr/bin/python

from resources.lib.utils import log
import xbmc
import time

class KodiMonitor(xbmc.Monitor):

    def __init__(self, **kwargs):
        xbmc.Monitor.__init__(self)
        self.win = kwargs.get("win")
        self.addon = kwargs.get("addon")

    '''
    def onScanStarted(self, library):
        log("Kodi_Monitor: %s scan started" % library)

    def onScanFinished(self, library):
        log("Kodi_Monitor: %s scan finished" % library)
        self.refresh_widgets()
    '''

    def onNotification(self, sender, method, data):

        if method == "Player.OnStop" or method == "VideoLibrary.OnUpdate" or method == "AudioLibrary.OnUpdate":
            log("Kodi_Monitor: sender %s - method: %s  - data: %s" % (sender, method, data))
            self.refresh_widgets()

        if method == "Player.OnStop":
            self.clear_playlist()

    def refresh_widgets(self):
        log("Refreshing widgets")
        timestr = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        xbmc.executebuiltin("AlarmClock(WidgetRefresh,SetProperty(EmbuaryWidgetUpdate,%s,home),00:04,silent)" % timestr)
        #self.win.setProperty("EmbuaryWidgetUpdate", timestr)

    def clear_playlist(self):
        xbmc.sleep(3000) # let's wait for the player so we don't clear it by mistake
        if xbmc.getCondVisibility("Skin.HasSetting(EmbuaryHelperClearPlaylist) + !Player.HasMedia + !Window.IsVisible(busydialog)"):
            xbmc.executebuiltin("Playlist.Clear")
            log("Playlist cleared")
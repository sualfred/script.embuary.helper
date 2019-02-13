#!/usr/bin/python

from resources.lib.utils import log
import xbmc
import xbmcgui
import time

class KodiMonitor(xbmc.Monitor):

    def __init__(self, **kwargs):
        xbmc.Monitor.__init__(self)
        self.win = kwargs.get("win")
        self.addon = kwargs.get("addon")
        self.player = kwargs.get("player")
        self.do_fullscreen_lock = False

    def onNotification(self, sender, method, data):

        if method in ["Player.OnPlay", "Player.OnStop", "Player.OnAVChange"]:
            log("Kodi_Monitor: sender %s - method: %s  - data: %s" % (sender, method, data))

        if method == "Player.OnPlay":
            self.do_fullscreen()

        if method == "Player.OnStop" or method == "VideoLibrary.OnUpdate" or method == "AudioLibrary.OnUpdate":
            self.refresh_widgets()

        if method == "Player.OnAVChange":
            self.get_audiotracks()

        if method == "Player.OnStop":
            xbmc.sleep(3000)
            if not self.player.isPlaying():
                self.clear_playlist()
                self.do_fullscreen_lock = False

    def refresh_widgets(self):

        log("Refreshing widgets")
        timestr = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        xbmc.executebuiltin("AlarmClock(WidgetRefresh,SetProperty(EmbuaryWidgetUpdate,%s,home),00:04,silent)" % timestr)

    def clear_playlist(self):

        if xbmc.getCondVisibility("Skin.HasSetting(EmbuaryHelperClearPlaylist)") and not self.player.isPlaying() and xbmcgui.getCurrentWindowId() not in [12005, 12006, 10028, 10500, 10138]:
            xbmc.executebuiltin("Playlist.Clear")
            log("Playlist cleared")

    def get_audiotracks(self):

        xbmc.sleep(100)
        self.win.clearProperty("EmbuaryPlayerAudioTracks")
        audiotracks = self.player.getAvailableAudioStreams()
        if len(audiotracks) > 1:
            self.win.setProperty("EmbuaryPlayerAudioTracks", "true")

    def do_fullscreen(self):

        xbmc.sleep(1000)
        if not self.do_fullscreen_lock and xbmc.getCondVisibility("Skin.HasSetting(StartPlayerFullscreen)") and self.player.isPlaying() and xbmcgui.getCurrentWindowId() not in [12005, 12006, 10028, 10500]:
            for i in range(1,200):
                if not xbmcgui.getCurrentWindowId() == 10138:
                    xbmc.executebuiltin("Dialog.Close(all,true)")
                    xbmc.executebuiltin("action(fullscreen)")
                    self.do_fullscreen_lock = True
                    break
                else:
                    xbmc.sleep(50)
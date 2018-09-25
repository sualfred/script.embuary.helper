#!/usr/bin/python
import sys
import xbmc
import xbmcgui
import xbmcaddon
import urlparse

from resources.lib.plugin_content import *
from resources.lib.utils import remove_quotes
from resources.lib.utils import log
from resources.lib.utils import smsjump

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_LANGUAGE = ADDON.getLocalizedString
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
WINDOW = xbmcgui.Window(10000)

class Main:

    def __init__(self):
        log("version %s started" % ADDON_VERSION)
        self._parse_argv()
        self.info = self.params.get("info")
        if self.info:
            self.info_actions()

    def _parse_argv(self):
        base_url = sys.argv[0]
        path = sys.argv[2]
        try:
            self.params = dict(urlparse.parse_qsl(path[1:]))
        except Exception:
            self.params = {}

    def info_actions(self):
        li = list()
        dbid = remove_quotes(self.params.get("dbid"))
        dbtype = remove_quotes(self.params.get("type"))
        dbtitle = remove_quotes(self.params.get("title"))
        action = remove_quotes(self.params.get("action"))
        plugin = PluginContent(dbtype,dbid,dbtitle,li)

        if self.info == 'getcast':
            plugin.get_cast()
        elif self.info == 'getsimilar':
            plugin.get_similar()
        elif self.info == 'getgenre':
            plugin.get_genre()
        elif self.info == 'getinprogress':
            plugin.get_inprogress()
        elif self.info == 'jumptoletter':
            if action:
                smsjump(action)
            else:
                plugin.jumptoletter()

        xbmcplugin.addDirectoryItems(int(sys.argv[1]), li)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

if __name__ == "__main__":
    Main()
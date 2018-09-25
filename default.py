import sys
import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.utils import *

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_LANGUAGE = ADDON.getLocalizedString
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
window = xbmcgui.Window(10000)

class Main:

    def __init__(self):
        log("version %s started" % ADDON_VERSION)
        self._parse_argv()
        if self.infos:
            self.info_actions(self.infos, self.params)

    def _parse_argv(self):
        args = sys.argv
        self.infos = []
        for arg in args:
            if arg == 'script.embuary.helper':
                continue
            if arg.startswith('info='):
                self.infos.append(arg[5:])
            else:
                try:
                    self.params[arg.split("=")[0].lower()] = "=".join(arg.split("=")[1:]).strip()
                    log("params %s" % self.params)
                except:
                    self.params = {}
                    pass

    def info_actions(self,infos,params):
        prettyprint(params)
        prettyprint(infos)

        action = self.params.get("action")

        for info in self.infos:
            if info == 'smsjump':
                smsjump(action)

if __name__ == "__main__":
    Main()

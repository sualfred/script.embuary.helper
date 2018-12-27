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
        self._parse_argv()
        if self.action:
            self.getactions()
        else:
            xbmcgui.Dialog().ok("Error", "This is a tool to provide features to a skin and requires skin integration.")

    def _parse_argv(self):
        args = sys.argv
        self.action = []
        for arg in args:
            if arg == 'script.embuary.helper':
                continue
            if arg.startswith('action='):
                self.action.append(arg[7:])
            else:
                try:
                    self.params[arg.split("=")[0].lower()] = "=".join(arg.split("=")[1:]).strip()
                except:
                    self.params = {}
                    pass

    def getactions(self):
        for action in self.action:
            if action == 'playfromhome':
                playfromhome(self.params)
            elif action == 'goto':
                goto(self.params)
            elif action == 'textviewer':
                textviewer(self.params)
            elif action == 'dialogok':
                dialogok(self.params)
            elif action == 'dialogyesno':
                dialogyesno(self.params)
            elif action == 'setkodisetting':
                setkodisetting(self.params)
            elif action == 'togglekodisetting':
                togglekodisetting(self.params)
            elif action == 'createselect':
                selectdialog(self.params)
            elif action == 'jumptoshow_by_episode':
                jumptoshow_by_episode(self.params)
            elif action == 'details_by_season':
                tvshow_details_by_season(self.params)

if __name__ == "__main__":
    Main()

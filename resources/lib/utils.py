import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmcvfs
import os
import sys
import simplejson
import hashlib
import urllib
import random

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
window = xbmcgui.Window(10000)

def remove_quotes(label):
    if not label:
        return ""
    if label.startswith("'") and label.endswith("'") and len(label) > 2:
        label = label[1:-1]
        if label.startswith('"') and label.endswith('"') and len(label) > 2:
            label = label[1:-1]
    return label

def play_from_home(item):
    item = remove_quotes(item)
    item = "PlayMedia(%s)" % item
    for i in range(50):
        if not xbmc.getCondVisibility("Window.IsVisible(home)"):
            xbmc.executebuiltin("Dialog.Close(all,true)")
            xbmc.executebuiltin("ActivateWindow(home)")
            xbmc.sleep(50)
        elif xbmc.getCondVisibility("Window.IsVisible(home)"):
            xbmc.executebuiltin(item)
            break


def jumptoshow(params):
    try:
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
    except Exception:
        pass
    finally:
        window.setProperty("TVShowRating",params.get("rating"))
        window.setProperty("TVShowDBID",params.get("dbid"))
        window.setProperty("TVShowYear",params.get("year"))
        window.setProperty("TVShowTotalSeasons",params.get("seasons"))
        window.setProperty("TVShowTotalEpisodes",params.get("episodes"))

        if not xbmc.getCondVisibility("Window.IsMedia"):
            execute = "ActivateWindow(videos,videodb://tvshows/titles/%s/,return)" % params.get("dbid")
        else:
            execute = "Container.Update(videodb://tvshows/titles/%s/)" % params.get("dbid")

        xbmc.executebuiltin("Dialog.Close(all,true)")
        xbmc.executebuiltin(execute)


def smsjump(letter):
    try:
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
    except Exception:
        pass
    finally:
        jumpcmd = ""
        if letter:
            letter = letter.upper()
        if letter == "0":
                if xbmc.getInfoLabel("Container.SortOrder") == "Descending":
                    jumpcmd = "lastpage"
                else:
                    jumpcmd = "firstpage"
        elif letter in ["A", "B", "C"]:
            jumpcmd = "jumpsms2"
        elif letter in ["D", "E", "F"]:
            jumpcmd = "jumpsms3"
        elif letter in ["G", "H", "I"]:
            jumpcmd = "jumpsms4"
        elif letter in ["J", "K", "L"]:
            jumpcmd = "jumpsms5"
        elif letter in ["M", "N", "O"]:
            jumpcmd = "jumpsms6"
        elif letter in ["P", "Q", "R", "S"]:
            jumpcmd = "jumpsms7"
        elif letter in ["T", "U", "V"]:
            jumpcmd = "jumpsms8"
        elif letter in ["W", "X", "Y", "Z"]:
            jumpcmd = "jumpsms9"
        if jumpcmd:
            xbmc.executebuiltin("SetFocus(50)")
            for i in range(40):
                xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Input.ExecuteAction",\
                    "params": { "action": "%s" }, "id": 1 }' % (jumpcmd))
                xbmc.sleep(50)
                if xbmc.getInfoLabel("ListItem.Sortletter").upper() == letter or letter == "0":
                    break

def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDON_ID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGNOTICE )

def prettyprint(string):
    log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))
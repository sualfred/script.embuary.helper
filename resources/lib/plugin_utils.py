import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmcvfs
import os
import sys
from resources.lib.library import *
from resources.lib.utils import *

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
window = xbmcgui.Window(10000)

def jumptoseason(params):
    try:
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
    except Exception:
        pass
    finally:
        path = "videodb://tvshows/titles/%s/%s/" % (params.get("dbid"),params.get("season"))
        gotopath(path)

def jumptoshow(params):
    try:
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
    except Exception:
        pass

    path = "videodb://tvshows/titles/%s/" % params.get("dbid")
    gotopath(path)

def smsjump(params):
    letter = params.get("letter")
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

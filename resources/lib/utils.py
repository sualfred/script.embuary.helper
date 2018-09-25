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

def smsjump(action):
    try:
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
    except Exception:
        pass
    finally:
        jumpcmd = ""
        if action:
            action = action.upper()
        if action == "0":
                if xbmc.getInfoLabel("Container.SortOrder") == "Descending":
                    jumpcmd = "lastpage"
                else:
                    jumpcmd = "firstpage"
        elif action in ["A", "B", "C"]:
            jumpcmd = "jumpsms2"
        elif action in ["D", "E", "F"]:
            jumpcmd = "jumpsms3"
        elif action in ["G", "H", "I"]:
            jumpcmd = "jumpsms4"
        elif action in ["J", "K", "L"]:
            jumpcmd = "jumpsms5"
        elif action in ["M", "N", "O"]:
            jumpcmd = "jumpsms6"
        elif action in ["P", "Q", "R", "S"]:
            jumpcmd = "jumpsms7"
        elif action in ["T", "U", "V"]:
            jumpcmd = "jumpsms8"
        elif action in ["W", "X", "Y", "Z"]:
            jumpcmd = "jumpsms9"
        if jumpcmd:
            xbmc.executebuiltin("SetFocus(50)")
            for i in range(40):
                xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Input.ExecuteAction",\
                    "params": { "action": "%s" }, "id": 1 }' % (jumpcmd))
                xbmc.sleep(50)
                if xbmc.getInfoLabel("ListItem.Sortletter").upper() == action or action == "0":
                    break

def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDON_ID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGNOTICE )

def prettyprint(string):
    log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))
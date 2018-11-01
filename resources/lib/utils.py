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
from resources.lib.library import *

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

def create_select_dialog(params):
    selectionlist = []
    indexlist = []
    headertxt = remove_quotes(params.get("header", ""))
    for i in range(1, 30):
        label = xbmc.getInfoLabel("Window.Property(Dialog.%i.Label)" % (i))
        if label == "":
            break
        elif label != "none" and label != "-":
            selectionlist.append(label)
            indexlist.append(i)
    if selectionlist:
        select_dialog = xbmcgui.Dialog()
        index = select_dialog.select(headertxt, selectionlist)
        if index > -1:
            value = xbmc.getInfoLabel("Window.Property(Dialog.%i.Builtin)" % (indexlist[index]))
            for builtin in value.split("||"):
                xbmc.executebuiltin(builtin)
                xbmc.sleep(30)
    for i in range(1, 30):
        xbmc.executebuiltin("ClearProperty(Dialog.%i.Builtin)" % (i))
        xbmc.executebuiltin("ClearProperty(Dialog.%i.Label)" % (i))

def dialogok(params):
    headertxt = remove_quotes(params.get("header", ""))
    bodytxt = remove_quotes(params.get("message", ""))
    dialog = xbmcgui.Dialog()
    dialog.ok(heading=headertxt, line1=bodytxt)
    del dialog

def dialogyesno(params):
    headertxt = remove_quotes(params.get("header", ""))
    bodytxt = remove_quotes(params.get("message", ""))
    yesactions = params.get("yesaction", "").split("|")
    noactions = params.get("noaction", "").split("|")
    if xbmcgui.Dialog().yesno(heading=headertxt, line1=bodytxt):
        for action in yesactions:
            xbmc.executebuiltin(action.encode("utf-8"))
    else:
        for action in noactions:
            xbmc.executebuiltin(action.encode("utf-8"))

def textviewer(params):
    headertxt = remove_quotes(params.get("header", ""))
    bodytxt = remove_quotes(params.get("message", ""))
    xbmcgui.Dialog().textviewer(headertxt, bodytxt)

def togglekodisetting(params):
    settingname = params.get("setting", "")
    cur_value = xbmc.getCondVisibility("system.getbool(%s)" % settingname)
    if cur_value:
        value = "false"
    else:
        value = "true"
    xbmc.executeJSONRPC(
        '{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}}' %
        (settingname, value))

def setkodisetting(params):
    settingname = params.get("setting", "")
    value = params.get("value", "")
    try:
        value = int(value)
    except Exception:
        if value.lower() in ["true", "false"]:
            value = value.lower()
        else:
            log("SetKodiSetting: No valid value")
            return
    xbmc.executeJSONRPC(
        '{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}}' %
        (settingname, value))

def close_and_open(params):
    window.setProperty("TVShowRating",params.get("rating"))
    window.setProperty("TVShowDBID",params.get("dbid"))
    window.setProperty("TVShowYear",params.get("year"))
    window.setProperty("TVShowTotalSeasons",params.get("seasons"))
    window.setProperty("TVShowTotalEpisodes",params.get("episodes"))
    window.setProperty("EmbyID",params.get("embyid"))

    xbmc.executebuiltin("Dialog.Close(all,true)")
    xbmc.sleep(50)

    path = remove_quotes(params.get("path"))
    target = params.get("target")

    if xbmc.getCondVisibility("Window.IsMedia"):
        execute = "Container.Update(%s)" % path
    else:
        execute = "ActivateWindow(%s,%s,return)" % (target,path)

    xbmc.executebuiltin(execute)

def play_from_home(item):
    for i in range(50):
        if xbmc.getCondVisibility("!Window.IsVisible(home) | Window.IsVisible(movieinformation)"):
            xbmc.executebuiltin("Dialog.Close(all,true)")
            xbmc.executebuiltin("ActivateWindow(home)")
            xbmc.sleep(50)
        else:
            ishome = True
            break

    if ishome:
        item = remove_quotes(item)
        item = "PlayMedia(%s)" % item
        xbmc.executebuiltin(item)

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

def jumptoseason(params):
    try:
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
    except Exception:
        pass
    finally:
        if not xbmc.getCondVisibility("Window.IsMedia"):
            execute = "ActivateWindow(videos,videodb://tvshows/titles/%s/%s/,return)" % (params.get("dbid"),params.get("season"))
        else:
            execute = "Container.Update(videodb://tvshows/titles/%s/%s/)" % (params.get("dbid"),params.get("season"))

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

def grabfanart():
    fanarts = list()

    movie_query = json_call("VideoLibrary.GetMovies",
                        properties=['art'],
                        sort={"method": "random"}, limit=20
                        )

    try:
        for art in movie_query["result"]['movies']:
                movie_fanart = art["art"].get("fanart", "")
                fanarts.append(movie_fanart)
    except Exception:
        log("Backgrounds: No movie artworks found.")

    tvshow_query = json_call("VideoLibrary.GetTVShows",
                        properties=['art'],
                        sort={"method": "random"}, limit=20
                        )

    try:
        for art in tvshow_query["result"]['tvshows']:
                tvshow_fanart = art["art"].get("fanart", "")
                fanarts.append(tvshow_fanart)
    except Exception:
        log("Backgrounds: No TV show artworks found.")

    return fanarts

def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDON_ID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGNOTICE )

def prettyprint(string):
    log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))
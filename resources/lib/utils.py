import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmcvfs
import os
import sys
import simplejson
from resources.lib.library import *
from resources.lib.json_map import *
from library import json_call

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
WIN = xbmcgui.Window(10000)
PLAYER = xbmc.Player()
VIDEOPLAYLIST = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
MUSICPLAYLIST = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)

def remove_quotes(label):
    if not label:
        return ""
    if label.startswith("'") and label.endswith("'") and len(label) > 2:
        label = label[1:-1]
        if label.startswith('"') and label.endswith('"') and len(label) > 2:
            label = label[1:-1]
    return label

def selectdialog(params):
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

def toggleaddons(params):
    addonid = params.get("addonid").split("+")
    enable = params.get("enable")
    for addon in addonid:
        try:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "id":1, "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled": %s}}' % (addon, enable))
            log("%s - enable: %s" % (addon, enable))
        except Exception:
            pass

def playsfx(params):
    path = remove_quotes(params.get("path", ""))
    xbmc.playSFX(path)

def playitem(params):
    VIDEOPLAYLIST.clear()
    xbmc.executebuiltin("Dialog.Close(all,true)")

    dbid = params.get("dbid")
    dbtype = "movieid" if not params.get("dbtype") == "episode" else "episodeid"

    if dbid:
        json_call("Player.Open",
                    item={dbtype: int(dbid)}
                    )
    else:
        xbmc.executebuiltin("PlayMedia(%s)" % remove_quotes(params.get("item")))

def playall(params):
    VIDEOPLAYLIST.clear()

    if params.get("method") == "fromhere":
        method = "Container(%s).ListItemNoWrap" % params.get("id")
    else:
        method = "Container(%s).ListItemAbsolute" % params.get("id")

    for i in range(int(xbmc.getInfoLabel("Container.NumItems"))):

        if xbmc.getCondVisibility("String.IsEqual(%s(%s).DBType,movie)" % (method,i)):
            media_type = "movie"
        elif xbmc.getCondVisibility("String.IsEqual(%s(%s).DBType,episode)" % (method,i)):
            media_type = "episode"
        else:
            media_type = None

        dbid = xbmc.getInfoLabel("%s(%s).DBID" % (method,i))
        url = xbmc.getInfoLabel("%s(%s).Filenameandpath" % (method,i))

        if media_type and dbid:
            json_call("Playlist.Add",
                        item={"%sid" % media_type: int(dbid)},
                        params={"playlistid": 1}
                        )

        elif url:
            json_call("Playlist.Add",
                        item={"file": url},
                        params={"playlistid": 1}
                        )

    PLAYER.play(VIDEOPLAYLIST, startpos=0, windowed=False)

def playrandom(params):
    VIDEOPLAYLIST.clear()

    i = random.randint(1,int(xbmc.getInfoLabel("Container.NumItems")))

    if xbmc.getCondVisibility("String.IsEqual(Container(%s).ListItemAbsolute(%s).DBType,movie)" % (params.get("id"),i)):
        media_type = "movie"
    elif xbmc.getCondVisibility("String.IsEqual(Container(%s).ListItemAbsolute(%s).DBType,episode)" % (params.get("id"),i)):
        media_type = "episode"
    else:
        media_type = None

    dbid = xbmc.getInfoLabel("Container(%s).ListItemAbsolute(%s).DBID" % (params.get("id"),i))
    url = xbmc.getInfoLabel("Container(%s).ListItemAbsolute(%s).Filenameandpath" % (params.get("id"),i))

    playitem({"dbtype": media_type, "dbid": dbid, "item": url})

def jumptoshow_by_episode(params):
    episode_query = json_call("VideoLibrary.GetEpisodeDetails",
                    properties=["tvshowid"],
                    params={"episodeid": int(params.get("dbid"))}
                    )
    try:
        tvshow_id = str(episode_query["result"]["episodedetails"]["tvshowid"])
    except Exception:
        log("Could not get the TV show ID")
        return

    path = "videodb://tvshows/titles/%s/" % tvshow_id
    gotopath(path)

def goto(params):
    path = remove_quotes(params.get("path"))
    target = params.get("target")
    gotopath(path,target)

def gotopath(path,target="videos"):
    if not xbmc.getCondVisibility("Window.IsMedia"):
        execute = "ActivateWindow(%s,%s,return)" % (target,path)
    else:
        execute = "Container.Update(%s)" % path

    xbmc.executebuiltin("Dialog.Close(all,true)")
    xbmc.executebuiltin(execute)

def resetposition(params):
    containers = params.get("container").split("||")
    for item in containers:
        try:
            current_item = "Container(%s).CurrentItem" % item
            current_item = xbmc.getInfoLabel(current_item)
            current_item = int(current_item) - 1
            execute = "Control.Move(%s,-%s)" % (item,str(current_item))
            xbmc.executebuiltin(execute)
        except Exception:
            pass

def tvshow_details_by_season(params):
    season_query = json_call("VideoLibrary.GetSeasonDetails",
                        properties=["tvshowid"],
                        params={"seasonid": int(params.get("dbid"))}
                        )
    try:
        tvshow_id = str(season_query["result"]["seasondetails"]["tvshowid"])
    except Exception:
        log("Show details by season: Could not get TV show ID")
        return

    tvshow_query = json_call("VideoLibrary.GetTVShowDetails",
                        properties=tvshow_properties,
                        params={"tvshowid": int(tvshow_id)}
                        )

    try:
        details = tvshow_query["result"]["tvshowdetails"]
    except Exception:
        log("Show details by season: Could not get TV show details")
        return

    if int(details["episode"]) > int(details["watchedepisodes"]):
        unwatchedepisodes = int(details["episode"]) - int(details["watchedepisodes"])
        unwatchedepisodes = str(unwatchedepisodes)
    else:
        unwatchedepisodes = "0"

    WIN.setProperty("tvshow.dbid", str(details["tvshowid"]))
    WIN.setProperty("tvshow.rating", str(round(details['rating'],1)))
    WIN.setProperty("tvshow.seasons", str(details["season"]))
    WIN.setProperty("tvshow.episodes", str(details["episode"]))
    WIN.setProperty("tvshow.watchedepisodes", str(details["watchedepisodes"]))
    WIN.setProperty("tvshow.unwatchedepisodes", unwatchedepisodes)

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
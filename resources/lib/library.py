#!/usr/bin/python

import xbmc
import xbmcgui
import xbmcaddon
import json as simplejson
from time import gmtime, strftime
#from resources.lib.utils import log

movie_properties = [
                        "title",
                        "originaltitle",
                        "votes",
                        "playcount",
                        "year",
                        "genre",
                        "studio",
                        "country",
                        "tagline",
                        "plot",
                        "runtime",
                        "file",
                        "plotoutline",
                        "lastplayed",
                        "trailer",
                        "rating",
                        "resume",
                        "art",
                        "streamdetails",
                        "mpaa",
                        "director",
                        "writer",
                        "cast",
                        "dateadded",
                        "imdbnumber"]
episode_properties = [
                        "title",
                        "playcount",
                        "season",
                        "episode",
                        "showtitle",
                        "plot",
                        "file",
                        "rating",
                        "resume",
                        "tvshowid",
                        "firstaired",
                        "art",
                        "streamdetails",
                        "runtime",
                        "director",
                        "writer",
                        "cast",
                        "dateadded",
                        "lastplayed"]
season_properties = [
                        "season",
                        "episode",
                        "art",
                        "watchedepisodes",
                        "showtitle",
                        "playcount",
                        "tvshowid"]
tvshow_properties = [
                        "title",
                        "studio",
                        "year",
                        "plot",
                        "cast",
                        "rating",
                        "votes",
                        "genre",
                        "episode",
                        "season",
                        "mpaa",
                        "premiered",
                        "playcount",
                        "art",
                        "dateadded",
                        "watchedepisodes",
                        "imdbnumber"]
music_properties = [
                        "title",
                        "playcount",
                        "genre",
                        "artist",
                        "album",
                        "year",
                        "file",
                        "thumbnail",
                        "fanart",
                        "rating",
                        "lastplayed"]
album_properties = [
                        "title",
                        "description",
                        "albumlabel",
                        "theme",
                        "mood",
                        "style",
                        "type",
                        "artist",
                        "genre",
                        "year",
                        "thumbnail",
                        "fanart",
                        "rating",
                        "playcount"]
musicvideo_properties = [
                        "title",
                        "artist",
                        "playcount",
                        "studio",
                        "director",
                        "year",
                        "plot",
                        "genre",
                        "runtime",
                        "art",
                        "file",
                        "streamdetails",
                        "resume"]

sort_lastplayed = {"order": "descending", "method": "lastplayed"}
sort_recent = {"order": "descending", "method": "dateadded"}
sort_random = {"method": "random"}
unplayed_filter = {"field": "playcount", "operator": "lessthan", "value": "1"}
specials_filter = {"field": "season", "operator": "greaterthan", "value": "0"}
inprogress_filter = {"field": "inprogress", "operator": "true", "value": ""}

def json_call(method,properties=None,sort=None,query_filter=None,limit=None,params=None):

    json_string = {"jsonrpc": "2.0", "id": 1, "method": method, "params": {}}

    if properties is not None:
        json_string["params"]["properties"] = properties
    if limit is not None:
        json_string["params"]["limits"] = {"start": 0, "end": limit}
    if sort is not None:
        json_string["params"]["sort"] = sort
    if query_filter is not None:
        json_string["params"]["filter"] = query_filter
    if params is not None:
        json_string["params"].update(params)

    json_string = simplejson.dumps(json_string)

    result = xbmc.executeJSONRPC(json_string)
    result = unicode(result, 'utf-8', errors='ignore')
    result = simplejson.loads(result)
    return result

def _get_cast(castData):
    listCast = []
    listCastAndRole = []
    for castmember in castData:
        listCast.append(castmember["name"])
        listCastAndRole.append((castmember["name"], castmember["role"]))
    return [listCast, listCastAndRole]


def _get_first_item(item):
    if len(item) > 0:
        item = item[0]
    else:
        item = ""
    return item


def _get_joined_items(item):
    if len(item) > 0:
        item = " / ".join(item)
    else:
        item = ""
    return item

def parse_movies(li, json_query, title=False):

    for movie in json_query:

        if "cast" in movie:
            cast = _get_cast(movie['cast'])

        li_item = xbmcgui.ListItem(movie['title'])
        li_item.setInfo(type="Video", infoLabels={"Title": movie['title'],
                                              "OriginalTitle": movie['originaltitle'],
                                              "Year": movie['year'],
                                              "Genre": _get_joined_items(movie.get('genre', "")),
                                              "Studio": _get_first_item(movie.get('studio', "")),
                                              "Country": _get_first_item(movie.get('country', "")),
                                              "Plot": movie['plot'],
                                              "PlotOutline": movie['plotoutline'],
                                              "dbid": movie['movieid'],
                                              "imdbnumber": movie['imdbnumber'],
                                              "Tagline": movie['tagline'],
                                              "Rating": str(float(movie['rating'])),
                                              "Votes": movie['votes'],
                                              "MPAA": movie['mpaa'],
                                              "lastplayed": movie['lastplayed'],
                                              "Cast": cast[0],
                                              "CastAndRole": cast[1],
                                              "mediatype": "movie",
                                              "Trailer": movie['trailer'],
                                              "Playcount": movie['playcount']})
        li_item.setProperty("resumetime", str(movie['resume']['position']))
        li_item.setProperty("totaltime", str(movie['resume']['total']))
        li_item.setProperty("fanart_image", movie['art'].get('fanart', ''))
        if title:
            li_item.setProperty("similartitle", title)
        li_item.setArt(movie['art'])
        li_item.setThumbnailImage(movie['art'].get('poster', ''))
        li_item.setIconImage('DefaultVideo.png')
        hasVideo = False
        for key, value in movie['streamdetails'].iteritems():
            for stream in value:
                if 'video' in key:
                    hasVideo = True
                li_item.addStreamInfo(key, stream)
        if not hasVideo:
            stream = {'duration': movie['runtime']}
            li_item.addStreamInfo("video", stream)
        li.append((movie['file'], li_item, False))

def parse_tvshows(li, json_query, title=False):

    for tvshow in json_query:

        if "cast" in tvshow:
            cast = _get_cast(tvshow['cast'])

        rating = str(round(tvshow['rating'],1))
        dbid = str(tvshow['tvshowid'])
        season = str(tvshow['season'])
        episode = str(tvshow['episode'])
        watchedepisodes = str(tvshow['watchedepisodes'])

        if int(episode) > int(watchedepisodes):
            unwatchedepisodes = int(episode) - int(watchedepisodes)
            unwatchedepisodes = str(unwatchedepisodes)
        else:
            unwatchedepisodes = "0"

        year = str(tvshow['year'])
        mpaa = tvshow['year']

        if not xbmc.getCondVisibility("Window.IsVisible(movieinformation)"):
            folder = True
            tvshow["file"] = "videodb://tvshows/titles/%s/" % dbid
        else:
            folder = False
            tvshow["file"] = "plugin://script.embuary.helper/?action=jumptoshow&dbid=%s&rating=%s&seasons=%s&episodes=%s&mpaa=%s&year=%s" % (dbid,rating,season,episode,mpaa,year)

        li_item = xbmcgui.ListItem(tvshow['title'])
        li_item.setInfo(type="Video", infoLabels={"Title": tvshow['title'],
                                              "Year": year,
                                              "Genre": _get_joined_items(tvshow.get('genre', "")),
                                              "Studio": _get_first_item(tvshow.get('studio', "")),
                                              "Country": _get_first_item(tvshow.get('country', "")),
                                              "Plot": tvshow['plot'],
                                              "Rating": rating,
                                              "Votes": tvshow['votes'],
                                              "Premiered": tvshow['premiered'],
                                              "MPAA": mpaa,
                                              "Cast": cast[0],
                                              "CastAndRole": cast[1],
                                              "mediatype": "tvshow",
                                              "dbid": dbid,
                                              "imdbnumber": str(tvshow['imdbnumber']),
                                              "Path": tvshow["file"],
                                              "DateAdded": tvshow["dateadded"],
                                              "Playcount": tvshow['playcount']})
        if title:
            li_item.setProperty("similartitle", title)
        li_item.setProperty("TotalSeasons", season)
        li_item.setProperty("TotalEpisodes", episode)
        li_item.setProperty("WatchedEpisodes", watchedepisodes)
        li_item.setProperty("UnwatchedEpisodes", unwatchedepisodes)
        li_item.setArt(tvshow['art'])
        li_item.setThumbnailImage(tvshow['art'].get('poster', ''))
        li_item.setIconImage('DefaultVideo.png')
        li.append((tvshow['file'], li_item, folder))

def parse_seasons(li, json_query, title=False):

    for season in json_query:
        tvshowdbid = str(season['tvshowid'])
        seasonnr = str(season['season'])
        episode = str(season['episode'])
        watchedepisodes = str(season['watchedepisodes'])

        title = "%s %s" % (xbmc.getLocalizedString(20373), seasonnr)

        if int(episode) > int(watchedepisodes):
            unwatchedepisodes = int(episode) - int(watchedepisodes)
            unwatchedepisodes = str(unwatchedepisodes)
        else:
            unwatchedepisodes = "0"

        if not xbmc.getCondVisibility("Window.IsVisible(movieinformation)"):
            folder = True
            file = "videodb://tvshows/titles/%s/%s/" % (tvshowdbid, seasonnr)
        else:
            folder = False
            file = "plugin://script.embuary.helper/?action=jumptoseason&dbid=%s&season=%s" % (tvshowdbid, seasonnr)

        li_item = xbmcgui.ListItem(title)
        li_item.setInfo(type="Video", infoLabels={"Title": title,
                                              "season": seasonnr,
                                              "episode": episode,
                                              "tvshowtitle": season['showtitle'],
                                              "playcount": season['playcount'],
                                              "dbid": season['seasonid']})
        li_item.setArt(season['art'])
        li_item.setProperty("WatchedEpisodes", watchedepisodes)
        li_item.setProperty("UnwatchedEpisodes", unwatchedepisodes)
        li_item.setThumbnailImage(season['art'].get('poster', ''))
        li_item.setIconImage('DefaultVideo.png')
        li.append((file, li_item, folder))


def parse_episodes(li, json_query):

    for episode in json_query:
        nEpisode = "%.2d" % float(episode['episode'])
        nSeason = "%.2d" % float(episode['season'])
        if "cast" in episode:
            cast = _get_cast(episode['cast'])
        li_item = xbmcgui.ListItem(episode['title'])
        li_item.setInfo(type="Video", infoLabels={"Title": episode['title'],
                                              "Episode": episode['episode'],
                                              "Season": episode['season'],
                                              "Premiered": episode['firstaired'],
                                              "Dbid": str(episode['episodeid']),
                                              "Plot": episode['plot'],
                                              "TVshowTitle": episode['showtitle'],
                                              "lastplayed": episode['lastplayed'],
                                              "Rating": str(float(episode['rating'])),
                                              "Playcount": episode['playcount'],
                                              "Director": _get_joined_items(episode.get('director', "")),
                                              "Writer": _get_joined_items(episode.get('writer', "")),
                                              "Cast": cast[0],
                                              "CastAndRole": cast[1],
                                              "mediatype": "episode"})
        li_item.setProperty("resumetime", str(episode['resume']['position']))
        li_item.setProperty("totaltime", str(episode['resume']['total']))
        li_item.setProperty("fanart_image", episode['art'].get('tvshow.fanart', ''))
        li_item.setArt(episode['art'])
        li_item.setThumbnailImage(episode['art'].get('thumb', ''))
        li_item.setIconImage('DefaultTVShows.png')

        hasVideo = False
        for key, value in episode['streamdetails'].iteritems():
            for stream in value:
                if 'video' in key:
                    hasVideo = True
                li_item.addStreamInfo(key, stream)

        # if duration wasnt in the streaminfo try adding the scraped one
        if not hasVideo:
            stream = {'duration': episode['runtime']}
            li_item.addStreamInfo("video", stream)
        li.append((episode['file'], li_item, False))


def parse_cast(li,json_query):

    for actor in json_query:
        li_item = xbmcgui.ListItem(actor["name"])
        li_item.setLabel(actor["name"])
        li_item.setLabel2(actor["role"])
        li_item.setThumbnailImage(actor.get('thumbnail', ""))
        li_item.setIconImage('DefaultActor.png')
        li.append(("", li_item, False))

def parse_genre(li,json_query):

    for genre in json_query:
        li_item = xbmcgui.ListItem(genre["label"])
        li_item.setInfo(type="Video", infoLabels={"Title": genre["label"],
                                              "dbid": str(genre["genreid"]),
                                              "Path": genre["file"]})
        li_item.setArt(genre["art"])
        li_item.setIconImage("DefaultGenre.png")
        li.append((genre["file"], li_item, True))

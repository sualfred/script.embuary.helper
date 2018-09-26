#!/usr/bin/python

import xbmcplugin
import json as simplejson
import random
from resources.lib.utils import log
from resources.lib.utils import remove_quotes
from resources.lib.library import *

class PluginContent(object):
    def __init__(self,params,li):

        self.dbtitle = remove_quotes(params.get("title"))
        self.dbtype = remove_quotes(params.get("type"))
        self.dbid = remove_quotes(params.get("dbid"))
        self.li = li

        if self.dbtype == "movie":
            self.method_details = "VideoLibrary.GetMovieDetails"
            self.method_item = "VideoLibrary.GetMovies"
            self.param = "movieid"
            self.key_details = "moviedetails"
            self.key_items = "movies"
            self.properties = movie_properties
        elif self.dbtype == "tvshow":
            self.method_details = "VideoLibrary.GetTVShowDetails"
            self.method_item = "VideoLibrary.GetTVShows"
            self.param = "tvshowid"
            self.key_details = "tvshowdetails"
            self.key_items = "tvshows"
            self.properties = tvshow_properties

    # inprogress media
    def get_inprogress(self):
        if not self.dbtype or self.dbtype == "movie":
            json_query = json_call("VideoLibrary.GetMovies",
                                properties=movie_properties,
                                query_filter=inprogress_filter
                                )
            try:
                json_query = json_query["result"]["movies"]
            except Exception:
                log("No inprogress movies found.")
            else:
                parse_movies(self.li,json_query)

        if not self.dbtype or self.dbtype == "tvshow":
            json_query = json_call("VideoLibrary.GetEpisodes",
                            properties=episode_properties,
                            query_filter=inprogress_filter
                            )
            try:
                json_query = json_query["result"]["episodes"]
            except Exception:
                log("No inprogress episodes found.")
            else:
                parse_episodes(self.li,json_query)

    # genres
    def get_genre(self):

        json_query = json_call("VideoLibrary.GetGenres",
                            sort={"method": "label"},
                            params={"type": self.dbtype}
                            )

        for genre in json_query["result"]["genres"]:

            genre_items = json_call(self.method_item,
                            properties=["art"],
                            sort=sort_random, limit=4,
                            query_filter={"operator": "is", "field": "genre", "value": genre['label']}
                            )
            posters = {}
            index=0
            for art in genre_items["result"][self.key_items]:
                poster = "poster.%s" % index
                posters[poster] = art["art"].get("poster", "")
                index+=1

            genre["art"] = posters
            genre["file"] = "videodb://%ss/genres/%s/" % (self.dbtype, genre["genreid"])

        try:
            json_query = json_query["result"]["genres"]
        except Exception:
            log("No genres found. Do nothing")
        else:
            parse_genre(self.li,json_query)


    # because you watched xyz
    def get_similar(self):

        if self.dbid:
            json_query = json_call(self.method_details,
                                properties=["title", "genre"],
                                params={self.param: int(self.dbid)}
                                )
        else:
            if self.dbtype == "tvshow":
                query_filter={"or": [{"field":"playcount","operator":"greaterthan","value":["0"]},{"field":"numwatched","operator":"greaterthan","value":["0"]}]}
            else:
                query_filter={"field":"playcount","operator":"greaterthan","value":["0"]}

            json_query = json_call(self.method_item,
                                properties=["title", "genre"],
                                sort={"method": "lastplayed","order": "descending"}, limit=10,
                                query_filter=query_filter
                                )
        try:
            if self.dbid:
                title = json_query["result"][self.key_details]["title"]
                genres = json_query["result"][self.key_details]["genre"]
            else:
                similar_list = []
                for x in json_query["result"][self.key_items]:
                    if x['genre']:
                        similar_list.append(x)

                random.shuffle(similar_list)

                title = similar_list[0]["title"]
                genres = similar_list[0]["genre"]

        except Exception:
            log ("Not able to get genres")
            return

        random.shuffle(genres)

        if len(genres) > 1:
            query_filter={"and": [{"operator": "isnot", "field": "title", "value": title},{"operator": "is", "field": "genre", "value": genres[0]}, {"operator": "is", "field": "genre", "value": genres[1]}]}
        else:
            query_filter={"and": [{"operator": "isnot", "field": "title", "value": title},{"operator": "is", "field": "genre", "value": genres[0]}]}

        json_query = json_call(self.method_item,
                            properties=self.properties,
                            sort=sort_random, limit=15,
                            query_filter=query_filter
                            )

        try:
            json_query = json_query['result'][self.key_items]
        except KeyError:
            log("No similar items. Do nothing")
        else:
            if self.dbtype == "movie":
                parse_movies(self.li,json_query,title)
            elif self.dbtype == "tvshow":
                parse_tvshows(self.li,json_query,title)

    # cast
    def get_cast(self):

        if self.dbtitle:
            json_query = json_call(self.method_item,
                                properties=["cast"],
                                limit=1,
                                query_filter={"operator": "is", "field": "title", "value": self.dbtitle}
                                )
        elif self.dbid:
            json_query = json_call(self.method_details,
                                properties=["cast"],
                                params={self.param: int(self.dbid)}
                                )

        try:
            if self.key_details in json_query['result']:
                json_query = json_query['result'][self.key_details]['cast']
            else:
                json_query = json_query['result'][self.key_items][0]['cast']

        except Exception:
            log("No cast found. Do nothing")

        else:
            parse_cast(self.li,json_query)

    # jump to letter
    def jumptoletter(self):

        if xbmc.getInfoLabel("Container.NumItems"):

            all_letters = []
            for i in range(int(xbmc.getInfoLabel("Container.NumItems"))):
                all_letters.append(xbmc.getInfoLabel("Listitem(%s).SortLetter" % i).upper())

            if len(all_letters) > 0:
                for letter in ["#", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                               "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:

                    li_item = xbmcgui.ListItem(label=letter)

                    if letter == "#":
                        li_path = "plugin://script.embuary.helper/?action=smsjump&letter=0"
                        li_item.setProperty("IsNumber", "0")
                    elif letter in all_letters:
                        li_path = "plugin://script.embuary.helper/?action=smsjump&letter=%s" % letter
                    else:
                        li_path = ""
                        li_item.setProperty("NotAvailable", "true")

                    self.li.append((li_path, li_item, False))


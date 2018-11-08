#!/usr/bin/python

import xbmcplugin
import json as simplejson
import random
from resources.lib.utils import log
from resources.lib.utils import remove_quotes
from resources.lib.library import *

class PluginContent(object):
    def __init__(self,params,li):

        self.params = params
        self.dbtitle = remove_quotes(params.get("title"))
        self.dbtype = remove_quotes(params.get("type"))
        self.dbid = remove_quotes(params.get("dbid"))
        self.season = remove_quotes(params.get("season"))
        self.tag = remove_quotes(params.get("tag"))
        self.unwatched = remove_quotes(params.get("unwatched"))
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

        self.sort_lastplayed = {"order": "descending", "method": "lastplayed"}
        self.sort_recent = {"order": "descending", "method": "dateadded"}
        self.sort_random = {"method": "random"}
        self.unplayed_filter = {"field": "playcount", "operator": "lessthan", "value": "1"}
        self.unplayedepisodes_filter = {"field":"numwatched","operator":"greaterthan","value":["0"]}
        self.specials_filter = {"field": "season", "operator": "greaterthan", "value": "0"}
        self.inprogress_filter = {"field": "inprogress", "operator": "true", "value": ""}
        self.notinprogress_filter = {"field": "inprogress", "operator": "false", "value": ""}
        self.tag_filter = {"operator": "is", "field": "tag", "value": self.tag}
        self.title_filter = {"operator": "is", "field": "title", "value": self.dbtitle}

    # get seasons
    def get_seasons(self):
        if not self.dbid:
            get_dbid = json_call("VideoLibrary.GetTVShows",
                            properties=["title"], limit=1,
                            query_filter=self.title_filter
                            )

            try:
                tvshow_dbid = get_dbid["result"]["tvshows"][0]["tvshowid"]
            except Exception:
                log("Get seasons by TV show: Show not found")
                return

        else:
            tvshow_dbid = self.dbid

        season_query = json_call("VideoLibrary.GetSeasons",
                            properties=season_properties,
                            sort={"order": "ascending", "method": "season"},
                            params={"tvshowid": int(tvshow_dbid)}
                            )

        try:
            season_query = season_query["result"]["seasons"]
        except Exception:
            log("Get seasons by TV show: No seasons found")
        else:
            parse_seasons(self.li,season_query)

    # get more episodes from the same season
    def get_seasonepisodes(self):

        if not self.dbid:
            get_dbid = json_call("VideoLibrary.GetTVShows",
                            properties=["title"], limit=1,
                            query_filter=self.title_filter
                            )

            try:
                tvshow_dbid = get_dbid["result"]["tvshows"][0]["tvshowid"]
            except Exception:
                log("Get more episodes by season: Show not found")
                return

        else:
            tvshow_dbid = self.dbid

        episode_query = json_call("VideoLibrary.GetEpisodes",
                            properties=episode_properties,
                            sort={"order": "ascending", "method": "episode"},
                            query_filter={"operator": "is", "field": "season", "value": self.season},
                            params={"tvshowid": int(tvshow_dbid)}
                            )

        try:
            episode_query = episode_query["result"]["episodes"]
        except Exception:
            log("Get more episodes by season: No episodes found")
        else:
            parse_episodes(self.li,episode_query)

    # get nextup episodes of last played tv shows
    def get_nextup(self):

        filters = [self.inprogress_filter]
        if self.tag:
            filters.append(self.tag_filter)
        filter = {"and": filters}

        json_query = json_call("VideoLibrary.GetTVShows",
                        properties=tvshow_properties,
                        sort=self.sort_lastplayed, limit=25,
                        query_filter=filter
                        )

        try:
            json_query = json_query['result']["tvshows"]
        except Exception:
            log("Get next up episodes: No TV shows found")
            return

        for episode in json_query:

                episode_query = json_call("VideoLibrary.GetEpisodes",
                            properties=episode_properties,
                            sort={"order": "ascending", "method": "episode"},limit=1,
                            query_filter={"and": [self.unplayed_filter,self.notinprogress_filter,{"field": "season", "operator": "greaterthan", "value": "0"}]},
                            params={"tvshowid": int(episode['tvshowid'])}
                            )

                try:
                    episode_details = episode_query["result"]["episodes"]
                except Exception:
                    log("Get next up episodes: No next episodes found for %s" % episode['title'])
                else:
                    parse_episodes(self.li,episode_details)

    # get mixed recently added tvshows/episodes
    def get_newshows(self):

        filters = [self.unplayed_filter]
        if self.tag:
            filters.append(self.tag_filter)
        filter = {"and": filters}

        json_query = json_call("VideoLibrary.GetTVShows",
                        properties=tvshow_properties,
                        sort=self.sort_recent, limit=25,
                        query_filter=filter
                        )

        try:
            json_query = json_query['result']["tvshows"]
        except Exception:
            log("Get new media: No TV shows found")
            return

        for tvshow in json_query:

            totalepisodes = tvshow['episode']
            watchedepisodes = tvshow['watchedepisodes']

            if totalepisodes > watchedepisodes:
                unwatchedepisodes = int(totalepisodes) - int(watchedepisodes)
            else:
                unwatchedepisodes = 0

            if unwatchedepisodes == 1:
                episode_query = json_call("VideoLibrary.GetEpisodes",
                            properties=episode_properties,
                            sort=self.sort_recent,limit=1,
                            params={"tvshowid": int(tvshow['tvshowid'])}
                            )

                try:
                    episode_query = episode_query["result"]["episodes"]
                except Exception:
                    log("Get new media: Error fetching by episode details")
                else:
                    parse_episodes(self.li,episode_query)

            else:
                tvshow_query = json_call("VideoLibrary.GetTVShowDetails",
                            properties=tvshow_properties,
                            params={"tvshowid": int(tvshow['tvshowid'])}
                            )
                try:
                    tvshow_query = tvshow_query["result"]["tvshowdetails"]
                except Exception:
                    log("Get new media: Error fetching by TV show details")
                else:
                    parse_tvshows(self.li,[tvshow_query])

    # media by genre
    def get_mediabygenre(self):

        genre = remove_quotes(self.params.get("genre"))

        if not genre:
            genres_list = []

            if not self.dbtype or self.dbtype == "movie":
                movies_genres_query = json_call("VideoLibrary.GetGenres",
                                    sort={"method": "label"},
                                    params={"type": "movie"}
                                    )
                try:
                    for item in movies_genres_query["result"]["genres"]:
                        genres_list.append(item.get("label"))
                except Exception:
                    log("Get movies by genre: no genres found")

            if not self.dbtype or self.dbtype == "tvshow":
                tvshow_genres_query = json_call("VideoLibrary.GetGenres",
                                    sort={"method": "label"},
                                    params={"type": "tvshow"}
                                    )
                try:
                    for item in tvshow_genres_query["result"]["genres"]:
                        genres_list.append(item.get("label"))
                except Exception:
                    log("Get TV shows by genre: no genres found")

            if genres_list:
                random.shuffle(genres_list)
                genre = genres_list[0]

        if genre:
            filters = [{"operator": "contains", "field": "genre", "value": genre}]
            if self.unwatched == "True":
                filters.append(self.unplayed_filter)
            if self.tag:
                filters.append(self.tag_filter)
            filter = {"and": filters}

            if not self.dbtype or self.dbtype == "movie":
                json_query = json_call("VideoLibrary.GetMovies",
                                    properties=movie_properties,
                                    sort=self.sort_random, limit=10,
                                    query_filter=filter
                                    )
                try:
                    json_query = json_query["result"]["movies"]
                except Exception:
                    log("Movies by genre %s: No movies found." % genre)
                else:
                    parse_movies(self.li,json_query,searchstring=genre)

            if not self.dbtype or self.dbtype == "tvshow":
                json_query = json_call("VideoLibrary.GetTVShows",
                                    properties=tvshow_properties,
                                    sort=self.sort_random, limit=10,
                                    query_filter=filter
                                    )
                try:
                    json_query = json_query["result"]["tvshows"]
                except Exception:
                    log("TV shows by genre %s: No shows found." % genre)
                else:
                    parse_tvshows(self.li,json_query,searchstring=genre)

            random.shuffle(self.li)

    # inprogress media
    def get_inprogress(self):

        if not self.dbtype or self.dbtype == "movie":
            json_query = json_call("VideoLibrary.GetMovies",
                                properties=movie_properties,
                                query_filter=self.inprogress_filter
                                )
            try:
                json_query = json_query["result"]["movies"]
            except Exception:
                log("In progress media: No movies found.")
            else:
                parse_movies(self.li,json_query)

        if not self.dbtype or self.dbtype == "tvshow":
            json_query = json_call("VideoLibrary.GetEpisodes",
                                properties=episode_properties,
                                query_filter=self.inprogress_filter
                                )
            try:
                json_query = json_query["result"]["episodes"]
            except Exception:
                log("In progress media: No episodes found.")
            else:
                parse_episodes(self.li,json_query)

    # genres
    def get_genre(self):

        json_query = json_call("VideoLibrary.GetGenres",
                            sort={"method": "label"},
                            params={"type": self.dbtype}
                            )
        try:
            json_query = json_query["result"]["genres"]
        except KeyError:
            log("Get genres: No genres found")
            return

        for genre in json_query:

            genre_items = json_call(self.method_item,
                            properties=["art"],
                            sort=self.sort_random, limit=4,
                            query_filter={"operator": "is", "field": "genre", "value": genre['label']}
                            )
            posters = {}
            index=0
            for art in genre_items["result"][self.key_items]:
                poster = "poster.%s" % index
                posters[poster] = art["art"].get("poster", "")
                index+=1

            genre["art"] = posters

            try:
                genre["file"] = "videodb://%ss/genres/%s/" % (self.dbtype, genre["genreid"])
            except Exception:
                log("Get genres: No genre ID found")
                return

        parse_genre(self.li,json_query)

    # get movies by director
    def get_directed_by(self):

        json_query = json_call("VideoLibrary.GetMovieDetails",
                            properties=["title", "director"],
                            params={"movieid": int(self.dbid)}
                            )

        try:
            directors = json_query['result']['moviedetails']['director']
            title = json_query['result']['moviedetails']['title']
            joineddirectors = " / ".join(directors)
        except Exception:
            log("Movies by director: No director found")
            return

        filters=[]
        for director in directors:
            filters.append({"operator": "is", "field": "director", "value": director})
        filter = {"and": [{"or": filters}, {"operator": "isnot", "field": "title", "value": title}]}

        json_query = json_call("VideoLibrary.GetMovies",
                                    properties=movie_properties,
                                    sort=self.sort_random,
                                    query_filter=filter
                                    )
        try:
            json_query = json_query["result"]["movies"]
        except Exception:
            log("Movies by director %s: No additional movies found" % joineddirectors)
        else:
            parse_movies(self.li,json_query,searchstring=joineddirectors)


    # because you watched xyz
    def get_similar(self):

        if self.dbid:
            json_query = json_call(self.method_details,
                                properties=["title", "genre"],
                                params={self.param: int(self.dbid)}
                                )
        else:
            if self.dbtype == "tvshow":
                query_filter={"or": [self.unplayed_filter,self.unplayedepisodes_filter]}
            else:
                query_filter=self.unplayed_filter

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
            log ("Get similar: Not able to get genres")
            return

        random.shuffle(genres)

        filters = [{"operator": "isnot", "field": "title", "value": title},{"operator": "is", "field": "genre", "value": genres[0]}]
        if len(genres) > 1:
            filters.append({"operator": "is", "field": "genre", "value": genres[1]})
        if self.tag:
            filters.append(self.tag_filter)
        filter = {"and": filters}

        json_query = json_call(self.method_item,
                            properties=self.properties,
                            sort=self.sort_random, limit=15,
                            query_filter=filter
                            )

        try:
            json_query = json_query['result'][self.key_items]
        except KeyError:
            log("Get similar: No matching items found")
        else:
            if self.dbtype == "movie":
                parse_movies(self.li,json_query,searchstring=title)
            elif self.dbtype == "tvshow":
                parse_tvshows(self.li,json_query,searchstring=title)

    # cast
    def get_cast(self):

        if self.dbtitle:
            json_query = json_call(self.method_item,
                                properties=["cast"],
                                limit=1,
                                query_filter=self.title_filter
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
            log("Get cast: No cast found.")

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


#!/usr/bin/python
# coding: utf-8

#################################################################################################

import xbmc
import sys

from resources.lib.helper import *

#################################################################################################

class Favourites(object):
    def __init__(self,dbid=None,dbtype=None):
        self.dbid = dbid
        self.dbtype = dbtype

        if not self.dbid or not self.dbtype:
            listitem = sys.listitem.getVideoInfoTag()
            self.dbid = listitem.getDbId()
            self.dbtype = listitem.getMediaType()

        if self.dbtype == 'movie':
            self.method_details = 'VideoLibrary.GetMovieDetails'
            self.method_setdetails = 'VideoLibrary.SetMovieDetails'
            self.param = 'movieid'
            self.key_details = 'moviedetails'
            self.tag = 'Fav. Kodi Movies'

        elif self.dbtype == 'tvshow':
            self.method_details = 'VideoLibrary.GetTVShowDetails'
            self.method_setdetails = 'VideoLibrary.SetTVShowDetails'
            self.param = 'tvshowid'
            self.key_details = 'tvshowdetails'
            self.tag = 'Fav. Kodi TV Shows'

        self.check_tag()
        self.update_info()

    def check_tag(self):
        result = json_call(self.method_details,
                               properties=['tag'],
                               params={self.param: int(self.dbid)}
                               )

        result = result['result'][self.key_details]

        self.tag_list = result.get('tag',[])
        self.is_fav = True if self.tag in self.tag_list else False

    def update_info(self):
        if not self.is_fav:
            self.tag_list.append(self.tag)
        else:
            self.tag_list.remove(self.tag)

        json_call(self.method_setdetails,
                  params={self.param: int(self.dbid), 'tag': self.tag_list}
                  )

        reload_widgets(reason='Fav. updated')
#!/usr/bin/python
# coding: utf-8

########################

import sys
import xbmc
import xbmcgui
import xbmcplugin

''' Python 2<->3 compatibility
'''
try:
	from urllib import urlencode
except ImportError:
	from urllib.parse import urlencode

from resources.lib.helper import *

########################

categories = [
		{'name': ADDON.getLocalizedString(32011), 'action': 'folder', 'type': 'mixed'},
		{'name': xbmc.getLocalizedString(342), 'action': 'folder', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(20343), 'action': 'folder', 'type': 'tvshow'},
		{'name': 'Emby: %s' % xbmc.getLocalizedString(342), 'action': 'folder', 'type': 'emby_movie'},
		{'name': 'Emby: %s' % xbmc.getLocalizedString(20343), 'action': 'folder', 'type': 'emby_tvshow'},
		]

mixed = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'}
		]

movie = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': xbmc.getLocalizedString(135), 'action': 'getgenre'}
		]

tvshow = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32008), 'action': 'getnextup'},
		{'name': ADDON.getLocalizedString(32010), 'action': 'getnewshows'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': xbmc.getLocalizedString(135), 'action': 'getgenre'}
		]

emby_movie = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': xbmc.getLocalizedString(20382), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'limit': '50', 'sort': '{"order": "descending", "method": "dateadded"}'},
		{'name': xbmc.getLocalizedString(16101), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'sort': '{"order": "ascending", "method": "title"}'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': ADDON.getLocalizedString(32012), 'action': 'byargs', 'limit': '50', 'sort': '{"order": "descending", "method": "rating"}'},
		{'name': xbmc.getLocalizedString(590), 'action': 'byargs', 'sort': '{"method": "random"}', 'limit': '50'},
		]

emby_tvshow = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': xbmc.getLocalizedString(20382), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'limit': '50', 'sort': '{"order": "descending", "method": "dateadded"}'},
		{'name': xbmc.getLocalizedString(16101), 'action': 'byargs', 'filter': '{"field": "numwatched", "operator": "lessthan", "value": "1"}', 'sort': '{"order": "ascending", "method": "title"}'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32008), 'action': 'getnextup'},
		{'name': ADDON.getLocalizedString(32010), 'action': 'getnewshows'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': ADDON.getLocalizedString(32012), 'action': 'byargs', 'limit': '50', 'sort': '{"order": "descending", "method": "rating"}'},
		{'name': xbmc.getLocalizedString(590), 'action': 'byargs', 'sort': '{"method": "random"}', 'limit': '50'},
		]

########################

class PluginListing(object):

	def __init__(self,params,li):
		self.subdir = params.get('folder','')
		self.li = li

		if params.get('browse'):
			self.widgets()
		else:
			self.folders()


	def folders(self):
		for folder in categories:
			label = folder['name']
			url = self._encode_url(folder=folder['type'],browse=True)
			self._add_item(folder['name'],url)


	def widgets(self):
		if self.subdir == 'mixed':
			cat = mixed
		elif self.subdir == 'movie':
			cat = movie
			cat_type = 'movie'
		elif self.subdir == 'tvshow':
			cat = tvshow
			cat_type = 'tvshow'
		elif self.subdir == 'emby_movie':
			cat = emby_movie
			cat_type = 'movie'
		elif self.subdir == 'emby_tvshow':
			cat = emby_tvshow
			cat_type = 'tvshow'

		if not self.subdir.startswith('emby_'):
			for widget in cat:
				if not self.subdir == 'mixed':
					url = self._encode_url(info=widget['action'], type=cat_type)
				else:
					url = self._encode_url(info=widget['action'])
				self._add_item(widget['name'],url)

		else:
			i = 0
			for prop in range(30):
				tag = winprop('emby.wnodes.%s.cleantitle' % i)
				database = winprop('emby.wnodes.%s.type' % i)

				if cat_type in database:
					for widget in cat:
						label = '%s: %s' % (tag, widget['name'])
						url = self._encode_url(info=widget['action'], type=cat_type, tag=tag, filter_args=widget.get('filter',''), sort_args=widget.get('sort',''), limit=widget.get('limit',''))
						self._add_item(label,url)

				i += 1


	def _set_icon(self,url):
		source = self.subdir or url
		if 'emby_' in source:
			return 'special://home/addons/plugin.video.emby/icon.png'
		else:
			return 'special://home/addons/script.embuary.helper/resources/icon.png'


	def _encode_url(self,**kwargs):
		return '{0}?{1}'.format(sys.argv[0], urlencode(kwargs))


	def _add_item(self,label,url):
		list_item = xbmcgui.ListItem(label=label)
		list_item.setInfo('video', {'title': label, 'mediatype': 'video'})
		list_item.setArt({'icon': 'DefaultFolder.png','thumb': self._set_icon(url)})
		self.li.append((url, list_item, True))

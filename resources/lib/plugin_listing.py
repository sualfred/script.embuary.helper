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

index = [
		{'name': ADDON.getLocalizedString(32011), 'action': 'folder', 'type': 'mixed'},
		{'name': xbmc.getLocalizedString(342), 'action': 'folder', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(20343), 'action': 'folder', 'type': 'tvshow'}
		]

index_emby = [
		{'name': xbmc.getLocalizedString(342), 'action': 'folder', 'type': 'emby_movie'},
		{'name': xbmc.getLocalizedString(20343), 'action': 'folder', 'type': 'emby_tvshow'},
		]

mixed = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'}
		]

movie = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32014), 'action': 'getsimilar', 'pos': '0'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': xbmc.getLocalizedString(135), 'action': 'getgenre'}
		]

tvshow = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32008), 'action': 'getnextup'},
		{'name': ADDON.getLocalizedString(32010), 'action': 'getnewshows'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32014), 'action': 'getsimilar', 'pos': '0'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': xbmc.getLocalizedString(135), 'action': 'getgenre'}
		]

emby_movie = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': xbmc.getLocalizedString(20382), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'limit': '50', 'sort': '{"order": "descending", "method": "dateadded"}'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32014), 'action': 'getsimilar', 'pos': '0'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': ADDON.getLocalizedString(32012), 'action': 'byargs', 'limit': '50', 'sort': '{"order": "descending", "method": "rating"}'},
		{'name': xbmc.getLocalizedString(16101), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'sort': '{"order": "ascending", "method": "title"}'},
		{'name': xbmc.getLocalizedString(590), 'action': 'byargs', 'sort': '{"method": "random"}', 'limit': '50'},
		]

emby_tvshow = [
		{'name': ADDON.getLocalizedString(32013), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32008), 'action': 'getnextup'},
		{'name': ADDON.getLocalizedString(32010), 'action': 'getnewshows'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar'},
		{'name': ADDON.getLocalizedString(32014), 'action': 'getsimilar', 'pos': '0'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': ADDON.getLocalizedString(32012), 'action': 'byargs', 'limit': '50', 'sort': '{"order": "descending", "method": "rating"}'},
		{'name': xbmc.getLocalizedString(16101), 'action': 'byargs', 'filter': '{"field": "numwatched", "operator": "lessthan", "value": "1"}', 'sort': '{"order": "ascending", "method": "title"}'},
		{'name': xbmc.getLocalizedString(590), 'action': 'byargs', 'sort': '{"method": "random"}', 'limit': '50'},
		]

########################

class PluginListing(object):

	def __init__(self,params,li):
		self.li = li
		self.subdir = params.get('folder','')

		if self.subdir:
			self.tag = None
			self.cat_type = None

			if 'tvshow' in self.subdir:
				self.cat_type = 'tvshow'
			elif 'movie' in self.subdir:
				self.cat_type = 'movie'

			self.widgets()

		else:
			self.folders()


	def folders(self):
		for folder in index:
			url = self._encode_url(folder=folder['type'])
			self._add_item(folder['name'],url)

		if visible('System.HasAddon(plugin.video.emby'):
			for folder in index_emby:
				label = 'Emby: %s' % folder['name']
				url = self._encode_url(folder=folder['type'])
				self._add_item(label,url)


	def widgets(self):
		if not self.subdir.startswith('emby_'):
			for widget in globals()[self.subdir]:
				url = self._get_url(widget)
				self._add_item(widget['name'],url)

		else:
			i = 0
			for prop in range(30):
				self.tag = winprop('emby.wnodes.%s.cleantitle' % i)
				database = winprop('emby.wnodes.%s.type' % i)

				if self.cat_type in database:
					for widget in globals()[self.subdir]:
						label = '%s: %s' % (self.tag, widget['name'])
						url = self._get_url(widget)
						self._add_item(label,url)

				i += 1


	def _get_url(self,widget):
		return self._encode_url(info=widget['action'], type=self.cat_type, tag=self.tag, pos=widget.get('pos',''), filter_args=widget.get('filter',''), sort_args=widget.get('sort',''), limit=widget.get('limit',''))


	def _encode_url(self,**kwargs):
		empty_keys = [key for key,value in kwargs.iteritems() if not value or value is None]
		for key in empty_keys:
			del kwargs[key]

		return '{0}?{1}'.format(sys.argv[0], urlencode(kwargs))


	def _add_item(self,label,url):
		icon = 'special://home/addons/script.embuary.helper/resources/icon.png'
		source = self.subdir or url

		if 'emby_' in source:
			icon = 'special://home/addons/plugin.video.emby/icon.png'

		list_item = xbmcgui.ListItem(label=label)
		list_item.setInfo('video', {'title': label, 'mediatype': 'video'})
		list_item.setArt({'icon': 'DefaultFolder.png','thumb': icon})
		self.li.append((url, list_item, True))

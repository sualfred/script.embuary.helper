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

widgets = [
		{'name': xbmc.getLocalizedString(575), 'action': 'getinprogress'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre'},
		{'name': xbmc.getLocalizedString(575), 'action': 'getinprogress', 'type': 'movie'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar', 'type': 'movie'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(135), 'action': 'getgenre', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(575), 'action': 'getinprogress', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32008), 'action': 'getnextup', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32010), 'action': 'getnewshows', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre', 'type': 'tvshow'},
		{'name': xbmc.getLocalizedString(135), 'action': 'getgenre', 'type': 'tvshow'}
		]

emby_movie_widgets = [
		{'name': xbmc.getLocalizedString(20382), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'limit': '50', 'sort': '{"order": "descending", "method": "dateadded"}', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(16101), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'sort': '{"order": "ascending", "method": "title"}', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(575), 'action': 'getinprogress', 'type': 'movie'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar', 'type': 'movie'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre', 'type': 'movie'},
		{'name': ADDON.getLocalizedString(32012), 'action': 'byargs', 'limit': '50', 'sort': '{"order": "descending", "method": "rating"}', 'type': 'movie'},
		{'name': xbmc.getLocalizedString(590), 'action': 'byargs', 'sort': '{"method": "random"}', 'limit': '50', 'type': 'movie'},
		]

emby_tvshow_widgets = [
		{'name': xbmc.getLocalizedString(20382), 'action': 'byargs', 'filter': '{"field": "playcount", "operator": "lessthan", "value": "1"}', 'limit': '50', 'sort': '{"order": "descending", "method": "dateadded"}', 'type': 'tvshow'},
		{'name': xbmc.getLocalizedString(16101), 'action': 'byargs', 'filter': '{"field": "numwatched", "operator": "lessthan", "value": "1"}', 'sort': '{"order": "ascending", "method": "title"}', 'type': 'tvshow'},
		{'name': xbmc.getLocalizedString(575), 'action': 'getinprogress', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32007), 'action': 'getsimilar', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32008), 'action': 'getnextup', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32010), 'action': 'getnewshows', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32009), 'action': 'getbygenre', 'type': 'tvshow'},
		{'name': ADDON.getLocalizedString(32012), 'action': 'byargs', 'limit': '50', 'sort': '{"order": "descending", "method": "rating"}', 'type': 'tvshow'},
		{'name': xbmc.getLocalizedString(590), 'action': 'byargs', 'sort': '{"method": "random"}', 'limit': '50', 'type': 'tvshow'},
		]

########################

def get_url(widget,tag=''):
	url = encode_url(info=widget['action'], type=widget.get('type',''), tag=tag, filter_args=widget.get('filter',''), sort_args=widget.get('sort',''), limit=widget.get('limit',''))
	return url


def encode_url(**kwargs):
	return '{0}?{1}'.format(sys.argv[0], urlencode(kwargs))


def add_item(category,name,url):
	label = '%s: %s' % (category, name)
	list_item = xbmcgui.ListItem(label=label)
	list_item.setInfo('video', {'title': label, 'mediatype': 'video'})
	list_item.setArt({'icon': 'DefaultFolder.png','thumb': 'special://home/addons/script.embuary.helper/resources/icon.png'})
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, list_item, True)


def listing():
	''' Regular widgets
	'''
	for widget in widgets:
		url = get_url(widget)
		mediatype = widget.get('type','')

		if mediatype == 'movie':
			category = xbmc.getLocalizedString(342)
		elif mediatype == 'tvshow':
			category = xbmc.getLocalizedString(20343)
		else:
			category = ADDON.getLocalizedString(32011)

		add_item(category,widget['name'],url)


	''' Emby widgets
	'''
	i = 0
	for prop in range(30):
		tag = winprop('emby.wnodes.%s.cleantitle' % i)
		database = winprop('emby.wnodes.%s.type' % i)

		if database == 'movies':
			for widget in emby_movie_widgets:
				url = get_url(widget,tag)
				category = 'Emby %s "%s"' % (xbmc.getLocalizedString(342), tag)
				add_item(category,widget['name'],url)

		if database == 'tvshows':
			for widget in emby_tvshow_widgets:
				url = get_url(widget,tag)
				category = 'Emby %s "%s"' % (xbmc.getLocalizedString(20343), tag)
				add_item(category,widget['name'],url)

		i += 1

	xbmcplugin.endOfDirectory(int(sys.argv[1]))


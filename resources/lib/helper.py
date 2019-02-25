#!/usr/bin/python
# coding: utf8

########################

import xbmc
import xbmcaddon
import xbmcgui
import simplejson

########################

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode('utf-8')

PLAYER = xbmc.Player()
VIDEOPLAYLIST = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
MUSICPLAYLIST = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)

########################

def get_kodiversion():

    build = xbmc.getInfoLabel('System.BuildVersion')
    return int(build[:2])

def log(txt,loglevel='notice'):

	if loglevel == 'notice':
		level = xbmc.LOGNOTICE
	elif loglevel == 'warning':
		level = xbmc.LOGWARNING
	elif loglevel == 'debug':
		level = xbmc.LOGDEBUG

	if isinstance(txt, str):
		txt = txt.decode('utf-8')
	message = u'[ %s ] %s' % (ADDON_ID, txt)

	xbmc.log(msg=message.encode('utf-8'), level=level )


def remove_quotes(label):
    if not label:
        return ''
    if label.startswith("'") and label.endswith("'") and len(label) > 2:
        label = label[1:-1]
        if label.startswith('"') and label.endswith('"') and len(label) > 2:
            label = label[1:-1]
    return label


def execute(cmd):
	xbmc.executebuiltin(cmd)


def visible(condition):
	return xbmc.getCondVisibility(condition)


def grabfanart():
    fanarts = list()

    movie_query = json_call('VideoLibrary.GetMovies',
                        properties=['art'],
                        sort={'method': 'random'}, limit=20
                        )

    try:
        for art in movie_query['result']['movies']:
                movie_fanart = art['art'].get('fanart', '')
                fanarts.append(movie_fanart)
    except Exception:
        log('Backgrounds: No movie artworks found.')

    tvshow_query = json_call('VideoLibrary.GetTVShows',
                        properties=['art'],
                        sort={'method': 'random'}, limit=20
                        )

    try:
        for art in tvshow_query['result']['tvshows']:
                tvshow_fanart = art['art'].get('fanart', '')
                fanarts.append(tvshow_fanart)
    except Exception:
        log('Backgrounds: No TV show artworks found.')

    return fanarts


def winprop(key, value=None, clear=False, window_id=10000):

    window = xbmcgui.Window(window_id)

    if clear:

        log('Clear prop: %s' % key)
        window.clearProperty(key.replace('.json', '').replace('.bool', ''))

    elif value is not None:

        if key.endswith('.json'):

            key = key.replace('.json', '')
            value = json.dumps(value)

        elif key.endswith('.bool'):

            key = key.replace('.bool', '')
            value = 'true' if value else 'false'

        window.setProperty(key, value)

    else:

        result = window.getProperty(key.replace('.json', '').replace('.bool', ''))

        if result:
            if key.endswith('.json'):
                result = json.loads(result)
            elif key.endswith('.bool'):
                result = result in ('true', '1')

        return result


def get_channeldetails(channel_name):

    channel_details = {}

    channels = json_call('PVR.GetChannels',
                properties=['channel', 'uniqueid', 'icon', 'thumbnail'],
                params={'channelgroupid': 'alltv'},
                )

    try:
        for channel in channels['result']['channels']:
            if channel['channel'] == channel_name:
                channel_details['channelid'] = channel['channelid']
                channel_details['channel'] = channel['channel']
                channel_details['icon'] = channel['icon']
                break
    except Exception:
        return

    return channel_details



def json_call(method,properties=None,sort=None,query_filter=None,limit=None,params=None,item=None):

    json_string = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}

    if properties is not None:
        json_string['params']['properties'] = properties

    if limit is not None:
        json_string['params']['limits'] = {'start': 0, 'end': limit}

    if sort is not None:
        json_string['params']['sort'] = sort

    if query_filter is not None:
        json_string['params']['filter'] = query_filter

    if item is not None:
        json_string['params']['item'] = item

    if params is not None:
        json_string['params'].update(params)

    json_string = simplejson.dumps(json_string)

    result = xbmc.executeJSONRPC(json_string)
    result = unicode(result, 'utf-8', errors='ignore')
    result = simplejson.loads(result)

    #log('json-string: %s' % json_string, 'warning')
    #log('json-result: %s' % result, 'warning')

    return result


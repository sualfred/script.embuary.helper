#!/usr/bin/python
#Based on script.toolbox by phil65 - https://github.com/phil65/script.toolbox/

#################################################################################################

from __future__ import division

import xbmc
import xbmcaddon
import xbmcvfs
import os
from PIL import ImageFilter,Image,ImageOps

''' Python 2<->3 compatibility
'''
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

from resources.lib.helper import *

#################################################################################################

BLUR_CONTAINER = xbmc.getInfoLabel('Skin.String(BlurContainer)') or 100000
BLUR_RADIUS = xbmc.getInfoLabel('Skin.String(BlurRadius)') or ADDON.getSetting('blur_radius')
OLD_IMAGE = ''

#################################################################################################


''' create imgage storage folders
'''
if not os.path.exists(ADDON_DATA_IMG_PATH):
    os.makedirs(ADDON_DATA_IMG_PATH)

if not os.path.exists(ADDON_DATA_IMG_TEMP_PATH):
    os.makedirs(ADDON_DATA_IMG_TEMP_PATH)


''' blur image and store result in addon data folder
'''
def image_blur(prop='listitem',file=None,radius=BLUR_RADIUS):
    global OLD_IMAGE
    image = file if file is not None else xbmc.getInfoLabel('Control.GetLabel(%s)' % BLUR_CONTAINER)

    try:
        radius = int(radius)
    except ValueError:
        log('No valid radius defined for blurring')
        return

    if image:
        if image == OLD_IMAGE:
            log('Image blurring: Image has not changed. Skip %s.' % image, DEBUG)
        else:
            log('Image blurring: Image changed. Blur %s.' % image, DEBUG)
            OLD_IMAGE = image

            filename = md5hash(image) + str(radius) + '.png'
            targetfile = os.path.join(ADDON_DATA_IMG_PATH, filename)

            if not xbmcvfs.exists(targetfile):
                img = _getimgcache(image,ADDON_DATA_IMG_PATH,filename)

                if img:
                    img = Image.open(img)
                    img.thumbnail((200, 200), Image.ANTIALIAS)
                    img = img.convert('RGB')
                    img = img.filter(ImageFilter.GaussianBlur(radius))
                    img.save(targetfile)

            else:
                log('Blurred img already created: ' + targetfile, DEBUG)
                img = Image.open(targetfile)

            if img:
                imagecolor = _imgcolors(img)
                winprop(prop + '_blurred', targetfile)
                winprop(prop + '_color', imagecolor)
                winprop(prop + '_color_noalpha', imagecolor[2:])


''' get image dimension and aspect ratio
'''
def image_info(image):
    width, height, ar = '', '', ''

    if image:
        filename = 'tmp_' + md5hash(image) + '.jpg'
        img = _getimgcache(image,ADDON_DATA_IMG_TEMP_PATH,filename)

        if img:
            img = Image.open(img)
            width,height = img.size
            ar = round(width / height,2)

        _deltemp()

    return width, height, ar


''' generate genre thumb and store result in addon data folder
'''
def create_genre_thumb(genre,images):
    filename = genre + '_' + md5hash(images) + '.jpg'
    genre_thumb = os.path.join(ADDON_DATA_IMG_PATH, filename)

    if not xbmcvfs.exists(genre_thumb):
        width, height = 356, 533
        cols, rows = 2, 2
        thumbnail_width = int(width / cols)
        thumbnail_height = int(height / rows)
        size = thumbnail_width, thumbnail_height

        ''' get real file names and move to temp if image has not been cached yet
        '''
        posters = list()
        for poster in images:
            posterfile = images.get(poster)
            temp_filename = genre + '_' + md5hash(posterfile) + '.jpg'
            image = _getimgcache(posterfile,ADDON_DATA_IMG_TEMP_PATH,temp_filename)

            if image:
                posters.append(image)

        if not posters:
            return ''

        ''' create collage
        '''
        collage = Image.new('RGB', (width, height), (19,19,19))
        collage_images = []
        for poster in posters:
            try:
                image = Image.open(xbmc.translatePath(poster))
                image = ImageOps.fit(image, (size), method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5))
                collage_images.append(image)
            except Exception:
                pass

        i, x, y = 0, 0 ,0
        for row in range(rows):
            for col in range(cols):
                try:
                    collage.paste(collage_images[i],(int(x), int(y)))
                except Exception:
                    pass
                i += 1
                x += thumbnail_width
            y += thumbnail_height
            x = 0

        collage.save(genre_thumb,optimize=True,quality=85)
        _deltemp()

    return xbmc.translatePath(genre_thumb)


''' get cached images or copy to temp if file has not been cached yet
'''
def _getimgcache(image,targetpath,filename):
    cachedthumb = xbmc.getCacheThumbName(image)
    vid_cachefile = os.path.join('special://profile/Thumbnails/Video', cachedthumb[0], cachedthumb)
    cachefile_jpg = os.path.join('special://profile/Thumbnails/', cachedthumb[0], cachedthumb[:-4] + '.jpg')
    cachefile_png = os.path.join('special://profile/Thumbnails/', cachedthumb[0], cachedthumb[:-4] + '.png')
    targetfile = os.path.join(targetpath, filename)
    img = None

    for i in range(1, 4):
        try:
            if xbmcvfs.exists(cachefile_jpg):
                img = cachefile_jpg
                log('Get cached file ' + cachefile_jpg, DEBUG)
                break
            elif xbmcvfs.exists(cachefile_png):
                img = cachefile_png
                log('Get cached file ' + cachefile_png, DEBUG)
                break
            elif xbmcvfs.exists(vid_cachefile):
                log('Get cache video file ' + vid_cachefile)
                img = vid_cachefile
                break
            else:
                image = urllib.unquote(image.replace('image://', ''))
                if image.endswith('/'):
                    image = image[:-1]
                log('Copy image from source: ' + image, DEBUG)
                xbmcvfs.copy(image, targetfile)
                img = targetfile
                break
        except Exception as error:
            log('Could not get image for %s (try %i)' % (image, i))
            log(error)
            xbmc.sleep(500)

    img = xbmc.translatePath(img) if img else ''
    return img


''' get average image color
'''
def _imgcolors(img):
    width, height = img.size
    imagecolor = 'FFF0F0F0'

    try:
        pixels = img.load()

        data = []
        for x in range(width / 2):
            for y in range(height / 2):
                cpixel = pixels[x * 2, y * 2]
                data.append(cpixel)

        counter, r, g, b = 0, 0, 0, 0
        for x in range(len(data)):
            brightness = data[x][0] + data[x][1] + data[x][2]
            if brightness > 150 and brightness < 720:
                r += data[x][0]
                g += data[x][1]
                b += data[x][2]
                counter += 1

        if counter > 0:
            rAvg = int(r / counter)
            gAvg = int(g / counter)
            bAvg = int(b / counter)
            Avg = (rAvg + gAvg + bAvg) / 3
            minBrightness = 130

            if Avg < minBrightness:
                Diff = minBrightness - Avg

                if rAvg <= (255 - Diff):
                    rAvg += Diff
                else:
                    rAvg = 255
                if gAvg <= (255 - Diff):
                    gAvg += Diff
                else:
                    gAvg = 255
                if bAvg <= (255 - Diff):
                    bAvg += Diff
                else:
                    bAvg = 255

            imagecolor = 'FF%s%s%s' % (format(rAvg, '02x'), format(gAvg, '02x'), format(bAvg, '02x'))
            log('Average color: ' + imagecolor, DEBUG)

        else:
            raise Exception

    except Exception:
        log('Use fallback average color: ' + imagecolor, DEBUG)
        pass

    return imagecolor


''' clean temporary copied files
'''
def _deltemp():
    tempdirs, tempfiles = xbmcvfs.listdir(ADDON_DATA_IMG_TEMP_PATH)
    for file in tempfiles:
        xbmcvfs.delete(os.path.join(ADDON_DATA_IMG_TEMP_PATH, file))
## The background service
This script is running different tasks to communicate to functions on events or give features to the Embuary skin.
Some of this things are might be useful to be used on other skins as well.

Note: The background and player monitor services can be disabled in the add-on settings.

## Restarting the service
Some features, like the background blurring daemon, require a service restart after they were enabled.
This can easily be done by calling:

`RunScript(script.embuary.helper,action=restartservice)`

## Global random background images
The script is calling the database in a interval to get a random set of 40 movie, 40 TV show and 40 artist fanarts. These background images are going to be stored in window propertyies, which are changing every 10s. 

**Available properties**
* `$INFO[Window(home).Property(EmbuaryBackground)]` (mix of all)
* `$INFO[Window(home).Property(EmbuaryBackgroundVideos)]` (mix of movies + TV shows)
* `$INFO[Window(home).Property(EmbuaryBackgroundMovies)]` (movies)
* `$INFO[Window(home).Property(EmbuaryBackgroundTVShows)]` (TV shows)
* `$INFO[Window(home).Property(EmbuaryBackgroundMusic)]` (artists)

**Note:** The 10s interval can be adjusted in the addon config and skinners also can override this value by using a skin setting, eg:

`Skin.String(BackgroundInterval,40)`

## Simple focus monitor
Some skinners may want splitted ListItem values to use them for resource addons. The service has implemented a simple focus monitor to get this job done for you, but it's disabled by default (expensive and slow).

**Enable the focus monitor** (service restart required)

`<onload condition="!Skin.HasSetting(FocusMonitor)">Skin.ToggleSetting(FocusMonitor)</onload>`

**Following info labels are supported:**

* ListItem.Genre
* ListItem.Studio
* ListItem.Country
* ListItem.Director
* ListItem.Cast

**Example**

`$INFO[ListItem.Genre] = "Action / Crime / Drama"`

**Result**
* $INFO[Window(home).Property(Genre.0) = "Action"
* $INFO[Window(home).Property(Genre.1) = "Crime "
* $INFO[Window(home).Property(Genre.2) = "Drama"

Note: It's also available as [script command](https://github.com/sualfred/script.embuary.helper/wiki/Script:-Actions-and-helpers#set--update-library-info-value-via-json)

## Auto playlist clearing
Kodi has a stupid bug with dynamic content containers. All widgets, or PlayMedia commands, are using the music playlist no matter if the item that is going to be played is a music or video item. It's a corner case issue, but skinners are having troubles to open the correct playlist window because this behaviour can lead into a filled music and video playlist. That means we have no option to check what is the correct and currently used one.

The background service offers the option to get rid of this issue by clearing the old existing playlist by listening to the playlist.onadd event. That means a existing video playlist is going to be cleared if a item is going to be added to the music playlist. 

This "helper" is disabled by default and has to be enabled.

**Enable the playlist monitor**

`<onload condition="!Skin.HasSetting(ClearPlaylist)">Skin.ToggleSetting(ClearPlaylist)</onload>`

## Kodi user profile and master lock issues
The Kodi profile system isn't in a good shape and never was. Since Kodi 18 it's even worse and it's possible that wrong content is displayed or the GUI is messed up completely (missing labels etc). 

As workaround the service monitors some login / master mode stuff to reload the skin to get rid of the most issues. This feature cannot be disabled.

## Auto refresh widgets
Useful to refresh dynamic widget containers. The service is providing a refresh interval to a window property after:
* a library item has been updated
* every 10 minutes

Just add `&reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)` to the end of a content path.

**Simple example**

`<content>plugin://script.embuary.helper/?info=getinprogress&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]</content>`

## Player audio track detection
The service checks the playing item for all available audio languages. Useful for skinners who want to show a "change audiotrack" button if more than 1 track is available.

**Example**

```
<control type="button" id="614">
<onclick>action(AudioNextLanguage)</onclick>
<visible>!String.IsEmpty(Window(home).Property(EmbuaryPlayerAudioTracks))</visible>
<visible>!String.IsEmpty(VideoPlayer.AudioLanguage)</visible>
<visible>!VideoPlayer.Content(musicvideos)</visible>
</control>
```

## Player audio and subtitle info labels
All VideoPlayer.Audio* info values of Kodi only return the current active track. There is no builtin way to get the additional available ones. The service will call a database query on playback start and adds the result to window properties.

**Result** (%i = 0,1,2,3,4, etc)

* Window(home).Property(AudioCodec.%i)
* Window(home).Property(AudioChannels.%i)
* Window(home).Property(AudioLanguage.%i)
* Window(home).Property(SubtitleLanguage.%i)

## Get the channel logo for the current playing recording
There is no Kodi builtin way to get the channel logo of a playing recording, if it has a EPG thumb stored.
The service tries to find the correct channel logo by the channel name and fills it to a window property.

**Example**

`<texture>$INFO[Window(home).Property(Player.ChannelLogo)]</texture>`

## Get artist and album artworks for music playback
The script automatically adds artworks to the currently playing song if some of them are missing (like discart of the album). This is usually the case if the a song is going to be played from a widget outside of the music database.
This is happen automatically and needs no further implementation.

## Auto fullscreen on playback
This feature forces Kodi to switch to fullscreen when playback is going to be started. It's disabled by default.

**Enable/disable auto fullscreen**

`Skin.ToggleSetting(StartPlayerFullscreen)`

## Next item of video playlist
There is no Kodi builtin to get information about the next queued playlist item of the video player. This monitor gets rid of this issue and stores nearly all available info labels as window property. The info labels get fetched automatically and there is no need to activate this feature.

**Available properties (if information exists)**
* Window(home).Property(VideoPlayer.Next.Title)
* Window(home).Property(VideoPlayer.Next.TVShowTitle)
* Window(home).Property(VideoPlayer.Next.Season)
* Window(home).Property(VideoPlayer.Next.Episode)
* Window(home).Property(VideoPlayer.Next.Tagline)
* Window(home).Property(VideoPlayer.Next.Rating)
* Window(home).Property(VideoPlayer.Next.UserRating)
* Window(home).Property(VideoPlayer.Next.Duration) _returns HH:MM:SS_
* Window(home).Property(VideoPlayer.Next.Duration(m)) _returns minutes_
* Window(home).Property(VideoPlayer.Next.Duration(s)) _returns seconds_
* Window(home).Property(VideoPlayer.Next.DBType)
* Window(home).Property(VideoPlayer.Next.DBID)
* Window(home).Property(VideoPlayer.Next.Year)
* Window(home).Property(VideoPlayer.Next.Art(thumb))
* Window(home).Property(VideoPlayer.Next.Art(fanart))
* Window(home).Property(VideoPlayer.Next.Art(poster))
* Window(home).Property(VideoPlayer.Next.Art(tvshow.poster))
* Window(home).Property(VideoPlayer.Next.Art(clearart))
* Window(home).Property(VideoPlayer.Next.Art(tvshow.clearart))
* Window(home).Property(VideoPlayer.Next.Art(landscape))
* Window(home).Property(VideoPlayer.Next.Art(tvshow.landscape))
* Window(home).Property(VideoPlayer.Next.Art(clearlogo))
* Window(home).Property(VideoPlayer.Next.Art(tvshow.clearlogo))
* Window(home).Property(VideoPlayer.Next.Art(banner))
* Window(home).Property(VideoPlayer.Next.Art(tvshow.banner))

## Player artwork dimension and aspect ratio
Stores width, height and aspect ratio of the most common player artwork info labels in window properties.

**Available properties**
* `$INFO[Window(home).Property(Player.Icon.width)]` (width)
* `$INFO[Window(home).Property(Player.Icon.height)]` (height)
* `$INFO[Window(home).Property(Player.Icon.ar)]` (aspect ratio)
* `$INFO[Window(home).Property(Player.Art(poster).width)]` (width)
* `$INFO[Window(home).Property(Player.Art(poster).height)]` (height)
* `$INFO[Window(home).Property(Player.Art(poster).ar)]` (aspect ratio)
* `$INFO[Window(home).Property(Player.Art(tvshow.poster).width)]` (width)
* `$INFO[Window(home).Property(Player.Art(tvshow.poster).height)]` (height)
* `$INFO[Window(home).Property(Player.Art(tvshow.poster).ar)]` (aspect ratio)
* `$INFO[Window(home).Property(Pvr.EPGEventIcon.width)]` (width)
* `$INFO[Window(home).Property(Pvr.EPGEventIcon.height)]` (height)
* `$INFO[Window(home).Property(Pvr.EPGEventIcon.ar)]` (aspect ratio)
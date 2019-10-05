## Get cast
Example 1

`plugin://script.embuary.helper?info=getcast&type=tvshow&title='$ESCINFO[VideoPlayer.TVShowTitle]'`

Example 2

`plugin://script.embuary.helper?info=getcast&type=movie&dbid=$INFO[ListItem.DBID]`

Example 3

`plugin://script.embuary.helper?info=getcast&type=tvshow&dbid=$INFO[ListItem.DBID]&idtype=episode'`

**Explanation**
* title / dbid = one of them is required
* type = required (tvshow or movie)
* idtype = optional (season or episode -> calls TV show data by season or episode id)

Returns the cast of a item. The listing has no <onclick> command set so skinners can use what ever they want by adding their own commands to the list container.

## Get resource addon images by string
Example 1

`plugin://script.embuary.helper/?info=getresourceimages&addon=resource.images.actorart&string='$ESCINFO[ListItem.Cast]''`

Example 2

`plugin://script.embuary.helper/?info=getresourceimages&addon=resource.images.studios.white&separator='" / "'&string='$ESCINFO[ListItem.Studio]'`

**Explanation**
* addon = required, the resource addon that should be used
* string = required, the string that needs to be splitted (eg: ListItem.Cast, ListItem.Genre, ListItem.Country, etc.)
* separator = optional, by default it is splitting by line

Crawls all available resource images (.png), then splits the provided string and after that it's going to add all available resources images as ListItem. If no resource image is available for a string value, it will be skipped.

**ListItem values**
* ListItem.Label = splitted value of the string (eg "Paul Walker")
* ListItem.Icon = image path (eg "resource://resource.images.actorart/Paul Walker.png")

## Get item details by DBID
Example

`plugin://script.embuary.helper/?info=getbydbid&dbid=$INFO[ListItem.DBID]&type=$INFO[ListItem.DBType]`

Returns a list with only 1 item (the current focused one). Used for skin hacks to easily get properties like ListItem.Property(Genre.0) or ListItem.Property(Country.1) via a hidden list container.

Also useful if you want to get ListItem.Rating(foo), because Kodi only returns them in the info dialog.

## Parse own JSON calls to the script
Example

`plugin://script.embuary.helper/?info=getbyargs&filter_args='"{"field": "playcount", "operator": "lessthan", "value": "1"}"'&sort_args='"{"order": "ascending", "method": "title"}"'&tag=HDR&type=movie`

**Important**

Depending on the JSON construct it's possible required to URL encode the request but to keep $INFO[] stuff as it is. Example:

`plugin://script.embuary.helper/?info=getbyargs&amp;filter_args=%7B%22and%22%3A%20%5B%7B%22or%22%3A%20%5B%7B%22operator%22%3A%20%22is%22%2C%20%22field%22%3A%20%22actor%22%2C%20%22value%22%3A%20%22$INFO[Container(200).ListItem.Label]%22%7D%2C%7B%22operator%22%3A%20%22is%22%2C%20%22field%22%3A%20%22actor%22%2C%20%22value%22%3A%20%22$INFO[Container(200).ListItem(1).Label]%22%7D%2C%7B%22operator%22%3A%20%22is%22%2C%20%22field%22%3A%20%22actor%22%2C%20%22value%22%3A%20%22$INFO[Container(200).ListItem(2).Label]%22%7D%5D%7D%2C%20%7B%22operator%22%3A%20%22isnot%22%2C%20%22field%22%3A%20%22title%22%2C%20%22value%22%3A%20%22$INFO[ListItem.Label]%22%7D%5D%7D&amp;type=movie`

[www.urldecoder.org](https://www.urldecoder.org/) is your best friend for this case.

**Explanation**
* {} = See https://kodi.wiki/view/JSON-RPC_API/v9 for reference.
* filter_args = required
* type  = required (movie,tvshow,episode)
* sort_args = optional
* limit = optional
* tag = optional, additional filter option to filter by library tag 

Parse own JSON calls to return a listing.

## Seasonal widgets
Example 1

`plugin://script.embuary.helper/?info=getseasonal&amp;list=horror&limit=15`

Example 2

`plugin://script.embuary.helper/?info=getseasonal&amp;list=horror&type=movie`

**Explanation**
* list = required, possible values: 'horror','starwars','startrek','xmas'
* limit = optional (eg 'limit=15' -> if no 'type' is provided it will return 15 movies and 15 shows)
* type = optional

By default it returns a mix of matching items to your "season". So it's possible that a listing contains movies, shows or episodes at the same time.

## Jump to letter
Example

`plugin://script.embuary.helper/?info=jumptoletter&amp;showall=false&amp;reload=$INFO[Container.NumItems]`

**Explanation**
* reload = required
* showall = optional

Returns the alphabet to quickly jump to a position of the container (#,A-Z). # represents the beginning of the container and depending on the sort direction it will jump to the first or last page of the listing.

By providing `showall=false` it will only display items that are really available.

Note: The visiblity is controlled by a skin. So it's recommended to only display the container if the container sortmethod supports it. See example below.

**Implementation example**

```
<control type="panel" id="123">
<visible>[[Container.HasNext | Container.HasPrevious] + [[Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(artists) | Container.Content(albums) | Container.Content(addons)] + [String.IsEqual(Container.SortMethod,$LOCALIZE[551]) | String.IsEqual(Container.SortMethod,$LOCALIZE[561]) | String.IsEqual(Container.SortMethod,$LOCALIZE[558]) | String.IsEqual(Container.SortMethod,$LOCALIZE[557]) | String.IsEqual(Container.SortMethod,$LOCALIZE[556])]]]</visible>
<itemlayout height="45" width="34"/>
<focusedlayoutheight="45" width="34"/>
<content>plugin://script.embuary.helper/?info=jumptoletter&amp;showall=false&amp;reload=$INFO[Container.NumItems]</content>
</control>
```
## Get path statistics
Example 1 (skinshortcuts or any other node based on another container)

`plugin://script.embuary.helper/?info=getpathstats&amp;path=$INFO[Container(100).ListItem.Property(path)]&amp;prefix=test'`

Example 2 (hardcoded path)

`plugin://script.embuary.helper/?info=getpathstats&amp;path='"special://profile/playlists/video/myplaylist.xsp"'&amp;prefix=test'`

**Explanation**
* path = video item path (playlist, library node, etc)
* prefix = optional (default is "Stats")

Doesn't really return widget items, but sets window properties with stats of the provided path. Useful if you want to provide some stats for nerds on your home screen based on the focused main menu item that links to a video library or playlist.

**Filled window properties**
* Window(Home).Property(test_watched)
* Window(Home).Property(test_count)
* Window(Home).Property(test_TVShowCount)
* Window(Home).Property(test_InProgress)
* Window(Home).Property(test_Unwatched)
* Window(Home).Property(test_Episodes)
* Window(Home).Property(test_WatchedEpisodes)
* Window(Home).Property(test_UnwatchedEpisodes)



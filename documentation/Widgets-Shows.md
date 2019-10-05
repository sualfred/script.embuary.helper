## Get in progress episodes
Example

`plugin://script.embuary.helper/?info=getinprogress&type=tvshow&tag=HDR`

**Explanation**
* type = required
* tag = optional, additional filter option to filter by library tag 

Returns in progress items.

## Get next up episode
Example

`plugin://script.embuary.helper/?info=getnextup&tag=HDR`

**Explanation**
* tag = optional, additional filter option to filter by library tag 

## Get recently updated TV shows

**Based on partly or unwatched shows**

`plugin://script.embuary.helper/?info=getnewshows&tag=HDR`

Recently added episodes based on unwatched or in progress shows. Episodes will be grouped if more than one unwatched episode is available.

**Based on all shows and date added**

`plugin://script.embuary.helper/?info=getnewshows&showall=true&tag=HDR`

All recently added episodes. Watched state is ignored and only items added of the same date will be grouped.

**Explanation**
* tag = optional, additional filter option to filter by library tag 
* showall = optional, true or false (default)

**Attention**
This widget returns a listing with mixed episodes and TV show items. Use ListItem.DBType to layout them differently.

## Get suggestions based on a watched TV show
Example

`plugin://script.embuary.helper/?info=getsimilar&type=tvshow&pos=0&tag=HDR`

**Explanation**
* type = required
* pos = optional, will return the result of the most recent watched item (starts with "0")
* tag = optional, additional filter option to filter by library tag 

**Available item properties**
* ListItem.Property(searchstring) = Item that was used for the query

Picks up to 2 random genres of a random watched item and returns similar items of your library.

## Get similar items based on TV show
Example

`plugin://script.embuary.helper/?info=getsimilar&dbid=$INFO[ListItem.DBID]&type=tvshow&tag=HDR`

**Explanation**
* dbid = required
* type = required
* tag = optional, additional filter option to filter by library tag 

**Available item properties**
* ListItem.Property(searchstring) = TV show that was used for the query

Picks up to 2 random genres of the item and returns similar items of your library.

## Get TV shows by random genre
Example

`plugin://script.embuary.helper/?info=getbygenre&unwatched=True&type=tvshow&tag=HDR`

**Explanation**
* type = required
* unwatched = optional (true or false)
* tag = optional, additional filter option to filter by library tag 

Returns suggestions based on a random genre of your library

## Get seasons of TV show
Example 1

`plugin://script.embuary.helper/?info=getseasons&dbid=$INFO[ListItem.DBID]&allseasons=false`

Example 2

`plugin://script.embuary.helper/?info=getseasons&title=$INFO[ListItem.TVShowTitle]&allseasons=false`

Example 3

`plugin://script.embuary.helper/?info=getseasons&dbid=$INFO[ListItem.DBID]&idtype=episode&allseasons=false`

**Explanation**
* dbid or title = one of them is required
* allseasons = false/true, to show or hide the "all seasons" item
* idtype = optional (season or episode -> calls TV show data by season or episode id)

Returns all available season of a TV show

## Get episodes of season
Example 1

`plugin://script.embuary.helper/?info=getseasonepisodes&dbid=$INFO[ListItem.DBID]&season=$INFO[ListItem.Season]`

Example 2

`plugin://script.embuary.helper/?info=getseasonepisodes&title='$ESCINFO[ListItem.TvShowTitle]'&season=$INFO[ListItem.Season]`

Example 3

`plugin://script.embuary.helper/?info=getseasonepisodes&dbid=$INFO[ListItem.DBID]&season=$INFO[ListItem.Season]&idtype=episode`

**Explanation**
* dbid or title = one of them is required
* season= required
* idtype = optional (season or episode -> calls TV show data by season or episode id)

Returns all available episodes of a season.

## Get TV show genres
Example

`plugin://script.embuary.helper/?info=getgenre&type=tvshow`

**Explanation**
* type = required

**Available item properties**
* ListItem.Property(Poster.%i) = random poster of the genre (%i = 0,1,2,3)

Returns all available genres. Each ListItem has 4 posters of each single genre stored as property. If PIL is supported it will create a collage thumb automatically and stores the value in ListItem.Art(thumb).
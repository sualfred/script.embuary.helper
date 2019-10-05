## Get in progress media
Example

`plugin://script.embuary.helper/?info=getinprogress&tag=HDR`

**Explanation**
* tag = optional, additional filter option to filter by library tag 

Returns a mix of in progress movies and shows.

## Get media by random genre
Example

`plugin://script.embuary.helper/?info=getbygenre&unwatched=True&tag=HDR`

**Explanation**
* unwatched = optional (true or false)
* tag = optional, additional filter option to filter by library tag 

Returns movie and show suggestions based on a random genre of your library

## Get more items of random actor

Examples

Movies based on a random actor of DBID item

`plugin://script.embuary.helper/?info=getitemsbyactor&type=tvshow&dbid=$INFO[ListItem.DBID]&content=movie`

Movies and TV shows based on a random actor of DBID item

`plugin://script.embuary.helper/?info=getitemsbyactor&type=tvshow&dbid=$INFO[ListItem.DBID]`

**Explanation**
* dbid = required (the DBID item will be exluded from the results)
* type = required
* content = optional (tvshow or movie)

**Available item properties**
* ListItem.Property(searchstring) = Actor

Picks a random person from the first 4 actor values of the library item (mostly the main cast) and returns other items with this actor. By default the listing contains movies and TV shows.

## Get more items by given actor

Examples

TV shows based on a given actor name excluding a given TV show

`plugin://script.embuary.helper/?info=getitemsbyactor&label=$INFO[Container(50).ListItem.Label]&exclude=$INFO[ListItem.TVShowTitle]&content=tvshow`

Movies and TV shows based on a given actor name

`plugin://script.embuary.helper/?info=getitemsbyactor&label='"Bruce Willis"'`

**Explanation**
* label = required (actor name)
* exclude = optional (exclude a movie or TV show by title)
* content = optional (tvshow or movie)

**Available item properties**
* ListItem.Property(searchstring) = Actor

Uses a given person name and returns other items with this actor. By default the listing contains movies and TV shows.

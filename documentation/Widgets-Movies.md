## Get in progress movies
Example

`plugin://script.embuary.helper/?info=getinprogress&type=movie&tag=HDR`

**Explanation**
* type = required
* tag = optional, additional filter option to filter by library tag 

Returns in progress items.

## Get suggestions based on watched movies
Example

`plugin://script.embuary.helper/?info=getsimilar&type=movie&pos=0&tag=HDR`

**Explanation**
* type = required
* pos = optional, will return the result of the most recent watched item (starts with "0")
* tag = optional, additional filter option to filter by library tag 

**Available item properties**
* ListItem.Property(searchstring) = Item that was used for the query

Picks up to 2 random genres of random watched item and returns similar items of your library.

## Get similar items based on movie
Example

`plugin://script.embuary.helper/?info=getsimilar&dbid=$INFO[ListItem.DBID]&type=movie&tag=HDR`

**Explanation**
* dbid = required
* type = required
* tag = optional, additional filter option to filter by library tag 

**Available item properties**
* ListItem.Property(searchstring) = Movie that was used for the query

Picks up to 2 random genres of the item and returns similar items of your library.

## Get movies by random genre
Example

`plugin://script.embuary.helper/?info=getbygenre&unwatched=True&type=movie&tag=HDR`

**Explanation**
* type = required
* unwatched = optional (true or false)
* tag = optional, additional filter option to filter by library tag 

Returns suggestions based on a random genre of your library

## Get movie genres
Example

`plugin://script.embuary.helper/?info=getgenre&type=movie`

**Explanation**
* type = required

**Available item properties**
* ListItem.Property(Poster.%i) = random poster of the genre (%i = 0,1,2,3)

Returns all available genres. Each ListItem has 4 posters of each single genre stored as property. If PIL is supported it will create a collage thumb automatically and stores the value in ListItem.Art(thumb).

## Get directed by
Example

`plugin://script.embuary.helper/?info=getdirectedby&dbid=$INFO[ListItem.DBID]`

**Explanation**
* dbid = required

**Available item properties**
* ListItem.Property(searchstring) = Director

Returns a list of available movies that are directed by the same directors.
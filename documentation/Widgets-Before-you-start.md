## Refresh widgets
The service part provides a window property to force containers to refresh (see: [auto refresh widgets](https://github.com/sualfred/script.embuary.helper/wiki/Service:-Running-tasks#auto-refresh-widgets))

## Additional properties

**Splitted values**

All movie, TV show and episode listings have special properties available:
* ListItem.Property(Genre.%i)
* ListItem.Property(Studio.%i)
* ListItem.Property(Country.%i)
* ListItem.Property(Director.%i)
* ListItem.Property(Writer.%i)
* ListItem.Property(Cast.%i)

%i = 0, 1, 2 , 3, etc. (max. 30)

**"Widget is based on XYZ"**

Other widgets that are providing information on a single item, like getsimilar, does have a property stored to display the search string:
* ListItem.Property(searchstring)

## Escape special characters
It's highly recommended to escape all info labels that could contain special characters or commas if you are providing them to script. Otherwise it's possible that things are going to break. Just use $ESCINFO[] or  $ESCVAR[] wrapped in a ''.

Example:

`'$ESCINFO[ListItem.Title]'`

## Use the widget listing

I do offer most of all regular widgets as accessable node by accessing the addon via the video addons listing.
It also supports Emby for Kodi so users can simply pick widgets based on the wanted Emby library.

But this requires a good Skin Shortcuts Script integration :)
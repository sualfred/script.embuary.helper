## Go to path

Closes all dialogs and goes to provided path. If a media window is active it updates the window content instead of destroying the window history.

`RunScript(script.embuary.helper,action=goto,path='$ESCINFO[ListItem.Filenameandpath]',target=videos)`

## Play item

Plays item via PlayMedia() but closes all dialogs before.

`RunScript(script.embuary.helper,action=playitem,item='$ESCINFO[ListItem.Filenameandpath]')`

## Play SFX sound

Plays .wav file. Benefit: SFX sounds are not touching the player at all. GUI and player sounds are still hearable even the .wav is played.

`RunScript(script.embuary.helper,action=playsfx,path='"special://skin/extras/holiday/winterintro.wav"')`

## Play all
Plays all content of a container. This is also supported for widgets if a <onclick> command is provided to the widget container.

**Optional arguments**

* `id=` (container ID)
* `method=` (shuffle / fromhere)

**Example: Play all items**

`RunScript(script.embuary.helper,action=playall)`

**Example: Play all items with shuffle enabled**

`RunScript(script.embuary.helper,action=playall,method=shuffle)`

**Example: Play all items from here from a widget with ID 123** (starting from the current focus position)

`RunScript(script.embuary.helper,action=playall,id=123,method=fromhere)`

## Play folder
Plays all content of a TV show or season folder.

**Optional arguments**

* `shuffle=true` (to randomize the playback)

**Example: Play all episodes of a TV show by providing its DBID**

`RunScript(script.embuary.helper,action=playfolder,dbid=$INFO[ListItem.DBID],shuffle=true)`

**Example: Play and shuffle all episodes of a season by providing its season DBID**

`RunScript(script.embuary.helper,action=playfolder,dbid=$INFO[ListItem.DBID],type=season)`

## Play random
Plays a random item of the container or of a widget

**Optional argument**

* `id=` (widget container ID) 

`RunScript(script.embuary.helper,action=playrandom,id=123)`

## Reset container positions

Resets all container positions to 0. Multiple ID's have to be splitted by `||`.

**Optional argument**

* `only=inactive` (only reset position for not focused items)

`RunScript(script.embuary.helper,action=resetposition,container=101||102||103||104||105||106,only=inactive)`

## Browse TV show of active episode

Closes all dialogs and jumps to the root of the TV show with provided DBID.

`RunScript(script.embuary.helper,action=jumptoshow_by_episode,dbid=$INFO[ListItem.DBID])`

## Get TV show details by episode as window property

Useful if you want to get TV show values on season level.

**Returned properties**
* `Window(home).Property(tvshow.dbid)` (TV show DBID)
* `Window(home).Property(tvshow.rating)` (TV show rating)
* `Window(home).Property(tvshow.seasons)` (Total TV show seasons)
* `Window(home).Property(tvshow.episodes)` (Total TV show episodes)
* `Window(home).Property(tvshow.watchedepisodes)` (Total TV show watched episodes)
* `Window(home).Property(tvshow.unwatchedepisodes)` (Total TV show unwatched episodes)

**Example invisible overlay as call on season level**

```
<?xml version="1.0" encoding="UTF-8"?>
<window id="1118" type="dialog">
<visible>Container.Content(seasons) + String.IsEmpty(Container.Pluginname)</visible>
<onload condition="Integer.IsGreater(ListItemAbsolute(0).Season,0) + !String.IsEmpty(Container.ListItemAbsolute(0).DBID)">RunScript(script.embuary.helper,action=details_by_season,dbid=$INFO[Container.ListItemAbsolute(0).DBID])</onload>
<onload condition="Integer.IsGreater(ListItemAbsolute(1).Season,0) + !String.IsEmpty(Container.ListItemAbsolute(1).DBID)">RunScript(script.embuary.helper,action=details_by_season,dbid=$INFO[Container.ListItemAbsolute(1).DBID])</onload>
<onload condition="Integer.IsGreater(ListItemAbsolute(2).Season,0) + !String.IsEmpty(Container.ListItemAbsolute(2).DBID)">RunScript(script.embuary.helper,action=details_by_season,dbid=$INFO[Container.ListItemAbsolute(2).DBID])</onload>
<onload condition="Integer.IsGreater(ListItemAbsolute(3).Season,0) + !String.IsEmpty(Container.ListItemAbsolute(3).DBID)">RunScript(script.embuary.helper,action=details_by_season,dbid=$INFO[Container.ListItemAbsolute(3).DBID])</onload>
<onunload>ClearProperty(tvshow.dbid,home)</onunload>
<onunload>ClearProperty(tvshow.rating,home)</onunload>
<onunload>ClearProperty(tvshow.seasons,home)</onunload>
<onunload>ClearProperty(tvshow.episodes,home)</onunload>
<onunload>ClearProperty(tvshow.watchedepisodes,home)</onunload>
<onunload>ClearProperty(tvshow.unwatchedepisodes,home)</onunload>
<controls/>
</window>
```

## Blur image
Blurs provided image and saves its path to a window property.

**Optional arguments**

* `prop=` (Prefix of the property. Default = "output")
* `radius=` (Blurring strength. Script default is "2", but this can be different if a skin setting has overwritten it.)

**Example**

`RunScript(script.embuary.helper,action=blurimg,file='"special://skin/extras/file.jpg"',prop=MyProp,radius=4)`

**Result**

* `Window(home).Property(MyProp_blurred)` = the image path
* `Window(home).Property(MyProp_color)` = the average color

## Split value
Splits a provided value by the set separator to window properties.

**Arguments**

* `value=` (required)
* `prop=` (required)
* `separator=` (optional, default splitting is done by lines)

**Example**

`RunScript(script.embuary.helper,action=split,value='$ESCINFO[ListItem.Genre]',separator='" / "',prop=MySplit)`

**Result example**

* `Window(home).Property(MySplit.0)`
* `Window(home).Property(MySplit.1)`
* `Window(home).Property(MySplit.2)`

## Check if file exists
Returns `true` if file exists. Otherwise the window property is going to be cleared.

**Arguments**

* `file=` (required)
* `prop=` (optional, default is "FileExists")

**Example**

`RunScript(script.embuary.helper,action=lookforfile,file='"C:\install.log"',prop=MyProp)`

**Result**

`Window(home).Property(MyProp)` = true or empty

## Set / update library info value via JSON
Updates a info value of a stored library item. Please check https://kodi.wiki/view/JSON-RPC_API/v9 for reference.

`RunScript(script.embuary.helper,action=setinfo,dbid=$INFO[ListItem.DBID],type=$INFO[ListItem.DBType],field=playcount,value=0)`

## Get .txt file content

Store content of a .txt file in a window property.

**Example**

`RunScript(script.embuary.helper,action=txtfile,path=special://skin/changelog.txt,header=$LOCALIZE[24036],prop=MyWindowProp)`

**Result**

`Window(home).Property(MyWindowProp)`

## Get system locale

Stores the system locale in short form as windows property. Example results: DE, EN, CN, etc.

`RunScript(script.embuary.helper,action=getlocale)`

**Result**

`Window(home).Property(SystemLocale)`

## Set timer

A more detailed alternative to Kodi's builtin `AlarmClock()` function.

**Example**

`RunScript(script.embuary.helper,action=settimer,do='"Runscript(...)||Notification(header,message)"',time=5000,delay=100,busydialog=false)`

**Arguments**

* `do=` (required, stores the action(s) that should be executed. Multiple actions can be run by adding `||` as separator)
* `time=` (optional, default is 50ms. The amount of time to wait before the actions are going to be executed)
* `delay=` (optional, default is 0ms. Useful if you want to pause between the actions)
* `busydialog=` (optional, default is true. Shows the busydialog before actions are going to be processed)

## Encode / decode string

Encodes/decodes a provided string to a window property.

**Encode**

`RunScript(script.embuary.helper,action=encode,string='"Umlauts & special characters, they always drive me crazy"',prop=MyEncodedString)`

**Decode** 

`RunScript(script.embuary.helper,action=decode,string=Umlauts%20%26%20special%20characters%2C%20they%20always%20drive%20me%20crazy,prop=MyDecodedString)`

**Result**

* `Window(home).Property(MyEncodedString)`
* `Window(home).Property(MyDecodedString)`

**Arguments**
* `string=` (required)
* `prop=` (optional, defaults are `EncodedString` and `DecodedString`)

## Calculate
Performs simple math operations and stores the restult to a property.

**Example**

`RunScript(script.embuary.helper,action=calc,do='"(10 + 5) / 2"',prop=MyResult)`

**Result**

`Window(home).Property(MyResult)` = `7.5`

**Arguments**
* `do=` (math operation wrapped in `'" "'`)
* `prop=` (optional, default is `CalcResult`)

## Get add-on setting
Stores an add-on setting to a window property.

**Example**

`RunScript(script.embuary.helper,action=getaddonsetting,addon=plugin.video.embycon,setting=group_movies)`

**Result**

`Window(home).Property(plugin.video.embycon-group_movies)` = `true`

**Arguments**
* `addon=` (the addon ID)
* `setting=` (the setting - take a look at the settings.xml of the addon in the addon_data folder)

## Image dimension and aspect ratio
Returns width, height and aspect ratio of provided image path.

**Example**

`RunScript(script.embuary.helper,action=imginfo,img=$INFO[ListItem.Icon],prop=MyImage)`

**Result**

* `Window(home).Property(MyImage.width)` = width
* `Window(home).Property(MyImage.height)` = height
* `Window(home).Property(MyImage.ar)` = aspect ratio (eg: 1.78)

**Arguments**
* `img=` (the image)
* `prop=` (optional, default is `img`)


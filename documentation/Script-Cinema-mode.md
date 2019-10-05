## Information
The cinema mode is a simple way (or complex way for skinner newbies) to add trailers and own available intros in the beginning of movie or episode playback. It needs a deeper skin integration and doesn't work out of the box.

**Note:** Intros or trailers, one of them has to be configured!

## Configuration

**Skin.String(IntroPath)**

This skin string has to be filled with a folder path where the intros are stored.

**Skin.String(TrailerCount)**

This skin string has to be filled with the amount of trailers which should be played.

## Calling the cinema mode
There are multiple ways how to add this to the skin. There is no rule to fit everybodies needs. Better skinners love to use skin hacks and workaround it should not be a big deal.

**Calling via <onlick>**

Works for own widget containers or via button in DialogVideo.xml for example.

**Optional arguments**

* `dbid=` (DBID of the movie/episode)
* `type=` (movie or episode)

**Call**

`RunScript(script.embuary.helper,action=playcinema)`

## Calling via context menu

More tricky, because the context menu has no ListItem.foobar values stored. This means we have provide the values somehow. And the context menu plugin method is limited so I highly recommend to do it on skin level. This also gives you the benefit to place the items on top of the list instead on the bottom. 

**Example**

In Embuary I have a invisible button control in my focusedlayout definitions:

```
<control type="list" id="123"
....
<focusedlayout>
<include content="SetPropertyOnFocus">
<param name="id" value="123"/>
</include>
...
</focusedlayout>
<content></content>
</control>
```

The include:

```
<include name="SetPropertyOnFocus">
<control type="button">
<texturefocus></texturefocus>
<texturenofocus></texturenofocus>
<onfocus>ClearProperty(FocusBounce,home)</onfocus>
<onfocus condition="String.IsEqual(Container($PARAM[id]).ListItem.DBType,movie) | String.IsEqual(Container($PARAM[id]).ListItem.DBType,season) | String.IsEqual(Container($PARAM[id]).ListItem.DBType,episode) | String.IsEqual(Container($PARAM[id]).ListItem.DBType,tvshow)">SetProperty(ListItemDBID,$INFO[Container($PARAM[id]).ListItem.DBID],home)</onfocus>
<onfocus condition="String.IsEqual(Container($PARAM[id]).ListItem.DBType,movie) | String.IsEqual(Container($PARAM[id]).ListItem.DBType,season) | String.IsEqual(Container($PARAM[id]).ListItem.DBType,episode) | String.IsEqual(Container($PARAM[id]).ListItem.DBType,tvshow)">SetProperty(ListItemDBType,$INFO[Container($PARAM[id]).ListItem.DBType],home)</onfocus>
<onfocus condition="[!String.IsEqual(Container($PARAM[id]).ListItem.DBType,movie) + !String.IsEqual(Container($PARAM[id]).ListItem.DBType,season) + !String.IsEqual(Container($PARAM[id]).ListItem.DBType,episode) + !String.IsEqual(Container($PARAM[id]).ListItem.DBType,tvshow)] | String.IsEqual(Container($PARAM[id]).ListItem.Label,$LOCALIZE[20366])">ClearProperty(ListItemDBID,home)</onfocus>
<onfocus condition="[!String.IsEqual(Container($PARAM[id]).ListItem.DBType,movie) + !String.IsEqual(Container($PARAM[id]).ListItem.DBType,season) + !String.IsEqual(Container($PARAM[id]).ListItem.DBType,episode) + !String.IsEqual(Container($PARAM[id]).ListItem.DBType,tvshow)] | String.IsEqual(Container($PARAM[id]).ListItem.Label,$LOCALIZE[20366])">ClearProperty(ListItemDBType,home)</onfocus>
</control>
</include>
```

The context menu:
```
<control type="grouplist" id="3">
...
<control type="button" id="1999">
<include content="ContextButton"/>
<label>$LOCALIZE[31326]</label>
<onclick>RunScript(script.embuary.helper,action=playcinema,dbid=$INFO[Window(home).Property(ListItemDBID)],type=$INFO[Window(home).Property(ListItemDBType)])</onclick>
<visible>!String.IsEmpty(Window(home).Property(ListItemDBID)) + [String.IsEqual(Window(home).Property(ListItemDBType),movie) | String.IsEqual(Window(home).Property(ListItemDBType),episode)] + $EXP[CinemaMode]</visible>
<visible>!String.IsEqual(Control.GetLabel(1002),$LOCALIZE[12021]) + String.IsEqual(Control.GetLabel(1001),$LOCALIZE[208])</visible>
</control>
...
</control>
```
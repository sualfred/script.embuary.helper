# script.embuary.helper
Addon for Kodi providing functions to the Embuary skin
________________________________________________________________________________________________________


# Utilities
________________________________________________________________________________________________________
## "Run from home"
```
RunScript(script.embuary.helper,action=playfromhome,item='$ESCINFO[ListItem.Filenameandpath]')
```

Closes all dialogs and goes back to the home window. Once home is active it starts the playback of the provided filename.




# Plugin sources
________________________________________________________________________________________________________
## In progress movies

```
plugin://script.embuary.helper/?info=getinprogress&amp;type=movie&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

________________________________________________________________________________________________________
## In progress episodes

```
plugin://script.embuary.helper/?info=getinprogress&amp;type=tvshow&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

________________________________________________________________________________________________________
## In progress movies and episodes

```
plugin://script.embuary.helper/?info=getinprogress&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

________________________________________________________________________________________________________
## Next up episodes

```
plugin://script.embuary.helper/?info=getnextup&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

Provides a list with the next unwatched episode of inprogress TV shows.
________________________________________________________________________________________________________
## Get episodes from the same season

```
plugin://script.embuary.helper/?info=getseasonepisodes&amp;season=$INFO[ListItem.Season]&amp;title='$ESCINFO[ListItem.TvShowTitle]'&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

Provides a list with all episodes from the same TV show season.

It's also possible to call the listing with the TV show ID if it's available for some reason (Window property for example).

```
plugin://script.embuary.helper/?info=getseasonepisodes&amp;season=$INFO[ListItem.Season]&amp;dbid=$INFO[Window(home).Property(TVShowDBID)&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

________________________________________________________________________________________________________
## Recently updated TV shows (mixed TV shows and episodes)

```
plugin://script.embuary.helper/?info=getnewshows&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

Provides a list with recently updated TV shows. If a show has only one new episode it will be listed as episode to directly start the playback. If more new episodes are available the item will link to the TV show instead.

________________________________________________________________________________________________________
## Genres movies / tvshows

```
plugin://script.embuary.helper/?info=getgenre&amp;type=movie&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

```
plugin://script.embuary.helper/?info=getgenre&amp;type=tvshow&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```
Provides a list of all available genres. Each item has stored 4 of the available movie posters in the genre category:
- ListItem.Art(poster.0)
- ListItem.Art(poster.1)
- ListItem.Art(poster.2)
- ListItem.Art(poster.3)

________________________________________________________________________________________________________
## Get cast for movie / tvshow

By title:
```
plugin://script.embuary.helper?info=getcast&amp;type=tvshow&amp;title='$ESCINFO[ListItem.TVShowTitle]'
```

```
plugin://script.embuary.helper?info=getcast&amp;type=movie&amp;title='$ESCINFO[ListItem.Label]'
```

By DBID
```
plugin://script.embuary.helper?info=getcast&amp;dbid=tvshow&amp;dbid=$INFO[ListItem.DBID]
```

```
plugin://script.embuary.helper?info=getcast&amp;type=movie&amp;dbid=$INFO[ListItem.DBID]
```

Results will have no <onlick> command. You have to use a own <onclick> override for the container to enable an action.

________________________________________________________________________________________________________
## Similar movie (because you watched ...)

Based on a random recently watched item:
```
plugin://script.embuary.helper/?info=getsimilar&amp;type=movie&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```
Available ListItem property
- ListItem.Property(similartitle) = Returns the used movie to create headings like "Because you watched '2 Guns'"

Based on a DBID
```
plugin://script.embuary.helper/?info=getsimilar&amp;type=movie&amp;dbid=$INFO[ListItem.DBID]&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```

________________________________________________________________________________________________________
## Similar TV show (because you watched ...)

Based on a random recently watched TV show (inprogress or completely watched):
```
plugin://script.embuary.helper/?info=getsimilar&amp;type=tvshow&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```
Available ListItem property
- ListItem.Property(similartitle) = Returns the used movie to create headings like "Because you watched 'Breaking Bad'"

Based on a DBID
```
plugin://script.embuary.helper/?info=getsimilar&amp;type=tvshow&amp;dbid=$INFO[ListItem.DBID]&amp;reload=$INFO[Window(home).Property(EmbuaryWidgetUpdate)]
```
Available window properties if the container was placed inside of DialogVideoInfo.xml and a item was called (useful if you want TV show info labels which aren't available on season level):
- Window(home).Property(TVShowDBID)
- Window(home).Property(TVShowRating)
- Window(home).Property(TVShowYear)
- Window(home).Property(TVShowTotalSeasons)
- Window(home).Property(TVShowTotalEpisodes)

________________________________________________________________________________________________________
## Jump to letter

```
plugin://script.embuary.helper/?info=jumptoletter&amp;reload=$INFO[Container.NumItems]
````

Provides a list to jump directly to a item inside of list in the media windows.

Available ListItem properties:
- ListItem.Property(NotAvailable)
- ListItem.Property(IsNumber)

Example implementation:
```

<itemlayout height="35" width="45">
	<control type="group">
		<visible>!String.IsEqual(ListItem.Label,Container.ListItem.SortLetter) + !String.IsEqual(ListItem.Property(IsNumber),Container.ListItem.SortLetter)</visible>
		<control type="textbox">
			<width>40</width>
			<height>40</height>
			<font>JumpToLetter</font>
			<align>center</align>
			<aligny>center</aligny>
			<textcolor>text_sublabel</textcolor>
			<label>$INFO[ListItem.Label]</label>
			<visible>String.IsEmpty(ListItem.Property(NotAvailable))</visible>
		</control>
		<control type="textbox">
			<width>40</width>
			<height>40</height>
			<font>JumpToLetter</font>
			<align>center</align>
			<aligny>center</aligny>
			<textcolor>disabled</textcolor>
			<label>$INFO[ListItem.Label]</label>
			<visible>!String.IsEmpty(ListItem.Property(NotAvailable))</visible>
		</control>
	</control>
	<control type="textbox">
		<width>40</width>
		<height>40</height>
		<font>JumpToLetter</font>
		<align>center</align>
		<aligny>center</aligny>
		<textcolor>white</textcolor>
		<label>$INFO[ListItem.Label]</label>
		<visible>String.IsEqual(ListItem.Label,Container.ListItem.SortLetter) | String.IsEqual(ListItem.Property(IsNumber),Container.ListItem.SortLetter)</visible>
	</control>
</itemlayout>
<focusedlayout height="35" width="45">
	<control type="group">
		<visible>!Control.HasFocus($PARAM[id])</visible>
		<control type="group">
			<visible>!String.IsEqual(ListItem.Label,Container.ListItem.SortLetter) + !String.IsEqual(ListItem.Property(IsNumber),Container.ListItem.SortLetter)</visible>
			<control type="textbox">
				<width>40</width>
				<height>40</height>
				<font>JumpToLetter</font>
				<align>center</align>
				<aligny>center</aligny>
				<textcolor>text_sublabel</textcolor>
				<label>$INFO[ListItem.Label]</label>
				<visible>String.IsEmpty(ListItem.Property(NotAvailable))</visible>
			</control>
			<control type="textbox">
				<width>40</width>
				<height>40</height>
				<font>JumpToLetter</font>
				<align>center</align>
				<aligny>center</aligny>
				<textcolor>disabled</textcolor>
				<label>$INFO[ListItem.Label]</label>
				<visible>!String.IsEmpty(ListItem.Property(NotAvailable))</visible>
			</control>
		</control>
		<control type="textbox">
			<width>40</width>
			<height>40</height>
			<font>JumpToLetter</font>
			<align>center</align>
			<aligny>center</aligny>
			<textcolor>white</textcolor>
			<label>$INFO[ListItem.Label]</label>
			<visible>String.IsEqual(ListItem.Label,Container.ListItem.SortLetter) | String.IsEqual(ListItem.Property(IsNumber),Container.ListItem.SortLetter)</visible>
		</control>
	</control>
	<control type="group">
		<visible>Control.HasFocus($PARAM[id])</visible>
		<control type="image">
			<left>-5</left>
			<width>51</width>
			<height>51</height>
			<texture border="20,20,20,20" colordiffuse="accent">items/focus.png</texture>
			<visible>Control.HasFocus($PARAM[id])</visible>
		</control>
		<control type="textbox">
			<width>40</width>
			<height>40</height>
			<font>JumpToLetter</font>
			<align>center</align>
			<aligny>center</aligny>
			<textcolor>white</textcolor>
			<label>$INFO[ListItem.Label]</label>
		</control>
	</control>
</focusedlayout>
```

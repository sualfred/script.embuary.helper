# script.embuary.helper
Addon for Kodi providing functions to the Embuary skin
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

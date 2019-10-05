## Before you start
The service part of this script supports realtime blurring of background images. This feature is very expensive because each image gets "downloaded" as copy, shrinked, processed and stored in the userdata folder with a minimal filesize. Depending on the database size this folder can grow bigger than expected after while. But don't worry, each file is just a few kilobyte.
Once the image is already blurred it doesn't get updated again (if you don't change the blurring radius). So you won't see any speed penalties after it. I highly reccomend to not use this feature with lemon devices like a Raspberry Pi 1-3.

Note: Blurring a image is also available as [script command](https://github.com/sualfred/script.embuary.helper/wiki/Script:-Actions-and-helpers#blur-image)

## How it works
The service is calling the texture path of a image control every 1s in a endless loop. The processed image path is going to be stored in a window property. This property can be used to display the background image. 

Just keep in mind that this "root" image control has to be available in all windows with the same ID. 
For a more detailed example please check the end of this wiki page.

## Enable blurring daemon
Add this to startup.xml or home.xml  (or somewhere where it makes sense and gets set)

```
<onload condition="!Skin.HasSetting(BlurEnabled)">Skin.ToggleSetting(BlurEnabled)</onload>		
<onload condition="!Skin.HasSetting(BlurEnabled)">RunScript(script.embuary.helper,action=restartservice)</onload>
```

After that following window properties will be filled:
* Window(home).property(listitem_blurred) = The path to the blurred image
* Window(home).property(listitem_color) = The average color of the blurred image

## Optional configuration

**Important: 
Changing the default config requires a daemon restart! Otherwise the changes will not do anything until Kodi is going to be restarted**

`RunScript(script.embuary.helper,action=restartservice)`

**Default image control**

By default the script is looking for a image control with the ID "100000". This value can be changed by skinners.

**Example**

`Skin.String(BlurContainer,1234)`

**Blurring strength**

The default config processes the images with a blurring radius of 2. If a softer or heavier blurring is wanted it can be changed by setting a own value to a skin setting. I suggest values between 1-10.

**Example**

`Skin.String(BlurRadius,5)`

## A very simplified implementation example

The variable that is controlling the background image source:
```
<variable name="TheBackgroundImage">
<value condition="Window.IsVisible(MyVideoNav.xml) + !String.IsEmpty(ListItem.Art(fanart)">$INFO[ListItem.Art(fanart)]</value>
<value>$INFO[Window(home).Property(EmbuaryBackground)]</value>
</variable>
```

The background image control that is placed in all windows:
```
<control type="image" id="100000">
<left>-3000</left>
<top>-3000</right>
<width>10</width>
<height>10</width>
<texture background="true">$VAR[TheBackgroundImage]</texture>
</control>

<control type="image">
<width>1920</width>
<height>1080</height>
<colordiffuse>$INFO[Window(home).Property(listitem_color)]</colordiffuse>
<texture>$INFO[Window(home).Property(listitem_blurred)]</texture>
</control>
```






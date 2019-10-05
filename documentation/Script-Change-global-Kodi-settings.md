# ATTENTION AND WARNING
**Changing global settings affects all skins! You never should do this without the users permssions or without letting the user know!**

In Embuary I've added a simple YES/NO dialog and I inform the users that I highly recommend to change a list of settings to get the best experience in Embuary. So the user has the option to disagree.

![](https://i.ibb.co/4mH2sh4/embuary-startup.jpg)

## Auto font change based on locales
Fonts are a pita for Kodi. For skinners and users. It's nearly impossible to find a font that covers all letters for all languages so most skins are using Arial (or another font) as fallback. But from a Asian user point of view it is bad, because he has to manually change the font set to Arial. Seeing no labels or only garbage symbols makes it more than hard to find the correct button in the skin. 

Solution: Automatically do it for the users based on the locale of the operation system!

**Required parameters**

* `locales=` (eg: ja+hr+ar+he)
* `font=` (fallback font)

**Example call in startup.xml**
```
<onload condition="!Skin.HasSetting(FontCheck)">RunScript(script.embuary.helper,action=fontchange,locales=ja+zh+ar+he+ko+vi+bn+my+hi+ks+km+ms,font=Arial)</onload>
<onload condition="!Skin.HasSetting(FontCheck)">Skin.ToggleSetting(FontCheck)</onload>
```

## Set Kodi setting
Sets Kodi setting with provided value. For reference please check `guisettings.xml` in the Kodi userdata folder.

**Example call**

`RunScript(script.embuary.helper,action=setkodisetting,setting=videolibrary.tvshowsselectfirstunwatcheditem,value=1)`

## Get Kodi setting
Gets a Kodi setting and stores the value to a window property. For reference please check `guisettings.xml` in the Kodi userdata folder.

**Example call**

`RunScript(script.embuary.helper,action=getkodisetting,setting=locale.country)`

**Result**

`Window(home).property(locale.country)` = Australia (12h)

**Example call with optional time format removal**

`RunScript(script.embuary.helper,action=getkodisetting,setting=locale.country,strip=timeformat)`

**Result**

`Window(home).property(locale.country)` = Australia

## Toggle Kodi setting bool
Toggles a Kodi setting bool from True to False or reversed. For reference please check `guisettings.xml` in the Kodi userdata folder.

**Example call**

`RunScript(script.embuary.helper,action=togglekodisetting,setting=filelists.showparentdiritems)`

## Enable/disable add-ons
Offers the option to disable or enable add-ons by skin. It's possible to change it for multiple add-ons at once by splitting them with `+`.

**Required parameters**

* `addonid=` (eg: script.foo.bar)
* `enable=` (true or false)

**Example call**

`RunScript(script.embuary.helper,action=toggleaddons,addonid=script.module.metadatautils+script.skin.helper.service,enable=true)`
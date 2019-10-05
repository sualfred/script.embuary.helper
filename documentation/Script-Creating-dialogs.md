## Important ##
Special characters and commas in arguments can break the called function. To bypass this issue it's required to escape the provided informations by wrapping them into `'" "'`.

**Example**

* `..&argument='"foo, bar"'&...`
* `..&argument='" / "'&...`
* `..&argument='$ESCINFO[ListItem.Plot]'&...`
* `..&argument='$ESCVAR[MyPlot]'&...`

## Open .txt file
Since Kodi dropped the support for changelog.txt it's a pita to maintain the changelog in addon.xml (keyword: indentation) and a lot of contributers are still using a more detailed changelog.txt. With this function it's possible to open a text file of your choice in the textviewer dialog.

**Example call**

`RunScript(script.embuary.helper,action=txtfile,path=special://skin/changelog.txt,header=$LOCALIZE[24036])`

Another option is to [store the text file content in a window property](https://github.com/sualfred/script.embuary.helper/wiki/Script:-Actions-and-helpers#get-txt-file-content) instead of using the textviewer dialog. This is useful if you want to compare the content of ListItem.AddonNews and changelog.txt so you are able to only show a changelog.txt button if it differs from the content of the addon.xml.

## Select dialog
Creates a select dialog with multiple supported actions per item. `||` is used as dividier if more than 1 action should be executed per item. `||` can be replaced by adding an additonal argument called `splitby=`. This is useful if you want to combine multiple select dialogs, because each one would require a own action divider. 

**Example: Regular call**
Note: Up to 30 select items are supported.

```
<onclick>SetProperty(Dialog.1.Label,First element label)</onclick>
<onclick>SetProperty(Dialog.1.BuiltIn,Skin.String(Foo,bar)</onclick>
<onclick>SetProperty(Dialog.2.Label,Second element label)</onclick>
<onclick>SetProperty(Dialog.2.BuiltIn,ClearProperty(Foo,home)||SetProperty(Foo,bar,home)</onclick>
<onclick>RunScript(script.embuary.helper,action=createselect,header=This is my heading)</onclick>
```

**Example: Split string and create select dialog based on values**

```
<onclick>SetProperty(Dialog.Builtin,ActivateWindow(videos)++Notification(Foo,Bar)</onclick>
<onclick>RunScript(script.embuary.helper,action=splitandcreateselect,header='"Whatever floats your boat"',items='$ESCINFO[ListItem.Director]',seperator='" / "',splitby='"++"')</onclick>
```

## Textviewer
Opens the text viewer with custom content.

**Example call**

`RunScript(script.embuary.helper,action=textviewer,header=$LOCALIZE[24036],message='$ESCINFO[ListItem.AddonNews]')`

## OK dialog
Opens the OK dialog with custom content.

**Example call**

`RunScript(script.embuary.helper,action=dialogok,header=$LOCALIZE[24036],message='$ESCINFO[ListItem.AddonNews]')`

## Yes/No dialog
Opens the Yes/No dialog with custom actions. Multiple actions are possible if they are divided by `|`.

**Parameters**

* `yesaction=` = actions for the "Yes" button
* `noaction=` = actions for the "No" button

**Example call**

`RunScript(script.embuary.helper,action=dialogyesno,header=$LOCALIZE[31313],message=$LOCALIZE[31314][CR][CR]$LOCALIZE[31315],yesaction=action1|action2)`
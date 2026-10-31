# CLAUDE.md

Kodi 21 (Omega) add-on `script.flatscan.widgets`: widget paths, skin helper actions and a background service for Kodi skins. Python 3 running inside Kodi's embedded interpreter. Originally forked from Embuary Helper and refactored into modules.

[README.md](README.md) is the user-facing reference (every `info=` widget, its params, script actions, settings, window properties). Keep it in sync when adding or changing widgets/actions.

## No build, no tests

- There is no test suite, linter config, or package manager. Code only runs inside Kodi — `xbmc`, `xbmcgui`, `xbmcplugin`, `xbmcaddon`, `xbmcvfs` don't exist outside it, so modules can't be imported or run with desktop Python.
- **Deploy:** the default VS Code build task ([.vscode/tasks.json](.vscode/tasks.json)) robocopies the repo (`/MIR`, excluding `.git`, `.vscode`, `__pycache__`, `*.md`) into `%APPDATA%\Kodi\addons\script.flatscan.widgets`. Restart Kodi or reload the add-on afterwards.
- **Release:** bump `version` (and the `<news>` entry) in [addon.xml](addon.xml) — Kodi only offers an update when the version goes up — merge to `master`, then run `python build.py` in the sibling `kodi-repo` repository (GitHub Pages: https://flatscan.github.io/kodi-repo/) and push it. Finally publish a GitHub release with the same zip: `gh release create v<version> --repo flatscan/flatscanwidgets --target master --title "Flatscan Widgets <version>" --notes-file <notes.md> ../kodi-repo/zips/script.flatscan.widgets/script.flatscan.widgets-<version>.zip` (always pass `--repo`: `gh` otherwise picks the `upstream` Embuary Helper remote). The zip is built with `git archive` from `master`, so only committed files ship; [.gitattributes](.gitattributes) `export-ignore` keeps dev files out.
- **Verify:** check `kodi.log` for lines tagged `[script.flatscan.widgets]`; exercise a widget by calling `Files.GetDirectory` over JSON-RPC with its `plugin://script.flatscan.widgets/?info=...` path.
- Active branch is `update-kodi-21`; `master` is the PR target.

## Three entry points, three separate processes

[addon.xml](addon.xml) declares three extension points. Each runs as its own Python invocation, so they share no in-memory state — they communicate through home-window (10000) properties and Kodi notifications.

| File | Extension point | Invoked by | Args |
|---|---|---|---|
| [plugin.py](plugin.py) | `xbmc.python.pluginsource` | `plugin://` widget paths | `sys.argv[1]` = handle, `sys.argv[2]` = `?query` |
| [default.py](default.py) | `xbmc.python.script` | skin `RunScript(script.flatscan.widgets,action=...,k=v)` | `sys.argv[1:]` = `key=value` strings |
| [service.py](service.py) | `xbmc.service` | Kodi at startup | none |

Each entry point inserts the add-on root into `sys.path` so `from resources.lib...` imports work. New modules must use absolute `resources.lib.` imports (or relative within a package).

Cross-process signals:
- `FlatscanWidgetUpdate` home property is pulsed (~100 ms) by the service on `VideoLibrary.OnUpdate`/`OnScanFinished` and by the `refreshwidgets` script action.
- `restartservice` action sends `NotifyAll(script.flatscan.widgets,restart_service)`; the service receives it as `method == 'Other.restart_service'` in `ServiceMonitor.onNotification`.
- Fanart rotation writes `FlatscanBackground`, `FlatscanBackgroundTitle`, `FlatscanBackgroundType`.

## Plugin: route registry → widget providers → ListItems

[plugin.py](plugin.py) is the core:

1. `@route(info, category=None, label=None)` registers a handler in `ROUTES`. Routes with a category/label also appear in the browsable menu (root → category → widgets, in definition order). Routes without them (`tvsimilar`, `seasons`, `episodes`, `similarmovies`, …) are path-only.
2. A handler has signature `(w, params, limit)` where `w` is a `Widgets` bundle (`w.shows`, `w.movies`, `w.mixed`) and returns `(items, mediatype, label)` or `None` to fail the directory (missing required param, feature disabled).
3. `router()` parses params, defaults `limit` to 100, calls the handler, and catches all exceptions (logged as `Error in router`).
4. `add_items_to_directory` / `create_listitem` turn item dicts into `xbmcgui.ListItem`s using the `InfoTagVideo` API (not deprecated `setInfo`). Per-item `mediatype` overrides the route's content type, which is how mixed widgets work.

URL/playability rules in `add_items_to_directory`:
- `episode`: URL is the item's `file`; no file (e.g. Sonarr upcoming) → empty URL, not playable.
- `movie`: `file`, else `videodb://movies/titles/<id>`.
- `season`/`tvshow`: folder into `videodb://tvshows/titles/...` unless the item has `is_playable` (then its `file` is played directly).
- Item dicts carry raw Kodi JSON-RPC field names (`showtitle`, `firstaired`, `resume`, `art`, `tvshowid`/`movieid`/`episodeid`, …) plus custom keys (`mediatype`, `is_playable`, `episode_count`, `season_title`, `tvshowtitle`, `is_group`, `group_type`, `first_episode_file`).

## Library code ([resources/lib/](resources/lib/))

- [addon.py](resources/lib/addon.py) — `ADDON` instance, paths, `get_setting(key, default)` (returns strings; compare bools as `== 'true'`). Creates the profile dir on import.
- [kodi_utils.py](resources/lib/kodi_utils.py) — `json_rpc_call(method, params)` (returns parsed dict, `{}` on failure — always read via `.get('result', {}).get(...)`), `set_window_property`.
- [cache.py](resources/lib/cache.py) — `read(name, max_age)` / `write(name, data)`: atomic JSON files in the add-on profile (`cache/`). Plugin calls are fresh processes, so this is the only cache that survives between widget loads. Used for Sonarr calendar data and season titles.
- [logger.py](resources/lib/logger.py) — `log(message, level='DEBUG')`; levels are strings (`'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`).
- [widgets/](resources/lib/widgets/) — data providers. `BaseWidget` supplies reusable JSON-RPC filter/sort dicts (`get_inprogress_filter`, `get_unwatched_filter`, `get_recent_sort`, `get_lastplayed_sort`, `get_recentlyaired_sort`, `get_random_sort`). Property lists live as class constants (`MovieWidgets.MOVIE_PROPERTIES`, `TVShowWidgets.EPISODE_PROPERTIES` / `TVSHOW_PROPERTIES` / `SEASON_PROPERTIES`) and are reused across classes. `MixedWidgets` composes the other two.
- [widgets/tvshows.py](resources/lib/widgets/tvshows.py) — largest module. Notable pieces:
  - `get_recently_added_grouped`: clusters episodes added within 20 h of the newest in the cluster, then per show emits a single episode, a season group, or a show group. `_set_navigation` makes groups either browse folders or play the first episode, per the `recentlyadded.navigation` setting.
  - `get_sonarr_upcoming`: reads the Sonarr calendar from the disk cache (`refresh_sonarr_cache`, refreshed by the service; 30 days ahead, max age 30 min) and filters by `days`; falls back to a live `_fetch_sonarr_calendar` (`urllib`, 10 s timeout) when the cache is missing or stale. Skips episodes with files. Its `tvshowid` is Sonarr's `tvdbId`, not a Kodi DBID.
  - `get_next_up`: per show, `_order_for_watching` puts the episodes in watch order (regulars by season/episode, specials slotted in by `firstaired`, undated specials last) and `_pick_next_up` returns the first unwatched episode after the furthest *regular* episode watched. Skipped episodes and specials before that point never come back, and a watched special does not move the marker (so a watched undated special can't hide the rest of the show). Listing every episode is the slow part, so each show's pick is cached in `nextup_choices` keyed by its episode count, watched count and `lastplayed` (plus a 1 day TTL); the episode details are always fetched fresh because resume points change without those counts changing. About half the specials in the author's library have no `firstaired`.
  - Artwork comes from `BaseWidget.episode_art()`, which maps the inherited art Kodi attaches to each episode (`season.poster`, `season.fanart`, `tvshow.poster`, `tvshow.fanart`, ...). Don't add per-show/season lookups: `GetSeasons` / `GetSeasonDetails` cost ~0.1 s each. `_get_season_details` (season titles) is the one remaining per-season lookup and is disk-cached for a day.
- [info/](resources/lib/info/) — `InfoProvider` subclasses (`TVShowDetails`, `PathStats`) that set window properties for `RunScript` actions and also back the `seasonshowdetails` / `pathstatswidget` routes. `PathStats` counts the media items Kodi lists for the path via `Files.GetDirectory` (sub-folders are ignored), so filtered nodes and playlists work.
- [service/](resources/lib/service/) — `ServiceMonitor` (`xbmc.Monitor`) runs `FanartService` (daemon thread), pauses it on screensaver, and restarts itself (by re-running `__init__` + `start`) on settings change or restart notification. `ArtworkCacheService` (`artwork_cache.py`, daemon thread, setting `artwork_cache_enabled`) starts 30 s after startup and then every 10 min or on library updates (debounced 15 s). Each cycle refreshes the Sonarr cache, runs the cached widget getters, and warms Kodi's texture cache for their images that are missing (max 150 per cycle) by opening `image://<url>/` with `xbmcvfs.File`, which goes through Kodi's texture cache. Warming checks the decoded URL against `Textures.GetTextures`, since Kodi stores keys with lowercase percent-encoding. Both service threads sleep in short slices so they stop within Kodi's 5 s limit.

## Conventions and gotchas

- **Adding a widget:** add a method to the right widget class, register a `@route` handler in [plugin.py](plugin.py), add it to the README tables. Adding a script action means a new branch in `route_action` in [default.py](default.py).
- Prefer server-side JSON-RPC `filter`/`sort`/`limits` (e.g. `dateadded`/`airdate` with `after`) over fetching everything and filtering in Python.
- **Performance (measured on a ~2700 movie / ~650 show library):** sorting all episodes by `dateadded` costs ~0.9 s but ~0.1 s with a date-window filter (`BaseWidget.get_recently_added`); requesting `cast`/`writer`/`director`/`streamdetails` roughly doubles query time, so the `*_PROPERTIES` lists are deliberately lean (nothing reads those fields from widget items); the plugin process itself costs ~0.3 s. The service can't reach into a plugin process, so share data through `cache.py`.
- Kodi wraps every art value as `image://<encoded url>/` once it is on a ListItem, so widgets may pass plain URLs or `image://` URLs interchangeably.
- `Addons.ExecuteAddon` over JSON-RPC does not start `default.py` for this add-on (the plugin extension wins); to test script actions use a Favourite or skin button with `RunScript(...)`. Kodi's TCP JSON-RPC (port 9090) is usually on even when the web server is off, handy for timing widgets with `Files.GetDirectory`.
- Use `datetime.fromisoformat`, not `strptime` — `strptime` can raise `TypeError` in Kodi's embedded Python.
- For episodes, Kodi's `year` sort method sorts by full air date (see `get_recentlyaired_sort`).
- Settings are defined in [resources/settings.xml](resources/settings.xml) (old-style flat format). IDs mix styles: `fanart_enabled` vs `sonarr.enabled`, `recentlyadded.navigation`. The service reads them with `getSettingBool`/`getSettingInt`; plugin code uses `get_setting` strings.
- Files keep the `#!/usr/bin/python` + `# coding: utf-8` header and module docstrings; match it in new files.
- Log through `log()` rather than `xbmc.log` directly, and default to `'DEBUG'` so messages only surface when the add-on's debug setting is on.

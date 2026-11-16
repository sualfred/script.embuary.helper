# Flatscan Widgets

A widget and helper add-on for Kodi 21 (Omega) skins. It provides library-backed widget paths, window-property helpers for skins, and a background service for fanart rotation.

- **Add-on ID:** `script.flatscan.widgets`
- **Requires:** Kodi 21 (Python 3)
- **License:** GPL-2.0-or-later

## Installation

Install the Flatscan repository once, and Kodi will keep the add-on up to date:

1. **Settings → File manager → Add source**, enter `https://flatscan.github.io/kodi-repo/` and name it `flatscan`.
2. **Settings → Add-ons → Install from zip file**. Kodi will say installing from unknown sources is disabled; choose **Settings** and enable **Unknown sources** (confirm the warning with **Yes**), then go back.
3. **Install from zip file → flatscan** and pick `repository.flatscan-<version>.zip`.
4. **Install from repository → Flatscan Repository → Video add-ons** (the add-on also shows under Program add-ons and Services) and install **Flatscan Widgets**.

**Unknown sources** is only needed to install the repository zip, so you can switch it off again afterwards.

### Manual install

Download `script.flatscan.widgets-<version>.zip` from the [GitHub releases](https://github.com/flatscan/flatscanwidgets/releases) and use **Install from zip file**. The zip must contain a top-level `script.flatscan.widgets/` folder with `addon.xml` inside it, so GitHub's *Download ZIP* of a branch (folder `flatscanwidgets-<branch>`) is rejected by Kodi.

## Using the widgets

Browse **Add-ons → Video add-ons → Flatscan Widgets** to pick a widget in your skin's widget editor, or use a path directly:

```
plugin://script.flatscan.widgets/?info=<widget>&limit=<n>
```

`limit` is optional and defaults to **100**. Some widgets take extra parameters, listed below. Parameters marked *(required)* make the widget fail (empty directory) when missing.

### TV Shows

| `info` | Description | Extra params |
|---|---|---|
| `inprogressepisodes` | Partially watched episodes | |
| `nextup` | Next episode to watch for each show you are watching: the first unwatched episode after the furthest episode you have watched, so episodes you skipped earlier (including specials) do not come back. Specials are ordered by air date; a special with no air date counts as coming after the last regular episode | |
| `recentepisodes` | Recently added episodes | |
| `recentlyaired` | Episodes that aired in the last N days, newest first. Episodes not yet aired are excluded | `days` (default 90) |
| `recenttvshows` | Recently updated shows | |
| `recentlyaddedgrouped` | Recently added episodes, grouped into season/show items (episodes added within 20 hours of each other are grouped) | `days` (default 30) |
| `upcomingepisodes` | Upcoming episodes from Sonarr (needs [Sonarr](#sonarr-integration) enabled). Items are informational and not playable | `days` (default: the *Days Ahead* setting) |
| `tvshowgenres` | TV show genres | |
| `tvshowsbyrandomgenre` | Shows from a random genre | |
| `tvsuggestions` | Suggested shows | |
| `tvsimilar` | Shows similar to a given show | `dbid` *(required)* |
| `seasons` | Seasons of a show | `dbid` *(required)* |
| `episodes` | Episodes of a season | `dbid`, `season` *(required)* |

### Movies

| `info` | Description | Extra params |
|---|---|---|
| `inprogressmovies` | Partially watched movies | |
| `recentmovies` | Recently added movies | `unwatched=true` |
| `recentlyreleasedmovies` | Movies released (premiered) in the last N days, newest first; includes pre-release copies with a future date | `days` (default 365), `unwatched=true` |
| `nextincollection` | For each started movie set, the first unwatched film after the furthest one watched (release order); most recently watched sets first. Sets listed in the exclude setting are skipped | |
| `collectionsinprogress` | Partly watched movie sets (at least one film watched and one not), with the set's artwork; most recently watched first; selecting one opens the set. Items carry `ListItem.Property(WatchedCount)`, `TotalCount`, `UnwatchedCount` and `NextTitle` (the film `nextincollection` would pick). Sets listed in the exclude setting are skipped | |
| `randommovies` | Random movies | |

### Mixed (movies and shows)

| `info` | Description | Extra params |
|---|---|---|
| `inprogressmedia` | Continue watching | |
| `suggestions` | Suggestions based on watch history | |
| `byrandomgenre` | Movies and shows from a random genre | |
| `similarmovies` | Movies similar to a given movie | `dbid` *(required)* |
| `similartvshows` | Shows similar to a given show | `dbid` *(required)* |
| `morebyactor` | Movies featuring an actor | `actor` *(required)* |

### Info widgets

| `info` | Description | Extra params |
|---|---|---|
| `seasonshowdetails` | Single item with show episode/watched counts | `dbid` *(required)* |
| `pathstatswidget` | Single item with total/watched/unwatched counts for a path | `path` *(required)* |

Examples:

```
plugin://script.flatscan.widgets/?info=recentlyaired&days=30&limit=20
plugin://script.flatscan.widgets/?info=recentmovies&unwatched=true
plugin://script.flatscan.widgets/?info=seasons&dbid=$INFO[ListItem.DBID]
```

## Script actions (for skins)

Call with `RunScript(script.flatscan.widgets,action=<action>,...)`.

| Action | Arguments | Result |
|---|---|---|
| `tvshowdetails` / `seasondetails` / `showdetails` | `dbid` *(required)*, `idtype` (default `season`), `window` (default 10000) | Sets TV show detail window properties |
| `pathstats` / `stats` | `path` *(required)*, `prop` (default `PathStats`), `window` (default 10000) | Sets `<prop>.Count`, `.Watched`, `.Unwatched`, `.InProgress` (plus `.Episodes`, `.WatchedEpisodes`, `.UnwatchedEpisodes` for TV paths) |
| `refreshwidgets` | | Pulses the `FlatscanWidgetUpdate` home window property (same signal the service sends on library updates) |
| `restartservice` | | Asks the background service to restart and re-read its settings |

Example:

```
RunScript(script.flatscan.widgets,action=pathstats,path=videodb://tvshows/titles/,prop=MyStats)
```

## Background service

When enabled, the service:

- Rotates random fanart from movies, TV shows and music artists, exposed through the `FlatscanBackground`, `FlatscanBackgroundTitle` and `FlatscanBackgroundType` home window properties.
- Warms Kodi's texture cache for the artwork your widgets display, so rows paint quickly instead of waiting on remote image downloads. It re-runs when the video library updates and every ten minutes, and caches a limited number of images per run (the rest follow on the next run).
- Keeps the Sonarr calendar cached on disk so the Upcoming Episodes widget does not wait on the network.
- Sets the `FlatscanWidgetUpdate` home window property briefly (about 100 ms) whenever the video library updates, so skins can refresh widgets.
- Pauses during the screensaver and restarts when settings change.

To refresh a skin container when the library changes, key it off the property, for example with a visibility or reload condition on `Window(Home).Property(FlatscanWidgetUpdate)`.

## Settings

| Category | Options |
|---|---|
| General | Enable background service, pre-cache widget artwork, debug logging |
| Background Fanart | Enable, rotation interval (seconds), include movies / TV shows / music |
| Widget Behavior | Recently Added navigation: `Browse` or `First Episode`; movie collections excluded from Next in Collection and Collections in Progress (comma-separated set names, case-insensitive) |
| Sonarr Integration | Enable, URL, API key, days ahead (1-30) |

### Sonarr integration

The `upcomingepisodes` widget reads your Sonarr calendar (`/api/v3/calendar`) and lists episodes that do not have a file yet, with poster and fanart from the series images.

1. In the add-on settings, open **Sonarr Integration** and enable it.
2. Set the Sonarr **URL** (for example `http://localhost:8989`) and the **API key** (Sonarr → Settings → General).
3. Choose how many days ahead to show (1-30). The `days` URL parameter overrides this per widget.

The calendar is cached on disk for up to 30 minutes, and the background service refreshes it about every ten minutes, so the widget itself loads instantly. Slow DNS or a slow Sonarr server only delays the service's refresh. If the service is disabled, or the cache is missing or older than 30 minutes, the widget fetches live instead (10 second timeout) and falls back to the last cached data if Sonarr cannot be reached. The cache always covers 30 days; larger `days` values bypass it.

## Troubleshooting

- **Enable debug logging** in the General settings. Without it, the add-on's debug messages are hidden; with it, they appear at INFO level in `kodi.log`. Look for lines containing `script.flatscan.widgets`.
- **A widget is empty:** check that required parameters (`dbid`, `season`, `actor`, `path`) are present, and look for `Error in router` in the log.
- **Upcoming Episodes is empty:** confirm Sonarr is enabled, the URL is reachable from the Kodi device, and the API key is correct. Failures are logged as `Sonarr API error`.
- **Images pop in late on the first view:** artwork is downloaded the first time Kodi displays it. Keep *Pre-cache widget artwork* enabled so the background service does this ahead of time; with debug logging on you will see `ArtworkCache:` lines in the log.
- **The first Upcoming Episodes load is slow:** with an empty cache the widget has to fetch from Sonarr itself. It is fast once the service has refreshed the cache.

## Development

Widget routes are defined in a registry in `plugin.py`. Each route is registered once with a decorator; the browsing menus (root and category folders) are generated from the same registry.

To add a widget:

1. Add a method to the matching widget class in `resources/lib/widgets/` (`tvshows.py`, `movies.py` or `mixed.py`). It returns a list of dicts with Kodi JSON-RPC fields and an `art` dict.
2. Register a handler in `plugin.py`:

   ```python
   @route('myinfo', 'tvshows', 'My Widget')   # info id, menu category, menu label
   def route_myinfo(w, params, limit):
       return w.shows.get_my_widget(limit=limit), 'episode', 'My Widget'
   ```

   A handler returns `(items, mediatype, label)`, or `None` to fail the directory (for example when a required parameter is missing). Omit the category and label to register a route that does not appear in the menus.
3. Add it to the tables in this README.

Tips:

- Prefer server-side filters and sorting in `VideoLibrary` JSON-RPC calls (for example `airdate` / `dateadded` with the `after` operator) over fetching large lists and filtering in Python.
- Kodi's embedded Python behaves differently from desktop Python in places. For example `datetime.strptime` can raise `TypeError`; use `datetime.fromisoformat` instead.
- Each plugin call runs in a fresh Python process, so an in-memory cache never survives between widget loads. Avoid per-item JSON-RPC lookups (they add up quickly: `GetSeasons` and `GetSeasonDetails` cost about 0.1 s each). Kodi already puts inherited season and show art on every episode (`season.poster`, `tvshow.fanart`, ...), which `BaseWidget.episode_art()` turns into widget art. For slow data that must be looked up, use `resources/lib/cache.py` (JSON files in the add-on profile), optionally refreshed by the service.
- Sorting a whole library by `dateadded` is slow; `BaseWidget.get_recently_added()` filters to a recent date window first and only falls back to the full sort when needed.
- Request only the properties a widget uses. `cast`, `writer`, `director` and similar roughly double the cost of a query.
- You can exercise a widget without a skin by calling `Files.GetDirectory` over JSON-RPC with the `plugin://` path.

## Project layout

```
addon.xml            Add-on manifest
default.py           Script entry point (RunScript actions)
plugin.py            Plugin entry point (route registry, widget paths and browsing)
service.py           Service entry point
resources/
  settings.xml       Add-on settings
  lib/
    addon.py         Add-on handle and settings helper
    kodi_utils.py    JSON-RPC helper
    cache.py         On-disk JSON cache in the add-on profile
    logger.py        Logging (honours the debug setting)
    widgets/         Widget data providers (tvshows, movies, mixed)
    info/            Window-property info providers
    service/         Fanart and artwork-cache services, and the monitor
```

## Links

- Source: <https://github.com/flatscan/flatscanwidgets>
- Discussions: <https://github.com/flatscan/flatscanwidgets/discussions>

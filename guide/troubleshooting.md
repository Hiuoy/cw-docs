# Help: errors and fixes

> What you see, why, and what to do. Start with the log: `<game>\cw-mod\client.log`, from the last `===== session start` line down.

## Read this first

- The game often shows an error as **three words and a number**, such as "Uniform 58 Guerrilla Boa". That is a code name, not a message. The log line just before it names the real cause.
- What happens on screen can mislead. The log is the record.
- Most settings are read when the game starts. After a change, restart.

## Starting the game

| What you see | Cause | Fix |
|---|---|---|
| No console window, no overlay | The mod's DLL is not next to `BlackOpsColdWar.exe`, or has another name | Run `scripts\launch.ps1` again. See [Install](/guide/install.md). |
| The game closes in the first seconds, before the console prints `MainEntryPoint reached` | The protection's own start-up failed. It happens now and then. | Start the game again. Every time: the game is not build 1.34.0.15931218. |
| The game closes when a debugger or a memory tool is attached | The protection | Do not attach one. |
| Features are missing and the Home tab shows an unknown game version | Another game build | Use build 1.34.0.15931218. |
| The Home tab says the settings file is broken | `cw-mod.json` is not valid JSON | Fix it and restart. See [Settings](/guide/settings.md). |
| The menus of the wrong mode | The mode is read at start | Set `"mode"`, save, restart. |
| A second, empty `cw-mod` folder somewhere | The game was started from another folder | Start it from inside `<game>`. |

## Online mode

| What you see | Cause | Fix |
|---|---|---|
| `Auth task failed with HTTP code [0]` | Any setup mistake: no backend running, certificate not trusted, old keys in the game folder, a port in use | `python run.py --check` names the cause. See [dwserver](/guide/tools/dwserver.md). |
| A Battle.net error dialog (BLZBNTBGS) | The game's sign-in watchdog. The mod switches it off at start, so you should not see it. | Report it with the log. Until then, use `offline` or `lan`. |
| Mode tiles with padlocks | No party was made: the title screen was skipped | Keep `"start_screen": true` and press start on the title screen. |
| "No preferred playlist is loaded" or no modes | No playlist files in `cw-mod\lpc`, or they are for another build | Copy your own playlist files there. The log's `(LPC)` lines say which were skipped. See [Online mode](/guide/play/online.md). |
| "Uniform 58 Guerrilla Boa" | A game zone file was renamed or changed. The game checks a signature that covers the file's name, and fails one zone later. For playlists: a renamed playlist file. | Put the files back under their original names. |
| "Failed to host lobby" on Start | The match went to public matchmaking | The backend is off or the mod is old: on a backend boot the mod routes Start to a private lobby. |
| The store is empty and the battle pass does not move | They need Activision's marketplace | Not available. See [Progression](/guide/play/progression.md). |

## Playing together

| What you see | Cause | Fix |
|---|---|---|
| The Server Browser list is empty | UDP 28970 is blocked on the listening PC | Allow it in the firewall. |
| The second PC cannot join, or joins itself | Both PCs have the same name, or the same `"xuid"` | Give each its own. Never copy `cw-mod.json` between PCs. |
| "Clientfield Mismatch" after the map loads | The two PCs run different scripts: different maps, different script mods, or an old-format custom map | Same map build and same scripts on both. See [Custom maps](/guide/play/custom-maps.md). |
| A crash on the second PC when a custom map loads | Left-over old-format zones of that map, with an older mod | Update the mod, delete the map's old `ww_1080_` and `ww_4k_` files, and build it again. |

## Scripts

| What you see | Cause | Fix |
|---|---|---|
| A script does nothing | It is not in `cw-mod\scripts`, was compiled for another game, or registers nothing | Check the overlay's Scripts tab. See [Game scripts](/guide/scripting/gsc.md). |
| "Clientfield Mismatch" with your script loaded | Your server script registers a clientfield with no client half | Register it on both sides. The mod writes both lists to `cw-mod\clientfields_*.txt`. |
| The game closes when your menu opens | Plain text reached a stock menu widget | Wrap it: `"\021text\020"`. See [Menu scripts](/guide/scripting/ui-scripts.md). |
| A `(UiScripts)` line with an error | A Lua error in your file | It names the file and line. |

## Custom maps

| What you see | Cause | Fix |
|---|---|---|
| No CUSTOM MAPS tab | `"ui_scripts"` or `"custom_maps"` is off, or no map is installed | Switch them on; build a map. |
| The stock map starts instead of yours | The map was not picked in CUSTOM MAPS | Pick it there, then start. |
| The overlay's Maps tab says "missing" | A zone of the map's set is not there | Build the map again. |
| A crash while the map loads | A build problem | Read the crash in the log, then build with a current cwlink. Report it with the log. |
| Walls draw but nothing is solid, or the other way round | `solid` and `rendered` on the brushes | See [Geometry](/guide/mapping/geometry.md). |
| No zombies, or zombies that stand still | Zones, spawners or the navmesh | See [Zones and spawns](/guide/mapping/zones-spawns.md) and [Navmesh](/guide/mapping/navmesh.md). |

## Building maps

| What you see | Cause | Fix |
|---|---|---|
| Build says the game folder, cwlink or the trace is missing | Setup is not finished | See [Setup](/guide/mapping/setup.md). |
| cwlink cannot write its files | The game is running | Close it. |
| The script step fails | ACTS is not on your PATH, or a level script has an error | Install ACTS; read its message. |
| "skipped" lines in the build output | An object beyond what Die Maschine has | See [What you can and cannot make](/guide/mapping/limitations.md). |
| Models are gray or boxes in the editor | Textures are not shown yet; boxes mean mkasset is not running | See [Props and models](/guide/mapping/props-models.md). |

## Reporting a problem

Send these, and a fix is much more likely:

1. The last run from `client.log`: from the last `===== session start` line to the end.
2. What you did, step by step, and what you expected.
3. Your mode, and whether the backend was running.
4. For a map problem: the build output and the `.mkmap`.

Leave your `"xuid"` and anything from the backend's `material` folder out of what you send.

**How it works inside:** [Errors: how the game stops](/re/engine/errors.md).

<!-- sources: cw-mod docs/ROADMAP.md, docs/backend-roadmap.md (B0, B3, B6 to B8), .claude/skills/bocw-reverse-engineering/SKILL.md (sections 6, 9 and 10), tools/dwserver/README.md, client/game/local_lpc.hpp, client/game/ui_scripts.hpp, client/game/mapkit_loader.hpp, client/overlay/tabs/*.cpp, mapkit/godot/README.md @ 36b1f18 + working tree, 2026-10-08 -->

# The overlay

> cw-mod's in-game menu. Press **Insert** to open or close it. **Status:** Done.

While the overlay is open, the keyboard and mouse belong to it and the game gets no input. A `(?)` next to a control explains it when you point at it.

Most players need three tabs: **Home**, **Server Browser** and **Scripts**. The others are tools for testing and for the people who work on the mod.

## Home

| Shows or does | Detail |
|---|---|
| Status | Game version, module name, frames drawn, whether the script system is up |
| Settings | Your name and mode, the state of unlock-all, and whether `cw-mod.json` loaded |
| Open cw-mod.json | Opens the settings file in your editor |
| Send test notification | Shows a message through the game. It proves the mod can call the game. |
| ZM progression | Saved XP and level, this match's XP, and bonus XP |
| +1000, +10000, +100000, Add XP | Queues bonus XP. It is added at your next XP event in a Zombies match (kill anything) and saved when the match ends. |

## Server Browser

Lists the games on your network and joins one. See [LAN mode](/guide/play/lan.md).

| Control | Detail |
|---|---|
| Advertise my lobby | Announce your lobby to the network once a second |
| Listen | Listen for other PCs' lobbies |
| The list | Host, map, mode, players, state, ping. Click a row for details. |
| Join | Join that lobby |

## Scripts

The game-script loader. See the Scripting guides.

| Control | Detail |
|---|---|
| Loader on / off | Whether your scripts are used |
| Reload folder | Read `cw-mod\scripts` again. In a match the change waits for the next match. |
| The table | Each script: file, inject or replace, name hash, string count, times served |
| Adding a script | The compile commands, in short |
| Diagnostics | For developers: signatures, script requests, and the decrypted-module dump |

## Maps

| Shows or does | Detail |
|---|---|
| The table | Each folder in `cw-mod\maps`, its zones, and whether the set is complete |
| CUSTOM MAPS pick | The map picked in the game's CUSTOM MAPS tab, and whose level scripts are being used |
| Start a custom map | For maps without a `map.json`: start one map when the lobby starts another. Apply it **before** you open the Zombies lobby. |
| Live-state dump, asset usage | Tools for map-tool development |
| Events | What the map loader did, newest last |

## Session

Network mode and joining by hand.

| Control | Detail |
|---|---|
| this boot | The mode this run was started in |
| Player cap | Sets `com_maxclients`. Apply it before a map starts. |
| Show host descriptor | Prints a `CWJOIN1` line for your current lobby. It is valid until the lobby is made again. |
| Join host by descriptor | Paste a `CWJOIN1` line from the host and join. Leave `ctx`, `pad`, `jointype` at 0, 0, 4. |
| Disconnect | Leave the current session |
| The rest | Diagnostics: session state, the join transcript, an experimental second local player |

## Demonware

Read-only. Shows whether Demonware names are redirected to your PC, whether they are blocked, every endpoint the game asked for, whether the backend's keys were put in, and the login state. **Save journal** writes the list to `cw-mod\dw_journal.txt`. See [Online mode](/guide/play/online.md).

## LUI Menus

A test tool: opens a game menu by name or hash, and lists the menus the game has registered. Menus opened this way often raise errors later, so the mod stops such errors from closing the game for the rest of the run. **Dump loaded Lua files** writes the menus' bytecode to `cw-mod\lua_dump`.

## Debug

| Control | Detail |
|---|---|
| Name hash | Type a name, read its hash. The same hash names dvars, menus and script literals. |
| Inspect, Set int, Set bool | Read or set a dvar by name |
| Dump all registered dvars | Writes every dvar to `cw-mod\dvars.txt` |
| Recover names from memory | Searches the game's memory for names that match known hashes |

**How it works inside:** [The overlay](/re/client/overlay.md).

<!-- sources: cw-mod client/overlay/menu.cpp, client/overlay/tabs/home.cpp, server_browser.cpp, scripting.cpp, maps.cpp, session.cpp, demonware.cpp, lui_menus.cpp, debug.cpp, client/overlay/d3d12_hook.cpp @ 36b1f18 + working tree, 2026-10-07 -->

# File structure

> Every file and folder the mod reads or writes, and what each one is for.

`<game>` is the folder that holds `BlackOpsColdWar.exe`.

## The mod folder

```text
<game>/
  discord_game_sdk.dll          the mod
  cw-mod/
    cw-mod.json                 settings
    client.log                  the log, all runs
    scripts/                    your compiled game scripts
    ui_scripts/                 your menu scripts
    maps/
      <id>/                     one folder per custom map
        map.json
        <id>.ff
        scripts/
        generated/
    dwserver/                   the backend's two public keys
    lpc/                        your own playlist files
    backups/                    copies of your saves
    mapkit/                     map-making data
```

| Path | Who writes it | What it is |
|---|---|---|
| `cw-mod.json` | The mod, then you | Every setting. Made on the first run. See [Settings](/guide/settings.md). |
| `client.log` | The mod | The log. See [Running the game](/guide/running.md). |
| `scripts/*.gscc`, `*.cscc` | You | Compiled game scripts, loaded at start and used in the next match. |
| `ui_scripts/*.lua` | You | Lua run in the menus, in file-name order. Edited files run again while the game is up. |
| `maps/<id>/map.json` | cwlink | The map's title, form and asset library. A map with this file is listed in the CUSTOM MAPS tab. |
| `maps/<id>/<id>.ff` | cwlink | The map's zone. Built from your own install: never share it. |
| `maps/<id>/scripts/` | cwlink | The map's own level scripts, used only while that map runs. |
| `maps/<id>/generated/` | cwlink | Readable copies of what the build generated: the zones script and the navmesh as `.obj`. |
| `dwserver/auth_pub.der`, `lsg_pub.der` | You | Their presence turns the local backend on. See [Online mode](/guide/play/online.md). |
| `lpc/*.ff` | You | The playlist files your own game downloaded. They never leave your PC. |
| `backups/player-<date>-<time>/` | The mod | Your save files, copied once per run. The newest 10 are kept. |

## Files for map makers

| Path | Who writes it | What it is |
|---|---|---|
| `mapkit/trace/<zone>.mktrace` | The mod, when `"mapkit_trace"` names the zone | Where each asset starts in a zone. The map tools need it. |
| `mapkit/brush_materials.txt` | cwlink | The game materials a brush can use, by name. |
| `mapkit/usage/<map>_<time>.mkuse` | The mod, with `"mapkit_usage"` | What a match looked up. Used to count what a map borrows. |
| `mapkit/live/<time>_<label>/` | The mod | Memory snapshots of a custom map's models, for debugging. |

## Files from the overlay's buttons

| Path | Button | What it is |
|---|---|---|
| `dw_journal.txt` | Demonware tab | Every Demonware name the game resolved and every connection it made |
| `clientfields_server.txt`, `clientfields_client.txt` | none: written on a mismatch | The two clientfield lists, to find the difference |
| `lua_dump/<hash>.luac` | LUI Menus: Dump loaded Lua files | The menus' Lua bytecode |
| `dvars.txt` | Debug: Dump all registered dvars | Every dvar's hash, type, flags and address |
| `names_recovered.txt` | Debug: Recover names from memory | Names found for known hashes |
| `<game>/bocw_dump.bin` | Scripts: Dump decrypted module | The decrypted game image, for a disassembler |
| `<game>/client_join_args.txt` | Session: netmsg transcript | The join messages of a session |
| `<game>/cw-mod.log` | none | The console's text for the current run only |

## Your saves

Saves are not in the game folder.

```text
Documents/Call Of Duty Black Ops Cold War/player/
  *.cgp                      the game's own save files
  cwmod_ae_sync_0.bin        your level and weapon levels, kept by the mod
```

## What never to share

- `maps/<id>/<id>.ff` and anything made by `cwlink clone` or `cwlink replace`: they hold data copied from your install.
- `lpc/`, `mapkit/trace/`, `lua_dump/`, `bocw_dump.bin`: game data.
- `cw-mod.json`: it holds your player id. Each PC needs its own.

<!-- sources: cw-mod client/game/settings.cpp, common/logger/log_service.cpp, common/logger/console.cpp, client/game/ui_scripts.hpp, client/scripting/scripting.hpp, client/game/mapkit_loader.hpp, client/game/zm_progression.cpp (DocumentsPlayerDir, BackupPlayerFolder), client/game/local_lpc.hpp, client/game/join_log.cpp, client/overlay/tabs/*.cpp, docs/ROADMAP.md @ 36b1f18 + working tree, 2026-10-07 -->

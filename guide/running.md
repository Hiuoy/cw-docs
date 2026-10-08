# Running the game

> How to start a modded game, pick its mode, and read what happened. **Status:** Done.

## Starting

Run `scripts\launch.ps1` from the cw-mod folder, or start `BlackOpsColdWar.exe` yourself **from inside `<game>`**. The mod keeps its files in a `cw-mod` folder under the folder the game was started from, so a shortcut with another "Start in" folder makes a second, empty `cw-mod` somewhere else.

A console window with the mod's log opens first. Press **Insert** in the game to open or close the [overlay](/guide/overlay.md). While it is open, the keyboard and mouse go to the overlay and not to the game.

## Picking a mode

The game builds its menus from its network mode while it starts, so the mode is a setting, not a button. Set `"mode"` in [cw-mod.json](/guide/settings.md), then start the game.

| `"mode"` | What you get | Use it for |
|---|---|---|
| `offline` | The offline menus. The default. | Solo play, scripts, custom maps |
| `lan` | The LAN menus | [Two PCs, LAN mode](/guide/play/lan.md) |
| `online` | The online menus, a party and playlists, served by a backend on your PC | [Online mode](/guide/play/online.md) |
| `lanlobby` | A LAN lobby with the mod's online-mode handling switched on | Tests only. See [the boot profile](/re/client/boot-profile.md). |

## The protection, and what it means for you

The game's executable is protected by Arxan. The mod deals with it during start-up. For you this means:

- **Do not attach a debugger.** The game closes.
- **A crash in the first seconds can happen.** If the game dies before the console prints `MainEntryPoint reached`, the protection's own start-up failed. Start the game again. If it happens every time, the game is not build 1.34.0.15931218.
- **The mod is tied to one build.** Its addresses are for that build only.

## Reading the log

Everything the mod does is written to `<game>\cw-mod\client.log`.

- The file is never emptied. Each start adds a line `===== session start <date> <time> =====`; the last one marks the current run.
- A line looks like `[2026-10-7 17:44:01] [INFO] (Settings) ...`. The word in round brackets says which part of the mod wrote it.
- Each line is saved as it is written, so a crash keeps everything before it.

| Line | Meaning |
|---|---|
| `(Settings) name "..." ..., mode ...` | The settings this run uses |
| `(Crash) Unhandled-looking exception` | A crash, with its address and the callers on the stack |
| `(Crash) known benign fault` | Two faults that happen on every healthy run. Ignore them. |
| `(Script) ...` | Text a game script printed on screen |
| `(Login) [status 27] Login Complete` | Online mode: the backend login worked |

From the cw-mod folder, `python tools\bootlog.py` prints the last run in short form: login steps, errors, crashes, and the backend's log for the same run.

Two crashes logged while the game closes (in `telescope.dll`, then in the executable) are the game's own and harmless.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The log says the settings file is broken | `cw-mod.json` is not valid JSON. The run used the defaults (offline). Fix the file and restart. |
| Menus of the wrong mode | The mode is read at start. Save `cw-mod.json`, then restart the game. |
| An error dialog with three words and a number | The game's code name for an error. The log line just before it names the real cause. See [Errors and fixes](/guide/troubleshooting.md). |

**How it works inside:** [The boot profile](/re/client/boot-profile.md), [Arxan](/re/client/arxan.md), [Errors](/re/engine/errors.md).

<!-- sources: cw-mod docs/ARCHITECTURE.md (boot profile), client/game/settings.cpp, client/game/boot_profile.hpp, common/logger/logger.hpp, common/logger/log_service.cpp, client/main.cpp (crash logger), .claude/skills/bocw-reverse-engineering/SKILL.md (sections 6 and 10), scripts/launch.ps1 @ 36b1f18 + working tree, 2026-10-07 -->

# Settings: cw-mod.json

> One file holds every cw-mod setting: `<game>\cw-mod\cw-mod.json`. It is read once, when the game starts.

## Rules of the file

- It is plain JSON: no comments, no trailing commas.
- The first run writes it with the defaults. A key you leave out is added with its default the next time the game starts.
- **Change it, save it, restart the game.** Nothing is re-read while the game runs.
- A key the mod does not know is ignored, and the log names it as a possible typo.
- If the file is not valid JSON, the run uses the defaults (offline). The log and the overlay's Home tab say so, and the broken file is left as it is.

## Examples

<!-- tabs:start -->

#### **Offline**

```json
{
  "name": "Player",
  "mode": "offline"
}
```

#### **LAN**

```json
{
  "name": "Player",
  "mode": "lan"
}
```

#### **Online**

```json
{
  "name": "Player",
  "mode": "online",
  "backend": true,
  "start_screen": true
}
```

<!-- tabs:end -->

## Who you are

| Key | Default | Effect |
|---|---|---|
| `name` | `""` | Your in-game name, at most 32 bytes. Empty uses your Windows account name. |
| `xuid` | made at first run | Your player id, as hex text such as `"0x1A2B3C4D5E6F7081"`. Used when the local backend is on. **Never copy it to another PC:** two players with one id look like one player joining itself. |

## How the game boots

| Key | Default | Effect |
|---|---|---|
| `mode` | `"offline"` | `offline`, `lan`, `online`, or `lanlobby` (for tests). See [Running the game](/guide/running.md). |
| `backend` | `true` | Use the local backend when `cw-mod\dwserver\auth_pub.der` and `lsg_pub.der` are there. `false` ignores that folder. |
| `start_screen` | `true` | Online mode with the backend: open on the title screen, so that pressing start creates your party. With `false` the game jumps straight to the menu and the mode tiles stay locked. |
| `local_playlists` | `true` | Load the playlist files in `cw-mod\lpc`. |
| `lobby_waiver` | `true` | Online mode: let the menus open although the store and public matchmaking never answer. |

## Features

| Key | Default | Effect |
|---|---|---|
| `scripts` | `true` | Load game scripts from `cw-mod\scripts` at start. The overlay's Scripts tab can still switch it. |
| `ui_scripts` | `true` | Run the Lua files in `cw-mod\ui_scripts` in the menus. This also carries the CUSTOM MAPS tab. |
| `custom_maps` | `true` | Load maps from `cw-mod\maps`. |
| `progression` | `true` | Keep Zombies XP, weapon levels and saves on this PC. See [Progression](/guide/play/progression.md). |
| `live_menus` | `true` | In a LAN lobby, show the menus as an online lobby does: locks and weapon levels appear. |
| `unlock_all` | `false` | Answer every lock and ownership check as unlocked or owned. Nothing is written to your save. |
| `ui_text` | `{}` | Replace text the game shows: `{ "text the game shows": "new text" }`. The whole string must match; upper and lower case are treated alike. Keep placeholders such as `&&1`. |

## Diagnostics

| Key | Default | Effect |
|---|---|---|
| `ui_text_log` | `false` | Write every piece of UI text to the log once, as a `(UiText)` line. Use it to find the exact text for `ui_text`. |
| `lua_print` | `true` | Write the lobby menus' own print output to the log. |
| `mapkit_trace` | `[]` | Zone names whose loading is recorded for the map tools, such as `["zm_silver", "zm_common"]`. `"*"` records every zone. |
| `mapkit_usage` | `false` | Record what a match looks up, to count what a map borrows. It slows every lookup a little. |
| `fpsession_standin` | `false` | For developers: hand out an empty first-party session instead of watching for callers that need one. |

## For one run only

Two environment variables override the file for one process. They exist so that two copies of the game can run on one PC.

| Variable | Overrides |
|---|---|
| `CW_MOD_NAME` | `name` |
| `CW_MOD_XUID` | `xuid` (hex) |

## Old marker files

Older versions used empty files such as `cw-mod\online` or `cw-mod\no-scripts`, and `cw_mod_name.txt`. They are not read any more. The first run with no `cw-mod.json` turns them into one, and the log lists any that are still there. Delete them.

**How it works inside:** [The boot profile](/re/client/boot-profile.md), [Dvars](/re/engine/dvars.md).

<!-- sources: cw-mod client/game/settings.hpp, client/game/settings.cpp, docs/ARCHITECTURE.md ("Boot profile"), docs/backend-roadmap.md (B6: start_screen, lobby_waiver) @ 36b1f18 + working tree, 2026-10-07 -->

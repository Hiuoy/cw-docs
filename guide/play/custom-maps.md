# Custom maps

> How to add a custom Zombies map to your game and start it. **Status:** Done, also with two PCs (2026-09-29).

## How a map reaches you

A custom map is shared as its **source**: a `.mkmap` file, with a folder of textures when the map has its own. The playable map is built from that source on **your** PC, because the build copies data from your own install into the map's zone. A zone someone else built must not be passed around, and it is not needed.

## Before you start

- `"custom_maps": true` and `"ui_scripts": true` in `cw-mod.json`. Both are the defaults.
- To build a map from its source you need what a map maker has: `cwlink.exe` (built with the mod), ACTS on your PATH to compile the map's scripts, Die Maschine installed, and a zone trace of it.

## Build a map you were given

From the cw-mod folder, with the game closed:

```powershell
build\t9_vs2022\x64\cwlink\cwlink.exe build zm_silver <map>.mkmap --game "<game>" --trace "<game>\cw-mod\mapkit\trace\zm_silver.mktrace"
```

Keep the map's texture folder next to its `.mkmap` file: the source names its textures by a path relative to itself.

cwlink writes the map into `<game>\cw-mod\maps\<id>\`: its zone `<id>.ff`, its level scripts, and `map.json`.

## Start it

1. Start the game.
2. Open Zombies, then **Private**. A **CUSTOM MAPS** tab lists every map in `cw-mod\maps` that has a `map.json`.
3. Pick the map and start the match as usual.

The stock maps stay stock: a custom map is used only while it is picked there.

## Two PCs

- Every player needs the map built on their own PC, under the same map id.
- The host picks the map. The lobby sends the map's name to the others, and each PC loads its own copy.

## Old-format maps

Maps built before 2026-09-29 came as two files, `ww_1080_<id>.ff` and `ww_4k_<id>.ff`. They work only on the PC that picks them: the other PCs load the stock map and are kicked with "Clientfield Mismatch". Build such a map again from its source, and delete its old files on every PC.

## Limits

- Today a custom map still loads part of Die Maschine as its asset library, so you need that map installed.
- The map's picture in the menu and its loading screen are still Die Maschine's.
- The after-action report after a custom-map match opens in online mode. In LAN mode it has not been checked.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| No CUSTOM MAPS tab | `"ui_scripts"` or `"custom_maps"` is `false`, or `cw-mod\maps` holds no map. |
| The map is not in the tab | Its folder has no `map.json`. Build it with `cwlink build`. |
| The overlay's Maps tab says "missing" | A zone of the map's set is not there. Build the map again. |
| "Clientfield Mismatch" on the second PC | That PC has no copy of the map, an older build of it, or an old-format map. |
| cwlink cannot write its files | The game is running and keeps the map's files open. Close it first. |
| cwlink asks for a trace | Add `"mapkit_trace": ["zm_silver", "zm_common"]` to `cw-mod.json` and start Die Maschine once. |

<!-- sources: cw-mod client/game/mapkit_loader.hpp, mapkit/README.md, mapkit/godot/README.md ("Build"), docs/ROADMAP.md (section 5, "Open and parked"), client/overlay/tabs/maps.cpp @ 36b1f18 + working tree, 2026-10-07 -->

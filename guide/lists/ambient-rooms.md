# Ambient rooms

> The room names an `MkAmbientRoom` can use: the rooms of Die Maschine's sound bank that its own areas use.

## The names

| `room` | Areas of Die Maschine that use it | By its name, fits |
|---|---|---|
| `zm_nacht_interior` | 5 | A building's inside |
| `zm_nacht_bunker_hallways` | 4 | Corridors |
| `zm_nacht_bunker_entrance` | 2 | An entrance |
| `zm_nacht_bunker` | 1 | A bunker room |
| `zm_nacht_bunker_medium_room` | 1 | A medium room |
| `zm_nacht_bunker_small_room` | 1 | A small room |

Outside every ambient room, the map plays the sound bank's **default room**. A name the bank does not have plays the default room too, and the build output says so.

## How to choose

Listen. The names are a hint only. Build the project's debug map, `maps\zm_debug.tscn`: it has one room of each kind side by side, and an open yard that plays the default room.

One warning: in `zm_nacht_bunker_hallways` the echo seems to change from point to point, following Die Maschine's walls. See [Sound](/guide/mapping/sound.md).

## In the game's own terms

For a scripter or a reader of the game's data, an ambient room is a trigger:

| Key | Value |
|---|---|
| `classname` | `trigger_multiple`, in the level's trigger list |
| `targetname` | `ambient_package` |
| `script_ambientroom` | The room's name |
| `script_ambientpriority` | Where rooms overlap, the higher wins |

A build writes one such trigger for each `MkAmbientRoom`.

<!-- sources: cw-mod mapkit/godot/README.md (MkAmbientRoom, "The debug map"), mapkit/cwlink/main.cpp (kAmbientRoomTargetname), the ambient_package triggers of Die Maschine's trigger list (ffinfo --entities-json, names and counts only), docs/ROADMAP.md ("Ambient rooms") @ 36b1f18 + working tree, 2026-10-08 -->

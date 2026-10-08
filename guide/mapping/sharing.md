# Sharing a map

> Share the map's source, never the built zone. Whoever plays it builds it on their own PC.

## Why

A build copies data from your own game install into your map's zone: lighting, images, the sound bank and more. That zone is a copy of game data. The source holds only your work, with game assets by name.

## What to share

Everything is in `mapkit\godot\build\` after an Export or a Build.

| File | What it is | Share? |
|---|---|---|
| `<map>.mkmap` | The map's source: your geometry, objects and settings, as JSON | **Yes** |
| `<map>_textures\` | Your own textures, as `.dds` | **Yes**, next to the `.mkmap` |
| Your Godot scene, `.glb` models and images | So others can open and change the map | If you like |
| Level scripts you changed | Your own script files | If you changed them |

The `.mkmap` names its textures by a path relative to itself, so keep the folder beside it.

## What never to share

| File | Why |
|---|---|
| `<game>\cw-mod\maps\<id>\<id>.ff` | Holds data copied from your install |
| Old-format `ww_1080_<id>.ff`, `ww_4k_<id>.ff` | The same |
| Anything made by `cwlink clone` or `cwlink replace` | A copy of a retail zone |
| Zone traces, model caches, dumps | Made from the game |
| A texture or model taken out of the game | Not yours to share |

## What the other player does

They need cw-mod and the map tools, like you. Then one command builds your map on their PC: see [Custom maps](/guide/play/custom-maps.md).

## Before you publish

- **Pick a name nobody else will pick.** The map's name is its id, its folder and its zone: `zm_`, then lowercase letters, digits and `_`, at most 48 characters. It must not be the name of a map the game ships.
- **Fill in `title` and `author`** on the `MkMap` node. The title is what players see in the CUSTOM MAPS tab.
- **Say which cw-mod version you built with.** A newer cwlink may build an old source a little differently.
- **Use only your own content** for textures and models, or content whose licence lets you share it.
- **Check it builds from the shared files alone.** Copy the `.mkmap` and its texture folder somewhere else and build from there.

## Playing together

Every player in a lobby needs the same map built from the same source. The host picks it; the others load their own copy by its name. A player with an older source is kicked with "Clientfield Mismatch" or sees a different world.

<!-- sources: cw-mod mapkit/mkmap-format.md, mapkit/godot/README.md ("Build", "What stays out of a map"), mapkit/README.md, docs/ROADMAP.md (section 5: the legal rule; old-format maps), client/game/mapkit_loader.hpp @ 36b1f18 + working tree, 2026-10-08 -->

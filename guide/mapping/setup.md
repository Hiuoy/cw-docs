# Setup

> What to install and switch on once, before your first build.

## What you need

| Thing | Why |
|---|---|
| cw-mod, built and working | The game loads your map through it. See [Install](/guide/install.md). |
| Godot 4, the standard build (not .NET) | The editor. mapkit is tested with 4.7.2. Godot has no installer: unzip and run. |
| `cwlink.exe`, `mkasset.exe` | Built with the mod: `scripts\build.ps1` builds the whole solution. |
| ACTS on your PATH | cwlink compiles the map's level scripts with it. |
| Die Maschine installed | Your map takes its zombies, weapons and shaders from it. |
| A zone trace | The tools cannot read a level zone without it. |

## Steps

1. **Open the project.** In Godot's Project Manager, choose **Import** and pick `mapkit\godot\project.godot` in the cw-mod folder.
2. **Find the dock.** A `mapkit` dock appears on the right. If it does not: Project, Project Settings, Plugins, enable mapkit.
3. **Set the game folder** at the bottom of the dock: the folder that holds `BlackOpsColdWar.exe`. It starts from the `MAPKIT_GAME_DIR` environment variable if you set one.
4. **Record the zone traces.** Add this to `cw-mod.json`, start the game, and start a Die Maschine match once:

   ```json
   { "mapkit_trace": ["zm_silver", "zm_common"] }
   ```

   The game writes `cw-mod\mapkit\trace\zm_silver.mktrace` and `zm_common.mktrace`. You can then take the key out again.
5. **Check the tools.** The dock says which one is missing when you press Build. If Godot does not find `cwlink.exe` or `mkasset.exe`, give their paths in Editor Settings under `mapkit/cwlink` and `mapkit/mkasset`.

## What the zone trace is

A level zone holds about 90 kinds of asset one after the other, and the file does not say where each one starts. While the game loads a zone that `"mapkit_trace"` names, the mod writes those positions down. The trace holds positions only, no game data. It belongs to your game build: record it again after the game is updated.

## Game models in the editor

With `mkasset.exe` and both traces in place, the editor draws the Zombies objects with the game's own models, read from your install and kept in a cache outside the project. The first model takes a moment, because mkasset needs about two seconds to start. They show gray: textures in the editor come later.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| Build says the game folder is missing | Set it at the bottom of the dock. |
| Build says cwlink is missing | Build the mod's solution, or set the path in Editor Settings. |
| Build says the trace is missing | Do step 4. The trace must be of the same game build. |
| Objects show as plain boxes | mkasset is missing, or the `zm_common` trace is. The Output panel says why. |
| The script compile fails | ACTS is not on your PATH. |

<!-- sources: cw-mod mapkit/godot/README.md ("Setup", "Build", "Game models"), mapkit/README.md, docs/mapkit-roadmap.md ("Zone trace"), mapkit/cwlink/main.cpp (usage) @ 36b1f18 + working tree, 2026-10-07 -->

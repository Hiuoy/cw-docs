# Guides

> How to install cw-mod, play with it, script it and build a custom Zombies map. No reverse-engineering knowledge needed.

## What cw-mod gives you

- **The game boots** past its protection, with an in-game menu (press Insert) and a log file.
- **Zombies progression on your PC**: XP, weapon levels and saves, offline and in LAN mode.
- **Two PCs in one match**, with no Activision server involved.
- **Scripts**: your own GSC scripts in a match, and your own Lua in the menus.
- **Custom maps**: build a Zombies map in Godot, press Build, and start it from a CUSTOM MAPS tab in the game.

What is finished and what is not changes often. The [roadmap](https://github.com/Hiuoy/cw-mod/blob/HEAD/docs/ROADMAP.md) has the live status.

## What you need

| Thing | Detail |
|---|---|
| The game | Black Ops Cold War on PC, build **1.34.0.15931218**, which you own. The mod's addresses are for this build only: on another one, features fail or the game crashes. |
| Windows | 64-bit. |
| To build the mod | Visual Studio 2022 or newer with the C++ desktop workload. |
| To play online mode | Python 3 for the local backend. |
| To make maps | Godot 4 and the mapkit tools from the same repository. ACTS to compile scripts. |

## Where to go

| You want to | Read |
|---|---|
| Put the mod in the game | [Install](/guide/install.md) |
| Start the game and read its log | [Running the game](/guide/running.md) |
| Change a setting | [Settings: cw-mod.json](/guide/settings.md) |
| Know what a file in the mod folder is | [File structure](/guide/file-structure.md) |
| Use the in-game menu | [The overlay](/guide/overlay.md) |
| Keep your level and weapon levels | [Progression](/guide/play/progression.md) |
| Play with a friend | [LAN mode](/guide/play/lan.md) or [Online mode](/guide/play/online.md) |
| Play a custom map | [Custom maps](/guide/play/custom-maps.md) |
| Write a script for a match or a menu | [Game scripts](/guide/scripting/gsc.md), [Menu scripts](/guide/scripting/ui-scripts.md) |
| Change the game's text | [Replacing the game's text](/guide/scripting/ui-text.md) |
| Make your own map | [Making a map](/guide/mapping/overview.md), then [Your first map](/guide/mapping/first-map.md) |
| Know what a map can and cannot have | [What you can and cannot make](/guide/mapping/limitations.md) |
| Look up a tool's options | [cwlink](/guide/tools/cwlink.md), [ffinfo](/guide/tools/ffinfo.md), [mkasset](/guide/tools/mkasset.md) |
| Look up a name | [Perks](/guide/lists/perks.md), [Weapons](/guide/lists/weapons.md), [Models](/guide/lists/models.md), [Materials](/guide/lists/materials.md) |
| Fix a problem | [Errors and fixes](/guide/troubleshooting.md), [Questions](/guide/faq.md) |

> [!NOTE]
> Want to know how a feature works inside the game? Each guide links to its page under [How we did it](/re/).

<!-- sources: cw-mod README.md, docs/ROADMAP.md, CONTRIBUTING.md ("Dev setup"), scripts/build.ps1 @ 36b1f18 + working tree, 2026-10-07 -->

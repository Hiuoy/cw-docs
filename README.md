# cw-mod docs

> Call of Duty: Black Ops Cold War Zombies, kept playable on a copy of the game you own. These pages explain how the mod works inside, and how to use it.

cw-mod is a community-owned, open-source client mod for game build **1.34.0.15931218**. It boots the game past its protection, lets two PCs play together without Activision's servers, keeps Zombies progression on your own PC, and loads custom maps built in Godot. The source is at [github.com/Hiuoy/cw-mod](https://github.com/Hiuoy/cw-mod).

## Two ways in

| Path | For | What it holds |
|---|---|---|
| **[How we did it](/re/)** | Reverse engineers | How each feature works inside the game: the functions and their parameters, layouts, bytes, hashes, and the wrong turns on the way. |
| **[Guides](/guide/)** | Players and map makers | Installing, settings, playing together, scripts, building a custom map, the tools, name lists, errors and fixes. |

Both paths share one [glossary](/glossary.md).

## What works today

As of 2026-10-07. The project's [roadmap](https://github.com/Hiuoy/cw-mod/blob/HEAD/docs/ROADMAP.md) is the one place that holds the live status; "Done" there means seen working in the game.

| Part | Status |
|---|---|
| The client: boot, overlay, script loader, settings file | Done |
| Two PCs in one match, in LAN mode or in online mode | Done (both PCs on one home network) |
| Local Demonware backend: login, party, playlists, match launch | Done up to a full online match |
| Zombies progression kept on your PC | Done offline and in LAN mode. Online mode: level and weapon levels pass; the match-end save fix is built, not yet run |
| Custom maps: your own layout, gameplay, meshes, textures, sky, navmesh, map name | Done |
| Custom maps: a map with its own asset set and its own lighting | In progress |

## House rules

> [!IMPORTANT]
> You must own the game. Nothing from the game is hosted in the mod or in these docs: no zones, no extracted assets, no decompiled game scripts. Pages give names, hashes, offsets and counts, and describe behaviour in our own words. See [Legal](/legal.md).

- Everything here is for build 1.34.0.15931218. Another build has other addresses and may have other layouts.
- Retail servers are never a target. The online mode talks to a backend that runs on your own PC.

## More

- [Glossary](/glossary.md)
- [Legal](/legal.md)
- [About these docs](/about.md): how they are made and kept correct

<!-- sources: cw-mod README.md, docs/ROADMAP.md ("At a glance") @ 36b1f18 + working tree, 2026-10-07 -->

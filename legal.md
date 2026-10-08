# Legal

> The rules the project keeps, and what they mean for you as a player, a map maker or a reader.

cw-mod is a preservation and modding project for a game you own. It is not affiliated with, endorsed by or connected to Activision, Treyarch or any other rights holder. Call of Duty and Black Ops Cold War are trademarks of their owners.

## You must own the game

The mod is a client-side change to your own copy of Black Ops Cold War. It does not include the game, and it does not help anyone get the game without buying it.

## What the project never ships

- Game files: zones (`.ff`, `.fd`, `.xpak`, `.xsub`), executables, libraries such as `oo2core_8_win64.dll`.
- Anything extracted from them: models, textures, sounds, decompiled game scripts or menus.
- Publisher data: the playlist files your own install downloaded.
- Memory dumps, analysis databases and zone traces. They are made on your PC, from your install, and stay there.

The tools read what they need from your own install at run time.

## What these docs contain

Names, name hashes, type ids, offsets, sizes, counts, function signatures and descriptions of behaviour, written in our own words. No page reproduces game data or decompiled game code. The scripts quoted in full are the project's own.

## Custom maps

| Thing | May it be shared? |
|---|---|
| The map source (`.mkmap`) and your own textures and models | Yes. It holds only your work; game assets appear in it by name. |
| The built map (`cw-mod/maps/<id>/<id>.ff`) | **No.** The build copies data from your install into that zone. Each player builds the zone on their own PC from their own install. |
| A cloned or repacked retail zone (`cwlink clone`, `cwlink replace`) | **No.** It is a copy of game data, for tests on your own PC. |

A shared map is its source. Whoever plays it builds the zone on their own PC: see [Sharing a map](/guide/mapping/sharing.md).

## Playing together

Players connect to each other directly. The game's Demonware traffic goes to a backend that each player runs on their own PC, with keys and certificates generated on that PC. The client redirects every `demonware.net` name to the local machine, so a modded game has no route to the retail servers.

Public matchmaking and the in-game store are not part of the project.

## Licence

cw-mod is MIT licensed. These docs follow the same licence unless a page says otherwise.

<!-- sources: cw-mod README.md ("Legal"), CONTRIBUTING.md, mapkit/README.md, mapkit/godot/README.md ("What stays out of a map"), docs/ROADMAP.md (section 5, the legal rule), tools/dwserver/README.md @ 36b1f18 + working tree, 2026-10-07 -->

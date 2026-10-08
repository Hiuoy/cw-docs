# Progression

> Zombies XP, your level, weapon levels and saves, kept on your own PC. **Status:** Done offline and in LAN mode (2026-09-23). Online mode: see the table.

## What you get

On its own, the game gives no XP offline or in LAN mode, and it keeps your level and weapon levels on Activision's servers. With `"progression": true` (the default) the mod opens the game's own XP path and keeps the save local:

- XP, level and the level-up popups;
- weapon XP, weapon levels and the attachments they unlock;
- crystals and upgrade tiers;
- the after-action report at the end of a match.

The mod computes nothing itself. The game adds the XP and writes the save.

## Where it stands

| Part | Offline and LAN mode | Online mode |
|---|---|---|
| XP, level, saving | Done | Level kept across restarts: passed 2026-10-07 |
| Weapon levels and attachment unlocks | Done | Passed on the log 2026-10-07 |
| The save of the two progression files at match end | Done | A fix is **built, not yet run in the game** |
| After-action report | Done | Opened without errors on 2026-10-06 |

## Where your save is

| File | Holds |
|---|---|
| `Documents\Call Of Duty Black Ops Cold War\player\*.cgp` | The game's own save files |
| `...\player\cwmod_ae_sync_0.bin` | Your level and weapon levels |
| `<game>\cw-mod\backups\player-<date>-<time>\` | A copy of both, made at every start. The newest 10 are kept. |

To go back to an older save, close the game and copy a backup folder's files over the ones in `player`.

## Checking it works

Open the overlay's Home tab during a match. "Saved XP" is what the save holds, "This match" counts up as you play. If "This match" says **NOT saved: blank start**, the match began without your save loaded, and the mod will not write its result over your real save.

## Menus in a LAN lobby

`"live_menus": true` (the default) makes the menus treat a LAN lobby as an online one, so weapon levels and locks show as they should.

## Unlock all

`"unlock_all": true` answers every "is this locked?" and "do you own this?" question with yes, unlocked and owned. **Status: built 2026-10-07, not yet run in the game.**

| Covered | Not covered |
|---|---|
| Weapons, attachments and equipment behind a level | Which items exist |
| Attachments behind a weapon level | The level and weapon levels shown |
| Camos and reticles behind challenges | Seven Zombies rewards the menus read straight from the save |
| Blueprints, bundles, operators, battle pass rewards | |
| The battle pass itself: owned, top tier | |

It changes answers only. Nothing is written to your save, your progress keeps recording underneath, and setting it back to `false` brings every lock back.

## Limits

- The in-game store and the battle pass's own progress do not work: they need Activision's marketplace. Unlock-all answers the ownership questions instead.
- A save made before you had a player id in `cw-mod.json` carries the old id. Online mode refuses to update such a file at match end; that is what the built fix addresses.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| No XP at all | `"progression"` is `false`, or the Home tab says an engine call did not resolve (wrong game build). |
| Level 1 after every restart in online mode | A build older than 2026-10-07. Update the mod. |
| A match ended and nothing was saved | Look for `NOT saved: blank start` on the Home tab and for `(Progression)` lines in the log. |

**How it works inside:** [Progression](/re/engine/progression.md), [PlayerData](/re/engine/playerdata.md), [Unlock-all](/re/engine/unlock-all.md), [Storage, the store and entitlements](/re/dwemu/storage-entitlements.md).

<!-- sources: cw-mod client/game/zm_progression.hpp, client/game/zm_progression.cpp (save paths, backups), client/game/unlock_all.hpp, client/overlay/tabs/home.cpp, docs/ROADMAP.md (section 4) @ 36b1f18 + working tree, 2026-10-07 -->

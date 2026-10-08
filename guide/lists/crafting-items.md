# Crafting items

> The 19 things a crafting table can sell, by the name an `MkCraftingTable` uses for each.

## How the table works

The crafting table is a shop: it sells a fixed list for salvage, at the game's own prices. For each item the game checks a game setting. Your map can switch items **off**; it cannot add new ones.

The settings are for the whole map. With several tables, an item is sold only if every table has it ticked.

## The names

| `items` entry | What it is | The game setting it switches |
|---|---|---|
| `frag` | Frag grenade | `zmenablefraggrenade` |
| `semtex` | Semtex | `zmenablesemtex` |
| `molotov` | Molotov | `zmenablemolotov` |
| `hatchet` | Hatchet | `zmenablehatchet` |
| `c4` | C4 | `zmenablec4` |
| `decoy` | Decoy grenade | `zmenabledecoygrenade` |
| `stun` | Stun grenade | `zmenablestungrenade` |
| `monkey` | Cymbal monkey | `zmenablecymbalmonkey` |
| `stimshot` | Stim shot | `zmenablestimshot` |
| `self_revive` | Self-revive | `zmenableselfrevive` |
| `turret` | Turret, a support item | `zmenablescorestreakultimateturret` |
| `chopper_gunner` | Chopper gunner, a support item | `zmenablescorestreakchoppergunner` |
| `death_machine` | Death machine, a support item | `zmenablescorestreakdeathmachine` |
| `flamethrower` | Flamethrower, a support item | `zmenablescorestreakflamethrower` |
| `bow` | Bow, a support item | `zmenablescorestreakbow` |
| `napalm` | Napalm strike, a support item | `zmenablescorestreaknapalmstrike` |
| `pineapple_gun` | Pineapple gun, a support item | `zmenablescorestreakpineapplegun` |
| `hand_cannon` | Hand cannon, a support item | `zmenablescorestreakhandcannon` |
| `rcxd` | RC-XD, a support item | `zmenablescorestreakarcxd` |

The "what it is" column goes by the setting's name; the menu's own names may differ. Leaving `items` out of the `.mkmap` means all of them.

## In a script

A level script switches an item off the same way the build does, with the game setting:

```c
setgametypesetting( #"zmenablec4", 0 );
```

The build writes these lines into the generated zones script's `settings()` for you.

## What is not here

"Three parts make one weapon" recipes, as in the game's quests, are a different system built on data bundles. mapkit cannot write those yet.

<!-- sources: cw-mod mapkit/cwlink/main.cpp (kCraftingItems), mapkit/mkmap-format.md (crafting_table), docs/mapkit-plan.md ("Devices": the crafting table) @ 36b1f18 + working tree, 2026-10-08 -->

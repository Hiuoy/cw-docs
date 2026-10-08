# Perks

> The ten perk names an `MkPerkMachine` takes, and which of them a build can place today.

## The names

| Perk | `perk` in the editor and the `.mkmap` | The game's name for its machine | A build places it |
|---|---|---|---|
| Juggernog | `juggernog` | `talent_juggernog` | Yes |
| Speed Cola | `speed_cola` | `talent_speedcola` | Yes |
| Quick Revive | `quick_revive` | `talent_quickrevive` | Yes |
| Stamin-Up | `stamin_up` | `talent_staminup` | Yes |
| Deadshot Daiquiri | `deadshot_dealer` | `talent_deadshot` | Yes |
| Elemental Pop | `elemental_pop` | `talent_elemental_pop` | Yes |
| Tombstone Soda | `tombstone_soda` | `talent_tombstone` | **No** |
| Mule Kick | `mule_kick` | `talent_mulekick` | **No** |
| PhD Slider (the editor says PHD Flopper) | `phd_flopper` | `talent_phdslider` | **No** |
| Death Perception | `death_perception` | `talent_deathperception` | **No** |

The game's name is the `script_noteworthy` of the machine's struct, whose `targetname` is `zm_perk_machine`. A script finds a machine by those two keys.

## Why only six

A build does not make perk machines. It moves the six that Die Maschine places to where you put yours. So:

- each of the six can stand in your map **once**;
- the other four are skipped, and the build output says so.

In the editor, Tombstone and Mule Kick show their machines, and PHD Flopper and Death Perception stay plain boxes: those two machines live in other maps' zones.

## The other four, another way

`MkWunderfizz` places Der Wunderfizz, which sells any perk. It is not limited to six, and you can place as many as you like.

## Power

| The map has | Perk machines |
|---|---|
| No `MkPowerSwitch` | Work from the first round |
| An `MkPowerSwitch` | Wait for the power. Quick Revive still works in a solo game. |

## Good to know

- A perk machine blocks the player with a shape around its model. That was built on 2026-10-05 and is not yet tested in the game.
- Prices are the game's own.

<!-- sources: cw-mod mapkit/cwlink/main.cpp (kPerks), mapkit/mkmap-format.md (perk_machine), mapkit/godot/README.md ("Build", "The debug map", "Game models"), the perk structs of Die Maschine's entity list (ffinfo --entities-json, names only) @ 36b1f18 + working tree, 2026-10-08 -->

# Gameplay objects

> Doors, perk machines, the Mystery Box, wall buys and the other machines: what each node does and what limits it has. **Status:** Done (2026-09-27; power switch and exfil 2026-09-29).

Put each object's origin on the floor. Its box is its size in the game and its arrow is the way it faces.

## Doors

| Node | Settings |
|---|---|
| `MkDoor` | `kind`: `door` or `debris`. `cost`. `opens`: the zones it opens, comma-separated. `size`: the box where it is bought. `model`: the door itself. `needs_power`: it opens by itself when the power comes on, and is not bought. |

The **model** is what blocks the way, with its own collision, and it sinks into the floor when the door is bought. Pick a model that fills the opening: a narrower one leaves a gap. Empty uses Die Maschine's metal door.

## Machines you can place freely

As many as you like, each working from the first round unless it waits for power.

| Node | What it is | Settings |
|---|---|---|
| `MkPackAPunch` | Pack-a-Punch: tiers 1 to 3 and ammo mods. No quest needed. | none |
| `MkArsenal`, `MkArmorStation` | The same machine: armor and weapon rarity upgrades | `needs_power` |
| `MkCraftingTable` | Equipment, support items and self-revives for salvage | `items`: what it sells |
| `MkAmmoCache` | An ammo crate | none |
| `MkWunderfizz` | Der Wunderfizz: any perk | none |

The crafting table's item list is one list for the whole map. With several tables, an item is sold only if every table has it. The names: [Crafting items](/guide/lists/crafting-items.md).

## Machines with a limit

These are Die Maschine's own objects, moved to where you put yours. You can place only as many as Die Maschine has.

| Node | Setting | Limit |
|---|---|---|
| `MkPerkMachine` | `perk` | Six perks, once each. See [Perks](/guide/lists/perks.md). |
| `MkWallBuy` | `weapon`, `cost` | Twelve weapons, once each. The price is the game's own. See [Weapons](/guide/lists/weapons.md). |
| `MkMysteryBox` | `start_here` | As many locations as Die Maschine has. The weapons in the box are Die Maschine's. |

A box location blocks like the box even while the box is elsewhere and only the bear sits there.

## Power

| Node | Effect |
|---|---|
| `MkPowerSwitch` | The power switch, used from its front. One per map. |

| The map has | Then |
|---|---|
| No power switch | Everything is powered from the start. |
| A power switch | Perk machines, Armor Stations and `needs_power` doors wait for it. Quick Revive works without it in a solo game. Those doors open by themselves when the power comes on. |

Turn `needs_power` off on an Armor Station to have it work from the start.

## Exfil

| Node | Settings |
|---|---|
| `MkExfil` | Where the helicopter lands, facing its arrow. `hold_seconds`. `attack_radius` and `attack_height`: where zombies attack from. `zones`: the zones players must reach; empty means the zones the landing point is in. `radio_live_at_start`: for testing. |
| `MkExfilRadio` | The radio players call the exfil at. |

One of each per map. The radio works from round 10 and then every fifth round, for two minutes. `radio_live_at_start` makes it work from the first round so you can test.

## Limits

- Prices of machines are the game's own.
- The exfil's zombie count and the rounds it opens are the game's own.
- That perk machines and box locations block the player was built on 2026-10-05 and is not yet tested in the game.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The build output says a perk or wall buy was skipped | It is not one of Die Maschine's, or you placed it twice. |
| A machine faces the wall | Turn the node: its arrow is its front. |
| A door leaves a gap | Its model is narrower than the opening. Pick a wider model. |
| A door never opens | `needs_power` is on and the map has no power switch. |
| The exfil radio does nothing | It is not round 10 yet. Use `radio_live_at_start` for a test. |

<!-- sources: cw-mod mapkit/godot/README.md ("The objects", "Build", "The debug map"), mapkit/mkmap-format.md ("entities"), docs/mapkit-plan.md ("Devices", "P1 step 3"), docs/ROADMAP.md ("Open and parked") @ 36b1f18 + working tree, 2026-10-07 -->

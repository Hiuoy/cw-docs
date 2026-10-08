# The editor

> The mapkit plugin for Godot 4: its dock, its checks, the walk-through and the units. **Status:** Done.

## The dock

| Control | Does |
|---|---|
| Name and **New map** | Makes a new map from the template |
| **Check** | Lists problems. Red stops the export, yellow is advice. Click a line to select its node. |
| **Export** | Writes `build\<map>.mkmap` in the Godot project, and your textures beside it |
| **Build** | Exports, then runs cwlink, which writes the map into `<game>\cw-mod\maps\<id>\` |
| Game folder | Where the game is. Check also warns when your map's name is one the game ships. |

## The nodes

Add them with Add Node and search for "Mk". Everything under the `MkMap` root is exported.

| Group | Nodes | Page |
|---|---|---|
| Geometry | `MkBrush`, `MkMesh` | [Geometry](/guide/mapping/geometry.md) |
| Areas and spawns | `MkZone`, `MkPlayerSpawn`, `MkZombieSpawner`, `MkBarrier` | [Zones and spawns](/guide/mapping/zones-spawns.md) |
| Machines and doors | `MkDoor`, `MkPerkMachine`, `MkWallBuy`, `MkMysteryBox`, `MkPackAPunch`, `MkArsenal`, `MkArmorStation`, `MkCraftingTable`, `MkAmmoCache`, `MkWunderfizz`, `MkPowerSwitch`, `MkExfil`, `MkExfilRadio` | [Gameplay objects](/guide/mapping/gameplay-objects.md) |
| Decoration | `MkProp` | [Props and models](/guide/mapping/props-models.md) |
| Sound | `MkAmbientRoom` | [Sound](/guide/mapping/sound.md) |
| Light | `MkLight`, and Godot's own `WorldEnvironment` and `DirectionalLight3D` | [Sky, sun and fog](/guide/mapping/sky-sun-fog.md) |

## Gizmos

- An object's **box** is its size in the game. Its **arrow** is the way it faces.
- Zones, ambient rooms and doors are volumes. Drag the handles on their faces to resize them: one face moves and the opposite one stays. Hold Shift to turn snapping off.
- Put every object's origin on the floor.

## The walk-through

Press F6 (Run Current Scene). You start at the first player spawn and walk on your brushes and meshes. Speed, jump height and eye height are the game's.

## Units

Godot works in meters with Y up. The game works in inches with Z up and X forward. Export converts for you.

| Thing | Godot | Game units |
|---|---|---|
| One meter | 1 m | 39.37 |
| A player's height | 1.83 m | 72 |
| A perk machine's box | about 2.3 m | about 90 |
| A new door's width | 2.5 m | about 98 |
| Grid lines on a brush | | one every 16, a heavier one every 128 |

## What Check enforces

- The map's name is valid and is not the name of a map the game ships.
- There is at least one brush, one player spawn and one zombie spawner.
- Every zone that a spawner, a barrier or a door names exists, and zone names are unique.
- Every ambient room names a room.
- Every wall buy has a weapon and every prop has a model.

Check also lists what the export will skip, such as a CSG shape that is not a box, and warns about a second sun.

## Limits

- Game names (weapons, materials) are typed in. Models have a picker.
- Game models show gray in the editor.
- Nothing is sent to a running game. Close the game, build, start it again.

<!-- sources: cw-mod mapkit/godot/README.md, mapkit/mkmap-format.md ("Rules a reader enforces"), docs/mapkit-roadmap.md (M5) @ 36b1f18 + working tree, 2026-10-07 -->

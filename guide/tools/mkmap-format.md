# The .mkmap format

> The map source that the editor writes and cwlink reads: JSON, format version 1. Any other editor can write it too.

A `.mkmap` holds only the creator's own work. Game assets appear by name, never as data.

## Space and numbers

| Thing | Rule |
|---|---|
| Units | Game units: 1 unit is 1 inch |
| Axes | Right-handed: X forward, Y left, Z up |
| Positions | Relative to the map's origin |
| Angles | `[pitch, yaw, roll]` in degrees. Pitch is positive looking down. |
| Rounding | Positions to 0.001, angles to 0.01 |

## The file

```json
{
  "mkmap": 1,
  "generator": "mapkit-godot 0.1",
  "units": "inch",
  "axes": "x forward, y left, z up",
  "map": { "name": "zm_template", "title": "Template", "author": "mapkit", "mode": "zm" },
  "brushes": [],
  "meshes": [],
  "sky": {},
  "lighting": {},
  "entities": []
}
```

| Key | Meaning |
|---|---|
| `mkmap` | Format version. A reader refuses a version it does not know. |
| `generator` | The tool that wrote the file. For information. |
| `map.name` | The map's id and zone name: `zm_`, then `a-z`, `0-9`, `_`; at most 48 characters |
| `map.title` | The name players see |
| `map.mode` | `zm`, the only mode so far |

`meshes`, `sky` and `lighting` are optional.

## brushes

A brush is a box that may be turned, scaled or sheared: a centre and three half-axis vectors. Its eight corners are `center ± half_axes[0] ± half_axes[1] ± half_axes[2]`.

```json
{
  "path": "Geometry/Floor",
  "center": [255.906, 0.0, -9.843],
  "half_axes": [[0.0, -236.22, 0.0], [0.0, 0.0, 9.843], [-511.811, 0.0, 0.0]],
  "material": "",
  "solid": true,
  "rendered": true
}
```

| Key | Meaning |
|---|---|
| `path` | Where it sits in the editor's tree. Used in messages only. |
| `material` | A game material by name. `""` is the default. |
| `solid` | Collides with players and zombies |
| `rendered` | Is drawn. `solid` without `rendered` is an invisible wall. |

## meshes

The creator's own geometry. A mesh has parts, and a part has triangle surfaces, **in map space**: the node's transform is already applied.

| Key | Meaning |
|---|---|
| `collision` | `faces`: every triangle is solid, as a slab 4 units deep behind its front. `hull`: one convex shape per part. `none`. |
| `game_material` | A game material for every surface that names none. `""` keeps the surfaces' own look. |
| `parts[].surfaces[]` | The surfaces, with the keys below |

| Surface key | Meaning |
|---|---|
| `material` | The editor material's name. If it is a game material, the surface draws with it. |
| `color_texture` | The surface's own look: a `.dds` path relative to the `.mkmap` (BC1, BC3, BC7 or RGBA8, with mip levels). Its alpha is the opacity. |
| `normal_texture` | A `.dds` (BC7 or RGBA8) in the game's form: x and y in red and green **with y pointing down the image**, blue for the roughness that each mip level's spread of normals adds |
| `roughness_texture` | Roughness in red (BC4 or R8): 0 smooth, 1 rough |
| `metal_texture` | Metalness in red (BC4 or R8). The surface then draws with a metal material. |
| `alpha` | `opaque`, `clip` (cut out) or `blend` (see-through, drawn as glass) |
| `emission_texture`, `emission_energy` | The light the surface gives off, and its strength |
| `vertices`, `normals`, `uvs` | Per vertex. `normals` and `uvs` may be empty. |
| `triangles` | Index triples, **clockwise seen from the front** |

## sky

```json
"sky": { "image": "zm_template_textures/sky_13e836a24310ff26.dds", "energy": 1.0 }
```

| Key | Meaning |
|---|---|
| `image` | An equirectangular panorama, twice as wide as high, one level, already turned to the game's directions: the column at `u` faces yaw `135° − 360° × u`. BC6H for HDR, else BC7. |
| `energy` | Brightness. 1 is as bright as the base map's own sky. |

## lighting

```json
"lighting": {
  "sun": { "direction": [-0.9397, 0.0, -0.342], "color": [1.0, 0.523, 0.263], "energy": 1.0 },
  "fog": { "enabled": true, "start": 0.0, "halfway": 1500.0, "base_height": 0.0,
           "halfway_height": 300.0, "color": [0.75, 0.8, 0.9], "opacity": 1.0 }
}
```

| Key | Meaning |
|---|---|
| `sun.direction` | The way the sun's light travels, a unit vector |
| `sun.color`, `sun.energy` | Linear colour 0 to 1; 1 is the base map's daytime sun |
| `fog.enabled` | `false` removes the base map's fog too |
| `fog.start`, `fog.halfway` | Where the fog starts, and how far past that it covers half the view |
| `fog.base_height`, `fog.halfway_height` | Where it is thickest, and how far above that it thins by half |
| `fog.color`, `fog.opacity` | Its colour as shown, and the most it covers |

## entities

```json
{
  "path": "Gameplay/Juggernog",
  "class": "perk_machine",
  "origin": [-137.795, -212.598, 0.0],
  "angles": [0.0, 90.0, 0.0],
  "props": { "perk": "juggernog" }
}
```

`origin` is the object's floor point. Volumes also carry `bounds`: `{ "min": [...], "max": [...] }`, in the entity's own axes.

| `class` | `props` |
|---|---|
| `player_spawn` | `player`: 1 to 4, 0 is any |
| `zombie_spawner` | `zone`, `kind`: `ground` or `barrier` |
| `zone` (volume) | `zone_name`, `active_at_start` |
| `ambient_room` (volume) | `room`, `priority` |
| `door` (volume) | `kind`: `door` or `debris`; `cost`; `opens`: zone names; `model`; `needs_power` |
| `barrier` | `zone`, `kind`: `wood` or `concrete` |
| `wall_buy` | `weapon`, `cost` |
| `perk_machine` | `perk`: see [Perks](/guide/lists/perks.md) |
| `mystery_box` | `start_here` |
| `pack_a_punch`, `ammo_cache`, `wunderfizz`, `exfil_radio`, `power_switch` | none |
| `arsenal`, `armor_station` | `needs_power` |
| `crafting_table` | `items`: see [Crafting items](/guide/lists/crafting-items.md) |
| `exfil` | `hold_seconds`, `attack_radius`, `attack_height`, `zones`, `radio_live_at_start` |
| `prop` | `model`, `solid`, `scale` |
| `light` | `color`, `intensity`, `radius` |

The class names are mapkit's own, not the game's.

## Rules a reader enforces

- `map.name` is valid and is not the name of a shipped map.
- At least one brush, one `player_spawn` and one `zombie_spawner`.
- Every zone a spawner, barrier or door names exists; `zone_name` values are unique.
- Every `ambient_room` names a `room`; every `wall_buy` has a `weapon`; every `prop` has a `model`.

<!-- sources: cw-mod mapkit/mkmap-format.md @ 36b1f18 + working tree, 2026-10-08 -->

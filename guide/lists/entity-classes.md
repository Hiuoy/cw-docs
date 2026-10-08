# Entity classes

> What your objects become in the game, and the entity classes of a retail Zombies map. For scripters who need to find an object from a level script.

## What your objects become

Scripts find entities by their keys. This is what a build writes for each node.

| Your node | In the game | Keys a script can use |
|---|---|---|
| `MkPlayerSpawn` | `script_struct` | `targetname` `initial_spawn_points`, `script_noteworthy` `player_<n>` |
| `MkZone` | `info_volume`, in the trigger list | `targetname` = the zone's name, `script_noteworthy` `player_volume` |
| `MkZombieSpawner` | `script_struct` | `targetname` `<zone>_spawns`, `script_noteworthy` `riser_location` |
| `MkBarrier` | A `zbarrier_...` entity with its helper structs | `targetname` and `script_string` `mapkit_barrier_<n>` |
| `MkDoor` | `trigger_use_touch` and a `script_model` it targets | Trigger: `targetname` `zombie_door`, `script_flag` `mapkit_door_<n>`. Model: `script_noteworthy` `model_clip` |
| `MkPerkMachine` | `script_struct` | `targetname` `zm_perk_machine`, `script_noteworthy` `talent_<perk>` |
| `MkMysteryBox` | Content struct | `content_key` `magicbox_zbarrier` |
| `MkWallBuy` | Two content structs | `content_key` `wallbuy_chalk` (`script_noteworthy` = the weapon) and `wallbuy_gun` |
| `MkPackAPunch` | Content struct | `content_key` `weapon_machine_spawn` |
| `MkArsenal`, `MkArmorStation` | Content struct | `content_key` `armor_machine` |
| `MkCraftingTable` | Content struct | `content_key` `crafting_table` |
| `MkAmmoCache` | Content struct | `content_key` `ammo_cache_spawn` |
| `MkWunderfizz` | Content struct | `content_key` `perk_machine_choice` |
| `MkPowerSwitch` | `trigger_use`, a struct and the console model | Trigger: `targetname` `use_elec_switch` |
| `MkExfil` | Content structs and helicopter path nodes | `content_key` `heli_spawn`, `exfil_loc`, `landing_zone`, `smoke` |
| `MkExfilRadio` | `script_struct` | `targetname` `exfil_radio`, `content_key` `beacon` |
| `MkProp` | `script_model` | Not solid: `targetname` `mapkit_prop_nonsolid` |
| `MkAmbientRoom` | `trigger_multiple`, in the trigger list | `targetname` `ambient_package`, `script_ambientroom` |
| Rendered brushes and meshes | One `script_model` | Its model is `mapkit_<map>` |

The build also makes a `player_respawn_point` struct in every zone, and two minimap corners around your zones.

## Content structs

The Mystery Box, wall buys and the machines are "content" objects. The shared Zombies scripts reach them through a chain, each link naming its parent in `target`:

```text
content_destination  <-  content_location  <-  content_instance  <-  content_struct
```

A struct without its chain spawns nothing. A build keeps the chains for you.

| Instance (`content_script_name`) | Its structs (`content_key`) |
|---|---|
| `magicbox` | `magicbox_zbarrier` |
| `wallbuy` | `wallbuy_chalk`, `wallbuy_gun` |
| `weapon_machine` | `weapon_machine_spawn` |
| `armor_machine` | `armor_machine` |
| `crafting_table` | `crafting_table` |
| `ammo_cache` | `ammo_cache_spawn` |
| `perk_machine_choice` | `perk_machine_choice` |
| `exfil` | `heli_spawn`, `exfil_loc`, `landing_zone`, `smoke`, `exfil_spawns`, and the two path starts |

## The classes of a retail map

Die Maschine's lists hold 2,707 entities: 2,380 in the entity list and 327 triggers.

| Class | Count | What it is | In a mapkit map |
|---|---|---|---|
| `script_struct` | 1,611 | Everything scripts look up: spawns, machine places, quest points | The ones your objects need |
| `info_volume` | 187 | Zone volumes and other volumes | One per zone |
| `script_model` | 140 | Scripted models: doors, quest props | Your props, doors and the map's own model |
| `node_pathnode`, `node_exposed`, `node_negotiation_*` | 286 | AI path nodes | Left out: they cannot be authored |
| `perf_camera`, `volume_performance`, `volume_fpstool`, `export_volume`, `occlusion_override` | 113 | Tool markers | Left out |
| `trigger_multiple` | 82 | Area triggers, ambient rooms among them | Your ambient rooms |
| `scriptbundle_scene`, `scriptbundle_zmintel`, `scriptbundle_itemspawnlist` | 65 | Placed scenes, intel, a supply stash | Left out |
| `info_vehicle_node`, `info_vehicle_node_rotate` | 92 | Helicopter paths | Kept; the exfil's are moved |
| `script_origin` | 26 | Script points, the minimap corners among them | The minimap corners |
| `zbarrier_zmcore_t8_basicwoodbarrier` | 24 | Wooden window barriers | One per wood `MkBarrier` |
| `zbarrier_zmcore_basicwallbarrier_concrete_silver` | 1 | The concrete wall barrier | One per concrete `MkBarrier` |
| `trigger_damage`, `trigger_use_touch`, `trigger_use`, `trigger_box`, `trigger_hurt` | 58 | Quest, door, trap and hazard triggers | Your doors and the power switch |
| `actor_spawner_*` | 5 | The zombie spawn templates | Kept. See [Zombie types](/guide/lists/zombies.md). |
| `navmesh_extra_verts`, `nav_volume` | 12 | Navmesh helpers | Left out |
| `worldspawn` | 1 | Level settings: gravity, wind, lighting names | Kept |
| `reflection_probe`, `volume_outdoor`, `heli_height_lock`, `script_vehicle` | 4 | One each | Left out |

## Keys you will meet

| Key | On | Meaning |
|---|---|---|
| `targetname` | Most | The name scripts look an entity up by |
| `target` | Structs, triggers | The `targetname` this one points at |
| `script_noteworthy` | Structs, models | A second name, read by the script that owns the object |
| `script_string`, `script_int`, `script_flag` | Structs, triggers | Values a script reads: a mode, a number, a flag to set |
| `model` | Models, some structs | A model, by name hash |
| `modelscale` | Models | One scale for the whole model |
| `zombie_cost` | Door triggers | The price |
| `variantName` | Content structs | The name the content chain links by |

<!-- sources: cw-mod docs/mapkit-roadmap.md ("Map entities"), docs/mapkit-plan.md ("P1 step 2", "Devices", "P1 step 3", "P2 step 1", "Leftovers"), docs/mapkit-map-anatomy.md (section 5), mapkit/cwlink/main.cpp, Die Maschine's entity and trigger lists (ffinfo --entities-json, class names, key names and counts only) @ 36b1f18 + working tree, 2026-10-08 -->

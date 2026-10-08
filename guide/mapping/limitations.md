# What you can and cannot make

> Every part of a map carries one of four tags. Read this page before you plan a map. As of 2026-10-07.

| Tag | Meaning |
|---|---|
| **Yours** | You create it in the editor. It is in the map's source. |
| **Copied at build** | cwlink copies it from your own install into your map's zone. This is why a built zone is never shared. |
| **Borrowed** | The game loads its own copy while your map runs. |
| **Not yet** | Not possible today. |

## The world

| Thing | Tag | Note |
|---|---|---|
| Boxes (`MkBrush`), solid or not, drawn or not | **Yours** | Other CSG shapes and subtraction do not export. |
| Your own models (`.glb`) | **Yours** | Drawn with their own textures; solid face by face, as a hull, or not at all. |
| Colour, normal, roughness and metal textures; cut-out and see-through | **Yours** | See-through always draws as glass. |
| Glow (emission) | **Not yet** | It exports, but no glow shows in the game. Parked. |
| UV scale and offset, triplanar, ORM textures, shader materials | **Not yet** | Tile in Blender instead. A shader material draws with the default. |
| Game materials, by name | **Borrowed** | Only materials Die Maschine's zone stores. |
| Game models as props | **Borrowed** | Only models of Die Maschine's and the common zone. One even scale per prop. |
| Hundreds of props | **Not yet** | Props are script entities. The retail way to place static models is parked. |
| The safety floor under the map | **Copied at build** | Die Maschine's terrain, flattened. |

## Sky and light

| Thing | Tag | Note |
|---|---|---|
| The sky panorama and its brightness | **Yours** | The sky's rotation is not exported. |
| The sun: direction, colour, strength | **Yours** | One sun. |
| Fog: colour, density, height | **Yours** | |
| Ambient light, reflections, exposure | **Copied at build** | Die Maschine's lighting, baked for its own buildings. Its lamps and its baked sun shadow are removed. |
| Your own lamps (`MkLight`) | **Not yet** | Editor preview only. |
| Baked shadows and reflection probes of your own geometry | **Not yet** | Open. |
| Colour grading | **Copied at build** | Die Maschine's. |

## Gameplay

| Thing | Tag | Note |
|---|---|---|
| Zones, player spawns, zombie spawners | **Yours** | |
| Doors and debris, bought or opened by power | **Yours** | The door model is a game model that has its own collision. |
| Wood barriers | **Yours** | Zombies tear the boards down. Players cannot pass. |
| Concrete barriers | **Not yet** | It asks for power and stays. Parked. |
| Perk machines | **Borrowed** | Only Die Maschine's six, once each: Tombstone, Mule Kick, PHD Flopper and Death Perception are skipped. |
| Wall buys | **Borrowed** | Only Die Maschine's twelve weapons, once each. Prices are the game's own. |
| Mystery Box locations | **Borrowed** | As many as Die Maschine has. The weapon list is Die Maschine's. |
| Pack-a-Punch, Arsenal, Armor Station, crafting table, ammo crate, Der Wunderfizz | **Yours** to place | As many as you like. Prices are the game's own. |
| Which items a crafting table sells | **Yours** | One list for the whole map. |
| Power switch | **Yours** | |
| Exfil: landing point, hold time, attack area | **Yours** | The helicopter flight is Die Maschine's, moved. One exfil point. |
| Exfil zombie count, the round it opens | **Not yet** | |
| Which zombie type a spawner makes | **Not yet** | The round logic decides. |
| New perks, weapons or zombie types | **Not yet** | No tool writes those assets. |
| Quests, voice lines, music, the intro cinematic | **Not yet** | |

## Movement and sound

| Thing | Tag | Note |
|---|---|---|
| The navmesh | **Yours** | Generated from your collision at build. |
| Mantles, jumps, moving doors and props in the navmesh | **Not yet** | Parked. |
| How each room sounds (`MkAmbientRoom`) | **Yours** to place | You pick one of Die Maschine's six rooms. |
| A room with your own sound settings | **Not yet** | |
| Placed sound emitters, placed effects | **Not yet** | |
| Wind, weather | **Not yet** | See [Effects and wind](/guide/mapping/effects-wind.md). |

## The map as a whole

| Thing | Tag | Note |
|---|---|---|
| The map's name, title, author | **Yours** | |
| The level script | **Yours** | mapkit ships one. You can edit it. |
| The zombies, weapons, machines, menus and shared scripts | **Borrowed** | From the common Zombies zone. |
| The sky's shaders | **Borrowed** | From one of Die Maschine's zones, which still loads. |
| The picture in the menu, the loading screen, the minimap picture | **Not yet** | Still Die Maschine's. |
| A change to the map while the game runs | **Not yet** | Close the game, build, start it again. |

## Built, not yet seen working

| Thing | State |
|---|---|
| Perk machines, box locations and barriers that block players | Built 2026-10-05, not yet tested in the game |
| Zombies walking around props; the collision of scaled props | Not yet checked in the game |

<!-- sources: cw-mod mapkit/godot/README.md ("Build", "The objects"), docs/ROADMAP.md (section 5, "Open and parked"), docs/mapkit-map-anatomy.md (section 2), mapkit/mkmap-format.md @ 36b1f18 + working tree, 2026-10-07 -->

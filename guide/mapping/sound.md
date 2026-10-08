# Sound

> How each part of your map sounds: its echo, its room tone and the tail of a gunshot. **Status:** Done for placing rooms (passed in the game 2026-10-03). Rooms with your own settings are parked.

## Ambient rooms: MkAmbientRoom

An ambient room is a box. While a player is inside it, the game uses that room's sound: its reverb, its quiet background tone, and indoor or outdoor gunfire tails.

| Setting | Effect |
|---|---|
| `room` | Which room it sounds like: one of the rooms in Die Maschine's sound bank, by name |
| `priority` | Where two rooms overlap, the higher number wins |
| `size` | The box. Drag its face handles. |

Cover each indoor space with one. Outside every room the map plays the sound bank's default room.

## The rooms you can pick

The `room` field suggests the six that Die Maschine's own areas use, from `zm_nacht_interior` to `zm_nacht_bunker_small_room`. The list: [Ambient rooms](/guide/lists/ambient-rooms.md).

Listen and choose: the names are only a hint. A name the sound bank does not have plays the default room.

## How it reaches the game

The build writes one trigger per ambient room into your map, the same kind Die Maschine uses for its own rooms. It also copies Die Maschine's sound bank into your map's zone, so its rooms, ambience and level sounds are there without Die Maschine's zones loaded.

## The catch: baked acoustics

Die Maschine also ships acoustics that were measured from its own walls. In a room that does not override them, they change the echo and the muffling from point to point, and they follow **Die Maschine's** walls, not yours. `zm_nacht_bunker_hallways` seems to be such a room.

If a room sounds wrong as you walk through it, try another room name. For a whole map without those acoustics, build with `cwlink build ... --no-acoustics`: reverb and muffling then come from the rooms alone. That switch has not been tried in the game yet.

## Limits

| Thing | State |
|---|---|
| A room with your own reverb settings | Not yet |
| Sounds placed in the map (a humming machine, a dripping pipe) | Not yet |
| Music, voice lines | Not yet |
| Footsteps and bullet impacts | The game's own, by the surface's material |

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| Everything sounds like one big room | No ambient room covers that spot, or its `room` is not a name the bank has. The build output says so. |
| The echo changes as you walk | Baked acoustics. See above. |
| Two rooms fight where they meet | Give one a higher `priority`. |

<!-- sources: cw-mod mapkit/godot/README.md ("The objects": MkAmbientRoom; "The debug map"), mapkit/mkmap-format.md (ambient_room), mapkit/cwlink/main.cpp (usage: --no-acoustics), docs/ROADMAP.md ("Ambient rooms", "Die Maschine's baked acoustics"), docs/mapkit-map-anatomy.md (sections 4.8 and 6) @ 36b1f18 + working tree, 2026-10-08 -->

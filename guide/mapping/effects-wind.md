# Effects, wind and weather

> The short version: the editor has no node for any of them yet. This page says what a built map has, and what a level script can try. As of 2026-10-08.

## Where things stand

| Thing | In a built map | From the editor |
|---|---|---|
| Placed ambient effects (smoke, sparks, drifting snow) | None. The map's list is written empty. | **Not yet** |
| Fog | Yours | Yes: see [Sky, sun and fog](/guide/mapping/sky-sun-fog.md) |
| Wind | Die Maschine's, copied | **Not yet** |
| Weather | None | **Not yet** |
| Lightning, a second sky for another mood | None | **Not yet** |
| Effects that belong to a machine, a weapon or a zombie | Work as in the game | Nothing to do |

## Effects

Die Maschine places 2,482 ambient effects of 139 kinds through one list in its zone, and its snow and mist come from that list, from effect volumes and from its level script. A map of yours carries an empty list, so none of them play. That is on purpose: they would play at Die Maschine's positions.

The effects of the things you place are not in that list. They belong to those things' own scripts in the common Zombies zone, which run as they do in the game: muzzle flashes, a zombie rising from the ground, a machine's own lights.

**From a level script:** the game's scripts play an effect at a point by name (`playfx`), and your map's level script can do the same. mapkit adds nothing for it and it is not tested. The names we have are on [Effects](/guide/lists/effects.md); only about 1 in 20 is known by name.

## Fog

Set fog in the editor. A script cannot change it here: the script fog calls (`setexpfog`, `setvolfog`) change nothing in this build, because the frame's fog is read from the map's lighting.

## Wind

Wind moves foliage and some particles. A built map holds a copy of Die Maschine's wind definition, and its level settings keep Die Maschine's wind keys, so the wind is Die Maschine's. There is no setting for it in the editor.

## Weather and lightning

There is none. Die Maschine's lighting has four states: day, two dark ones for the Dark Aether (one of them with lightning, going by its sky's name), and a black one. A map runs in the day state, and a build writes your sky, sun and fog into that state only. The game switches states from a level script (`setlightingstate`); with a custom map that is not tested.

## What is planned

| Step | State |
|---|---|
| A node that places an effect | Open. The list's format is known: 80 bytes per placed effect. |
| Effect volumes | Open. Their shape is read, their meaning is a guess. |
| Your own wind | Open |

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| No snow or mist as in Die Maschine | Expected: those were its placed effects. |
| A scripted fog call does nothing | Expected. Set fog in the editor. |

<!-- sources: cw-mod docs/mapkit-research-parked.md ("Level effects, the minimap, and script bundles"; "P4 lighting"), docs/mapkit-plan.md ("P4 sky and lighting, step 2": script fog), docs/mapkit-map-anatomy.md (sections 4.3 and 6), docs/ROADMAP.md (P6 step 2a) @ 36b1f18 + working tree, 2026-10-08 -->

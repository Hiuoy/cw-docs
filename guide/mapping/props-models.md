# Props and models

> Decorate your map with the game's own models, picked from a list with pictures. **Status:** Done (2026-09-28): props are drawn and solid.

## MkProp

A prop is one of the game's models at a place you choose.

| Setting | Effect |
|---|---|
| `model` | The model: its name, or `#` and its hash. Use **Pick**. |
| `solid` | Players and zombies collide with it. |

Turn it any way you like and scale it evenly: one scale for all three axes.

## The model picker

A model field (`MkProp.model`, `MkDoor.model`, `MkWallBuy.weapon`) shows a picture of its model and a **Pick** button.

1. Press **Pick**. A window lists every model the tools can read from your install, about 4,700 of them.
2. Choose a category on the left, such as "Doors & gates" or "Foliage & rocks", or type in the search box. It searches names and hashes.
3. Double-click a model, or select it and press **Use this model**. Ctrl+Z undoes it.

A model's picture is drawn the first time it scrolls into view and is kept in a cache. Pictures are gray: textures in the editor come later.

The names alone: [Models](/guide/lists/models.md).

## What the picker needs

- `mkasset.exe` and the game folder, as in [Setup](/guide/mapping/setup.md).
- The traces of both `zm_silver` and `zm_common`. The perk machines come from `zm_common`.

The editor runs mkasset in the background while it is open. The models it reads go to a cache in Godot's user data folder, outside the project, so no game data ends up in your map's files.

## How a prop behaves in the game

| Thing | Behaviour |
|---|---|
| Drawing | The game's own model with its own materials |
| Collision of a solid prop | One shape wrapped around the model. A hollow model (a table, an arch) is filled in: you cannot walk under or through it. |
| A prop that is not solid | Players and zombies pass through it. |
| Navmesh | Solid props are part of the collision the navmesh is built over. |

## Which models you can use

Only models that Die Maschine's zone or the common Zombies zone hold. The picker lists only those. A model from another map's zone is not loaded in your map, so it would not draw.

That is also why two perk machines stay plain boxes in the editor: PHD Flopper and Death Perception have their machines in other maps' zones.

## Limits

- A prop is a script entity. A few dozen are fine. Hundreds are not what this path is for: the retail way to place static models is parked.
- One even scale per prop.
- About 7 in 100 models have no known name. They are listed by hash and work the same.
- Not yet checked in the game: zombies walking around props, and the collision of scaled props.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The Pick window is empty | mkasset did not start, or a trace is missing. Godot's Output panel says why. |
| A model shows as a hash | It has no known name. It still works. |
| A prop does not draw in the game | Its model is not in Die Maschine's or the common zone. Pick it from the picker. |
| You walk through a prop | `solid` is off. |
| You cannot walk under a table | Solid props are filled in. Turn `solid` off and block the legs with invisible brushes. |

<!-- sources: cw-mod mapkit/godot/README.md ("Game models", "Build", "The objects"), mapkit/README.md (mkasset), mapkit/godot/addons/mapkit/mk_model_catalog.gd, docs/ROADMAP.md (P2; "Open and parked") @ 36b1f18 + working tree, 2026-10-08 -->

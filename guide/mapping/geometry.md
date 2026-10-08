# Geometry

> The walls, floors and shapes of your map: boxes for a block-out, your own models for the real thing. **Status:** Done (brushes 2026-09-26, own meshes 2026-09-28).

## Boxes: MkBrush

Add an `MkBrush` for a floor, a wall or a platform. Size it with its box handles or with `size`, and turn it any way you like.

| Setting | Effect |
|---|---|
| `game_material` | The game material it is drawn with, by name. Empty uses the default, a cinder-block wall. See [Materials](/guide/lists/materials.md). |
| `solid` | Players and zombies collide with it. |
| `rendered` | It is drawn. |

| `solid` | `rendered` | You get |
|---|---|---|
| on | on | A normal wall |
| on | off | An invisible wall |
| off | on | A wall you can walk through |

A plain Godot `CSGBox3D` exports the same way. Other CSG shapes and CSG subtraction do not export; Check lists what it will skip.

## Your own models: MkMesh

For anything a box cannot be (a room, stairs, a building), make the model in Blender and bring it in.

1. Export the model from Blender as `.glb`.
2. Copy the file into the Godot project.
3. Add an `MkMesh` under the map and drag the `.glb` onto it.

A `.glb` dragged straight under the map exports too, as an MkMesh with the default settings.

| Setting | Effect |
|---|---|
| `collision` | `faces`: every triangle is solid, exact for hollow shapes such as rooms. `hull`: one wrapped shape per part, fast. `none`: walk-through. |
| `game_material` | Draw every surface with this game material instead of the model's own look. Empty keeps the model's own textures. |

How the model's own materials are drawn: [Materials and textures](/guide/mapping/materials-textures.md).

## Simple shapes without Blender

Put a Godot `MeshInstance3D` under an MkMesh and give it one of Godot's own meshes: a box, a sphere, a cylinder. It exports like a model.

## Text and signs

Put a `MeshInstance3D` under an MkMesh and give it a `TextMesh`. Its letters become real geometry in the material's colour.

- Set that MkMesh's `collision` to `none`.
- With `depth` 0 the text is flat and shows from the front only. A depth above 0 gives solid letters.
- A `curve_step` of 2 to 4 keeps small text light.
- Godot's `Label3D` does not export.

## What the build makes of it

| Yours | In the game |
|---|---|
| Solid brushes | Collision shapes in the level's world |
| Rendered brushes | One model for all of them, drawn at the map's origin |
| Each MkMesh | A model of its own, with its textures inside the map's zone |
| Nothing under the map | A flat safety floor, just below your lowest brush |

Die Maschine's buildings and terrain are not there. What you place is the whole world.

## Limits

- `faces` collision makes each triangle a thin slab, 4 units deep behind its front face. A very thin double-sided wall should be a brush or use `hull`.
- `hull` fills hollow shapes: you cannot walk under an arch made solid that way.
- The game checks every collision shape on each trace: there is no search tree yet. Check warns past 4,000 faces. Give a detailed model `hull` or `none`, and block it with a few brushes.
- Triangles must wind clockwise seen from the front, which is Godot's own rule, so a normal import is right.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| A model draws but you walk through it | Its `collision` is `none`, or it came in without an MkMesh and is very thin. |
| A model does not draw at all | Read the build output: a surface it could not export is named there. |
| A dragged-in model ignores your material | Turn on **Editable Children** on it first, then set the material. |

<!-- sources: cw-mod mapkit/godot/README.md ("Making a map", "Build", "The objects"), mapkit/mkmap-format.md ("brushes", "meshes"), docs/mapkit-map-anatomy.md (section 1.2) @ 36b1f18 + working tree, 2026-10-07 -->

# Materials and textures

> How a surface gets its look: your own textures, or a game material by name. **Status:** Done (2026-09-28). Glow is parked.

## Two ways to dress a surface

| Way | How | Good for |
|---|---|---|
| **Your own look** | The material on your model, as Godot shows it | Anything you made yourself |
| **A game material** | Name it: on an `MkBrush`, on an `MkMesh`, or as the Blender material's name | Matching the game's own walls and floors |

## Your own look

A material draws in the game as it looks in Godot's viewport. The build exports the material the viewport draws, so a `StandardMaterial3D` set as a mesh's Surface Material Override wins over the one inside the `.glb`.

| In Godot | In the game |
|---|---|
| Albedo texture, tinted by the albedo colour | The surface's colour |
| Albedo colour alone | A flat colour |
| Normal map | Its bumps |
| Roughness (texture or value) | How shiny or dull |
| Metallic (texture or value) | A metal surface. It also counts as metal for bullet impacts. |
| Transparency: alpha scissor or alpha hash | A cut-out, such as a grate or a fence |
| Transparency: alpha blend | See-through, drawn as glass |
| Emission, with its energy | Exported. **No glow shows in the game yet.** |

Export writes each texture as a `.dds` file into `build\<map>_textures\`, next to the `.mkmap`.

## What does not export

| Thing | Do this instead |
|---|---|
| UV1 scale and offset | Tile the texture in Blender |
| Triplanar mapping | Unwrap the model |
| An ORM texture | Use separate roughness and metallic textures |
| A shader material | It draws with the default material. Use a `StandardMaterial3D`. |

## A game material

Name one of the materials Die Maschine's zone holds, such as `mc/mtl_p7_barrier_block_concrete_rusty`.

| Where | How |
|---|---|
| `MkBrush` | Set `game_material`. Empty is `mc/mtl_p7_cinder_block`. |
| `MkMesh`, whole model | Set `game_material`. Every surface that is not named after a game material uses it. |
| `MkMesh`, one surface | Name the Blender material after the game material. |

The names: [Materials](/guide/lists/materials.md). On a brush, the texture repeats over each face by itself.

## Limits

- A see-through surface is always glass. It cannot be metal as well.
- A surface that glows cannot be metal, cut out or see-through.
- A game material must be one that Die Maschine's zone stores, because your map links it by name.
- Game models show gray in the editor. Their materials are right in the game.
- Large textures are stored whole inside your map's zone. There is no streaming for custom textures yet, so keep them modest.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| A surface is plain gray in the game | It has a shader material, or its game material name is not one the zone stores. |
| Bumps look inside out | The normal map is not in the usual OpenGL form that Godot and glTF use. Re-export it that way. |
| A cut-out has a hard edge where you wanted a soft one | Cut-outs are on or off. For a soft edge use alpha blend, which draws as glass. |

<!-- sources: cw-mod mapkit/godot/README.md ("Making a map", "Build"), mapkit/mkmap-format.md ("meshes"), mapkit/zonekit/material_writer.hpp, docs/ROADMAP.md (P4; "Glowing surfaces") @ 36b1f18 + working tree, 2026-10-07 -->

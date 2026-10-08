# Sky, sun and fog

> Your map's own sky picture, its sun and its fog, set with Godot's own nodes. **Status:** Done (2026-09-29). The rest of the lighting is still Die Maschine's.

## The sky

1. Add a `WorldEnvironment` under the map.
2. Give its environment a **Sky** background.
3. Give the sky a `PanoramaSkyMaterial` with an equirectangular image: twice as wide as high. Use `.hdr` or `.exr` for an HDR sky, `.png` or `.jpg` otherwise.

The viewport now shows the sky the game will show.

| Setting | Effect |
|---|---|
| The panorama | The sky picture |
| Energy multiplier times background energy | Brightness. 1 draws a pixel as bright as the same pixel in Die Maschine's sky. |
| Another sky material (procedural, physical) | Baked to a panorama when you export from the editor |
| The sky's rotation | **Not exported yet** |

## The sun

Add a `DirectionalLight3D` under the map.

| Setting | Effect |
|---|---|
| The way it points | The direction of the sunlight |
| Colour | The sun's colour |
| Energy | Strength. 1 is as strong as Die Maschine's daytime sun. |

The game has one sun. Check warns about a second directional light.

## Fog

Use the `WorldEnvironment`'s fog.

| Setting | Effect |
|---|---|
| Light colour times light energy | The fog's colour |
| Density, or depth mode's begin and end | How thick it is with distance |
| Fog height and height density | Where it sits and how fast it thins upwards |
| Fog switched off | No fog in the game either |

## With none of these

Without a sun or a `WorldEnvironment`, the map keeps Die Maschine's daytime sky, sun and fog.

## What is still Die Maschine's

Your sky, sun and fog are written over a copy of Die Maschine's lighting. Everything else in that copy is unchanged:

| Thing | State |
|---|---|
| The light your walls get from their surroundings | Die Maschine's, baked for its own buildings |
| Reflections | Die Maschine's |
| Exposure and colour grading | Die Maschine's |
| Die Maschine's 948 lamps | Removed from your map (2026-10-05) |
| Die Maschine's baked sun shadow | Removed (2026-10-05). Nearby shadows from your own geometry still draw. |

So a room in your map is lit by your sun and sky, plus an ambient light that was measured in another building. It usually looks fine outdoors and can look odd indoors.

## Your own lights

`MkLight` (and the lights in the template) light the **editor preview only**. They do not reach the game yet. Lights of your own, a baked shadow of your own geometry, and your own reflection probes are the next steps of this work.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The sky is turned compared with the editor | You set a sky rotation in Godot, which is not exported. Turn the picture itself instead. The debug map marks the game's axes on its horizon. |
| The sky is far too bright or dark | Check both energy values: they multiply. |
| No fog | Fog is off in the environment, which means off in the game. |
| Indoor walls look lit from nowhere | That is Die Maschine's ambient light. There is no fix yet. |

<!-- sources: cw-mod mapkit/godot/README.md ("Making a map", "Build", "The debug map"), mapkit/mkmap-format.md ("sky", "lighting"), docs/ROADMAP.md ("The map's own lighting, step 1" and its last part) @ 36b1f18 + working tree, 2026-10-07 -->

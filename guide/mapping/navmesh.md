# Navmesh

> The surface zombies walk on. The build makes it for you from your map's collision. **Status:** Done for the basics (2026-09-29): zombies chase a player through a custom layout, up stairs and ramps. The rest is parked.

## What you do

Nothing. Every Build generates the navmesh from the same collision the game gets: your solid brushes, your meshes' collision, and the shapes around solid props and machines.

## The numbers it uses

They are Die Maschine's own settings.

| Thing | Value |
|---|---|
| Room a zombie needs to stand | 72 units high (1.83 m) |
| Highest step it walks up | 18 units (about 0.46 m) |
| Steepest slope it walks | 46° |

## What to keep in mind while you build

| Rule | Why |
|---|---|
| Keep floors connected | A zombie can only reach places the walkable surface connects. |
| Use ramps or stairs between levels | Both are walked. A ledge higher than a step is not climbed. |
| Do not rely on jumps or mantles | There are none yet: a gap a player can jump is a wall to a zombie. |
| Put something on every floor you want walked | Walkable floor is kept only where it connects to a player spawn, a zombie spawner or an object players use. Wall tops and the tops of props are dropped. |
| Leave room around machines | The navmesh goes around perk machines, box locations and barriers. |

A door's model is not part of the navmesh: the navmesh runs through the doorway. Zombies of the zone behind it only come once the door is bought and that zone is active.

## Looking at the result

The build writes the walkable polygons to `<game>\cw-mod\maps\<id>\generated\navmesh.obj`. Open it in Blender next to your map to see where zombies can go. Holes and islands show at once.

## Limits

| Thing | State |
|---|---|
| Mantles, jumps, drops | Parked |
| A door or a prop that moves and changes the walkable area | Parked |
| Very large maps (more than one navmesh cell) | Parked |
| Settings in the editor (how wide, how steep) | Parked |
| Points where zombies take cover or wait | Parked |
| Zombies walking cleanly around props | Not yet checked in the game |

To keep Die Maschine's navmesh instead of your own, for a test, build with `cwlink build ... --no-navmesh`. Zombies then walk where Die Maschine's floors were.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| Zombies rise and stand still | The spawner sits on a piece of floor that is not connected to you. Check `navmesh.obj`. |
| Zombies stop at a step | The step is higher than 18 units. Use a ramp or lower steps. |
| Zombies will not enter a room | Its floor is a separate island, or the ceiling is lower than 72 units. |
| Zombies walk through a wall | The wall is not `solid`. |

<!-- sources: cw-mod docs/mapkit-plan.md ("P5 step 1: the map's own navmesh"), docs/ROADMAP.md (P5; "Navmesh" in "Open and parked"; object clip), mapkit/cwlink/main.cpp (usage: --no-navmesh, generated\navmesh.obj), mapkit/godot/README.md ("Build") @ 36b1f18 + working tree, 2026-10-08 -->

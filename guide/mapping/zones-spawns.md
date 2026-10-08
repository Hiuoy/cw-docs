# Zones and spawns

> Where players start, where zombies come from, and how the map opens up. **Status:** Done (2026-09-27; barriers 2026-09-29).

## Zones: MkZone

A zone is a box-shaped area. Zombies spawn at the spawners of the zones that are active, and a zone becomes active when players can reach it.

| Setting | Effect |
|---|---|
| `zone_name` | Its name. Unique in the map. Spawners, barriers and doors refer to it. |
| `active_at_start` | Active from the first round. Every start zone is connected to every other start zone. |
| `size` | The box. Drag its face handles. |

Cover every place a player can stand with a zone. A player outside every zone is outside the play area.

A zone that is not active at start needs a door that opens it: see the door's `opens` in [Gameplay objects](/guide/mapping/gameplay-objects.md).

## Player spawns: MkPlayerSpawn

Place four, on the floor of a start zone.

| Setting | Effect |
|---|---|
| `player` | 1 to 4 for that player, 0 for any |

The build also makes a respawn point in every zone.

## Zombie spawners: MkZombieSpawner

| Setting | Effect |
|---|---|
| `zone` | The zone it belongs to. It is used only while that zone is active. |
| `kind` | `ground`: the zombie climbs out of the ground and hunts the players. `barrier`: it climbs out, walks to the nearest barrier of its zone, tears the boards down and climbs in. |

A `barrier` spawner with no barrier in its zone acts as `ground`.

## Barriers: MkBarrier

A boarded window. Zombies tear the boards off and climb through; players rebuild them.

1. Put it on the floor in the middle of the opening.
2. Point its arrow **into** the play area.
3. Keep the opening inside its box: the box is what stops players. Bullets pass through.
4. Put a `barrier` spawner outside, in the same zone.

| Setting | Effect |
|---|---|
| `zone` | The zone whose barrier spawners use it |
| `kind` | `wood`: Die Maschine's boarded window. `concrete`: its wall of concrete chunks, which **does not work yet**. |

## A layout that works

```text
 [barrier spawner]                      [barrier spawner]
        |                                      |
   == barrier ==                         == barrier ==
 +---------------------+   door   +---------------------+
 |  start zone         |==========|  second zone        |
 |  4 player spawns    |          |  ground spawners    |
 |  ground spawners    |          |                     |
 +---------------------+          +---------------------+
```

## Limits

- Zones are boxes. Cover an L-shaped room with one zone per arm, each with its own name, both active at start.
- You do not choose the zombie type per spawner. The round logic of the shared Zombies scripts decides.
- The concrete barrier asks for power and never opens. Parked.
- Whether the barrier's box really stops players was built on 2026-10-05 and is not yet tested in the game.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| No zombies in a room | No spawner names that zone, or the zone never becomes active. |
| Zombies appear but stand still | They cannot reach you: see [Navmesh](/guide/mapping/navmesh.md). |
| You take damage or are moved back for no reason | You are outside every zone. |
| Check: "zone does not exist" | A spawner, barrier or door names a zone that has no `MkZone`. |
| A barrier's zombies rise inside the room | The spawner's `kind` is `ground`, or it is in another zone than the barrier. |

<!-- sources: cw-mod mapkit/godot/README.md ("The objects", "Build"), mapkit/mkmap-format.md ("entities"), docs/mapkit-plan.md ("P1 step 2"), docs/ROADMAP.md ("Open and parked") @ 36b1f18 + working tree, 2026-10-07 -->

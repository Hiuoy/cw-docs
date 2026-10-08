# Your first map

> From an empty editor to walking your own map in the game. Do [Setup](/guide/mapping/setup.md) first.

## 1. Make a map from the template

In the mapkit dock, type a name and press **New map**. The name is `zm_` followed by lowercase letters, digits and `_`, such as `zm_garage`. It becomes the map's id, its folder and its zone.

You get a copy of the template: two rooms with a door between them, ready to build.

## 2. Look around

| In the scene | What it is |
|---|---|
| `MkMap`, the root | Everything under it is exported. Its `title` is the name players see. |
| Seven `MkBrush` | The floor, four walls and a divider with a doorway |
| Four `MkPlayerSpawn` | Where players start |
| Two `MkZone` volumes | The start room and the second room |
| Four `MkZombieSpawner` | Where zombies come out of the ground |
| `MkDoor` | The door a player buys to open the second room |
| `MkBarrier` | A boarded window |
| Two `MkPerkMachine` | Juggernog and Speed Cola |
| Three `MkMysteryBox` | The places the Mystery Box can be |
| `MkPackAPunch`, `MkPowerSwitch` | Pack-a-Punch and the power switch |
| Two `MkLight` | Lights for the editor's preview |

Each object shows a box of its size in the game and an arrow for the way it faces.

## 3. Change something

1. Select a wall, drag its box handles, and make the first room bigger.
2. Add a node (search "Mk"), pick `MkAmmoCache`, and put it on the floor against a wall.
3. Keep every object's origin on the floor.

## 4. Check it

Press **Check** in the dock. Red lines stop the export, yellow ones are advice. Click a line to select the node it is about.

## 5. Walk it

Press **F6** to walk the map in first person from the first player spawn.

| Key | Does |
|---|---|
| W A S D, mouse | Move and look |
| Shift | Sprint |
| Space | Jump |
| Esc | Free the mouse. Click to take it back. |

Speed, jump height and eye height match the game, so a gap you can jump here is a gap you can jump there.

## 6. Build

Close the game if it is running, then press **Build**. The output panel lists what was placed and what was left out. The map is now in `<game>\cw-mod\maps\<your map>\`.

## 7. Play

1. Start the game.
2. Zombies, **Private**, the **CUSTOM MAPS** tab.
3. Pick your map and start.

## What to expect in the game

- Your rooms, drawn and solid. Die Maschine's buildings are gone.
- A flat floor under the whole map, just below your lowest brush, so nobody falls forever.
- Zombies rising at the spawners of the zone you are in.
- The door: buy it at its box, its model sinks into the floor, and the next zone comes alive.
- The perk machines waiting for power. The template has a power switch: turn it on from its front. Delete the switch and everything is powered from the start.
- Pack-a-Punch working from the first round.
- Die Maschine's ambient light on your walls. See [Sky, sun and fog](/guide/mapping/sky-sun-fog.md).

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The game starts Die Maschine itself | The map was not picked in CUSTOM MAPS, or its build failed. Read the build output. |
| You fall through the floor | The brush is not `solid`. |
| A wall is invisible | The brush is not `rendered`. That is how an invisible wall is made. |
| No zombies | No spawner names the zone you are in, or the zone is not `active_at_start` and no door opens it. |
| You cannot get into the next room | The door's `opens` does not name that zone. |

More: [Help](/guide/troubleshooting.md).

<!-- sources: cw-mod mapkit/godot/README.md ("Making a map", "Build", "The objects"), mapkit/mkmap-format.md ("Rules a reader enforces") @ 36b1f18 + working tree, 2026-10-07 -->

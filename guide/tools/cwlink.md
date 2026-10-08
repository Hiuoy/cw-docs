# cwlink

> The command-line tool that builds a map from its `.mkmap` source. The editor's Build button runs it. **Status:** Done.

```text
cwlink [--game <dir>] [--out <dir>] build <map> <source.mkmap> --trace <zone.mktrace> [options]
```

`<map>` is the retail map the build takes its assets from. Today that is `zm_silver`, Die Maschine.

## The usual call

```powershell
cwlink build zm_silver mymap.mkmap --game "<game>" --trace "<game>\cw-mod\mapkit\trace\zm_silver.mktrace"
```

It writes `<game>\cw-mod\maps\<id>\`:

| File | What |
|---|---|
| `<id>.ff` | The map's zone. Read back and checked before it is kept. |
| `scripts\` | The compiled level scripts |
| `map.json` | Title, author, the asset library, the map's form. The CUSTOM MAPS tab lists maps that have it. |
| `generated\` | Readable copies: the zones script, and the navmesh as `.obj` |

The output of every command holds copies of your own game data. Never share it.

## Commands

| Command | Does |
|---|---|
| `build <map> <source.mkmap>` | Builds a map of its own from a source |
| `clone <map> <newmap>` | Copies every zone of a retail map under a new name. Tests only. |
| `replace <map>` | Repacks `<map>.ff` without its patch file. Tests only. |
| `patch <map>` | Writes override zones holding the map's entity list, with `--move` edits. Tests only. |
| `plane <map>` | Writes the plane test map: no world, a flat floor. Tests only. |

## Options for every command

| Option | Meaning |
|---|---|
| `--game <dir>` | The game folder. Default: `%MAPKIT_GAME_DIR%`, then the current folder. |
| `--out <dir>` | Write here instead of `<game>\cw-mod\maps\<name>\` |
| `--trace <file>` | The zone trace of `<map>`. Needed by `build`, `patch` and `plane`. |

## Options for build

| Option | Meaning |
|---|---|
| `--as <id>` | The map's id. Default: the name in the source. |
| `--at <x>,<y>,<z>` | Where the source's origin lands in the world. Default: the middle of `<map>`'s player spawns. |
| `--floor <z>` | The height of the safety floor. Default: just under the lowest brush. |
| `--level <dir>` | The folder of level scripts to compile. Default: `mapkit\level\<map>` of the repository. |
| `--no-level-scripts` | Ship no level scripts: `<map>`'s own run. For finding out which side a bug is on. |
| `--no-navmesh` | Keep `<map>`'s navmesh instead of generating the map's own |
| `--no-acoustics` | Leave `<map>`'s baked acoustics out of the copied sound bank |
| `--no-object-clip` | Do not make perk machines, box locations and barriers block players |
| `--keep-lights` | Leave `<map>`'s lamps lit where `<map>` has them |
| `--keep-baked-shadows` | Keep `<map>`'s baked sun shadow |
| `--keep-terrain` | Keep `<map>`'s terrain drawing |
| `--keep-decals` | Keep `<map>`'s projected decals |
| `--retail-gfx` | Write no drawn world of the map's own: `<map>`'s draws |
| `--draw-test` | Add test objects around player 1, for debugging what draws |

## Options that go back to older forms

They exist to compare a new build step with the one before it.

| Option | Meaning |
|---|---|
| `--overlay` | Write the old form: two override zones laid over `<map>`. Such a map works only on the PC that picked it. |
| `--with-library` | Load `<map>`'s whole zone set under the map, instead of the copies in the map's own zone |
| `--library-world` | With `--with-library`: leave the level's world assets to `<map>` |
| `--link-library` | With `--with-library`: link what those assets need by name instead of copying it |

## Options for the test commands

| Option | For | Meaning |
|---|---|---|
| `--move <key>=<value>@<x>,<y>,<z>[,<yaw>]` | `replace`, `patch` | Move every entity whose key has that value |
| `--tiles <n>` | `plane` | An odd number from 1 to 21: floor tiles per side |
| `--tile <hash>` | `plane` | The model to use as a floor tile |

## What build copies and changes

- Solid brushes and mesh collision become collision shapes; rendered brushes become one model.
- `<map>`'s spawns, perks, box locations and wall buys are moved to yours; the rest of its entities are left out.
- The level's world assets are written as the map's own: lighting with every lamp black and every baked shadow tree empty, the drawn world without buildings, terrain and decals, an empty list of placed effects.
- What those assets link is copied too, with the sound bank.
- Of `<map>`'s zones, only `techset_<map>` still loads under your map.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The usage text and nothing else | A misspelled option, or a missing value. |
| It cannot find the zone | `--game` is wrong, or `MAPKIT_GAME_DIR` is not set. |
| It cannot write the output | The game is running. Close it. |
| ACTS errors | `acts` is not on your PATH, or a level script does not compile. |
| "skipped" lines for perks or wall buys | See the limits on [Gameplay objects](/guide/mapping/gameplay-objects.md). |

<!-- sources: cw-mod mapkit/cwlink/main.cpp (Usage, ParseArgs), mapkit/README.md, client/game/mapkit_loader.hpp (map.json) @ 36b1f18 + working tree, 2026-10-08 -->

# ffinfo

> A command-line inspector for the game's zones: what a zone holds, how it is laid out, and what a map still takes from it. **Status:** Done.

```text
ffinfo [--game <dir>] <zone | file.ff> [options]
ffinfo [--game <dir>] --scan
ffinfo [--game <dir>] --walk-scan
```

A zone is given by its name (`zm_silver`) or by the path of a `.ff` file. `--game <dir>` is the game folder; the default is `%MAPKIT_GAME_DIR%`, then the current folder.

What ffinfo prints or writes about a retail zone is game data. Keep it on your PC.

## Looking at a zone

| Option | Shows |
|---|---|
| none | The header: version, flags, stream size, block sizes, and asset counts by type |
| `--assets` | Every asset's index and type |
| `--stream <file>` | Writes the zone's current data stream, patch applied |
| `--repack <file>` | Writes a stand-alone `.ff` with no patch file, and checks it reads back the same |
| `--scan` | Decodes every zone in `<game>\zone` and reports any that fail |
| `--walk` | Walks the stream asset by asset with mapkit's loaders and checks the result |
| `--walk-scan` | Walks every zone: which walk completely, and which missing loader stops the most zones |
| `--dump <asset or type>:<bytes>` | Prints the first bytes of an asset, or of every asset of a type |

## Entities

| Option | Shows |
|---|---|
| `--entities` | A level zone's entities, counted by class name |
| `--entities-json <file>` | Every entity with all its keys, as JSON |
| `--map <name>` | Whose entity lists to look for, when the zone belongs to a custom map |

## With a zone trace

A level zone cannot be walked from start to end, so these need `--trace <file>`: the trace the game recorded for that zone.

| Option | Shows |
|---|---|
| `--trace <file>` | Checks the trace against the zone, then decodes every asset mapkit has a loader for and checks it ends where the next one starts |
| `--world` | The level's streamer world: its model list and cell records |
| `--cell <n>` | The models of one cell |
| `--clipmap` | The collision map: cells and collision trees |
| `--gfx` | The drawn world: what it links to and its sub-arrays |
| `--level-assets` | The level's other world assets, the lighting's lights and its baked shadow trees |
| `--library-assets` | Every image, model, material and sound asset, read with mapkit's copy readers: how many decode exactly |
| `--check-copies <ff>` | Compares the copies in a map's zone with their originals in this zone |

## Models, materials and images

All with `--trace`.

| Option | Shows |
|---|---|
| `--mesh <asset>` | One mesh's geometry, fetched from the zone or from the streaming packages. A name or `#<hash>` names a model. |
| `--obj <file>` | With `--mesh`: also writes the geometry as OBJ |
| `--resident-meshes` | The meshes whose geometry is stored in the zone itself |
| `--material <name or #hash>` | One material, its image table and each image's header |
| `--dds <dir>` | With `--material` or `--images`: writes the images as `.dds` |
| `--images` | Every image stored in the zone, by format, size and whether it is streamed |
| `--resident-materials` | The materials whose images are all in the zone, by shader set |
| `--semantics` | Every image role the materials use, with its formats |
| `--semantic <hex>` | One image role: its formats and constants per shader set |
| `--material-table <file>` | One line per material: name, shader set, images, constants |
| `--model-materials <file>` | Every model's materials |

## What a map borrows

| Option | Shows |
|---|---|
| `--needs` | With `--trace`, on a level zone: what a map built on it still takes from it, by type and size |
| `--usage <file>` | With `--needs`: the game's record of one match (`"mapkit_usage"` in `cw-mod.json`) |
| `--usage-base <file>` | With `--usage`: a record from before the match, to leave out what the menus looked up |
| `--map-zone <file>` | With `--needs`: the map's own zone, whose links count as used |
| `--keep <zone>[:<trace>]` | With `--needs`: a zone that stays loaded anyway, such as `zm_common` |
| `--needs-list <file>` | Writes every asset to copy, one per line |
| `--needs-graph <file>` | Writes every asset of the zone with its type, name hash and links |

## Navigation data

| Option | Shows |
|---|---|
| `--hk <file>` | Reads a Havok tagfile, lists its types and items, and checks mapkit writes it back byte for byte |

## Examples

```powershell
ffinfo zm_silver                                  # what is in Die Maschine's zone
ffinfo zm_silver --entities                       # its entities, by class
ffinfo --scan                                     # can every zone of the install be read?
ffinfo "<game>\cw-mod\maps\zm_mymap\zm_mymap.ff" --walk    # is my built map well-formed?
```

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| "no loader" stops a walk | Normal for a retail level zone. Use `--trace`. |
| The trace does not match | It was recorded from another version of the zone. Record it again. |
| A zone fails to decode | The game's `oo2core_8_win64.dll` was not found: ffinfo loads it from your install. |

<!-- sources: cw-mod mapkit/ffinfo/main.cpp (Usage, Options), mapkit/README.md @ 36b1f18 + working tree, 2026-10-08 -->

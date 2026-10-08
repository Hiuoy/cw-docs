# mkasset

> Reads the game's models out of your own install, so the editor can show them. **Status:** Done.

You rarely run it yourself: the editor starts it in the background. Run it by hand to export one model, or to rebuild the list of model names.

```text
mkasset [--game <dir>] [--zone <name>]... catalog <out.json>
mkasset [--game <dir>] [--zone <name>]... export <model> <out.glb> [--lod <n>]
mkasset [--game <dir>] [--zone <name>]... serve
```

What mkasset writes is game geometry. Keep it in a local cache, never in a repository or anywhere shared.

## Commands

| Command | Does |
|---|---|
| `catalog <out.json>` | Lists every model of the zones it reads: zone, bounds, levels of detail, materials |
| `export <model> <out.glb>` | Writes one model as binary glTF, in Godot's space: Y up, meters |
| `serve` | Stays loaded and answers one request per line. This is what the editor uses. |

## Options

| Option | Meaning |
|---|---|
| `--game <dir>` | The game folder. Default: `%MAPKIT_GAME_DIR%`, then the current folder. |
| `--zone <name>` | A zone to read. Repeatable. Default: every zone that has a trace. |
| `--lod <n>` | With `export`: the level of detail. 0 is full detail, the default; higher numbers are coarser. |

`<model>` is a model's name or its hash, 16 hex digits.

## What it needs

A zone is read through its trace, `<game>\cw-mod\mapkit\trace\<zone>.mktrace`. A model that one zone only refers to is read from the zone that stores it, so that zone needs a trace too. For Zombies maps: `zm_silver` and `zm_common`.

Reading Die Maschine's index takes about a second, and each model a few milliseconds after that.

## The serve protocol

After `{"ready": true, ...}` on its output, mkasset reads one JSON request per line and answers with one JSON line. Every answer carries the request's `id` and `ok`; a failed one has `error`.

```json
{"id": 1, "cmd": "export", "model": "<model>", "out": "<file.glb>", "lod": 0}
{"id": 2, "cmd": "catalog", "out": "<file.json>", "brief": true}
{"id": 3, "cmd": "quit"}
```

## The model names

The zones store hashes of model names, not the names. The names the editor shows come from a list in the repository, `mapkit\godot\addons\mapkit\game_model_names.txt`: names and hashes only. To rebuild it from a catalog:

```powershell
python mapkit\mkasset\model_names.py catalog.json mapkit\godot\addons\mapkit\game_model_names.txt
```

The script asks ACTS for each hash and keeps a name only when it hashes back to the same value. About 93 in 100 models get a name.

## Good to know

- A model's levels of detail are not stored in order of detail. On Die Maschine the full model is usually the last one. mkasset ranks them by triangle count, so `--lod 0` is always the full model.
- The exported `.glb` has geometry and material names. Textures are not exported yet, which is why models show gray in the editor.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| No zones found | No trace in `cw-mod\mapkit\trace`. See [Setup](/guide/mapping/setup.md). |
| A model is not found | Its zone is not being read. Add `--zone`, or record that zone's trace. |
| The editor shows boxes | It could not start mkasset. Godot's Output panel says why. |

<!-- sources: cw-mod mapkit/mkasset/main.cpp (header, Usage), mapkit/README.md ("mkasset"), mapkit/godot/README.md ("Game models") @ 36b1f18 + working tree, 2026-10-08 -->

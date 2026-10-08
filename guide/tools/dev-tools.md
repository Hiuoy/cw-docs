# Developer tools

> The small Python scripts in the repository's `tools\` folder: reading a run back, naming hashes, reading menu bytecode. Most players never need them.

Run them from the cw-mod folder with `python tools\<script>`. Each prints its full usage with `--help` or at the top of its file.

## Reading a run back

| Script | Does | Use |
|---|---|---|
| `bootlog.py` | Prints the last run from `client.log` in short form: the boot profile, the login steps, Demonware redirects, errors and crashes. It ends with the backend's log for the same run. | `python tools\bootlog.py`. `--back 1` is the run before; `--all` shows every line; `--full` keeps whole crash dumps. |

## Making the game readable for a disassembler

| Script | Does | Use |
|---|---|---|
| `dump_fixup.py` | Turns the memory image written by the overlay's **Dump decrypted module** button into a file a disassembler can open | `python tools\dump_fixup.py <game>\bocw_dump.bin` |
| `ida_lui_recon.py` | An IDAPython script: gathers the Lua functions and the "UI Error" path in one pass. Changes nothing in the database. | Run inside IDA |

The dump is the game's code. It stays on your PC.

## Naming hashes

The game stores hashes of names, not names. These scripts guess names and keep the ones whose hash matches.

| Script | Does |
|---|---|
| `dvar_hash_match.py` | Matches a list of candidate names against the dvar hashes the game reports (`cw-mod\dvars.txt` from the overlay's Debug tab) |
| `dvar_hash_brute.py` | Builds candidate names from the words of names already found, and tests the combinations |
| `hash_harvest_strings.py` | Hashes every printable string in a file and matches it against unknown hashes |
| `lui_menu_names.py` | Names the menus in a Lua dump and writes `cw-mod\lui_menus.txt`, which the overlay's LUI Menus tab reads |
| `menu_hash_match.py` | Finds which field of a menu registry entry is the name hash |
| `wordlists\` | The candidate lists those scripts read. Its README says what each file is. |

About 37 in 100 dvar names are recovered this way.

## Reading the menus' Lua

| Script | Does | Use |
|---|---|---|
| `lua_disasm.py` | Disassembles the menu bytecode written by the overlay's **Dump loaded Lua files** button | `python tools\lua_disasm.py <chunk> list`, or `... line <n>` for the code of one source line |

A Lua error in the log names a chunk and a **source line**. The bytecode keeps the line table, so `line <n>` shows the instructions that failed.

## Model names

| Script | Does |
|---|---|
| `mapkit\mkasset\model_names.py` | Rebuilds the model picker's name list from an `mkasset catalog`. See [mkasset](/guide/tools/mkasset.md). |

## The docs' own tools

The scripts that build and check this site are in the docs repository. See [About these docs](/about.md).

**How it works inside:** [Tools](/re/method/tooling.md), [Hashes and names](/re/method/hashes.md), [The binary and its dump](/re/method/binary.md).

<!-- sources: cw-mod tools/bootlog.py, dump_fixup.py, dvar_hash_match.py, dvar_hash_brute.py, hash_harvest_strings.py, lui_menu_names.py, menu_hash_match.py, lua_disasm.py, ida_lui_recon.py (docstrings), tools/wordlists/README.md, .claude/skills/bocw-reverse-engineering/SKILL.md (section 8) @ 36b1f18 + working tree, 2026-10-08 -->

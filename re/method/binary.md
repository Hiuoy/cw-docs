# The binary and its dump

> The game's executable is encrypted on disk, so everything is read from a copy of the running game's memory. **Status:** Done.

## In short

- `BlackOpsColdWar.exe` on disk is encrypted by [Arxan](/glossary.md#arxan): only its headers are readable. Static analysis of that file is impossible.
- The mod writes the **decrypted image** out of the running process, and a small script makes that file loadable.
- In the fixed dump, **file offset equals RVA** for every section, so bytes can be read straight from the file.
- The dump's image base is the base of the run it was taken from. Refer to things by name and RVA.

## Taking the dump

1. Start the game with the mod and stay in the main menu.
2. Overlay, **Scripts** tab, Diagnostics, **Dump decrypted module**. The mod walks the module page by page with `VirtualQuery`, copies every committed, readable page, and writes `bocw_dump.bin` into the game folder. It changes no page protection.
3. Run `python tools\dump_fixup.py bocw_dump.bin`. It writes `bocw_dump_fixed.exe`.

## What the fix-up does

The snapshot is a flat memory image: each section sits at its RVA, not at a file offset. The script only rewrites the section table.

| Field | New value |
|---|---|
| `FileAlignment` | `SectionAlignment` |
| Each section's `PointerToRawData` | Its `VirtualAddress` |
| Each section's `SizeOfRawData` | Its virtual size, rounded up to the alignment |

No byte moves. The header's `ImageBase` is left as it was in memory: the address the game was loaded at in that run.

## The image

Our dump is 520,821,760 bytes, equal to `SizeOfImage` (0x1F0B1C00). Its image base is `0x7FF71CBC0000`. The build string `1.34.0.15931218` is plain text in the image.

| Section | RVA | Size | Holds |
|---|---|---|---|
| `.text` | 0x1000 | 0xD75B800 | The game's code |
| `.rdata` | 0xD75D000 | 0x596C00 | Constants, tables, strings |
| `.data` | 0xDCF4000 | 0xCDB2BB4 | Globals, mostly zero at start |
| `.pdata` | 0x1AAA7000 | 0x166A00 | Unwind records |
| `_RDATA` | 0x1AC0E000 | 0xA00 | |
| `.rsrc` | 0x1AC0F000 | 0x2D3C00 | Resources |
| `.reloc` | 0x1AEE3000 | 0x4AA00 | Relocations |
| `.idata` | 0x1AF2E000 | 0x6000 | Imports |
| second `.text` | 0x1AF34000 | 0x417DC00 | **Arxan's own code** |

The table was read from the dump's own headers.

## Reading bytes

Read from the file, not through the disassembler: it is instant and never blocks.

```python
import mmap
BASE = 0x7FF71CBC0000
fh = open("bocw_dump_fixed.exe", "rb")              # keep fh alive or the map closes
mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)

def read(va, n):
    o = va - BASE                                    # file offset == RVA
    return bytes(mm[o:o + n])
```

## What the dump does not hold

| Thing | Where it is instead |
|---|---|
| Menu rules, lock rules, lobby flow | In the menus' Lua, which is an asset in the zones |
| Round logic, perks, quests | In GSC scripts, also assets |
| Names of dvars, menus, script functions | Nowhere. The game stores hashes. See [Hashes and names](/re/method/hashes.md). |
| World geometry | In the zones and the streaming packages |

## How the client finds things at run time

The mod never subtracts by hand.

| Way | Where | Use |
|---|---|---|
| An [anchor](/glossary.md#anchor): the address in our dump, as a constant | `client/game/dump_anchors.hpp` | `live = moduleBase + (dumpAddress - 0x7FF71CBC0000)`, with a bounds check |
| An [AOB signature](/glossary.md#aob-signature) | `client/game/signature_store.hpp` | Survives small code movement |

Every anchor is listed in the [function index](/re/reference/functions.md) and the [globals index](/re/reference/globals.md).

## Limits

- A dump holds what was mapped at that moment. Take it from the main menu.
- Pages that were not committed read as zeros.
- A dump is taken with the mod running, so it holds the mod's own detours. In ours, `BB_Alert` starts with `E9` and a jump out of the image, where its signature expects `40 55 53 56 48`. A function that starts with `E9` is a jump stub of the game's, or a hook of yours.
- The dump is the game's code: it stays on your PC. See [Legal](/legal.md).

## See also

- [Arxan](/re/client/arxan.md): what else the protection does
- [Address and byte math](/re/method/address-math.md)

<!-- checked against the dump file 2026-10-08: size, image base, section table; the build string's first occurrence is in .data, not .rdata as the skill says -->
<!-- sources: cw-mod .claude/skills/bocw-reverse-engineering/SKILL.md (section 2), tools/dump_fixup.py (the code; its docstring's "preferred base" line is older than the skill and is not used here), client/scripting/scripting.cpp (DumpDecryptedModule), client/game/dump_anchors.hpp @ 36b1f18 + working tree, 2026-10-08 -->

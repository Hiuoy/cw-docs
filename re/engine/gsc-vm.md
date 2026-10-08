# The GSC VM and the script loader

> Game logic runs in compiled GSC scripts, which are assets in the zones. This page explains how cw-mod makes the engine load scripts that never came from a zone. **Status:** Done, in game 2026-09-23. Level scripts for custom maps since 2026-09-26.

## In short

- A compiled script is an asset of type 68, `scriptparsetree`: a name hash, a buffer, a length.
- One detour on the asset lookup serves cw-mod's scripts. The engine's own linker does the rest.
- **Replace**: your script carries a stock script's name. **Inject**: it is added to the include table of a script every Zombies match loads.
- Three things do not hold for such a script: its [string ids](/re/engine/gsc-strings.md) are not written, lazy function references do nothing in retail, and nothing makes sure it exists on both the server and the client. The loader covers each.

## The script object

The header follows ACTS's layout for this game. All offsets are from the start of the object.

| Offset | Type | Field |
|---|---|---|
| 0x00 | 8 bytes | Magic `80 47 53 43 0D 0A 00 38` |
| 0x10 | u64 | Name: hash of the path **with** `.gsc` or `.csc` |
| 0x18 | u16 | String count |
| 0x1A | u16 | Export count |
| 0x1C | u16 | Import count |
| 0x24 | u16 | Include count |
| 0x30 | u32 | String table offset |
| 0x34 | u32 | Include table offset: one u64 name per include |
| 0x38 | u32 | Export table offset |
| 0x3C | u32 | Import table offset |
| 0x48 | u32 | File size |
| 0x50 | u32 | Code size |

Linked objects are listed in `gObjFileInfo`: 800 entries of 24 bytes for each VM, server and client.

## Serving and injecting

```text
DB_FindXAssetHeader(type, nameHash, ...):
    not a scriptparsetree              -> the original
    the name is one of our scripts     -> our buffer            (REPLACE)
    the name is the host script        -> a copy of the stock host with our names
                                          appended to its include table      (INJECT)
    otherwise                          -> the original
```

- The host is `scripts/zm_common/zm_utility.gsc`. Every Zombies match loads it through an include.
- The copy is the stock bytes plus a new include table at the end. Only the table's offset, the count and the file size change.
- Inject or replace is decided per match, when the host is first asked for. By then the map's zones are loaded, so "does a stock script have this name" has a true answer.
- If the host was already linked from its stock buffer by another path, the loader does not inject. Linking it twice would be worse.
- Client scripts (`.cscc`) and a custom map's own level scripts are replace-only.

## Lazy function references

`&namespace::function` across scripts compiles to opcode `0x13` with the operand `{u32 namespace, u32 name, u64 script}`. Retail's handler copies the operand into a local and does nothing.

The loader's handler, a port of ACTS's, looks the export up in the named script, falls back to any linked object that exports it, and pushes a script-function value. It is written into `gVmOpJumpTable[0x13]` when one of our scripts is first served, and taken out when the loader is turned off.

## Clientfields

A clientfield is registered once on the server VM and once on the client VM, and the two lists must match. A script that registers one and exists on one side only ends the match with "Clientfield Mismatch". The engine prints which field only to a console that does not exist.

Each VM's table is 13 pools of 4,120 bytes. A pool holds a count at `+8` and up to 512 pointers from `+16`, each to a 64-byte entry. The loader hooks `ClientField_Shutdown`, reads both tables just before they are erased, and writes the difference to the log.

## Natives and prints

- GSC built-ins are rows of 32 bytes in read-only data: `{u32 nameHash, u32 minArgs, u64 maxArgs, function, flags}`. The hash is [canon32](/re/method/hashes.md). There are 2,689, about half of them named by hashing identifiers from decompiled scripts.
- The game draws a script's plain-text `iprintln` as an empty box. cw-mod detours `Scr_ConstructMessageString` read-only and mirrors the text to the log, as `(Script)` lines, and to the top of the screen.
- That function's output is one segment per argument, each led by a code byte: `0x12` string, `0x10` a localized key that exists, `0x11` a hash with no entry, `0x13` int, `0x15` float.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `DB_FindXAssetHeader` | 0xB3021F0 | 0x7FF727EC21F0 | `header (u8 type, u64 name, bool includeOverride, int waitTime)` | The one detour. No caller guard. |
| (stock handler of GSC opcode 0x13) | 0x1BF6EB0 | 0x7FF71E7B6EB0 | | The empty lazy-link handler |
| `gVmOpJumpTable` | 0xDE87740 | 0x7FF72AA47740 | pointer per opcode | The VM's handler table |
| `gObjFileInfo` | 0xF6EC9D0 | 0x7FF72C2AC9D0 | `[2][800]`, 24 bytes each | Linked script objects |
| `ClientField_Register` | 0xAECD190 | 0x7FF727A8D190 | | Fills one 64-byte entry |
| `ClientField_Shutdown` | 0xAECD6C0 | 0x7FF727A8D6C0 | `()` | Erases the current VM's table |
| `g_serverVmCtx` | 0x11AFBA40 | 0x7FF72E6BBA40 | | The server VM's context. Its first pointer is the clientfield table. |
| `Scr_ConstructMessageString` | 0xB8400B0 | 0x7FF7284000B0 | `void (int inst, u32* out, u32 firstParam, int count)` | Builds the text of `iprintln` and `iprintlnbold` |

## Limits

- One injection host, and it is a Zombies script.
- A replace script must keep the exports the stock scripts import from it.
- Scripts are compiled with ACTS for this game. Another compiler's string table is not understood.

## See also

- [Script strings](/re/engine/gsc-strings.md): the string ids
- [GSC scripts, the guide](/guide/scripting/gsc.md)
- [Level scripts](/guide/scripting/level-scripts.md)

<!-- addresses of the signature-bound names read from the dump file 2026-10-08; slot 0x13 of the handler table holds RVA 0x1BF6EB0 -->
<!-- sources: cw-mod client/scripting/scripting.hpp, scripting.cpp, cw_gsc.hpp (layouts from ACTS, MIT), client/game/dump_anchors.hpp (Scr_ConstructMessageString), .claude/skills/bocw-reverse-engineering/SKILL.md (sections 3.4, 5, 9) @ 36b1f18 + working tree, 2026-10-08 -->

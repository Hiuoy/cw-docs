# Script strings

> A script that did not come from a zone has no string ids. This page covers the engine's string pool, how the loader gives a script its ids, and the three ways those ids went wrong. **Status:** Done, in game 2026-09-26.

## In short

- A string in the script VM is a 32-bit id into one pool. Two strings are equal when their ids are equal.
- The engine writes a script's string ids when its **zone loads**, not when it links. Nothing on the link path does it.
- The loader interns each literal itself and writes the id into the bytecode.
- The intern function is [caller-guarded](/re/client/arxan.md) in an unusual way: called from outside the image it works, and files the string where no lookup will find it.

## The operand

`VM_OP_GetString` reads a 32-bit id from a 4-aligned operand. ACTS, the compiler, leaves the placeholder `0x12345678` there.

The script's string table says where the operands are. An entry is 8 bytes, `{u32 textOffset, u8 refCount, u8 type}`, followed by `refCount` offsets into the bytecode. The text itself has a 3-byte header (`0x8B`, length + 1, 0) in the style of a zone's encrypted strings, then plain characters.

## The pool

The pool is addressed in 16-byte slots: an entry is at `poolBase + 16 * id`. Buckets are indexed by the low 16 bits of the hash, and hold the first id of a chain.

| Offset | Type | Field |
|---|---|---|
| +0 | u16 | Reference count |
| +2 | u8 | Flags: bits 0 to 5 users, `0x40` skipped by every lookup, `0x80` stored encrypted |
| +4 | u32 | Length |
| +8 | u32 | Next id in the bucket |
| +16 | u64 | Hash of the text: FNV-1a, 64 bits, case kept, no mask |
| +24 | | The text |

## What the loader does

Before a script is first served:

1. For each literal, call `SL_GetString(text, user 0, type 0, decrypt false)` through a thunk.
2. Read the new entry back and check that its stored hash is the text's own.
3. Write the id into every operand the table lists.
4. Check that every operand held the placeholder before. If not, the table does not point where the loader thinks, and the log says so.

User 0 gives a plain counted entry that no shutdown frees.

## Three ways it went wrong

| Symptom | Cause | Answer |
|---|---|---|
| The script ran and every string was garbage | Nothing had written the ids | The steps above |
| Strings looked right in prints, but `classname == "script_model"` was false | Called from the DLL, `SL_GetString` stored the **complement** of the hash. The entry holds the right text in the wrong bucket, so it is a private copy that never equals the engine's. | Call through an Arxan thunk. Step 2 catches it if the thunk is ever not enough. |
| A level script was dropped with "November 406 Cut Rain" | The engine re-interns its constant strings at **every map start**. The script's `"int"` id, taken earlier, was no longer the one the clientfield type check compares against. | On every script lookup, re-check the ids of scripts already served and intern the stale ones again |

The same re-check also covers a later finding: the engine was seen to overwrite served operands with id `0x2`, the empty string.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `SL_GetString_Guarded` | 0x1BC3780 | 0x7FF71E783780 | `u32 (const char* text, u8 user, int type, bool decrypt)` | Interns a string |
| `VM_OP_GetString` | 0x1BB01E0 | 0x7FF71E7701E0 | | Reads the id operand |
| `ClientField_TypeFromString` | 0xAECBE60 | 0x7FF727A8BE60 | | Opens with a compare against the engine's own `"int"` id |

The loader finds the pool base and the bucket table the way `SL_GetString` itself does: from the two instructions inside it that load them, at `+0x23F` and `+0x1B0` from its start.

## Diagnostics

On every script drop, and on a script's first serve, the loader logs for each literal whether its id is still what a lookup of the text returns, next to the engine's own `"int"`. Look for `String check` lines in `cw-mod\client.log`.

## Limits

- When `SL_GetString` cannot be reached through a thunk, a script that has string literals is refused. Serving it would hand the VM garbage ids.
- The pool's layout and the two instruction offsets are for this build.

## See also

- [The GSC VM and the script loader](/re/engine/gsc-vm.md)
- [Arxan](/re/client/arxan.md): the guard and the thunk
- [GSC scripts, the guide](/guide/scripting/gsc.md)

<!-- sources: cw-mod client/scripting/scripting.cpp (EnsureStrings, the SL_* helpers, the string diagnostics), cw_gsc.hpp, .claude/skills/bocw-reverse-engineering/SKILL.md (sections 6, 9) @ 36b1f18 + working tree, 2026-10-08 -->

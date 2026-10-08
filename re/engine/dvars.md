# Dvars

> The game's settings system. No names, no console, values that cannot be read directly, and a write that can vanish without a trace. **Status:** Done.

## In short

- A dvar is found by the [hash](/re/method/hashes.md) of its name in a table of 1,024 buckets. The image holds no dvar names.
- Each dvar holds one value **per game mode**, and a bool is stored mixed with a per-process key. Read through the engine's getters.
- Flag `0x400` marks a server-owned dvar: a write from the main thread is **dropped silently** unless a latch byte is set.
- The console is compiled out. A recovered name still works with the engine's setters, so the overlay's Debug tab is the console.

## Finding a dvar

`Dvar_FindVar(hash)` takes a spinlock, picks the bucket `hash & 0x3FF`, and walks the chain comparing hashes masked to 63 bits.

## The node

| Offset | Type | Meaning |
|---|---|---|
| +0 | u64 | Name hash |
| +8 | pointer | Next node in the bucket |
| +16 | pointer | Value block: 96 bytes per game mode |
| +24 | int | Type |
| +28 | int | Flags |
| +32 | 16 bytes | Domain: the limits of the value |

| Type | Meaning | | Flag | Meaning |
|---|---|---|---|---|
| 1 | bool | | 0x10 | Read-only |
| 2 | float | | 0x40 | Write-protected |
| 6 | int | | 0x80 | Cheat |
| 7 | enum | | 0x400 | Server-authoritative |
| 8 | string | | 0x800 | One value per game mode |
| 10 | int64 | | 0x4000 | Undefined |
| 11 | uint64 | | | |

## The value block

- Without flag `0x800`, the value is in slot 0. With it, the slot is the session's game mode (0 zm, 1 mp, 2 cp, 3 wz), and game mode 4 falls back to slot 0. `Dvar_GetBool` opens exactly this way.
- A built value is 32 bytes. The first bytes hold a plain copy. The word at +24 holds the copy the getters decode, mixed with a key taken from the process. The engine trusts the second.

So a direct read of the block gives a number that may or may not be what the engine sees. The client reads byte 0 only for diagnostics, and says so in its output.

## The latch

`Dvar_ApplyValueInternal`, where every setter ends, opens with this test (in our words):

```c
if (dvar == null || (dvar->hash & 0x7FFFFFFFFFFFFFFF) == 0)
    return;
if ((dvar->flags & 0x400) && Sys_IsMainThread() && !g_dvarAllowServerFlaggedWrites)
    return;                 // no log, no return code
```

- The engine's own path shows the intended use: `Dvar_ApplyServerDvarPacket` sets the latch to 1, applies the packet, and sets it back to 0.
- `Dvar_CanSetValue` looks like the gate but is not: it screens only `0x10`, `0x40` and `0x80`, and source 0 skips it.
- The D3D12 present thread **is** the main thread for this test, so a write from the overlay was dropped too.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `Dvar_FindVar` | 0xC0B2090 | 0x7FF728C72090 | `uintptr* (u64 nameHash)` | The lookup. Null when nothing is registered under the hash. |
| (Dvar_FindVar's thunk) | 0xC0B2230 | 0x7FF728C72230 | | An `E9` jump to the lookup. Bind the implementation. |
| `Dvar_GetBool` | 0x1A68F50 | 0x7FF71E628F50 | `bool (void* dvar)` | Decodes the mixed copy |
| (Dvar_GetInt's thunk) | 0xE82540 | 0x7FF71DA42540 | | A split thunk that dispatches on the return address. Calling it from the mod faults. |
| `Dvar_SetBoolFromSource` | 0xC0B5580 | 0x7FF728C75580 | `void (uintptr* dvar, bool value, int source)` | Builds both copies, then applies |
| `Dvar_SetIntFromSource` | 0xC0B7530 | 0x7FF728C77530 | `void (uintptr* dvar, int value, int source)` | Switches on the dvar's type |
| `Dvar_StringToValue` | 0xC0BA580 | 0x7FF728C7A580 | `void* (void* value, int type, const void* domain, const char* text)` | Builds a 32-byte value from text |
| `Dvar_ApplyValueInternal` | 0xC0B8DB0 | 0x7FF728C78DB0 | `void (uintptr* dvar, const void* value, uint source)` | Holds the latch test. Copies a string into engine memory. |
| `Dvar_CanSetValue` | 0xC0ACBB0 | 0x7FF728C6CBB0 | | Screens flags 0x10, 0x40, 0x80 |
| `Dvar_ApplyServerDvarPacket` | 0xC0B3A80 | 0x7FF728C73A80 | | The network path that holds the latch |
| `Dvar_SetAllowServerFlaggedWrites` | 0xC0B5A80 | 0x7FF728C75A80 | `void (bool)` | One instruction: store `cl` into the latch |
| `g_dvarAllowServerFlaggedWrites` | 0x18A4D544 | 0x7FF73560D544 | u8 | The latch |
| `g_dvarHashTable` | 0x18A55570 | 0x7FF735615570 | pointer[1024] | The buckets |
| `Com_FormatHash64` | 0xC48A3F0 | 0x7FF72904A3F0 | | Prints a hash as 16 hex digits. All the engine can do with one. |

## What cw-mod does

| What | Where | How |
|---|---|---|
| Every write | `Pointers::WriteDvarBool`, `WriteDvarInt`, `WriteDvarString` in `client/game/dvars.cpp` | Saves the latch, sets it to 1, calls the engine's setter with source 0, restores the latch. Restoring, not clearing: the engine may be in the middle of a packet. |
| Lookup by name | Overlay, Debug tab | Hashes the name and calls `Dvar_FindVar`. Shows type and flags, decoded. |
| Dump | Debug tab, writes `cw-mod\dvars.txt` | Walks all 1,024 buckets with guarded reads and no lock. The hash list to match a word list against. |
| Recover names | Debug tab, writes `cw-mod\names_recovered.txt` | Hashes every name-shaped string in the process and joins with the registry |

## How we found it

- **The hash.** `H("r_fog")`, `H("cg_fov")`, `H("r_mode")` and `H("com_maxclients")` each appear as the 64-bit immediate loaded right before that dvar's registration call.
- **The latch.** A bool set through `Dvar_SetBoolFromSource` read 0 before and after, for two full test runs. The setter was correct. Reading on into the function it ends in found the three-part test.
- **The getter thunk.** Reading `com_maxclients` back through `Dvar_GetInt` crashed the boot. The client now remembers what it set and reads the server's plain player-cap global instead.

## Limits and open points

- About 37 in 100 dvars have a name. See [Hashes and names](/re/method/hashes.md).
- **Open, found 2026-10-08.** The signature the client uses for `Dvar_SetIntFromSource` matches three setters with the same opening bytes: one tests its value as 32 bits, two as 64 bits. The scanner binds the first, a 64-bit one with no name in the IDB. The 32-bit one that the client's comment describes is the second, `Dvar_SetInt_cand` at RVA 0xC0B7B90.
- A dvar pointer slot found by signature holds the pointer only after the dvar is registered.

## See also

- [The boot profile](/re/client/boot-profile.md): `nodw`
- [Settings](/guide/settings.md): what a player sets instead of dvars
- [Developer tools](/guide/tools/dev-tools.md): the hash tools

<!-- checked against the dump file 2026-10-08: the head of Dvar_GetBool (type at +0x18, flags at +0x1C, values at +0x10, flag bit 11, game mode 4 -> 0); the three matches of the Dvar_SetIntFromSource signature at RVA 0xC0B7530, 0xC0B7B90, 0xC0B8620 -->
<!-- sources: cw-mod client/game/dvars.cpp, game.hpp (kDvar_*), game.cpp (signatures), dump_anchors.hpp (g_dvarAllowServerFlaggedWrites, Dvar_StringToValue), .claude/skills/bocw-reverse-engineering/SKILL.md (sections 7, 9) @ 36b1f18 + working tree, 2026-10-08 -->

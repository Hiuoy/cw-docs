# Address and byte math

> The four forms of an address, how to decode an operand by hand, and how to read a structure's shape out of code. Every example is from our dump.

## In short

- **RVA = address − image base.** It is the same in every dump of the build. Pages give both.
- In the fixed dump, **file offset = RVA**.
- A call or jump target is `address + length + rel32`. A RIP-relative operand is `address of the next instruction + disp32`.
- An offset needs **two witnesses**: a writer and a reader.
- A function's return value can lie. Read the thing it writes.

## Four forms of one address

Example: `Com_SessionMode_SetNetworkMode`.

| Form | Value | Rule |
|---|---|---|
| Address in our IDB | 0x7FF728D7C630 | What the disassembler shows |
| RVA | 0xC1BC630 | Address − `0x7FF71CBC0000` |
| Offset in the dump file | 0xC1BC630 | Equal to the RVA |
| Address in a running game | module base + 0xC1BC630 | The base changes every run |

Hand arithmetic drifts. One working note gave a global's RVA with a digit dropped. Recompute from the full address, and confirm by decoding the instruction that uses it.

## Decoding operands

```text
call, rel32 (5 bytes):   target = addr + 5 + int32
  7FF71D0B3D27: e8 44 7f 03 0d      -> 7FF71D0B3D2C + 0D037F44 = 7FF72A0EBC70

negative rel32:
  7FF723D4858B: e8 b0 9f cf f9      -> rel = F9CF9FB0 - 2^32 = -6306050 -> 7FF71DA42540

an Arxan split thunk (E9 = jmp):
  7FF728C72230: e9 5b fe ff ff      -> 7FF728C72235 - 1A5 = 7FF728C72090

RIP-relative: target = address of the NEXT instruction + disp32
  7FF723D48584: 48 8b 0d 95 8a f7 08   (7 bytes) -> 7FF72CCC1020
  7FF728C75A80: 88 0d be 7a 99 0c      (6 bytes) -> 7FF73560D544
```

The instruction length includes any immediate after the displacement (`cmp dword [rip+d], imm8` adds 1). Let a disassembler library give the length.

What those targets are:

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `Dvar_FindVar` | 0xC0B2090 | 0x7FF728C72090 | The implementation. Hook this. |
| (Dvar_FindVar's thunk) | 0xC0B2230 | 0x7FF728C72230 | An `E9` jump to it |
| (Dvar_GetInt's thunk) | 0xE82540 | 0x7FF71DA42540 | Dispatches on the return address |
| `p_dvar_com_maxclients` | 0x10101020 | 0x7FF72CCC1020 | Holds the dvar's pointer |
| `g_dvarAllowServerFlaggedWrites` | 0x18A4D544 | 0x7FF73560D544 | See [Dvars](/re/engine/dvars.md) |

## Signatures

A signature keeps opcode and ModRM bytes and wildcards every displacement, relative offset and immediate that relocates. It must match exactly once. The client's helpers (`client/memory/scanned_result.hpp`):

| Match starts at | To reach the target |
|---|---|
| A call | `.Add(1).Rip()` |
| `48 8B 0D` (a load) | `.Add(3).Rip()` |
| A call right after a 7-byte load | `.Add(8).Rip()` |

`.Rip()` is `field + 4 + int32(field)`.

## Reading structure from bytes

**Bit fields.** `Com_SessionMode_SetNetworkMode` is seven instructions:

```nasm
mov eax, [g]
shl ecx, 4
xor ecx, eax
and ecx, 0F0h
xor eax, ecx
mov [g], eax
ret
```

That is `g ^= ((v << 4) ^ g) & 0xF0`: the field is bits 4 to 7 of the packed word.

**Strides** come from `imul reg, reg, imm` or from the allocation.

| Array | Stride | Seen as |
|---|---|---|
| `g_svClients` | 70,864 | `alloc(70864 * cap)` |
| The playerdata store | 86,040 per controller, 336 per entry | |
| Join candidates | 248 | |
| Storage backends | 8,272 = 48 + 4 × 2,056 | A layout that tiles exactly is a good self-check |

**Two witnesses for an offset.** The disassembler once drew a sorted table's count as if it sat inside entry 0. The insert's `memmove` from `base+8+40i` to `base+48+40i` proved the entries start at +8 with a stride of 40.

**Every count that indexes an array.** The loop bound gives one. Look for others that only run-time code reads: the clip map has a third dynamic-entity count at +460, and the renderer walks decal index ranges and never reads the count field.

## Return values lie

| Function | Returns | And yet |
|---|---|---|
| `PlayerDataStorage_FlushWrites` | 0 | Both on success and on an empty queue |
| `PlayerData_SubmitLocationLoad` | 1 | When nothing matched |
| `Ddl_CopyInstanceToInstance` | 1 | A no-op on an invalid source |
| `Session_SendInfoRequestMsg` | 1 | Always |
| A Lua native | Its push count | 1 for a pushed nil too |

Read the engine's own witness: the queue count, the pushed Lua slot, the field it writes.

## Bytes you will write

| Bytes | Meaning |
|---|---|
| `B0 01 C3` | `mov al,1; ret`. The engine's own `DwAuth_StubReturnTrue` is exactly this. |
| `31 C0 C3` | `xor eax,eax; ret` |
| `E9 rel32` | `jmp`; rel32 = target − (source + 5) |
| `48 B8 imm64 FF E0` | `mov rax, imm64; jmp rax` (12 bytes) |
| `FF 25 00000000 imm64` | `jmp [rip]` (14 bytes) |

## Counts worth knowing

Measured on this build.

| What | Count |
|---|---|
| `.pdata` records | 122,402: 79,200 primary and 43,202 chained fragments |
| Functions the disassembler lists | About 297,000 |
| Asset types (`g_xassetTypeNames`) | 221, of which `Load_XAssetHeader` dispatches 211 |
| Lua C API functions | 65 |
| Lua native registrations | 2,556 |
| GSC natives | 2,689, of which 1,340 are named |
| Dvar hash buckets, registered dvars | 1,024 and 3,655 (37 in 100 named) |
| Asset entries | 737,280, 16 bytes each, a fixed array |
| Zone folder | 948 `.ff`, 948 `.fd`, 67 `.xpak`, 519 `.xsub` (131 GB) |

The disassembler lists more functions than `.pdata` has records for two reasons: leaf functions have no unwind record, and Arxan splits functions into chunks. **A `.pdata` size is a chunk, not a function.**

A size times bytes per call site is a sanity check on a count. `LUI_RegisterEngineNatives_cand` is 70,983 bytes and makes 2,556 calls to its registrar, in two encodings. A scan for one encoding found only 1,683.

## See also

- [The binary and its dump](/re/method/binary.md)
- [Function index](/re/reference/functions.md)

<!-- sources: cw-mod .claude/skills/bocw-reverse-engineering/SKILL.md (section 3), client/memory/scanned_result.hpp, client/game/dump_anchors.hpp @ 36b1f18 + working tree, 2026-10-08 -->

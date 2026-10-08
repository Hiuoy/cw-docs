# Tools

> What each tool is good for, where to look first, and where outside the executable the answers often are.

## In short

- **Python over the dump file** for bytes, strings and immediates. It is instant.
- **A disassembler** (we use IDA) for cross-references, decompiling and keeping names.
- **The game itself** as the instrument: read-only detours that log.
- **The zones and the scripts** hold most rules. The executable holds the machinery.

## Who does what

| Task | Tool |
|---|---|
| Read bytes at an address | Python and `mmap` over the fixed dump. See [The binary and its dump](/re/method/binary.md). |
| Find a 64-bit hash or a 32-bit error code in code | A byte scan of the dump. With `numpy` over the 8 alignments, thousands of hashes take under a minute. |
| Who calls this? What does it call? | The disassembler's cross-references |
| What does this function do? | The decompiler, then the bytes for anything that looks wrong |
| Which of these paths really runs? | A detour that logs each caller once |
| What is in a zone? | [ffinfo](/guide/tools/ffinfo.md) |
| What does a menu do? | The Lua dump and `tools/lua_disasm.py` |
| What does a script do? | The community's decompiled GSC, and ACTS |

## What to search for, in order of yield

1. **The stage's own strings.** Status lines, per-gate error strings, assert text, format strings. `"%s/%s/%s%s"` builds the level-script path. Some name tables are stubbed out: one error-to-text function returns "HIDDEN" for every code, and the menus' print functions are compiled out.
2. **Hash immediates.** A name exists only as its hash, loaded as a 64-bit immediate. Hash a candidate and scan for its 8 bytes: `mov rcx, H("r_fog")` sits right before the dvar's registration.
3. **Registration tables.**

   | Table | Row |
   |---|---|
   | Lua natives | Two call forms into one registrar. See [Lua and the menus](/re/engine/lua-lui.md). |
   | GSC natives | 32 bytes: `{u32 hash, u32 minArgs, u64 maxArgs, function, flags}` |
   | Lobby messages | `{u64 msgId, u64 handler}`, 14 rows |
   | Asset types | Names at `g_xassetTypeNames`; per-type link callbacks and name offsets beside them |

4. **Error codes as 32-bit immediates.** A dialog shows three words; the log's line carries the code. Scan for the code.
5. **Forwards from what runs**: the callees of the per-frame function, the dispatcher, the state machine.
6. **Writers of a field.** Scan for the store's encoding across the subsystem (`C6 4x 3C 01` is `mov byte [reg+3Ch], 1`). This found a third writer the cross-references missed.
7. **Callers that Arxan hides.** Scan for every `E8` or `E9` whose target lands on the function. Or read the consumer of a message instead of its builder.
8. **Imports.** The import table is complete for what it covers: `getaddrinfo`, `gethostbyname` and `connect` for the network, `GetRawInputBuffer` for input, the certificate functions for TLS.
9. **Data outside the executable.** Decompiled scripts and menus hold the gameplay and menu rules. Zone traces and the zones themselves hold the layouts.
10. **Prior art, for layouts.** Read it, then write your own code: Greyhound for models and meshes, ACTS for the script format and hashes, the boiii and shield projects for the client architecture.

## Working with the disassembler on this binary

| Habit | Why |
|---|---|
| Open the database without re-running analysis | The image is half a gigabyte. Analysis is already saved. |
| Never search the whole image for a string or a regular expression | It builds a huge cache and blocks. Scan the dump file with Python instead. |
| Bound every byte search to a range | The same |
| Name functions `Subsystem_VerbObject`, globals `g_`, inferred names `_cand` | So that a name reads the same in the notes, the code and the database |
| Put the signature, the argument meanings and the evidence in the comment | The comment is the record |
| After a rename, check that it was applied | A rename with a wrong argument shape fails without an error |

## Instruments inside the game

| Instrument | Where | Use |
|---|---|---|
| The log | `cw-mod\client.log` | Everything. See [Running the game](/guide/running.md). |
| The Demonware journal | Overlay, Demonware tab | Every name resolved and connection made |
| The login transcript | A detour on the login status setter | The login's own status lines |
| The lobby-message transcript | Overlay, Session tab | Each message after decryption, where a packet capture sees nothing |
| The zone trace | `"mapkit_trace"` | Where each asset starts in a zone |
| The asset-usage census | `"mapkit_usage"` | What a match looked up |
| The Lua dump | Overlay, LUI Menus tab | The menus' bytecode |

An external debugger is not one of them: attaching one closes the game. See [Arxan](/re/client/arxan.md).

## See also

- [Developer tools](/guide/tools/dev-tools.md): the scripts, with usage
- [Hashes and names](/re/method/hashes.md)
- [Hooking](/re/client/hooking.md)

<!-- sources: cw-mod .claude/skills/bocw-reverse-engineering/SKILL.md (sections 4, 5, 7), client/overlay/tabs/*.cpp @ 36b1f18 + working tree, 2026-10-08 -->

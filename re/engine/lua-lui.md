# Lua and the menus (LUI)

> Every menu of the game is Lua run by a modified LuaJIT. This page gives the value format, the C API, how names work, how a menu opens, and the engine bug that killed the game on any Lua error. **Status:** Done.

## In short

- The menus' rules (locks, lobby flow, what a button does) are **in Lua**, an asset in the zones. The executable holds the VM and about 2,500 native functions.
- The VM is LuaJIT-derived with a Lua 5.1 C API. Values are NaN-boxed with the game's own type tags.
- Identifiers are compiled to **hashed names**: `Engine.GetModel` in the source is a 63-bit hash at run time, not a string.
- The whole C API is [caller-guarded](/re/client/arxan.md): called from the mod without a thunk, it does nothing.
- There is no native "open menu by name". A menu opens through an `addmenu` event that Lua resolves.

## Values

```text
tag     = (int64)v >> 47
payload = v & 0x7FFFFFFFFFFF
```

| Tag | Type | Note |
|---|---|---|
| (none) | number | Anything outside the tag range is a double |
| -1 | nil | An empty table slot is all ones, which also reads as tag -1 |
| -2, -3 | false, true | |
| -5 | string | Length u32 at +16, characters at +24 |
| -6 | hashed name | The hash at +16. Type byte 5 at +8. |
| -10 | function | C flag u8 at +11, code or native pointer at +32 |
| -13 | table | See below |
| -14 | LUI element | The userdata behind every widget |

| `lua_State` | | `Table` | |
|---|---|---|---|
| +24 | `global_State` | +24 | Hash part: nodes of 24 bytes (value +0, key +8) |
| +32 | Stack base (allocated) | +32 | Metatable (also for an element) |
| +40 | Stack end | +40 | Array part, 8 bytes per entry |
| +48 | `_G`, a raw table pointer | +48 | Last node index (u32) |
| +56 | `L->top` | +52 | Array size (u32) |
| +80 | `L->base` | | |

- The canonical nil object is at `global_State + 304`. The string table is at `global_State + 0` (buckets) and `+8` (mask).
- `g_luiCtx` **is** the `lua_State*` of the menus.

## Bytecode

- Dumped chunks start with `LJ`. A chunk's name is `x64:<hash of the path without .lua>.lua`.
- Instructions are four bytes: op, A, B, C. Known operations: 18 MOVE, 40 LOADK, 55 GETGLOBAL, 56 SETGLOBAL, 57 the hashed-name lookup, 58 GETFIELD, 67 CALL.
- The registers are the frame: `R[n]` is frame slot `n + 1`, and the running function is slot `-1`.
- Constants are raw object pointers indexed backwards from an end pointer, not boxed values.
- **Local names are kept**, packed, with their live ranges. Line numbers are kept as deltas, 1, 2 or 4 bytes wide per function.

`tools/lua_disasm.py` reads every dumped chunk. See [Developer tools](/guide/tools/dev-tools.md).

## Names are hashes

| In Lua source | What it is at run time |
|---|---|
| `Engine.PrintInfo` (in a stock chunk) | A lookup by hashed name |
| `Engine["PrintInfo"]` or `Engine.PrintInfo` in **your** text | A lookup by **string**: finds another slot, or nothing |
| `Engine[@"PrintInfo"]` | The game lexer's own hash literal: a hashed name |
| `element[@"GetModel"](element)` | A method call by hash |

- Natives are registered by one function, `LUI_RegisterEngineNatives_cand`, 70,983 bytes long, with **2,556** registrations in two call forms.
- `_G` and `Engine` refuse plain assignment. Use `rawset`.
- Every `Enum.X` table is an empty read-only proxy. The values are behind `getmetatable(proxy).__index`.
- The parser rewrites the first string after the identifier `require` into the hashed chunk name.
- `debug.getinfo` raises.

## The C API

All 65 entries call `lua_index2adr`, which is how they were found and named against Lua 5.1's source.

| Name | RVA | IDA address | Signature |
|---|---|---|---|
| `lua_index2adr` | 0xD27EC10 | 0x7FF729E3EC10 | |
| `lua_getfield` | 0xD27CC50 | 0x7FF729E3CC50 | `void (void* L, int idx, const char* k)` |
| `lua_setfield` | 0xD27D460 | 0x7FF729E3D460 | `void (void* L, int idx, const char* k)` |
| `lua_gettable` | 0xD27CD90 | 0x7FF729E3CD90 | `void (void* L, int idx)` |
| `lua_rawgeti` | 0xD27CE40 | 0x7FF729E3CE40 | `void (void* L, int idx, int n)` |
| `lua_next` | 0xD27E310 | 0x7FF729E3E310 | `int (void* L, int idx)`. No type check: faults on a non-table. |
| `lua_pushvalue` | 0xD27B2E0 | 0x7FF729E3B2E0 | `void (void* L, int idx)` |
| `lua_settop` | 0xD27B1E0 | 0x7FF729E3B1E0 | |
| `lua_type` | 0xD27B860 | 0x7FF729E3B860 | `int (void* L, int idx)` |
| `lua_tolstring` | 0xD27BD70 | 0x7FF729E3BD70 | `const char* (void* L, int idx, size_t* len)` |
| `lua_tonumber` | 0xD27EA90 | 0x7FF729E3EA90 | `double (void* L, int idx)` |
| `lua_getmetatable` | 0xD27D150 | 0x7FF729E3D150 | `int (void* L, int objindex)` |
| `lua_createtable` | 0xD27CF30 | 0x7FF729E3CF30 | `void (void* L, int narr, int nrec)` |
| `lua_pcall` | 0xD27DB70 | 0x7FF729E3DB70 | Modified by the game. Drive it only through the wrapper below. |
| `LUI_ProtectedCall` | 0x56D3FA0 | 0x7FF722293FA0 | `int (void* L, int nargs, int nresults, int errfunc)`. Not guarded. |
| `lua_load` | 0xD288AE0 | 0x7FF729E48AE0 | `int (void* L, reader, void* data, const char* chunkname)`. Takes bytecode **or text**. |
| `lua_getstack` | 0xD287100 | 0x7FF729E47100 | `int (void* L, int level, void* ar)` |
| `lua_getinfo` | 0xD287E20 | 0x7FF729E47E20 | `int (void* L, const char* what, void* ar, int extra)` |

Three traps when driving it from outside:

1. Push the engine's own nil, never a built one. `lua_next` on a "nil" it does not recognise raises "invalid key to 'next'" with no protected call above it.
2. Save stack positions relative to `L->base`. A push can reallocate the stack.
3. After every guarded call, check that `L->top` moved. If it did not, the guard rejected the call.

## How a menu opens

The `openmenu` console command is gone, but its function is still there:

```text
Cmd_OpenMenu_f:
    controller = CL_LocalClientToController(localClient)
    UI_SetUiActive(localClient, true)
    LUI_DispatchAddMenuEvent(LUI_GetRootName(controller), hash(name), -1, g_luiCtx)

LUI_DispatchAddMenuEvent, in Lua terms:
    _G.LUI.roots[rootName]:processEvent(<an "addmenu" event with the menu's hash and the controller>)
```

The menu registry is the Lua table `LUI.createMenu`, keyed by hashed name. There is no native list.

| Name | RVA | IDA address | Signature |
|---|---|---|---|
| `Cmd_OpenMenu_f` | 0xA4037E0 | 0x7FF726FC37E0 | |
| `LUI_DispatchAddMenuEvent` | 0xADD7770 | 0x7FF727997770 | `i64 (const char* root, u64 menuHash, int controller, void* L)` |
| `LUI_GetRootName` | 0x8D17050 | 0x7FF7258D7050 | `const char* (int controller)` |
| `UI_SetUiActive` | 0x8D272E0 | 0x7FF7258E72E0 | `void (i64 localClient, bool active)` |
| `CL_LocalClientToController` | 0xC058BD0 | 0x7FF728C18BD0 | `int (int localClient)` |
| `LuiEvent_Dispatch` | 0xAFCCA80 | 0x7FF727B8CA80 | Runs a builder under the protected call |
| `LUI_RunFile` | 0xAFCCCD0 | 0x7FF727B8CCD0 | `u8 (void* L, const char* name)`. Loads a chunk asset and runs it. |
| `LuaFile_LoadAsset` | 0xCA82580 | 0x7FF729642580 | The engine's only caller of `lua_load` |
| `g_luiCtx` | 0x139F2F38 | 0x7FF7305B2F38 | The `lua_State*` |

Two ways, two limits:

| Way | Builds the menu with | Limit |
|---|---|---|
| `addmenu` | The controller only | A menu that reads its session mode raises ("table index is nil") |
| `CoD.BaseUtility.OpenOverlay(self, menu, controller, params)` | Params, as the game's buttons do | `self` must be an **open menu**, not the root |

A menu opened by hand can still raise later, from its own handlers.

## When Lua raises

The engine runs a builder under a protected call with `luaL_traceback` as the error function. When the call fails, `LuiError_ReportFatal` reads the message and hands it to `LuiError_ReportAndDie`, which files a record, waits about a second and **ends the process on purpose**. No exception handler sees it.

And before that could happen, the game crashed by itself:

| Step | Function | What happens |
|---|---|---|
| 1 | `luaG_getobjname` | On the hashed-name call path it returns the text `"xhashfunc"` **without writing the name** |
| 2 | `lua_getinfo` | Clears the name only when the result is null, which it is not |
| 3 | `luaL_traceback` | Formats `" in function '%s'"` with a pointer nobody set |

Usually the stray pointer was readable and the traceback printed nonsense such as `in function '@&['`. When it was not, the process died inside the string formatter. Offline nothing raises, so nobody sees it. The online menus raised on every build.

| Name | RVA | IDA address | Signature |
|---|---|---|---|
| `luaL_traceback` | 0xD288320 | 0x7FF729E48320 | `u64 (void* B, void* L, const char* msg, int level)` |
| `luaG_getobjname` | 0xD2876D0 | 0x7FF729E476D0 | `const char* (void* L, void* proto, void* pc, uint reg, const char** nameOut)` |
| `aXhashfuncNoName` | 0xE3ED9B0 | 0x7FF72AFAD9B0 | The literal returned on the non-writing path |
| `LuiError_ReportFatal` | 0x5702340 | 0x7FF7222C2340 | `u64 (const char* context, void* L)` |
| `LuiError_ReportAndDie` | 0x57004C0 | 0x7FF7222C04C0 | |

## What cw-mod does

| What | Where | How |
|---|---|---|
| Repairs the traceback bug | Detour on `luaG_getobjname` | Writes a valid name pointer when the returned pointer **is** that one literal. Always installed. |
| Reads the failing stack | Detour on `luaL_traceback` | An error function runs before the stack unwinds, so the frames and their arguments still exist. Logs each frame, the instruction and the names of its constants, with memory reads only. |
| Survives a failing menu | Detour on `LuiError_ReportFatal` | Logs the message. On an online boot, and for a menu the overlay opened, it drops the report instead of ending the process. |
| Skips a missing chunk | Detour on `LUI_RunFile` | `ui/ffotd_tu<N>.lua` is skipped when it is not loaded. A missing chunk is a hard exit inside the asset lookup, before any Lua error exists. |
| Shows the menus' own narration | Detours on the three print natives | `Engine.PrintInfo`, `PrintWarning` and `PrintError` are compiled out. Their arguments go to the log as `(LuaPrint)` lines. |
| Opens a menu | Overlay, LUI Menus tab | Replays `Cmd_OpenMenu_f` with the real controller, or calls `OpenOverlay` |
| Lists the menus | Same tab | Reads the keys of `LUI.createMenu` out of memory |
| Runs your Lua | [Menu scripts](/re/engine/ui-scripts.md) | `lua_load` on text |

## How we found it

- A walk of `_G` returned nothing and no error. The first instructions of `lua_getfield` test the return address: the caller guard.
- The first online boot died right after its first Lua error, at a `strlen` reached from `luaL_traceback`. Decompiling the three functions gave the chain above. The same bug had been in the logs for weeks as garbled function names.
- "Lua strips local names" was assumed and was wrong. The names are there; the engine only declines to print them.

## Limits and open points

- The opcode table is only partly mapped.
- A hashed name can be turned back into text only if that text is interned in the current UI state, or known from a word list.
- A menu's data models are built by other menus. Opening one out of order raises.

## See also

- [Menu scripts](/re/engine/ui-scripts.md) and the [guide](/guide/scripting/ui-scripts.md)
- [UI text](/re/engine/ui-text.md)
- [Errors](/re/engine/errors.md)
- [Hashes and names](/re/method/hashes.md)

<!-- sources: cw-mod client/game/game.hpp (kLua* layout notes), lua_state.cpp, lui_menu.cpp, dump_anchors.hpp (Lua C API, debug API, traceback bug, LuiError_ReportFatal, LUI_RunFile, opening menus, lua_load), client/hooks/hook.hpp, .claude/skills/bocw-reverse-engineering/SKILL.md (sections 3.4, 9) @ 36b1f18 + working tree, 2026-10-08 -->

# Arxan

> The game's executable is protected by Arxan. This page lists what the protection does, how the mod gets past it at start-up, and how the mod calls functions that check who is calling. **Status:** Done.

## In short

- The file on disk is encrypted. Analysis works on a [dump](/re/method/binary.md).
- At run time Arxan checksums its code and **writes the original bytes back** over changes. The bypass corrects the checksums and blocks those writes where the mod has hooks.
- Some engine functions return at once, having done nothing, when their caller is outside the game image. The mod calls them through a small thunk that makes the call look local.
- A debugger cannot be attached. Everything is observed from inside the process.

## What it does to you

| Mechanism | Symptom | Answer |
|---|---|---|
| Encrypted image on disk | A disassembler shows junk | Dump the running game |
| **Caller guard** | A function called from the mod returns having done **nothing**: no crash, no error | Call through a thunk |
| The thunk's limit | It forwards 4 register arguments. A 5th is read from the wrong place. | Call such a function directly, after checking it has no guard |
| Guard plus detour | The detour's call to the original comes from the mod, so the original does nothing, and the breakage shows far away | Call the original through a thunk too |
| A guard variant in the string table | From outside the image it stores a hash **inverted**, so the string lands in another bucket | Thunk |
| Split thunks | Hooking the stub misses callers; calling a getter thunk from the mod faults | Hook or call the implementation |
| Flattened control flow | Missing cross-references | Scan for relative calls; read the consumer side |
| Anti-debug | Attaching a debugger closes the game | Log from inside |
| Start-up race | Now and then a crash before the mod's entry point | Start again |
| Zone signature trap | A zone whose signature fails corrupts the asset free list; the **next** zone dies | Blame the zone loaded before |

## The start-up bypass

The bypass comes from the open t9-mod lineage the client is built on. It runs inside a hook on `NtAllocateVirtualMemory`, on the game's own thread: Arxan allocates an executable region the size of ntdll for its private copy, and that allocation is the cue.

| When | Step | What it does |
|---|---|---|
| First such allocation | Checksum stubs | Finds every place Arxan stores a computed checksum (three byte patterns: 57, 41 and about 30 sites) and redirects each to a generated stub. The stub puts the **original** checksum back on the stack, so a hooked function still passes. |
| First such allocation | Healing stubs | Finds every place Arxan writes original bytes back (four patterns, about 820 sites). The stub skips the write when it would land on one of the mod's own hooks. |
| Sixth such allocation | TLS callbacks | Replaced by an empty function |
| Sixth | `KiUserApcDispatcher` | Arxan overwrites its start. The clean bytes are read from the ntdll file on disk and written back, so no Windows version is hard-coded. |
| Sixth | Thread start | The game swaps ntdll's pointer to `BaseThreadInitThunk` for its own, which runs timing checks on new threads. The pointer is found by scanning `RtlUserThreadStart` for a `mov rax, [rip+disp]`, checked to lie inside ntdll, and restored. |
| Sixth | 14 ntdll debug functions | Arxan overwrites `DbgBreakPoint`, `DbgUiRemoteBreakin` and twelve more with a jump to `ExitProcess`, then checksums its own patch. The mod saved each function's first 15 bytes when the DLL loaded and writes them back. The 14 sites in the game that read those bytes are pointed at a buffer that holds the patched form, so the checksum still passes. |

Beside it, system hooks answer the protection's questions: `GetThreadContext` and `SetThreadContext` (hardware breakpoints), `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess`, `CreateMutexExA` (the single-instance check), and the window-listing calls, where tool names such as a debugger's are blanked out of titles.

## The caller guard

A whole class of engine functions opens with a check of its own return address. In words:

```text
ret = the return address on the stack
if ret is below the image base, or above image base + 0x20000000:  leave
if the byte at ret-5 is E8:                                        go on   (a call rel32 came before)
if the byte at ret-2, -3, -4, -6 or -7 is FF:                      go on   (a call through a register or memory)
otherwise:                                                         leave
```

"Leave" is not a crash and not an error return. The function skips its body and returns as if it had run. Called from the mod, the Lua C API walks nothing and reports success.

## The thunk

The check only looks at the return address, so the answer is to hand it one inside the image. The image already holds what is needed: a call followed by `add rsp, 28h; retn`.

| Name | RVA | IDA address | Note |
|---|---|---|---|
| (return gadget for ArxanCall thunks) | 0x4F3D2C | 0x7FF71D0B3D2C | `48 83 C4 28 C3`, right after an `E8` call |

`ArxanCall::MakeThunk` builds 30 bytes per target:

| Bytes | Instruction | Why |
|---|---|---|
| `48 83 EC 30` | `sub rsp, 30h` | Make room; keep the stack aligned as a callee expects |
| `49 BB <gadget>` | `mov r11, gadget` | |
| `4C 89 1C 24` | `mov [rsp], r11` | The return address the callee will see |
| `48 B8 <target>` | `mov rax, target` | |
| `FF E0` | `jmp rax` | Enter the callee |

The callee returns into the gadget. `add rsp, 28h` then `retn` pops the mod's real return address. `rax` is untouched, and `rcx`, `rdx`, `r8`, `r9` pass through.

**Limit: register arguments only, so at most four.** A fifth argument sits on the caller's stack, and the thunk has moved the stack by 0x30. `Ddl_InitInstance` takes seven: through the thunk, its fifth became a callback the engine later jumped to. The typed `MakeThunk` now refuses such a signature at compile time.

`ArxanCall::Init` checks the gadget's bytes before use. On another build it reports "not ready" and every caller refuses, instead of calling directly and getting plausible empty results.

## Functions that carry the guard

| Name | RVA | IDA address | Seen as |
|---|---|---|---|
| `lua_getfield` | 0xD27CC50 | 0x7FF729E3CC50 | Every entry of the Lua C API |
| `lua_load` | 0xD288AE0 | 0x7FF729E48AE0 | |
| `luaL_traceback` | 0xD288320 | 0x7FF729E48320 | |
| `SL_GetString_Guarded` | 0x1BC3780 | 0x7FF71E783780 | The variant that inverts the hash |

Functions checked to have **no** guard, and so called directly: `Ddl_InitInstance`, `LUI_ProtectedCall`, `DecryptString`, `DB_Signature_VerifyZone`, `LUI_RunFile`.

## How we found it

- The game crashed during start-up, before the mod's entry point, four builds in a row. The log's last line pointed at one restore step, which had a real bug: it looked for `BaseThreadInitThunk` in ntdll, and that function is exported by kernel32.
- Fixing that bug changed nothing: the crash point was byte-identical. A correct bug fix is not a cause.
- Switching parts of the bypass off one by one found it: a helper thread that kept writing a value into the process's "being debugged" flag. With that thread not started, the game reached the menu.
- The caller guard was found the other way round: a walk of the Lua state "worked" and returned nothing. Reading the first instructions of `lua_getfield` showed the return-address test.

## Limits

- The 14 ntdll sites are fixed addresses for this build.
- The start-up race is not solved, only rare.
- A function reached through a thunk with a wrong argument count fails late and far away. Count the arguments first.

## See also

- [Hooking](/re/client/hooking.md): detours on guarded functions
- [The client](/re/client/overview.md)

<!-- byte examples re-read from the dump file 2026-10-08: the gadget is 48 83 C4 28 C3 and the call before it is E8 44 7F 03 0D (a comment in arxan_call.hpp prints 7E) -->
<!-- sources: cw-mod client/game/arxan_call.hpp, client/arxan/arxan_utility.cpp, arxan_stubs.cpp, arxan_internal.hpp, arxan_internal.cpp, ntdll_restore.hpp, sys_hooks.hpp, sys_hooks/ntdll/NtAllocateVirtualMemory.cpp, client/common.cpp, .claude/skills/bocw-reverse-engineering/SKILL.md (section 6), docs/crash_boot_arxan.md (deleted; read from git history and checked against the code) @ 36b1f18 + working tree, 2026-10-08 -->

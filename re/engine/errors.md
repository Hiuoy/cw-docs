# Errors: how the game stops

> The ways this game ends a match or the process, how to read its three-word error names, and the story of the one error that took five wrong fixes. **Status:** Done.

## In short

- An error shows three words and a number ("Uniform 58 Guerrilla Boa"). That is a rendering of a 32-bit **code**. The log line carries the code, and the code can be found in the image.
- `BB_Alert` only **reports**. Text in a popup proves that the report ran, not who raised the error.
- Some exits are deliberate and cannot be caught: a Lua error in a menu, a missing asset of certain types, an error on the asset thread.
- An online session with no Battle.net sign-in is ended by a **watchdog**, not by any error handler.

## The ways out

| Path | Function | What it does | Survivable |
|---|---|---|---|
| Drop | `Com_Error` at the drop level | Ends the match, back to the menus | Yes |
| The error popup | `ErrorQueue_Push` | Queues `{flag, level, text}` in a ring of 4. The menus draw it. Returns 1 queued, 0 refused: on 0 the **caller** raises the error itself. | Depends on the level |
| Battle.net class | `Com_Error` at level 1024 | A dialog that cannot be closed, then exit | No |
| Menu Lua error | `LuiError_ReportFatal`, then `LuiError_ReportAndDie` | Files a record, waits about a second, ends the process | Only by a [detour](/re/engine/lua-lui.md) |
| Missing asset | Inside `DB_FindXAssetHeader` | For some asset types a miss is fatal there, before the caller's null check | No |
| Error on the asset thread | | Any drop raised on the asset-loading thread becomes a hard exit | No |
| UI error code | `LUI_ReportUiErrorCode_cand` | "UI Error 100004" and a dialog. Returns. | Yes, by itself |

## Reading a three-word error

1. Find the `(BB_Alert)` line in `cw-mod\client.log`. It has the type (`err_drop` or `sys_error`), the original message, the thread, and the call chain as offsets into the game image.
2. The first offset inside the image is the code that raised it. Paste it into the disassembler.
3. If the message carries a hex code, search the dump for it as a 32-bit immediate.

Known ones:

| Shown | Code | Cause |
|---|---|---|
| Uniform 58 Guerrilla Boa | 0x3F6FDE09 | A zone's signature failed **earlier**. The engine's response corrupts the asset free list on purpose, and the next zone to allocate dies. Blame the zone loaded before. |
| (a `sys_error` with `<hash>,luafile` or `<hash>,localizeentry`) | 0x3580ADA5 | A missing asset of a type for which a miss is fatal |
| (a `sys_error` right after a drop) | 0xE4BD8598 | The drop happened on the asset thread |
| Boy 501 Gothic Missile | | An online-mode session was dropped to offline when Demonware connected. Fixed: see below. |
| West 683 Winning Clover | | The match-start stats copy failed. See [Progression](/re/engine/progression.md). |
| November 406 Cut Rain | | A script's clientfield type string was not the engine's `"int"`. See [The GSC VM](/re/engine/gsc-vm.md). |

More in [Troubleshooting](/guide/troubleshooting.md).

## The Battle.net wall

With network mode 2 the client brings its Battle.net layer up for real. With nothing to sign in to, every online boot ended in `BLZBNTBGS000003EA` and "exit to desktop". Each fix below was found by reasoning **backwards from the message text**. Each was installed, measured, and changed nothing.

| # | Hooked | Why it looked right | What the log said |
|---|---|---|---|
| 1, 2 | The two Battle.net error reporters | They format `BLZBNTBGS%08X` and call `Com_Error(1024)` | Suppressed, and the popup still came |
| 3, 4 | The two functions that set the first-party error state | The popup is a menu that **asks** for the stored error | Never fired |
| 5 | `ErrorQueue_Push`, dropping level 1024 | "Every producer goes through the queue" | Never fired |

Then the question was turned round: what runs every frame? `LiveFirstParty_Frame` ends in a call to `LiveUser_ForceSignOutAndFatal`, a "you must stay signed in" check:

```text
LiveFirstParty_Frame:            runs only while nodw is false
    if signed in, and four more conditions:
        LiveUser_ForceSignOutAndFatal()
            sign both controllers out
            build the message
            Com_Error(1024) directly      <- no queue, no reporter
```

The whole frame is behind `nodw`. So the fix is not a hook at all: set `nodw` true before the menus are built. See [The boot profile](/re/client/boot-profile.md). The detours stay installed as a second line, switched by one atomic.

Two more, found on the way:

| Error | Cause | Fix |
|---|---|---|
| The title screen's error dialog on an online boot with the backend | The "disconnected" callback of the Battle.net layer stores an error about 10 seconds in. The title screen polls it every 400 ms. | The detour runs the original, then clears the stored error |
| "Boy 501 Gothic Missile" one second after login | A function that **promotes** the user to "signed in online" on connect also asks for a drop to offline when the user was "local" in an online session | The detour lets the promotion run and returns 0 for the drop |

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `Com_Error` | 0x571A030 | 0x7FF7222DA030 | `(file, line, level, fmt, ...)` | Level 1024 is not survivable |
| `ErrorQueue_Push` | 0x5789D60 | 0x7FF722349D60 | `char (int level, const char* message, char flag)` | The popup's queue |
| `BB_Alert` | 0x1B261E0 | 0x7FF71E6E61E0 | `void (const char* type, const char* msg)` | Reporting only |
| `LuiError_ReportFatal` | 0x5702340 | 0x7FF7222C2340 | `u64 (const char* context, void* L)` | |
| `LuiError_ReportAndDie` | 0x57004C0 | 0x7FF7222C04C0 | | |
| `LiveFirstParty_Frame` | 0xCAF5F00 | 0x7FF7296B5F00 | | Per frame, gated on `nodw` |
| `LiveUser_ForceSignOutAndFatal` | 0xB37A320 | 0x7FF727F3A320 | `char* ()` | The watchdog |
| `LiveUser_HandleSignOut` | 0xCB92990 | 0x7FF729752990 | | A sign-out, silent offline |
| `LiveUser_BuildSignOutErrorMessage` | 0xCB93600 | 0x7FF729753600 | | Returns "no message" unless the session is online |
| `LiveUser_PromoteSigninOnline_MaybeDrop` | 0xCB93740 | 0x7FF729753740 | `char (u32 controller, const char** outMsg)` | Promotes, and may ask for a drop |
| `BnetError_ReportFatalUnguarded` | 0xCAF7C70 | 0x7FF7296B7C70 | `u64 (u32 bgsErrorCode)` | Reporter 1 |
| `BnetError_ReportFatalIfSignedIn` | 0xCAF7CF0 | 0x7FF7296B7CF0 | `void (uintptr ctx, u32* bgsErrorCode)` | Reporter 2 |
| `FirstParty_SetError` | 0xCC1F340 | 0x7FF7297DF340 | `u64 (uintptr obj, int code)` | State 4, with a code |
| `FirstParty_SetErrorState` | 0xCC1E380 | 0x7FF7297DE380 | `u64 (uintptr obj)` | State 4, no code |
| `FirstParty_OnBgsDisconnected` | 0xCC1F2E0 | 0x7FF7297DF2E0 | `u64 (uintptr obj, uintptr, const u32* bgsCode)` | The third writer |
| `Lua_FirstParty_GetErrorMessage` | 0x1D5EF40 | 0x7FF71E91EF40 | | What the popup's menu calls |
| `DB_TamperResponse_CorruptEntryFreeList` | 0xB301410 | 0x7FF727EC1410 | | The response to a failed zone signature |

The first-party object: state at `+56` (3 signed in, 4 error), has-error at `+60`, disconnected at `+61`, the code at `+64`.

## What cw-mod does

| What | Detail |
|---|---|
| Mirrors every `BB_Alert` | Type, original message, thread, and 16 return addresses as image offsets |
| Logs script string state on a drop | A script error drops with an obfuscated code; the loader's string check runs at that moment |
| Keeps a crash log | See [The client](/re/client/overview.md) |
| Suppresses the Battle.net class | Only on an online profile. On an offline start a real Battle.net failure is still fatal. |

## What we learned

- Trace **forwards** from the code that runs, not backwards from the text on screen.
- Log pass-throughs. "The hook is silent" was the evidence each time, and it was only readable because every hook logged every call.
- Garbled text is an observation, not decoration.
- The game heals itself between runs: retries, files it writes back, and a counter that purges downloaded content after three crashed starts. A change in behaviour with no change in code still needs an explanation.

## See also

- [Troubleshooting](/guide/troubleshooting.md)
- [Lua and the menus](/re/engine/lua-lui.md): the traceback bug
- [The cycle](/re/method/cycle.md)

<!-- sources: cw-mod client/game/dump_anchors.hpp (BLZBNTBGS notes, LiveUser_SignOutBuildDropMessage, LuiError_ReportFatal, LUI_RunFile, DecryptString notes), client/hooks/hook.hpp, client/hooks/impl/game/BB_Alert.cpp, client/game/boot_profile.cpp, .claude/skills/bocw-reverse-engineering/SKILL.md (sections 5, 6, 9, 10, 12) @ 36b1f18 + working tree, 2026-10-08 -->

# Hooking

> How the client finds a function, replaces it, and stays alive when a guess is wrong. The rules at the end each cost a failed boot to learn. **Status:** Done.

## In short

- A function is found by an **anchor** (its address in our dump, moved to the live base) or by a **byte signature**.
- A detour is a typed template with a callback and a pointer to the original. Each hook has its own file.
- System hooks go in when the DLL starts. Engine detours go in at the game's **first exception**.
- Every detour is checked after it is enabled: the target must start with `E9`.
- Every read of game memory by a guessed offset is guarded.

## Finding the target

| Way | Looks like | Good | Bad |
|---|---|---|---|
| Anchor | `live = moduleBase + (kDump_X - kDumpImagebase)`, bounds-checked | Exact. One line per address, with the evidence as its comment. | Build-locked |
| Signature | `48 89 5C 24 ? 57 48 83 EC 20 ...`, then optional steps | Survives code that moves | Can match more than once, or the wrong function |

A signature result can be stepped: `Add(3).Rip()` moves 3 bytes in, reads the 32-bit displacement there and follows it, which turns `mov rcx, [rip+disp]` into the address of the global. See [Address and byte math](/re/method/address-math.md).

Signatures in the client and where they land in our dump:

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `Dvar_FindVar` | 0xC0B2090 | 0x7FF728C72090 | The implementation. The public entry is a jump stub that can move. |
| `g_dvarHashTable` | 0x18A55570 | 0x7FF735615570 | From the `and ecx, 3FFh` bucket load inside `Dvar_FindVar` |
| `Dvar_SetBoolFromSource` | 0xC0B5580 | 0x7FF728C75580 | |
| `Dvar_SetIntFromSource` | 0xC0B7530 | 0x7FF728C77530 | The signature matches three functions in the dump. The scanner takes the first. |
| `p_dvar_nodw` | 0x17160108 | 0x7FF733D20108 | The slot that holds the `nodw` dvar's pointer |
| `p_dvar_showOverStack` | 0x11847DF8 | 0x7FF72E407DF8 | The slot the [tick](/re/client/overview.md) borrows |
| `g_scrInitialized` | 0x139F4826 | 0x7FF7305B4826 | A byte: the script system is up |
| `CL_Disconnect` | 0x5CD2110 | 0x7FF722892110 | |
| `LobbyBase_SetNetworkMode` | 0xAF59B60 | 0x7FF727B19B60 | See [The boot profile](/re/client/boot-profile.md) |
| `BB_Alert` | 0x1B261E0 | 0x7FF71E6E61E0 | In our dump its first five bytes are the mod's own detour |

`RtlDispatchException` is found the same way inside ntdll, with one signature for Windows 10 and one for Windows 11.

## The hook pattern

Declared in `client/hooks/hook.hpp`, implemented in `client/hooks/impl/game/<Name>.cpp`:

```cpp
// hook.hpp
using HK_Dw_GetLoginFlow = HookPlate::FastcallHook<"Dw_GetLoginFlow", std::uint64_t, void*>;
Memory::MinHook<Game::Functions::Dw_GetLoginFlowT>* m_Dw_GetLoginFlowHK{};

// impl/game/Dw_GetLoginFlow.cpp
template <>
std::uint64_t Client::Hook::Hooks::HK_Dw_GetLoginFlow::hkCallback(void* loginConfig) {
	if (Client::Game::DwBackend::g_Enabled) {
		return 9;  // studio auth
	}
	return m_Original(loginConfig);
}
```

| Kind | Tool | Used for |
|---|---|---|
| Inline detour | MinHook, behind `Memory::MinHook<T>` | Engine functions, ntdll, user32 |
| Import-table hook | `Memory::IAT` | `getaddrinfo`, `gethostbyname`, `connect`, `SetUnhandledExceptionFilter`. The import table is the whole surface, and no code byte changes. |

## When hooks go in

| Moment | What | Why then |
|---|---|---|
| DLL start | The Arxan system hooks | Before the protection runs |
| `DiscordCreate` | Exception dispatch, input, network imports, the tick | First safe point |
| First exception through `RtlDispatchException` | Every engine detour (`PostArxanDetectionHooks`) | Arxan's start-up checks are over. Claimed with an atomic exchange: two threads once faulted together and installed everything twice. |

By then the game's own start-up code has already run. A detour on `PlayerData_Init` was installed on a function that had already been called. The fix was a **self-timing seam**: hook the tick that submits the work, so the first call necessarily comes before the work goes out.

## Guarded reads

```cpp
template <typename T>
bool SafeRead(const void* addr, T& out);   // false if the address faults; out untouched
bool SafeCopy(void* dst, const void* src, std::size_t n);
```

- The `__try` lives in a helper that holds only plain data: MSVC refuses `__try` in a function that needs object unwinding.
- A probe raises a per-thread counter first. The crash logger sees a fault **before** the `__except` does, and without the counter it reported the mod's own handled probes as crashes.

## The rules

| # | Rule | Why |
|---|---|---|
| 1 | Install always, switch the behaviour with an atomic | A mode switched later from the overlay had no hook |
| 2 | Start-up code has already run when engine detours go in | A detour that never fired |
| 3 | Engine calls come from the game-thread tick | The overlay only draws: a button queues a closure and the tick runs it |
| 4 | Guard every pointer chase | A wrong offset must be a log line, not a crash |
| 5 | Log the pass-through too, once per caller, with a cap, and count what was muted | "The hook is silent" proved nothing. One event was 1,999 of the first 2,000 lines. |
| 6 | Check the detour is live (`E9` at the target) | The wrapper drops MinHook's return code |
| 7 | Read the engine's own witness, not a return code | A guarded function returns "success" having done nothing. For a Lua native, compare `L->top` before and after. |
| 8 | Scope a forced answer to its readers | One dvar had four readers that wanted opposite answers. Bracket the outer function. |
| 9 | Never read a dvar's value block directly | A bool is stored mixed with a per-process key. See [Dvars](/re/engine/dvars.md). |
| 10 | A hook on a worker thread must not call Lua or block | An error on the asset thread is a hard exit |
| 11 | A hook that changes data changes what the next hook sees | A veto's `0 → 0` became `1 → 0`. Detect by the end state. |
| 12 | A detour on a [caller-guarded](/re/client/arxan.md) function must call the original through a thunk | The original did nothing, and the break showed far away |
| 13 | Count the arguments before using a thunk | A 7-argument function crashed map load |

## Limits

- A signature that matches more than once binds the first match. Nothing reports the others.
- Anchors are for one build.

## See also

- [Arxan](/re/client/arxan.md): the caller guard and the thunk
- [Function index](/re/reference/functions.md): every anchored address
- [The cycle](/re/method/cycle.md): when to instrument

<!-- signature addresses read from the dump file 2026-10-08 (each signature scanned over .text) -->
<!-- sources: cw-mod client/hooks/hook.hpp, hook.cpp, hook_types.hpp, client/hooks/impl/game/RtlDispatchException.cpp, client/game/game.cpp, game_internal.hpp, anchors.cpp, client/memory/scanned_result.hpp, .claude/skills/bocw-reverse-engineering/SKILL.md (section 7) @ 36b1f18 + working tree, 2026-10-08 -->

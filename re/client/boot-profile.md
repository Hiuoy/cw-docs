# The boot profile

> The game decides which menus exist from its network mode while it starts. This page gives the word that holds that mode, the calls that write it, and the order the client sets things in. **Status:** Done, with one open point found while writing this page.

## In short

- One packed word, `g_sessionModePacked`, holds the game mode, the network mode and the match type.
- The lobby keeps a **second** network mode of its own. Setting the lobby's mode sets the session's too.
- The menus are built from the network mode **at boot**. Changing it later adds no menus, which is why `"mode"` is a setting and not a button.
- `nodw` is written twice on an online boot: true early, so a sign-in watchdog never runs, then false, so the login starts.

## The session word

| Bits | Field | Values | Written by |
|---|---|---|---|
| 0 to 3 | gameMode | 0 zm, 1 mp, 2 cp, 3 wz. 4 reads as "none". | `Com_SessionMode_SetGameMode` |
| 4 to 7 | networkMode | 0 offline, 1 LAN, 2 online, 3 lobby mode unknown | `Com_SessionMode_SetNetworkMode` |
| 12 to 15 | matchType | 1 = custom. Every LAN lobby runs 1. | `Com_SessionMode_SetMatchType` |

A Zombies lobby on an offline or LAN boot reads `0x1010`.

The three setters sit one after another and have the same shape. The network one, whole:

```nasm
mov  eax, [g_sessionModePacked]
shl  ecx, 4
xor  ecx, eax
and  ecx, 0F0h
xor  eax, ecx          ; eax = word with bits 4-7 replaced
mov  [g_sessionModePacked], eax
ret
```

## The lobby's own mode

| Value | Name |
|---|---|
| 0 | UNKNOWN |
| 1 | LAN (also called LOCAL) |
| 2 | LIVE |

`LobbyBase_SetNetworkMode` does three things:

```text
g_lobbyNetworkMode = mode
LobbyRoot_SetNetworkModeModel(mode)                  ; the copy the menus read
Com_SessionMode_SetNetworkMode(map(mode))            ; a tail jump
map: 1 -> 1, 2 -> 2, anything else -> 3
```

- With the lobby left at UNKNOWN, the mode tiles stay padlocked.
- LAN hides online-only screens on purpose: feature tests ask `LobbyBase_GetNetworkMode() != 1`.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `Com_SessionMode_SetNetworkMode` | 0xC1BC630 | 0x7FF728D7C630 | `void (int mode)` | Writes bits 4 to 7 |
| `Com_SessionMode_SetGameMode` | 0xC1BC610 | 0x7FF728D7C610 | `void (int mode)` | Writes bits 0 to 3 |
| `Com_SessionMode_SetMatchType` | 0xC1BC5F0 | 0x7FF728D7C5F0 | `void (int type)` | Writes bits 12 to 15 |
| `Com_SessionMode_GetGameMode` | 0xC1BC100 | 0x7FF728D7C100 | `int ()` | Bits 0 to 3 |
| `Com_SessionMode_GetNetworkMode` | 0xC1BC280 | 0x7FF728D7C280 | `int ()` | Bits 4 to 7 |
| `Com_SessionMode_IsOnline` | 0xC1BC4B0 | 0x7FF728D7C4B0 | `bool ()` | `(word & 0xF0) == 0x20` |
| `LobbyBase_SetNetworkMode` | 0xAF59B60 | 0x7FF727B19B60 | `void (int lobbyMode)` | See above |
| `LobbyBase_GetNetworkMode` | 0xAF59A40 | 0x7FF727B19A40 | `int ()` | Returns `g_lobbyNetworkMode` |
| `LobbyBase_NetworkModeToSessionNetworkMode` | 0xB5A66F0 | 0x7FF7281666F0 | `int (int lobbyMode)` | The map |
| `LobbyRoot_SetNetworkModeModel` | 0xB1EF360 | 0x7FF727DAF360 | `u64 (int mode)` | The menus' copy |
| `LobbyUI_SetTargetMenuAndNotify` | 0xB1EF430 | 0x7FF727DAF430 | `(int menu, bool)` | Tells the lobby UI which menu it is on |
| `g_sessionModePacked` | 0x18A5C7F8 | 0x7FF73561C7F8 | u32 | The word |
| `g_lobbyNetworkMode` | 0x157EF2A8 | 0x7FF7323AF2A8 | int | The lobby's mode |

## What cw-mod does

Two inputs, both read once in the `Pointers` constructor: `"mode"` in [cw-mod.json](/guide/settings.md), and whether the local backend's public key is present.

**Step 1, before the menus are built** (`Boot::ApplyEarly`, through `Pointers::SetMode`):

| `"mode"` | Lobby mode set | Menu jump | Online flags of the mod |
|---|---|---|---|
| `offline` | LAN | To menu 10, the LAN director | Off |
| `lan` | LAN | To menu 10 | Off |
| `lanlobby` | LAN | To menu 10 | On |
| `online` | LIVE | None with the backend and `"start_screen"` on. Else to menu 10. | On |

- The jump to menu 10 skips the title screen. The title screen's start step is the only thing that creates the **party**, and without a party the director's "am I the leader" test is false and the mode tiles lock. So an online boot with the backend keeps the title screen.
- "Online flags" are the mod's own switches: they arm the handling of Battle.net errors and the online-only work in the tick.
- On an online profile, `nodw` is set **true** here.

**Step 2, when the script system is up** (`Boot::ApplyAfterScriptInit`):

| Profile | Backend | `nodw` | Also |
|---|---|---|---|
| Online | Yes | false | The login dials the local backend |
| Online | No | stays true | |
| Offline or LAN | Yes | false | The login dials the local backend |
| Offline or LAN | No | true | `CL_Disconnect(0, false, "")` |

On this build `nodw` defaults to true.

## Why nodw is written twice

`LiveFirstParty_Frame` runs a watchdog, `LiveUser_ForceSignOutAndFatal`: on an online session with no Battle.net sign-in it signs the player out and raises a fatal error (the `BLZBNTBGS` wall). The whole frame is skipped while `nodw` is true.

- `nodw = true` set after the script system came up measured about **6 seconds too late**: the watchdog had already fired. So it is set in the constructor.
- But the login driver's first state is `if (Dvar_GetBool(nodw)) return;`. Left true, an online boot never dials the backend. So it goes back to false once the menus are built and the watchdog's window has passed.

See [Errors](/re/engine/errors.md) for the full story of that wall.

## Limits and open points

- **Open, found 2026-10-08.** `Pointers::SetMode` also calls a second setter with the number 0, 1 or 2, through a pointer the client names `Com_SessionMode_SetNetworkMode`. That pointer is bound by a byte signature, and in the dump the signature matches `Com_SessionMode_SetGameMode`, the setter of **bits 0 to 3** (RVA 0xC1BC610), not the network setter (RVA 0xC1BC630). The log's `(Scanner) Found 'Com_SessionMode_SetNetworkMode' ...` line shows the offset a run bound. What follows from the bytes:
  - The network bits are written only by `LobbyBase_SetNetworkMode`. So `lanlobby` leaves the engine's network mode at LAN, like `lan`, and differs from it only by the mod's own online flags.
  - That call writes 0, 1 or 2 into the game-mode bits at boot. A Zombies lobby reads 0 there later, so the game writes it again.
  - The overlay's "pin online mode" switch and the join-by-descriptor path use the same pointer.
- The two byte flags `SetMode` sets to 1 come from the t9-mod base and are not named.

## How we found it

- The first "online mode" set only the session word. It half-applied: the lobby still said LAN.
- A sign-in error ended every online boot. Hooking the reporters did not help; reading forwards from the per-frame function found the watchdog and its `nodw` gate.
- The claim that failed its check is the open point above: the bytes of each setter were read from the dump, the signature was run over the dump, and the IDB names the function it matches `Com_SessionMode_SetGameMode`.

## See also

- [Running the game](/guide/running.md): the modes from the player's side
- [Errors](/re/engine/errors.md), [Dvars](/re/engine/dvars.md)
- [The client](/re/client/overview.md)

<!-- checked against the dump file 2026-10-08: the bytes of the three setters, the three getters, LobbyBase_SetNetworkMode and its map; the client's signature for Com_SessionMode_SetNetworkMode ("8B 05 ? ? ? ? 8B D0 33 D1 83 E2 0F 33 C2 89 05 ? ? ? ? C3") has one match in .text, at RVA 0xC1BC610 -->
<!-- sources: cw-mod client/game/boot_profile.hpp, boot_profile.cpp, game.cpp (SetMode, the signatures), session.cpp (OnlineMode), join.cpp, dump_anchors.hpp (BLZBNTBGS notes), docs/fork-findings.md (section 1), .claude/skills/bocw-reverse-engineering/SKILL.md (section 9) @ 36b1f18 + working tree, 2026-10-08 -->

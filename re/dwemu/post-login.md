# After login

> "Login Complete" was not the end. The game then crashed, dropped to offline, sat on a "connecting" overlay, locked its mode tiles, and failed to start a match. This page goes through each wall. None of them needed a server reply. **Status:** Done. An online Zombies match on 2026-09-24, two PCs on 2026-09-29.

## In short

- Studio auth skips Battle.net on purpose. Much of the engine still asks Battle.net questions afterwards, and each one needed its own answer.
- The central question is **first-party presence**: one predicate with about 30 callers. It gets three different answers depending on who asks.
- The online menus wait for a checklist of 25 bits. Five can never be set here. They are waived, for the menus only.
- The padlocks on the mode tiles were never about ownership. They meant "you have no party".

## The walls, in the order they were met

| # | What the player saw | Cause | Fix |
|---|---|---|---|
| 1 | A crash one second after "Login Complete" | A read through the first-party **session**, which studio auth never creates | `FirstParty_GetLocalUserIndex` answers 0 when the session is null |
| 2 | "Boy 501 Gothic Missile", back to offline | The connect handler promotes the user to "signed in online", then asks for a drop to offline | The drop is declined. See [Errors](/re/engine/errors.md). |
| 3 | Nothing: no request after login | Every per-user online tick is behind presence | The presence detour |
| 4 | A "connecting to online services" overlay, flashing | The 25-bit checklist, then the local-files check | The waiver, and [default save data](/re/engine/playerdata.md) for every version |
| 5 | "You don't own the game" on the tiles | The trial check reads a Battle.net license list | `LiveUser_IsTrial` answers "not a trial" on a backend start |
| 6 | Padlocked tiles; a click only plays a sound | No party: the start jumped past the step that creates it | Keep the title screen. See [The boot profile](/re/client/boot-profile.md). |
| 7 | No modes or maps in the menu | No playlist | [Local playlists](/re/dwemu/publisher-data.md) |
| 8 | "Failed to host lobby" after 12.5 seconds | Start went to dedicated-server matchmaking | One dvar forced false |
| 9 | A crash at "Launching game" | A missing Lua chunk, then a null Battle.net account | Skip the chunk; deny presence to the account pickers |

## Wall 1: the null session

`FirstParty_GetSession_MayBeNull` is five bytes: return `manager + 24`. Nothing on the studio-auth path fills that field. The static count said 15 call sites dereference the result unchecked.

The measured count was **one**. A census detour handed back a zeroed stand-in and logged each caller: one site, once. It wanted `session + 0xD0`, the local user index, so 0 is the correct answer on a PC with one player. No fake object is kept in the process.

## Wall 3: presence

`LiveUser_FirstPartyPresenceOk` asks "is a Battle.net user signed in and present". On these starts the true answer is always false. The detour decides by **return address**:

| Caller | Answer | Why |
|---|---|---|
| The login driver | True, always | Otherwise it parks in its first state and never dials |
| Identity setup | The real false | With true it reads the player's name from the Battle.net manager, which was never signed in |
| The two account-id pickers | The real false | With true they ask a null account object. This was the launch crash of wall 9. |
| Everyone else | True, once Demonware login is complete: login state 4 and sign-in state 2 | That is exactly the state a retail client is in when presence holds |

"Everyone else" includes `LiveUser_IsOnlineReady`, which is `presence && signinState == 2 && loginState == 4 && connected`, and gates every per-user online subsystem. With it answered, the client sent its first post-login requests in the same second.

- The widened answer is given only while the Battle.net watchdog is neutralised: a true answer makes its branch reachable.
- Each overridden call site is logged once, as a `(Presence)` line. If a newly reached path crashes, the last line names it.

## Wall 4: the checklist

Lua opens the online menu only when `Engine.IsDemonwareFetchingDone` and `Engine.AreLocalFilesReady` are both true. The first ends in `DwFetch_GetStatus`, which sets one bit per ready subsystem and needs all of `0x17337FA`. The engine prints the same mask as 25 letters in its connection-info text, `A` for bit 0, `-` for a missing one.

| Bit | Letter | Set when | Here |
|---|---|---|---|
| 0x2 | B | Presence, signed in online | Set |
| 0x8 | D | The network session's launch state is 8 | Set |
| 0x10 | E | `LiveUser_IsOnlineReady` | Set |
| 0x20 | F | The publisher file list is loaded | Set |
| 0x40 | G | The `core_ffotd` content slot is in the publisher file list | **Never** |
| 0x80, 0x200 | H, J | Content slots 0 and 1 are loaded | Set by the client |
| 0x100 | I | Publisher variables fetched | Set |
| 0x400 | K | The online save maps are ready | Set |
| 0x2000 | N | Dedicated-server ping data arrived | **Never** |
| 0x20000 | R | The marketplace inventory loaded | **Never** |
| 0x400000 | W | A relay is bound | **Never** |
| 0x1000000 | Y | The in-game store's file is fetched | **Never** |

Measured on the first start with the transcript: the mask settled at `0x3D1FBF`, everything but those five. All five are public matchmaking or commerce.

`DwFetch_IsDone` gets a detour that answers true when the **only** missing bits are those five, and only to the Lua native (by return address). The engine's own callers, such as the store, keep the truth. `"lobby_waiver": false` turns it off.

The marketplace cannot hold the checklist up by itself: while its sync is unfinished, the required mask gains a bit that means "sync not finished".

## Wall 6: the padlock

The tile's lock state in Lua is `not privateClient.isHost`. The party is created by one step only: from the title screen to the online menu. The client's start-up, inherited from the project's base, jumped straight to the menu. No step, no party, locked tiles.

Keeping the title screen exposed a Battle.net error dialog there, fixed in the same pass, and then walls 4 and 7.

## Walls 8 and 9: starting a match

| Wall | Cause | Fix |
|---|---|---|
| Start | The Zombies Start handler in Lua picks dedicated-server matchmaking while one bool dvar is true. The executable registers it true, and nothing native reads it. | The client sets it false every frame on a backend start. Start then opens a lobby hosted on this PC. |
| The missing chunk | With both content slots marked loaded, the UI start-up runs `ui/ffotd_tu34.lua`, whose zone never loads. A missing chunk is a [hard exit](/re/engine/errors.md). | A detour on `LUI_RunFile` skips that one name |
| The account id | With presence true, the launch asked the Battle.net account for an id | Presence is denied inside the two pickers, so they take the Demonware id |

## Two PCs

| Problem | Fix |
|---|---|
| Every PC's backend gave user id 1, so a join to the host was a join to oneself | `"xuid"` in [cw-mod.json](/guide/settings.md), carried in the login token into the ticket |
| Online, the engine gives this PC's peer address a public part (preset, or found by STUN). A peer behind another public address then needs Demonware's NAT traversal or relay, and the backend has neither. | A detour on `bdCommonAddr_Ctor` builds the LAN form instead: no public address, NAT type "open". Peers use each other's local addresses. |

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `LiveUser_FirstPartyPresenceOk` | 0xCAF79B0 | 0x7FF7296B79B0 | `bool ()` | The presence question |
| `LiveUser_IsOnlineReady` | 0x96ECD00 | 0x7FF7262ACD00 | | Gates the online subsystems |
| `LiveUser_UpdateSigninState` | 0xCB60390 | 0x7FF729720390 | | Runs those subsystems per frame |
| `LiveUser_OnDwConnected` | 0xCB62670 | 0x7FF729722670 | | Runs on login state 4 |
| `FirstParty_GetSession` | 0xCC1F050 | 0x7FF7297DF050 | `void* (void* mgr)` | Returns `mgr + 24` |
| `FirstParty_GetLocalUserIndex` | 0xCC19EE0 | 0x7FF7297D9EE0 | `u32 ()` | Reads `session + 0xD0` |
| `DwFetch_GetStatus` | 0x96E4BA0 | 0x7FF7262A4BA0 | `u8 (u32 controller, u32* got, void* scratch)` | The checklist |
| `DwFetch_IsDone` | 0x96ECBE0 | 0x7FF7262ACBE0 | `u8 (u32 controller)` | Its wrapper, where the waiver sits |
| `LiveUser_IsTrial` | 0xB591A00 | 0x7FF728151A00 | `u8 ()` | Not a trial under `nodw`; else needs a license |
| `LiveUser_GetAccountId_cand` | 0xCAEB340 | 0x7FF7296AB340 | | One of the two pickers |
| `bdCommonAddr_Ctor` | 0xD1773D0 | 0x7FF729D373D0 | `void* (void* self, void* localAddrs, const void* publicAddr, u32 natType, i32)` | Builds this PC's peer address |

The user object: sign-in state at `+5764` (0 none, 1 local, 2 online), login state at `+5768` (4 connected).

## Limits

- Two PCs were tested on one home network. Different networks, over a VPN, are not tested since these fixes.
- Each fix answers one question the engine asks. A menu or mode not yet opened may ask a new one.

## See also

- [The service router](/re/dwemu/router.md): the requests that started at wall 3
- [Storage and entitlements](/re/dwemu/storage-entitlements.md): the three bits that stay unset
- [Online mode, the guide](/guide/play/online.md)

<!-- sources: cw-mod docs/backend-roadmap.md (B1, B6, B7, B8), docs/fork-findings.md, client/hooks/impl/game/LiveUser_FirstPartyPresenceOk.cpp, client/game/dump_anchors.hpp (first-party session, presence, DwFetch, IsTrial, padlock notes, peer addressing), client/game/session.cpp, client/hooks/hook.hpp @ 36b1f18 + working tree, 2026-10-08 -->

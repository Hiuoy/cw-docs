# Publisher data and playlists

> The list of modes and maps the online menus show is not in the game's main files. It is "publisher data", fetched from Demonware into a folder on the PC. This page covers how the game fetches and checks it, and how cw-mod loads the player's own copy with no server at all. **Status:** Done, in game 2026-09-24: "Loaded 177 as preferred playlist".

## In short

- Publisher files are small zones with names like `core_playlists_tu35_100_<build id>.ff`. The game downloads them once and keeps them.
- Without a playlist the online menu has no modes or maps.
- The engine loads a publisher zone only after a list from Demonware and an MD5 check of every file. Offline it never gets that far.
- cw-mod loads the playlist zones from `<game>\cw-mod\lpc\` itself, the way the engine would, under their **own names**.
- The files are the game publisher's data. They stay on the player's PC and are never part of cw-mod. See [Legal](/legal.md).

## How the engine does it

```text
Lpc_SyncFrame:
    ask the object store for category "tu<N>_<build id>"        (through the lobby, as tunnelled HTTP)
    on a good list:  Lpc_WriteManifest      write ".manifest" from the list
                     MD5 every listed file in the local folder
                     all match -> manifest loaded, the folder becomes a search path
    on a bad list:   Lpc_OnListFailed       try again in 15 seconds

OnlineContent_LoaderFrame:
    needs publisher variables, and refuses in the offline menus
    slot 0: load zone core_playlists_...  (and its language twin), then Playlist_LoadFromAssets
    slot 1: load zone core_ffotd_...      then reinitialise save data, game types and Lua
```

Two slots, each a zone flag and a callback:

| Slot | Zone flag | Content | Callback |
|---|---|---|---|
| 0 | 0x2000 | Playlists | Loads the playlist asset (type `0x8F`), applies dvar overrides |
| 1 | 0x800 | The "ffotd" daily fixes | Reinitialises several systems |

Slot state: 0 idle, 1 loading, 2 loaded.

## The list reply

Each object in the list needs these keys. A string must be shorter than the client's buffer.

| Key | Limit | Note |
|---|---|---|
| `name` | 64 | The file name |
| `checksum` | 32 | Base64 MD5. Becomes the manifest's hash. |
| `objectVersion` | 32 | |
| `contentLength` | number | |
| `created`, `modified`, `expiresOn` | number, or a numeric string | |
| `acl` | | `public` or `private` |
| `context` | 15 | |
| `owner` | 29 | |
| `category` | 64, or null | |
| `contentURL` | 511, optional | Where to download on an MD5 mismatch |

And beside the objects, `nextPageToken`: required, null for the last page. See [The service router](/re/dwemu/router.md) for the envelope.

## Three traps

| Trap | What happened | Rule |
|---|---|---|
| **The name is signed** | A zone's RSA signature covers the name it is loaded under. The files at hand were from title update 35; this executable is title update 34 and builds names with `tu34`. Renamed to match, they failed the check. | Never rename a signed zone. Load it under the name it shipped with. |
| **A failed signature is not an error** | The engine answers by corrupting its asset free list on purpose. The **next** zone to allocate dies with "Uniform 58 Guerrilla Boa". | That error means "a signature failed earlier", not "out of memory" |
| **The other parser** | A detour on the list parser never fired. The list request uses a second parser with the same job. | Hook what runs. The transcript named it. |

The build's content id is inside the file names and in the zone header, and the engine compares it. The update 35 files carry this executable's content id, which is why they load at all.

## What the server does

By default the server answers the list request with an **empty list**. The engine then writes a manifest with no entries and reports "manifest loaded", which sets its bit in the [checklist](/re/dwemu/post-login.md) without loading a single file. Serving the real list was tried first and met the traps above.

Two environment variables bring the old behaviour back for tests: `CWMOD_LPC_FILES=1` lists the files of the publisher folder, and `CWMOD_LPC_EXCLUDE` leaves names out (default: the `ffotd` ones).

## What the client does

`client/game/local_lpc.cpp`, once per start, from the game-thread tick:

| Step | Detail |
|---|---|
| 1. Find | `<game>\cw-mod\lpc\[<lang>_]core_playlists_tu<N>_100_<build id>.ff`, with this executable's build id |
| 2. Mount | `FS_AddSearchPath(folder, 300, 2, 0)`: the same call, priority and device the engine uses for its verified folder |
| 3. Wait | Until the asset database is idle and no level is loading |
| 4. Load | `DB_LoadXAssets` and `DB_SyncXAssets` for the base zone (flag 0x2000) and its language twin (flag 0x2000 with 0x8000), under the files' own names |
| 5. Finish | When the zones report loaded, call the slot 0 callback |

- Slot 1 is left alone. Its callback reinitialises save data and Lua.
- On an online start with the backend, the client also marks both content slots as loaded. The engine's loader then has nothing to do, and a later mode switch, which waits for both slots, can proceed.
- While the two zones load, a detour on `DB_AllocXAssetEntry` counts allocations per asset type. If a check is about to fail, it logs which, and names a failed signature when the free list's head is outside its array.

Runs on offline, LAN and online-with-backend starts. `"local_playlists": false` turns it off.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `Lpc_SyncFrame` | 0xAF76860 | 0x7FF727B36860 | | Asks for the list, checks the files |
| `Lpc_WriteManifest` | 0xAF760A0 | 0x7FF727B360A0 | | Writes `.manifest` from a good list |
| `Lpc_OnListFailed` | 0xAF76070 | 0x7FF727B36070 | | Arms the 15-second retry |
| `PublisherObjectsResource_Parse` | 0xD1CB130 | 0x7FF729D8B130 | `u8 (void* resource, void* response)` | The parser the list really uses |
| `ObjectMetadata_ParseJson` | 0xD1B0BD0 | 0x7FF729D70BD0 | `u8 (void* metadata, void* json, u32 ownerType)` | One object's keys |
| `OnlineContent_LoadSlotZones` | 0xA2CD740 | 0x7FF726E8D740 | | The engine's own slot load |
| `OnlineContent_OnPlaylistsLoaded` | 0xA2CA570 | 0x7FF726E8A570 | | The slot 0 callback |
| `FS_AddSearchPath` | 0xCA86DC0 | 0x7FF729646DC0 | `void (const char* path, int priority, int device, u64)` | Adds and indexes a folder |
| `DB_LoadXAssets` | 0xB304700 | 0x7FF727EC4700 | `void (XZoneInfo* zones, u32 count, int freeFlags)` | Queues zones |
| `DB_SyncXAssets` | 0xB3050D0 | 0x7FF727EC50D0 | | Blocks until they are in |
| `Com_GetTuVersion` | 0xCA2FA70 | 0x7FF7295EFA70 | `int ()` | 34 on this build |
| `Lpc_GetBuildContentIdString` | 0xC6EDE60 | 0x7FF7292ADE60 | `const char* ()` | The 16 hex digits in the file names |
| `g_onlineContentSlots` | 0x1343AD80 | 0x7FF72FFFAD80 | int[2] | Slot states |
| `g_playlistValid` | 0x1348348C | 0x7FF73004348C | u8 | Set by the playlist loader only |

## How we found it

- The first server reply was answered twice, 15 seconds apart, and no manifest appeared. Five read-only detours along the path named the failing step: the missing `nextPageToken`.
- With the list accepted, the game dropped one second later inside the asset allocator. Twice. The cause was the rename, found by reading what the signature covers.
- Offline the playlist was missing for a different reason: the loader that owns it never runs there.

## Limits

- The player must already have the publisher files: the ones their own game downloaded into its publisher folder. cw-mod cannot supply them.
- Only playlists. The daily-fix zone is not loaded, and its checklist bit is waived.
- A download on an MD5 mismatch is not served.

## See also

- [Online mode, the guide](/guide/play/online.md): where the files go
- [After login](/re/dwemu/post-login.md): the checklist bits these slots feed
- [Errors](/re/engine/errors.md): "Uniform 58 Guerrilla Boa"

<!-- sources: cw-mod client/game/local_lpc.hpp, local_lpc.cpp, client/game/dump_anchors.hpp (B3 notes, LPC playlists outside LIVE), client/game/session.cpp (content slots), tools/dwserver/lobby_router.py (the object list), docs/backend-roadmap.md (B3) @ 36b1f18 + working tree, 2026-10-08 -->

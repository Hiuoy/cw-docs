# PlayerData: where saves live

> Every saved thing (levels, stats, loadouts, settings) is a "data map" with a storage location. The maps that hold progression are stored on Demonware, so without it they never load. This page gives the layout and the three-part fix. **Status:** Done. Online boots since 2026-07-29; offline and LAN boots with progression since 2026-09-23.

## In short

- A data map is a DDL buffer described by a **def**. The def names its storage: local disk, Demonware user storage, memory and so on.
- 18 of the 32 defs are on Demonware user storage (`dwuser`). With no Demonware their reads are never even queued.
- A menu that reads such a map gets `nil` and raises. This was the first wall of the online menus, and the reason nothing was saved offline.
- The fix: change those defs to local disk at the last moment that still counts, fill them with defaults, and undo the engine's veto of the failed reads.

## Structures

**The def**, found through `g_playerDataDefsById` (data map ids 1 to 45):

| Offset | Type | Meaning |
|---|---|---|
| +16 | u64 | Hash of the DDL asset's name |
| +48 | int | Default version, used when a caller passes -1 |
| +56 | int | Data map id |
| +60 | int | Scope: 1 means controller 0 only |
| **+64** | int | **Storage location** |
| +68 | bool | Persist this map. 0 means never written. |

**Storage locations**, rows of 8,272 bytes in `g_playerDataStorageBackends`:

| Id | Name | |
|---|---|---|
| 0 | hdd | Local `.cgp` files |
| 1 | dwuser | Demonware user storage. Not available under `nodw`. |
| 2 | dwclan | |
| 3 | memory | |
| 4 | fastfile | Read-only defaults from a zone |

A backend row is a 48-byte header and four queues of 2,056 bytes: `queue = backend + 2056 * (kind + 2 * controller)`, with 256 pointers from `+48` and the count at `+2096`. **Kind 0 is read, kind 1 is write.**

**The store**, `g_playerDataStore`, 86,040 bytes per controller:

| Offset | Meaning |
|---|---|
| +0 | User key |
| +8 | One "submitted" byte per storage location (5) |
| +16 | 256 entries of 336 bytes |
| +86,032 | Entry count |

**An entry:**

| Offset | Type | Meaning |
|---|---|---|
| +0 | int | Data map id |
| +8 | pointer | Its def |
| +28 | int | Buffer size |
| +32 | int | Version |
| +40 | pointer | The DDL bytes |
| +56 | | A DDL instance: buffer, size, root. This is what `PlayerData_GetBuffer` returns. |
| **+120** | int | **Settled.** 1 means readable. |
| +132, +136 | u32 | Read retry: attempt count, next time |

## How loading works

```text
PlayerData_ControllerStorageTick(controller), every frame:
    for each location 0..4:
        if not submitted[location] and the location is available:
            queue a read for every entry whose def says this location
            submitted[location] = 1          <- latches
        run the queued reads and writes
```

- With `nodw`, `dwuser` is never available. Location 1 is skipped: nothing is queued, nothing fails, nothing is retried.
- Reads run on a job thread. Each one ends in `PlayerData_OnStorageOpComplete`, which sets `entry+120`. So the set of readable maps grows over seconds during the start.
- On a **failed** read the engine still sets `+120 = 1`: "settled, keep what is in the buffer". Then a per-map callback may veto that, set it back to 0, and arm a retry with a growing delay.

`PlayerData_IsBufferReady` answers false for six different reasons. Print the cause, not only the verdict:

1. The system is not initialised.
2. The entry count.
3. No entry has this data map id **and** version. Only -1 means the default version.
4. The def's scope excludes this controller.
5. The block's XUID.
6. `entry+120` is 0.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `PlayerData_Init` | 0xAA017C0 | 0x7FF7275C17C0 | | Builds the defs and entries. Runs before the mod's detours exist. |
| `PlayerData_ControllerStorageTick` | 0xAA01E90 | 0x7FF7275C1E90 | `char (uint controller)` | The load driver |
| `PlayerData_OnStorageOpComplete` | 0xAA01920 | 0x7FF7275C1920 | `void* (uint controller, int opKind, uint resultCode, uint* entry)` | Sets `entry+120`. Job thread. |
| `PlayerData_ResetBufferToDefaults` | 0xAA02250 | 0x7FF7275C2250 | `i64 (uint controller, uint dataMapId, int version)` | Fills a buffer from the DDL's defaults, then sets `+120` |
| `PlayerData_IsBufferReady` | 0xAA01620 | 0x7FF7275C1620 | `bool (int controller, uint dataMapId, int version)` | The six-reason gate |
| `PlayerData_GetBuffer` | 0xAA00DF0 | 0x7FF7275C0DF0 | `void* (i64 controller, uint dataMapId, int version)` | Returns the entry's DDL instance |
| `PlayerData_AreLocalFilesReady` | 0x96E31D0 | 0x7FF7262A31D0 | | Every version of every local map settled. Behind the menus' "Connecting". |
| `PlayerData_ResetControllerStore` | 0xA9FF690 | 0x7FF7275BF690 | | Clears a controller's store |
| `PlayerDataStorage_EnqueueOp` | 0xB5B3EB0 | 0x7FF728173EB0 | | Adds to a queue. Refuses at 256. |
| `PlayerDataStorage_DwUser_IsAvailable` | 0xB83FD20 | 0x7FF7283FFD20 | | False under `nodw` |
| `g_playerDataDefsById` | 0x137BBA60 | 0x7FF73037BA60 | pointer per id | The defs |
| `g_playerDataStore` | 0x13791A10 | 0x7FF730351A10 | | The store |
| `g_playerDataStorageBackends` | 0xE22F800 | 0x7FF72ADEF800 | | The five locations |
| `g_playerDataMapCallbacks` | 0x137BBBD0 | 0x7FF73037BBD0 | | The per-map veto callbacks |

## What cw-mod does

| # | Step | Where | Detail |
|---|---|---|---|
| 1 | The redirect | First call of `PlayerData_ControllerStorageTick`, before the original | Every def with location 1 gets location 0. The same 4-byte store the engine performs in `PlayerData_Init` when its "force local storage" dvar is set. |
| 2 | The defaults | The same call | `PlayerData_ResetBufferToDefaults` for **every version** of every redirected map |
| 3 | The veto | `PlayerData_OnStorageOpComplete` | For a redirected map whose read failed and was vetoed: `+120` back to 1, retry state cleared |

- **Why the tick.** It is self-timing: it is the code that submits locations, so its first call is before location 0 went out. Anything later is too late for good, because `submitted[]` latches.
- **Why defaults.** The redirected reads fail: the data only ever lived on Demonware. A failed read leaves a zeroed buffer, which is not a valid DDL instance.
- **Why every version.** Two maps have 20 and 10 versions. Seeding only the default left 28 entries unsettled, and the menus' "local files ready" test stayed false.
- Step 3 also runs on the job thread, so it must stay thread-safe and never call Lua.

Scope: online boots, and offline and LAN boots while [progression](/re/engine/progression.md) is on. Stock maps keep stock behaviour.

## How we found it

- The online director menu raised: a DDL native returned `nil` for data map 4, and `IsBufferReady` said cause 6.
- A transcript of every completion showed 50 reads, all local, all fine, and map 4 **absent**. Not failed: never attempted.
- The first fix hooked the init function and never fired: init had already run.
- The second fix worked, and 14 reads failed. The instrument said "`+120` unchanged at 0". Inside the call it went 0, 1, 0: set, then vetoed. Sampling before and after cannot see that.
- Return codes lied: the load submit returns 1 when nothing matched, and the queue runner returns 0 for "all fine" and for "empty". The queue's own count is the honest witness.

## Limits and open points

- The redirect is marked temporary in the code: it exists because the local backend does not serve user storage. With that, `dwuser` would be available for real.
- The dvar the engine uses for the same rewrite could not be identified with certainty, so it is not used.

## See also

- [Progression](/re/engine/progression.md): what is saved and when
- [Saves and progression, the guide](/guide/play/progression.md)
- [Hooking](/re/client/hooking.md): the self-timing seam

<!-- sources: cw-mod client/hooks/impl/game/PlayerData_ControllerStorageTick.cpp, PlayerData_OnStorageOpComplete.cpp, client/game/game.hpp (kPd* layout), dump_anchors.hpp (PlayerData notes), client/hooks/hook.hpp, docs/fork-findings.md (section 3), .claude/skills/bocw-reverse-engineering/SKILL.md (section 9) @ 36b1f18 + working tree, 2026-10-08 -->

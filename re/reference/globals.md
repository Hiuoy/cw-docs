# Globals index

> Every named address this project uses or has written down: 110 globals, tables and other data addresses. The page is generated, so no address here was typed by hand.

- **RVA** is the offset from the image base. It is the same in every dump of build 1.34.0.15931218.
- **IDA address** is the address in our IDB, whose image base is `0x7FF71CBC0000`. Your own dump has another base: add the RVA to it.
- A name that ends in `_cand` is inferred, not proven.
- The first table of a group lists what the client anchors in `client/game/dump_anchors.hpp`. "Named in the notes" lists names written next to an address in the project's notes and code comments.
- How to read and check an address: [Address and byte math](/re/method/address-math.md).

## Demonware, login and first party

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `dvar_liveConnectMode` | 0x17160100 | 0x7FF733D20100 | The state-1 connect path in LiveUser_LoginDriver_Tick only calls Dw_GetOrCreateConnection443 when ALL of these hold: g_liveUserSystemActive!=0, nodw==false, live_connect_mode==1, ctrl==0, g_liveUserLoginAllowed!=0, and ... |
| `g_bdAddrEmpty` | 0x1A97F5E0 | 0x7FF73753F5E0 | g_bdAddrEmpty is the engine's own empty bdAddr, the one bdAddr_IsValid 0x7FF729E04330 compares with. |
| `g_bnetEverSignedInLatch` | 0x1A5FF272 | 0x7FF7371BF272 | g_bnetEverSignedInLatch - read-only here, purely so the diagnostic can say which reporter could have fired. |
| `g_dwAuthSigPubKey_DER` | 0xD9781B0 | 0x7FF72A5381B0 | RVA 0xD9781B0 |
| `g_dwFetchCtrl20000` | 0x16FB9520 | 0x7FF733B79520 | 801056/ctrl: +944 byte, +900 int == 3 |
| `g_dwFetchFlag1000` | 0x11C3A64F | 0x7FF72E7FA64F | byte, bit 0x1000 |
| `g_dwFetchFlag200000` | 0x12373444 | 0x7FF72EF33444 | byte (if a dvar &gt;= 2) |
| `g_dwFetchState2000` | 0x15D9357C | 0x7FF73295357C | int &gt;= 4, bit 0x2000 |
| `g_dwFetchState400000` | 0x13C6D838 | 0x7FF73082D838 | int 2..3, bit 0x400000 |
| `g_firstPartyManager` | 0x1A5FF208 | 0x7FF7371BF208 | g_firstPartyManager SLOT (off_7FF7371BF208). |
| `g_firstPartyManagerObj` | 0x1A61A520 | 0x7FF7371DA520 | The first-party manager OBJECT itself (not the pointer slot kDump_g_firstPartyManager above -- that is a different global). |
| `g_inventory` | 0x16FB9520 | 0x7FF733B79520 | 801056 bytes per controller |
| `g_liveUserLoginAllowed` | 0x1A6175D7 | 0x7FF7371D75D7 | g_liveUserLoginAllowed byte (LiveUser_GetLoginAllowedFlag returns it). |
| `g_liveUserObjects` | 0xE203390 | 0x7FF72ADC3390 | LiveUser_GetObject(c) is literally this array indexed by c - the whole function is one load. |
| `g_liveUserSystemActive` | 0xDF2018D | 0x7FF72AAE018D | The master gate for the per-frame LiveUser update loop (LiveUserSystem_Tick, sub_7FF7262ACAA0): if (g_liveUserSystemActive && reentryGuard &lt;= 0) { for c in 0..1 LiveUser_LoginDriver_Tick(c); } If this byte is 0, the login ... |
| `g_lsgHandshakePubKey_DER` | 0xD977330 | 0x7FF72A537330 | RVA 0xD977330 |
| `g_mtxSyncBackoff` | 0xE5B3390 | 0x7FF72B173390 | 36 bytes per controller |
| `g_mtxSyncState` | 0xE5B3420 | 0x7FF72B173420 | int[2]: 0 idle, 1 waiting Bnet token, 2 sync sent, 3 done |
| `g_onlineContentSlots` | 0x1343AD80 | 0x7FF72FFFAD80 | int[2]: 0 idle, 1 loading, 2 loaded |
| `g_onlineContentSlotTable` | 0xD7D5F28 | 0x7FF72A395F28 | {u32 flags, pad, fn} x2: 0x2000 playlists, 0x800 ffotd |
| `g_playlistAsset` | 0x13483470 | 0x7FF730043470 | asset type 0x8F, set by Playlist_LoadFromAssets |
| `g_playlistValid` | 0x1348348C | 0x7FF73004348C | u8 |
| `g_pubVarsState` | 0x174BBAF4 | 0x7FF73407BAF4 | 2 fetching, 3 failed/retry, 4 ready |

## Demonware, login and first party: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `dvar_mtxSyncEnabled` | 0x1A616B18 | 0x7FF7371D6B18 |  |

## Sessions and netcode

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `cl_lobbyLaunchState` | 0x1394A740 | 0x7FF73050A740 |  |
| `g_clientFlags` | 0x101B00E0 | 0x7FF72CD700E0 |  |
| `g_clientJoinCtx` | 0x13870DA0 | 0x7FF730430DA0 |  |
| `g_controllerClientMap` | 0x18A492C4 | 0x7FF7356092C4 |  |
| `g_expectedHostAdr` | 0x13873E98 | 0x7FF730433E98 |  |
| `g_hostLaunchPhase` | 0x1598F5E8 | 0x7FF73254F5E8 | host-launch FSM phase |
| `g_joinResponseCode` | 0x13877710 | 0x7FF730437710 |  |
| `g_lobbyNetworkMode` | 0x157EF2A8 | 0x7FF7323AF2A8 | int, LobbyBase_GetNetworkMode |
| `g_lobbyRootModel_lobbyNetworkMode` | 0x160093F0 | 0x7FF732BC93F0 | u32 model id, 0 until created |
| `g_localClientControllers` | 0x18A492C0 | 0x7FF7356092C0 | 60-byte entries |
| `g_localPlayerCount` | 0x157EF2A8 | 0x7FF7323AF2A8 | Old name. The value is the lobby's network mode: see g_lobbyNetworkMode. |
| `g_netFieldChecksum` | 0x1A322EA4 | 0x7FF736EE2EA4 |  |
| `g_netMsgHandlers` | 0xD7D2110 | 0x7FF72A392110 |  |
| `g_netMsgNames` | 0xE22F4E0 | 0x7FF72ADEF4E0 |  |
| `g_netSessionLaunchState` | 0xE207CA0 | 0x7FF72ADC7CA0 | launch-state enum the pump drives |
| `g_netSessionManager` | 0x1A97F5C8 | 0x7FF73753F5C8 | ptr to NetSession manager (null until session exists) |
| `g_primaryLocalClient` | 0xE36E788 | 0x7FF72AF2E788 | int idx |
| `g_sessionModePacked` | 0x18A5C7F8 | 0x7FF73561C7F8 | The packed session-mode word. gameMode = bits 0-3, networkMode = bits 4-7, matchType = bits 12-15. Read-only here: progression keys off matchType, LAN discovery keys off networkMode == 1, and the two must not be conflated. |
| `g_sessionSlots_type0` | 0x134BABD0 | 0x7FF73007ABD0 | 3 x 237728 |
| `g_sessionSlots_typeN` | 0x13483A50 | 0x7FF730043A50 | 3 x 75216 |
| `g_svClients` | 0x10EB5B00 | 0x7FF72DA75B00 |  |
| `HostLaunchBlock` | 0x1598EAC0 | 0x7FF73254EAC0 | latched StartLaunch param block (0x140 bytes) |
| `pendingJoin_awaiting` | 0x13877720 | 0x7FF730437720 |  |
| `pendingJoin_hostName` | 0x13877750 | 0x7FF730437750 |  |
| `pendingJoin_nonce` | 0x13877724 | 0x7FF730437724 |  |
| `pendingJoin_secId` | 0x1387778C | 0x7FF73043778C |  |
| `pendingJoin_secKey` | 0x13877794 | 0x7FF730437794 |  |
| `pendingJoin_serializedAdr` | 0x138777A5 | 0x7FF7304377A5 |  |
| `pendingJoin_sessionId` | 0x13877748 | 0x7FF730437748 |  |
| `pendingJoin_slot` | 0x13877774 | 0x7FF730437774 |  |
| `pendingJoin_valid` | 0x13877738 | 0x7FF730437738 |  |
| `pendingJoin_xuid` | 0x13877728 | 0x7FF730437728 |  |
| `qportCounter` | 0x10C00AC4 | 0x7FF72D7C0AC4 |  |
| `sv_migrationInProgress` | 0x10AB2950 | 0x7FF72D672950 |  |

## Sessions and netcode: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_svMaxClients` | 0x10EB3780 | 0x7FF72DA73780 | Bound by signature. The live server's player cap, a plain int. |

## LUI and Lua

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `aXhashfuncNoName` | 0xE3ED9B0 | 0x7FF72AFAD9B0 | the non-writing return |
| `g_luiCtx` | 0x139F2F38 | 0x7FF7305B2F38 | A replay of the engine's own `openmenu` console command, Cmd_OpenMenu_f (0x7FF726FC37E0): controller = CL_LocalClientToController(localClient); UI_SetUiActive(localClient, true); ... |
| `g_uiLevelRunning` | 0x10102719 | 0x7FF72CCC2719 | u8 |
| `g_uiModelNodes` | 0x1751C250 | 0x7FF7340DC250 | UI model nodes, 48 B each, indexed by model id: +0 value (i64), +8 type (3 = int). UIModel_SetInt_cand. |

## GSC VM: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_scrInitialized` | 0x139F4826 | 0x7FF7305B4826 | Bound by signature (Scr_Initialized in the client). A byte: the script system is up. |
| `g_serverVmCtx` | 0x11AFBA40 | 0x7FF72E6BBA40 |  |
| `gObjFileInfo` | 0xF6EC9D0 | 0x7FF72C2AC9D0 | Bound by signature. The linked script objects: 800 entries of 24 bytes for each of the two VMs. |
| `gObjFileInfoCount` | 0xF6F5FD0 | 0x7FF72C2B5FD0 | Bound by signature. Two counts, one for each VM. |
| `gVmOpJumpTable` | 0xDE87740 | 0x7FF72AA47740 | Bound by signature. The GSC VM's handler table, one pointer per opcode. |

## PlayerData, stats and progression

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `dvarPtr_ddlCopyIntegrityCheck` | 0x11C3A088 | 0x7FF72E7FA088 |  |
| `g_playerDataDefsById` | 0x137BBA60 | 0x7FF73037BA60 |  |
| `g_playerDataInitialized` | 0x13791A06 | 0x7FF730351A06 | byte, IsBufferReady's first test |
| `g_playerDataMapCallbacks` | 0x137BBBD0 | 0x7FF73037BBD0 | The redirect worked: 66 completions instead of 50, and map 4 finally appears as a real storage=hdd(0) READ. |
| `g_playerDataMapGroups` | 0xE207BB0 | 0x7FF72ADC7BB0 | 10 x 24: +0 dataMapId, +4 mode (1 or 2) |
| `g_playerDataStore` | 0x13791A10 | 0x7FF730351A10 |  |
| `g_statsTransfer` | 0x1126E650 | 0x7FF72DE2E650 | g_statsTransfer: 528 bytes per controller. |
| `g_unlockableItemsByMode` | 0x10CDCB90 | 0x7FF72D89CB90 | Unlockables_GetItemRow (0x7FF724132DD0): table + 409832 * mode + 320 * item, valid when byte +23 has bit 4; the row is entry + 16 and its attachment count is the byte at row + 84. |

## PlayerData, stats and progression: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_playerDataStorageBackends` | 0xE22F800 | 0x7FF72ADEF800 |  |

## AI and navigation

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_aiNav` | 0x10BD1D50 | 0x7FF72D791D50 | -&gt; the nav world Also written as `g_aiNav_cand`. |

## World, collision and rendering

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_rendererGlobals` | 0x198B4930 | 0x7FF736474930 | -&gt; the renderer's globals |
| `g_xmodelMeshIndexBase` | 0x11E4FFB8 | 0x7FF72EA0FFB8 | -&gt; xmodelmesh pool items |

## World, collision and rendering: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_clipMap` | 0x19814060 | 0x7FF7363D4060 |  |
| `g_comWorld_cand` | 0x1A050750 | 0x7FF736C10750 |  |
| `g_streamKeyTypeCallbacks` | 0xE375800 | 0x7FF72AF35800 |  |
| `g_terrainGfx_cand` | 0x17516350 | 0x7FF7340D6350 |  |

## Fastfiles and asset loaders

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_bgCacheNames` | 0x11868C50 | 0x7FF72E428C50 |  |
| `g_bgCacheTables` | 0xDF1B4F0 | 0x7FF72AADB4F0 |  |
| `g_dbReady` | 0x18A59A2B | 0x7FF735619A2B | u8; DB_IsIdle_cand = this && !syncPending |
| `g_dbSyncPending` | 0x16FB7998 | 0x7FF733B77998 | u64 |
| `g_mapPreloadName` | 0x189A23F8 | 0x7FF7355623F8 | char[128] |
| `g_mapPreloadState` | 0x189A22F0 | 0x7FF7355622F0 | i32: 0 idle, 1 parsed, 2 loading, 3 preloaded |
| `g_streamPos` | 0x1A323140 | 0x7FF736EE3140 | u64 |
| `g_streamPosArray` | 0x1A3230D0 | 0x7FF736EE30D0 | u64[13] |
| `g_streamPosIndex` | 0x1A3230C8 | 0x7FF736EE30C8 | i32 |
| `g_streamPosStackIndex` | 0x1A323148 | 0x7FF736EE3148 | i32 |
| `g_xassetEntries` | 0x16415320 | 0x7FF732FD5320 | 16 B each |
| `g_xassetEntryFreeHead` | 0x16415318 | 0x7FF732FD5318 |  |
| `g_xassetEntryUsedBits` | 0x16F6BB20 | 0x7FF733B2BB20 | 23040 u32 |
| `g_xassetPools` | 0x11E50670 | 0x7FF72EA10670 | 32 B {items, u32 size, i32 count, u8 singleton, i32 used, freeHead} |
| `g_zoneInfoRows` | 0x16FAFA7C | 0x7FF733B6FA7C | 76 B {name[64], flags, status} x63 |
| `g_zoneInfos` | 0x16FAFA70 | 0x7FF733B6FA70 | Per loaded zone, 76 B: +0 u32 zone flags (what DB_EnumXAssetsInZones_cand 0x7FF727EC1F00 masks). |
| `g_zoneSigName` | 0x198171A0 | 0x7FF7363D71A0 | char[64]: basename of the zone name being verified |

## Fastfiles and asset loaders: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_defaultAssetNames` | 0xD7C9480 | 0x7FF72A389480 |  |
| `g_xassetTypeNames` | 0xD7C8D90 | 0x7FF72A388D90 |  |

## Dvars

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_dvarAllowServerFlaggedWrites` | 0x18A4D544 | 0x7FF73560D544 | g_dvarAllowServerFlaggedWrites - WHY THE FORCE-RAW-BLOCK-COPY SET SILENTLY DID NOTHING. |
| `p_dvar_svRunning` | 0x10101158 | 0x7FF72CCC1158 | p_dvar_svRunning holds the Dvar*; value block = *(dvar + 16), byte 0. |

## Dvars: named in the notes

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_dvarHashTable` | 0x18A55570 | 0x7FF735615570 | Bound by signature. 1,024 buckets; the index is hash & 0x3FF. |
| `p_dvar_com_maxclients` | 0x10101020 | 0x7FF72CCC1020 | Holds the dvar's pointer. |
| `p_dvar_nodw` | 0x17160108 | 0x7FF733D20108 | Bound by signature. Holds the nodw dvar's pointer. |
| `p_dvar_showOverStack` | 0x11847DF8 | 0x7FF72E407DF8 | Bound by signature. The dvar pointer the client swaps to get its game-thread tick. |

## Common, session mode and boot

| Name | RVA | IDA address | Note |
|---|---|---|---|
| `g_mainThreadId` | 0x18A5A0C0 | 0x7FF73561A0C0 | u64, Sys_IsMainThread compares to it |

<!-- generated by tools/gen_functions.py from cw-mod 36b1f18 (client/game/dump_anchors.hpp, client/game/function_types.hpp, and the names written next to an address in the notes and comments). Do not edit by hand. -->

# Function index

> Every named address this project uses or has written down: 580 functions and other code addresses. The page is generated, so no address here was typed by hand.

- **RVA** is the offset from the image base. It is the same in every dump of build 1.34.0.15931218.
- **IDA address** is the address in our IDB, whose image base is `0x7FF71CBC0000`. Your own dump has another base: add the RVA to it.
- A name that ends in `_cand` is inferred, not proven.
- The first table of a group lists what the client anchors in `client/game/dump_anchors.hpp`. "Named in the notes" lists names written next to an address in the project's notes and code comments.
- How to read and check an address: [Address and byte math](/re/method/address-math.md).

## Errors and termination

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `BnetError_ReportFatalIfSignedIn` | 0xCAF7CF0 | 0x7FF7296B7CF0 | <code class="wrap">void BnetError_ReportFatalIfSignedIn(uintptr ctx, u32* bgsErrorCode)</code> |
| `BnetError_ReportFatalUnguarded` | 0xCAF7C70 | 0x7FF7296B7C70 | <code class="wrap">u64 BnetError_ReportFatalUnguarded(u32 bgsErrorCode)</code> |
| `ErrorQueue_Push` | 0x5789D60 | 0x7FF722349D60 | <code class="wrap">char ErrorQueue_Push(int level, const char* message, char flag)</code><br>Tracing the dialog properly: ErrorQueue_Push(int level, const char* msg, char flag) is the ONE place the "ERROR / EXIT TO DESKTOP" popup comes from. |
| `LuiError_ReportFatal` | 0x5702340 | 0x7FF7222C2340 | <code class="wrap">u64 LuiError_ReportFatal(const char* context, void* luaState)</code><br>LuiError_ReportFatal(const char* context, lua_State* L) - THE reason opening some menu hashes kills the game, and it is not a fault we can catch. |

## Errors and termination: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `BB_Alert` | 0x1B261E0 | 0x7FF71E6E61E0 | <code class="wrap">void BB_Alert(const char* type, const char* msg)</code><br>Bound by signature. In our dump its first five bytes are the mod's own detour: the dump was taken with the hook in place. |
| `Com_Error` | 0x571A030 | 0x7FF7222DA030 |  |
| `Com_NotifyLuiError` | 0xAE782A0 | 0x7FF727A382A0 |  |
| `LuiError_ReportAndDie` | 0x57004C0 | 0x7FF7222C04C0 |  |

## Demonware, login and first party

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `bdCommonAddr_Ctor` | 0xD1773D0 | 0x7FF729D373D0 | <code class="wrap">void* bdCommonAddr_Ctor(void* self, void* localAddrs, const void* publicAddr, u32 natType, i32 extra)</code> |
| `BdLobbyMsg_WriteHeader` | 0xD1D8EC0 | 0x7FF729D98EC0 | <code class="wrap">u64 BdLobbyMsg_WriteHeader(void** buffer, u8 msgType, u8 serviceId)</code><br>Every header goes through BdLobbyMsg_WriteHeader(buf, msgType, serviceId) (8 callers incl. |
| `BdRemoteHttpTask_FinishRow` | 0xD21FDA0 | 0x7FF729DDFDA0 | <code class="wrap">u64 BdRemoteHttpTask_FinishRow(void** task, void* response)</code><br>The reply reaches BdRemoteHttpTask_FinishRow, which calls the resource's parser (PublisherObjectsResource_ParseResponse, which calls ObjectMetadata_ParseJson once per object) and sets task state 2 (done) or 3 (failed). |
| `Dw_GetLoginFlow` | 0xD22BF90 | 0x7FF729DEBF90 | <code class="wrap">u64 Dw_GetLoginFlow(void* loginConfig)</code><br>Dw_GetLoginFlow (bdLogin flow/service selector): returns *(uint*)(loginConfig+3124), with a 1-&gt;4/8 remap. |
| `DwFetch_GetStatus` | 0x96E4BA0 | 0x7FF7262A4BA0 | <code class="wrap">u8 DwFetch_GetStatus(u32 controller, u32* got, void* scratch)</code><br>IsDemonwareFetchingDone (native hash 0x603CD0351DA0D371, registered at 0x7FF71E914788) -&gt; 0x7FF7262ACBE0 -&gt; this function: DwFetch_GetStatus(controller, u32* got) -&gt; (required & *got) == required It ORs one bit per ready ... |
| `DwFetch_IsDone` | 0x96ECBE0 | 0x7FF7262ACBE0 | <code class="wrap">u8 DwFetch_IsDone(u32 controller)</code><br>DwFetch_IsDone(controller) is a wrapper that calls DwFetch_GetStatus(c, &got, &zeroed16). |
| `DwFetch_IsInventoryReady` | 0xB35B990 | 0x7FF727F1B990 | <code class="wrap">bool DwFetch_IsInventoryReady(unsigned int controller)</code><br>bool(uint ctrl) |
| `DwLogin_BuildStudioToken` | 0xD22CA90 | 0x7FF729DECA90 | <code class="wrap">u8 DwLogin_BuildStudioToken(void* loginConfig, void* userObj, void* outBuf)</code><br>DwLogin_BuildStudioToken(loginConfig, userObj, outBuf6784). |
| `Entitlement_IsOwned` | 0xB953340 | 0x7FF728513340 | <code class="wrap">char Entitlement_IsOwned(int controller, u64 nameHash)</code><br>char(int ctrl, u64 nameHash) |
| `FirstParty_GetLocalUserIndex` | 0xCC19EE0 | 0x7FF7297D9EE0 | <code class="wrap">u32 FirstParty_GetLocalUserIndex()</code><br>FirstParty_GetLocalUserIndex_ViaSession() -&gt; *(uint*)(*(void**)(mgr+24) + 0xD0). Nullary, 7 instructions, 0x19 bytes, prologue `sub rsp,28h` - ample room for a 5-byte jmp rel32. RVA 0xCC19EE0. Also written as `FirstParty_GetLocalUserIndex_ViaSession`, `FirstParty_GetSessionFieldD0_NULLDEREF`. |
| `FirstParty_GetSession` | 0xCC1F050 | 0x7FF7297DF050 | <code class="wrap">void* FirstParty_GetSession(void* mgr)</code><br>FirstParty_GetSession_MayBeNull(mgr) = *(void**)(mgr + 24), the first-party (Battle.net) SESSION object hanging off that manager. |
| `FirstParty_OnBgsDisconnected` | 0xCC1F2E0 | 0x7FF7297DF2E0 | <code class="wrap">u64 FirstParty_OnBgsDisconnected(uintptr firstPartyObj, uintptr unused, const u32* bgsCode)</code><br>(obj, ?, const u32* bgsCode) |
| `FirstParty_SetError` | 0xCC1F340 | 0x7FF7297DF340 | <code class="wrap">u64 FirstParty_SetError(uintptr firstPartyObj, int code)</code><br>(obj, code): +60=1, +64=code, +56=4 |
| `FirstParty_SetErrorState` | 0xCC1E380 | 0x7FF7297DE380 | <code class="wrap">u64 FirstParty_SetErrorState(uintptr firstPartyObj)</code><br>(obj): +56=4 only, no code |
| `Inventory_GetItemQuantity` | 0xB35B3E0 | 0x7FF727F1B3E0 | <code class="wrap">u64 Inventory_GetItemQuantity(int controller, unsigned int itemId)</code><br>u32(int ctrl, u32 itemId) |
| `Live_DwTokensRequired` | 0x9AE9370 | 0x7FF7266A9370 | bool(), int dvar &gt;= 1 |
| `LiveUser_AccountIdPickers` | 0xCAEB2F0 | 0x7FF7296AB2F0 | The two account-id pickers, the same kind of caller (2026-09-24 22:58, site #15 at RVA 0xCAEB368): LiveUser_GetAccountId_cand(ctrl, u64* out) 0x7FF7296AB340, 0x62 &lt;- match launch LiveUser_RefreshAccountId_cand(userData) ... Also written as `LiveUser_RefreshAccountId_cand`. |
| `LiveUser_FirstPartyPresenceOk` | 0xCAF79B0 | 0x7FF7296B79B0 | <code class="wrap">bool LiveUser_FirstPartyPresenceOk()</code><br>LiveUser_FirstPartyPresenceOk (bool()). |
| `LiveUser_ForceSignOutAndFatal` | 0xB37A320 | 0x7FF727F3A320 | <code class="wrap">char* LiveUser_ForceSignOutAndFatal()</code><br>The real producer is the tail call of LiveFirstParty_Frame: LiveFirstParty_Frame (0x7FF7296B5F00, gated on !Dvar_GetBool(nodw) && byte_7FF7371BF1FF) -&gt; if Dvar_GetBool(0x7FF733D20160) && LiveUser_IsSignedIn(0) && ...4 more ... |
| `LiveUser_GetXuidIfSignedIn` | 0xCAEB130 | 0x7FF7296AB130 | <code class="wrap">u64 LiveUser_GetXuidIfSignedIn(int controller)</code><br>u64(int ctrl) |
| `LiveUser_IsTrial` | 0xB591A00 | 0x7FF728151A00 | <code class="wrap">u8 LiveUser_IsTrial()</code><br>"Do you own the game" (LuaUtils.IsTrial = native 0x33698526482CB1F8 -&gt; 0x7FF726933CF0 -&gt; this). |
| `LiveUser_LoginDriver_Tick` | 0xB379160 | 0x7FF727F39160 | LiveUser_LoginDriver_Tick base + size: the return-address window the guard accepts. |
| `LiveUser_SetupIdentity` | 0xCB93500 | 0x7FF729753500 | LiveUser_OnSigninStateChange_SetupIdentity (0x7FF729753500, 0xFC bytes). Also written as `LiveUser_OnSigninStateChange_SetupIdentity`. |
| `LiveUser_SignOutBuildDropMessage` | 0xCB93740 | 0x7FF729753740 | <code class="wrap">char LiveUser_SignOutBuildDropMessage(u32 controller, const char** outMsg)</code><br>LiveUser_SignOut_BuildDropMessage(controller, const char** outMsg) -&gt; bool. RVA 0xCB93740. Also written as `LiveUser_PromoteSigninOnline_MaybeDrop`. |
| `Login_SetStatus` | 0xD22C4D0 | 0x7FF729DEC4D0 | <code class="wrap">u64 Login_SetStatus(void* ctx, const char* status, u32 code)</code><br>Login_SetStatus(ctx, const char* statusString, unsigned int code): the login state machine's own status setter (sub_7FF729DECF80 calls it at every transition). |
| `Loot_GetBattlePassOwned` | 0xAD41460 | 0x7FF727901460 | <code class="wrap">char Loot_GetBattlePassOwned(unsigned int controller, int season)</code><br>char(uint ctrl, int season) |
| `Loot_GetBattlePassRank` | 0xAD414F0 | 0x7FF7279014F0 | <code class="wrap">u64 Loot_GetBattlePassRank(unsigned int controller, int season)</code><br>u8(uint ctrl, int season) |
| `Loot_GetItemQuantity` | 0xAD41C60 | 0x7FF727901C60 | <code class="wrap">u64 Loot_GetItemQuantity(unsigned int controller, u64 itemId, u64, u64)</code><br>u32(uint ctrl, u32 itemId, -, -) |
| `Loot_UpdateBattlePassModels` | 0xB35DD00 | 0x7FF727F1DD00 | <code class="wrap">void Loot_UpdateBattlePassModels(int controller)</code><br>(int ctrl) |
| `Lpc_GetBuildContentIdString` | 0xC6EDE60 | 0x7FF7292ADE60 | const char*(); "%08x%08x" of the content id |
| `Lpc_OnListFailed` | 0xAF76070 | 0x7FF727B36070 |  |
| `Lpc_WriteManifest` | 0xAF760A0 | 0x7FF727B360A0 |  |
| `MtxSync_IsDoneOrInFlight` | 0x1B8DCB0 | 0x7FF71E74DCB0 |  |
| `MtxSync_OnBnetToken` | 0x1B90600 | 0x7FF71E750600 | <code class="wrap">u8 MtxSync_OnBnetToken(i32 error, i64* token)</code> |
| `MtxSync_RequestBnetTokenZEUS` | 0x1B906C0 | 0x7FF71E7506C0 |  |
| `MtxSync_ShouldStart` | 0x1B8DE40 | 0x7FF71E74DE40 |  |
| `ObjectMetadata_ParseJson` | 0xD1B0BD0 | 0x7FF729D70BD0 | <code class="wrap">u8 ObjectMetadata_ParseJson(void* metadata, void* json, u32 ownerType)</code> |
| `OnlineContent_OnPlaylistsLoaded` | 0xA2CA570 | 0x7FF726E8A570 | slot 0 callback: Playlist_LoadFromAssets + dvar overrides |
| `PublisherObjectsResource_Parse` | 0xD1CB130 | 0x7FF729D8B130 | <code class="wrap">u8 PublisherObjectsResource_Parse(void* resource, void* response)</code> |

## Demonware, login and first party: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `AntiCheat_StartReportExtendedAuthInfo` | 0xD232420 | 0x7FF729DF2420 |  |
| `bdAddr_IsValid` | 0xD244330 | 0x7FF729E04330 |  |
| `bdAuthTicket_Deserialize` | 0xD1742E0 | 0x7FF729D342E0 |  |
| `bdByteBuffer_CheckTypeTag` | 0xD1788D0 | 0x7FF729D388D0 | Reads one whole byte and compares it with the expected type id. Type 22 splices the buffer and reads again. |
| `bdByteBuffer_ReadBlob` | 0xD1784D0 | 0x7FF729D384D0 | Checks tag 0x13, then reads a typed UInt32 length, then that many bytes. |
| `bdByteBuffer_ReadRaw` | 0xD178470 | 0x7FF729D38470 |  |
| `bdByteBuffer_ReadStringInto` | 0xD178D00 | 0x7FF729D38D00 |  |
| `bdByteBuffer_ReadStructDataHeader` | 0xD178DB0 | 0x7FF729D38DB0 |  |
| `bdByteBuffer_ReadUChar8` | 0xD178E00 | 0x7FF729D38E00 |  |
| `bdByteBuffer_ReadUInt32` | 0xD178EC0 | 0x7FF729D38EC0 |  |
| `bdByteBuffer_ReadUInt64` | 0xD178F20 | 0x7FF729D38F20 |  |
| `bdByteBuffer_TypeName` | 0xD17BEF0 | 0x7FF729D3BEF0 |  |
| `bdByteBuffer_WriteStructDataHeader` | 0xD1794D0 | 0x7FF729D394D0 |  |
| `bdCommonAddr_Deserialize` | 0xD1777F0 | 0x7FF729D377F0 |  |
| `bdCommonAddr_IsSameAddr` | 0xD177AC0 | 0x7FF729D37AC0 |  |
| `BdLobby_OnServiceReply_Tag1` | 0xD218090 | 0x7FF729DD8090 |  |
| `BdLobbyConnection_PumpRecv` | 0xD217850 | 0x7FF729DD7850 |  |
| `BdLobbyMsg_Ctor` | 0xD212300 | 0x7FF729DD2300 |  |
| `BdLobbyMsg_WriteStructDataPayload` | 0xD20CFB0 | 0x7FF729DCCFB0 |  |
| `BdLobbyTask_OnReplyPayload_SetErr4` | 0xD1AB930 | 0x7FF729D6B930 |  |
| `BdRemoteHttp_ReadResponse` | 0xD208C50 | 0x7FF729DC8C50 |  |
| `BdRemoteHttp_ReadResponseHeader` | 0xD208390 | 0x7FF729DC8390 |  |
| `BdRemoteHttp_SendLobbyRequest_Svc10` | 0xD2117C0 | 0x7FF729DD17C0 |  |
| `bdStructBufferInputStream_Ctor` | 0xD2070F0 | 0x7FF729DC70F0 |  |
| `BdStructTask_ReadStructDataReply` | 0xD20CE20 | 0x7FF729DCCE20 |  |
| `BdUser_SubmitRequestForLocalUser` | 0xD37C084 | 0x7FF729F3C084 |  |
| `Crypto_KdfCounterMode` | 0xD17A560 | 0x7FF729D3A560 |  |
| `Crypto_RsaImportPubKey` | 0xD17AE60 | 0x7FF729D3AE60 |  |
| `Crypto_RsaPss_Verify` | 0xCE64210 | 0x7FF729A24210 | RSASSA-PSS verify: SHA-256, MGF1 with SHA-256, salt length 0. |
| `DwAuth_BuildRequest` | 0xD22F740 | 0x7FF729DEF740 | Builds the POST /auth/ request. Its host template is "%s-%s-auth3.%s.demonware.net". |
| `DwAuth_ParseReply` | 0xD2301E0 | 0x7FF729DF01E0 |  |
| `DwAuth_StubReturnTrue` | 0xD230AA0 | 0x7FF729DF0AA0 |  |
| `DwAuth_VerifyReplySignature` | 0xD230F90 | 0x7FF729DF0F90 |  |
| `FirstParty_GetBnetAccountId_cand` | 0xCAF6440 | 0x7FF7296B6440 |  |
| `FirstParty_GetErrorMessage` | 0xCAF6460 | 0x7FF7296B6460 |  |
| `FirstParty_IsKoreaMinor_cand` | 0xCAF78B0 | 0x7FF7296B78B0 |  |
| `FirstParty_IsKoreanIGR_cand` | 0xCAF7AE0 | 0x7FF7296B7AE0 |  |
| `FirstParty_Manager_Ctor_NullsSessionAt24` | 0xCC1D5A0 | 0x7FF7297DD5A0 |  |
| `FirstParty_NotifyStateListeners` | 0xCAFF680 | 0x7FF7296BF680 |  |
| `FirstParty_PushErrorMessageToLua` | 0x98CAFA0 | 0x7FF72648AFA0 |  |
| `FirstParty_RefreshUserRequest` | 0xCC281B0 | 0x7FF7297E81B0 |  |
| `FirstParty_StateTick` | 0xCC1E3A0 | 0x7FF7297DE3A0 |  |
| `Inventory_Frame` | 0xB35D5E0 | 0x7FF727F1D5E0 |  |
| `LiveFirstParty_Frame` | 0xCAF5F00 | 0x7FF7296B5F00 |  |
| `LiveUser_AttachLiveStats` | 0xA8F3690 | 0x7FF7274B3690 |  |
| `LiveUser_BuildSignOutErrorMessage` | 0xCB93600 | 0x7FF729753600 |  |
| `LiveUser_GetAccountId_cand` | 0xCAEB340 | 0x7FF7296AB340 |  |
| `LiveUser_GetUserDataForController` | 0xA8F2E70 | 0x7FF7274B2E70 | <code class="wrap">uintptr* LiveUser_GetUserDataForController(int controllerIndex)</code><br>Bound by signature. |
| `LiveUser_HandleSignOut` | 0xCB92990 | 0x7FF729752990 |  |
| `LiveUser_IsOnlineReady` | 0x96ECD00 | 0x7FF7262ACD00 |  |
| `LiveUser_OnDwConnected` | 0xCB62670 | 0x7FF729722670 |  |
| `LiveUser_OnDwLoginComplete_SetState4` | 0xB378F30 | 0x7FF727F38F30 |  |
| `LiveUser_PresenceOkAndSignedInOnline` | 0xA8F3540 | 0x7FF7274B3540 |  |
| `LiveUser_SetOfflineLocalName` | 0xCB93920 | 0x7FF729753920 |  |
| `LiveUser_UpdateSigninState` | 0xCB60390 | 0x7FF729720390 |  |
| `Lpc_SyncFrame` | 0xAF76860 | 0x7FF727B36860 |  |
| `Lsg_BuildHandshake_ParseBDDATA` | 0xD227050 | 0x7FF729DE7050 |  |
| `Lsg_ConnectTask_BeginResolve` | 0xD231BE0 | 0x7FF729DF1BE0 |  |
| `Lsg_ConnectTask_Ctor` | 0xD231140 | 0x7FF729DF1140 |  |
| `Lsg_ErrorCodeToString` | 0xD195E90 | 0x7FF729D55E90 | A stub in retail: returns the text HIDDEN for every code. |
| `Lsg_OnEncryptedMessage` | 0xD227780 | 0x7FF729DE7780 | Receives a 0x85 record: counter check, HMAC check, AES-128-CBC decrypt. |
| `Lsg_PumpRecv` | 0xD228470 | 0x7FF729DE8470 |  |
| `Lsg_RecvLengthPrefix` | 0xD2286A0 | 0x7FF729DE86A0 |  |
| `Lsg_SendEncryptedMessage` | 0xD228D60 | 0x7FF729DE8D60 |  |
| `Lsg_SendHello` | 0xD228940 | 0x7FF729DE8940 | Writes the 28-byte HELLO: u32 200, 200, 220, 220, the maximum payload, then an 8-byte client nonce. |
| `Lsg_Task_GetErrorCode` | 0xD1AB720 | 0x7FF729D6B720 |  |
| `MtxSync_BeginBnetTokenRequest` | 0x1B90420 | 0x7FF71E750420 |  |
| `OnlineContent_LoadSlotZones` | 0xA2CD740 | 0x7FF726E8D740 |  |

## Sessions and netcode

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `CL_LocalClientToController` | 0xC058BD0 | 0x7FF728C18BD0 | <code class="wrap">int CL_LocalClientToController(int localClient)</code><br>A replay of the engine's own `openmenu` console command, Cmd_OpenMenu_f (0x7FF726FC37E0): controller = CL_LocalClientToController(localClient); UI_SetUiActive(localClient, true); ... |
| `ClientSession_JoinKick` | 0xB400470 | 0x7FF727FC0470 |  |
| `ClientSession_JoinKnownHost` | 0xAD86AD0 | 0x7FF727946AD0 | ClientSession_JoinKnownHost is the one-shot trigger; the other two are the primitives it composes, hooked so a real join tells us what a valid host candidate - above all the 16-byte netadr handle - actually contains. |
| `ClientSession_JoinPendingTarget` | 0xAD86A30 | 0x7FF727946A30 |  |
| `ClientSession_QueryHostByXuid` | 0xAD87190 | 0x7FF727947190 |  |
| `ClientSession_StartJoin` | 0xAD86640 | 0x7FF727946640 |  |
| `GScr_LaunchP2P` | 0xAED9000 | 0x7FF727A99000 | GScr_LobbyHost_LaunchPrivateP2P |
| `GScr_LaunchP2P_Full` | 0xAED9190 | 0x7FF727A99190 | ..._Full |
| `GScr_LaunchP2P_Named` | 0xAED90F0 | 0x7FF727A990F0 | ..._Named |
| `JoinCtx_AddHostCandidate` | 0xAD86520 | 0x7FF727946520 |  |
| `Lobby_ApplySessionSettings_cand` | 0xA8F5540 | 0x7FF7274B5540 | a member applies the host's settings |
| `LobbyHost_LaunchP2P_Plain` | 0x958EE00 | 0x7FF72614EE00 | The native host-launch entrypoint we REPLAY through. LobbyHost_LaunchPrivateP2P_Plain builds the two GSC istring/script-value handles and the pointer-laden session-config blob itself (via sub_7FF729E07240 + sub_7FF728C18B00), so ... Also written as `LobbyHost_LaunchPrivateP2P_Plain`. |
| `LobbyRoot_SetNetworkModeModel` | 0xB1EF360 | 0x7FF727DAF360 | <code class="wrap">u64 LobbyRoot_SetNetworkModeModel(int mode)</code><br>(int mode) |
| `NetMsg_Dispatch` | 0xA039370 | 0x7FF726BF9370 |  |
| `NetMsg_SendJoinResponse` | 0xA0382C0 | 0x7FF726BF82C0 |  |
| `Session_GetSessionObject` | 0xA3C2D20 | 0x7FF726F82D20 |  |
| `Session_ParseJoinLobbyRequest` | 0xA03B070 | 0x7FF726BFB070 | The JoinLobby request parser. Hooked on the HOST so the incoming request's fields are readable side by side with the verdict they produce - otherwise a refusal names a code but never the value that earned it. |
| `Session_PickActiveSlot` | 0xA3C27C0 | 0x7FF726F827C0 | <code class="wrap">int Session_PickActiveSlot(int type)</code><br>BOOL(int type) |
| `Session_SetMapName` | 0xAF672A0 | 0x7FF727B272A0 | <code class="wrap">char Session_SetMapName(u32 slot, const char* mapName)</code><br>char(u32 slot, const char* map) |
| `SV_ClientStatsReady` | 0x7058230 | 0x7FF723C18230 | <code class="wrap">char SV_ClientStatsReady(u8* svClient)</code><br>char(svClient*) |
| `SV_DirectConnect` | 0x718AB60 | 0x7FF723D4AB60 | <code class="wrap">i64 SV_DirectConnect(void* netadr)</code> |
| `SV_GetClientStatsInstance` | 0x7019720 | 0x7FF723BD9720 | <code class="wrap">void* SV_GetClientStatsInstance(i16 clientNum, int source)</code><br>inst*(short client, int source); svClient+53808+64*src |
| `SV_IsClientStatsSlotReady` | 0x70193D0 | 0x7FF723BD93D0 | <code class="wrap">bool SV_IsClientStatsSlotReady(i16 clientNum, int source)</code><br>bool(short client, int source) |
| `SV_ReseatClientLoopback` | 0x7189410 | 0x7FF723D49410 | was 0x7FF71FD49410 (mid-function typo); IDB names this address |
| `SV_StageConnectMessage` | 0x9ADE1F0 | 0x7FF72669E1F0 | <code class="wrap">i64 SV_StageConnectMessage(const char* connectStr)</code> |
| `SV_StartMap` | 0x71884F0 | 0x7FF723D484F0 | <code class="wrap">u64 SV_StartMap(u32 a1, const char* mapName, u32 kind, u8 a4, u32 a5)</code><br>SV_StartMap is where the map name enters: SV_SpawnServer, CL_MapLoading, the mapname dvar and Com_LoadLevelFastFiles all take it from here. |
| `SV_UnstageConnectMessage` | 0x9ADE1A0 | 0x7FF72669E1A0 | <code class="wrap">i64 SV_UnstageConnectMessage()</code> |

## Sessions and netcode: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `CL_ApplyServerStatDelta_cand` | 0x232D600 | 0x7FF71EEED600 |  |
| `CL_Disconnect` | 0x5CD2110 | 0x7FF722892110 | <code class="wrap">void CL_Disconnect(int localClientNum, bool deactivateClient, const char* message)</code><br>Bound by signature. |
| `HostSession_StartLaunch` | 0xAF6A790 | 0x7FF727B2A790 |  |
| `LobbyBase_GetNetworkMode` | 0xAF59A40 | 0x7FF727B19A40 |  |
| `LobbyBase_NetworkModeToSessionNetworkMode` | 0xB5A66F0 | 0x7FF7281666F0 |  |
| `LobbyBase_SetNetworkMode` | 0xAF59B60 | 0x7FF727B19B60 | <code class="wrap">void LobbyBase_SetNetworkMode(T9::LobbyNetworkMode networkMode)</code><br>Bound by signature. Stores the lobby's network mode, updates the menus' model, then tail-calls Com_SessionMode_SetNetworkMode with the mapped value. |
| `LobbyClient_ApplyLobbyStateUpdate` | 0xA690060 | 0x7FF727250060 |  |
| `LobbyClient_JoinServerEntry` | 0xB52D250 | 0x7FF7280ED250 |  |
| `LobbyUI_PushGameSettings` | 0xAF66C50 | 0x7FF727B26C50 |  |
| `LobbyUI_RaiseLeaderActivityChanged` | 0xB1EF230 | 0x7FF727DAF230 |  |
| `LobbyUI_SetTargetMenuAndNotify` | 0xB1EF430 | 0x7FF727DAF430 | <code class="wrap">void LobbyUI_SetTargetMenuAndNotify(int targetMenu, char fromLobbyState)</code> |
| `NetMsg_Handle_JoinLobby` | 0xA036380 | 0x7FF726BF6380 |  |
| `NetMsg_Handle_JoinResponse` | 0xAD86C90 | 0x7FF727946C90 |  |
| `NetMsg_SendAnnounceHost` | 0xAA07430 | 0x7FF7275C7430 |  |
| `NetSession_Launch` | 0xAEE4650 | 0x7FF727AA4650 |  |
| `Session_BuildLobbyDescriptor` | 0xB35EB70 | 0x7FF727F1EB70 |  |
| `Session_ParseJoinDescriptor` | 0xA03ADE0 | 0x7FF726BFADE0 |  |
| `Session_WriteJoinRequestMsg` | 0xA038460 | 0x7FF726BF8460 |  |
| `SV_ImportClientStatsBlobs` | 0xAA00420 | 0x7FF7275C0420 |  |

## LUI and Lua

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `lua_createtable` | 0xD27CF30 | 0x7FF729E3CF30 | <code class="wrap">void lua_createtable(void* L, int narr, int nrec)</code><br>lua_createtable(L, narr, nrec) - the IDB used to call this lua_call. |
| `Lua_Engine_GetLobbyNetworkMode` | 0xAECE790 | 0x7FF727A8E790 | <code class="wrap">u64 Lua_Engine_GetLobbyNetworkMode(void* luaState)</code><br>(L) |
| `Lua_GameModeIsMode_Impl` | 0x98CAA40 | 0x7FF72648AA40 | <code class="wrap">u64 Lua_GameModeIsMode_Impl(void* luaState, int mode)</code><br>(L, int mode) |
| `lua_getfield` | 0xD27CC50 | 0x7FF729E3CC50 | <code class="wrap">void lua_getfield(void* L, int idx, const char* k)</code> |
| `lua_getinfo` | 0xD287E20 | 0x7FF729E47E20 | <code class="wrap">int lua_getinfo(void* L, const char* what, void* ar, int extra)</code> |
| `lua_getmetatable` | 0xD27D150 | 0x7FF729E3D150 | <code class="wrap">int lua_getmetatable(void* L, int objindex)</code> |
| `lua_getstack` | 0xD287100 | 0x7FF729E47100 | <code class="wrap">int lua_getstack(void* L, int level, void* ar)</code><br>lua_getstack fills lua_Debug::i_ci (+316) with a packed frame locator: lo16 = (frame - L-&gt;stack) &gt;&gt; 3 (L-&gt;stack is the pointer at L+32) hi16 = the frame's slot count so frame_base = *(TValue**)(L+32) + lo16, the ... |
| `lua_gettable` | 0xD27CD90 | 0x7FF729E3CD90 | <code class="wrap">void lua_gettable(void* L, int idx)</code> |
| `Lua_IsDemonwareFetchingDone_Impl` | 0x878AE20 | 0x7FF72534AE20 | The waiver answers true for these five ONLY, and only to Lua (the call from Lua_IsDemonwareFetchingDone_Impl); the engine's own callers keep the truth. |
| `lua_load` | 0xD288AE0 | 0x7FF729E48AE0 | <code class="wrap">int lua_load(void* L, lua_ReaderT* reader, void* data, const char* chunkname)</code><br>Verified 2026-09-26: lua_load(L, reader, data, chunkname) -&gt; status: caller-guarded, straight into luaD_protectedparser(L, reader, data, chunkname, mode = 0) (0x7FF729E48B70) -&gt; lj_cpparser (0x7FF729E49330), which takes ... Also written as `lua_load_cand`. |
| `lua_next` | 0xD27E310 | 0x7FF729E3E310 | <code class="wrap">int lua_next(void* L, int idx)</code> |
| `Lua_PushAeSyncBuffer` | 0x9EBE500 | 0x7FF726A7E500 | <code class="wrap">u64 Lua_PushAeSyncBuffer(void* luaState, int controller)</code><br>(L, ctrl), Engine.GetAESyncBuffer's body; inlines the +40024 read |
| `lua_pushvalue` | 0xD27B2E0 | 0x7FF729E3B2E0 | <code class="wrap">void lua_pushvalue(void* L, int idx)</code> |
| `lua_rawgeti` | 0xD27CE40 | 0x7FF729E3CE40 | <code class="wrap">void lua_rawgeti(void* L, int idx, int n)</code> |
| `lua_setfield` | 0xD27D460 | 0x7FF729E3D460 | <code class="wrap">void lua_setfield(void* L, int idx, const char* k)</code><br>lua_setfield(L, idx, k) - t[k] = top, pops. |
| `lua_tolstring` | 0xD27BD70 | 0x7FF729E3BD70 | <code class="wrap">const char* lua_tolstring(void* L, int idx, size_t* len)</code> |
| `lua_tonumber` | 0xD27EA90 | 0x7FF729E3EA90 | <code class="wrap">double lua_tonumber(void* L, int idx)</code> |
| `lua_type` | 0xD27B860 | 0x7FF729E3B860 | <code class="wrap">int lua_type(void* L, int idx)</code> |
| `luaG_getobjname` | 0xD2876D0 | 0x7FF729E476D0 | <code class="wrap">const char* luaG_getobjname(void* L, void* proto, void* pc, unsigned int reg, const char** nameOut)</code><br>MEASURED, not theorised: the online frontend's first Lua error was followed immediately by 0xC0000005 (reading 0x39) at BlackOpsColdWar.exe+0xD291273 which is luaO_pushvfstring's inline strlen of a "%s" argument, reached from ... |
| `luaL_traceback` | 0xD288320 | 0x7FF729E48320 | <code class="wrap">u64 luaL_traceback(void* B, void* L, const char* msg, int level)</code><br>luaL_traceback is the errfunc LUI installs around those pcalls - it is what appends "stack traceback:" to the message - and an errfunc runs BEFORE the throw unwinds. |
| `LuaNative_AreLocalFilesReady` | 0x1D57CC0 | 0x7FF71E917CC0 | "AreLocalFilesReady" |
| `LuaNative_ConnectionInfo` | 0x1D6D690 | 0x7FF71E92D690 | 0x5451F40A2FEDDF88 -&gt; table, .connectionState |
| `LuaNative_ConnErrorGate` | 0x1D6F700 | 0x7FF71E92F700 | 0x545A16E755DB1D5C (read when state 263/264) |
| `LuaNative_ContentIsFullyInstalled` | 0x1D73020 | 0x7FF71E933020 | 0x5541E6CA5E529182 -&gt; Content_IsModeFullyInstalled_cand |
| `LuaNative_ContentIsInstalling` | 0x1D73050 | 0x7FF71E933050 | 0x5242D2DE58485C35 -&gt; Content_IsModeInstalling_cand |
| `LuaNative_ContentIsPlayable` | 0x1D730A0 | 0x7FF71E9330A0 | 0x06CD1640D0F93036 -&gt; Content_IsModePlayable_cand |
| `LuaNative_FirstPartyDisconnected` | 0x1D6E800 | 0x7FF71E92E800 | 0x34D07729ED48730D -&gt; g_firstPartyManager+61 |
| `LuaNative_FirstPartyHasError` | 0x1D6E8A0 | 0x7FF71E92E8A0 | 0x2FFC1C70C8D5B359 -&gt; g_firstPartyManager+60 |
| `LuaNative_ForceOfflineGate` | 0x1D730D0 | 0x7FF71E9330D0 | 0x3573048F8D3B4E25 (CoDShared.ForceOffline) |
| `LuaNative_GetDvarInt` | 0x1D619A0 | 0x7FF71E9219A0 | 0x622EAAB59AA27E9B (CoDShared.IsIntDvarNonZero) |
| `LuaNative_GetLobbyNav` | 0x1D66230 | 0x7FF71E926230 | 0x69882F293C327557 |
| `LuaNative_GetPlayerQueueInfo` | 0x1D68B20 | 0x7FF71E928B20 | "GetPlayerQueueInfo" -&gt; table (closed/queued/disabled) |
| `LuaNative_IsKoreaMinor` | 0x1D715E0 | 0x7FF71E9315E0 | 0x45405A6484A88367 -&gt; FirstParty_IsKoreaMinor_cand |
| `LuaNative_IsLobbySlotLive` | 0x1D71700 | 0x7FF71E931700 | 0x10EA2BE00F49480D -&gt; Session_IsSlotActiveAndState2_cand |
| `LuaNative_IsPlayerQueued` | 0x1D725F0 | 0x7FF71E9325F0 | "IsPlayerQueued" |
| `LuaNative_IsSignedInToLive` | 0x1D73150 | 0x7FF71E933150 | "IsSignedInToLive" (the title timer's test) |
| `LuaNative_PrintError` | 0x1D7C000 | 0x7FF71E93C000 | native 0x4458FE92FEB39D4E |
| `LuaNative_PrintInfo` | 0x1D7C050 | 0x7FF71E93C050 | native 0x28C5711DAACC99F4 |
| `LuaNative_PrintWarning` | 0x1D7C0C0 | 0x7FF71E93C0C0 | native 0x65DF86CF48135674 |
| `LuaNative_QueueGate` | 0x1D71830 | 0x7FF71E931830 | 0x0F62AEC4075B0105 |
| `LuaNative_UniversalAccountA` | 0x1D73940 | 0x7FF71E933940 | 0x7CE050ECDC5CFD1D |
| `LuaNative_UniversalAccountB` | 0x1D73920 | 0x7FF71E933920 | 0x21E94361FF6923EA |
| `LUI_DispatchAddMenuEvent` | 0xADD7770 | 0x7FF727997770 | <code class="wrap">i64 LUI_DispatchAddMenuEvent(const char* root, u64 menuHash, int controller, void* luaState)</code><br>A replay of the engine's own `openmenu` console command, Cmd_OpenMenu_f (0x7FF726FC37E0): controller = CL_LocalClientToController(localClient); UI_SetUiActive(localClient, true); ... |
| `LUI_GetRootName` | 0x8D17050 | 0x7FF7258D7050 | <code class="wrap">const char* LUI_GetRootName(int controller)</code><br>A replay of the engine's own `openmenu` console command, Cmd_OpenMenu_f (0x7FF726FC37E0): controller = CL_LocalClientToController(localClient); UI_SetUiActive(localClient, true); ... |
| `LUI_ProtectedCall` | 0x56D3FA0 | 0x7FF722293FA0 | <code class="wrap">int LUI_ProtectedCall(void* L, int nargs, int nresults, int errfunc)</code><br>LUI_ProtectedCall(L, nargs, nresults, errfunc) -&gt; status - the setjmp-guarded wrapper LuiEvent_Dispatch uses around T9's modified lua_pcall (0x7FF729E3DB70). |
| `LUI_RunFile` | 0xAFCCCD0 | 0x7FF727B8CCD0 | <code class="wrap">u8 LUI_RunFile(void* luaState, const char* name)</code><br>LUI_RunFile(lua_State* L, const char* name) -&gt; bool. |
| `UI_SetUiActive` | 0x8D272E0 | 0x7FF7258E72E0 | <code class="wrap">void UI_SetUiActive(i64 localClient, bool active)</code><br>A replay of the engine's own `openmenu` console command, Cmd_OpenMenu_f (0x7FF726FC37E0): controller = CL_LocalClientToController(localClient); UI_SetUiActive(localClient, true); ... |

## LUI and Lua: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Cmd_AddCommandInternal` | 0x9ACBAD0 | 0x7FF72668BAD0 |  |
| `Cmd_OpenMenu_f` | 0xA4037E0 | 0x7FF726FC37E0 |  |
| `lj_parse` | 0xD29D720 | 0x7FF729E5D720 |  |
| `lj_strfmt_obj` | 0xD290E30 | 0x7FF729E50E30 |  |
| `Lua_FirstParty_GetErrorMessage` | 0x1D5EF40 | 0x7FF71E91EF40 |  |
| `lua_index2adr` | 0xD27EC10 | 0x7FF729E3EC10 |  |
| `lua_pcall` | 0xD27DB70 | 0x7FF729E3DB70 |  |
| `lua_settop` | 0xD27B1E0 | 0x7FF729E3B1E0 |  |
| `luaD_protectedparser` | 0xD288B70 | 0x7FF729E48B70 |  |
| `luaF_getlocalname` | 0xD288970 | 0x7FF729E48970 |  |
| `LuaFile_LoadAsset` | 0xCA82580 | 0x7FF729642580 |  |
| `luaG_currentline` | 0xD2886A0 | 0x7FF729E486A0 |  |
| `luaG_currentpc` | 0xD288740 | 0x7FF729E48740 |  |
| `luaH_next` | 0xD28CE80 | 0x7FF729E4CE80 |  |
| `LuaNative_Localize_Impl` | 0x878C140 | 0x7FF72534C140 | The body of Engine.Localize and Engine.LocalizeHash. Returns a string argument untouched only when its first byte is 0x15; any other string or hash is the name of a localize entry, and a missing entry is fatal. |
| `luaS_new` | 0xD28BD20 | 0x7FF729E4BD20 |  |
| `LUI_Init_cand` | 0x8D172D0 | 0x7FF7258D72D0 |  |
| `LUI_RegisterEngineNatives_cand` | 0x1D44CF0 | 0x7FF71E904CF0 |  |
| `LUI_ReportUiErrorCode_cand` | 0x5702390 | 0x7FF7222C2390 |  |
| `LuiEvent_Dispatch` | 0xAFCCA80 | 0x7FF727B8CA80 |  |
| `LuiNative_JoinPendingTarget` | 0x1D73F10 | 0x7FF71E933F10 |  |
| `LuiNative_JoinServerEntry` | 0x1D73E50 | 0x7FF71E933E50 |  |
| `UI_RestartUILevel_cand` | 0x57895C0 | 0x7FF7223495C0 |  |

## GSC VM

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `GScr_AreStatWritesEnabled` | 0x5E4E2D0 | 0x7FF722A0E2D0 | Its sibling, same force dvar plus a kill switch, for the 7 GSC stat-write helpers (sub_7FF722A093F0 .. sub_7FF722A0E1E0): `(force \|\| modecheck) && !dvar(off_7FF72CCC1308)`. |
| `Scr_ConstructMessageString` | 0xB8400B0 | 0x7FF7284000B0 | <code class="wrap">void Scr_ConstructMessageString(int inst, u32* out, u32 firstParam, int count)</code><br>Scr_ConstructMessageString(inst, out, firstParam, count): builds the payload of iprintln and iprintlnbold (function and player-method forms) from the script args, into out = {u32 length; char text[1024]}. |

## GSC VM: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `ClientField_Register` | 0xAECD190 | 0x7FF727A8D190 |  |
| `ClientField_Shutdown` | 0xAECD6C0 | 0x7FF727A8D6C0 |  |
| `ClientField_TypeFromString` | 0xAECBE60 | 0x7FF727A8BE60 |  |
| `GScr_IPrintLnBold` | 0x3C59D20 | 0x7FF720819D20 |  |
| `Scr_AddEntity` | 0x737F490 | 0x7FF723F3F490 |  |
| `Scr_ConstructMessageString_Fmt` | 0xB840010 | 0x7FF728400010 |  |
| `Scr_GetStringTableArg_cand` | 0xCA45590 | 0x7FF729605590 |  |
| `SL_GetString_Guarded` | 0x1BC3780 | 0x7FF71E783780 |  |
| (stock handler of GSC opcode 0x13) | 0x1BF6EB0 | 0x7FF71E7B6EB0 | Copies its operand into a dead local and does nothing else. The loader patches its own handler into the table. |
| `VM_OP_GetString` | 0x1BB01E0 | 0x7FF71E7701E0 |  |

## PlayerData, stats and progression

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Ddl_FindRootByHash` | 0xCABB6D0 | 0x7FF72967B6D0 | <code class="wrap">void* Ddl_FindRootByHash(u64 hash, int unused)</code><br>root*(u64 hash, int) |
| `Ddl_GetUInt64` | 0xCABBBC0 | 0x7FF72967BBC0 | <code class="wrap">u64 Ddl_GetUInt64(void* state, void* instance)</code><br>u64(state*, inst*) |
| `Ddl_GetValue` | 0xCABBD50 | 0x7FF72967BD50 | <code class="wrap">u64 Ddl_GetValue(void* state, void* instance)</code><br>u64(state*, inst*), any scalar type |
| `Ddl_InitInstance` | 0xCABCA70 | 0x7FF72967CA70 | <code class="wrap">u64 Ddl_InitInstance(void* buffer, int size, void* root, void* instance, u64, u64, u64)</code> |
| `Ddl_InitRootState` | 0xCABB900 | 0x7FF72967B900 | <code class="wrap">void* Ddl_InitRootState(void* state, void* instance)</code><br>state*(state*, inst*) |
| `Ddl_IsInstanceValid` | 0xCABB200 | 0x7FF72967B200 | <code class="wrap">bool Ddl_IsInstanceValid(void* instance)</code><br>bool(inst*) |
| `Ddl_MoveToMemberByHash` | 0xCABC890 | 0x7FF72967C890 | <code class="wrap">bool Ddl_MoveToMemberByHash(void* inState, void* outState, const u64* hash)</code><br>bool(in*, out*, const u64* hash) |
| `Ddl_ParseHeader` | 0xCAD2160 | 0x7FF729692160 | <code class="wrap">void* Ddl_ParseHeader(void* out, const void* buffer, char headerless)</code><br>out*(out*, buf*, char headerless) |
| `Ddl_PushStateToLua` | 0xCAAE790 | 0x7FF72966E790 | <code class="wrap">u64 Ddl_PushStateToLua(void* luaState, void* state, void* instance)</code><br>(L, state*, inst*) -&gt; ddl userdata |
| `Ddl_ScrambleInstanceBuffer` | 0xCAC0420 | 0x7FF729680420 | <code class="wrap">void Ddl_ScrambleInstanceBuffer(void* instance, void* buffer, unsigned int size, unsigned int key)</code><br>(inst*, buf*, u32 size, u32 key) |
| `Ddl_SetUInt64` | 0xCABD180 | 0x7FF72967D180 | <code class="wrap">bool Ddl_SetUInt64(void* state, void* instance, u64 value)</code><br>bool(state*, inst*, u64) |
| `Ddl_UnscrambleInstanceBuffer` | 0xCAC04C0 | 0x7FF7296804C0 | <code class="wrap">void Ddl_UnscrambleInstanceBuffer(void* instance, void* buffer, unsigned int size)</code><br>(inst*, buf*, u32 size) |
| `G_AddPlayerRankXp` | 0x70238F0 | 0x7FF723BE38F0 | <code class="wrap">u64 G_AddPlayerRankXp(i16 clientNum, i64 xp, i64 xpType, u64 eventHash)</code><br>G_AddPlayerRankXp(clientNum, xp, xpType, eventHash): every GSC XP source lands here. |
| `LiveStats_GetAeRootStateSlot` | 0x9EBD3F0 | 0x7FF726A7D3F0 | <code class="wrap">void* LiveStats_GetAeRootStateSlot(int controller)</code><br>state*(int ctrl); LiveUser+40024 -&gt; +18392 (32 B) |
| `LiveStats_GetLiveUserStatsInstance` | 0x9EBD380 | 0x7FF726A7D380 | <code class="wrap">void* LiveStats_GetLiveUserStatsInstance(int controller)</code><br>inst*(int ctrl); LiveUser+40024 -&gt; +18328 |
| `LiveStats_GetXp` | 0x9EBD710 | 0x7FF726A7D710 | <code class="wrap">unsigned int LiveStats_GetXp(void* instance, unsigned int season)</code><br>u32(inst*, u32 season=-1) |
| `LiveStats_SetAarModelFlag` | 0x875F590 | 0x7FF72531F590 | <code class="wrap">u64 LiveStats_SetAarModelFlag(i64 controller, u64 member, u64 value)</code><br>(ctrl, member hash, bool) on model 0x749D1EE50313ACCA |
| `LiveStats_SetXp` | 0x9EBF100 | 0x7FF726A7F100 | <code class="wrap">bool LiveStats_SetXp(void* instance, unsigned int season, int xp)</code><br>bool(inst*, u32 season=-1, int xp) |
| `LiveStorage_AreMatchStatsEnabled` | 0xAA03DA0 | 0x7FF7275C3DA0 | The match-stats gate. `forceDvar \|\| (mp/wz ? eligible : zm && networkMode == 2 && matchType != 1)`. |
| `LiveStorage_AreStatsReadable` | 0x875F360 | 0x7FF72531F360 | <code class="wrap">bool LiveStorage_AreStatsReadable(unsigned int controller)</code><br>bool(uint ctrl) |
| `LiveStorage_BeginStatsTransfer` | 0x875A310 | 0x7FF72531A310 | <code class="wrap">char LiveStorage_BeginStatsTransfer(int controller)</code><br>LiveStorage_BeginStatsTransfer(ctrl) -&gt; bool, from CL_ConnectionlessPacket on connect. |
| `LiveStorage_CommitStatsTransfer` | 0x8760000 | 0x7FF725320000 | <code class="wrap">u64 LiveStorage_CommitStatsTransfer(int controller, int source, unsigned int checksum, char final)</code><br>LiveStorage_CommitStatsTransfer(ctrl, source, checksum, final): copies the server's final stats instance for `source` into the playerdata buffer and queues its write. |
| `LiveStorage_GetGametypeStatsMapId` | 0xAA03D40 | 0x7FF7275C3D40 | unsigned(), 19 for ZM |
| `LiveStorage_GetPrimaryStatsMapId` | 0xAA03C50 | 0x7FF7275C3C50 | unsigned(), 5 (25 in CP) |
| `LiveStorage_GetStatsDdlRootForSource` | 0xAA03740 | 0x7FF7275C3740 | <code class="wrap">void* LiveStorage_GetStatsDdlRootForSource(int source)</code><br>root*(int source) |
| `PlayerData_AreLocalFilesReady` | 0x96E31D0 | 0x7FF7262A31D0 | The native -&gt; PlayerData_AreLocalFilesReady(ctrl): LiveUser[ctrl]+5760 != 0 && LiveStorage_AreOnlineDataMapsReady(ctrl, 1) (true for any mode but 2) && PlayerData_AreDataMapGroupReady(ctrl, 1) (mode-1 rows of the group table) ... |
| `PlayerData_ControllerStorageTick` | 0xAA01E90 | 0x7FF7275C1E90 | <code class="wrap">char PlayerData_ControllerStorageTick(unsigned int controller)</code><br>PlayerData_ControllerStorageTick(controller) - the per-frame load driver, and the seam that actually works. |
| `PlayerData_GetBuffer` | 0xAA00DF0 | 0x7FF7275C0DF0 | <code class="wrap">void* PlayerData_GetBuffer(i64 controller, unsigned int dataMapId, int version)</code><br>inst*(int ctrl, unsigned id, int ver) |
| `PlayerData_IsBufferReady` | 0xAA01620 | 0x7FF7275C1620 | <code class="wrap">bool PlayerData_IsBufferReady(int controller, unsigned int dataMapId, int version)</code><br>bool(int ctrl, unsigned id, int ver) |
| `PlayerData_OnStorageOpComplete` | 0xAA01920 | 0x7FF7275C1920 | <code class="wrap">void* PlayerData_OnStorageOpComplete(unsigned int controller, int opKind, unsigned int resultCode, unsigned int* entry)</code><br>PlayerData_OnStorageOpComplete(controller, opKind, resultCode, entry) - THE writer of entry+120 on the load path, and the thing that actually decides when a data map becomes readable. |
| `PlayerData_ResetBufferToDefaults` | 0xAA02250 | 0x7FF7275C2250 | <code class="wrap">i64 PlayerData_ResetBufferToDefaults(unsigned int controller, unsigned int dataMapId, int version)</code><br>PlayerData_ResetBufferToDefaults(controller, dataMapId, version). |
| `Progression_IsAttachmentLockedInBlock` | 0x75791E0 | 0x7FF7241391E0 | <code class="wrap">char Progression_IsAttachmentLockedInBlock(int mode, void* statsBlock, unsigned int itemIndex, int slot, char a5)</code><br>char(int mode, block*, uint item, int slot, char) |
| `Progression_IsAttachmentSlotLocked` | 0x7578F10 | 0x7FF724138F10 | <code class="wrap">bool Progression_IsAttachmentSlotLocked(unsigned int mode, unsigned int controller, unsigned int itemIndex, int slot)</code><br>bool(uint mode, uint ctrl, uint item, int slot) |
| `Progression_IsItemLocked` | 0x75795C0 | 0x7FF7241395C0 | <code class="wrap">bool Progression_IsItemLocked(int mode, unsigned int controller, int itemIndex)</code><br>bool(int mode, uint ctrl, int item) |
| `Progression_IsItemOptionLockedCore` | 0x757AC90 | 0x7FF72413AC90 | <code class="wrap">char Progression_IsItemOptionLockedCore(unsigned int mode, unsigned int controller, unsigned int itemIndex, unsigned int optionIndex, char skipPrerequisite)</code><br>char(uint mode, uint ctrl, uint item, uint option, char skipPrereq) |
| `Rank_GetLevelForXp` | 0xAD44DC0 | 0x7FF727904DC0 | <code class="wrap">int Rank_GetLevelForXp(int xp)</code><br>int(int xp) |
| `Rank_GetMaxXp` | 0xAD44820 | 0x7FF727904820 | <code class="wrap">int Rank_GetMaxXp()</code><br>int() |
| `StatsTransfer_IsValidForController` | 0x875DAF0 | 0x7FF72531DAF0 | <code class="wrap">bool StatsTransfer_IsValidForController(unsigned int controller)</code><br>bool(unsigned ctrl) |
| `Unlockables_Begin` | 0x756F280 | 0x7FF72412F280 |  |
| `Unlockables_End` | 0x757C6B2 | 0x7FF72413C6B2 |  |

## PlayerData, stats and progression: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Ddl_CopyInstanceToInstance` | 0x8760A90 | 0x7FF725320A90 |  |
| `Ddl_IsInstanceWritable` | 0xCABC390 | 0x7FF72967C390 |  |
| `Ddl_WriteBits` | 0xCAC0C50 | 0x7FF729680C50 |  |
| `LiveStats_CreateLiveUserStatsInstance` | 0x9EBC600 | 0x7FF726A7C600 |  |
| `LiveStats_PathProgressionWeaponXp` | 0xAA04D10 | 0x7FF7275C4D10 |  |
| `LiveStats_RecordMatchStatsIfEnabled` | 0x702F590 | 0x7FF723BEF590 |  |
| `LiveStorage_ApplyStatDeltaMsg_cand` | 0x875FE60 | 0x7FF72531FE60 |  |
| `LiveStorage_LuiAarRecap` | 0x87613C0 | 0x7FF7253213C0 |  |
| `LiveStorage_OnStatsMapRead_cand` | 0x8761910 | 0x7FF725321910 |  |
| `PlayerData_Init` | 0xAA017C0 | 0x7FF7275C17C0 |  |
| `PlayerData_ResetControllerStore` | 0xA9FF690 | 0x7FF7275BF690 |  |
| `PlayerDataStorage_DwUser_IsAvailable` | 0xB83FD20 | 0x7FF7283FFD20 |  |
| `PlayerDataStorage_EnqueueOp` | 0xB5B3EB0 | 0x7FF728173EB0 |  |
| `Progression_IsItemOptionLocked` | 0x757AC20 | 0x7FF72413AC20 |  |
| `Unlockables_GetItemRow` | 0x7572DD0 | 0x7FF724132DD0 |  |

## Sound: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `SND_ApplyListenerRoom` | 0xC978990 | 0x7FF729538990 |  |
| `SND_CurrentRoomOverridesTriton` | 0xC978790 | 0x7FF729538790 |  |
| `SND_FindDefaultRoom` | 0xC660F40 | 0x7FF729220F40 |  |
| `SND_FindReverb` | 0xCA3E620 | 0x7FF7295FE620 |  |
| `SND_FindRoom` | 0xC661920 | 0x7FF729221920 |  |
| `SND_GetRoomReverb` | 0xBC58B70 | 0x7FF728818B70 |  |
| `SND_PlayRoomLoop` | 0xC9787D0 | 0x7FF7295387D0 |  |
| `SND_RoomRingoffSide` | 0xC9786E0 | 0x7FF7295386E0 |  |
| `SND_SetListenerRoom` | 0xC978940 | 0x7FF729538940 |  |
| `SND_SetupReverbBuses` | 0xAF52BF0 | 0x7FF727B12BF0 |  |
| `SND_SetVoiceSends` | 0xBC53350 | 0x7FF728813350 |  |
| `SND_Triton_LoadBankAcoustics` | 0xCDD2B50 | 0x7FF729992B50 |  |
| `SND_Triton_QueryEmitter` | 0xCDD2CB0 | 0x7FF729992CB0 |  |
| `SND_Triton_ReverbActive` | 0xCDD33B0 | 0x7FF7299933B0 |  |
| `SND_Triton_ReverbBusGains` | 0xCDD21D0 | 0x7FF7299921D0 |  |
| `SND_UpdateAmbientRooms` | 0xC978BE0 | 0x7FF729538BE0 |  |
| `SND_UpdateVoice3D` | 0xBC618E0 | 0x7FF7288218E0 |  |
| `SND_VoiceDryLevel` | 0xBC58E20 | 0x7FF728818E20 |  |
| `SND_VoiceWetLevel` | 0xBC5B2F0 | 0x7FF72881B2F0 |  |
| `TritonRuntime_GetOutdoornessAtListener` | 0xD15AAC0 | 0x7FF729D1AAC0 |  |

## AI and navigation: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `AI_AddNavMeshCellsToWorld_cand` | 0x6FDD100 | 0x7FF723B9D100 |  |
| `AI_InitNavWorld_cand` | 0x6FED970 | 0x7FF723BAD970 |  |
| `AI_LoadNavmeshForMap` | 0x6FDD5E0 | 0x7FF723B9D5E0 |  |
| `hkaiNavMesh_GetOrBuildFaceIterator_cand` | 0xCF96F50 | 0x7FF729B56F50 |  |
| `Nav_BuildMovingPlatformNavMesh_cand` | 0x835AFE0 | 0x7FF724F1AFE0 |  |
| `Nav_FaceMaterialFlags_cand` | 0x9EC3400 | 0x7FF726A83400 |  |
| `Nav_TagfileBlobFromStreamBuffer_cand` | 0x9C11500 | 0x7FF7267D1500 |  |
| `Tac_ClosestPointNear_cand` | 0x9409910 | 0x7FF725FC9910 |  |

## World, collision and rendering

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `R_BeginRemoteScreenUpdate` | 0xB5F0940 | 0x7FF7281B0940 |  |
| `R_EndRemoteScreenUpdate` | 0xB5FA620 | 0x7FF7281BA620 |  |
| `R_InitWorld_cand` | 0xB3A4E50 | 0x7FF727F64E50 | void() |
| `R_RemoteScreenUpdateAllow` | 0xB5F59C0 | 0x7FF7281B59C0 | <code class="wrap">void R_RemoteScreenUpdateAllow(bool allow)</code><br>(bool) |

## World, collision and rendering: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `CM_CellRecord_GetClipModel_cand` | 0xC61F040 | 0x7FF7291DF040 |  |
| `CM_ForEachStreamedCell_cand` | 0x1A68130 | 0x7FF71E628130 |  |
| `CM_Hull_GetFaceSurface` | 0xCA351A0 | 0x7FF7295F51A0 |  |
| `CM_Hull_TraceCapsule` | 0xCA332C0 | 0x7FF7295F32C0 |  |
| `CM_RegisterDynEntSettingsAssets` | 0xC4610E0 | 0x7FF7290210E0 |  |
| `CM_TerrainTile_TraceQuad` | 0xBC02270 | 0x7FF7287C2270 |  |
| `CM_Tree_RemapFaceSurfaces` | 0xC6EC0F0 | 0x7FF7292AC0F0 |  |
| `CM_Tree_TraceCallback` | 0xCA9C330 | 0x7FF72965C330 |  |
| `CM_TreeHull_Trace` | 0xCA35DC0 | 0x7FF7295F5DC0 |  |
| `CM_TriggerModelTouch` | 0xC6BE210 | 0x7FF72927E210 |  |
| `CM_World_PointContents_cand` | 0xC82AB90 | 0x7FF7293EAB90 |  |
| `CM_World_Trace_cand` | 0xC823270 | 0x7FF7293E3270 |  |
| `Com_CopyPrimaryLightsToCG_cand` | 0xCA30520 | 0x7FF7295F0520 |  |
| `Com_FindComWorld_cand` | 0xCA304A0 | 0x7FF7295F04A0 |  |
| `DynEnt_Create_cand` | 0x74AD7A0 | 0x7FF72406D7A0 |  |
| `Image_CreateResident_cand` | 0xC553680 | 0x7FF729113680 |  |
| `Image_GetMipDataSize` | 0xC661E20 | 0x7FF729221E20 |  |
| `Image_PostLoad_cand` | 0xC554050 | 0x7FF729114050 |  |
| `LevelLoad_RegisterStreamGroups_cand` | 0x9405F90 | 0x7FF725FC5F90 |  |
| `Light_Copy688_cand` | 0x8C68760 | 0x7FF725828760 |  |
| `Lighting_LinkStreamedTextureA_cand` | 0xC8D38A0 | 0x7FF7294938A0 |  |
| `Lighting_LinkStreamedTextureB_cand` | 0xC8D38B0 | 0x7FF7294938B0 |  |
| `Lighting_StreamedTexture_Install_cand` | 0xC8D39B0 | 0x7FF7294939B0 |  |
| `LightingState_Copy` | 0x8C790F0 | 0x7FF7258390F0 |  |
| `R_BeginLoadWorld` | 0xB3A4DB0 | 0x7FF727F64DB0 |  |
| `R_CollectVisibleProjectedDecals_cand` | 0x9ED9E70 | 0x7FF726A99E70 |  |
| `R_Image_MarkUsed_cand` | 0xA2C8130 | 0x7FF726E88130 |  |
| `R_Lighting_FindImageSetAtPoint_cand` | 0x8CA4850 | 0x7FF725864850 |  |
| `R_LoadWorldFrame` | 0xB3A5100 | 0x7FF727F65100 |  |
| `R_SetupFrameLightingImageSet_cand` | 0x8CC6C80 | 0x7FF725886C80 |  |
| `R_SunShadowTreeConstants_cand` | 0xC8B5900 | 0x7FF729475900 |  |
| `StreamKey_IsReady_cand` | 0xC425F30 | 0x7FF728FE5F30 |  |
| `StreamKeyType2_Install_cand` | 0xC8D3880 | 0x7FF729493880 |  |
| `World_LoadByMapName_cand` | 0xC48A850 | 0x7FF72904A850 |  |
| `XCollision_GetContents` | 0xC82FBD0 | 0x7FF7293EFBD0 |  |
| `XModel_GetDrawableLod_cand` | 0xC82F5B0 | 0x7FF7293EF5B0 |  |
| `XModel_LodForDistance_cand` | 0xC82F940 | 0x7FF7293EF940 |  |
| `XModel_PrefetchLods_cand` | 0x9CA9680 | 0x7FF726869680 |  |
| `XModel_SelectLod_cand` | 0xC8303F0 | 0x7FF7293F03F0 |  |
| `XModelMesh_GetIndex` | 0x97294C0 | 0x7FF7262E94C0 |  |
| `XModelMesh_IsReadyToDraw_cand` | 0xC425EB0 | 0x7FF728FE5EB0 |  |
| `XModelMesh_IsStreamed` | 0xC830860 | 0x7FF7293F0860 |  |

## Game entities and spawning: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `CG_RegisterAmbientRoomTrigger` | 0x8209370 | 0x7FF724DC9370 |  |
| `CG_SpawnClientTrigger` | 0xB3358D0 | 0x7FF727EF58D0 |  |
| `CG_SpawnMapTriggersAndEntities` | 0xB34E890 | 0x7FF727F0E890 |  |
| `CG_UpdateAmbientRooms_cand` | 0x81C9090 | 0x7FF724D89090 |  |
| `CG_ZBarrier_SetupPieces_cand` | 0xB1262D0 | 0x7FF727CE62D0 |  |
| `G_InitGame_LevelSetup_cand` | 0x3D53500 | 0x7FF720913500 |  |
| `G_RegisterZBarriers_cand` | 0x3D52790 | 0x7FF720912790 |  |
| `G_SetModel_cand` | 0x71E8F70 | 0x7FF723DA8F70 |  |
| `G_SpawnMapEntities_cand` | 0x736BE30 | 0x7FF723F2BE30 |  |
| `G_SpawnMapEntity_cand` | 0x65113A0 | 0x7FF7230D13A0 |  |
| `G_SpawnTriggers` | 0x736C3B0 | 0x7FF723F2C3B0 |  |
| `SP_ScriptModel_cand` | 0xB8CECA0 | 0x7FF72848ECA0 |  |
| `SP_ZBarrier_cand` | 0xBB925D0 | 0x7FF7287525D0 |  |
| `VehNode_SpawnFromMapEnt_cand` | 0x714A600 | 0x7FF723D0A600 |  |
| `ZBarrier_InitAnimTree_cand` | 0x3D4D3A0 | 0x7FF72090D3A0 |  |

## Fastfiles and asset loaders

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `BG_Cache_FindIndex_cand` | 0x9652E90 | 0x7FF726212E90 | i64(u8 table, u64 name) |
| `BG_Cache_Register_cand` | 0x9653DB0 | 0x7FF726213DB0 | size 0x24D |
| `DB_AllocXAssetEntry` | 0xB301310 | 0x7FF727EC1310 | <code class="wrap">void* DB_AllocXAssetEntry(u64 type, u64 zone)</code><br>DB_AllocXAssetEntry(type, zone) drops with 0x3F6FDE09 when the global entry list is empty and 0xE554F200 when g_xassetPools[type] has no free item. |
| `DB_ExpandZoneVariants` | 0xCA32490 | 0x7FF7295F2490 | <code class="wrap">int DB_ExpandZoneVariants(XZoneInfo* zones, int count, char* names, XZoneInfo* out, int max)</code><br>int(zones, count, names[64 each], out[], max) |
| `DB_LoadXAssets` | 0xB304700 | 0x7FF727EC4700 | <code class="wrap">void DB_LoadXAssets(XZoneInfo* zones, u32 count, int freeFlags)</code><br>(XZoneInfo {name, u32 flags, pad}[], count, 0) |
| `DB_LoadXFile_Internal` | 0xAADFC00 | 0x7FF72769FC00 | <code class="wrap">i64 DB_LoadXFile_Internal(i64 a1, i64 a2, const char* zoneName, int a4, void* assetList, void* blocks, u64 a7, int a8, int flags)</code><br>9 args, see above |
| `DB_ReadXFile` | 0xAAE07D0 | 0x7FF7276A07D0 | <code class="wrap">void DB_ReadXFile(void* dst, int size)</code><br>(dst, int size) |
| `DB_ReadXFileString` | 0xAADF470 | 0x7FF72769F470 | <code class="wrap">void DB_ReadXFileString(u8* dst, u32* count)</code><br>(dst, u32* count incl. NUL) |
| `DB_Signature_VerifyZone` | 0xC6ED410 | 0x7FF7292AD410 | <code class="wrap">void DB_Signature_VerifyZone()</code><br>void(); no caller check (prologue checked) |
| `DB_SyncXAssets` | 0xB3050D0 | 0x7FF727EC50D0 | blocks until the queued zones are in |
| `DB_ZoneFileExists` | 0xB302020 | 0x7FF727EC2020 | <code class="wrap">bool DB_ZoneFileExists(const char* zoneName)</code><br>bool(name): "&lt;zone dir&gt;/&lt;name&gt;.ff" through the search paths |
| `DecryptString` | 0xC990AE0 | 0x7FF729550AE0 | <code class="wrap">char* DecryptString(char* s)</code><br>DecryptString(char* s) -&gt; char*. |
| `FS_AddSearchPath` | 0xCA86DC0 | 0x7FF729646DC0 | <code class="wrap">void FS_AddSearchPath(const char* path, int priority, int device, u64 unused)</code><br>(path, priority, device, 0); indexes the dir now |
| `FS_OpenFileRead` | 0xC83C9A0 | 0x7FF7293FC9A0 | <code class="wrap">void* FS_OpenFileRead(const char* path, int mode, int device)</code><br>handle(path, mode, device); 3-arg wrapper, 13 callers |
| `Load_XAsset` | 0x1C37560 | 0x7FF71E7F7560 | <code class="wrap">i64 Load_XAsset(char atStreamStart, u8* asset)</code><br>(atStreamStart, XAsset*) |
| `Load_XAsset_Preload` | 0x1CA7350 | 0x7FF71E867350 | same signature |
| `MapPreload_StartZoneRead` | 0xAF72E60 | 0x7FF727B32E60 | <code class="wrap">u64 MapPreload_StartZoneRead(const char* mapName, u64 a2, u64 a3, u64 a4)</code><br>(name, 3 unused pass-through args) |
| `MapTable_FindEntryByHash` | 0xC1BB040 | 0x7FF728D7B040 | <code class="wrap">void* MapTable_FindEntryByHash(u64 mapHash)</code><br>entry*(u64 map name hash) |
| `MapTable_GetMapFlags` | 0xC1BB1D0 | 0x7FF728D7B1D0 | <code class="wrap">u32 MapTable_GetMapFlags(const char* mapName)</code><br>u32(const char* map), ~0 = none |

## Fastfiles and asset loaders: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `BG_Cache_RegisterAll_cand` | 0x9653850 | 0x7FF726213850 |  |
| `BuildKv_KeyHash_cand` | 0xCA3C9B0 | 0x7FF7295FC9B0 |  |
| `BuildKv_Register_cand` | 0xCAC1490 | 0x7FF729681490 |  |
| `DB_AllocStreamPos` | 0xCAAEB50 | 0x7FF72966EB50 |  |
| `DB_AllocXBlocks` | 0xCA16020 | 0x7FF7295D6020 |  |
| `DB_AnyPreloadZoneFailed` | 0xB3013E0 | 0x7FF727EC13E0 |  |
| `DB_ConvertOffsetToAlias` | 0xCAA8CC0 | 0x7FF729668CC0 |  |
| `DB_ConvertOffsetToPointer` | 0xCAA8D00 | 0x7FF729668D00 |  |
| `DB_ConvertZoneScriptString` | 0xCAAF1E0 | 0x7FF72966F1E0 |  |
| `DB_DecompressBlockJob` | 0xAADF6E0 | 0x7FF72769F6E0 |  |
| `DB_EnumXAssetsInZones_cand` | 0xB301F00 | 0x7FF727EC1F00 |  |
| `DB_FillCompressedBlocks` | 0xAAE2050 | 0x7FF7276A2050 |  |
| `DB_FindXAssetHeader` | 0xB3021F0 | 0x7FF727EC21F0 | Bound by signature. The asset lookup by type and name hash. For some types a missing asset is fatal inside it. |
| `DB_FinishPreloadedZone` | 0xAADF990 | 0x7FF72769F990 |  |
| `DB_ForEachXAssetEntry_cand` | 0xB2FF560 | 0x7FF727EBF560 |  |
| `DB_GetZonePriority` | 0xB302F50 | 0x7FF727EC2F50 |  |
| `DB_Image_LinkCallback` | 0xCA2D880 | 0x7FF7295ED880 |  |
| `DB_InitStreams` | 0xCAAEBA0 | 0x7FF72966EBA0 |  |
| `DB_InsertOverrideEntry` | 0xB301210 | 0x7FF727EC1210 |  |
| `DB_InsertPointer` | 0xCAAECC0 | 0x7FF72966ECC0 |  |
| `DB_LinkMissingReference` | 0xB301860 | 0x7FF727EC1860 |  |
| `DB_LinkNavmeshAsset` | 0xBE7E1F0 | 0x7FF728A3E1F0 |  |
| `DB_LinkSoundBank` | 0xBE7E290 | 0x7FF728A3E290 |  |
| `DB_LinkXAssetEntry` | 0xB303AA0 | 0x7FF727EC3AA0 |  |
| `DB_LoadXFile_Finish` | 0xAAE0C30 | 0x7FF7276A0C30 |  |
| `DB_LoadXFileData` | 0xCAA8D60 | 0x7FF729668D60 |  |
| `DB_LoadZone` | 0xB304370 | 0x7FF727EC4370 |  |
| `DB_OpenZonePackages_cand` | 0xC6CAB20 | 0x7FF72928AB20 |  |
| `DB_Patch_VcdiffDecodeWindow` | 0xCA4AAD0 | 0x7FF72960AAD0 |  |
| `DB_PopStreamPos` | 0xCAAEE30 | 0x7FF72966EE30 |  |
| `DB_PostLoadFrame_ApplyOverrides` | 0xB304A30 | 0x7FF727EC4A30 |  |
| `DB_ProcessLoadQueue` | 0xB303E50 | 0x7FF727EC3E50 |  |
| `DB_PushPointerFixup` | 0xCAAF010 | 0x7FF72966F010 |  |
| `DB_PushStreamPos` | 0xCAAEEB0 | 0x7FF72966EEB0 |  |
| `DB_QueueZoneLoads_cand` | 0xB301B40 | 0x7FF727EC1B40 |  |
| `DB_ReadFastfileHeaderTLV` | 0xAAE1C30 | 0x7FF7276A1C30 |  |
| `DB_ReadZoneFileHeader` | 0xB301510 | 0x7FF727EC1510 |  |
| `DB_ResolveScriptStringIndex` | 0xCAAF0E0 | 0x7FF72966F0E0 |  |
| `DB_ResolveScriptStringIndexLazy` | 0xCAAF070 | 0x7FF72966F070 |  |
| `DB_SaveStreamPositions_Preload` | 0xCAAEF90 | 0x7FF72966EF90 |  |
| `DB_ShouldLoadStreamedBlock` | 0x9CAC7C0 | 0x7FF72686C7C0 |  |
| `DB_SwapXAssetHeaders` | 0xB304F80 | 0x7FF727EC4F80 |  |
| `DB_TamperResponse_CorruptEntryFreeList` | 0xB301410 | 0x7FF727EC1410 |  |
| `DB_UnloadMarkedZones` | 0xB302760 | 0x7FF727EC2760 |  |
| `DB_ZoneMem_FreeZone` | 0xA03FDD0 | 0x7FF726BFFDD0 |  |
| `Finish_ClipMap` | 0x1C7C3E0 | 0x7FF71E83C3E0 |  |
| `Load_BgcacheAsset` | 0x1C0A8C0 | 0x7FF71E7CA8C0 |  |
| `Load_ClipMap` | 0x1C3A1D0 | 0x7FF71E7FA1D0 |  |
| `Load_ClipMapAsset` | 0x1C3A100 | 0x7FF71E7FA100 |  |
| `Load_ClipMapStruct992` | 0x1C13840 | 0x7FF71E7D3840 |  |
| `Load_ClipMapTerrainEntries` | 0x1C2AB70 | 0x7FF71E7EAB70 |  |
| `Load_ComMapAsset` | 0x1C11080 | 0x7FF71E7D1080 |  |
| `Load_ComWorld` | 0x1C10EE0 | 0x7FF71E7D0EE0 |  |
| `Load_CpuOcclusionData_cand` | 0x1C116F0 | 0x7FF71E7D16F0 |  |
| `Load_CpuOcclusionDataAsset` | 0x1C119D0 | 0x7FF71E7D19D0 |  |
| `Load_Districts` | 0x1C14440 | 0x7FF71E7D4440 |  |
| `Load_DistrictsAsset` | 0x1C145B0 | 0x7FF71E7D45B0 |  |
| `Load_EntitylistAsset` | 0x1C150F0 | 0x7FF71E7D50F0 |  |
| `Load_FxAsset` | 0x1C16B40 | 0x7FF71E7D6B40 |  |
| `Load_GameMapAsset` | 0x1C18420 | 0x7FF71E7D8420 |  |
| `Load_GameWorld` | 0x1C18390 | 0x7FF71E7D8390 |  |
| `Load_GameWorldPath_cand` | 0x1C23B60 | 0x7FF71E7E3B60 |  |
| `Load_GfxBlob3` | 0x1C18D80 | 0x7FF71E7D8D80 |  |
| `Load_GfxImage` | 0x1C195E0 | 0x7FF71E7D95E0 |  |
| `Load_GfxImagePixels` | 0x1C196C0 | 0x7FF71E7D96C0 |  |
| `Load_GfxImagePtrArray` | 0x1C19850 | 0x7FF71E7D9850 |  |
| `Load_GfxMapAsset` | 0x1C1C6B0 | 0x7FF71E7DC6B0 |  |
| `Load_GfxPixels56` | 0x1C1A0D0 | 0x7FF71E7DA0D0 |  |
| `Load_GfxWorld` | 0x1C1B2A0 | 0x7FF71E7DB2A0 |  |
| `Load_GfxWorldDraw` | 0x1C1BEA0 | 0x7FF71E7DBEA0 |  |
| `Load_GfxWorldDrawMaterials` | 0x1C1AB80 | 0x7FF71E7DAB80 |  |
| `Load_GfxWorldRuntimeBuffers` | 0x1C1BDE0 | 0x7FF71E7DBDE0 |  |
| `Load_GlassesAsset` | 0x1C1CD30 | 0x7FF71E7DCD30 |  |
| `Load_GrouplodmodelAsset` | 0x1C19410 | 0x7FF71E7D9410 |  |
| `Load_ImageAsset` | 0x1C197A0 | 0x7FF71E7D97A0 |  |
| `Load_ImpactsfxtableAsset` | 0x1C17250 | 0x7FF71E7D7250 |  |
| `Load_ImpactsoundstableAsset` | 0x1C2A280 | 0x7FF71E7EA280 |  |
| `Load_KeyValuePairs` | 0x1C1D5D0 | 0x7FF71E7DD5D0 |  |
| `Load_KeyvaluepairsAsset` | 0x1C1D6A0 | 0x7FF71E7DD6A0 |  |
| `Load_Klf` | 0x1C175A0 | 0x7FF71E7D75A0 |  |
| `Load_KlfAsset` | 0x1C17340 | 0x7FF71E7D7340 |  |
| `Load_KlfEntryArray_cand` | 0x1C173F0 | 0x7FF71E7D73F0 |  |
| `Load_Lighting` | 0x1C1DE70 | 0x7FF71E7DDE70 |  |
| `Load_LightingImageSet128Array_cand` | 0x1C1AFD0 | 0x7FF71E7DAFD0 |  |
| `Load_LightingLightArray_cand` | 0x1C10E10 | 0x7FF71E7D0E10 |  |
| `Load_LightingStreamedTexture104_cand` | 0x1C1A810 | 0x7FF71E7DA810 |  |
| `Load_LightingVolumeArray` | 0x1C1A940 | 0x7FF71E7DA940 |  |
| `Load_LocalizeentryAsset` | 0x1C1EAF0 | 0x7FF71E7DEAF0 |  |
| `Load_MapEntityArray` | 0x1C1E900 | 0x7FF71E7DE900 |  |
| `Load_Material` | 0x1C1FFB0 | 0x7FF71E7DFFB0 |  |
| `Load_MaterialAsset` | 0x1C20960 | 0x7FF71E7E0960 |  |
| `Load_MaterialHandleArray` | 0x1C20A10 | 0x7FF71E7E0A10 |  |
| `Load_NavMeshData` | 0x1C21EE0 | 0x7FF71E7E1EE0 |  |
| `Load_NavvolumeAsset` | 0x1C22120 | 0x7FF71E7E2120 |  |
| `Load_NavVolumeData` | 0x1C22070 | 0x7FF71E7E2070 |  |
| `Load_PhysconstraintsAsset` | 0x1C24290 | 0x7FF71E7E4290 |  |
| `Load_PhyspresetAsset` | 0x1C24340 | 0x7FF71E7E4340 |  |
| `Load_RawfileAsset` | 0x1C27870 | 0x7FF71E7E7870 |  |
| `Load_SanimAsset` | 0x1C1A300 | 0x7FF71E7DA300 |  |
| `Load_ScriptbundleAsset` | 0x1C282D0 | 0x7FF71E7E82D0 |  |
| `Load_ScriptStringList` | 0x1C28A80 | 0x7FF71E7E8A80 |  |
| `Load_SettingsTree` | 0x1C27E80 | 0x7FF71E7E7E80 |  |
| `Load_SoundAcousticsAsset` | 0x1C294F0 | 0x7FF71E7E94F0 |  |
| `Load_SoundAliasArray` | 0x1C295A0 | 0x7FF71E7E95A0 |  |
| `Load_SoundAliasModifier` | 0x1C29730 | 0x7FF71E7E9730 |  |
| `Load_SoundAliasModifierAsset` | 0x1C298A0 | 0x7FF71E7E98A0 |  |
| `Load_SoundAssetAsset` | 0x1C29950 | 0x7FF71E7E9950 |  |
| `Load_SoundBank` | 0x1C29A80 | 0x7FF71E7E9A80 |  |
| `Load_SoundBankAsset` | 0x1C29D50 | 0x7FF71E7E9D50 |  |
| `Load_SoundDuckAsset` | 0x1C2A1C0 | 0x7FF71E7EA1C0 |  |
| `Load_StaticlevelfxlistAsset` | 0x1C2BF40 | 0x7FF71E7EBF40 |  |
| `Load_StreamerWorld` | 0x1C2D3B0 | 0x7FF71E7ED3B0 |  |
| `Load_StreamerworldAsset` | 0x1C2D870 | 0x7FF71E7ED870 |  |
| `Load_StreamkeyAsset` | 0x1C2CFC0 | 0x7FF71E7ECFC0 |  |
| `Load_StreamKeyData` | 0x1C2CF00 | 0x7FF71E7ECF00 |  |
| `Load_TechsetAsset` | 0x1C21920 | 0x7FF71E7E1920 |  |
| `Load_TechsetAsset_Preload` | 0x1C92EB0 | 0x7FF71E852EB0 |  |
| `Load_TerrainGfx` | 0x1C2B650 | 0x7FF71E7EB650 |  |
| `Load_TerraingfxAsset` | 0x1C2BBC0 | 0x7FF71E7EBBC0 |  |
| `Load_TriggerList` | 0x1C2EEE0 | 0x7FF71E7EEEE0 |  |
| `Load_TriggerlistAsset` | 0x1C2F010 | 0x7FF71E7EF010 |  |
| `Load_VehicleAsset` | 0x1C31080 | 0x7FF71E7F1080 |  |
| `Load_WinddefAsset` | 0x1C365D0 | 0x7FF71E7F65D0 |  |
| `Load_XanimcurveAsset` | 0x1C368B0 | 0x7FF71E7F68B0 |  |
| `Load_XAssetHeader` | 0x1C375A0 | 0x7FF71E7F75A0 |  |
| `Load_XCollision` | 0x1C37FE0 | 0x7FF71E7F7FE0 |  |
| `Load_XcollisionAsset` | 0x1C381B0 | 0x7FF71E7F81B0 |  |
| `Load_XCollisionData` | 0x1C38260 | 0x7FF71E7F8260 |  |
| `Load_XCollisionTree` | 0x1C39A90 | 0x7FF71E7F9A90 |  |
| `Load_XModel` | 0x1C38420 | 0x7FF71E7F8420 |  |
| `Load_XmodelAsset` | 0x1C38D50 | 0x7FF71E7F8D50 |  |
| `Load_XModelMesh` | 0x1C38A50 | 0x7FF71E7F8A50 |  |
| `Load_XmodelmeshAsset` | 0x1C38BF0 | 0x7FF71E7F8BF0 |  |
| `Load_XModelMeshPart` | 0x1C39290 | 0x7FF71E7F9290 |  |
| `Load_XModelMeshSurfaceData` | 0x1C393B0 | 0x7FF71E7F93B0 |  |
| `Load_XModelPtrArray` | 0x1C38E00 | 0x7FF71E7F8E00 |  |
| `Load_XSkeleton` | 0x1C38EB0 | 0x7FF71E7F8EB0 |  |
| `Load_XskeletonAsset` | 0x1C39180 | 0x7FF71E7F9180 |  |
| `Load_XStringInline` | 0xCAA8E00 | 0x7FF729668E00 |  |
| `Load_ZbarrierAsset` | 0x1C399E0 | 0x7FF71E7F99E0 |  |
| `Load_ZBarrierBoardArray` | 0x1C395C0 | 0x7FF71E7F95C0 |  |
| `Load_ZBarrierDef` | 0x1C39910 | 0x7FF71E7F9910 |  |
| `MapPreload_Frame` | 0xBF77700 | 0x7FF728B37700 |  |
| `MapPreload_LoadPreloaded` | 0xBF77610 | 0x7FF728B37610 |  |
| `MapPreload_LoadQueued` | 0xAF72B30 | 0x7FF727B32B30 |  |
| `MapPreload_OnLoadXAssets` | 0xAF73190 | 0x7FF727B33190 |  |
| `MapPreload_SessionFrame` | 0xAF73430 | 0x7FF727B33430 |  |

## Dvars

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Dvar_ApplyValueInternal` | 0xC0B8DB0 | 0x7FF728C78DB0 | <code class="wrap">void Dvar_ApplyValueInternal(uintptr* dvar, const void* value, unsigned int source)</code><br>String dvar writes, the way Dvar_ApplyServerDvarPacket (0x7FF728C73A80) applies a PubVar: Dvar_StringToValue(out32, dvar-&gt;type, &dvar-&gt;domain (+32, 16 B), text) builds the 32-byte value, including the obfuscated check word ... |
| `Dvar_GetBool` | 0x1A68F50 | 0x7FF71E628F50 | <code class="wrap">bool Dvar_GetBool(void* dvar)</code><br>bool(dvar*) |
| `Dvar_StringToValue` | 0xC0BA580 | 0x7FF728C7A580 | <code class="wrap">void* Dvar_StringToValue(void* value, int type, const void* domain, const char* text)</code><br>String dvar writes, the way Dvar_ApplyServerDvarPacket (0x7FF728C73A80) applies a PubVar: Dvar_StringToValue(out32, dvar-&gt;type, &dvar-&gt;domain (+32, 16 B), text) builds the 32-byte value, including the obfuscated check word ... |

## Dvars: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Dvar_ApplyServerDvarPacket` | 0xC0B3A80 | 0x7FF728C73A80 |  |
| `Dvar_CanSetValue` | 0xC0ACBB0 | 0x7FF728C6CBB0 |  |
| `Dvar_FindVar` | 0xC0B2090 | 0x7FF728C72090 | <code class="wrap">uintptr* Dvar_FindVar(u64 nameHash)</code> |
| (Dvar_FindVar's thunk) | 0xC0B2230 | 0x7FF728C72230 | An E9 jump to Dvar_FindVar. Hook the implementation, not this. |
| (Dvar_GetInt's thunk) | 0xE82540 | 0x7FF71DA42540 | An Arxan split thunk that dispatches on the return address. Calling it from another module faults. |
| `Dvar_RegisterInt` | 0xC0C7360 | 0x7FF728C87360 |  |
| `Dvar_SetAllowServerFlaggedWrites` | 0xC0B5A80 | 0x7FF728C75A80 | One instruction: mov g_dvarAllowServerFlaggedWrites, cl; ret. |
| `Dvar_SetBoolFromSource` | 0xC0B5580 | 0x7FF728C75580 | <code class="wrap">void Dvar_SetBoolFromSource(uintptr* dvar, bool value, int source)</code> |
| `Dvar_SetInt_cand` | 0xC0B7B90 | 0x7FF728C77B90 | The int setter with the type switch the client's comments describe: it tests its value as 32 bits. It is the second of the three functions the Dvar_SetIntFromSource signature matches. |
| `Dvar_SetIntFromSource` | 0xC0B7530 | 0x7FF728C77530 | <code class="wrap">void Dvar_SetIntFromSource(uintptr* dvar, int value, int source)</code><br>Bound by signature: the first of three matches in the dump. Switches on the dvar's type. |

## Common, session mode and boot

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Com_GetTuVersion` | 0xCA2FA70 | 0x7FF7295EFA70 | int(); BuildKv "tu_version" |
| `Com_SessionMode_GetStr` | 0xC1BBD60 | 0x7FF728D7BD60 |  |
| `Com_SessionMode_IsProgressionExemptContext` | 0xC1BC2D0 | 0x7FF728D7C2D0 | <code class="wrap">bool Com_SessionMode_IsProgressionExemptContext()</code><br>bool() |
| `Loc_GetLanguage` | 0xBE97A60 | 0x7FF728A57A60 | int(); language dvar |
| `Loc_GetLanguagePrefix` | 0xBE97CE0 | 0x7FF728A57CE0 | <code class="wrap">const char* Loc_GetLanguagePrefix(unsigned int language)</code><br>const char*(lang), e.g. "en_" |

## Common, session mode and boot: named in the notes

| Name | RVA | IDA address | Signature or note |
|---|---|---|---|
| `Com_FormatHash64` | 0xC48A3F0 | 0x7FF72904A3F0 |  |
| `Com_IsGameServerRunning` | 0x5789350 | 0x7FF722349350 |  |
| `Com_SessionMode_GetGameMode` | 0xC1BC100 | 0x7FF728D7C100 |  |
| `Com_SessionMode_GetNetworkMode` | 0xC1BC280 | 0x7FF728D7C280 |  |
| `Com_SessionMode_IsOnline` | 0xC1BC4B0 | 0x7FF728D7C4B0 |  |
| `Com_SessionMode_SetGameMode` | 0xC1BC610 | 0x7FF728D7C610 | Writes the gameMode bits (0-3) of g_sessionModePacked. The signature the client binds under the name Com_SessionMode_SetNetworkMode matches this function, not the one at RVA 0xC1BC630. |
| `Com_SessionMode_SetMatchType` | 0xC1BC5F0 | 0x7FF728D7C5F0 | Writes the matchType bits (12-15) of g_sessionModePacked. Sits right before the two other setters. |
| `Com_SessionMode_SetNetworkMode` | 0xC1BC630 | 0x7FF728D7C630 | <code class="wrap">void Com_SessionMode_SetNetworkMode(int mode)</code> |
| (return gadget for ArxanCall thunks) | 0x4F3D2C | 0x7FF71D0B3D2C | The return point after an in-image call: add rsp,28h; retn. |

<!-- generated by tools/gen_functions.py from cw-mod 36b1f18 (client/game/dump_anchors.hpp, client/game/function_types.hpp, and the names written next to an address in the notes and comments). Do not edit by hand. -->

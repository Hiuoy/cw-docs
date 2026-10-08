# Auth

> The first Demonware stage: one HTTPS request, one signed JSON reply. This page gives the reply's contract in the order the client checks it, the ticket inside it, and how the login gets there without Battle.net. **Status:** Done, in game.

## In short

- The login state machine has several "flows". Flow 9, studio auth, goes straight to Demonware and skips the Battle.net token step. cw-mod selects it.
- Studio auth needs a signed token the retail build cannot make. cw-mod hands the state machine an unsigned one, which only its own server will ever read.
- The auth reply is JSON with a signature header. The parser checks its fields in a fixed order, and **every number is a string**.
- The reply carries two 128-byte tickets. They must be **plaintext**: this build's "decrypt" step is a function that does nothing.

## Getting to the request

| Gate | Normal answer | What cw-mod does |
|---|---|---|
| The login driver runs at all | Needs `nodw` false, the connect-mode dvar at 1, controller 0, a "login allowed" byte, and first-party presence | Clears `nodw` at the right moment. See [The boot profile](/re/client/boot-profile.md). |
| First-party presence | False: no Battle.net sign-in | A detour answers true to the login driver. See [After login](/re/dwemu/post-login.md). |
| `Dw_GetLoginFlow` | The Battle.net flow | Returns **9**. All 12 callers are login code, so there is no side effect. |
| `DwLogin_BuildStudioToken` | Fails: the token is signed with a studio key the retail build does not carry. The log says "Studio auth login failed to build token" (code 26). | Calls the original; on failure writes its own token into the output buffer and returns success |

The substituted token is a JWT with the algorithm "none": two base64url parts and an empty signature. The engine's own token code can produce that shape. Its claims carry two values from [cw-mod.json](/guide/settings.md):

| Claim | From | Becomes |
|---|---|---|
| `name` | `"name"` | The user name in the ticket: the name shown in game |
| `xuid` | `"xuid"` | The user id in the ticket: the id other PCs see |

## The request

`POST https://<auth host>/auth/`, built by `DwAuth_BuildRequest`. A real one, with values shortened:

```text
{"auth_task":"94","iv_seed":"1152714428","title_id":"5836","extra_data":"{\"token\":\"<jwt>\"}", ...}
```

`extra_data` is a JSON document **inside a string**. The reply uses the same convention.

## The reply contract

`DwAuth_ParseReply` checks in this order. Each failure has its own log text.

| # | Field | Rule | If wrong |
|---|---|---|---|
| 1 | `auth_task` | The request's value **plus 1**: 94 gives 95 on flow 9 | "Invalid or No Task ID" |
| 2 | `code` | 700, "success, tickets follow". Any other code returns here, **before** the signature is looked at. | The code is reported |
| 3 | `X-Signature` header | RSASSA-PSS over the raw body. See [Keys](/re/dwemu/keys.md). | Signature failure |
| 4 | `extra_data` | A string of at most 5,120 bytes holding JSON, which must hold a string `extended_data` of at most 4,097 bytes. **Mandatory.** | "Auth task reply contains invalid data" |
| 5 | `client_ticket`, `server_ticket` | Base64 of exactly 128 bytes each | "Auth ticket decryption error" (status 25) |

The other fields the server sends:

| Field | Value | Why |
|---|---|---|
| `iv_seed` | The request's, **echoed as the same text** | It also feeds the LSG key schedule. Any change of spelling would give the two sides different keys, and the failure would show two stages later. |
| `lsg_endpoint` | A bare host, `127.0.0.1` | The port is fixed at 3074 inside the client. A `:port` suffix is read as part of the host name. |
| `crossplay_enabled` | false | Selects the legacy path, which skips the cross-play services |
| `loginqueue_enabled` | false | |
| `account_type` | `"0"` | |

The content of `extended_data` is not validated at this point: it is stored in the login config. `{}` passes.

## The ticket

The classic Demonware auth ticket, 128 bytes, packed with no alignment. Read from `bdAuthTicket_Deserialize`, which walks from 0 to 128 with nothing left over.

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | Magic `0xEFBDADDE` (bytes `DE AD BD EF`) |
| 4 | 1 | Type |
| 5 | 4 | Title id (5836) |
| 9 | 4 | Time issued |
| 13 | 4 | Time expires |
| 17 | 8 | License id |
| 25 | 8 | **User id**: the XUID |
| 33 | 64 | User name |
| 97 | 24 | **Session key**: the root of the LSG keys |
| 121 | 7 | Hash fields, zero |

**Why plaintext.** The parser sends a ticket through a decrypt slot only when its first four bytes are **not** the magic. On this build that slot is `DwAuth_StubReturnTrue`: `mov al, 1; ret`. It decrypts nothing, so an encrypted ticket can never reach the magic check. 128 random bytes gave exactly "Auth ticket decryption error". A ticket that starts with the magic is the only form this build can read.

Both tickets hold the **same** session key. The client keeps its copy from `client_ticket` and passes `server_ticket` on to the LSG server untouched.

## The step after: umbrella

With cross-play off, the client then sends `POST /v1.0/tokens/lsg/` to the umbrella host, with its own ticket, the seed and the title id. The reply handler does two things: parse the body as JSON, and check that the root is an object. It reads no field. `200` and `{}` is the whole contract, and the login logs "Got successful Umbrella Legacy Login reply".

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `Dw_GetLoginFlow` | 0xD22BF90 | 0x7FF729DEBF90 | `u64 (void* loginConfig)` | The flow selector |
| `DwLogin_BuildStudioToken` | 0xD22CA90 | 0x7FF729DECA90 | `u8 (void* loginConfig, void* userObj, void* outBuf)` | Writes the token as a C string into a 6,784-byte buffer |
| `DwAuth_BuildRequest` | 0xD22F740 | 0x7FF729DEF740 | | Builds the POST |
| `DwAuth_ParseReply` | 0xD2301E0 | 0x7FF729DF01E0 | | The contract above |
| `DwAuth_VerifyReplySignature` | 0xD230F90 | 0x7FF729DF0F90 | | Check 3 |
| `DwAuth_StubReturnTrue` | 0xD230AA0 | 0x7FF729DF0AA0 | | The "decrypt" slot |
| `bdAuthTicket_Deserialize` | 0xD1742E0 | 0x7FF729D342E0 | | Reads the 128 bytes |
| `Login_SetStatus` | 0xD22C4D0 | 0x7FF729DEC4D0 | `u64 (void* ctx, const char* status, u32 code)` | The state machine's own status line |
| `LiveUser_LoginDriver_Tick` | 0xB379160 | 0x7FF727F39160 | | Runs the login per frame |

## The login transcript

`Login_SetStatus` is called at every step with a text and a code, and the texts go to the game's internal log. cw-mod detours it read-only and copies each line to `client.log`:

```text
(Login) [status ..] Studio auth login detected, starting Auth task
(Login) [status ..] Authenticated to Demonware
(Login) [status ..] Connecting to LSG
(Login) [status 27] Login Complete
```

Status 25 is an error with its reason, 26 a token that could not be built.

## How we found it

- "Invalid or No Task ID": the server echoed the request's task id. Comparing the builder and the parser across flows showed the expected reply id is always the request id plus one.
- The first real request crashed the server: it added 1 to `"94"`, a string. The game showed `HTTP code [0]`, the same as a TLS failure. The server's recorder writes each request from a `finally` block, so the traceback was in the record.
- "Auth task reply contains invalid data" was the missing `extra_data`.
- The ticket: reading the parser showed the decrypt slot's body is three bytes.

## Limits

- The token is unsigned and the tickets are plaintext. That is right for a server on the same PC and nothing else.
- The cross-play login path has a real schema and is not implemented.

## See also

- [Keys](/re/dwemu/keys.md), [The LSG connection](/re/dwemu/lsg.md)
- [Settings](/guide/settings.md): `"name"` and `"xuid"`

<!-- sources: cw-mod tools/dwserver/authserver.py, dwsign.py, client/hooks/impl/game/DwLogin_BuildStudioToken.cpp, client/game/dump_anchors.hpp (Dw_GetLoginFlow, Login_SetStatus, the state-1 gates, studio token), .claude/skills/bocw-reverse-engineering/SKILL.md (section 9) @ 36b1f18 + working tree, 2026-10-08 -->

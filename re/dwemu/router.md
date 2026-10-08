# The service router

> After login the client talks to a dozen Demonware services over the one encrypted connection. This page lists what it asks for, what the server answers, and what three wrong answers did. **Status:** Part done. Every request seen is answered; most services get an empty but well-formed reply.

## In short

- A request names a **service** and a **task**. The server looks up a handler for the pair, then for the service, then falls back to a default.
- The default is "success, nothing to report" in the shape the task expects. It exists because every request **must** be answered. See [the rule](/re/dwemu/lobby-protocol.md).
- The list of what the client asks for was not guessed: the server writes every request to a journal, and one start with the menus open gives the census.
- Service names marked `?` come from other titles' tables and match our (service, task) pairs. They are not yet confirmed on this game.

## What the client asks for

From the census. The first clean one, 2026-09-24: 19 requests, no retries.

| Service | Task | Name | Request | Reply today |
|---|---|---|---|---|
| 38 | 8 | `bdAntiCheat::reportExtendedAuthInfo` | Client version, a network card address, extra data | Zero rows. **The login gate.** |
| 8 | 1 | `bdProfiles::getPublicInfos?` | `UInt64 1` | Error 800, "not found" |
| 8 | 3 | `bdProfiles::setPublicInfo?` | A blob | Default |
| 12 | 6 | `bdTitleUtilities::getServerTime?` | Nothing | One row: `UInt32` Unix time |
| 27 | 3 | `bdDML::getUserHierarchicalData?` | | Default |
| 95 | 3 | `bdPublisherVariables::retrievePublisherVariables?` | StructData: four namespaces | Empty StructData |
| 104 | 6 | `bdMarketingComms::getMessages?` | StructData | Empty StructData |
| 125 | 9 | `bdAchievementsEngine::getUserState?` | StructData: a context and a list of keys | Empty StructData |
| 125 | 3 | The same service, task not named | | Empty StructData |
| 196 | 100 | Unknown | | Empty StructData |
| 255 | 10 | `bdRESTLegacy::request` | An HTTP request, tunnelled | By URL, see below |

Only the first name is proven on this game: its builder passes the service id in the code, and the same byte is in the captured login request.

## Three replies that mattered

| Request | Wrong reply | What the client did | Right reply |
|---|---|---|---|
| (95, 3) | The plain default, `08 00000000` | Retried every 2 seconds, four times, then gave up. The task requires a StructData and failed its type check. | An empty StructData. Sent once per start since. |
| (8, 1) | Success with zero rows | **2,129 requests in 40 seconds**, one per frame. The success handler returns at zero rows before it sets its "fetched" flag, so the next frame asks again. | Error 800. The failure handler treats "not found" as "no data yet": it resets the data to defaults and sets the flag. One request per start. |
| A list over (255, 10) | JSON without `nextPageToken` | The whole list failed after every object had parsed, then a retry every 15 seconds. The parser accepts the key only as null or a string, and **requires** it. | `"nextPageToken": null` |

## Tunnelled HTTP

The object store, part of umbrella, and presence do not use HTTPS at all on this build. They go through the lobby as service 255, task 10.

Request:

```text
UInt32 1
Blob   a protobuf: the resource, the method, the URL (field 11), the service
Bool   has a body
Blob   the body
```

Reply: the usual `count, total`, then one row per request:

```text
UInt32 1                 version, must be 1
Blob   header protobuf   1: HTTP status   203: a double   302: content type, 1 = JSON   400: a bool
Bool   has a body
Blob   the body          the client writes a zero byte after it, in place
```

- Field 302 must be 1, or the body is never parsed.
- One byte must follow the body: the reply's closing `00` serves.

What the server does with the URL:

| Path | Answer |
|---|---|
| `/v2/core/publishers/treyarch/objects` with a `tu...` category | The publisher file list. See [Publisher data](/re/dwemu/publisher-data.md). |
| The same path, another category | An empty list |
| `/v2/core/users/<id>/objects/` | An empty list |
| Anything else | Zero rows: no HTTP response at all |

The last row is deliberate. The success format of those endpoints has not been read, and a wrong 200 is worse than no answer.

## What the achievement service asks

The (125, 9) request is the native path to the data [progression](/re/engine/progression.md) stands in for. Its body is a protobuf: a context, `"5836"`, and a list of keys such as `/t9/battlepass`, `/t9/doublexp` and `/t9/progression...`. A server for another title answers it with one JSON string holding a value per key. The value format for this game is not known, so the server sends an empty message and the client fills the level block itself.

## How the labels were wrong until 2026-09-24

The first router called the untyped byte the "message type" and the typed byte after it the "service id", and kept the next `UInt32` "on probation" as a task id. That reading came from a single captured request.

On 2026-09-24 a newly released project for other titles was read. Its router decodes the same two bytes as **(service, task)**. Read that way, the census of 9,017 rows matched the public service tables of two other titles pair for pair: six exact pairs. Nothing on the wire changed, only the labels.

Journal rows carry `"schema": 2` since then. Older rows use the old labels.

## Adding a handler

In `tools/dwserver/lobby_router.py`:

```python
@lobby_router.handler(service_id=12, task_id=6)     # omit task_id to catch a whole service
def get_server_time(req, session):
    return lobby_router.rows_success(bdbuf.w_u32(int(time.time())))
```

`req.params` is the decoded field list. `session` is per connection. Ready-made replies: `empty_success()`, `rows_success(...)`, `struct_success(...)`, and `Reply(error_code=...)` for an error.

## The census, both ends

| End | What | Where |
|---|---|---|
| Server | Every request and its reply | `material/lobby_requests.jsonl` |
| Client | The first sighting of each (service, task), with its callers, and a count | A read-only detour on `BdLobbyMsg_WriteHeader`, `(LobbyCensus)` lines in the log |

The client hook moved once: a detour on the message constructor missed the StructData requests, which build their header elsewhere. All eight builders go through the header writer.

## Functions

| Name | RVA | IDA address | Role |
|---|---|---|---|
| `BdLobbyMsg_WriteHeader` | 0xD1D8EC0 | 0x7FF729D98EC0 | Every request passes here |
| `AntiCheat_StartReportExtendedAuthInfo` | 0xD232420 | 0x7FF729DF2420 | Builds (38, 8) |
| `BdRemoteHttp_SendLobbyRequest_Svc10` | 0xD2117C0 | 0x7FF729DD17C0 | Builds a tunnelled HTTP request |
| `BdRemoteHttp_ReadResponse` | 0xD208C50 | 0x7FF729DC8C50 | Reads one reply row |
| `BdRemoteHttp_ReadResponseHeader` | 0xD208390 | 0x7FF729DC8390 | Reads the header protobuf, fields in rising order |
| `BdRemoteHttpTask_FinishRow` | 0xD21FDA0 | 0x7FF729DDFDA0 | Calls the resource's parser, sets done or failed |
| `BdStructTask_ReadStructDataReply` | 0xD20CE20 | 0x7FF729DCCE20 | The StructData type check |

## Limits and open points

- The full service map (every caller of the message constructor, with its request fields and reply decoder) is not written. Many decoders sit behind Arxan thunks.
- Task numbers drift between titles. The `?` names are for reading the journal, not for trusting.
- The task id is echoed in the reply's flag byte by another title's server. Ours sends 0, and every reply so far was accepted.

## See also

- [The lobby protocol](/re/dwemu/lobby-protocol.md)
- [Publisher data](/re/dwemu/publisher-data.md), [Storage and entitlements](/re/dwemu/storage-entitlements.md)
- [The server](/re/dwemu/server.md)

<!-- sources: cw-mod tools/dwserver/lobby_router.py, docs/codrevamped-notes.md, docs/backend-roadmap.md (B1, B2, B3), client/game/dump_anchors.hpp (B3 notes, BdLobbyMsg_WriteHeader), client/hooks/hook.hpp, tools/dwserver/README.md @ 36b1f18 + working tree, 2026-10-08 -->

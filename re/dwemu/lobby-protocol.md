# The lobby protocol

> What is inside an encrypted record: the format of a request, the format of the reply, and the two wrong beliefs that kept the client silent for three sessions. **Status:** Done. A reply in this format produced `[status 27] Login Complete` on 2026-08-02.

## In short

- A record's first plaintext byte after the length is an **inner tag**. The two directions use different tags.
- The body is `bdByteBuffer`: byte-aligned, and **every field carries a one-byte type** in front.
- A request is `[service][task][fields]`. A reply is `[handle][error][flag][results]`.
- Replies are matched to requests by **queue order** and nothing else. Skip one reply and every later reply lands on the wrong request.

## Inner tags

| Tag | Direction | Meaning |
|---|---|---|
| `0x86` | Client to server | A lobby request |
| `0x88` | Client to server | A migrate acknowledgement |
| 1 | Server to client | **The reply to a request** |
| 2, 3, 5 | Server to client | Other server messages |

`BdLobbyConnection_PumpRecv` subtracts 1 three times and compares with 2: it dispatches 1, 2, 3 and 5 and nothing else. A reply sent with tag `0x86` is decrypted, its checksum is verified, it is stored, reported as received, and then **dropped without a word**.

## The type table

The engine holds all 25 names as a literal array, `bdByteBuffer_TypeName`, used for its own mismatch message.

| Id | Type | On the wire after the type byte |
|---|---|---|
| 0 | NoType | Nothing. An end marker. |
| 1 | Bool | 1 byte |
| 2, 3 | Char8, UChar8 | 1 byte |
| 4, 5, 6 | WChar16, Int16, UInt16 | 2 bytes |
| 7, 8 | Int32, UInt32 | 4 bytes |
| 9, 10 | Int64, UInt64 | 8 bytes |
| 13, 14 | Float32, Float64 | 4, 8 bytes |
| 16, 17 | String | Bytes up to a zero byte |
| 19 | Blob | A **typed** UInt32 length, then the bytes: `13 08 <u32> <bytes>` |
| 22 | (splice) | Not a value: the reader splices the buffer and reads the type again. Never seen on the wire. |
| 23 | StructData | A typed UInt32 length, then a **protobuf** message: `17 08 <u32> <bytes>` |

All integers are little-endian. Each read is "check the type byte, then read the bytes": `bdByteBuffer_ReadUInt32` is `CheckTypeTag(8)` and `ReadRaw(4)`.

## A request

`BdLobbyMsg_Ctor` builds every outgoing message and calls `BdLobbyMsg_WriteHeader`, which is two writes:

```text
[service id, one RAW byte][03 task id][ the task's own fields ][00]            a plain task
[service id, one RAW byte][03 task id][17 08 <u32 len>][protobuf][00]          a StructData task
```

The service id is the only untyped byte. The first request any login sends, 62 bytes, decodes exactly:

```text
26                     service 38, bdAntiCheat
03 08                  task 8, reportExtendedAuthInfo
UInt32 4
UInt32 378             the client version, as in the auth request
UInt64 0, UInt64 0, UInt64 0
Blob(6)                a network card address
String "{}"            extra data
Int32 0
00
```

## A reply

`BdLobby_OnServiceReply_Tag1` reads, in order:

| Field | Type | Note |
|---|---|---|
| handle | UInt64 | The server's to choose. Not used for matching. |
| errorCode | UInt32 | 0 is success. 200 goes to a handler map. Anything else is reported as an error. |
| flag | UChar8 | Read only when errorCode is 0 |
| results | | Handed to the task's own decoder |

There is **no leading byte** in this direction: byte 0 of the reply is the `0A` type tag of the handle.

What "results" must be depends on the task class:

| Task kind | Results | The honest minimum |
|---|---|---|
| Plain | `UInt32 count, UInt32 total`, then `count` rows | `08 00000000`: zero rows |
| StructData | A StructData, then nothing | `17 08 00000000`: an empty message, every field at its default |

A plain reply to a StructData task fails its type check, and the client retries.

## The rule: one reply per request, in order

`BdLobby_OnServiceReply_Tag1` pops its queue of pending requests **before it reads a single byte** of the reply. Nothing on the wire says which request a reply answers: the handle is read after the pop.

So an unknown request must still be answered. Silence does not produce a clean failure: it shifts every later reply by one, and the errors that follow describe requests that were answered correctly. This is the opposite of the HTTPS side, where the server answers an unknown path with 404 on purpose.

## Error 4

The client's log shows a failed task as `error: HIDDEN (n)`. The text is a stub; the number is real. **4** has exactly two writers, both hardcoded, both meaning "did not parse":

| Where | When |
|---|---|
| The tag-1 handler's else branch | The envelope itself did not read |
| The generic task reply handler | The task's result decoder returned false |

That is why a reply with `flag = 0` and one with `flag = 1` gave the same error: the flag is read before the decoder runs.

## Functions

| Name | RVA | IDA address | Role |
|---|---|---|---|
| `BdLobbyConnection_PumpRecv` | 0xD217850 | 0x7FF729DD7850 | The inner-tag dispatch |
| `BdLobby_OnServiceReply_Tag1` | 0xD218090 | 0x7FF729DD8090 | Pops the queue, reads the envelope |
| `BdLobbyMsg_Ctor` | 0xD212300 | 0x7FF729DD2300 | Builds a request |
| `BdLobbyMsg_WriteHeader` | 0xD1D8EC0 | 0x7FF729D98EC0 | Service byte, then the typed task id |
| `BdLobbyMsg_WriteStructDataPayload` | 0xD20CFB0 | 0x7FF729DCCFB0 | The StructData request body |
| `BdStructTask_ReadStructDataReply` | 0xD20CE20 | 0x7FF729DCCE20 | Requires a StructData in the reply |
| `bdByteBuffer_CheckTypeTag` | 0xD1788D0 | 0x7FF729D388D0 | One whole byte |
| `bdByteBuffer_ReadRaw` | 0xD178470 | 0x7FF729D38470 | A plain byte cursor |
| `bdByteBuffer_ReadUInt32` | 0xD178EC0 | 0x7FF729D38EC0 | |
| `bdByteBuffer_ReadStringInto` | 0xD178D00 | 0x7FF729D38D00 | Reads to the zero byte |
| `bdByteBuffer_ReadBlob` | 0xD1784D0 | 0x7FF729D384D0 | |
| `bdByteBuffer_ReadStructDataHeader` | 0xD178DB0 | 0x7FF729D38DB0 | |
| `bdByteBuffer_TypeName` | 0xD17BEF0 | 0x7FF729D3BEF0 | The 25 names |

## How we found it: two wrong beliefs

For three sessions the client finished the handshake, sent one record, and then waited forever with a keepalive every 40 seconds. No error.

1. **"The reply is tag `0x86`."** It is tag 1. Proven from the dispatch instructions, not inferred.
2. **"The body is bit-packed with 5-bit type tags."** It is byte-aligned. The byte-aligned reading had been found earlier and written off as a coincidence. The handshake buffer of the layer below really is bit-packed, and the two were taken for one class.

The lesson is about the silence. A wrong tag is thrown away **before the body is looked at**. So the silence said nothing about the body, and three sessions were spent reading it as evidence about the body.

After tag 1, the client's behaviour changed at once: it closed and reported a named error with a number. From there one start could test several replies: the client retries the whole login on an error, so the server answered each retry with the next variant of a list, and the game's log lined up with the list.

## Limits

- Types 11, 12, 15, 18, 20 and 21 have no proven width. The server's parser stops at one instead of guessing.
- The StructData result of most services is an empty message. Their schemas are not read.

## See also

- [The LSG connection](/re/dwemu/lsg.md): the record around this
- [The service router](/re/dwemu/router.md): which service wants what

<!-- the decoded capture is from cw-mod docs/re/demonware-login.md; the 6-byte blob is described, not printed -->
<!-- sources: cw-mod docs/re/demonware-login.md, tools/dwserver/bdbuf.py, lobby_router.py, lsgserver.py (the error-4 notes, the sweep), tools/dwserver/README.md, docs/codrevamped-notes.md @ 36b1f18 + working tree, 2026-10-08 -->

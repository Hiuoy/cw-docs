# The story: from "HTTP code [0]" to a two-PC match

> The backend in the order it happened, with the wrong turns left in. The other pages of this section say what is true. This one says how it was found out, which is the part worth copying. **Status:** the history up to 2026-09-29.

## The idea

Before the backend, the project forced the game's menus into states they would not reach by themselves, one predicate at a time. The pivot was to stop that and give the game what it waits for: a Demonware that answers. Other projects for earlier titles had shown the shape. None of them had a menu-forcing component: they make the client's own online path succeed, and the menus then build themselves.

## The timeline

| Date | What happened | What it showed |
|---|---|---|
| | Two public keys found in the image, replaced in memory. A signed reply verifies offline. | The server needs no secret of Demonware's |
| | The hosts file replaced by import-table hooks | The redirect became part of the code |
| 2026-07-31 | `HTTP code [0]`, nothing at the server. `curl` fails the same way; `curl --ssl-no-revoke` works. | Windows checks revocation. The certificate needs a revocation list it can fetch. |
| | The first real auth request arrives, and the server crashes on it: every number is a string. The game shows `HTTP code [0]` again. | Two faults, one symptom. Record from a `finally` block. |
| 2026-07-31 | The server says its LSG port is 3075. The client dials 3074. | The port is fixed in the client |
| 2026-08-01 | A challenge with no length prefix: the client stalls 9 seconds. With the prefix but no frame byte: 10 seconds. | A stall means "waiting for bytes" |
| 2026-08-01 | The key schedule matches on three connections | The hashed range was solved from one recorded frame, offline |
| 2026-08-01 | All seven recorded client records decrypt, checksums match | The record layer is right |
| 2026-08-01 | The client sends one record and then only keepalives, forever | See "the silence" below |
| 2026-08-01 | A reply with inner tag 1: the client closes and reports error 4 | Tag 1 is right. Now it is a parse problem with a number. |
| 2026-08-02 | Error 4 read out of the engine: "the result decoder returned false". A reply with a zero row count is sent. | **`[status 27] Login Complete`** |
| 2026-08-02 | A crash one second later | A null first-party session. One caller, not fifteen. |
| 2026-08-02 | "Boy 501 Gothic Missile" on the first online start with the backend | A promotion with an unwanted drop to offline |
| 2026-09-16 | `HTTP code [0]` again | No server was running: its journals had not been written since 2026-08-02. The preflight script came out of this. |
| 2026-09-16 | Presence answered: the first post-login requests arrive | The wall after login was on the client |
| 2026-09-16 | One request retried four times | It wanted a StructData |
| 2026-09-16 | A full re-login every 2 minutes | The 120-second receive timer |
| 2026-09-16 | The publisher list is refused twice, then accepted, then the game drops one second later, twice | A missing key; then a renamed signed file |
| 2026-09-16 | 2,129 requests in 40 seconds | "Zero rows" never set the fetched flag |
| 2026-09-22 | Two forks of the project are read | The padlocks are a missing lobby; saves need no server |
| 2026-09-24 | The census start: 19 requests, no retries. The checklist mask is five bits short. | All five are matchmaking or commerce |
| 2026-09-24 | Another project's router is read | Our "message type" was the service id all along |
| 2026-09-24 | Waiver, trial answer, title screen kept, save data seeded, playlists loaded, Start rerouted, one chunk skipped, account id fixed | **An online Zombies match, 23:06** |
| 2026-09-29 | A user id per PC, and peer addresses in the LAN form | **Two PCs in one online match, 22:18** |

## The silence

The most expensive mistake of the whole effort, and the most useful.

The client completed the handshake, sent exactly one encrypted record, and then waited. No error, no disconnect, a keepalive every 40 seconds. Three sessions went into explaining that silence, with two theories:

1. The reply must be tagged `0x86`, like the request.
2. The body must be a bit-packed stream with 5-bit type tags.

Both were wrong. The reply tag is 1, and the body is byte-aligned. Worse, the byte-aligned reading had been found first and dismissed as a coincidence, in a commit whose message said the bit grammar was "confirmed against known plaintext".

Why it lasted: the client throws a reply with the wrong tag away **before it looks at the body**. The silence carried no information about the body at all, and it was read as evidence about the body for three sessions.

What ended it was reading the dispatch code instead of the capture: a few instructions that subtract and compare. Then a reply with tag 1, and the client's behaviour changed within one start.

## Five things that were not what they looked like

| It looked like | It was |
|---|---|
| "The client rejected our reply and disconnected" (three times) | The server's own timeout closing the socket |
| "The flag does nothing" | Two servers on one port; the game talked to the old one |
| "The login is unstable" | The 120-second timer, fed only by the server's bytes |
| "The file list is wrong" | The list was fine. A renamed file failed its signature, and the engine's answer to that is to break the **next** zone. |
| "The tiles are locked because we own nothing" | There was no party |

## What the effort bought

| Rule | From |
|---|---|
| A silent client is not evidence about what you sent. First find out whether it was read. | The silence |
| Record everything the client sends before trying to answer it | Every stage |
| Build the experiment that tells two theories apart, not another guess at one of them | Error 4: one reply with a non-zero error code separated "the envelope does not parse" from "the result does not parse" |
| When your own instrument can end the test, make sure it does not | The socket timeouts |
| Read the consumer, in order | The auth reply's five checks; the lobby reply's envelope |
| A static count of call sites is the size of a fear | Fifteen dereferences, one of which ran |
| The engine's own error strings are the best documentation it has | "Bad recv counter", "HMAC mismatch", "Invalid or No Task ID" |
| A passing offline test is a claim. The game's log line is the result. | Every milestone |
| Read prior art for layout, then check each number | The service table matched six pairs; task numbers still differ between titles |

## What is still open

- The service map: every request's fields and every reply's decoder.
- The marketplace, the store, the battle pass. Not planned. See [Storage and entitlements](/re/dwemu/storage-entitlements.md).
- Two PCs on different networks.

The live status is in the project's roadmap, not here.

## See also

- [DWEmu: the map](/re/dwemu/overview.md)
- [The cycle](/re/method/cycle.md): the same method, stated generally
- [Errors](/re/engine/errors.md): the other long hunt

<!-- sources: cw-mod docs/re/demonware-login.md, docs/backend-roadmap.md, docs/codrevamped-notes.md, docs/fork-findings.md, tools/dwserver/README.md, authserver.py, lsgserver.py, lsgcrypto.py, bdbuf.py, lobby_router.py (the dated notes in their comments), docs/ROADMAP.md (section 3) @ 36b1f18 + working tree, 2026-10-08 -->

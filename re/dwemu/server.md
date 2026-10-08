# The server: built as an instrument

> `tools/dwserver` is a few Python files. This page is about how it is built and why: it was a **recorder** before it was a server, and that is how each contract in this section was found. For commands and flags, see [dwserver](/guide/tools/dwserver.md). **Status:** Done for what the game needs to reach a match.

## In short

- Two small servers: one for HTTPS (auth, umbrella, the revocation list), one for the TCP connection on 3074.
- Every request is written to a journal **before** anyone tries to answer it well. The journal is the request contract, observed instead of guessed.
- Each protocol layer has an offline test pinned to bytes the real game sent.
- A handful of design rules, each paid for with a failed test run.

## The parts

| File | Layer | Explained in |
|---|---|---|
| `gen_keys.py`, `reissue_cert.py` | Key pairs, the certificate authority, the leaf, the revocation list | [Keys](/re/dwemu/keys.md), [Redirect and TLS](/re/dwemu/redirect-tls.md) |
| `dwsign.py` | The PSS signature | [Keys](/re/dwemu/keys.md) |
| `authserver.py` | `/auth/`, umbrella, the revocation list on port 80, and the recorder for every other path | [Auth](/re/dwemu/auth.md) |
| `lsgserver.py` | The handshake and the record pump | [The LSG connection](/re/dwemu/lsg.md) |
| `lsgcrypto.py` | The key schedule and the record layer | [The LSG connection](/re/dwemu/lsg.md) |
| `bdbuf.py` | The typed format, and a schema-less protobuf reader | [The lobby protocol](/re/dwemu/lobby-protocol.md) |
| `lobby_router.py` | Service and task dispatch, the handlers, the census | [The service router](/re/dwemu/router.md) |
| `run.py` | Preflight, both servers as child processes, one log | [dwserver](/guide/tools/dwserver.md) |

The auth server hands the session key to the LSG server through a file in the private `material` folder. The two are separate processes on purpose: each can be restarted or run by hand with its own flags.

## The rules it is built on

| Rule | What it replaced | What that cost |
|---|---|---|
| **Record first.** Every HTTP request goes to the journal from a `finally` block. | A handler that raised lost the only evidence the game had asked | A type error on the first real request looked like a TLS failure. The traceback in the journal named it in one pass. |
| **Unknown HTTP path: 404.** | Answering every path, GET included, with the signed auth reply | The object store got an auth reply and discarded it. From outside: "the client silently does nothing". |
| **Unknown lobby request: a default success.** | | The opposite rule, for the opposite reason: replies are matched by order, so silence shifts every later reply. See [The lobby protocol](/re/dwemu/lobby-protocol.md). |
| **Bind ports exclusively.** | Python's default lets a second process bind a port that is already in use on Windows | Two servers on 443. The game's requests went to the older one, and a new flag "did nothing". It had never run. |
| **Never close the connection yourself.** | A reader that took one burst and returned | Three times, "the client disconnected" was the server's own socket closing. The session is now held for 15 minutes. |
| **Do not answer blind.** If the derived challenge does not match the client's, send nothing. | | A wrong echo is dropped with no message, which looks exactly like a framing bug |
| **One start, several questions.** `--sweep` answers each login retry with the next variant of a list. | One hypothesis per game start | The client retries the whole login on an error, several times in a row. Each retry was a free trial being thrown away. |
| **Fixed values where random is not needed.** The server's challenge nonce is constant. | | Two captures can be compared byte for byte |
| **A flag that changes answers is an experiment, not a mode.** | | `--answer-unknown` and `--unknown-error` hide which request caused a later failure |

## The journals

All in `material`, one JSON object per line, written as things happen.

| File | One line is | Used for |
|---|---|---|
| `requests.jsonl` | An HTTP request: host, path, headers, body, what was served | Which endpoints exist. After the redirect the `Host` header is the only thing that says which service the game meant. |
| `lsg_frames.jsonl` | One TCP connection: every message both ways in hex, the derived keys' check values, each decrypted record | The handshake, the record layer, the offline tests' ground truth |
| `lobby_requests.jsonl` | One lobby request: service, task, the decoded fields, the reply, which handler answered | The census. See [The service router](/re/dwemu/router.md). |
| `server.log` | Both servers' console output, timestamped | Reading a run back in order |

A body that is not text is stored as base64 with a flag, so the recorder never has to guess.

## The offline tests

`python run.py --test` runs all six. None needs the game or a free port.

| Test | Pins |
|---|---|
| `selftest` | A signed reply verifies with the game's PSS parameters; the key blob is 294 bytes; a ticket is 128 |
| `smoketest_http` | The auth server over real TLS, trusted through the local authority; code 700; ticket sizes |
| `recordtest` | Routing: an unknown path gets 404, not the auth reply. And the shape of the journal. |
| `lsgtest` | The KDF is feedback mode; labels have no separator; the HMAC operand order; the listener binds 3074 |
| `bdbuftest` | The one captured first request decodes to values that can be checked elsewhere **and** consumes the buffer exactly |
| `routertest` | The login request and its reply, byte for byte, from the session that first reached "Login Complete" |

What they cannot do is prove the game agrees. A layer counts as done when the game's own log line says so.

On "consumes the buffer exactly": a wrong grammar usually reads the first field or two without trouble. What it cannot do is land on the last byte having produced a known version number on the way.

## The instruments on the other end

The client side has a transcript for each stage. All are read-only detours, installed only when the backend is on, and each logs under its own tag in `cw-mod\client.log`.

| Tag | Shows |
|---|---|
| `(DwNet)` | Every Demonware name resolved and address dialled, with the verdict |
| `(Login)` | The login state machine's own status lines |
| `(LobbyCensus)` | The first sighting of each service and task, with the callers |
| `(Presence)` | Each call site whose presence answer was changed |
| `(DwFetch)` | The checklist mask, the missing bits, and the state behind each |
| `(LpcList)` | Each step of the publisher file list |
| `(MtxSync)` | Which gate holds the marketplace sync |
| `(Trial)`, `(PeerAddr)` | The trial answer per call site; this PC's peer address as built |

`python tools\bootlog.py` puts both ends together: the game's last run, with the matching part of the server's log under it.

## How a milestone was done

1. Start the backend, start the game, read both logs.
2. The failing status line names a **stage**. Read that stage's handler in the disassembler: the fields it parses, their order, each error text.
3. Build the smallest server change that meets the contract.
4. Pass: the game's log line for that stage. An offline test alone never counts.

## Limits

- Python's standard HTTP server and one thread per connection. It serves one game on one PC.
- No download endpoint, no real object store, no storage.
- The `material` folder holds private keys. It is never committed and never shared.

## See also

- [dwserver](/guide/tools/dwserver.md): commands, flags, the preflight
- [The story](/re/dwemu/story.md)
- [The cycle](/re/method/cycle.md)

<!-- sources: cw-mod tools/dwserver/README.md, run.py, authserver.py, lsgserver.py, lobby_router.py, selftest.py, smoketest_http.py, recordtest.py, lsgtest.py, bdbuftest.py, routertest.py, docs/backend-roadmap.md ("How every milestone is done"), client/hooks/impl/game/*.cpp (log tags) @ 36b1f18 + working tree, 2026-10-08 -->

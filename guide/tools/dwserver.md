# dwserver

> The local Demonware backend: a set of Python scripts in `tools\dwserver`. This page is the command reference. To set it up and play, see [Online mode](/guide/play/online.md).

## run.py: the one command

```text
python run.py                 check the setup, start both servers, one combined log
python run.py --check         check the setup only
python run.py --test          run every offline test; no game and no ports needed
```

| Option | Meaning |
|---|---|
| `--check` | Preflight only |
| `--test` | Run the offline tests. They must end with `ALL PASS`. |
| `--game <dir>` | The game folder, to compare its keys with yours |
| `--force` | Start the servers even if the preflight fails |
| `--auth-args "<flags>"` | Extra flags for `authserver.py`, as one quoted string |
| `--lsg-args "<flags>"` | Extra flags for `lsgserver.py`, as one quoted string |

## What the preflight checks

The game reports every setup mistake with one line, `Auth task failed with HTTP code [0]`. The preflight names the cause before you start the game.

| Check | What a failure means |
|---|---|
| Your certificate authority is in Windows' trusted root store | The game's TLS will refuse the server |
| The server certificate and the revocation list are valid | The same |
| The keys in `<game>\cw-mod\dwserver\` are the ones in `material\` | The game will refuse the server's signatures. Copy the `.der` files again. |
| Ports 443, 80 and 3074 are free | Another program holds one. The preflight names it. |

After the start it probes both servers the way the game will, and prints `READY`.

## The files

| File | Role |
|---|---|
| `gen_keys.py` | Makes your keys, your certificate authority and the server certificate. Run once. |
| `run.py` | Preflight, both servers, the combined log |
| `authserver.py` | The login service on HTTPS (443), the revocation list on HTTP (80), and a recorder for every other web request |
| `lsgserver.py` | The lobby connection on port 3074 |
| `lobby_router.py` | Sorts each lobby request by service and task and answers it |
| `lsgcrypto.py`, `bdbuf.py`, `dwsign.py` | The connection's encryption, the message format, and the signatures |
| `reissue_cert.py` | Makes a new server certificate from your existing authority |
| `*test.py`, `selftest.py` | The offline tests |
| `material\` | Everything generated: keys, certificates, logs. **Private. Never share it.** |

## The logs

All in `material\`.

| File | Holds |
|---|---|
| `server.log` | Both servers' output, timestamped, all runs |
| `requests.jsonl` | Every web request the game made: host, path, headers, body |
| `lobby_requests.jsonl` | Every lobby request and the reply it got |
| `lsg_frames.jsonl` | The raw frames of the lobby connection |

From the repository's root, `python tools\bootlog.py` prints the game's last run with the matching part of `server.log` under it.

## Flags for experiments

These change what the servers answer. They are for finding out what the game needs, not for playing. Pass them through `--auth-args` or `--lsg-args`.

| Server | Flag | Effect |
|---|---|---|
| auth | `--answer-unknown` | Answer web requests nothing handles with an empty 200 instead of 404 |
| auth | `--reply-ints` | Send numbers as JSON numbers instead of text |
| auth | `--extended-data <text>` | The extra data string in the login reply |
| auth | `--user-id <n>`, `--username <name>` | The identity in the login ticket when the game sends none. A current client sends its own. |
| auth | `--lsg-endpoint <host>` | The host of the lobby server. A bare host name: the game always dials port 3074. |
| auth | `--no-crl`, `--crl-port <n>` | Do not serve the revocation list, or serve it on another port |
| lsg | `--unknown-error <n>` | Answer requests nothing handles with this error code |
| lsg | `--reply-error <n>`, `--reply-handle <n>`, `--reply-flag <n>` | Override fields of every reply |
| lsg | `--no-reply` | Do not answer at all |
| lsg | `--sweep <v1,v2,...>` | Answer each new login attempt with the next variant, to test several ideas in one run |

Three environment variables change which playlist files the router lists: `CWMOD_LPC_DIR`, `CWMOD_LPC_EXCLUDE`, `CWMOD_LPC_FILES`. The game's own local playlist loading does not need them.

## Adding a reply

```python
@lobby_router.handler(service_id=8, task_id=4)     # leave task_id out to catch a whole service
def my_task(req, session):
    return lobby_router.empty_success()            # or Reply(error_code=..., results=...)
```

The one rule: answer every request, exactly once, in order. The game matches replies to requests by their order alone.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The preflight fails on the certificate authority | Import `material\ca_cert.pem` again, in an elevated PowerShell. |
| A port is in use | Close the program the preflight names. A second copy of the backend is the usual one. |
| `ModuleNotFoundError: cryptography` | `pip install cryptography` |
| The game logs in again and again | The backend was stopped while the game ran. Start it and restart the game. |

**How it works inside:** [The server: built as an instrument](/re/dwemu/server.md), [The service router](/re/dwemu/router.md), [The lobby protocol](/re/dwemu/lobby-protocol.md).

<!-- sources: cw-mod tools/dwserver/README.md, tools/dwserver/run.py, authserver.py and lsgserver.py (argument parsers), lobby_router.py (LPC environment variables) @ 36b1f18 + working tree, 2026-10-08 -->

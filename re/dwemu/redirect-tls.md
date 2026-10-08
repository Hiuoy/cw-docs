# Redirect and TLS

> How every Demonware connection ends on the player's own PC, and why "trust the certificate" was not enough to get one HTTP byte through. **Status:** Done, in game.

## In short

- The game imports all of its networking from one DLL, `WS2_32`. Three hooks on its import table see every name it resolves and every address it dials.
- A Demonware name is answered with `127.0.0.1` when the local backend is on, and **refused** when it is not. It never reaches the real resolver.
- The game has **two** TLS clients, and both ask Windows to validate the chain. One local certificate authority in the Windows store satisfies both.
- Windows also checks **revocation**. A certificate with no reachable revocation list fails the handshake, and the game reports only `HTTP code [0]`.

## The choke point

| Hook | Kind | What it does |
|---|---|---|
| `getaddrinfo` | Import table | The resolver both TLS clients use. Redirect or refuse. |
| `gethostbyname` | Import table | The old resolver. Same policy. |
| `connect` | Import table | The backstop: sees addresses that were never resolved by name |

Three switches, set once at start:

| Switch | On when | Effect |
|---|---|---|
| Redirect | `"backend"` is on and `<game>\cw-mod\dwserver\` exists | A Demonware name resolves to `127.0.0.1` |
| Block | `"mode"` is not `offline` and there is no backend | A Demonware name fails as "host not found". A routable address is refused as "connection refused". |
| Journal | Either of the above | Every resolve and connect is written to `cw-mod\dw_journal.txt` |

Details that matter:

- **What counts as Demonware.** Any name that contains `demonware.net`, `activision.com` or `callofduty.com`. The game builds its host names from templates at run time, so a list of full names would be incomplete, and an incomplete list fails **open**. The rule is the domain.
- **How the redirect is done.** The hook asks the real `getaddrinfo` for `127.0.0.1` instead of the name. The result is a chain the system allocated, with the caller's own port and hints, and the system's `freeaddrinfo` frees it. Building a chain by hand would need a matching free hook, and a mistake there is heap corruption somewhere else.
- **Failing the way the game expects.** A blocked name returns the resolver's own "not found" code, and a blocked address the "refused" code, so the game takes paths it has.
- **LAN keeps working.** Loopback, private and link-local addresses are never blocked.
- **Which port for which host.** After the redirect every endpoint is `127.0.0.1`. Both TLS clients resolve and connect on one thread, so the journal labels a connect with the last Demonware name resolved on that thread. It is a hint; the address is the fact.

## The names and the ports

The auth host is built from the template `%s-%s-auth3.%s.demonware.net`: title, provider, environment. On this build that gives `t9-bnet-auth3.prod.demonware.net`.

| Service | Host pattern | Port |
|---|---|---|
| Auth | `...-auth3.<env>.demonware.net` | 443 |
| Umbrella | `<env>.umbrella.demonware.net` | 443 |
| Uno | `<env>.uno.demonware.net` | 443 |
| Object store | `objectstore.<env>.demonware.net` | 443, but see [Publisher data](/re/dwemu/publisher-data.md) |
| Login queue | `loginqueue.<env>.demonware.net` | 443 |
| LSG | The host comes from the auth reply | **3074**, fixed in the client |
| STUN | `stun.<region>.demonware.net` | Not served |

## Two TLS clients

| Client | Evidence | Validates through |
|---|---|---|
| libcurl with the Schannel backend | The Windows certificate-chain functions are imported, and the image holds curl's Schannel strings | The Windows chain engine |
| WinHTTP | Imported and called from four functions | The Windows chain engine |

Other projects for earlier titles switch off curl's verification. Here that would cover one client of two. A certificate authority of the player's own, installed in the Windows Trusted Root store, covers both. The leaf certificate lists every Demonware host name.

## The revocation trap

With the authority trusted and the server listening, the game still logged:

```text
Auth task failed with HTTP code [0]
```

Nothing reached the server: no request, no log line.

| Step | Finding |
|---|---|
| The same request with `curl` | Failed the same way |
| `curl --ssl-no-revoke` | 200 and a valid signed reply |
| The Windows error | `CRYPT_E_NO_REVOCATION_CHECK`: the revocation function could not check revocation |

Schannel checks the whole chain for revocation. A leaf with no revocation information cannot be checked, and "cannot check" is a failure. So:

1. The leaf carries a revocation list address.
2. The server serves an empty, signed list there, over **plain HTTP on port 80**. A revocation list cannot be fetched over HTTPS: that connection would need its own revocation check.
3. The address is the literal `http://127.0.0.1/cwmod.crl`. The fetch is made by Windows' own crypto library, which has its own link to the network DLL and never passes the game's import table. A host name there would go out to real DNS: it would fail, and it would leak a query.

`HTTP code [0]` therefore means "TLS failed, or nothing was listening". Every setup mistake looks the same from the game, which is why the server's start script checks each cause first. See [The server](/re/dwemu/server.md).

## What cw-mod does

| Where | What |
|---|---|
| `client/game/dw_net.cpp` | The policy, the journal |
| `client/hooks/impl/patched/ws2_32/` | The three hooks. Installed always; inert until a switch is on. |
| Overlay, Demonware tab | The journal, live, with repeat counts |
| `tools/dwserver/gen_keys.py` | The authority, the leaf, the revocation list |

## How we found it

- Two unrelated faults had one symptom: a TLS failure, and later a bug in the server's reply code, both showed as `HTTP code [0]`.
- The hosts file was used first. It needs an administrator, changes the whole PC, and outlives the game. The import-table hooks need none of that and cannot be forgotten.
- The journal exists because an online start usually ended in a crash. Lines are written as they happen, so the run that reaches something new keeps its record.

## Limits

- IPv4 only. Another address family passes through.
- A connection that Windows itself makes, like the revocation fetch, is outside the hooks. That is why its address is a literal loopback one.

## See also

- [Keys](/re/dwemu/keys.md), [Auth](/re/dwemu/auth.md)
- [Online mode, the guide](/guide/play/online.md): installing the authority
- [Errors and fixes](/guide/troubleshooting.md): `HTTP code [0]`

<!-- sources: cw-mod client/game/dw_net.hpp, dw_net.cpp, client/hooks/impl/patched/ws2_32/getaddrinfo.cpp, connect.cpp, tools/dwserver/gen_keys.py (host names, the CRL notes), authserver.py (CrlHandler), tools/dwserver/README.md @ 36b1f18 + working tree, 2026-10-08 -->

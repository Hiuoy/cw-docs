# Online mode

> The game's online menus, party and playlists, with a Demonware backend that runs on your own PC. **Status:** Done up to a full match (2026-09-24); two PCs in one match (2026-09-29).

## What it is

Online mode normally needs Activision's Demonware servers. Here a small Python server on your PC, `tools\dwserver`, answers in their place, and the mod sends the game's Demonware traffic to it. Each player runs their own. Players still connect to each other directly.

## Before you start

- Python 3 with the `cryptography` package (`pip install cryptography`).
- An elevated PowerShell for one step.
- Ports 443, 80 and 3074 free on your PC.
- The playlist files your own game downloaded.

## Set it up once

Run these in `tools\dwserver`.

1. **Make your keys and certificates.**

   ```powershell
   python gen_keys.py
   ```

2. **Test the server**, with no game needed. It must end with `ALL PASS`.

   ```powershell
   python run.py --test
   ```

3. **Trust your certificate authority.** In an elevated PowerShell:

   ```powershell
   Import-Certificate -FilePath "material\ca_cert.pem" -CertStoreLocation Cert:\LocalMachine\Root
   ```

4. **Give the game your public keys.** Copy `material\auth_pub.der` and `material\lsg_pub.der` into `<game>\cw-mod\dwserver\`.
5. **Give the game its playlists.** Copy `core_playlists_tu*_100_*.ff` and the one for your language, such as `en_core_playlists_tu*_100_*.ff`, from `%ProgramData%\Activision\Call Of Duty Black Ops Cold War\LPC` into `<game>\cw-mod\lpc\`.
6. **Set the mode** in `cw-mod.json`:

   ```json
   { "mode": "online", "backend": true }
   ```

> [!WARNING]
> Step 3 adds a certificate authority to Windows that only your PC holds the key for. Keep the `material` folder private, never share it, and remove the certificate from the store when you stop using the backend.

## Play

1. Start the backend and leave it running. It checks the setup first and prints `READY`.

   ```powershell
   python run.py
   ```

2. Start the game. On the title screen, press start: that creates your party.
3. The online menus open, with the modes and maps of your playlist. Start a Zombies match as usual.

The log shows `[status 27] Login Complete` when the login worked.

## Two PCs

- Each PC runs its own backend and does the whole setup itself.
- Each PC has its own `"xuid"` in `cw-mod.json`. It is made on the first run. Never copy `cw-mod.json` from one PC to another.
- The second PC joins through the overlay's [Server Browser](/guide/play/lan.md).

## Limits

| Thing | State |
|---|---|
| The store, the battle pass's own progress, owned bundles | Not available: they need Activision's marketplace. Not planned. |
| Public matchmaking, dedicated servers | Not planned |
| Two PCs on different networks | Open: not tested |
| Saves | Kept on your PC. See [Progression](/guide/play/progression.md). |

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| `Auth task failed with HTTP code [0]` | Every setup mistake looks like this. Run `python run.py --check`: it names the cause (no server running, certificate not trusted, old keys in the game folder, a port in use). |
| Mode tiles with padlocks | You skipped the title screen. Keep `"start_screen": true` and press start. |
| "No preferred playlist" or no modes in the menu | No playlist files in `cw-mod\lpc`, or their build id is not this game's. The log's `(LPC)` lines say which. |
| The second PC cannot join | Both PCs use the same `"xuid"`, from a copied `cw-mod.json`. Delete the key on one PC and restart: a new id is made. |

`python tools\bootlog.py` prints the game's login steps next to the backend's log for the same run.

**How it works inside:** [DWEmu: a local Demonware](/re/dwemu/overview.md), [After login](/re/dwemu/post-login.md), [Publisher data and playlists](/re/dwemu/publisher-data.md).

<!-- sources: cw-mod tools/dwserver/README.md, tools/dwserver/run.py (header), tools/dwserver/lobby_router.py (LPC folder), client/game/local_lpc.hpp, client/game/local_lpc.cpp, docs/backend-roadmap.md (B2, B3, B6 to B8), docs/ROADMAP.md (sections 2 and 3) @ 36b1f18 + working tree, 2026-10-07 -->

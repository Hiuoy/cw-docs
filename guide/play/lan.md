# LAN mode

> Two PCs in one Zombies match over your own network. **Status:** Done (2026-07-23). The Server Browser: Done (2026-09-29).

## Before you start

- cw-mod on both PCs, the same build of the mod, and the same game build.
- Both PCs on one network.
- A different `"name"` in each PC's `cw-mod.json`. Two PCs with the same name look like one player joining itself.

## Steps

1. On **both** PCs, set the mode and restart the game:

   ```json
   { "mode": "lan" }
   ```

2. **Host:** open Zombies and create your match the usual way, through the game's own menus. Wait in the lobby.
3. **Host:** open the overlay's **Server Browser** tab. It should say `Advertising` with your lobby's name and map.
4. **Second PC:** open the Server Browser tab. The host's lobby appears in the list within a second or two. Press **Join**.
5. The second player appears in the host's lobby. The host starts the match.

## Without the browser

If the list stays empty, the join still works by hand:

1. Host: overlay, **Session** tab, **Show host descriptor**. Copy the line that starts with `CWJOIN1`.
2. Send that line to the second PC by any means.
3. Second PC: Session tab, paste the line, **Join host by descriptor**.

The line is valid only for the host's current lobby. If the host makes the lobby again, take a new line.

## How the browser works

The game has no LAN discovery left in this build, so the mod carries its own. A PC with a live lobby broadcasts a small UDP message on **port 28970** once a second: who hosts, the map, the mode, the players, and what is needed to join. Every PC lists what it hears. A row disappears 5 seconds after its host goes quiet.

## Limits

- Tested on one home network. Two PCs on different networks through a VPN is **open**: not tested since the fixes of 2026-09-24.
- There is no public matchmaking and there are no dedicated servers.
- A join needs join type 4, which the Join buttons already use.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The list is empty, and the host's "sent" count climbs | The second PC's firewall drops UDP 28970 inbound. Allow it. |
| `LAN socket down` | The mod could not open the port. The tab shows the reason. |
| `Not advertising: no live lobby on this PC` | The host has not created a lobby yet. |
| The join is refused | Use the Join button, not a hand-edited join type. The reason is printed under the list. |
| A row is marked "different build" | The two PCs run different game builds. Use the same one. |
| The second player is not let into the match | In the host's Session tab, set the player cap to 2 or more before the map starts. |

To play in the game's online menus instead, see [Online mode](/guide/play/online.md).

<!-- sources: cw-mod client/game/lan_browser.cpp (header), client/overlay/tabs/server_browser.cpp, client/overlay/tabs/session.cpp, client/game/settings.hpp (PlayerName), docs/ROADMAP.md (section 2), docs/fork-findings.md (section 6) @ 36b1f18 + working tree, 2026-10-07 -->

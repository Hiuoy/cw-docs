# How we did it

> The reverse-engineering side of cw-mod: how each feature works inside the game, written so that another reverse engineer can check it and build on it.

Black Ops Cold War shipped with no mod tools, an encrypted executable and an online-only frontend. Every feature of cw-mod started as a question about the game's own code. These pages are the answers, one feature per page.

## How to read these pages

| Thing | Rule |
|---|---|
| Game build | Everything is for **1.34.0.15931218**. Another build has other addresses. |
| Addresses | A function is given as an **RVA** and as its address in our IDB, whose image base is `0x7FF71CBC0000`. In your own dump, add the RVA to your base. |
| Names | Names are ours, in the engine's style (`Subsystem_VerbObject`, globals `g_`). A name ending in `_cand` is inferred, not proven. |
| Offsets | `+64` means 64 bytes from the start of the structure, in decimal unless written `0x`. |
| Hashes | A name hash is 64-bit FNV-1a over the lowercased name with the top bit cleared, unless the page says otherwise. |

Every page has the same parts, in the same order: a short summary, how the thing works, the functions, the structures, what cw-mod does about it, how we found it, and the limits.

## Status words

The words are the roadmap's.

| Word | Meaning |
|---|---|
| **Done** | Seen working in the game, on the date given |
| **Part done** | Some of it works; the page says what is left |
| **Built** | Written, not yet seen working in the game |
| **Open** | Known work, not started |
| **Parked** | Set aside on purpose |

## Sections

| Section | What it covers |
|---|---|
| Method | [The cycle](/re/method/cycle.md), [the binary and its dump](/re/method/binary.md), [address math](/re/method/address-math.md), [hashes](/re/method/hashes.md), [the tools](/re/method/tooling.md) |
| The client | [The DLL](/re/client/overview.md), [Arxan](/re/client/arxan.md), [hooking](/re/client/hooking.md), [the boot profile](/re/client/boot-profile.md), [the overlay](/re/client/overlay.md) |
| Engine systems | [Dvars](/re/engine/dvars.md), [Lua and the menus](/re/engine/lua-lui.md), [menu scripts](/re/engine/ui-scripts.md), [UI text](/re/engine/ui-text.md), [the script VM](/re/engine/gsc-vm.md), [script strings](/re/engine/gsc-strings.md), [player data](/re/engine/playerdata.md), [progression](/re/engine/progression.md), [unlock-all](/re/engine/unlock-all.md), [errors](/re/engine/errors.md) |
| DWEmu, the local Demonware backend | [The map](/re/dwemu/overview.md), [redirect and TLS](/re/dwemu/redirect-tls.md), [the two keys](/re/dwemu/keys.md), [auth](/re/dwemu/auth.md), [the LSG connection](/re/dwemu/lsg.md), [the lobby protocol](/re/dwemu/lobby-protocol.md), [the service router](/re/dwemu/router.md), [after login](/re/dwemu/post-login.md), [publisher data](/re/dwemu/publisher-data.md), [storage and entitlements](/re/dwemu/storage-entitlements.md), [the server](/re/dwemu/server.md), [the story](/re/dwemu/story.md) |
| Reference | [Function index](/re/reference/functions.md), [Globals index](/re/reference/globals.md) |

Not written yet:

| Section | What it will cover |
|---|---|
| Netcode | Addresses, hosting, joining, the message dispatcher, the server browser |
| Fastfiles and zones | The container, the stream, the loaders, the zone trace, writing zones |
| Asset types | One page per type: layout, loader, what mapkit reads and writes |
| Mapkit internals | How a custom map is built, from level script to navmesh |

Until then, the [guides](/guide/mapping/overview.md) cover how to use the map tools, and [what you can and cannot make](/guide/mapping/limitations.md) lists what is yours, copied or borrowed.

## What is not here

No game data and no decompiled game scripts: see [Legal](/legal.md). To use the mod, go to the [Guides](/guide/).

<!-- sources: cw-mod .claude/skills/bocw-reverse-engineering/SKILL.md (sections 0 to 4), docs/ROADMAP.md (status words) @ 36b1f18 + working tree, 2026-10-07 -->

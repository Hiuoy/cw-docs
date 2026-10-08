# Glossary

> The words these docs use, in one or two lines each. Pages link here the first time they use a term.

## A to C

### Anchor
An engine address the client uses. It is stored as an address in our dump and moved to the running game's base at start-up. See the [function index](/re/reference/functions.md).

### AOB signature
A byte pattern with wildcards that finds a piece of code without knowing its address. It survives a rebuild of the game better than an anchor does.

### Arxan
The commercial protection on the game's executable. The file on disk is encrypted; at run time it checks its own code, resists debuggers, and guards some functions against callers from outside the game image.

### Asset
One item in a zone: a model, an image, a script, a sound bank. Each has a type and a name hash. The engine's word is XAsset.

### Asset library
The retail zones a custom map loads to get zombies, weapons, effects and sounds. Today that is Die Maschine's.

### Auth ticket
128 bytes inside Demonware's login reply. It holds the user id, the user name and the session key. See [Auth](/re/dwemu/auth.md).

### bdByteBuffer
The format of a Demonware lobby message: byte-aligned fields, each with a one-byte type in front. See [The lobby protocol](/re/dwemu/lobby-protocol.md).

### bgcache
An asset that lists the names scripts and entities may use. A model that an entity names must be listed there, or it never draws.

### Brush
A box of level geometry in the map editor (`MkBrush`).

### Build
Two meanings. The game version these docs are for, 1.34.0.15931218. And the editor's Build button, which runs cwlink.

### Caller guard
An Arxan check at the start of some engine functions. When the caller's return address is outside the game image, the function returns at once having done nothing, with no error.

### Census
A run whose purpose is to record what the game asks for: every lobby request, or every caller of one function. The list then decides what to build.

### Clientfield
A value a server script replicates to the client scripts. Both sides must register the same list, or the player is dropped with "Clientfield Mismatch".

### Clip map
The asset that holds a level's collision.

### Content chain
How the shared Zombies scripts find a map's machines: destination, location, instance, struct, each pointing at its parent.

### CSC
The game's client-side script. See GSC.

### cwlink
The mapkit tool that builds a map's zone and scripts from its `.mkmap` source.

## D to F

### DDL
The engine's format for player data: a schema plus a packed buffer.

### Demonware
Activision's online backend: login, playlists, player storage, the store.

### Detour
A hook: the start of an engine function is replaced with a jump to our code, which may call the original.

### Die Maschine
The retail Zombies map whose zone is named `zm_silver`. Custom maps use it as their asset library.

### Dump
A copy of the game's decrypted image taken from inside the running game. It is what the disassembler reads, since the file on disk is encrypted.

### Dvar
An engine variable. It is found by a hash of its name; the names themselves are not in the game.

### DWEmu
The local Demonware emulator in `tools/dwserver`, which each player runs on their own PC.

### Entity list
The asset that holds a level's entities. Its sibling, the trigger list, holds the trigger entities and their shapes.

### Fastfile
The game's asset container, a `.ff` file. See Zone.

### fd file
A `.fd` file is a binary patch that brings the `.ff` of the same name up to the current game build.

### ffinfo
mapkit's command-line zone inspector.

### First-party presence
The engine's test "is a Battle.net user signed in and present". The local backend has no Battle.net, so the client answers it. See [After login](/re/dwemu/post-login.md).

### FNV-1a
The hash behind most engine names. The engine uses the 64-bit form over the lowercased name and clears the top bit.

## G to L

### gfx_map
The asset that holds the drawn world: placed models, decals, draw materials.

### GSC
The game's server-side script language. A script is compiled to a `.gscc` file with ACTS.

### Hull
A convex collision shape.

### IDB
The disassembler's database of the dump, with the names and comments the project has added.

### Image base
The address a module is loaded at. Ours in the IDB is `0x7FF71CBC0000`; a running game has another one each time.

### Inner tag
The first byte of a decrypted LSG record. It says what the record carries: `0x86` is a request from the game, 1 is the server's reply.

### KAPI
The format of the `.xpak` and `.xsub` streaming packages.

### LAN mode
Playing together with the game's network mode set to LAN. See also Online mode.

### LazyLink
GSC opcode 0x13, a function reference resolved at run time. The game's own handler does nothing; the script loader supplies one.

### LPC
Demonware's publisher content, such as playlists, kept on disk as small fastfiles.

### LSG
Demonware's lobby gateway: the encrypted TCP connection on port 3074 that carries every lobby service request.

### LUI
The game's menu system, written in Lua.

## M to R

### mapkit
The custom-map tools: the Godot plugin, cwlink, zonekit, ffinfo and mkasset.

### mkasset
The mapkit tool that reads the game's models from your install for the editor's preview.

### mkmap
A `.mkmap` file is a map's source: JSON with your geometry, objects and settings, and game assets by name only.

### Navmesh
The surfaces zombies walk on and find their path over.

### netadr
The engine's 16-byte network address. In this game it is a handle into Demonware's address tables, not an IP address.

### Online mode
Playing together with the game's network mode set to online, against the local backend. The game's online menus and party are used.

### Overlay
Two meanings. cw-mod's in-game menu, opened with Insert. And the older form of a custom map, built as override zones on top of Die Maschine.

### Override zone
A zone whose assets replace another zone's assets of the same name, because its priority is higher.

### PlayerData
The engine's store of per-player data blocks: stats, loadouts, progression.

### Preload
The lobby's early load of the picked map's zone, before the match starts.

### Publisher data
Files the game's publisher serves through Demonware, such as the playlists. The game keeps them in a folder on the PC. See [Publisher data](/re/dwemu/publisher-data.md).

### RVA
Relative virtual address: an address minus the image base. It is the same in every dump of one build.

## S to Z

### Script string
A string in the engine's string table, used by scripts and entities and referred to by an id. Inside a zone the ids are zone-local.

### Session key
The 24 bytes in the auth ticket from which both sides derive the keys of the LSG connection.

### Stream key
A handle to data that lives in the streaming packages instead of the zone.

### StructData
A lobby message field that holds a protobuf message. Some Demonware services send and expect only this.

### Studio auth
The Demonware login flow the client is switched to (flow 9). It needs no Battle.net account.

### Techset
A set of compiled shaders. A material draws only with a technique that a loaded techset has.

### Thunk
A small piece of generated code that jumps somewhere else. cw-mod builds one per guarded engine function so the call appears to come from inside the game.

### Trigger list
See Entity list.

### XBlock
One of the 13 memory blocks a zone's data is laid out in.

### XUID
A player's 64-bit id.

### zm_common
The zone every Zombies map loads. It holds the shared scripts, the menus and the machines.

### zm_silver
The zone name of Die Maschine.

### Zone
A named fastfile and what it loads. A map is a set of zones.

### Zone trace
A recording of where each asset starts while the game loads a zone (`.mktrace`). mapkit's tools need it to read a level zone.

### zonekit
mapkit's library for reading and writing zones.

<!-- sources: cw-mod docs/ROADMAP.md ("Terms"), .claude/skills/bocw-reverse-engineering/SKILL.md, docs/mapkit-roadmap.md, docs/mapkit-map-anatomy.md, client/game/arxan_call.hpp @ 36b1f18 + working tree, 2026-10-07 -->

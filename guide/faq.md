# Questions

> Short answers. Each links to the page with the detail.

## The basics

### Do I need to own the game?

Yes. The mod is a change to your own copy. It ships no game files and does not help anyone get the game. See [Legal](/legal.md).

### Which version of the game?

Build **1.34.0.15931218** on PC. The mod's addresses are for that build only.

### Is there a download, or do I build it?

These guides build the mod from its source. It takes two commands. See [Install](/guide/install.md).

### Which modes does it cover?

Zombies. The project's aim is to keep this version of Zombies playable and moddable. Multiplayer and Campaign are not what it works on.

### Does a modded game talk to Activision's servers?

Not to Demonware, the game's online backend. With the local backend on, every `demonware.net` name leads to your own PC. In online mode without it, those names are blocked. In offline and LAN mode the game's Demonware login is switched off.

## Playing

### Can I play with a friend?

Yes, two PCs in one match, in [LAN mode](/guide/play/lan.md) or [Online mode](/guide/play/online.md). It is tested on one home network. Over the internet through a VPN it is not tested yet. There is no matchmaking.

### Do I keep my level and my weapon levels?

Yes, in a save on your PC. See [Progression](/guide/play/progression.md).

### Is that my real account's progress?

No. The save is local and separate. Nothing is read from or written to your Activision account.

### Can I unlock everything?

`"unlock_all": true` answers every lock as open. It is built and not yet tested in the game. It changes nothing in your save.

### Do the store and the battle pass work?

No. They need Activision's marketplace, and bringing them back is not planned.

## Maps

### Can I make my own map?

Yes: the layout, the gameplay, your own models and textures, the sky, sun and fog, and the navmesh. Start at [Making a map](/guide/mapping/overview.md) and read [What you can and cannot make](/guide/mapping/limitations.md).

### Why Godot?

The game shipped with no map tools. mapkit reads and writes the game's files itself, and uses Godot only as the editor: it is free, needs no installer, and imports models from Blender.

### Can I add a new weapon, perk or zombie?

Not yet. No tool writes those assets.

### Can I use another map than Die Maschine as the base?

Not today. A custom map takes its zombies, weapons and shaders from Die Maschine.

### Can I share my map?

Share its source, never the built zone. See [Sharing a map](/guide/mapping/sharing.md).

### My friend and I get "Clientfield Mismatch" on a custom map.

You have different builds of the map, or one of you has an old-format map. See [Custom maps](/guide/play/custom-maps.md).

## Scripts

### Can I write my own scripts?

Yes: [game scripts](/guide/scripting/gsc.md) in a match and [Lua](/guide/scripting/ui-scripts.md) in the menus.

### Can I change the game's text?

Yes, from a list in the settings file. See [Replacing the game's text](/guide/scripting/ui-text.md).

## When something breaks

### Where is the log?

`<game>\cw-mod\client.log`. See [Running the game](/guide/running.md).

### The game shows three odd words and a number.

That is the game's code name for an error. The log line before it has the cause. See [Help](/guide/troubleshooting.md).

### How does it all work inside?

That is the other half of these docs: [How we did it](/re/).

<!-- sources: cw-mod README.md, docs/ROADMAP.md, tools/dwserver/README.md (redirect and block), docs/mapkit-roadmap.md (M5: why Godot), the guide pages this one links to @ 36b1f18 + working tree, 2026-10-08 -->

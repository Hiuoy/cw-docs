# Game scripts (GSC)

> Run your own GSC scripts in a Zombies match. **Status:** Done (2026-09-23); client scripts and per-map scripts 2026-09-26.

GSC is the game's own script language: rounds, perks, the Mystery Box and every quest are written in it. The mod loads compiled scripts from a folder and hands them to the game.

## Before you start

- [ACTS](https://github.com/ate47/atian-cod-tools) on your PATH. It compiles GSC for Cold War.
- `"scripts": true` in `cw-mod.json` (the default).
- A reference for the game's own script functions. The community's decompiled Cold War scripts are the usual one.

## Steps

1. **Write a script**, in a folder of its own. The smallest useful one:

   ```c
   #using scripts\core_common\callbacks_shared;
   #using scripts\core_common\system_shared;

   #namespace my_mod;

   function private autoexec __init__system__()
   {
       system::register( #"my_mod", &preinit, undefined, undefined, undefined );
   }

   function private preinit()
   {
       callback::on_spawned( &on_player_spawned );
   }

   function private on_player_spawned()
   {
       self endon( #"disconnect" );
       wait 5;
       self iprintlnbold( "my_mod is running" );
   }
   ```

2. **Compile it.**

   ```powershell
   acts gscc -g cw -o my_mod <folder with your .gsc>
   ```

3. **Copy** `my_mod.gscc` into `<game>\cw-mod\scripts\`. Any file name and any subfolder work.
4. **Start a Zombies match.** The folder is read when the game starts. The overlay's Scripts tab has **Reload folder** for a script you changed; in a match, the change waits for the next match.

## Two ways a script is used

| Way | When | What happens |
|---|---|---|
| **Inject** | The script's name is new | It is added to every Zombies match. Its `autoexec` functions run like the game's own. |
| **Replace** | The script's name is a stock script's name | The game gets yours instead of its own. Yours must provide everything the original did. |

To replace, give the script the stock name when you compile. The `.gsc` is part of the name:

```powershell
acts gscc -g cw --name scripts/zm_common/foo.gsc -o foo <folder>
```

Or name the file after the stock script's hash: `0x<16 hex digits>.gscc`. To find hashes, switch on **Record script requests** under the Scripts tab's Diagnostics; `acts -t lookup <hash>` names most of them.

Client scripts (`.cscc`, compiled with ACTS `--name-client`) can only replace.

## The samples

They are in the repository's `gsc\` folder, each with its build line at the top.

| File | Does |
|---|---|
| `cwmod_hello.gsc` | Prints a counter. The smallest proof that a script runs. |
| `cwmod_cash.gsc` | Gives every player 1000 points every 3 seconds |
| `cwmod_trainer.gsc` | Adds crystals, Pack-a-Punches your weapon to tier 3, refills ammo |
| `cwmod_devtools.gsc` | God mode and noclip (hold aim, press melee) for walking a map you are building |

## Rules that bite

- **Clientfields must match.** If your server script registers a clientfield, the client side must register the same one, or players are dropped with "Clientfield Mismatch". The mod then writes both lists to `cw-mod\clientfields_server.txt` and `clientfields_client.txt`, and a `Clientfield diff` line to the log.
- **A reference to a function that is not linked gives `undefined`**, not an error. The Scripts tab counts these as "unresolved".
- **String literals work.** The loader prepares them before the game sees the script.

## Seeing what happened

- Text a script prints with `iprintln` or `iprintlnbold` also goes to the log as a `(Script)` line.
- The Scripts tab lists each script: inject or replace, its name hash, how often the game asked for it, and why a script was rejected.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The script is not in the Scripts tab | It is not a `.gscc` in `cw-mod\scripts`, or `"scripts"` is `false`. |
| The tab shows an error for the script | The file is not a Cold War script object. Compile with `-g cw`. The tab gives the reason. |
| "Host ... was linked outside the loader; injection was skipped" | The game linked that script before the loader could add yours to it. Start a new match. |
| Nothing happens in the match | Your `autoexec` did not register anything, or the code waits for an event that already passed. |
| Dropped with "Clientfield Mismatch" | See the rule above. |

**How it works inside:** [The GSC VM and the script loader](/re/engine/gsc-vm.md), [Script strings](/re/engine/gsc-strings.md).

<!-- sources: cw-mod client/scripting/scripting.hpp, client/overlay/tabs/scripting.cpp, gsc/cwmod_hello.gsc, gsc/cwmod_cash.gsc, gsc/cwmod_trainer.gsc, gsc/cwmod_devtools.gsc, docs/mapkit-plan.md (P1 step 1: clientfield diff), docs/ROADMAP.md (section 1) @ 36b1f18 + working tree, 2026-10-08 -->

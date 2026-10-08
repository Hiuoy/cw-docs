# Install

> Build the mod's DLL and put it next to the game's executable. **Status:** Done.

## Before you start

- Black Ops Cold War, build **1.34.0.15931218**, in a folder you can write to. These pages call it `<game>`: the folder that holds `BlackOpsColdWar.exe`.
- Visual Studio 2022 or newer, with the "Desktop development with C++" workload.
- The cw-mod source: [github.com/Hiuoy/cw-mod](https://github.com/Hiuoy/cw-mod). Everything it needs to build is in the repository.

## Steps

1. **Generate the solution.** In the cw-mod folder:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
   ```

2. **Build.**

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\build.ps1
   ```

   The script picks an installed C++ toolset by itself. The result is `build\t9_vs2022\x64\client\discord_game_sdk.dll`.

3. **Keep the game's own file.** `<game>\discord_game_sdk.dll` is the game's Discord library. Copy it somewhere safe: the mod takes its place, and you need it to go back.

4. **Put the mod in and start the game.**

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\launch.ps1 -GamePath "<game>"
   ```

   It copies the DLL to `<game>\discord_game_sdk.dll` and starts the game. The path is remembered, so later runs need no `-GamePath`.

5. **Check the first boot.**
   - A console window opens beside the game and prints the mod's log.
   - In the main menu, press **Insert**. The overlay opens, and its Home tab shows the game version.
   - The folder `<game>\cw-mod` now exists, with `cw-mod.json` (the settings, all at their defaults) and `client.log`.

## How the game loads it

At start-up the game loads `discord_game_sdk.dll` from its own folder and calls its `DiscordCreate` function. The mod's DLL has that name and that function, so the game loads the mod. No game file is patched on disk. The game's Discord features are off while the mod is in.

## Updating and removing

| To | Do |
|---|---|
| Update | Close the game (it keeps the DLL open), build again, run `launch.ps1` again. |
| Remove | Close the game and put the game's own `discord_game_sdk.dll` back. |
| Remove everything | Also delete `<game>\cw-mod`. Your saves are not in there: see [File structure](/guide/file-structure.md). |

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| `DLL not built. Run scripts\build.ps1 first.` | The build did not finish. Read its last lines for the error. |
| `No C++ PlatformToolset found` | Install the "Desktop development with C++" workload in Visual Studio. |
| `LNK2019` errors after you added a source file | Run `bootstrap.ps1` again: the project files are generated. |
| No console window and no overlay | The DLL is not in `<game>`, or it has another name. |
| The game closes during start-up | See [Running the game](/guide/running.md). |

**How it works inside:** [The client: one DLL](/re/client/overview.md).

<!-- sources: cw-mod scripts/bootstrap.ps1, scripts/build.ps1, scripts/launch.ps1, client/main.cpp (DiscordCreate), common/logger/log_service.cpp, client/overlay/d3d12_hook.cpp (VK_INSERT), CONTRIBUTING.md @ 36b1f18 + working tree, 2026-10-07 -->

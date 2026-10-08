# Menu scripts: the Lua loader

> How cw-mod runs your own Lua **source** inside the game's menu state, how that Lua talks back to the DLL, and the one mistake that ends the process with no error to catch. **Status:** Done. The loader and the CUSTOM MAPS tab passed in game 2026-09-26.

## In short

- The game ships its menus as bytecode, but it kept the whole parser. `lua_load` takes text.
- cw-mod loads every `cw-mod\ui_scripts\*.lua` right after the game's `ui/main.lua`, and again whenever a file changes.
- Hashed names are written `@"Name"`. The lexer needs a hash callback that retail never sets, so the loader puts its own in for the length of the parse.
- Lua reaches the DLL through a print native that is compiled out of retail: `Engine[@"PrintInfo"](0, "cw-mod <command>")`.
- A plain string handed to the game's localize call **ends the process**.

## Loading

```text
lua_load(L, reader, data, chunkname)
  -> luaD_protectedparser
     -> bytecode reader, or the text parser (lj_parse)
```

| Step | What the loader does | Why |
|---|---|---|
| 1 | Reads `L->top`, `L->base`, the stack end and `global_State`. Refuses when fewer than 8 slots are free. | Guarded reads only |
| 2 | Remembers the stack depth **relative to `L->base`** | The parser can reallocate the stack |
| 3 | Writes its own function into `global_State + 816`, the lexer's hash callback | See below |
| 4 | Calls `lua_load` through an [Arxan thunk](/re/client/arxan.md) | Four arguments: exactly the thunk's limit |
| 5 | Puts the previous callback back | |
| 6 | Calls the loaded function with `LUI_ProtectedCall`, one result | A raise is caught and logged |
| 7 | Sets `L->top` back to the remembered depth, on every path | |

One `(UiScripts)` line per run goes to the log: the returned string or number, `ok`, or the error.

## Hash literals

The game's lexer adds two tokens to Lua: `@"text"` and `@name`. Both become a hashed name. To hash the text it calls a function pointer in the global state, and it **asserts** the pointer is set. Retail chunks are all bytecode, so retail never sets it: parsing a hash literal without help aborts.

The loader's callback takes three forms:

| You write | You get |
|---|---|
| `@"DirectorPrivateZM"` | The engine's hash of the text (63 bits) |
| `@"0x9E283FFCDB06CE1"` | A hash as the Lua dump prints it (60 bits): the loader looks up the hashed name already in the state with those bits |
| `@"0x39E283FFCDB06CE1"` | A hash in full, as written |

Hashed names are interned by their exact 64-bit value, in a table at `global_State + 16` (mask at `+24`). Two names that share 60 bits are different objects, which is why the short form needs the lookup. When none or more than one matches, the number is used as written and the log says so.

## When scripts run

1. The `LUI_RunFile` detour sees `ui/main.lua` finish. This is before the engine sends `main_loaded` and opens the first menu.
2. A generated prelude sets `CWMOD.maps` and `CWMOD.active` from the [map loader](/guide/play/custom-maps.md).
3. The built-in scripts run: the CUSTOM MAPS tab and the SERVER BROWSER menu. A file of the same name in the folder replaces one.
4. The folder runs in file-name order.
5. Once a second the tick looks at the folder. A file that changed or appeared runs again **in the same state**.

So a script must be safe to run twice. Keep the original of anything you wrap in a global, and set it once. The game's menu state is rebuilt at map load and on return to the menus, and the scripts then run from step 1 again.

## The command channel

`Engine.PrintInfo`, `PrintWarning` and `PrintError` exist as natives, but their bodies are compiled out. cw-mod detours the wrappers to read their arguments. A text that starts with `cw-mod ` is a command, not a print:

| Command | Effect |
|---|---|
| `cw-mod map <id>` | The CUSTOM MAPS pick. `cw-mod map` alone means none. |
| `cw-mod browser open` / `close` | The SERVER BROWSER menu came up or went away |
| `cw-mod browser join <xuid>` | Join that listed host on the next tick |
| `cw-mod log <text>` | A `(UiScripts)` line in the log |

The other way, DLL to Lua: while the browser menu is open, the tick runs a small chunk that only **sets data** in `CWMOD.browser`. The menu's own timer reads it, so no widget changes outside the UI's update.

## The localize trap

The game's Lua passes nearly all widget text through `Engine.LocalizeHash`, often twice.

| What the call gets | What it does |
|---|---|
| A string that starts with byte 21 | Returns it untouched. This is the form of its own results: byte 21, the text, byte 20. |
| Any other string, or a hash | Treats it as the **name of a localize entry** |
| A name with no entry | Shows "UI Error 100004", then the asset lookup raises its fatal error for a missing localize asset and the process ends |

No `pcall` sees that exit: it is not a Lua error. The first SERVER BROWSER build ended the game on the Zombies main screen this way (2026-10-07).

- Text of your own for a stock widget: `"\021My text\020"`.
- A button prompt label: a hash the game's own menus use.
- An element's own `setText` takes plain text.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `lua_load` | 0xD288AE0 | 0x7FF729E48AE0 | `int (void* L, reader, void* data, const char* chunkname)` | Caller-guarded |
| `luaD_protectedparser` | 0xD288B70 | 0x7FF729E48B70 | | Picks bytecode or text |
| `lj_parse` | 0xD29D720 | 0x7FF729E5D720 | | The text parser |
| `LUI_ProtectedCall` | 0x56D3FA0 | 0x7FF722293FA0 | `int (void* L, int nargs, int nresults, int errfunc)` | Runs the chunk |
| `LUI_RunFile` | 0xAFCCCD0 | 0x7FF727B8CCD0 | `u8 (void* L, const char* name)` | The seam after `ui/main.lua` |
| `LuaNative_PrintInfo` | 0x1D7C050 | 0x7FF71E93C050 | `int (void* L)` | The command channel |
| `LUI_ReportUiErrorCode_cand` | 0x5702390 | 0x7FF7222C2390 | | Shows "UI Error 100004" and returns |
| `lj_strfmt_obj` | 0xD290E30 | 0x7FF729E50E30 | | `tostring` of a hashed name gives `xhash:0x...` |

## How we found it

- The engine has one caller of `lua_load`, the chunk-asset loader, and it only ever passes bytecode. Following `lua_load` down showed both readers behind it.
- The first test script with `@"..."` would have aborted in the lexer's assert. Reading the lexer first showed the callback slot.
- A native method called by string key found a different function. In the decompiled text both forms print alike, by name. The bytecode tells them apart: `tools/lua_disasm.py` shows a hashed key as `KXHASH`.

## Limits

- A script runs in the menus' state only. It cannot touch the game's GSC.
- Built on stock widgets: one that was never fed the data it expects can raise later, from its own handlers.
- Turn the whole feature off with `"ui_scripts": false`.

## See also

- [Menu scripts, the guide](/guide/scripting/ui-scripts.md): how to write one
- [Lua and the menus](/re/engine/lua-lui.md)
- [UI text](/re/engine/ui-text.md)

<!-- sources: cw-mod client/game/ui_scripts.hpp, ui_scripts.cpp, ui_scripts_custom_maps.hpp, client/game/dump_anchors.hpp (lua_load, DecryptString notes of 2026-10-07, print natives), client/hooks/hook.cpp (print detours) @ 36b1f18 + working tree, 2026-10-08 -->

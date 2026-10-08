# Menu scripts (Lua)

> Run your own Lua in the game's menus: add a tab, change a list, wrap a menu function. **Status:** Done (2026-09-26). The CUSTOM MAPS tab is built this way.

The game's menus are written in Lua. The mod runs every `.lua` file in `<game>\cw-mod\ui_scripts\` inside the same Lua state, as source text.

## How a script runs

| When | What |
|---|---|
| Right after the game loads its main menu script, before the first menu opens | The mod's built-in scripts, then your files in file-name order |
| Once a second while the game is up | Any file that changed or appeared is run **again**, in the same state |
| After each run | One `(UiScripts)` line in the log: the value the script returned, `ok`, or the Lua error |

Because a changed file runs again, you can edit a script and see the result without restarting the game. It also means **a script must be safe to run twice**.

A file named like a built-in (`custom_maps.lua`, `server_browser.lua`) replaces that built-in.

## A first script

```lua
-- hello.lua: prove the script ran, and say so in the log.
local print_info = Engine[@"PrintInfo"]
print_info(0, "cw-mod log hello from ui_scripts")
return "hello loaded"
```

Save it as `cw-mod\ui_scripts\hello.lua`. The log gets `(UiScripts) hello from ui_scripts` and a line with `hello loaded`.

## The rules of this Lua

The menus' Lua is not stock Lua. These rules cost a crash each to find.

| Rule | Do this |
|---|---|
| Global variables cannot be created by assignment | `rawset(_G, "MYMOD", {})`, then use `rawget(_G, "MYMOD")` |
| Engine functions are stored under a **hash** of their name | `Engine[@"PrintInfo"]`, not `Engine.PrintInfo`. The dot form finds a different function. |
| `Engine` ignores a plain assignment | `rawset(Engine, key, my_function)` |
| A widget's native methods are stored under a hash too | `element[@"GetModel"](element)` |
| Methods the menus' own Lua defines use plain names | `element:setClass(...)` works as written |
| `@"Text"` is a hash literal | The game's name hash of `Text`. `@"0x..."` takes a hash as a number. |
| Text handed to a stock widget is treated as the **name of a text entry** | Wrap your own text: `"\021My text\020"`. A plain string that names no entry **ends the game**. |
| An element's own `setText` | Takes plain text |

## Wrapping a game function safely

Keep the original once, in a table that survives a re-run:

```lua
rawset(_G, "MYMOD", rawget(_G, "MYMOD") or {})
local S = rawget(_G, "MYMOD")

local director = CoD[@"0xA568193B170CB53"]        -- a game utility table, by its hash
local SELECT = @"0x8776F086512EAA0"               -- one of its functions

S.original = S.original or director[SELECT]       -- kept from the FIRST run only
director[SELECT] = function(menu, element, controller, ...)
    -- your code here
    return S.original(menu, element, controller, ...)
end
return "wrapped"
```

Without the `S.original or` part, the second run would wrap your own wrapper.

## Talking to the mod

A script sends the mod a line through the print function. The text must start with `cw-mod `.

| Line | Effect |
|---|---|
| `cw-mod log <text>` | Writes `<text>` to the log as a `(UiScripts)` line |
| `cw-mod map <id>` | Picks a custom map, as the CUSTOM MAPS tab does. `cw-mod map` alone picks none. |

The mod gives scripts a table before they run: `CWMOD.maps` (the listed custom maps: id, title, base, description) and `CWMOD.active`.

## Finding names

Menu functions have no readable names in the game, only hashes. The built-in `custom_maps.lua` (in the repository, `client\game\ui_scripts_custom_maps.hpp`) is the worked example: it adds a tab, a page and a list, and wraps two functions. To find other hashes you have to read the menus' own Lua, which is reverse-engineering work.

## Limits

- No readable names: you work with hashes.
- A mistake in a menu callback can leave a menu broken until you restart.
- Off with `"ui_scripts": false`. That also removes the CUSTOM MAPS tab.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| A `(UiScripts)` line with a Lua error | Read it: it names the file and the line. |
| "attempt to call a nil value" on an Engine function | You used the dot form. Use `Engine[@"Name"]`. |
| The game closes when your menu opens | Plain text reached a stock widget. Wrap it as `"\021text\020"`. |
| Your change seems to apply twice | The script ran again and wrapped its own wrapper. Keep the original as shown above. |

**How it works inside:** [Menu scripts: the Lua loader](/re/engine/ui-scripts.md), [Lua and the menus](/re/engine/lua-lui.md).

<!-- sources: cw-mod client/game/ui_scripts.hpp, client/game/ui_scripts_custom_maps.hpp, docs/ROADMAP.md (sections 1 and 2) @ 36b1f18 + working tree, 2026-10-08 -->

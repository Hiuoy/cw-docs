# UI text

> Every localized string the game shows passes through one function on its way out. That function is where cw-mod swaps text. **Status:** Done, in game 2026-09-25.

## In short

- A localized string is an asset of type `0x1D`, keyed by the hash of its name. Its text is stored **encrypted**.
- There is no central "get string" function in this build. About 100 places look the asset up and each calls `DecryptString` itself.
- `DecryptString` decrypts in place and returns plain text untouched. So its return value is the one point where any UI string can be recognised and replaced.

## How it works

```c
char* DecryptString(char* s);
```

| Step | Detail |
|---|---|
| First test | `if ((*s & 0xC0) != 0x80) return s;` A string that does not start with a byte in `0x80..0xBF` is already plain. |
| Otherwise | Decrypts **in place**. The first byte is overwritten, so every later call on the same string takes the early return. |
| Header byte `0x8B` | The identity cipher: the text follows as it is |
| Locking | One recursive spinlock before the body |

Because plain text is passed back untouched, a replaced string is safe to hand to code that may call `DecryptString` on it again.

Callers include Lua's `Engine.Localize` and the native UI code alike.

## Functions

| Name | RVA | IDA address | Signature | Role |
|---|---|---|---|---|
| `DecryptString` | 0xC990AE0 | 0x7FF729550AE0 | `char* (char* s)` | The choke point. No caller guard. |
| `LuaNative_Localize_Impl` | 0x878C140 | 0x7FF72534C140 | `int (void* L)` | The body behind `Engine.Localize` |
| `Load_LocalizeentryAsset` | 0x1C1EAF0 | 0x7FF71E7DEAF0 | | Loads a type-`0x1D` asset from a zone |

## What cw-mod does

`"ui_text"` in [cw-mod.json](/guide/settings.md) maps "text the game shows" to "text to show instead". The detour is installed only when `"ui_text"` or `"ui_text_log"` is set, because every decrypted string pays for it.

```text
out = original(s)
h   = FNV-1a over out, ASCII case folded
if the table has h, and the lengths and the folded text match:  return the replacement
return out
```

| Choice | Reason |
|---|---|
| Match on the **whole** string, case ignored | Menus often upper-case a string after localizing it. `CONNECTING` on screen can be `Connecting` in the asset. |
| The table is built before the detour is enabled and never changed | The hook runs on any thread, with no lock |
| A replacement that starts with a byte in `0x80..0xBF` is refused | The engine would decrypt it if it saw it again |
| `"ui_text_log": true` lists each distinct string once, up to 4,000 | To find the exact text when a key does not match |

A replacement must keep the original's placeholders (`&&1` and so on). The caller fills them in after `DecryptString` returns.

## How we found it

- The search for one "localize" function found none: the lookups are spread over about 100 call sites.
- All of them shared one callee. Its first instruction is the `0xC0`/`0x80` test, and its prologue has no caller guard, so it can be hooked and called freely.

## Limits

- Only localized text. A script's own plain print, or text a menu builds from numbers, never passes here.
- A string used in several places changes in all of them.
- The match is exact. Use `"ui_text_log"` and copy the text from the log.

## See also

- [Replacing the game's text](/guide/scripting/ui-text.md): the guide
- [Menu scripts](/re/engine/ui-scripts.md): the localize trap, which is about names, not text

<!-- sources: cw-mod client/hooks/impl/game/DecryptString_UiText.cpp, client/game/dump_anchors.hpp (kDump_DecryptString), client/hooks/hook.cpp, .claude/skills/bocw-reverse-engineering/SKILL.md (section 9) @ 36b1f18 + working tree, 2026-10-08 -->

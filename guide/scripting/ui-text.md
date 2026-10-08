# Replacing the game's text

> Change any text the game shows, from a list in `cw-mod.json`. **Status:** Done (2026-09-25).

## What it does

`"ui_text"` in `cw-mod.json` is a list of pairs: the text the game shows, and the text to show instead. It works for every localized string, in menus and in a match.

```json
{
  "ui_text": {
    "Connecting to Call of Duty™ Online Services.": "Connecting to cw-mod."
  }
}
```

## Steps

1. **Find the exact text.** Set `"ui_text_log": true` and start the game.
2. **Open the screen** that shows the text.
3. **Read the log.** `cw-mod\client.log` now has one `(UiText)` line for each piece of text the game showed. Copy the text from there.
4. **Add the pair** to `"ui_text"`, set `"ui_text_log"` back to `false`, and restart the game.

## Rules

| Rule | Detail |
|---|---|
| The whole string must match | A part of a sentence does not match. |
| Upper and lower case do not matter | Menus often show a string in capitals that is stored in mixed case. `CONNECTING` on screen still matches `Connecting`. |
| Keep the placeholders | A string with `&&1` or `&&2` gets values put in afterwards. Your text must keep them. |
| Plain JSON | A quote inside the text is written `\"`. |

## Limits

- Only text that comes from the game's text entries. Text drawn in a picture, and text a script builds letter by letter, does not pass through.
- One replacement per exact string. The same words in two different entries need two pairs only if the strings differ.
- The log lists up to 4,000 different strings in one run.
- The file is read when the game starts. Restart to see a change.

## If it goes wrong

| What you see | Cause and fix |
|---|---|
| The text does not change | The key is not the whole string. Use `"ui_text_log"` and copy it exactly, with its punctuation. |
| The log says an entry was skipped | The value is not a text, or the key is empty. |
| A number or a name is missing from the new text | You dropped a `&&1` placeholder. |
| Every setting is back at its default | The file is no longer valid JSON. See [Settings](/guide/settings.md). |

**How it works inside:** [UI text](/re/engine/ui-text.md).

<!-- sources: cw-mod client/hooks/impl/game/DecryptString_UiText.cpp (header), client/game/settings.cpp (ui_text parsing), docs/ARCHITECTURE.md ("Boot profile" table) @ 36b1f18 + working tree, 2026-10-08 -->

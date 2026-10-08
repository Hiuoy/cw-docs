# Unlock-all

> Where the game decides that something is locked or not owned, and how one setting answers those questions without writing anything. **Status:** Built 2026-10-07, not run in the game yet.

## In short

- A lock is never a stored flag. It is a **question** the menus and the match ask a handful of native predicates.
- Each predicate gets a detour that asks the engine first and changes only a "locked" or "not owned" answer.
- Nothing is written to a save or to the engine's stats. Turn the setting off and every lock is back as the save has it. Progress keeps recording underneath.
- Off by default: `"unlock_all": true` in [cw-mod.json](/guide/settings.md). It works the same offline, in LAN and online.

## The four kinds of lock

### 1. Level rules

One module holds every level rule: item locks, "is purchased", unlock levels, the "new" markers, unlock tokens. All 26 of its rule sites start with the same test: the rules are **off** when `Com_SessionMode_IsProgressionExemptContext()` is true. That function means "match type 0 on one of two exempt playlists".

The detour answers yes, but only to a caller whose return address is **inside that module**. The function's other 54 callers (XP, storage, matchmaking) keep the real answer. So the level rules are switched off the engine's own way.

### 2. Rules that test is not part of

All return true for "locked".

| Predicate | Decides | Reads |
|---|---|---|
| `Progression_IsItemLocked` | Weapons, equipment, perks behind a level | The level rule, or the item's loot id in the inventory |
| `Progression_IsAttachmentLockedInBlock` | An attachment behind a weapon level | Required weapon XP against `progression.weapons[w].xp` |
| `Progression_IsAttachmentSlotLocked` | An attachment slot | The slot's weapon level |
| `Progression_IsItemOptionLockedCore` | Camos and reticles | The option's challenge stat against its tier target, and an entitlement mask. Calls itself for a prerequisite. |

A slot the weapon does not have is also reported as "locked" by the engine. That answer is kept: the detour checks the weapon's attachment count first.

### 3. Ownership

Blueprints, bundles, operators, battle pass rewards and challenge-reward weapons are all one thing: "the quantity of item id N in the Demonware marketplace inventory". That inventory never loads on the local backend (measured: state 1, 0 items).

| Predicate | Note |
|---|---|
| `Inventory_GetItemQuantity` | 21 call sites, every one an ownership read. Items 500000 to 500002 are the **trial state** and keep their 0. |
| `Loot_GetItemQuantity` | The same, behind "loot enabled" and "inventory ready" |
| `Entitlement_IsOwned` | `Engine.HasEntitlement` and entitlement-locked weapon options |
| `DwFetch_IsInventoryReady` | 13 loot functions answer nothing until it is true. The lobby gate also asks it, and keeps the real answer. |

### 4. The battle pass

Eight bytes per season in the user's loot block: owned, tier, XP. Only a Demonware event writes them. The getters are answered "owned" and "tier 100". The menus read a UI model that the engine refreshes on inventory events, which never arrive here, so the tick calls the refresh itself.

## Functions

| Name | RVA | IDA address | Signature |
|---|---|---|---|
| `Com_SessionMode_IsProgressionExemptContext` | 0xC1BC2D0 | 0x7FF728D7C2D0 | `bool ()` |
| `Progression_IsItemLocked` | 0x75795C0 | 0x7FF7241395C0 | `bool (int mode, uint controller, int itemIndex)` |
| `Progression_IsAttachmentLockedInBlock` | 0x75791E0 | 0x7FF7241391E0 | `char (int mode, void* statsBlock, uint itemIndex, int slot, char)` |
| `Progression_IsAttachmentSlotLocked` | 0x7578F10 | 0x7FF724138F10 | `bool (uint mode, uint controller, uint itemIndex, int slot)` |
| `Progression_IsItemOptionLockedCore` | 0x757AC90 | 0x7FF72413AC90 | `char (uint mode, uint controller, uint itemIndex, uint optionIndex, char skipPrerequisite)` |
| `Inventory_GetItemQuantity` | 0xB35B3E0 | 0x7FF727F1B3E0 | `u64 (int controller, uint itemId)` |
| `Loot_GetItemQuantity` | 0xAD41C60 | 0x7FF727901C60 | `u64 (uint controller, u64 itemId, u64, u64)` |
| `Entitlement_IsOwned` | 0xB953340 | 0x7FF728513340 | `char (int controller, u64 nameHash)` |
| `DwFetch_IsInventoryReady` | 0xB35B990 | 0x7FF727F1B990 | `bool (uint controller)` |
| `Loot_GetBattlePassOwned` | 0xAD41460 | 0x7FF727901460 | `char (uint controller, int season)` |
| `Loot_GetBattlePassRank` | 0xAD414F0 | 0x7FF7279014F0 | `u64 (uint controller, int season)` |
| `Loot_UpdateBattlePassModels` | 0xB35DD00 | 0x7FF727F1DD00 | `void (int controller)` |

The item table: `table + 409832 * mode + 320 * item`. An entry is valid when the byte at `+23` has bit 4; the row starts at `+16` and its attachment count is the byte at row `+84`.

## How the detours stay honest

- A detour that needs the engine's own answer first raises a per-thread flag. While it is up, every unlock-all detour passes through, so the engine's nested questions get real answers.
- Each kind counts how often it was asked and how often it changed the answer. The log gets at most one summary line a minute.
- The level-rule and inventory-ready detours decide by **return address**, so one function can answer differently to different callers.

## Limits

- Not run in the game yet.
- Not changed: which items exist, the level and weapon levels shown, the trial state.
- Seven Zombies rewards are read by the menus' Lua straight from the save, with no native in between. They stay locked.

## See also

- [Progression](/re/engine/progression.md)
- [Saves and progression, the guide](/guide/play/progression.md)

<!-- sources: cw-mod client/game/unlock_all.hpp, client/game/dump_anchors.hpp ("unlock_all" section, decompiled 2026-10-07), client/hooks/hook.hpp, docs/ROADMAP.md (section 4) @ 36b1f18 + working tree, 2026-10-08 -->

# Hashes and names

> The game ships almost no names: dvars, menus, script functions and assets are all known by a hash. This page gives the hash functions and the ways a name is won back.

## In short

- One hash names nearly everything: **64-bit FNV-1a over the lowercased name, top bit cleared** ("63-bit").
- The menus' Lua shows the same hash with only its **low 60 bits**.
- GSC function and namespace ids use a different **32-bit** hash.
- There is **no hash-to-name table** in the image. Names are recovered by hashing candidates.

## The functions

```python
def fnv63(s):
    """Com_HashString: dvars, menus, Lua natives and methods, asset names, GSC #"..." literals,
    and script paths WITH their extension."""
    h = 0xCBF29CE484222325
    for c in s.encode():
        if 65 <= c <= 90:          # lowercases ASCII only
            c += 32
        h = ((h ^ c) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h & 0x7FFFFFFFFFFFFFFF

def canon32(s):
    """GSC function and namespace ids. Not the textbook Jenkins one-at-a-time."""
    h = 0x4B9ACE2F
    for c in s.lower().encode():
        t = (c + h) & 0xFFFFFFFF
        t = (t ^ (t << 10)) & 0xFFFFFFFF
        h = (t + (t >> 6)) & 0xFFFFFFFF
    h = (9 * h) & 0xFFFFFFFF
    return (0x8001 * (h ^ (h >> 11))) & 0xFFFFFFFF
```

## Values to check your own code against

| Input | Function | Value |
|---|---|---|
| `lobby` | fnv63 | 0x1CCAE3B6EF72F533 |
| `com_maxclients` | fnv63 | 0x65A2E5EE8014325D |
| `nodw` | fnv63 | 0x3C2F09BAD1862417 |
| `printinfo` | fnv63 | 0x28C5711DAACC99F4 |
| `player_xuid` | fnv63 | 0x10CBB4E93D94E4F3 |
| `scripts/core_common/system_shared.gsc` | fnv63 | 0x39C5D5881CC195B0 |
| `iprintlnbold` | canon32 | 0x061F222E |

## Where each hash is used

| Thing | Hash | Note |
|---|---|---|
| Dvar names | fnv63 | The engine masks the top bit before comparing |
| Menu names, Lua native names, Lua method names, enum keys | fnv63 | |
| Asset names | fnv63 | A hash with the top bit **set** is a reference to an asset in another zone |
| GSC `#"text"` literals | fnv63 | |
| Script names | fnv63 of the path **with** `.gsc` or `.csc` | |
| GSC function and namespace ids | canon32 | |
| DDL member names (`player_xuid`, `rankxp`) | fnv63 | |
| The game-type registry | djb2 (5381, × 33) over the lowercased name | |

## The 60-bit form

The menus' decompiled Lua and its bytecode print a hash as `fnv63 & 0x0FFFFFFFFFFFFFFF`. So `Engine[0xA63E42B2FB6EC02]` in a dump is a native whose full hash has three more bits on top.

| In the bytecode | Form |
|---|---|
| A hashed-name constant | Tag `0x04`, then the high 32 bits and the low 32 bits, each as a ULEB number |
| A chunk's name | `x64:<63-bit hash of the path without .lua>.lua` |

The game keeps hashed names by their exact 64-bit value, so two names that agree in 60 bits are still different objects.

## Winning names back

`Com_FormatHash64` is just `sprintf("%016llx")`: the engine itself cannot turn a hash into a name. In order of yield:

1. **ACTS**: `acts -t lookup <hex...>`. Its index names GSC functions, most materials, models and weapons.
2. **Hash every string you have** (the dump, the zones, decompiled scripts) and join with the unknown hashes: `tools/hash_harvest_strings.py`.
3. **Word lists** of names from other titles, re-hashed. Their own hashes are useless here: another title uses another prime.
4. **Combinations**: build names from the words of names already found (`tools/dvar_hash_brute.py`).
5. **Meet in the middle**: FNV-1a can be run backwards, because its prime is odd.

Dvar names are fully stripped: none of the unknown ones appears as a string anywhere in the image. About 37 in 100 dvars have a name today.

## Three-word error names

The game shows an error as three words and a number, such as "Uniform 58 Guerrilla Boa". It is a rendering of a 32-bit error code, not a string in the image: hashing the words finds nothing. The log carries the code. See [Errors](/re/engine/errors.md).

## What cw-mod does

| Where | What |
|---|---|
| Overlay, Debug tab | A hash calculator, and a dump of every registered dvar hash |
| Overlay, Debug tab, **Recover names from memory** | Hashes every name-shaped string in the game's memory and joins it with the live dvar registry |
| The menu-script loader | Accepts `@"Name"` and `@"0x..."` hash literals. See [Menu scripts](/re/engine/ui-scripts.md). |

## See also

- [Developer tools](/guide/tools/dev-tools.md): the scripts, with usage
- [Dvars](/re/engine/dvars.md)

<!-- sources: cw-mod .claude/skills/bocw-reverse-engineering/SKILL.md (section 8), client/game/dump_anchors.hpp (kDdlMember_PlayerXuid, lua_load notes), tools/wordlists/README.md, client/overlay/tabs/debug.cpp @ 36b1f18 + working tree, 2026-10-08 -->

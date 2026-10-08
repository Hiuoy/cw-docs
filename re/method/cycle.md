# The work cycle

> How every finding on these pages was made: one loop, eight steps, and five rules that each cost a wasted test to learn.

## In short

- A plausible explanation is a **hypothesis** until one observation separates it from the others.
- Work **forwards from code that runs**, not backwards from an error text.
- The game's log decides what happened, never the screen.
- Each identified function is renamed and commented in the disassembler in the same sitting.
- A game start is the expensive step. Make each one answer several questions.

## The loop

```text
1 SYMPTOM     name the STAGE: a status code, a log line, a crash address, a 32-bit error code
2 STATIC      find the code for that stage, decompile it, read its contract and EVERY exit
3 HYPOTHESES  at least two, and the ONE observation that tells them apart
4 INSTRUMENT  a read-only detour or probe that logs pass-throughs and raw fields
5 RECORD      rename, comment, save; write the finding down
6 RUN         build, put the DLL in, start the game, read the log
7 VERDICT     from the log, never from what it looked like
8 FIX         only the measured cause; then expect the next wall right behind it
```

## The five rules

| Rule | What it cost to learn |
|---|---|
| A plausible mechanism is a hypothesis | Three of four "fixes" for one dialog were dead code: each shipped the first explanation that fitted. |
| Trace forwards from the per-frame function | "Who formats this message?" found four wrong choke points. "What does the frame function call?" found the right one at once. See [Errors](/re/engine/errors.md). |
| A silent hook proves nothing | Log pass-throughs, check the hook is in (the first byte of the target is `E9`), print the raw value next to every verdict. |
| Record in the same turn | A name that is not written down is found again next week. |
| Never wait on a slow tool | Read bytes from the dump file. Use the disassembler for cross-references, decompiling and names. |

## Making a game start count

- **Name the stage, not the symptom.** The engine usually says which gate failed: a login status such as `[status 25]`, an error string inside a parser (`Auth signature error`, `Bad recv counter`), or an error number. Decompile that stage's handler and read what it wants.
- **Measure what the game asks for before building anything.** A journal of every name resolved and every request sent comes first. Server code is written only after that list exists.
- **Buy several answers per start.** Make the variable part data (a settings key, a server flag) and not a rebuild. When the game retries after a failure, answer attempt N with variant N: the lobby server's `--sweep` settled four hypotheses in one start.
- **Prefer an experiment that discriminates.** Answering with error 5 on purpose separated "the envelope did not parse" from "the task decoder failed": the game echoed 5, so the envelope was fine.
- **Classify a gate before attacking it.** A predicate (signed in? which mode?) can be answered by a detour. A gate that needs data (playlists, an inventory) cannot: it needs the data.
- **Look for the engine's own lever first**: a shipped dvar, a code path another mode already uses, an existing stub. It is the cheapest fix and the safest.
- **After a milestone, the next crash is newly reached code**, not a regression.

## Reading the evidence

- A behaviour change without a code change needs an explanation too. The engine heals itself between starts: it retries, writes files back, counts boot crashes.
- Silence does not mean "it did not run". It can mean "dropped unread" or "the hook is not installed".
- A diagnostic's verdict is also a hypothesis. Print the raw value beside it.
- Garbled text in a log is an unexplained observation, not decoration. One such line was the uninitialised pointer that later killed the process. See [Lua and the menus](/re/engine/lua-lui.md).
- A count of call sites that could fail is an upper bound on a fear, not a measurement. Fifteen sites "that could crash" turned out to be one that ran.

## The lessons, one line each

| What happened | The rule it bought |
|---|---|
| Four fixes hooked paths the fatal error never took | Trace forwards from the running frame function |
| A detour on a guarded function broke every menu event | Call guarded functions through a thunk. See [Arxan](/re/client/arxan.md). |
| A 7-argument function called through the thunk crashed at map load | Count the arguments before using the thunk |
| A "save" button ran the load path | Decompile the direction parameter; check file times |
| "Not ready": ordering or absence? | Enumerate every exit. There were six causes. See [PlayerData](/re/engine/playerdata.md). |
| A dvar set "did nothing" | A server-flagged dvar drops main-thread writes. See [Dvars](/re/engine/dvars.md). |
| Hooks on an init function never fired | Init ran before the hooks went in. Find a seam that times itself. |
| A copied asset crashed the next zone | Re-point zone-local indices inside copies |
| A lobby reply was ignored | A wrong inner tag is dropped in silence |
| A server flag "did nothing" | Two servers had bound one port |
| A join was "refused" | It was our own join type. Read the verdict code. |
| A count came out as 1,683 | Count by call target, not by one encoding. It was 2,556. |

## See also

- [The binary and its dump](/re/method/binary.md)
- [Address and byte math](/re/method/address-math.md)
- [Tools](/re/method/tooling.md)

<!-- sources: cw-mod .claude/skills/bocw-reverse-engineering/SKILL.md (sections 0, 1, 10, 12) @ 36b1f18 + working tree, 2026-10-08 -->

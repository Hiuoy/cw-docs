#!/usr/bin/env python3
"""Build the function and globals index from the cw-mod sources.

Reads (never writes) a cw-mod checkout:
  client/game/dump_anchors.hpp     every kDump_<Name> = 0x7FF7... with its comment
  client/game/function_types.hpp   using <Name>T = <signature>;
  docs/, mapkit/, tools/dwserver/, client/, the RE skill: "Name 0x7FF7..." pairs in notes and comments

Writes, in this repo:
  tools/data/addresses.json        the index check_docs.py and fn.py read
  re/reference/functions.md        code addresses
  re/reference/globals.md          data addresses

No address is typed by hand: the RVA is the dump address minus the dump's image base.

Usage: python tools/gen_functions.py --cw-mod <path to cw-mod>
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

BASE = 0x7FF71CBC0000
IMAGE_SIZE = 0x20000000
# Sections of the fixed dump (file offset == RVA), from the RE playbook. Anything else is data.
CODE_RANGES = ((0x1000, 0x1000 + 0xD75B800), (0x1AF34000, 0x1AF34000 + 0x417DC00))

ROOT = Path(__file__).resolve().parent.parent
VA_RE = re.compile(r"0x7FF7[0-9A-Fa-f]{8}\b")
ANCHOR_RE = re.compile(
    r"^\s*(?:inline\s+)?constexpr\s+std::uintptr_t\s+kDump_(\w+)\s*=\s*(0x[0-9A-Fa-f]+)(?:ULL|ull|uLL)?\s*;\s*(?://\s*(.*))?$"
)
BANNER_RE = re.compile(r"^-{2,}\s*(.*?)\s*-{2,}$")
USING_RE = re.compile(r"\busing\s+(\w+?)T\s*=\s*([^;]+);", re.S)
IDENT_RE = re.compile(r"(?<![0-9A-Za-z_])[A-Za-z_~][A-Za-z0-9_]*(?:::[A-Za-z_~][A-Za-z0-9_]*)*")

# Words that may stand between a name and its own address ("Dvar_FindVar: impl 0x...").
SKIP_WORDS = {"impl", "at", "is", "the", "address", "addr", "dump", "va", "ida", "idb", "a", "an", "its", "now"}

# Names the notes abbreviate; the full name is in the same sentence of the source.
RENAMES = {
    "GetGameMode": "Com_SessionMode_GetGameMode",
    "GetNetworkMode": "Com_SessionMode_GetNetworkMode",
    "IsOnline": "Com_SessionMode_IsOnline",
}
# Pairs the pattern cannot read ("...TextureA/B_cand 0x...A0/0x...B0"), and addresses the notes describe
# without a symbol name. Each one names its source.
EXTRA = (
    ("Lighting_LinkStreamedTextureA_cand", 0x7FF7294938A0, "mapkit/zonekit/library_assets.hpp", ""),
    ("Lighting_LinkStreamedTextureB_cand", 0x7FF7294938B0, "mapkit/zonekit/library_assets.hpp", ""),
    ("(stock handler of GSC opcode 0x13)", 0x7FF71E7B6EB0, ".claude/skills/bocw-reverse-engineering/SKILL.md",
     "Copies its operand into a dead local and does nothing else. The loader patches its own handler into the table."),
    ("(return gadget for ArxanCall thunks)", 0x7FF71D0B3D2C, "client/game/arxan_call.hpp",
     "The return point after an in-image call: add rsp,28h; retn."),
    ("(Dvar_GetInt's thunk)", 0x7FF71DA42540, ".claude/skills/bocw-reverse-engineering/SKILL.md",
     "An Arxan split thunk that dispatches on the return address. Calling it from another module faults."),
    ("(Dvar_FindVar's thunk)", 0x7FF728C72230, ".claude/skills/bocw-reverse-engineering/SKILL.md",
     "An E9 jump to Dvar_FindVar. Hook the implementation, not this."),
    ("p_dvar_com_maxclients", 0x7FF72CCC1020, ".claude/skills/bocw-reverse-engineering/SKILL.md",
     "Holds the dvar's pointer."),
    ("Dvar_SetAllowServerFlaggedWrites", 0x7FF728C75A80, "client/game/dump_anchors.hpp",
     "One instruction: mov g_dvarAllowServerFlaggedWrites, cl; ret."),
    # Named in the backend's Python sources with the address on the next line, which the pattern cannot pair.
    ("DwAuth_BuildRequest", 0x7FF729DEF740, "tools/dwserver/authserver.py",
     "Builds the POST /auth/ request. Its host template is \"%s-%s-auth3.%s.demonware.net\"."),
    ("Crypto_RsaPss_Verify", 0x7FF729A24210, "tools/dwserver/dwsign.py",
     "RSASSA-PSS verify: SHA-256, MGF1 with SHA-256, salt length 0."),
    ("Lsg_SendHello", 0x7FF729DE8940, "tools/dwserver/lsgserver.py",
     "Writes the 28-byte HELLO: u32 200, 200, 220, 220, the maximum payload, then an 8-byte client nonce."),
    ("Lsg_OnEncryptedMessage", 0x7FF729DE7780, "tools/dwserver/lsgcrypto.py",
     "Receives a 0x85 record: counter check, HMAC check, AES-128-CBC decrypt."),
    ("Lsg_ErrorCodeToString", 0x7FF729D55E90, "tools/dwserver/lsgserver.py",
     "A stub in retail: returns the text HIDDEN for every code."),
    ("bdByteBuffer_CheckTypeTag", 0x7FF729D388D0, "tools/dwserver/bdbuf.py",
     "Reads one whole byte and compares it with the expected type id. Type 22 splices the buffer and reads again."),
    ("bdByteBuffer_ReadBlob", 0x7FF729D384D0, "tools/dwserver/bdbuf.py",
     "Checks tag 0x13, then reads a typed UInt32 length, then that many bytes."),
    ("LuaNative_Localize_Impl", 0x7FF72534C140, "client/game/dump_anchors.hpp",
     "The body of Engine.Localize and Engine.LocalizeHash. Returns a string argument untouched only when its "
     "first byte is 0x15; any other string or hash is the name of a localize entry, and a missing entry is fatal."),
    # Bound by an AOB signature in the client, so the sources hold no address. Each address below is where
    # that signature matches in the dump file (scanned 2026-10-08).
    ("BB_Alert", 0x7FF71E6E61E0, "client/game/game.cpp",
     "Bound by signature. In our dump its first five bytes are the mod's own detour: the dump was taken with the hook in place."),
    ("CL_Disconnect", 0x7FF722892110, "client/game/game.cpp", "Bound by signature."),
    ("Dvar_SetIntFromSource", 0x7FF728C77530, "client/game/game.cpp",
     "Bound by signature: the first of three matches in the dump. Switches on the dvar's type."),
    ("LobbyBase_SetNetworkMode", 0x7FF727B19B60, "client/game/game.cpp",
     "Bound by signature. Stores the lobby's network mode, updates the menus' model, then tail-calls "
     "Com_SessionMode_SetNetworkMode with the mapped value."),
    ("g_dvarHashTable", 0x7FF735615570, "client/game/game.cpp",
     "Bound by signature. 1,024 buckets; the index is hash & 0x3FF."),
    ("g_svMaxClients", 0x7FF72DA73780, "client/game/game.cpp",
     "Bound by signature. The live server's player cap, a plain int."),
    ("LiveUser_GetUserDataForController", 0x7FF7274B2E70, "client/game/game.cpp", "Bound by signature."),
    ("p_dvar_nodw", 0x7FF733D20108, "client/game/game.cpp", "Bound by signature. Holds the nodw dvar's pointer."),
    ("p_dvar_showOverStack", 0x7FF72E407DF8, "client/game/game.cpp",
     "Bound by signature. The dvar pointer the client swaps to get its game-thread tick."),
    ("g_scrInitialized", 0x7FF7305B4826, "client/game/game.cpp",
     "Bound by signature (Scr_Initialized in the client). A byte: the script system is up."),
    ("DB_FindXAssetHeader", 0x7FF727EC21F0, "client/scripting/scripting.cpp",
     "Bound by signature. The asset lookup by type and name hash. For some types a missing asset is fatal inside it."),
    ("gVmOpJumpTable", 0x7FF72AA47740, "client/scripting/scripting.cpp",
     "Bound by signature. The GSC VM's handler table, one pointer per opcode."),
    ("gObjFileInfo", 0x7FF72C2AC9D0, "client/scripting/scripting.cpp",
     "Bound by signature. The linked script objects: 800 entries of 24 bytes for each of the two VMs."),
    ("gObjFileInfoCount", 0x7FF72C2B5FD0, "client/scripting/scripting.cpp",
     "Bound by signature. Two counts, one for each VM."),
    # The IDB's names for the two sibling setters (looked up in the IDB 2026-10-08).
    ("Com_SessionMode_SetGameMode", 0x7FF728D7C610, "client/game/game.cpp",
     "Writes the gameMode bits (0-3) of g_sessionModePacked. The signature the client binds under the name "
     "Com_SessionMode_SetNetworkMode matches this function, not the one at RVA 0xC1BC630."),
    ("Com_SessionMode_SetMatchType", 0x7FF728D7C5F0, "client/game/game.cpp",
     "Writes the matchType bits (12-15) of g_sessionModePacked. Sits right before the two other setters."),
    ("Dvar_SetInt_cand", 0x7FF728C77B90, "client/game/game.hpp",
     "The int setter with the type switch the client's comments describe: it tests its value as 32 bits. "
     "It is the second of the three functions the Dvar_SetIntFromSource signature matches."),
)
NOTE_OVERRIDES = {
    "g_localPlayerCount": "Old name. The value is the lobby's network mode: see g_lobbyNetworkMode.",
}

# (label, name prefixes). First match wins, so the specific ones come first.
GROUPS = (
    ("Errors and termination", ("Com_Error", "ErrorQueue_", "BB_Alert", "BnetError_", "LuiError_", "Com_NotifyLuiError")),
    ("Demonware, login and first party", (
        "Dw", "Bd", "bd", "Lsg_", "Login_", "LiveUser_", "LiveFirstParty_", "FirstParty_", "Bnet", "MtxSync_",
        "Lpc_", "Crypto_", "ObjectMetadata", "PublisherObjects", "AntiCheat_", "g_firstParty", "g_pubVars",
        "g_playlist", "Playlist", "g_dw", "g_lpc", "Entitlement", "Inventory_", "Loot_", "g_mtx", "g_liveUser",
        "g_bnet", "g_lsg", "g_bdAddr", "g_inventory", "Live_", "OnlineContent_", "g_onlineContent",
        "dvar_liveConnectMode", "dvar_mtxSync",
    )),
    ("Sessions and netcode", (
        "ClientSession_", "HostSession_", "Session_", "NetMsg_", "NetSession_", "LobbyHost_", "LobbyBase_",
        "LobbyClient_", "LobbyMsg", "LobbyUI_", "LobbyRoot_", "Lobby_", "JoinCtx_", "pendingJoin", "g_net",
        "g_lobby", "g_pendingJoin", "g_clientJoin", "cl_lobby", "g_hostLaunch", "HostLaunch", "GScr_Launch",
        "SV_", "sv_", "g_sv", "qportCounter", "CL_", "g_session", "g_join", "g_expectedHost",
        "g_controllerClientMap", "g_localClientControllers", "g_primaryLocalClient", "g_clientFlags",
        "g_localPlayerCount",
    )),
    ("LUI and Lua", (
        "LUI_", "Lui", "lua_", "luaL_", "luaG_", "luaD_", "luaV_", "luaH_", "luaS_", "luaF_", "lj_", "Lua", "g_lui",
        "g_lua", "Cmd_", "UI_", "g_ui", "aXhashfunc",
    )),
    ("GSC VM", ("Scr_", "GScr_", "CScr_", "VM_", "SL_", "ClientField_", "gVm", "gObjFile", "g_scr", "g_serverVm", "(stock handler of GSC")),
    ("PlayerData, stats and progression", (
        "PlayerData", "Ddl_", "LiveStorage_", "LiveStats_", "G_AddPlayerRankXp", "Progression_", "g_playerData",
        "StatsTransfer_", "g_statsTransfer", "Rank_", "Unlockables", "g_unlockable", "dvarPtr_ddl",
    )),
    ("Sound", ("SND_", "Triton")),
    ("AI and navigation", ("AI_", "Nav_", "hkai", "Tac_", "g_aiNav")),
    ("World, collision and rendering", (
        "CM_", "R_", "Light", "Image_", "XModel", "XCollision_", "DynEnt_", "Streamer_", "StreamKey", "World_",
        "g_clipMap", "g_comWorld", "g_terrainGfx", "g_streamKey", "g_renderer", "g_xmodelMesh", "g_cm",
        "Com_FindComWorld", "Com_CopyPrimaryLights", "LevelLoad_",
    )),
    ("Game entities and spawning", ("G_", "SP_", "VehNode_", "CG_", "ZBarrier_")),
    ("Fastfiles and asset loaders", (
        "DB_", "Load_", "Finish_", "FS_", "MapTable_", "MapPreload_", "BuildKv_", "g_xasset", "g_defaultAssetNames",
        "BG_Cache", "g_bgCache", "g_db", "g_zone", "g_streamPos", "g_mapPreload", "DecryptString",
    )),
    ("Dvars", ("Dvar_", "g_dvar", "p_dvar_", "dvar_", "(Dvar_")),
    ("Common, session mode and boot", ("Com_", "g_sessionMode", "Sys_", "Loc_", "g_mainThread", "(return gadget")),
)
OTHER = "Other"

TYPE_SHORT = (
    ("std::uint64_t", "u64"), ("std::uint32_t", "u32"), ("std::uint16_t", "u16"), ("std::uint8_t", "u8"),
    ("std::int64_t", "i64"), ("std::int32_t", "i32"), ("std::int16_t", "i16"), ("std::int8_t", "i8"),
    ("std::uintptr_t", "uintptr"), ("std::size_t", "size_t"),
)


def is_code(rva: int) -> bool:
    return any(lo <= rva < hi for lo, hi in CODE_RANGES)


def group_of(name: str) -> str:
    for label, prefixes in GROUPS:
        if name.startswith(prefixes):
            return label
    return OTHER


def first_sentences(text: str, limit: int = 230) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text.rfind(". ", 60, limit)
    if cut != -1:
        return text[: cut + 1]
    return text[:limit].rsplit(" ", 1)[0] + " ..."


def clean_note(text: str) -> str:
    # Pointers to working documents and memory notes mean nothing to a reader of the site.
    text = re.sub(r"\s*\(?[Ss]ee (?:docs/[\w./-]+|dump_anchors\.hpp|game\.hpp|memory [\w-]+)[^.)]*\)?\.?", "", text)
    text = text.replace("—", "-").replace("–", "-")
    text = text.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()


def read_text(path: Path) -> str:
    data = path.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace")


def parse_anchors(path: Path) -> list[dict]:
    entries: list[dict] = []
    block: list[str] = []      # comment lines above the current run of constants
    group: list[dict] = []     # the run itself
    group_block = ""

    def close_group() -> None:
        # A block that sits on a run of several constants describes them together: a constant takes the
        # sentence that names it, and nothing otherwise (the same sentence on ten rows says nothing).
        for item in group:
            if item["note"]:
                continue
            if not group_block:
                continue
            sentences = re.split(r"(?<=[.!?])\s+", group_block)
            named = [s for s in sentences if re.search(rf"\b{re.escape(item['name'])}\b", s)]
            if named:
                item["note"] = first_sentences(clean_note(named[0]))
            elif len(group) == 1:
                item["note"] = first_sentences(clean_note(group_block))
        group.clear()

    for number, raw in enumerate(read_text(path).splitlines(), 1):
        stripped = raw.strip()
        match = ANCHOR_RE.match(raw)
        if match:
            if not group:
                group_block = " ".join(block)
                block = []
            name, value, trailing = match.group(1), int(match.group(2), 16), (match.group(3) or "").strip()
            item = {
                "name": name, "va": value, "note": first_sentences(clean_note(trailing)) if trailing else "",
                "source": f"client/game/dump_anchors.hpp:{number}",
            }
            group.append(item)
            entries.append(item)
            continue
        if stripped.startswith("//"):
            if group:
                close_group()
                block = []
            text = stripped.lstrip("/").strip()
            if BANNER_RE.match(text):
                block = []     # a section banner starts a new block and is not part of any note
                continue
            block.append(text)
            continue
        if group:
            close_group()
        block = []
    close_group()
    return entries


def parse_signatures(path: Path) -> dict[str, str]:
    text = re.sub(r"//[^\n]*", "", read_text(path))
    out: dict[str, str] = {}
    for match in USING_RE.finditer(text):
        name = match.group(1)
        signature = re.sub(r"\s+", " ", match.group(2)).strip()
        for long, short in TYPE_SHORT:
            signature = signature.replace(long, short)
        if "(" in signature:
            ret, _, args = signature.partition("(")
            out[name] = f"{ret.strip()} {name}({args}"
    return out


def looks_like_symbol(token: str) -> bool:
    if len(token) < 4 or token.lower() in SKIP_WORDS:
        return False
    if token.startswith(("sub_", "loc_", "unk_", "off_", "qword_", "dword_", "byte_", "kDump", "__")):
        return False
    if token.lower() in ("imagebase", "sizeofimage"):
        return False
    if re.fullmatch(r"[A-Za-z]_cand", token) or re.fullmatch(r"x[0-9A-Fa-f]+", token):
        return False
    if token.isupper() and "_" not in token:
        return False
    if "_" in token or "::" in token:
        return True
    return sum(1 for c in token if c.isupper()) >= 2


def harvest_line(line: str) -> list[tuple[str, int]]:
    found = []
    for match in VA_RE.finditer(line):
        prefix = line[max(0, match.start() - 110): match.start()]
        # "Name(0x7FF7..." passes the address as an argument: it is not the address of Name.
        if re.search(r"[A-Za-z0-9_]\($", prefix):
            continue
        # An argument list right after a name does not separate the name from its address.
        prefix = re.sub(r"(?<=[A-Za-z0-9_])\([^()]*\)", "", prefix)
        tokens = list(IDENT_RE.finditer(prefix))
        name = None
        end = len(prefix)
        for token in reversed(tokens):
            between = prefix[token.end(): end]
            if re.search(r"[^\s`'\"()\[\]|@=:,*-]", between):
                break
            word = token.group(0)
            if looks_like_symbol(word):
                name = word
                break
            if word.lower() not in SKIP_WORDS:
                break
            end = token.start()
        if name:
            found.append((RENAMES.get(name, name), int(match.group(0), 16)))
    return found


def harvest(cw_mod: Path) -> dict[str, dict]:
    patterns = (
        "docs/**/*.md", ".claude/skills/**/*.md", "mapkit/**/*.hpp", "mapkit/**/*.cpp", "mapkit/*.md",
        "tools/dwserver/*.py", "tools/dwserver/*.md", "client/**/*.hpp", "client/**/*.cpp",
    )
    skip_parts = {"build", ".godot", "vendor", "__pycache__"}
    names: dict[str, dict] = {}
    for pattern in patterns:
        for path in sorted(cw_mod.glob(pattern)):
            rel = path.relative_to(cw_mod)
            if skip_parts & set(rel.parts):
                continue
            try:
                lines = read_text(path).splitlines()
            except OSError:
                continue
            # The anchor table's constants are parsed on their own; its comments name many more addresses.
            comments_only = rel.name == "dump_anchors.hpp"
            for number, line in enumerate(lines, 1):
                if "0x7FF7" not in line and "0x7ff7" not in line:
                    continue
                if comments_only and not line.lstrip().startswith("//"):
                    continue
                for name, va in harvest_line(line):
                    entry = names.setdefault(name, {"vas": defaultdict(list)})
                    entry["vas"][va].append(f"{rel.as_posix()}:{number}")
    return names


def same_family(a: str, b: str) -> bool:
    """Two names for one address count as aliases only when they plainly name the same thing."""
    def key(name: str) -> str:
        parts = [p for p in re.split(r"_+", name) if p]
        if parts and parts[0] in ("g", "p", "s"):
            parts = parts[1:]
        return (parts[0] if parts else "").lower()
    ka, kb = key(a), key(b)
    return bool(ka) and (ka == kb or ka.startswith(kb) or kb.startswith(ka))


def cw_mod_commit(cw_mod: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(cw_mod), "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True, timeout=20)
        return out.stdout.strip() or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def fmt(value: int) -> str:
    return f"0x{value:X}"


def table(rows: list[dict], with_signature: bool) -> list[str]:
    head = "Signature or note" if with_signature else "Note"
    out = [f"| Name | RVA | IDA address | {head} |", "|---|---|---|---|"]
    for row in rows:
        detail = row.get("note", "")
        if row.get("also"):
            detail = (detail + " " if detail else "") + "Also written as " + ", ".join(f"`{a}`" for a in row["also"]) + "."
        if with_signature and row.get("sig"):
            signature = row["sig"].replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
            detail = f'<code class="wrap">{signature}</code>' + (f"<br>{detail}" if detail else "")
        name = row["name"] if row["name"].startswith("(") else f"`{row['name']}`"
        out.append(f"| {name} | {fmt(row['rva'])} | {fmt(row['va'])} | {detail} |")
    return out


def page(title: str, intro: list[str], sections: list[tuple[str, list[dict]]], with_signature: bool, footer: str) -> str:
    lines = [f"# {title}", ""] + intro + [""]
    for label, rows in sections:
        if not rows:
            continue
        lines += [f"## {label}", ""] + table(rows, with_signature) + [""]
    lines += [footer, ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cw-mod", required=True, type=Path, help="path to a cw-mod checkout (read only)")
    args = parser.parse_args()
    cw_mod: Path = args.cw_mod.resolve()

    anchors_path = cw_mod / "client/game/dump_anchors.hpp"
    types_path = cw_mod / "client/game/function_types.hpp"
    if not anchors_path.is_file():
        print(f"error: {anchors_path} not found", file=sys.stderr)
        return 2

    anchors = parse_anchors(anchors_path)
    signatures = parse_signatures(types_path) if types_path.is_file() else {}
    noted = harvest(cw_mod)

    entries: list[dict] = []
    by_va: dict[int, dict] = {}
    by_name: dict[str, dict] = {}
    problems: list[str] = []

    def add(name: str, va: int, note: str, origin: str, source: str) -> None:
        rva = va - BASE
        entry = {
            "name": name, "va": va, "rva": rva, "kind": "code" if is_code(rva) else "data",
            "group": group_of(name), "sig": signatures.get(name, ""), "note": NOTE_OVERRIDES.get(name, note),
            "origin": origin, "source": source, "also": [],
        }
        entries.append(entry)
        by_name[name] = entry
        by_va.setdefault(va, entry)

    for anchor in anchors:
        name, va = anchor["name"], anchor["va"]
        if not (BASE <= va < BASE + IMAGE_SIZE):
            problems.append(f"anchor {name} = {fmt(va)} is outside the image")
            continue
        if name in by_name and by_name[name]["va"] != va:
            problems.append(f"anchor {name} has two addresses: {fmt(by_name[name]['va'])} and {fmt(va)}")
            continue
        add(name, va, anchor["note"], "anchor", anchor["source"])

    for name, va, source, note in EXTRA:
        if name not in by_name:
            add(name, va, note, "notes", source)

    rejected_aliases: list[str] = []
    for name, data in sorted(noted.items()):
        vas = data["vas"]
        if len(vas) > 1:
            listed = ", ".join(f"{fmt(v)} ({srcs[0]})" for v, srcs in sorted(vas.items()))
            problems.append(f"'{name}' is written with {len(vas)} addresses in the notes: {listed}")
        # The address named most often wins; ties go to the lowest.
        va, sources = max(sorted(vas.items(), reverse=True), key=lambda item: len(item[1]))
        if not (BASE <= va < BASE + IMAGE_SIZE):
            continue
        if name in by_name:
            if by_name[name]["va"] != va:
                problems.append(f"'{name}': the notes say {fmt(va)} ({sources[0]}), the index has {fmt(by_name[name]['va'])}")
            continue
        if va in by_va:
            owner = by_va[va]
            if same_family(name, owner["name"]):
                owner["also"].append(name)
            else:
                rejected_aliases.append(f"{name} == {owner['name']} ({sources[0]})")
            continue
        add(name, va, "", "notes", sources[0])

    entries.sort(key=lambda e: (e["group"], e["name"].lstrip("(").lower()))
    commit = cw_mod_commit(cw_mod)

    data_dir = ROOT / "tools" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "base": fmt(BASE),
        "cw_mod_commit": commit,
        "entries": [dict(e, va=fmt(e["va"]), rva=fmt(e["rva"])) for e in entries],
    }
    (data_dir / "addresses.json").write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8", newline="\n")

    labels = [label for label, _ in GROUPS] + [OTHER]
    footer = (f"<!-- generated by tools/gen_functions.py from cw-mod {commit} (client/game/dump_anchors.hpp, "
              "client/game/function_types.hpp, and the names written next to an address in the notes and comments). "
              "Do not edit by hand. -->")

    def rows(kind: str, label: str, origin: str) -> list[dict]:
        return [e for e in entries if e["kind"] == kind and e["group"] == label and e["origin"] == origin]

    math_page = "- How to read and check an address: [Address and byte math](/re/method/address-math.md)."
    for kind, filename, title, what in (
        ("code", "functions.md", "Function index", "functions and other code addresses"),
        ("data", "globals.md", "Globals index", "globals, tables and other data addresses"),
    ):
        count = sum(1 for e in entries if e["kind"] == kind)
        intro = [
            f"> Every named address this project uses or has written down: {count} {what}. The page is generated, "
            "so no address here was typed by hand.",
            "",
            "- **RVA** is the offset from the image base. It is the same in every dump of build 1.34.0.15931218.",
            f"- **IDA address** is the address in our IDB, whose image base is `{fmt(BASE)}`. Your own dump has "
            "another base: add the RVA to it.",
            "- A name that ends in `_cand` is inferred, not proven.",
            "- The first table of a group lists what the client anchors in `client/game/dump_anchors.hpp`. "
            "\"Named in the notes\" lists names written next to an address in the project's notes and code comments.",
        ]
        if (ROOT / "re/method/address-math.md").is_file():
            intro.append(math_page)
        sections: list[tuple[str, list[dict]]] = []
        for label in labels:
            sections.append((label, rows(kind, label, "anchor")))
            sections.append((f"{label}: named in the notes", rows(kind, label, "notes")))
        out_path = ROOT / "re" / "reference" / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page(title, intro, sections, with_signature=(kind == "code"), footer=footer),
                            encoding="utf-8", newline="\n")

    code = sum(1 for e in entries if e["kind"] == "code")
    print(f"{len(entries)} names: {code} code, {len(entries) - code} data "
          f"({sum(1 for e in entries if e['origin'] == 'anchor')} from dump_anchors.hpp, "
          f"{sum(1 for e in entries if e['origin'] == 'notes')} from notes), "
          f"{sum(len(e['also']) for e in entries)} second names, {sum(1 for e in entries if e['sig'])} with a signature, "
          f"{sum(1 for e in entries if e['group'] == OTHER)} ungrouped")
    if rejected_aliases:
        print(f"\n{len(rejected_aliases)} name(s) share an address with an unrelated name (left out):")
        for alias in rejected_aliases:
            print("  - " + alias)
    if problems:
        print(f"\n{len(problems)} thing(s) to look at:")
        for problem in problems:
            print("  - " + problem)
    return 0


if __name__ == "__main__":
    sys.exit(main())

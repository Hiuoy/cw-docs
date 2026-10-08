#!/usr/bin/env python3
"""Print ready table rows for names in the index, so a page never carries a hand-typed address.

Usage:
  python tools/fn.py Dvar_FindVar Dvar_GetBool        rows: | `name` | RVA | IDA address | signature |
  python tools/fn.py --find Lobby                     every name that contains the text
  python tools/fn.py --va 0x7FF728C72090              the name at an address
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

INDEX = Path(__file__).resolve().parent / "data" / "addresses.json"


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    entries = json.loads(INDEX.read_text(encoding="utf-8"))["entries"]
    by_name = {}
    for entry in entries:
        by_name[entry["name"]] = entry
        for other in entry.get("also", []):
            by_name.setdefault(other, entry)

    if args[0] == "--find":
        needle = args[1].lower()
        for entry in entries:
            if needle in entry["name"].lower() or any(needle in a.lower() for a in entry.get("also", [])):
                also = f"  (also {', '.join(entry['also'])})" if entry.get("also") else ""
                print(f"{entry['rva']:>11}  {entry['va']}  {entry['name']}{also}")
        return 0
    if args[0] == "--va":
        wanted = int(args[1], 16)
        for entry in entries:
            if int(entry["va"], 16) == wanted:
                print(f"{entry['name']}  RVA {entry['rva']}  ({entry['source']})")
        return 0

    missing = 0
    for name in args:
        entry = by_name.get(name)
        if entry is None:
            print(f"| `{name}` | NOT IN THE INDEX | | |")
            missing += 1
            continue
        signature = f"`{entry['sig']}`" if entry.get("sig") else ""
        print(f"| `{name}` | {entry['rva']} | {entry['va']} | {signature} |")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

# About these docs

> How the site is put together, where its facts come from, and how to keep it correct.

## Where the facts come from

Every page is written from the cw-mod repository, in this order of trust:

1. The code as it is today, and the comments at the top of each file.
2. `docs/ROADMAP.md` for what is done and what is not.
3. The working notes in `docs/` and the tool READMEs.
4. The project's reverse-engineering playbook.

When two sources disagree, the newer one is used and checked against the code. A point that could not be settled is marked "unverified" on the page.

Each page ends with a hidden comment that names its sources and the cw-mod commit it was written from. View the page's markdown to read it.

## The rules a page follows

- One topic per page. A reverse-engineering page has about 600 words of prose at most, a guide page about 400. Tables and code do not count.
- A fact lives on one page. A guide says how to use a thing and what its limits are; the matching page under [How we did it](/re/) says how it works inside. They link to each other.
- Status uses the roadmap's words: **Done** (seen working in the game), **Part done**, **Built** (written, not yet seen working in the game), **Open**, **Parked**.
- A name that ends in `_cand` was inferred from the code around it and is not proven.
- Addresses are never typed by hand. They come from the generated [function index](/re/reference/functions.md).

## How it is built

The site is [docsify](https://docsify.js.org) 5: plain markdown files, turned into pages in the browser. Nothing is compiled.

| File | Role |
|---|---|
| `index.html`, `assets/site.js`, `assets/custom.css` | The shell, the configuration and the styling |
| `_navbar.md`, `_sidebar.md`, `re/_sidebar.md`, `guide/_sidebar.md` | The menus. Each path has its own sidebar |
| `tools/gen_functions.py` | Builds the function and globals index from cw-mod's address table |
| `tools/check_docs.py` | Checks links, anchors, addresses, coverage of settings and tool flags, and that nothing private or copyrighted slipped in |
| `tools/fn.py` | Prints table rows for a function name, with its addresses |

## Working on the docs

Preview the site on your PC, from the repository folder:

```powershell
python -m http.server 3000
```

Then open `http://localhost:3000`. `npx docsify-cli serve .` does the same with live reload.

Before you commit:

```powershell
python tools/gen_functions.py --cw-mod <path to cw-mod>
python tools/check_docs.py --cw-mod <path to cw-mod> --write-index
```

The first rebuilds the index when cw-mod's addresses changed. The second must end with `0 error(s)`; `--write-index` refreshes the page list the search box uses.

Links are written from the site root with a leading slash, such as `/guide/install.md`. That form works on the site and on GitHub.

## When cw-mod changes

Find the pages whose sources comment names the file that changed, update them, and bring their status line in line with the roadmap. The roadmap stays the one place for status; a page here only repeats it with a date.

<!-- sources: this repository's own layout and tools, 2026-10-07 -->

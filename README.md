# reflex-anthropic-skill

**Reflex** is a [Claude skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) (installable agent skill) that acts as a **convention-based meta-skill dispatcher**. The model does not load every submodule up front: it reads a small `SKILL.md` frontmatter, runs a local Python router, then loads only the matching module’s instructions.

In this repo, the skill is rooted at **`reflex/`** (that folder contains `SKILL.md`, `scripts/`, and `modules/`).

## What it does

- **Trigger:** The skill is written to activate when the user’s message contains the word **`callsign`** (see the `description` in `reflex/SKILL.md` frontmatter). Examples: `callsign code-review`, `callsign plan`, `callsign help`.
- **Routing:** `reflex/scripts/dispatch.py` scans `reflex/modules/`, parses the user message against each module’s optional `PARAMS.json`, resolves dependency chains (`DEPENDS.json`) or variant pickers (`RESOLVE.py`), and prints a **single protocol line** telling the assistant what to load next.
- **Modules:** Each capability lives under `reflex/modules/<name>/` with at least `MODULE.md`. Optional files add parameters, dependencies, or runtime variant selection.

Full protocol, module levels, and agent rules are documented in **`reflex/SKILL.md`** (read that file when authoring or extending the skill).

## Repository layout

```text
reflex/
├── SKILL.md              # Skill definition + instructions for the model
├── scripts/
│   ├── dispatch.py       # Router: message → LOAD_MODULE / CHAIN / RESOLVED / …
│   └── sources.py      # Injected context (e.g. module registry)
└── modules/
    └── <module-name>/
        ├── MODULE.md     # Instructions loaded only when this module wins
        ├── PARAMS.json   # Optional: declared inputs
        ├── DEPENDS.json  # Optional: chained sub-modules
        ├── RESOLVE.py    # Optional: pick a variants/<name>/MODULE.md
        └── variants/     # Optional: Level-3 variants
```

## Installing the skill in Claude

1. Use the directory **`reflex/`** as the skill package (it must contain `SKILL.md` at the top level of that folder).
2. Add or upload that folder through your Claude **Skills** / **Agent skills** workflow in the product you use (desktop app, API, or team settings—depending on what your account supports).
3. After installation, invoke it in chat with **`callsign`** plus a module name and any arguments described in that module’s `PARAMS.json`.

If your tooling expects a zip, zip the **contents** of `reflex/` or the `reflex` folder itself according to that tool’s docs, preserving `SKILL.md` at the skill root.

## Local testing of the router

From the repo root (adjust paths if you run from elsewhere):

```bash
python3 reflex/scripts/dispatch.py - <<'DISPATCH_INPUT'
callsign help
DISPATCH_INPUT
```

Pass the **exact** user message you want to simulate; the script’s parsing is sensitive to wording and token order. stdout will be one line such as `LOAD_MODULE:…`, `CHAIN:…`, `MISSING_PARAMS:…`, etc.

## Adding a new module

- **Minimal:** `reflex/modules/<name>/MODULE.md`
- **With inputs:** add `PARAMS.json` (see conventions in `reflex/SKILL.md`)
- **With pipeline steps:** add `DEPENDS.json`
- **With runtime branch / A–B variants:** add `RESOLVE.py` and `variants/<variant>/MODULE.md`

Optional context for `PARAMS.json` can be wired in `reflex/scripts/sources.py` via the `SOURCES` registry (again documented in `reflex/SKILL.md`).

## License / contributions

Add a `LICENSE` if you publish this repo; skill content is otherwise plain Markdown and Python in-tree.

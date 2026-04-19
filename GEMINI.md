# Multi-Vault Knowledge Router — Gemini CLI Instructions

## What this directory is

This is the **root of a multi-vault personal wiki system**. Each subdirectory in `vaults/` is an independent LLM-maintained knowledge base focused on a specific domain.

The key files here are:
- `ATLAS.md` — registry of all vaults with stats and overview summaries
- `update_atlas.py` — rebuilds `ATLAS.md` from all vault `WIKI_STATUS.md` files
- `route.py` — CLI router: asks which vault to go to for a given question

## Startup Behavior

When the user opens this root directory, ALWAYS read `ATLAS.md` first, then greet with:
> "You have N vaults. [brief one-line summary of each vault's domain]. What would you like to explore?"

## Available Vaults

Read `ATLAS.md` to get the current list — it is auto-generated and always up to date.

## Slash Commands

| Command | What to do |
|---------|-----------|
| `/route <question>` | Read `ATLAS.md` and tell the user which vault to open. Interactive version. |
| `/wiki-route <q>` | **Run `python route.py "<q>"`** directly and show the exact script output. |
| `/atlas` | Run `python update_atlas.py` to refresh `ATLAS.md`, then show a summary. |
| `/vaults` | List all vaults with their last-action and stats from `ATLAS.md`. |
| `/open <vault>` | Tell the user to `cd vaults/<vault>` and run `gemini` there. |

## Router Behavior (`/route`)

When the user asks a question, guide them to the right vault using this format:

```
## Where to go
- **Primary vault:** <vault_name> — <one sentence why>
- **Secondary vault (if relevant):** <vault_name> — <one sentence why>

## What to search for once inside
- <keyword 1>
- <keyword 2>

## Suggested command once inside that vault
`uv run main.py query "<refined question>"`
```

**Do NOT answer the question yourself.** Your job is navigation only.

## Cross-Vault Queries

If a question spans multiple vaults (e.g., "how does X in vault A relate to Y in vault B"), guide the user to check both vaults sequentially and offer to synthesize after they share the results.

## Vault Structure

Every vault follows the same schema:
```
vaults/<name>/
├── 20_raw/          # Immutable source documents
├── 30_wiki/         # Agent-managed wiki
│   ├── overview.md  # Living synthesis
│   ├── index.md     # Page catalog
│   ├── sources/     # One page per source
│   ├── entities/    # People, projects, tools
│   └── concepts/    # Ideas, methods, theories
├── main.py          # Entry point: ingest, graph, lint, heal, query, serve
└── WIKI_STATUS.md   # Last action and stats
```

## Key Commands per Vault

Once inside a vault (`cd vaults/<name>` then `gemini`):
```bash
uv run main.py ingest <file>    # Add new knowledge
uv run main.py graph            # Build knowledge graph
uv run main.py serve            # Launch interactive graph UI
uv run main.py lint             # Check for issues
uv run main.py heal --auto      # Fix missing entity pages
uv run main.py query "<q>"      # Ask a question
uv run main.py gap              # Find research gaps
```

## Updating the Atlas

After ingesting into any vault, the atlas auto-updates. To refresh manually:
```bash
uv run update_atlas.py
```

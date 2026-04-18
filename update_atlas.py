from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
ATLAS_FILE = ROOT / "ATLAS.md"

# List your vaults here
VAULTS = [
    ROOT / "biosignal-wiki",
    ROOT / "ml-wiki",
    # add more as you create them
]

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def parse_status(status_content: str) -> dict:
    """Extract stats from WIKI_STATUS.md"""
    result = {}
    for line in status_content.splitlines():
        if "Last action:" in line:
            result["last_action"] = line.split("Last action:")[-1].strip()
        if "Last updated:" in line:
            result["last_updated"] = line.split("Last updated:")[-1].strip()
        if "Papers:" in line:
            result["papers"] = line.split("Papers:")[-1].strip()
        if "Concepts:" in line:
            result["concepts"] = line.split("Concepts:")[-1].strip()
        if "Entities:" in line:
            result["entities"] = line.split("Entities:")[-1].strip()
    return result

def build_atlas():
    today = date.today().isoformat()
    lines = [
        f"# ATLAS — Knowledge Vault Registry",
        f"Last updated: {today}",
        f"Total vaults: {len(VAULTS)}",
        "",
        "---",
        "",
    ]

    for vault in VAULTS:
        if not vault.exists():
            print(f"  [skip] vault not found: {vault}")
            continue

        vault_name = vault.name
        status = parse_status(read_file(vault / "WIKI_STATUS.md"))
        overview = read_file(vault / "30_wiki" / "overview.md").strip()

        # Truncate overview if too long
        if len(overview) > 500:
            overview = overview[:500] + "..."

        lines += [
            f"## {vault_name}",
            f"- **Last updated:** {status.get('last_updated', 'unknown')}",
            f"- **Last action:** {status.get('last_action', 'unknown')}",
            f"- **Papers:** {status.get('papers', '0')} | "
            f"**Concepts:** {status.get('concepts', '0')} | "
            f"**Entities:** {status.get('entities', '0')}",
            f"- **Path:** `{vault}/`",
            "",
            "### What this vault covers",
            overview if overview else "_No overview yet — run ingest first._",
            "",
            "---",
            "",
        ]

    ATLAS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"ATLAS.md updated — {len(VAULTS)} vaults registered")

if __name__ == "__main__":
    build_atlas()
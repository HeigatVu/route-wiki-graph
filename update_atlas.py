from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.resolve()
ATLAS_FILE = ROOT / "ATLAS.md"

# Auto-discover all vaults in the vaults/ directory
VAULTS_DIR = ROOT / "vaults"
VAULTS = sorted(
    [p.resolve() for p in VAULTS_DIR.iterdir() if p.is_dir() and (p / "WIKI_STATUS.md").exists()],
    key=lambda x: x.name.lower()
)

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
        if "Knowledge notes:" in line:
            result["notes"] = line.split("Knowledge notes:")[-1].strip()
        if "Books:" in line:
            result["books"] = line.split("Books:")[-1].strip()
        if "Concepts:" in line:
            result["concepts"] = line.split("Concepts:")[-1].strip()
        if "Entities:" in line:
            result["entities"] = line.split("Entities:")[-1].strip()
    return result

def trim_overview(text: str, max_chars: int = 2500) -> str:
    """Trim at a clean paragraph boundary, not mid-sentence."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    # Find last double-newline (paragraph break) before the limit
    last_para = truncated.rfind("\n\n")
    if last_para > max_chars // 2:  # Only cut at paragraph if it's reasonably far in
        return truncated[:last_para].strip() + "\n\n_[...overview continues — open `30_wiki/overview.md` for full content]_"
    return truncated.strip() + "..."

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
        overview_display = trim_overview(overview)

        stats = (
            f"**Papers:** {status.get('papers', '0')} | "
            f"**Notes:** {status.get('notes', '0')} | "
            f"**Books:** {status.get('books', '0')} | "
            f"**Concepts:** {status.get('concepts', '0')} | "
            f"**Entities:** {status.get('entities', '0')}"
        )

        vault_rel = vault.relative_to(ROOT)
        lines += [
            f"## {vault_name}",
            f"- **Last updated:** {status.get('last_updated', 'unknown')}",
            f"- **Last action:** {status.get('last_action', 'unknown')}",
            f"- {stats}",
            f"- **Path:** `{vault_rel}/`",
            "",
            "### What this vault covers",
            overview_display if overview_display else "_No overview yet — run ingest first._",
            "",
            "---",
            "",
        ]

    ATLAS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"ATLAS.md updated — {len(VAULTS)} vaults registered")

if __name__ == "__main__":
    build_atlas()
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Dict

FOLDERS = [
    "00_Channels",
    "00_Discovery",
    "01_Library",
    "02_Creators",
    "03_Venues",
    "04_Topics",
    "05_Journeys",
    "06_Aesthetics",
    "98_templets",
    "99_Inbox",
]

TEMPLATES: Dict[str, str] = {
    "TPL_Creator.md": """---\ntype: \nstatus: \nmonitor: false\n---\n\n# Creator Notes\n- Focus:\n- Highlights:\n""",
    "TPL_Venue.md": """---\ngeo: [0.0, 0.0]\nradius: 0\nseason: \n---\n\n# Venue Details\n- Access:\n- Notes:\n""",
    "TPL_Trip.md": """---\nstatus: [Planned, Past]\ndates: \n---\n\n# Trip Plan\n- Locations:\n- Checklist:\n""",
    "TPL_Channel.md": """---\ncost: \nvpn_required: false\nownership: \n---\n\n# Channel Details\n- Notes:\n""",
}


def get_project_root() -> Path:
    return Path(__file__).resolve().parent


def get_vault_root(project_root: Path) -> Path:
    env_path = os.getenv("CULTUREDB_ROOT")
    if env_path:
        return Path(env_path).expanduser()
    return project_root / "CultureDB"


def ensure_directories(vault_root: Path) -> None:
    for name in FOLDERS:
        (vault_root / name).mkdir(parents=True, exist_ok=True)


def write_env_file(project_root: Path, vault_root: Path, overwrite: bool = False) -> Path:
    env_path = project_root / ".env"
    if env_path.exists() and not overwrite:
        return env_path
    lines = [
        f"CULTUREDB_ROOT={vault_root}",
        "# Add your secrets below",
        "API_KEY_EXAMPLE=REPLACE_ME",
        "# Never commit this file to git",
    ]
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return env_path


def write_templates(vault_root: Path, overwrite: bool = False) -> int:
    template_dir = vault_root / "98_templets"
    template_dir.mkdir(parents=True, exist_ok=True)
    created = 0
    for name, content in TEMPLATES.items():
        target = template_dir / name
        if target.exists() and not overwrite:
            continue
        target.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
        created += 1
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize CultureDB Obsidian vault directories, templates, and .env.")
    parser.add_argument("--overwrite-env", action="store_true", help="Overwrite existing .env with fresh placeholders.")
    parser.add_argument(
        "--overwrite-templates",
        action="store_true",
        help="Overwrite template files under 98_templets even if they already exist.",
    )
    args = parser.parse_args()

    project_root = get_project_root()
    vault_root = get_vault_root(project_root)

    vault_root.mkdir(parents=True, exist_ok=True)
    ensure_directories(vault_root)
    env_path = write_env_file(project_root, vault_root, overwrite=args.overwrite_env)
    templates_created = write_templates(vault_root, overwrite=args.overwrite_templates)

    print(f"[init] Project root: {project_root}")
    print(f"[init] Vault root: {vault_root}")
    print(f"[init] .env: {env_path}")
    print(f"[init] Templates created: {templates_created}")


if __name__ == "__main__":
    main()
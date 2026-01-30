from __future__ import annotations

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
    "98_templets",
    "99_Inbox",
]

DATA_FILES: Dict[str, str] = {
    "00_Channels/Service - BBC iPlayer.md": """---\nvpn_required: true\nvpn_location: UK\ncost: Free (License)\n---\n""",
    "00_Channels/Service - Spotify.md": """---\ncost: Subscription\ncontent: [Music, Audiobooks]\n---\n""",
    "02_Creators/Aardman Animations.md": """---\ntype: Studio\nmonitor: true\ntags: [Stop Motion]\n---\n\nLinked topics: [[Topic - Stop Motion]]\n""",
    "02_Creators/Stephen Fry.md": """---\ntype: Person\nmonitor: true\nrole: [Narrator, Presenter]\n---\n""",
    "03_Venues/Skulptur i Pilane.md": """---\ngeo: [58.029, 11.556]\nseason: Summer\nstatus: Must Visit\n---\n""",
    "03_Venues/Bryggvingen.md": """---\ngeo: [58.0831, 11.5034]\nlocation: [[Location - Lyr]]\n---\n\nThe restaurant at Lyr.\n""",
    "03_Venues/Nordiska Akvarellmuseet.md": """---\ngeo: [57.994, 11.536]\nstatus: Always Visit\n---\n""",
    "04_Topics/Topic - Stop Motion.md": "We prefer tactile/imperfection over CGI.\n",
    "04_Topics/Topic - Vivid Light.md": "The aesthetic reason we like Impressionism and Watercolor.\n",
    "04_Topics/Location - Lyr.md": """---\ngeo: [58.077, 11.520]\nsubtype: Island\n---\n""",
    "05_Journeys/Trip - Gothenburg Sailing 2026.md": """---\nstatus: Planned\ndates: 2026-07\nlocations: [[Location - Gothenburg Archipelago]]\n---\n""",
    "00_Discovery/List - Guardian Time Loop Films.md": """---\nsource: [[Source - The Guardian]]\n---\n\nRecommendations including [[Installation - The Clock]] and [[Movie - Groundhog Day]].\n""",
}


def get_vault_root() -> Path:
    project_root = Path(__file__).resolve().parent
    env_path = os.getenv("CULTUREDB_ROOT")
    if env_path:
        return Path(env_path).expanduser()
    return project_root / "CultureDB"


def ensure_directories(root: Path) -> None:
    for folder in FOLDERS:
        target = root / folder
        os.makedirs(target, exist_ok=True)


def write_file(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    path.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    return not existed

def create_data_files(root: Path) -> int:
    count = 0
    for relative_path, content in DATA_FILES.items():
        count += write_file(root / relative_path, content)
    return count


def main() -> None:
    vault_root = get_vault_root()
    ensure_directories(vault_root)

    created_files = create_data_files(vault_root)

    print(f"[setup_vault] Vault root: {vault_root}")
    print(f"[setup_vault] Created {created_files} files.")


if __name__ == "__main__":
    main()

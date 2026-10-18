# =============================================================================
# URTC-DOCS - src/urtc_docs/family.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Find the repositories of the URTC ecosystem next to this one and read their manifests."""
from __future__ import annotations

import json
from pathlib import Path

MANIFEST_FILE = "urtc.project.json"
OWN_NAME = "URTC-DOCS"
REQUIRED_KEYS = ("name", "version", "role", "stack", "maturity", "family", "parent", "deployment_target")


def is_family_name(name: str) -> bool:
    """The firmware repository is called exactly URTC (no trailing dash)."""
    return name == "URTC" or name.startswith("URTC-")


def workspace_of(repo: Path) -> Path:
    """The folder that holds this repository and its siblings."""
    return repo.resolve().parent


def discover(workspace: Path) -> list[Path]:
    """The sibling directories of the ecosystem that carry a manifest, sorted by name."""
    found = [
        entry
        for entry in sorted(workspace.iterdir(), key=lambda p: p.name)
        if entry.is_dir() and is_family_name(entry.name) and (entry / MANIFEST_FILE).is_file()
    ]
    return found


def read_manifest(repo: Path) -> dict:
    """The manifest of one repository, checked for the keys the catalogue needs."""
    data = json.loads((repo / MANIFEST_FILE).read_text(encoding="utf-8"))
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ValueError(f"{repo.name}: manifest lacks {', '.join(missing)}")
    if data["name"] != repo.name:
        raise ValueError(f"{repo.name}: manifest name is {data['name']!r}")
    return data


def load_manifests(workspace: Path) -> list[dict]:
    return [read_manifest(repo) for repo in discover(workspace)]

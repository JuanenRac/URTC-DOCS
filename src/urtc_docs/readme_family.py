# =============================================================================
# URTC-DOCS - src/urtc_docs/readme_family.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The repositories of the ecosystem by group, as the Related Projects section of the READMEs lists them.

The list is written here, not read from the manifests, so that the READMEs can be
produced and checked in a CI run that has no sibling repository. The structure
check of the catalogue compares this list with the manifests found next to this
repository, so a repository that appears or disappears is reported.
"""
from __future__ import annotations

FAMILY_REPOS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "URTC Tool Platform",
        (
            "URTC",
            "URTC-FLASHER",
            "URTC-SMART-RACK",
            "URTC-TESTER",
            "URTC-VISION-TOOL",
            "URTC-WEB-STUDIO",
        ),
    ),
    (
        "Ecosystem Operations",
        (
            "URTC-DOCS",
            "URTC-UPDATER",
        ),
    ),
)


def all_names() -> set[str]:
    return {name for _, names in FAMILY_REPOS for name in names}

# =============================================================================
# URTC-DOCS - src/urtc_docs/drift.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Drift of the files that every repository of the ecosystem carries as the same copy.

A few small files are meant to be identical in every repository (the documentation-policy and README-parity
checks, the manifest version bumper). Only the name of the repository inside the file may differ. When one copy is
edited, or one repository is left behind, the checks stop meaning the same thing in each place. This reads the
copies next to each other, takes the text most repositories share as the reference, and reports the repositories
that differ, with the first differing line.
"""
from __future__ import annotations

import difflib
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from . import family

# Relative to the root of each repository. The community templates under .github/ are written by the central
# synchronisation of the profile repository and are not compared here.
SHARED_FILES: tuple[str, ...] = (
    "tools/_doc_policy.py",
    "tools/_readme_parity.py",
    "bump_manifest_version.py",
)

_PLACEHOLDER = "<REPO>"


@dataclass(frozen=True)
class Drift:
    file: str
    repository: str
    detail: str


_FAMILY_NAME = re.compile(r"(?<![A-Za-z0-9_-])URTC(?:-[A-Z0-9]+)*(?![A-Za-z0-9_])")


def normalize(text: str) -> str:
    """The text with Windows line endings turned into newlines and every name of a repository of the family (a
    header says which repository the file sits in) made generic: the name is the one thing allowed to differ."""
    return _FAMILY_NAME.sub(_PLACEHOLDER, text.replace("\r\n", "\n"))


def _first_difference(reference: str, other: str) -> str:
    for line in difflib.unified_diff(reference.splitlines(), other.splitlines(), "reference", "this", n=0, lineterm=""):
        if line.startswith(("---", "+++", "@@")):
            continue
        return line[:160]
    return "different"


def compare(copies: dict[str, str]) -> list[Drift]:
    """``copies`` maps a repository name to the text of one shared file. Returns the repositories that differ from
    the text most of them share (a tie is settled in favour of the text that sorts first by repository name)."""
    normalized = {name: normalize(text) for name, text in copies.items()}
    if len(normalized) < 2:
        return []
    counts = Counter(normalized.values())
    best = max(counts.values())
    first_of = {}
    for name in sorted(normalized):
        first_of.setdefault(normalized[name], name)
    reference = min((text for text, count in counts.items() if count == best), key=lambda text: first_of[text])
    reference_name = first_of[reference]
    return [Drift("", name, f"differs from {reference_name}: {_first_difference(reference, text)}")
            for name, text in sorted(normalized.items()) if text != reference]


def check_workspace(workspace: Path, files: tuple[str, ...] = SHARED_FILES) -> tuple[list[Drift], int]:
    """Returns the drift found and how many repositories were compared."""
    repos = family.discover(workspace)
    found: list[Drift] = []
    for relative in files:
        copies = {}
        for repo in repos:
            path = repo / relative
            if path.is_file():
                copies[repo.name] = path.read_text(encoding="utf-8", errors="replace")
        found += [Drift(relative, d.repository, d.detail) for d in compare(copies)]
    return found, len(repos)

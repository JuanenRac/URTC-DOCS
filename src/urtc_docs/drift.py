# =============================================================================
# URTC-DOCS - src/urtc_docs/drift.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Drift of the files that every repository of the ecosystem carries as the same copy.

A few small files are meant to be identical in every repository (the documentation-policy and README-parity
checks, the manifest version bumper, the dashboard notifier). Only the name of the repository inside the file may differ. When one copy is
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
    ".github/workflows/dashboard-dispatch.yml",
    "tools/_tracked_names.py",
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


def compare(copies: dict[str, str], reference_text: str | None = None) -> list[Drift]:
    """``copies`` maps a repository name to the text of one shared file. Returns the repositories that differ from
    the text most of them share (a tie is settled in favour of the text that sorts first by repository name)."""
    normalized = {name: normalize(text) for name, text in copies.items()}
    if reference_text is not None:
        return [Drift("", name, f"differs from the template: {_first_difference(reference_text, text)}") for name, text in sorted(normalized.items()) if text != reference_text]
    if len(normalized) < 2:
        return []
    counts = Counter(normalized.values())
    best = max(counts.values())
    first_of: dict[str, str] = {}
    for name in sorted(normalized):
        first_of.setdefault(normalized[name], name)
    reference = min((text for text, count in counts.items() if count == best), key=lambda text: first_of[text])
    reference_name = first_of[reference]
    return [Drift("", name, f"differs from {reference_name}: {_first_difference(reference, text)}")
            for name, text in sorted(normalized.items()) if text != reference]


def check_workspace(workspace: Path, files: tuple[str, ...] = SHARED_FILES, template_dir: Path | None = None) -> tuple[list[Drift], int]:
    """Returns the drift found and how many repositories were compared. With a template the copies are compared with it, without one with each other."""
    repos = family.discover(workspace)
    found: list[Drift] = []
    for relative in files:
        copies = {}
        for repo in repos:
            path = repo / relative
            if path.is_file():
                copies[repo.name] = path.read_text(encoding="utf-8", errors="replace")
        found += [Drift(relative, d.repository, d.detail) for d in compare(copies, template_text(relative, template_dir) if template_dir else None)]
    return found, len(repos)


# ---------------------------------------------------------------------------------------------------------------
# The template: one canonical copy of each shared file, written once here and put into every repository.
# ---------------------------------------------------------------------------------------------------------------
TEMPLATE_NAME = "eh3d-repo-template"
TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "template" / TEMPLATE_NAME


def template_text(relative: str, template_dir: Path | None = None) -> str | None:
    """The canonical text of a shared file (the name of the repository written as <REPO>), or None when the template has none."""
    path = (template_dir or TEMPLATE_DIR) / relative
    return path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.is_file() else None


def render_for(repository: str, canonical: str, newline: str = "\n") -> str:
    """The canonical text for one repository: its own name where the template says <REPO>."""
    return canonical.replace(_PLACEHOLDER, repository).replace("\n", newline)


def make_canonical(text: str) -> str:
    """The canonical form of a copy: line endings as newlines and the name of the repository as <REPO>."""
    return normalize(text)


@dataclass(frozen=True)
class SyncItem:
    repository: str
    file: str
    path: Path
    new_text: str
    newline: str


def plan_sync(workspace: Path, files: tuple[str, ...] = SHARED_FILES, template_dir: Path | None = None) -> list[SyncItem]:
    """Every copy that differs from the template, with the text it should have (the line endings of the copy are kept)."""
    items: list[SyncItem] = []
    for relative in files:
        canonical = template_text(relative, template_dir)
        if canonical is None:
            continue
        for repo in family.discover(workspace):
            path = repo / relative
            if not path.is_file():
                continue
            raw = path.read_bytes().decode("utf-8", errors="replace")
            newline = "\r\n" if "\r\n" in raw else "\n"
            if normalize(raw) != canonical:
                items.append(SyncItem(repo.name, relative, path, render_for(repo.name, canonical, newline), newline))
    return items


def apply_sync(items: list[SyncItem]) -> None:
    for item in items:
        item.path.write_bytes(item.new_text.encode("utf-8"))

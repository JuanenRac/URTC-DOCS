# =============================================================================
# URTC-DOCS - src/urtc_docs/catalog.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Write the table of docs/PROJECT_CATALOG.md from the manifests of the repositories.

No version, maturity or role in the table is typed by hand, so none can be
behind its project. The table sits between two markers; the text around it is
written by hand and is never touched.
"""
from __future__ import annotations

import re
from pathlib import Path

from .descriptions import DESCRIPTIONS

BEGIN, END = "<!-- catalog:begin -->", "<!-- catalog:end -->"
MATURITY_ORDER = ("scaffolding", "functional", "established", "production")
MATURITY_LABEL = {"scaffolding": "Scaffolding", "functional": "Functional", "established": "Established", "production": "Production"}
URL = "https://github.com/JuanenRac/{name}"


def describe(manifest: dict) -> str:
    """The one-line description: the curated sentence, else the start of the manifest's notes."""
    curated = DESCRIPTIONS.get(manifest["name"])
    if curated:
        return curated
    first = re.split(r"(?<=[.!?])\s", str(manifest.get("notes", "")).strip())[0]
    return (first[:117] + "...") if len(first) > 120 else first


def cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def group_by_family(manifests: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for manifest in manifests:
        groups.setdefault(manifest["family"], []).append(manifest)
    ordered: dict[str, list[dict]] = {}
    for family in sorted(groups, key=str.casefold):
        members = groups[family]
        # the integration parent of the family first, then by name
        ordered[family] = sorted(members, key=lambda m: (m["parent"] is not None, m["name"].casefold()))
    return ordered


def maturity_counts(manifests: list[dict]) -> dict[str, int]:
    counts = {level: 0 for level in MATURITY_ORDER}
    for manifest in manifests:
        counts[manifest["maturity"]] = counts.get(manifest["maturity"], 0) + 1
    return counts


def table(manifests: list[dict]) -> str:
    """The generated block, without its markers."""
    counts = maturity_counts(manifests)
    summary = ", ".join(f"{counts[level]} {MATURITY_LABEL[level].lower()}" for level in MATURITY_ORDER if counts.get(level))
    lines = [f"**{len(manifests)} repositories** in {len(group_by_family(manifests))} families: {summary}.", ""]
    for family, members in group_by_family(manifests).items():
        lines += [f"### {family}", "", "| Repository | Version | Maturity | Role | Stack | Target | Parent | What it is |", "|---|---|---|---|---|---|---|---|"]
        for m in members:
            parent = m["parent"] or "-"
            lines.append(
                f"| [{m['name']}]({URL.format(name=m['name'])}) | {cell(m['version'])} | {MATURITY_LABEL.get(m['maturity'], cell(m['maturity']))} "
                f"| {cell(m['role'])} | {cell(m['stack'])} | {cell(m['deployment_target'])} | {cell(parent)} | {cell(describe(m))} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n")


def structure(manifests: list[dict]) -> list[tuple[str, str, str, str, str, str]]:
    """What changes rarely: which repositories exist and what kind each is. Versions and maturity are left out."""
    return sorted((m["name"], m["family"], m["role"], m["stack"], m["deployment_target"], str(m["parent"])) for m in manifests)


def render(current: str, manifests: list[dict]) -> str:
    """The document with the block between the markers replaced by the table."""
    if BEGIN not in current or END not in current:
        raise ValueError(f"the catalogue needs the markers {BEGIN} and {END}")
    head, rest = current.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n{table(manifests)}\n{END}{tail}"


def read_block(current: str) -> str | None:
    if BEGIN not in current or END not in current:
        return None
    return current.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")


def structure_from_block(block: str) -> list[tuple[str, str, str, str, str, str]] | None:
    """The same tuples, read back from a written table, so the structure can be compared without versions."""
    rows: list[tuple[str, str, str, str, str, str]] = []
    family = ""
    for line in block.splitlines():
        if line.startswith("### "):
            family = line[4:].strip()
        elif line.startswith("| [URTC"):
            cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) < 8:
                return None
            name = re.match(r"\[([^\]]+)\]", cells[0])
            if not name:
                return None
            parent = cells[6]
            rows.append((name.group(1), family, cells[3], cells[4], cells[5], "None" if parent == "-" else parent))
    return sorted(rows)


def missing_descriptions(manifests: list[dict]) -> list[str]:
    return sorted(m["name"] for m in manifests if m["name"] not in DESCRIPTIONS)


def check_file(path: Path, manifests: list[dict], structure_only: bool = False) -> tuple[bool, str]:
    """(ok, message) for a catalogue file against the manifests."""
    current = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    block = read_block(current)
    if block is None:
        return False, "the catalogue has no generated block"
    if structure_only:
        written = structure_from_block(block)
        if written is None or written != structure(manifests):
            return False, "the set of repositories (or their family, role, stack, target or parent) differs from the catalogue: run tools/make_catalog.py"
        return True, "structure current"
    if render(current, manifests) != current:
        return False, "docs/PROJECT_CATALOG.md is out of date: run tools/make_catalog.py"
    return True, "catalogue current"

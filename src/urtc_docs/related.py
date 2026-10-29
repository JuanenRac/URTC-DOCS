# =============================================================================
# URTC-DOCS - src/urtc_docs/related.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Write the Related Projects section of the README files of the other repositories of the family.

The section is the same in every repository (the family by group, then the sister projects), with the
repository's own name in bold; it is produced from the same text and the same list as the README of
this repository (``readmes.related_lines``), so the eight languages and the ten repositories cannot
drift apart. Only the body of the section is replaced: its heading, its place and everything else in
the file stay as they are. Standard library only.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import readmes
from .readme_family import all_names

FILES = {code: filename for code, (filename, _) in readmes.LANGUAGES.items()}
HEADING = "## 🔗 "


def apply_to_text(text: str, code: str, name: str) -> str:
    """The README text with the body of its Related Projects section replaced (the text unchanged when it has no such section)."""
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.replace("\r\n", "\n").split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith(HEADING)), None)
    if start is None:
        raise ValueError("no Related Projects heading (## 🔗)")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"## ", lines[i])), len(lines))
    body = ["", *readmes.related_lines(code, name)]
    return newline.join(lines[: start + 1] + body + lines[end:])


def run(workspace: Path, names: list[str] | None = None, write: bool = False) -> tuple[list[str], int]:
    """(problems, files written or already current). A repository that is not next to this one is a problem."""
    problems: list[str] = []
    done = 0
    for name in sorted(names or all_names()):
        if name == readmes.NAME:
            continue
        folder = workspace / name
        if not folder.is_dir():
            problems.append(f"{name}: not found in {workspace}")
            continue
        for code, filename in FILES.items():
            path = folder / filename
            if not path.is_file():
                problems.append(f"{name}/{filename}: missing")
                continue
            current = path.read_bytes().decode("utf-8")
            try:
                expected = apply_to_text(current, code, name)
            except ValueError as error:
                problems.append(f"{name}/{filename}: {error}")
                continue
            if expected == current:
                done += 1
            elif write:
                path.write_bytes(expected.encode("utf-8"))
                done += 1
            else:
                problems.append(f"{name}/{filename}: the Related Projects section is out of date")
    return problems, done

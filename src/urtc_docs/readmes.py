# =============================================================================
# URTC-DOCS - src/urtc_docs/readmes.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Write README.md and its seven translations of this repository from readme_text.py and its manifest.

The version and the maturity are read from urtc.project.json, and the list
of related projects from readme_family.py, so the eight files have the same
structure and the same links by construction (the CI check of the ecosystem
compares exactly that).
"""
from __future__ import annotations

import json
from pathlib import Path

from . import glance
from .readme_claims_text import COMMENT as CLAIMS_COMMENT, NOTE as CLAIMS_NOTE, TOOLS as CLAIMS_TOOLS
from .readme_drift_text import COMMENT as DRIFT_COMMENT, TOOLS as DRIFT_TOOLS
from .readme_doctor_text import COMMENT as DOCTOR_COMMENT, TOOLS as DOCTOR_TOOLS
from .readme_family import FAMILY_REPOS
from .readme_text import LANGUAGES, TEXT

NAME = "URTC-DOCS"
URL = "https://github.com/JuanenRac/{name}"
BADGE_COLOUR = {"scaffolding": "FFB020", "functional": "0F6CBD", "established": "2EA44F", "production": "2EA44F"}


def language_bar(code: str) -> str:
    items = []
    for other, (filename, label) in LANGUAGES.items():
        if other == code:
            flag, _, text = label.partition(" ")
            items.append(f"{flag} <b>{text}</b>")
        else:
            items.append(f'<a href="{filename}">{label}</a>')
    return '<p align="center">' + " | ".join(items) + "</p>"


def render(code: str, manifest: dict, entry: dict) -> str:
    text = TEXT[code]
    version, maturity = manifest["version"], manifest["maturity"]
    tree = text["tree"]
    lines: list[str] = []
    add = lines.append

    add('<p align="center">')
    add(f'  <img src="images/URTC_DOCS_BANNER.svg" alt="{NAME} banner" width="100%">')
    add("</p>")
    add("")
    add(f"# 📚 {NAME}")
    add("")
    add(language_bar(code))
    add("")
    add(f"### {text['subtitle']}")
    add("")
    add('<p align="center">')
    add('  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">')
    add('  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">')
    add('  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">')
    add(f'  <img src="https://img.shields.io/badge/Version-{version}-0f6cbd.svg" alt="Version">')
    add(f'  <img src="https://img.shields.io/badge/Maturity-{maturity}-{BADGE_COLOUR.get(maturity, "0f6cbd")}.svg" alt="Maturity">')
    add("</p>")
    add("")
    add("---")
    add("")
    add(f"**{text['honesty_label']}** {text['honesty']}")
    add("")
    add("---")
    add("")
    add(CLAIMS_NOTE[code])
    add("")
    add(glance.render_section(code, manifest, entry).rstrip(chr(10)))
    add("")
    add(f"## 🎯 {text['h_overview']}")
    add("")
    add('<p align="center">')
    add('  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">')
    add("</p>")
    add("")
    add(str(text["overview_intro"]))
    add("")
    for label, path, description in text["overview"]:  # type: ignore[misc]
        add(f"* [{label}]({path}): {description}")
    add(f"* **{text['tools_label']}** {text['tools']}{CLAIMS_TOOLS[code]}{DRIFT_TOOLS[code]}{DOCTOR_TOOLS[code]}")
    add("")
    add(f"## 🧩 {text['h_role']}")
    add("")
    add(str(text["role"]))
    add("")
    add(f"## 📂 {text['h_structure']}")
    add("")
    add("```text")
    add(f"{NAME}/")
    add(f"├── docs/     {tree['docs']}")
    add(f"├── src/      {tree['src']}")
    add(f"├── tools/    {tree['tools']}")
    add(f"├── tests/    {tree['tests']}")
    add(f"├── images/   {tree['images']}")
    add(f"├── brand/    {tree['brand']}")
    add("├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat")
    add("└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md")
    add("```")
    add("")
    add(f"## 🛠️ {text['h_dev']}")
    add("")
    add(str(text["dev_requirements"]))
    add("")
    comments = list(text["dev_comments"])
    comments.insert(5, CLAIMS_COMMENT[code])
    comments.insert(6, DRIFT_COMMENT[code])
    comments.insert(8, DOCTOR_COMMENT[code])
    commands = (
        "python tools/make_catalog.py --check",
        "python tools/make_brand.py --check",
        "python tools/make_readmes.py --check",
        "python tools/make_glance.py --check",
        "python tools/publication_check.py",
        "python tools/check_claims.py --require-siblings",
        "python tools/check_repo_tools.py --require-siblings",
        "bash tools/check_all.sh",
        "python tools/urtc_doctor.py",
        "python -m pytest tests -q",
    )
    add("```bash")
    width = max(len(command) for command in commands)
    for command, comment in zip(commands, comments):  # type: ignore[arg-type]
        add(f"{command.ljust(width)}  # {comment}")
    add("```")
    add("")
    add(str(text["dev_note"]))
    add("")
    add(f"## 🔗 {text['h_related']}")
    add("")
    add(str(text["related_intro"]))
    add("")
    for family_name, names in FAMILY_REPOS:
        entries = []
        for name in names:
            if name == NAME:
                entries.append(f"**{name}** ({text['related_this']})")
            else:
                entries.append(f"[{name}]({URL.format(name=name)})")
        add(f"* **{family_name}:** " + ", ".join(entries))
    add("")
    add(f"**{text['related_beyond']}**")
    add("")
    for name, url, description in text["beyond"]:  # type: ignore[misc]
        add(f"* **[{name}]({url})** - {description}")
    add("")
    add(f"## 📚 {text['h_docs']}")
    add("")
    add(str(text["docs_intro"]))
    add("")
    for label, path in text["docs_links"]:  # type: ignore[misc]
        add(f"* [{label}]({path})")
    add(f"* {text['docs_contact']}")
    add("")
    add(f"## 👤 {text['h_author']}")
    add("")
    add("**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com")
    add("")
    add(f"## 📜 {text['h_license']}")
    add("")
    add(str(text["license"]))
    return "\n".join(lines) + "\n"


def outputs(repo: Path) -> dict[str, str]:
    """File name -> content, for the eight languages."""
    manifest = json.loads((repo / "urtc.project.json").read_text(encoding="utf-8"))
    entry = glance.load_data(repo / "data" / "glance.json")[manifest["name"]]
    return {filename: render(code, manifest, entry) for code, (filename, _) in LANGUAGES.items()}

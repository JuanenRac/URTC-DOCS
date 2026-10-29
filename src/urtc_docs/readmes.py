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
from typing import cast

from . import glance, status
from .readme_claims_text import COMMENT as CLAIMS_COMMENT, NOTE as CLAIMS_NOTE, TOOLS as CLAIMS_TOOLS
from .readme_drift_text import COMMENT as DRIFT_COMMENT, TOOLS as DRIFT_TOOLS
from .readme_doctor_text import COMMENT as DOCTOR_COMMENT, TOOLS as DOCTOR_TOOLS
from .readme_family import FAMILY_REPOS
from .readme_text import LANGUAGES, TEXT
from .readme_universal_text import CONTRIBUTING, ICONS, LANGUAGES_TEXT, ROADMAP, SECTION_NAMES, TESTING

NAME = "URTC-DOCS"
URL = "https://github.com/JuanenRac/{name}"
BADGE_COLOUR = {"scaffolding": "FFB020", "functional": "0F6CBD", "established": "2EA44F", "production": "2EA44F"}


ALT_ARCH = {
    "en": "URTC-DOCS architecture: what it reads, what it holds and what it feeds",
    "es": "Arquitectura de URTC-DOCS: qué lee, qué contiene y qué alimenta",
    "de": "Architektur von URTC-DOCS: was es liest, was es enthält und was es speist",
    "fr": "Architecture d'URTC-DOCS : ce qu'il lit, ce qu'il contient et ce qu'il alimente",
    "it": "Architettura di URTC-DOCS: che cosa legge, che cosa contiene e che cosa alimenta",
    "zh": "URTC-DOCS 的架构：读取什么、包含什么、供给什么",
    "ja": "URTC-DOCS のアーキテクチャ：何を読み、何を持ち、何に供給するか",
    "pt": "Arquitetura do URTC-DOCS: o que lê, o que contém e o que alimenta",
}
ARCH_CAPTION = {
    "en": "How the parts of this repository fit together. The picture is drawn from `docs/architecture.json` and checked against the code.",
    "es": "Cómo encajan las partes de este repositorio. La imagen se dibuja desde `docs/architecture.json` y se comprueba contra el código.",
    "de": "Wie die Teile dieses Repositorys zusammenpassen. Das Bild wird aus `docs/architecture.json` gezeichnet und gegen den Code geprüft.",
    "fr": "Comment les parties de ce dépôt s'articulent. L'image est dessinée à partir de `docs/architecture.json` et vérifiée par rapport au code.",
    "it": "Come si incastrano le parti di questo repository. L'immagine è disegnata da `docs/architecture.json` e verificata rispetto al codice.",
    "zh": "本仓库各部分如何协作。图片由 `docs/architecture.json` 绘制，并与代码核对。",
    "ja": "このリポジトリの各部分の関係。図は `docs/architecture.json` から描かれ、コードと照合されます。",
    "pt": "Como as partes deste repositório se encaixam. A imagem é desenhada a partir de `docs/architecture.json` e verificada com o código.",
}
SUMMARY_TREE = {
    "en": "Text version of the tree", "es": "Versión en texto del árbol", "de": "Textversion des Baums", "fr": "Version texte de l'arborescence",
    "it": "Versione testuale dell'albero", "zh": "目录树的文本版", "ja": "ツリーのテキスト版", "pt": "Versão em texto da árvore",
}
ALT_STRUCTURE = {
    "en": "Repository structure of URTC-DOCS", "es": "Estructura del repositorio URTC-DOCS", "de": "Struktur des Repositorys URTC-DOCS", "fr": "Structure du dépôt URTC-DOCS",
    "it": "Struttura del repository URTC-DOCS", "zh": "URTC-DOCS 的仓库结构", "ja": "URTC-DOCS のリポジトリ構成", "pt": "Estrutura do repositório URTC-DOCS",
}


def related_lines(code: str, name: str) -> list[str]:
    """The body of Related Projects for the repository `name`, ending with a blank line: the family by group, then the sister projects."""
    text = TEXT[code]
    out = [str(text["related_intro"]), ""]
    for family_name, names_in_family in FAMILY_REPOS:
        entries = []
        for member in names_in_family:
            if member == name:
                entries.append(f"**{member}** ({text['related_this']})")
            else:
                entries.append(f"[{member}]({URL.format(name=member)})")
        out.append(f"* **{family_name}:** " + ", ".join(entries))
    out += ["", f"**{text['related_beyond']}**", ""]
    for other, url, description in cast("list[tuple[str, str, str]]", text["beyond"]):
        out.append(f"* **[{other}]({url})** - {description}")
    out.append("")
    return out


def architecture_block(name: str, code: str) -> str:
    return (f'<p align="center">\n  <img src="images/architecture.svg" alt="{ALT_ARCH[code]}" width="100%">\n</p>\n\n{ARCH_CAPTION[code]}')


def structure_block(name: str, code: str) -> str:
    """The picture of the repository and the text tree of docs/structure.json (the tree is written by tools/make_structure.py, so the names are the same everywhere)."""
    import importlib.util
    import sys

    root = Path(__file__).resolve().parents[2]
    tools = str(root / "tools")
    sys.path.insert(0, tools)
    try:
        spec_module = importlib.util.spec_from_file_location("urtc_make_structure", root / "tools" / "make_structure.py")
        module = importlib.util.module_from_spec(spec_module)  # type: ignore[arg-type]
        spec_module.loader.exec_module(module)  # type: ignore[union-attr]
        spec = json.loads((root / "docs" / "structure.json").read_text(encoding="utf-8"))
        tree = module.render_tree(spec, code).rstrip("\n")
    finally:
        sys.path.remove(tools)
    if not tree.lstrip().startswith("```"):
        tree = "```text\n" + tree + "\n```"
    return (f'<p align="center">\n  <img src="images/repository-structure.svg" alt="{ALT_STRUCTURE[code]}" width="100%">\n</p>\n\n'
            f"<details>\n<summary>{SUMMARY_TREE[code]}</summary>\n\n{tree}\n\n</details>")


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
    add(status.render_own(code).rstrip(chr(10)))
    add("")
    names = SECTION_NAMES[code]

    def section(key: str, title: str | None = None) -> None:
        add(f"## {ICONS[key]} {title or names[key]}")
        add("")

    section("overview")
    add('<p align="center">')
    add('  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">')
    add("</p>")
    add("")
    add(str(text["overview_intro"]))
    add("")
    for label, path, description in cast("list[tuple[str, str, str]]", text["overview"]):
        add(f"* [{label}]({path}): {description}")
    add(f"* **{text['tools_label']}** {text['tools']}{CLAIMS_TOOLS[code]}{DRIFT_TOOLS[code]}{DOCTOR_TOOLS[code]}")
    add("")
    section("role", str(text["h_role"]))
    add(str(text["role"]))
    add("")
    section("architecture")
    add(architecture_block(NAME, code))
    add("")
    section("quickstart")
    add(str(text["dev_requirements"]))
    add("")
    comments = list(cast("list[str]", text["dev_comments"]))
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
    section("testing")
    add(TESTING[code])
    add("")
    section("build")
    add(str(text["dev_note"]))
    add("")
    section("structure")
    add(structure_block(NAME, code))
    add("")
    section("roadmap")
    add(ROADMAP[code])
    add("")
    section("languages")
    add(LANGUAGES_TEXT[code])
    add("")
    section("related")
    lines.extend(related_lines(code, NAME))
    section("documentation")
    add(str(text["docs_intro"]))
    add("")
    for label, path in cast("list[tuple[str, str]]", text["docs_links"]):
        add(f"* [{label}]({path})")
    add("")
    section("contributing")
    words = CONTRIBUTING[code]
    add(f"* {words['first'].format(cmd='URTC_CI=1 python tools/ci_validate.py')}")
    add(f"* {words['readme']}")
    add(f"* {words['honest']}")
    add(f"* {words['report']}")
    add(f"* {text['docs_contact']}")
    add("")
    section("author")
    add("**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com")
    add("")
    section("license")
    add(str(text["license"]))
    text_out = "\n".join(lines) + "\n"
    # the "Jump to" line that follows the table of At a glance (the same line that tools/make_glance.py writes)
    return glance.apply_to_text(text_out, glance.with_jump(glance.render_section(code, manifest, entry), code, text_out))


def outputs(repo: Path) -> dict[str, str]:
    """File name -> content, for the eight languages."""
    manifest = json.loads((repo / "urtc.project.json").read_text(encoding="utf-8"))
    entry = glance.load_data(repo / "data" / "glance.json")[manifest["name"]]
    return {filename: render(code, manifest, entry) for code, (filename, _) in LANGUAGES.items()}

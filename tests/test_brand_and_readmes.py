# =============================================================================
# URTC-DOCS - tests/test_brand_and_readmes.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import importlib.util
import json
import re
import xml.etree.ElementTree as ElementTree
from pathlib import Path


from urtc_docs import brand, readme_family, readme_text, readmes
from urtc_docs.descriptions import DESCRIPTIONS

REPO = Path(__file__).resolve().parents[1]
PRIVATE = ("SON" + "NET", "BIB" + "LIA", "Cla" + "ude", "Anthro" + "pic")


def load_parity():
    spec = importlib.util.spec_from_file_location("_readme_parity", REPO / "tools" / "_readme_parity.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- brand --------------------------------------------------------------------------------------------

def test_every_asset_is_well_formed_xml_with_a_title():
    for path, content in brand.outputs().items():
        root = ElementTree.fromstring(content)
        assert root.tag.endswith("svg"), path
        assert any(element.tag.endswith("title") for element in root.iter()), path


def test_assets_are_deterministic_and_the_committed_ones_are_current():
    assert brand.outputs() == brand.outputs()
    for relative, content in brand.outputs().items():
        assert (REPO / relative).read_text(encoding="utf-8") == content, relative


def test_the_banner_escapes_the_name():
    assert "&lt;x&amp;y&gt;" in brand.banner("<x&y>")


def test_the_map_has_a_box_for_every_repository_and_no_two_boxes_overlap():
    assert set(brand.NODES) == readme_family.all_names()
    positions = [(x, row) for x, row, _ in brand.NODES.values()]
    assert len(set(positions)) == len(positions)
    text = brand.ecosystem_map()
    for name in brand.NODES:
        assert name in text
    for name in (*brand.SOLID_ON_BUS, *brand.DASHED_ON_BUS):
        assert name in brand.NODES


def test_a_repository_that_waits_for_a_board_is_drawn_dashed_to_the_bus():
    text = brand.ecosystem_map()
    assert text.count("stroke-dasharray=\"5 6\"") == len(brand.DASHED_ON_BUS)
    assert not set(brand.SOLID_ON_BUS) & set(brand.DASHED_ON_BUS)


def test_a_repository_not_in_the_map_would_get_its_own_row_not_a_crash():
    nodes = dict(brand.NODES, **{"URTC-NEW": (600, 4, "a new one")})
    assert "URTC-NEW" in brand.ecosystem_map(nodes)


# --- readme source ------------------------------------------------------------------------------------

def test_every_language_has_the_same_keys_and_no_empty_text():
    reference = readme_text.TEXT["en"]
    for code, block in readme_text.TEXT.items():
        assert set(block) == set(reference), code
        for key, value in block.items():
            assert value, (code, key)
        assert len(block["overview"]) == len(reference["overview"]), code
        assert len(block["dev_comments"]) == len(reference["dev_comments"]), code
        assert set(block["tree"]) == set(reference["tree"]), code
        assert len(block["docs_links"]) == len(reference["docs_links"]), code
        assert [item[1] for item in block["beyond"]] == [item[1] for item in reference["beyond"]], code


def test_eight_languages_in_the_agreed_files():
    assert list(readme_text.LANGUAGES.values())[0][0] == "README.md"
    assert [name for name, _ in readme_text.LANGUAGES.values()] == [
        "README.md", "README_spa.md", "README_fra.md", "README_ita.md", "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md",
    ]


def test_the_family_list_has_no_duplicates_and_matches_the_descriptions():
    names = [name for _, group in readme_family.FAMILY_REPOS for name in group]
    assert len(names) == len(set(names))
    assert set(names) == set(DESCRIPTIONS)
    assert readme_family.all_names() == set(names)
    for name in names:
        assert name == "URTC" or name.startswith("URTC-")


# --- generated READMEs --------------------------------------------------------------------------------

def test_the_committed_readmes_are_what_the_generator_writes():
    for filename, content in readmes.outputs(REPO).items():
        assert (REPO / filename).read_text(encoding="utf-8").replace("\r\n", "\n") == content, filename


def test_every_image_a_readme_shows_exists():
    for filename, text in readmes.outputs(REPO).items():
        for source in re.findall(r'<img src="(images/[^"]+)"', text):
            assert (REPO / source).is_file(), (filename, source)


def test_readmes_pass_the_shared_parity_check_of_the_ecosystem():
    parity = load_parity()
    assert parity.check_readme_section_parity(REPO) == []


def test_every_readme_has_the_same_headings_links_and_version():
    manifest = json.loads((REPO / "urtc.project.json").read_text(encoding="utf-8"))
    outputs = readmes.outputs(REPO)
    headings = {name: re.findall(r"(?m)^## (\S+)", text) for name, text in outputs.items()}
    assert len({tuple(value) for value in headings.values()}) == 1
    assert len(headings["README.md"]) == 9
    links = {name: set(re.findall(r"\]\((https?://[^)\s]+)\)", text)) for name, text in outputs.items()}
    assert len({frozenset(value) for value in links.values()}) == 1
    for name, text in outputs.items():
        assert f"`{manifest['version']}`" in text, name
        assert f"Version-{manifest['version']}-" in text, name
        assert "GPL-3.0-or-later" in text, name


def test_readmes_name_every_repository_of_the_family_once_as_a_link():
    text = readmes.outputs(REPO)["README.md"]
    for _, group in readme_family.FAMILY_REPOS:
        for name in group:
            if name == "URTC-DOCS":
                assert "**URTC-DOCS** (this repository)" in text
            else:
                assert f"[{name}](https://github.com/JuanenRac/{name})" in text


def test_the_language_bar_marks_the_current_language_and_links_the_others():
    bar = readmes.language_bar("es")
    assert "<b>Español</b>" in bar and 'href="README_spa.md"' not in bar and 'href="README.md"' in bar


def test_the_maturity_is_translated_from_the_manifest():
    manifest = {"name": "X", "version": "1.2.3", "maturity": "functional", "technologies": ["Python"], "role": "tool", "deployment_target": "user-pc"}
    entry = {"hardware": "not_applicable"}
    assert "| Funcional |" in readmes.render("es", manifest, entry)
    assert "Maturity-functional" in readmes.render("en", manifest, entry)


def test_no_readme_carries_a_private_name_a_date_or_an_unfinished_marker():
    for filename, text in readmes.outputs(REPO).items():
        for word in PRIVATE:
            assert word.lower() not in text.lower(), (filename, word)
        assert re.search(r"\b20\d\d-\d\d-\d\d\b", text) is None, filename
        assert "TODO" not in text, filename


def test_the_honesty_paragraph_says_that_no_board_exists_in_every_language():
    for code, block in readme_text.TEXT.items():
        assert block["honesty"] and block["honesty_label"], code

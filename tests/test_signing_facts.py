# =============================================================================
# URTC-DOCS - tests/test_signing_facts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The signature statements come from the key files of URTC."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from urtc_docs import readme_claims_text, readmes, signing_facts

HUB = Path(__file__).resolve().parents[1]
REAL = signing_facts.load(HUB / "data" / signing_facts.FACTS_NAME)


def urtc(workspace: Path, release: list, dev: list) -> Path:
    keys = workspace / "URTC" / "keys"
    keys.mkdir(parents=True, exist_ok=True)
    flavours = {"release": {"keys": release}, "dev": {"keys": dev}}
    (keys / "image_trust.json").write_text(json.dumps({"flavours": flavours}), encoding="utf-8")
    registry = {"keys": [{"id": "urtc-release-ed25519", "algorithm": "ed25519", "public": "ab" * 32}]}
    (keys / "registry.json").write_text(json.dumps(registry), encoding="utf-8")
    return workspace / "URTC"


def hub_with(workspace: Path, facts: dict) -> Path:
    hub = workspace / "URTC-DOCS"
    (hub / "data").mkdir(parents=True)
    (hub / "docs").mkdir()
    (hub / "data" / signing_facts.FACTS_NAME).write_text(json.dumps(facts), encoding="utf-8")
    text = f"# Baseline\n\n{signing_facts.BEGIN}\n{signing_facts.END}\n"
    (hub / signing_facts.TABLE_DOCUMENT).write_text(signing_facts.with_table(text, facts), encoding="utf-8")
    return hub


KEY = {"state": "current", "key_id": "00", "public": "cd" * 32}


@pytest.mark.parametrize("release, dev, expected", [([KEY], [KEY], "release_key"), ([], [KEY], "development_only"), ([], [], "unknown")])
def test_the_phrase_follows_the_trust_table(tmp_path, release, dev, expected):
    facts = signing_facts.from_urtc(urtc(tmp_path, release, dev))
    assert signing_facts.variant(facts) == expected
    for code, note in readme_claims_text.NOTE.items():
        assert note.count("{signing}") == 1
        assert readme_claims_text.SIGNING[expected][code]


def test_the_readmes_of_this_repository_carry_the_phrase_of_the_facts():
    for code, name in (("en", "README.md"), ("es", "README_spa.md"), ("ja", "README_jpn.md")):
        phrase = readme_claims_text.SIGNING[signing_facts.variant(REAL)][code]
        assert phrase in (HUB / name).read_text(encoding="utf-8")
    assert readmes.SIGNING_FACTS == HUB / "data" / signing_facts.FACTS_NAME


def test_a_new_key_needs_its_line_in_the_table():
    facts = {"keys": [{"id": "urtc-new", "algorithm": "ed25519", "public": "00" * 32}], "trust": {}}
    with pytest.raises(ValueError, match="urtc-new"):
        signing_facts.table(facts)


def test_a_family_that_agrees_has_no_problem(tmp_path):
    repo = urtc(tmp_path, [KEY], [KEY])
    hub = hub_with(tmp_path, signing_facts.from_urtc(repo))
    (repo / "README.md").write_text("The official table holds the public release keys.\n", encoding="utf-8")
    assert signing_facts.problems(hub, [repo]) == []


@pytest.mark.parametrize("sentence", [
    "The table of the official build is empty until the image-signing key is created.",
    "La tabla de la build oficial está vacía hasta que se cree la clave de firma.",
    "Die offizielle Schlüsseltabelle ist leer.",
    "La table de clés officielle est vide.",
    "La tabella di chiavi ufficiale è vuota.",
    "A tabela de chaves oficial está vazia.",
    "公式の鍵テーブルは空です。",
    "官方密钥表为空。",
])
def test_a_document_that_still_calls_the_table_empty_fails(tmp_path, sentence):
    repo = urtc(tmp_path, [KEY], [KEY])
    hub = hub_with(tmp_path, signing_facts.from_urtc(repo))
    (repo / "README.md").write_text(sentence + "\n", encoding="utf-8")
    assert any("official trust table is empty" in found for found in signing_facts.problems(hub, [repo]))


def test_with_an_empty_table_the_same_sentence_is_true(tmp_path):
    repo = urtc(tmp_path, [], [KEY])
    hub = hub_with(tmp_path, signing_facts.from_urtc(repo))
    (repo / "README.md").write_text("The official key table is empty.\n", encoding="utf-8")
    assert signing_facts.problems(hub, [repo]) == []


def test_a_copy_behind_urtc_and_an_edited_table_fail(tmp_path):
    repo = urtc(tmp_path, [KEY], [KEY])
    hub = hub_with(tmp_path, signing_facts.from_urtc(repo))
    urtc(tmp_path, [], [KEY])
    assert any("is not what URTC says today" in found for found in signing_facts.problems(hub, [repo]))
    document = hub / signing_facts.TABLE_DOCUMENT
    document.write_text(document.read_text(encoding="utf-8").replace("Ed25519", "HMAC"), encoding="utf-8")
    assert any("signing table" in found for found in signing_facts.problems(hub, []))


def test_an_hmac_given_to_the_main_bootloader_fails_in_this_repository(tmp_path):
    repo = urtc(tmp_path, [KEY], [KEY])
    hub = hub_with(tmp_path, signing_facts.from_urtc(repo))
    note = hub / "docs" / "NOTE.md"
    note.write_text("The main bootloader checks an HMAC-SHA256 of the image.\n", encoding="utf-8")
    assert any("HMAC" in found for found in signing_facts.problems(hub, [repo]))
    note.write_text("The main bootloader of the earlier generation checks an HMAC.\n", encoding="utf-8")
    assert signing_facts.problems(hub, [repo]) == []


def test_the_documents_of_this_repository_agree_with_its_own_copy():
    assert signing_facts.problems(HUB, []) == []

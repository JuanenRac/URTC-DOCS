# =============================================================================
# URTC-DOCS - tests/test_claims.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The claim check: risk words need a status marker or a reviewed line."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import write_repo
from urtc_docs import claims, cli


def readme(repo: Path, text: str) -> None:
    (repo / "README.md").write_text(text, encoding="utf-8")


def test_a_risk_word_without_a_marker_is_reported():
    found = claims.findings("# Title\n\nThe controller has an E-STOP and enforces torque limits.\n")
    assert len(found) == 1 and "E-STOP" in found[0][1]


def test_a_marker_in_the_sentence_or_next_to_it_clears_it():
    assert claims.findings("The controller has an E-STOP (planned).\n") == []
    assert claims.findings("There is no E-STOP yet.\n") == []
    assert claims.findings("Safety interlocks guard the door. Not implemented.\n") == []
    assert claims.findings("Safety interlocks guard the door. A second sentence. A third. Not implemented.\n") != []


def test_each_list_item_and_table_row_stands_alone():
    text = "* E-STOP wired to the drive.\n* Everything else is planned.\n"
    assert len(claims.findings(text)) == 1
    table = "| a | b |\n|---|---|\n| E-STOP | in use |\n| other | planned |\n"
    assert len(claims.findings(table)) == 1


def test_code_blocks_names_urls_and_inline_code_are_ignored():
    text = "```\nE-STOP everywhere\n```\n\nSee URTC-FLASHER and https://example.org/estop and `interlock_ok`.\n"
    assert claims.findings(text) == []


def test_badges_are_read_by_their_words():
    badge = '<img src="https://img.shields.io/badge/Bus-FDCAN-yellow.svg" alt="FDCAN">\n'
    assert len(claims.findings(badge)) == 1
    honest = '<img src="https://img.shields.io/badge/Bus-Classic%20CAN%20(FDCAN%20peripheral)-yellow.svg" alt="Classic CAN">\n'
    # The word "classic" is not a status marker: the label alone does not clear the risk word.
    assert len(claims.findings(honest)) == 1
    assert claims.findings(honest.replace("peripheral", "peripheral, no FDCAN frames")) == []


def test_a_roadmap_section_describes_what_is_not_there():
    text = "## Overview\n\nHas an E-STOP.\n\n## Roadmap\n\n* AI-driven maintenance.\n\n## Other\n\nHas an interlock.\n"
    lines = [line for line, _sentence in claims.findings(text)]
    assert lines == [3, 11]


def test_the_key_of_a_sentence_ignores_case_spacing_and_punctuation():
    assert claims.key_of("Has an  E-STOP!") == claims.key_of("has an e stop")


def test_reviewed_lines_clear_a_sentence_for_one_repository_or_for_all(tmp_path):
    write_repo(tmp_path, "URTC-A")
    write_repo(tmp_path, "URTC-B")
    for name in ("URTC-A", "URTC-B"):
        readme(tmp_path / name, "Controls the E-STOP relay.\n")
    key = claims.key_of("Controls the E-STOP relay.")
    only_a = {"URTC-A": {key: "x"}}
    assert claims.check_repo(tmp_path / "URTC-A", only_a)[0] == []
    assert len(claims.check_repo(tmp_path / "URTC-B", only_a)[0]) == 1
    assert claims.check_repo(tmp_path / "URTC-B", {"*": {key: "x"}})[0] == []


def test_repositories_are_the_family_without_the_hub(tmp_path):
    for name in ("URTC", "URTC-X", "URTC-DOCS", "HYDRA-UMC", "OTHER", "URTCX"):
        (tmp_path / name).mkdir()
        readme(tmp_path / name, "text\n")
    names = [repo.name for repo in claims.repositories(tmp_path, "URTC-DOCS")]
    assert names == ["URTC", "URTC-X"]


def test_build_reviewed_shares_lines_found_in_three_repositories_but_not_maturity(tmp_path):
    for name in ("URTC-A", "URTC-B", "URTC-C"):
        (tmp_path / name).mkdir()
        readme(tmp_path / name, "Real-time dashboard.\n\n| Maturity | Established |\n")
    (tmp_path / "URTC-A" / "README.md").write_text("Real-time dashboard.\n\nLocal interlock.\n", encoding="utf-8")
    reviewed = claims.build_reviewed(tmp_path, "URTC-DOCS")
    assert claims.key_of("Real-time dashboard.") in reviewed["*"]
    assert claims.key_of("Maturity | Established") not in reviewed.get("*", {})
    assert claims.key_of("Maturity | Established") in reviewed["URTC-B"]


def test_the_command_passes_fails_and_skips(tmp_path, capsys):
    hub = tmp_path / "URTC-DOCS"
    hub.mkdir()
    data = tmp_path / "reviewed.json"
    args = ["--workspace", str(tmp_path), "--data", str(data)]
    assert cli.check_claims(args) == 0
    assert "CLAIMS=SKIP" in capsys.readouterr().out
    assert cli.check_claims(args + ["--require-siblings"]) == 1
    capsys.readouterr()
    write_repo(tmp_path, "URTC-X")
    readme(tmp_path / "URTC-X", "Has an E-STOP.\n")
    assert cli.check_claims(args) == 1
    err = capsys.readouterr().err
    assert "URTC-X/README.md:1" in err and "CLAIMS=FAIL" in err
    assert cli.check_claims(args + ["--update-reviewed"]) == 1
    assert not data.exists()
    assert "--confirm --reviewer" in capsys.readouterr().err
    assert cli.check_claims(args + ["--update-reviewed", "--confirm"]) == 1
    assert not data.exists()
    assert cli.check_claims(args + ["--update-reviewed", "--confirm", "--reviewer", "someone"]) == 0
    written = json.loads(data.read_text(encoding="utf-8"))
    assert written["log"][0]["reviewer"] == "someone" and len(written["log"][0]["added"]) == 1
    # With nothing new to accept, no confirmation is needed and the log stays.
    assert cli.check_claims(args + ["--update-reviewed"]) == 0
    assert json.loads(data.read_text(encoding="utf-8"))["log"] == written["log"]
    assert written["reviewed"]["URTC-X"]
    capsys.readouterr()
    assert cli.check_claims(args) == 0
    assert "CLAIMS=PASS" in capsys.readouterr().out


def test_a_stale_reviewed_line_is_noted_and_fails_only_when_strict(tmp_path, capsys):
    write_repo(tmp_path, "URTC-X")
    readme(tmp_path / "URTC-X", "Fine text.\n")
    data = tmp_path / "reviewed.json"
    data.write_text(json.dumps({"reviewed": {"URTC-X": {"abcdef123456": "gone"}}}), encoding="utf-8")
    args = ["--workspace", str(tmp_path), "--data", str(data)]
    assert cli.check_claims(args) == 0
    assert "no longer match" in capsys.readouterr().out
    assert cli.check_claims(args + ["--strict-stale"]) == 1


def test_the_reviewed_file_of_this_repository_is_valid_json_with_short_keys():
    path = cli.CLAIMS_FILE
    data = json.loads(path.read_text(encoding="utf-8"))["reviewed"]
    for entries in data.values():
        assert all(len(key) == 12 for key in entries)


@pytest.mark.parametrize("sentence", [
    "The E-STOP is certified and tested.",
    "Signed firmware, no exceptions.",
    "A classic safety interlock guards the door.",
    "The E-STOP would stop every axis.",
    "Tests cover the emergency stop.",
    "Not only signed but also encrypted.",
    "It has no display, and the firmware is signed.",
    "Nothing in the long list of parts of this big machine changes how the interlock works.",
    "The E-STOP stops the drives until a person releases it.",
])
def test_a_loose_word_no_longer_clears_a_claim(sentence):
    assert len(claims.findings(sentence + "\n")) == 1


@pytest.mark.parametrize("sentence", [
    "The E-STOP is not certified.",
    "There is no hardware E-STOP path.",
    "It never sends an emergency stop.",
    "The link isn't encrypted.",
    "Runs without authentication.",
    "The E-STOP has not been tested on hardware.",
    "An untested interlock guards the door.",
    "The safety logic runs in a simulator.",
])
def test_an_explicit_negation_or_marker_clears_a_claim(sentence):
    assert claims.findings(sentence + "\n") == []


def test_a_negation_in_a_neighbouring_sentence_does_not_count():
    assert len(claims.findings("There is no display. The E-STOP stops the drives. Nobody can say no.\n")) == 1


def test_explain_says_what_cleared_each_sentence(tmp_path, capsys):
    text = "* The E-STOP is not signed.\n* The interlock is planned.\n* Signed firmware.\n"
    assert [why for _line, _sentence, why in claims.explain(text)] == ["negation 'not'", "marker 'planned'", ""]
    write_repo(tmp_path, "URTC-X")
    readme(tmp_path / "URTC-X", text)
    assert cli.check_claims(["--workspace", str(tmp_path), "--data", str(tmp_path / "r.json"), "--explain"]) == 1
    out = capsys.readouterr().out
    assert "[negation 'not']" in out and "[nothing] Signed firmware." in out


def test_update_reviewed_keeps_what_was_accepted_and_asks_only_for_new_lines(tmp_path):
    write_repo(tmp_path, "URTC-X")
    readme(tmp_path / "URTC-X", "Has an E-STOP.\n")
    shared = claims.key_of("Has an E-STOP.")
    previous = {"*": {shared: "Has an E-STOP."}}
    proposed = claims.build_reviewed(tmp_path, "URTC-DOCS", previous)
    assert proposed["*"] == previous["*"]
    assert claims.additions(previous, proposed) == []


def test_a_pending_line_passes_is_counted_and_only_leaves_the_list(tmp_path, capsys):
    write_repo(tmp_path, "URTC-X")
    readme(tmp_path / "URTC-X", "Has an E-STOP.\n")
    data = tmp_path / "claims_reviewed.json"
    pending_file = tmp_path / "claims_pending.json"
    key = claims.key_of("Has an E-STOP.")
    claims.save_pending(pending_file, {"URTC-X": {key: "Has an E-STOP."}})
    args = ["--workspace", str(tmp_path), "--data", str(data)]
    assert cli.check_claims(args) == 0
    assert "1 line(s) still wait" in capsys.readouterr().out
    # A new sentence is not covered, and rewriting the reviewed list never adds to the pending one.
    readme(tmp_path / "URTC-X", "Has an E-STOP.\n\nHas an interlock.\n")
    assert cli.check_claims(args) == 1
    assert cli.check_claims(args + ["--update-reviewed"]) == 1
    assert list(claims.load_pending(pending_file)["URTC-X"]) == [key]
    # Confirming the new line leaves the pending one where it is; only naming its repository moves it.
    assert cli.check_claims(args + ["--update-reviewed", "--confirm", "--reviewer", "someone"]) == 0
    assert list(claims.load_pending(pending_file)["URTC-X"]) == [key]
    assert key not in claims.load_reviewed(data).get("URTC-X", {})
    assert cli.check_claims(args) == 0
    assert cli.check_claims(args + ["--update-reviewed", "--accept-pending", "URTC-X", "--confirm", "--reviewer", "someone"]) == 0
    assert claims.load_pending(pending_file) == {}
    assert key in claims.load_reviewed(data)["URTC-X"]


def test_the_pending_list_loses_what_a_readme_no_longer_says():
    pending = {"A": {"k1": "x", "k2": "y"}, "B": {"k3": "z"}}
    assert claims.without(pending, {"*": {"k3": "z"}}, {"A": {"k2"}}) == {"A": {"k2": "y"}}


def test_the_pending_file_of_this_repository_holds_only_keys_of_its_texts():
    path = cli.CLAIMS_FILE.with_name("claims_pending.json")
    for entries in claims.load_pending(path).values():
        assert all(len(key) == 12 for key in entries)


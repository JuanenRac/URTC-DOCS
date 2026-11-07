# =============================================================================
# URTC-DOCS - tests/test_gap_cases.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Failures of the test counter that the other tests do not reach: an unreadable data file, a runner that cannot start or times out, a repository counted with
unittest, a missing test folder and a repository with no tests documented. Subprocesses are replaced by fakes; nothing is run."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from urtc_docs import count_tests


def data_file(tmp_path: Path, repos: dict) -> Path:
    path = tmp_path / "glance.json"
    path.write_text(json.dumps({"repos": repos}), encoding="utf-8")
    return path


def test_a_data_file_that_cannot_be_read_is_a_clear_error(tmp_path):
    with pytest.raises(count_tests.CountError, match="cannot read"):
        count_tests.load_documented(tmp_path / "missing.json")
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(count_tests.CountError, match="cannot read"):
        count_tests.load_documented(bad)


@pytest.mark.parametrize("content", ['{}', '{"repos": []}', '{"repos": {"A": 3}}', '[]', '{"repos": null}'])
def test_a_data_file_of_the_wrong_shape_is_a_clear_error(tmp_path, content):
    path = tmp_path / "glance.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(count_tests.CountError):
        count_tests.load_documented(path)


def test_the_documented_counts_are_read_and_a_missing_one_is_none(tmp_path):
    path = data_file(tmp_path, {"A": {"tests": {"count": 4}}, "B": {"tests": None}, "C": {}, "D": {"tests": {}}})
    assert count_tests.load_documented(path) == {"A": 4, "B": None, "C": None, "D": None}


def test_a_runner_that_cannot_start_or_times_out_is_a_count_error(monkeypatch, tmp_path):
    def raising(error):
        def fake(*args, **kwargs):
            raise error
        return fake

    for error in (OSError("no such program"), subprocess.TimeoutExpired("pytest", 1)):
        monkeypatch.setattr(count_tests.subprocess, "run", raising(error))
        with pytest.raises(count_tests.CountError):
            count_tests._run(["pytest", "--collect-only"], tmp_path)


def test_the_output_of_both_streams_is_kept_and_the_search_path_is_passed(monkeypatch, tmp_path):
    seen = {}

    def fake(command, cwd, env, **kwargs):
        seen.update(env=env, cwd=cwd)
        return SimpleNamespace(stdout="out ", stderr="err")

    monkeypatch.setattr(count_tests.subprocess, "run", fake)
    assert count_tests._run(["x"], tmp_path, "/some/path") == "out err"
    assert seen["env"]["PYTHONPATH"] == "/some/path" and seen["cwd"] == tmp_path
    monkeypatch.setattr(count_tests.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=None, stderr=None))
    assert count_tests._run(["x"], tmp_path) == ""


def test_a_repository_counted_with_unittest_uses_its_summary_line(monkeypatch, tmp_path):
    repo = tmp_path / "URTC-DEVTOOLS"
    repo.mkdir()
    monkeypatch.setattr(count_tests, "_run", lambda *a, **k: "COUNT=95 FAILED=0")
    assert count_tests.count_repo(repo) == (95, "")
    monkeypatch.setattr(count_tests, "_run", lambda *a, **k: "COUNT=95 FAILED=3")
    counted, note = count_tests.count_repo(repo)
    assert counted is None and "unittest discovery failed" in note
    monkeypatch.setattr(count_tests, "_run", lambda *a, **k: "")
    assert count_tests.count_repo(repo)[0] is None


def test_a_repository_whose_test_folder_is_missing_is_unknown_not_zero(tmp_path):
    repo = tmp_path / "URTC-VISION-TOOL"
    repo.mkdir()
    counted, note = count_tests.count_repo(repo)
    assert counted is None and "test folder is missing" in note


def test_pytest_that_cannot_collect_is_unknown_not_zero(monkeypatch, tmp_path):
    repo = tmp_path / "URTC-Z"
    repo.mkdir()
    monkeypatch.setattr(count_tests, "_run", lambda *a, **k: "ImportError while importing\n3 errors in 0.2s")
    counted, note = count_tests.count_repo(repo)
    assert counted is None and "pytest could not collect" in note
    monkeypatch.setattr(count_tests, "_run", lambda *a, **k: "41 tests collected in 0.3s")
    assert count_tests.count_repo(repo) == (41, "")


def test_a_repository_with_no_tests_documented_is_not_counted(monkeypatch, tmp_path):
    (tmp_path / "URTC-Q").mkdir()
    monkeypatch.setattr(count_tests, "count_repo", lambda repo: pytest.fail("a repository with no tests documented must not be counted"))
    results = count_tests.compare(tmp_path, data_file(tmp_path, {"URTC-Q": {"tests": None}}))
    assert len(results) == 1 and results[0].documented is None and results[0].counted is None
    assert results[0].agrees and not results[0].exact and results[0].note == "no tests documented"


def test_a_name_that_is_not_in_the_data_is_an_error(tmp_path):
    path = data_file(tmp_path, {"URTC-A": {"tests": {"count": 1}}})
    with pytest.raises(count_tests.CountError, match="not in glance.json"):
        count_tests.compare(tmp_path, path, ["URTC-B"])


def test_the_comparison_agrees_when_nothing_was_counted_or_the_numbers_match():
    assert count_tests.Result("A", 5, None, "").agrees and not count_tests.Result("A", 5, None, "").exact
    assert count_tests.Result("A", 5, 5, "").agrees and count_tests.Result("A", 5, 5, "").exact
    assert not count_tests.Result("A", 5, 6, "").agrees
    assert count_tests.Result("A", 0, 0, "").agrees


@pytest.mark.parametrize(("text", "expected"), [
    ("0 tests collected in 0.1s", 0),
    ("1 test collected", 1),
    ("12345 tests collected", 12345),
    ("1 error in 0.1s", None),
    ("2 errors in 0.2s", None),
    ("3 tests collected, 1 error in 0.2s", None),
    ("", None),
])
def test_pytest_summary_variants(text, expected):
    assert count_tests.parse_pytest(text) == expected


def test_the_results_are_listed_in_name_order(monkeypatch, tmp_path):
    for name in ("URTC-B", "URTC-A", "URTC-C"):
        (tmp_path / name).mkdir()
    monkeypatch.setattr(count_tests, "count_repo", lambda repo: (3, ""))
    data = data_file(tmp_path, {name: {"tests": {"count": 3}} for name in ("URTC-B", "URTC-A", "URTC-C")})
    assert [r.repo for r in count_tests.compare(tmp_path, data)] == ["URTC-A", "URTC-B", "URTC-C"]
    assert [r.repo for r in count_tests.compare(tmp_path, data, ["URTC-C", "URTC-A"])] == ["URTC-A", "URTC-C"]

# =============================================================================
# URTC-DOCS - tests/test_count_tests.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The test counter: parsing the runners' output, the comparison with the data file and --apply."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from urtc_docs import cli, count_tests


def data_file(tmp_path: Path, **counts) -> Path:
    path = tmp_path / "glance.json"
    path.write_text(json.dumps({"repos": {name: {"tests": {"count": count}} for name, count in counts.items()}}, indent=2) + "\n", encoding="utf-8")
    return path


def test_pytest_output_is_parsed_and_collection_errors_mean_unknown():
    assert count_tests.parse_pytest("a.py::t\n\n12 tests collected in 0.5s\n") == 12
    assert count_tests.parse_pytest("1 test collected in 0.1s") == 1
    assert count_tests.parse_pytest("32 tests collected, 10 errors in 2.70s") is None
    assert count_tests.parse_pytest("nothing useful") is None


def test_unittest_output_is_parsed_and_failed_loads_mean_unknown():
    assert count_tests.parse_unittest("COUNT=28 FAILED=0") == 28
    assert count_tests.parse_unittest("COUNT=28 FAILED=2") is None
    assert count_tests.parse_unittest("") is None


def test_a_repository_that_needs_a_toolchain_is_unknown_not_zero(tmp_path):
    (tmp_path / "URTC-SMART-RACK").mkdir()
    results = count_tests.compare(tmp_path, data_file(tmp_path, **{"URTC-SMART-RACK": 5}))
    assert results[0].counted is None and results[0].agrees and "C compiler" in results[0].note


def test_a_missing_repository_is_skipped(tmp_path):
    results = count_tests.compare(tmp_path, data_file(tmp_path, **{"URTC-X": 5}))
    assert not results[0].exact and results[0].agrees


def test_a_real_suite_is_counted_and_compared(tmp_path):
    repo = tmp_path / "URTC-X"
    (repo / "tests").mkdir(parents=True)
    (repo / "tests" / "test_a.py").write_text("def test_one():\n    pass\n\n\ndef test_two():\n    pass\n", encoding="utf-8")
    ok = count_tests.compare(tmp_path, data_file(tmp_path, **{"URTC-X": 2}))[0]
    assert ok.counted == 2 and ok.agrees
    stale_data = data_file(tmp_path, **{"URTC-X": 7})
    stale = count_tests.compare(tmp_path, stale_data)[0]
    assert stale.counted == 2 and not stale.agrees
    assert count_tests.apply_counts(stale_data, [stale]) == ["URTC-X"]
    assert json.loads(stale_data.read_text(encoding="utf-8"))["repos"]["URTC-X"]["tests"]["count"] == 2


def test_unknown_repository_name_is_an_error(tmp_path):
    with pytest.raises(count_tests.CountError):
        count_tests.compare(tmp_path, data_file(tmp_path, **{"URTC-X": 1}), ["URTC-Y"])


def test_the_command_fails_on_a_stale_number_and_passes_after_apply(tmp_path, capsys):
    repo = tmp_path / "URTC-X"
    repo.mkdir()
    (repo / "test_a.py").write_text("def test_one():\n    pass\n", encoding="utf-8")
    data = data_file(tmp_path, **{"URTC-X": 9})
    args = ["--workspace", str(tmp_path), "--data", str(data)]
    assert cli.check_test_counts(args) == 1
    assert "DIFFERS URTC-X" in capsys.readouterr().out
    assert cli.check_test_counts(args + ["--apply"]) == 0
    assert cli.check_test_counts(args) == 0

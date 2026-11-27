# =============================================================================
# URTC-DOCS - tests/test_process_output_encoding.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""What the programs started by the test counter and the doctor print is read as UTF-8, whatever the code page of the computer (Windows: cp1252)."""
from __future__ import annotations

import io
import json
import locale
import re
import subprocess
import sys
from pathlib import Path

import pytest

from urtc_docs import cli, count_tests, doctor, readme_universal_text


@pytest.fixture
def cp1252(monkeypatch):
    # the same answer a Western European Windows gives; PYTHONUTF8 off, as it is by default there
    monkeypatch.setattr(locale, "getencoding", lambda: "cp1252", raising=False)
    monkeypatch.setattr(locale, "getpreferredencoding", lambda do_setlocale=True: "cp1252")
    monkeypatch.delenv("PYTHONUTF8", raising=False)
    monkeypatch.delenv("PYTHONIOENCODING", raising=False)


def test_the_counter_reads_utf8_bytes_the_code_page_cannot_decode(cp1252, tmp_path):
    # the second byte of this capital A with an acute accent is 0x81, which cp1252 has no character for
    child = r"import sys; sys.stdout.buffer.write('\u00c1\n12 tests collected in 0.1s\n'.encode('utf-8'))"
    assert count_tests.parse_pytest(count_tests._run([sys.executable, "-c", child], tmp_path)) == 12


def test_the_counter_lets_a_child_python_print_any_character(cp1252, tmp_path):
    child = "print('a \u2192 b'); print('COUNT=' + '3 FAILED=0')"
    assert count_tests.parse_unittest(count_tests._run([sys.executable, "-c", child], tmp_path)) == 3


def test_the_doctor_shows_the_last_line_of_a_program_that_prints_any_character(cp1252, tmp_path):
    flasher = tmp_path / "URTC-FLASHER"
    (flasher / "tools").mkdir(parents=True)
    (flasher / "tools" / "sync_firmware.py").write_text("print('firmware/ \u00c1 \u2192 consistent')\n", encoding="utf-8")
    lines = doctor.check_firmware(tmp_path, python=sys.executable, runner=subprocess.run)
    first = next(line for line in lines if line.name == "URTC-FLASHER firmware/")
    assert first.status == doctor.PASS
    assert first.detail == "firmware/ Á → consistent"


def test_the_report_is_printed_on_an_output_that_cannot_hold_every_character(monkeypatch):
    raw = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(raw, encoding="cp1252"))
    monkeypatch.setattr(doctor, "run_doctor", lambda *args, **kwargs: [doctor.Line("firmware", "images", doctor.PASS, "firmware/ → consistent")])
    assert cli.doctor(["--fast"]) == 0
    sys.stdout.flush()
    assert b"firmware/ ? consistent" in raw.getvalue()


def test_the_readme_states_the_count_of_the_table():
    data = json.loads((Path(__file__).resolve().parents[1] / "data" / "glance.json").read_text(encoding="utf-8"))
    expected = str(data["repos"]["URTC-DOCS"]["tests"]["count"])
    for language, text in readme_universal_text.TESTING.items():
        assert expected in re.findall(r"\d+", text), f"the {language} text does not state {expected}"

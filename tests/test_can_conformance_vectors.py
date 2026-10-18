# =============================================================================
# URTC-DOCS - tests/test_can_conformance_vectors.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The shared CAN protocol vectors are well formed and agree with themselves.

tests/fixtures/can_conformance_vectors.json is the reference copy of the
vectors that the Flasher, the Tester and the Web Studio each keep a committed
copy of and run their own reader against. Nothing in those repositories reads
this one at run time. Here the file is only checked for being coherent: every
expected value is recomputed with a small independent implementation, so a
mistake in a vector is caught before it is copied anywhere."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

PATH = Path(__file__).parent / "fixtures" / "can_conformance_vectors.json"
VECTORS = json.loads(PATH.read_text(encoding="utf-8"))
SECTIONS = ["identifiers", "magic_payloads", "slcan_encode", "slcan_encode_rejected", "slcan_decode", "quick_state", "version_query", "minor_field", "version_order"]
CLIENTS = {"flasher", "tester", "web"}
HEX_ID = re.compile(r"^0x[0-9A-F]{3}$")
HEX_DATA = re.compile(r"^([0-9A-F]{2}){0,8}$")


def test_the_file_is_utf8_json_with_a_format_number_and_every_section():
    assert VECTORS["format"] == 1
    assert isinstance(VECTORS["about"], str) and VECTORS["about"]
    for section in SECTIONS:
        assert isinstance(VECTORS[section], list) and VECTORS[section], section
    assert set(VECTORS) == {"format", "about", *SECTIONS}
    assert PATH.read_bytes().endswith(b"\n") and b"\r" not in PATH.read_bytes()


def test_identifiers_are_unique_standard_ids_known_to_at_least_two_clients():
    seen = set()
    for entry in VECTORS["identifiers"]:
        assert HEX_ID.match(entry["id"]), entry
        assert int(entry["id"], 16) <= 0x7FF
        assert entry["id"] not in seen
        seen.add(entry["id"])
        assert set(entry["names"]) <= CLIENTS and len(entry["names"]) >= 2, entry
        assert all(re.fullmatch(r"CAN_ID_[A-Z0-9_]+", name) for name in entry["names"].values()), entry


def test_the_bootloader_range_is_present():
    ids = {entry["id"] for entry in VECTORS["identifiers"]}
    assert {f"0x{value:03X}" for value in range(0x7F0, 0x800)} <= ids


def test_magic_payloads():
    names = [entry["name"] for entry in VECTORS["magic_payloads"]]
    assert len(names) == len(set(names))
    assert set(names) == {"enter_bootloader", "authorize_downgrade", "erase_fram", "solder_feeder_reset"}
    for entry in VECTORS["magic_payloads"]:
        assert HEX_ID.match(entry["id"]) and HEX_DATA.match(entry["data"]) and len(entry["data"]) == 8, entry


def line_for(identifier: int, data: bytes) -> str:
    return "t%03X%X%s" % (identifier, len(data), data.hex().upper())


def test_encode_lines_are_what_the_slcan_framing_says():
    for entry in VECTORS["slcan_encode"]:
        assert HEX_ID.match(entry["id"]) and HEX_DATA.match(entry["data"]), entry
        assert entry["line"] == line_for(int(entry["id"], 16), bytes.fromhex(entry["data"])), entry
    covered = {int(e["id"], 16) for e in VECTORS["slcan_encode"]}
    assert 0x000 in covered and 0x7FF in covered
    assert any(len(e["data"]) == 0 for e in VECTORS["slcan_encode"]) and any(len(e["data"]) == 16 for e in VECTORS["slcan_encode"])


def test_rejected_encodes_are_really_out_of_range():
    for entry in VECTORS["slcan_encode_rejected"]:
        too_big = int(entry["id"], 16) > 0x7FF
        too_long = len(entry["data"]) // 2 > 8
        assert too_big or too_long, entry


def test_decode_vectors_are_consistent():
    names = [entry["name"] for entry in VECTORS["slcan_decode"]]
    assert len(names) == len(set(names))
    for entry in VECTORS["slcan_decode"]:
        frame = entry["frame"]
        if frame is None:
            continue
        assert HEX_ID.match(frame["id"]) and HEX_DATA.match(frame["data"]), entry
        if "note" not in entry:
            # An accepted line is exactly the framing of its frame, in either hex case.
            assert entry["line"][0] == "t"
            assert entry["line"][1:].upper() == line_for(int(frame["id"], 16), bytes.fromhex(frame["data"]))[1:], entry
    rejected = [e for e in VECTORS["slcan_decode"] if e["frame"] is None]
    assert len(rejected) >= 10
    assert any(e["line"].startswith("T") for e in rejected), "extended frames must be covered"
    assert any(e["line"][:1] in "rR" and e["line"] for e in rejected), "remote frames must be covered"
    assert any(e["frame"] is not None and "note" in e for e in VECTORS["slcan_decode"]), "the timestamp case must be marked as a tolerated difference"


def test_quick_state_expectations_follow_the_documented_layout():
    for entry in VECTORS["quick_state"]:
        data = bytes.fromhex(entry["data"])
        expect = entry["expect"]
        if len(data) < 4:
            assert expect is None
            continue
        assert expect["tool_id"] == data[0]
        assert expect["system_error"] is bool(data[1])
        assert expect["can_error"] is bool(data[2])
        assert expect["booting"] is bool(data[3])
        assert expect["thermal_fault"] == (data[4] if len(data) > 4 else None)
        assert expect["reset_cause"] == (data[5] if len(data) > 5 else None)
        assert expect["watchdog_reset"] is bool(len(data) > 5 and data[5] & 1)


def test_version_query_expectations_follow_the_documented_frames():
    for entry in VECTORS["version_query"]:
        frames = {int(identifier, 16): bytes.fromhex(data) for identifier, data in entry["frames"]}
        assert len(frames) == len(entry["frames"]), "one frame per identifier"
        first = frames[0x7F9]
        expect = entry["expect"]
        if len(first) < 8:
            assert expect is None
            continue
        assert expect["responder"] == ("application" if first[0] == 0 else "bootloader")
        assert int(expect["hardware_id"], 16) == int.from_bytes(first[1:5], "big")
        assert expect["major"] == int.from_bytes(first[5:7], "big") and expect["minor"] == first[7]
        patch_frame = frames.get(0x7E9)
        aware = patch_frame is not None and len(patch_frame) >= 3
        assert expect["patch_aware"] is aware
        assert expect["patch"] == (None if not aware or patch_frame[1] == 0xFF else patch_frame[1])
        assert expect["accepts_patch_in_end_update"] is bool(aware and patch_frame[2] & 1)
        if "bootloader" in expect:
            assert list(frames[0x7FA][:3]) == expect["bootloader"]


def reference_minor_field(minor: int, patch, accepts: bool) -> int:
    if accepts and patch is not None and 0 <= patch <= 0x7F:
        return ((0x80 | patch) << 8) | (minor & 0xFF)
    return minor


def test_minor_field_expectations():
    for entry in VECTORS["minor_field"]:
        assert entry["expect"] == reference_minor_field(entry["minor"], entry["patch"], entry["bootloader_accepts_patch"]), entry
        assert 0 <= entry["expect"] <= 0xFFFF


def reference_order(installed, candidate) -> int:
    if candidate[0] != installed[0]:
        return 1 if candidate[0] > installed[0] else -1
    if candidate[1] != installed[1]:
        return 1 if candidate[1] > installed[1] else -1
    if installed[2] is not None and candidate[2] is not None and candidate[2] != installed[2]:
        return 1 if candidate[2] > installed[2] else -1
    return 0


@pytest.mark.parametrize("entry", VECTORS["version_order"], ids=lambda entry: json.dumps([entry["installed"], entry["candidate"]]))
def test_version_order_expectations(entry):
    assert entry["expect"] == reference_order(entry["installed"], entry["candidate"])

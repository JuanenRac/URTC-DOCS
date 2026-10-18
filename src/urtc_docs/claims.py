# =============================================================================
# URTC-DOCS - src/urtc_docs/claims.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Claim hygiene: a README may not state a risky capability without saying what its status is.

A README that says, in the present tense, that a robot "has" an E-STOP, "enforces" limits, "uses" signed
firmware or "runs" a detector is read as true. This module scans the English README of every repository
next to this one and finds the sentences that contain a *risk word* (E-STOP, interlock, torque, real-time,
signed, mTLS, FDCAN, YOLO, AI-driven, autonomous, certified, ...) and give no sign of their status.

A sentence passes when

* it, or the sentence just before or after it in the same list item or paragraph, carries a *status
  marker* (planned, not implemented, optional, off by default, opt-in, experimental, v0, simulated, test,
  and the plain negations that disclaim a capability), or
* its normalised text is in the allow-list ``data/claims_reviewed.json`` under the name of the repository
  (or under ``*`` for a sentence that is shared by several repositories). An entry means that a person read
  the line next to the code and the capability matrix and found it true as written.

Everything else is reported. Only the English README is scanned: the other seven are kept in step with it
by the README parity check, and the risk words are English identifiers in every language.

This file is shared, line by line, with the other documentation hub (HYDRA-UMC-DOCS).
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

FAMILY_PREFIXES = ("URTC",)
EXTRA_NAMES: tuple[str, ...] = ()
README = "README.md"
GLOBAL_KEY = "*"

RISK = re.compile(
    r"""e-?stop|emergency|interlock|torque|kinematic|real-?time|\bsafety\b|safe-?stop|\bsign(?:ed|ature|atures|ing)\b
    |ed25519|\bhmac|\bm?tls\b|encrypt|authenticat|\bsecur(?:e|ity)\b|fdcan|can-?fd|\byolo|ai-driven|autonomous
    |certified|industrial-grade|\bproduction(?:-ready|-grade)?\b|\blimits?\b|\bestablished\b""",
    re.IGNORECASE | re.VERBOSE,
)

MARKER = re.compile(
    r"""planned|not\ implemented|not\ yet|\bnot\b|\bno\b|\bnever\b|\bnothing\b|\bwithout\b|cannot|can't|isn't|aren't
    |doesn't|does\ not|\byet\b|unless|until|optional|off\ by\ default|opt-in|experimental|\bv0\b|simulat|\btests?\b|\btested\b
    |emulat|\bfake|stub|placeholder|future|intended|design\ goal|aspirational|hobbyist
    |\bclassic\b|\bphase\ \d|\bwould\b|\(design\)|design\ target|meant\ to|\bneither\b|\bnor\b""",
    re.IGNORECASE | re.VERBOSE,
)

_FENCE = re.compile(r"^\s*(```|~~~)")
# A section whose heading says it is about the future, the limits or the honest status describes what is NOT there.
_PLANNED_SECTION = re.compile(r"roadmap|future|planned|not (?:yet )?(?:built|implemented)|known (?:limit|gap)|limitation|honesty|what is missing", re.IGNORECASE)
_ITEM_START = re.compile(r"^\s*(?:[*+-]\s|\d+[.)]\s|\||#{1,6}\s|>\s?|<)")
_REPO_NAME = re.compile(r"\b(?:HYDRA-UMC|URTC|ELECTRO-HOBBY-3D|ARMOR)(?:-[A-Z0-9]+)+\b")
_IMG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_URL = re.compile(r"https?://\S+")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_CODE = re.compile(r"`[^`]*`")
_TAG = re.compile(r"</?[A-Za-z][^>]*>")
_SPLIT = re.compile(r"(?<=[.;!?])\s+(?=[A-Z0-9*_`(\[\"'])|\s+[—–]\s+")


def _badge_text(tag: str) -> str:
    """The words a badge shows: its alt text and the label inside its address."""
    alt = re.search(r'alt="([^"]*)"', tag)
    src = re.search(r'src="[^"]*/badge/([^"?]*)', tag)
    label = src.group(1).replace("%20", " ").replace("-", " ").replace("_", " ") if src else ""
    return " ".join(part for part in ((alt.group(1) if alt else ""), label) if part)


def clean(text: str) -> str:
    """Prose of one line: badges become their words, links their text; names, URLs and code vanish."""
    text = _IMG.sub(lambda m: " " + _badge_text(m.group(0)) + " ", text)
    text = _LINK.sub(r"\1", text)
    text = _URL.sub(" ", text)
    text = _CODE.sub(" ", text)
    text = _TAG.sub(" ", text)
    text = _REPO_NAME.sub(" ", text)
    text = text.replace("**", "").replace("__", "")
    return re.sub(r"\s+", " ", text).strip(" |-*+>#")


def key_of(sentence: str) -> str:
    normal = re.sub(r"\W+", " ", sentence.lower()).strip()
    return hashlib.sha1(normal.encode("utf-8")).hexdigest()[:12]


def units(text: str) -> list[tuple[int, list[str], bool]]:
    """(first line number, sentences, in a planned section) of every list item, table row, heading or paragraph outside code."""
    result: list[tuple[int, list[str], bool]] = []
    in_fence = False
    current: list[str] = []
    start = 0
    levels = {2: False, 3: False}

    def flush() -> None:
        nonlocal current
        if current:
            prose = clean(" ".join(current))
            sentences = [part.strip() for part in _SPLIT.split(prose) if part and part.strip()]
            if sentences:
                result.append((start, sentences, levels[2] or levels[3]))
        current = []

    for number, line in enumerate(text.splitlines(), start=1):
        if _FENCE.match(line):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not line.strip():
            flush()
            continue
        if _ITEM_START.match(line) or not current:
            flush()
            start = number
        heading = re.match(r"^(#{2,3})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            levels[level] = bool(_PLANNED_SECTION.search(heading.group(2)))
            if level == 2:
                levels[3] = False
        current.append(line)
    flush()
    return result


def findings(text: str) -> list[tuple[int, str]]:
    """(line, sentence) of every sentence with a risk word and no status marker near it."""
    found: list[tuple[int, str]] = []
    for line, sentences, planned in units(text):
        if planned:
            continue
        for index, sentence in enumerate(sentences):
            if not RISK.search(sentence):
                continue
            window = sentences[max(0, index - 1): index + 2]
            if any(MARKER.search(part) for part in window):
                continue
            found.append((line, sentence))
    return found


def load_reviewed(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {repo: dict(entries) for repo, entries in data.get("reviewed", {}).items()}


def save_reviewed(path: Path, reviewed: dict[str, dict[str, str]]) -> None:
    body = {"reviewed": {repo: dict(sorted(reviewed[repo].items())) for repo in sorted(reviewed)}}
    path.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def is_family_name(name: str) -> bool:
    return name in EXTRA_NAMES or any(name == prefix or name.startswith(prefix + "-") for prefix in FAMILY_PREFIXES)


def repositories(workspace: Path, own_name: str) -> list[Path]:
    """The sibling repositories whose README is scanned (not this hub: its README is generated)."""
    return [
        entry
        for entry in sorted(workspace.iterdir(), key=lambda p: p.name)
        if entry.is_dir() and entry.name != own_name and is_family_name(entry.name) and (entry / README).is_file()
    ]


def check_repo(repo: Path, reviewed: dict[str, dict[str, str]]) -> tuple[list[tuple[int, str]], set[str], int]:
    """(unreviewed findings, keys of the reviewed-or-flagged sentences, number of sentences with a risk word)."""
    text = (repo / README).read_text(encoding="utf-8", errors="replace")
    allowed = set(reviewed.get(repo.name, {})) | set(reviewed.get(GLOBAL_KEY, {}))
    bad: list[tuple[int, str]] = []
    seen: set[str] = set()
    for line, sentence in findings(text):
        key = key_of(sentence)
        seen.add(key)
        if key not in allowed:
            bad.append((line, sentence))
    risky_total = sum(1 for _line, sentences, _planned in units(text) for s in sentences if RISK.search(s))
    return bad, seen, risky_total


def stale_entries(repo_name: str, reviewed: dict[str, dict[str, str]], seen: set[str]) -> list[str]:
    return sorted(set(reviewed.get(repo_name, {})) - seen)


def build_reviewed(workspace: Path, own_name: str, previous: dict[str, dict[str, str]] | None = None) -> dict[str, dict[str, str]]:
    """The allow-list for the current READMEs. Sentences found in three or more repositories go under ``*``."""
    per_repo: dict[str, dict[str, str]] = {}
    for repo in repositories(workspace, own_name):
        text = (repo / README).read_text(encoding="utf-8", errors="replace")
        per_repo[repo.name] = {key_of(s): s[:110] for _line, s in findings(text)}
    counts: dict[str, int] = {}
    for entries in per_repo.values():
        for key in entries:
            counts[key] = counts.get(key, 0) + 1
    shared = {
        key: next(e[key] for e in per_repo.values() if key in e)
        for key, n in counts.items()
        if n >= 3 and not re.search(r"established", next(e[key] for e in per_repo.values() if key in e), re.IGNORECASE)
    }
    result = {repo: {k: v for k, v in entries.items() if k not in shared} for repo, entries in per_repo.items()}
    result = {repo: entries for repo, entries in result.items() if entries}
    if shared:
        result[GLOBAL_KEY] = shared
    return result

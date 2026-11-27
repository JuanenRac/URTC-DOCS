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

* it, or the sentence just before or after it in the same list item or paragraph, carries a *status marker*
  (planned, not implemented, optional, off by default, opt-in, experimental, v0, simulated, not tested, never
  run on hardware, ...), or
* it holds an *explicit negation next to a risk word*: ``not``, ``no``, ``never``, ``without``, ``n't``, ... in
  the same clause (commas, colons, brackets and the like end a clause) and at most ``NEGATION_REACH`` words
  from the risk word. A negation in a neighbouring sentence, in another clause or far from the risk word does
  not count, and neither do the words "test", "tested", "classic" or "would": "The E-STOP is certified and
  tested" and "Signed firmware, no exceptions" are reported, or
* its normalised text is in the allow-list ``data/claims_reviewed.json`` under the name of the repository
  (or under ``*`` for a sentence that is shared by several repositories). An entry means that a person read
  the line next to the code and the capability matrix and found it true as written.

A hub may also keep ``data/claims_pending.json``: the sentences that passed under the older, looser markers and
that nobody has read yet. They do not fail the check, every run says how many are left, and no command adds
to that list: it only gets shorter, and ``--update-reviewed`` moves a line out of it only for the repositories
named with ``--accept-pending``.

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

# Words that say by themselves what the state of something is. They count for the sentence that holds them and for
# the one just before and just after it.
MARKER = re.compile(
    r"""planned|not\ implemented|not\ yet|\bunimplemented|optional|off\ by\ default|disabled\ by\ default|opt-in
    |experimental|\bv0\b|simulat|emulat|\bfake|stub|placeholder|future|intended|design\ goal|aspirational|hobbyist
    |\bphase\ \d|\(design\)|design\ target|meant\ to
    |\buntested\b|\bunverified\b|\buncertified\b|\bnot\ (?:been\ )?(?:tested|verified|certified|validated|checked|measured|built|run)\b
    |\bnever\ (?:been\ )?(?:tested|verified|certified|validated|measured|built|run)\b|\bhas\ not\ (?:run|been)\b""",
    re.IGNORECASE | re.VERBOSE,
)

# An explicit negation counts only next to a risk word of its own clause (see ``negated``).
NEGATION = re.compile(r"\bnot\b|\bno\b|\bnever\b|\bnothing\b|\bnone\b|\bneither\b|\bnor\b|\bwithout\b|\bcannot\b|n't\b|n’t\b", re.IGNORECASE)
NEGATION_REACH = 6
# Phrases with a negating word that deny nothing.
_EMPTY_NEGATION = re.compile(
    r"\bnot (?:only|just|merely)\b|\bno matter\b|\b(?:with )?no exceptions?\b|\bwithout (?:exception|doubt)\b|\bnone other than\b",
    re.IGNORECASE,
)
_CLAUSE = re.compile(r"[,;:()\[\]{}|]|\s[-\u2013\u2014]+\s|\b(?:but|however|although|though|whereas)\b", re.IGNORECASE)
_WORD = re.compile(r"\S+")


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
    """(line, sentence) of every sentence with a risk word that nothing clears."""
    return [(line, sentence) for line, sentence, why in explain(text) if not why]


def _word_of(starts: list[int], position: int) -> int:
    """The index of the word that holds the character at ``position``."""
    return max((index for index, start in enumerate(starts) if start <= position), default=0)


def negated(sentence: str) -> str:
    """The negation that stands next to a risk word of the sentence, or an empty string."""
    for clause in _CLAUSE.split(_EMPTY_NEGATION.sub(" _ ", sentence)):
        starts = [match.start() for match in _WORD.finditer(clause)]
        denials = [(_word_of(starts, m.start()), m.group(0)) for m in NEGATION.finditer(clause)]
        if not denials:
            continue
        for risk in RISK.finditer(clause):
            first, last = _word_of(starts, risk.start()), _word_of(starts, risk.end() - 1)
            for index, word in denials:
                if first - NEGATION_REACH <= index <= last + NEGATION_REACH:
                    return word
    return ""


def saved_by(sentences: list[str], index: int) -> str:
    """What clears the sentence ``index`` of one unit: a status marker near it or a negation in it ('' = nothing)."""
    for part in [sentences[index], *sentences[max(0, index - 1): index], *sentences[index + 1: index + 2]]:
        marker = MARKER.search(part)
        if marker:
            return f"marker '{marker.group(0)}'"
    word = negated(sentences[index])
    return f"negation '{word}'" if word else ""


def explain(text: str) -> list[tuple[int, str, str]]:
    """(line, sentence, what cleared it) of every sentence with a risk word outside the planned sections."""
    result: list[tuple[int, str, str]] = []
    for line, sentences, planned in units(text):
        if planned:
            continue
        result += [(line, sentence, saved_by(sentences, index)) for index, sentence in enumerate(sentences) if RISK.search(sentence)]
    return result


def load_reviewed(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {repo: dict(entries) for repo, entries in data.get("reviewed", {}).items()}


def load_log(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return list(json.loads(path.read_text(encoding="utf-8")).get("log", []))


def load_pending(path: Path) -> dict[str, dict[str, str]]:
    """The lines that wait for a person's review ({} when the hub keeps none)."""
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {repo: dict(entries) for repo, entries in data.get("pending", {}).items()}


def without(pending: dict[str, dict[str, str]], reviewed: dict[str, dict[str, str]], seen: dict[str, set[str]] | None = None) -> dict[str, dict[str, str]]:
    """``pending`` less what is now reviewed and, for the repositories in ``seen``, what their README no longer says."""
    result: dict[str, dict[str, str]] = {}
    shared = set(reviewed.get(GLOBAL_KEY, {}))
    for repo, entries in pending.items():
        kept = {
            key: line for key, line in entries.items()
            if key not in shared and key not in reviewed.get(repo, {}) and (seen is None or repo not in seen or key in seen[repo])
        }
        if kept:
            result[repo] = kept
    return result


def save_pending(path: Path, pending: dict[str, dict[str, str]]) -> None:
    about = "Sentences that passed under the older markers and that no person has read next to the code yet. This list only gets shorter."
    body = {"about": about, "pending": {repo: dict(sorted(pending[repo].items())) for repo in sorted(pending)}}
    path.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def held_back(proposed: dict[str, dict[str, str]], previous: dict[str, dict[str, str]], pending: dict[str, dict[str, str]], accepted: set[str]) -> dict[str, dict[str, str]]:
    """``proposed`` without the lines that still wait for a review, except those of the names in ``accepted`` (a repository or ``*``)."""
    everywhere = {key for entries in pending.values() for key in entries}
    result: dict[str, dict[str, str]] = {}
    for name, entries in proposed.items():
        waiting = everywhere if name == GLOBAL_KEY else set(pending.get(name, {})) | set(pending.get(GLOBAL_KEY, {}))
        kept = {key: line for key, line in entries.items() if name in accepted or key not in waiting or key in previous.get(name, {})}
        if kept:
            result[name] = kept
    return result


def additions(previous: dict[str, dict[str, str]], proposed: dict[str, dict[str, str]]) -> list[tuple[str, str, str]]:
    """(repository or ``*``, key, text) of the lines of ``proposed`` that no person has accepted yet."""
    shared = set(previous.get(GLOBAL_KEY, {}))
    return [
        (repo, key, line)
        for repo in sorted(proposed)
        for key, line in sorted(proposed[repo].items())
        if key not in shared and key not in previous.get(repo, {})
    ]


def save_reviewed(path: Path, reviewed: dict[str, dict[str, str]], log: list[dict] | None = None) -> None:
    body: dict = {"reviewed": {repo: dict(sorted(reviewed[repo].items())) for repo in sorted(reviewed)}}
    entries = load_log(path) if log is None else log
    if entries:
        body["log"] = entries
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
    """The allow-list for the current READMEs. Sentences found in three or more repositories go under ``*``.

    A line that ``previous`` already holds under ``*`` stays there, however many repositories still show it."""
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
        if (n >= 3 or key in (previous or {}).get(GLOBAL_KEY, {})) and not re.search(r"established", next(e[key] for e in per_repo.values() if key in e), re.IGNORECASE)
    }
    result = {repo: {k: v for k, v in entries.items() if k not in shared} for repo, entries in per_repo.items()}
    result = {repo: entries for repo, entries in result.items() if entries}
    if shared:
        result[GLOBAL_KEY] = shared
    return result

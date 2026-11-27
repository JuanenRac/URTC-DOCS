# =============================================================================
# URTC-DOCS - src/urtc_docs/signing_facts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""What the documentation says about firmware signatures comes from the key files of URTC.

``keys/image_trust.json`` (which keys the bootloaders trust) and ``keys/registry.json`` (every key of the family)
are read from the URTC repository next to this one and kept here as ``data/signing_facts.json``. From that copy:

* the signature sentence of the safety note of the READMEs is one of a few closed phrases,
* the table "who verifies what, with which key" of ``docs/SECURITY_BASELINE.md`` is written,

and the check fails when the copy is behind URTC, when the table is not the one of the copy, when a document of
the family still says that the official trust table is empty while it holds a key, or when a document of this
repository gives the main bootloader an HMAC key without saying that it was the earlier generation.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

FACTS_NAME = "signing_facts.json"
TABLE_DOCUMENT = "docs/SECURITY_BASELINE.md"
BEGIN = "<!-- signing-table:begin (written from data/signing_facts.json; do not edit) -->"
END = "<!-- signing-table:end -->"
URTC = "URTC"

# Every key of the registry has its line here: a new key makes the generator fail until somebody says what it signs.
ROWS = {
    "urtc-release-ed25519": ("Every asset of an official release", "URTC-FLASHER, URTC-WEB-STUDIO and the publishing tool, before they trust a download"),
    "urtc-image-signing-release-current": ("The application images of official builds", "The main bootloader of an official build"),
    "urtc-image-signing-release-next": ("Nothing yet: reserved for the next image-signing key", "The main bootloader of an official build, which already trusts it"),
    "urtc-image-signing-development": ("Bench images; its seed is published, so it proves nothing about who made one", "The main bootloader of a bench build"),
    "urtc-main-bootloader-hmac-development": ("Nothing any current bootloader checks", "Only the main bootloader of the earlier generation"),
}


def from_urtc(urtc: Path) -> dict:
    trust = json.loads((urtc / "keys" / "image_trust.json").read_text(encoding="utf-8"))
    registry = json.loads((urtc / "keys" / "registry.json").read_text(encoding="utf-8"))
    flavours = trust["flavours"]
    return {
        "about": "Copied from keys/image_trust.json and keys/registry.json of URTC by check_claims.py --update-signing. Public values only.",
        "trust": {name: [{"state": key["state"], "key_id": key["key_id"]} for key in flavours.get(name, {}).get("keys", [])] for name in ("release", "dev")},
        "keys": [{"id": key["id"], "algorithm": key["algorithm"], "public": key["public"]} for key in registry["keys"]],
    }


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def variant(facts: dict) -> str:
    """Which closed phrase of the safety note is true: ``release_key``, ``development_only`` or ``unknown``."""
    trust = facts.get("trust", {})
    if trust.get("release"):
        return "release_key"
    return "development_only" if trust.get("dev") else "unknown"


def table(facts: dict) -> str:
    unknown = sorted(key["id"] for key in facts.get("keys", []) if key["id"] not in ROWS)
    if unknown:
        raise ValueError("no line for the key(s) " + ", ".join(unknown) + " (src/urtc_docs/signing_facts.py, ROWS)")
    names = {"ed25519": "Ed25519", "hmac-sha256": "HMAC-SHA256"}
    lines = ["| Key | Algorithm | Public value (start) | Signs | Checked by |", "|---|---|---|---|---|"]
    for key in facts.get("keys", []):
        signs, checked = ROWS[key["id"]]
        lines.append(f"| `{key['id']}` | {names.get(key['algorithm'], key['algorithm'])} | `{key['public'][:16]}` | {signs} | {checked} |")
    lines.append("| (no key) | SHA-256 | - | The image of the expansion slave | The slave bootloader, which also asks that the main board confirmed that exact image |")
    return "\n".join(lines)


def with_table(text: str, facts: dict) -> str:
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError("the markers of the signing table are not there exactly once")
    head, rest = text.split(BEGIN)
    tail = rest.split(END)[1]
    return f"{head}{BEGIN}\n{table(facts)}\n{END}{tail}"


# "official table ... empty" in the eight languages of the READMEs.
_OFFICIAL = re.compile(r"official|release|offiziell|officiel|ufficiale|oficial|正式|公式|官方", re.IGNORECASE)
_TABLE = re.compile(r"table|tabla|tabelle|tabella|tabela|テーブル|表", re.IGNORECASE)
_EMPTY = re.compile(r"\bempty\b|vac[ií]a|\bleer\b|\bvide\b|\bvuota\b|\bvazia\b|空", re.IGNORECASE)
_KEY = re.compile(r"key|clav|schl[üu]ssel|clé|chiav|chave|鍵|密钥|公钥", re.IGNORECASE)
_SENTENCE = re.compile(r"(?<=[.;!?])\s+|(?<=[。；！？])")


def says_the_official_table_is_empty(sentence: str) -> bool:
    return all(pattern.search(sentence) for pattern in (_OFFICIAL, _TABLE, _EMPTY, _KEY))


def gives_the_main_bootloader_an_hmac(sentence: str) -> bool:
    low = sentence.lower()
    if "hmac" not in low or "main bootloader" not in low and "main-board bootloader" not in low:
        return False
    return not re.search(r"earlier|legacy|old |no hmac|holds no|not use|no longer|any more", low)


def _documents(repo: Path) -> list[Path]:
    return sorted(repo.glob("README*.md")) + sorted(repo.glob("docs/*.md")) + sorted(repo.glob("docs/*.TXT"))


def _sentences(path: Path):
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        for sentence in _SENTENCE.split(line):
            yield number, sentence


def problems(hub: Path, repos: list[Path]) -> list[str]:
    """What is wrong. ``repos`` are the family repositories found next to the hub."""
    facts = load(hub / "data" / FACTS_NAME)
    if not facts:
        return []
    found: list[str] = []
    urtc = next((repo for repo in repos if repo.name == URTC and (repo / "keys" / "image_trust.json").is_file()), None)
    if urtc is not None and from_urtc(urtc) != facts:
        found.append(f"data/{FACTS_NAME} is not what URTC says today (run tools/check_claims.py --update-signing and make_readmes.py)")
    document = hub / TABLE_DOCUMENT
    if document.is_file():
        text = document.read_text(encoding="utf-8")
        try:
            if with_table(text, facts) != text:
                found.append(f"{TABLE_DOCUMENT}: the signing table is not the one of data/{FACTS_NAME}")
        except ValueError as error:
            found.append(f"{TABLE_DOCUMENT}: {error}")
    for repo in [hub, *repos]:
        for path in _documents(repo):
            for number, sentence in _sentences(path):
                where = f"{repo.name}/{path.relative_to(repo).as_posix()}:{number}"
                if facts["trust"].get("release") and says_the_official_table_is_empty(sentence):
                    found.append(f"{where}: says the official trust table is empty, and it holds {len(facts['trust']['release'])} key(s)")
                if repo == hub and gives_the_main_bootloader_an_hmac(sentence):
                    found.append(f"{where}: gives the main bootloader an HMAC key without saying it was the earlier generation")
    return found

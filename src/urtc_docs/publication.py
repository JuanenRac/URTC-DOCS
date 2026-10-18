# =============================================================================
# URTC-DOCS - src/urtc_docs/publication.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""What would leak if a repository of the family were published.

It reads git only (tracked files, and with history every revision, commit
authors and messages), never the ignored files, and it never prints a matched
secret: a finding shows the file, the line number and the kind, with the value
cut to its first characters.

BLOCK  something that must not go public: a private key, a public IP address,
       a personal e-mail address, a tracked secrets or .env file, the name of a
       private planning document or an internal tracking code, a commit with a
       co-author or AI trailer, a commit author other than the project's.
REVIEW a line that looks like a literal password or token, a mention of an AI
       tool or of an internal review round, or a calendar date in a document: a person
       has to look (test fixtures and documentation examples are common).

Nothing here proves the absence of a secret.
"""
from __future__ import annotations

import ipaddress
import re
import subprocess
from pathlib import Path

from .family import is_family_name

Finding = tuple[str, str, str, str]   # (BLOCK or REVIEW, repository, where, what)

FIXTURE_PATH = re.compile(r"(^|/)(tests?|conformance|fixtures)/|(^|/)test_[^/]*$")
ALLOWED_AUTHORS = {
    "JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>",
    "Electro Hobby 3D <electrohobby3d@gmail.com>",
}
PUBLIC_EMAILS = {"electrohobby3d@gmail.com"}   # the project's own public address

# Written in pieces so that this very file is never flagged by the check it implements.
PRIVATE_MARKERS = ("SON" + "NET", "BIB" + "LIA")
PRIVATE_PHRASES = ("private development" + " plan", "internal work" + " log", "plan de desarrollo" + " privado")
AI_ASSISTANT = "cla" + "ude"   # the assistant that must never be named in a commit
AI_NAMES = (AI_ASSISTANT, "anthro" + "pic")
TRACKING_CODE = re.compile(
    r"(V07-[0-9]{3}|REV-[0-9]{3}|PROM-[A-Z]+-[A-Z]?[0-9]+|(DOC|CODE)-BUG-[0-9]+|\[\[(project|feedback|reference|user)_[a-z0-9_]+\]\])"
)
REVIEW_WORD = "aud" + "it"   # written in pieces: this file is read by the check it implements
REVIEW_ROUND = re.compile(r"(?i)\b" + REVIEW_WORD + r"(?:s|ed)?\s+(?:round|pass|finding|id|code)\b|\bronda\s+de\s+" + REVIEW_WORD + "or")
ISO_DATE = re.compile(r"\b20\d\d-[01]\d-[0-3]\d\b")

PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@(?:gmail|hotmail|outlook|yahoo|icloud|proton(?:mail)?)\.[a-z]{2,}\b", re.I)
IPV4 = re.compile(r"(?<![\d.])(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?![\d.])")
LITERAL = re.compile(r"""(?ix)\b(pass(?:word|wd)?|secret|token|api[_-]?key|psk)\b["']?\s*[:=]\s*["']([^"'\s$`{}<>()]{8,})["']""")
BAD_PATH = re.compile(r"(^|/)(secrets/(?!.*example)|\.env$|.*\.env$|.*\.pem$|.*\.key$|id_[a-z0-9]+$)", re.I)
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".pdf", ".zip", ".gz", ".bin", ".hex", ".elf", ".woff", ".woff2", ".ttf",
    ".jar", ".apk", ".stl", ".step", ".fcstd", ".glb", ".hef", ".onnx", ".lock", ".svg",
}
# addresses that are public but say nothing about anyone: well-known resolvers and the boundary values that tests of private ranges use
BENIGN_IPS = {
    "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "9.9.9.9", "1.2.3.4", "8.8.8.0", "8.0.0.1", "11.0.0.1",
    "172.15.0.1", "172.32.0.1", "192.169.0.1", "172.15.255.255", "172.32.0.0", "172.15.0.0", "1.0.0.0",
}
# words that make a "literal" obviously not a secret
HARMLESS = re.compile(r"(?i)(example|placeholder|changeme|change-me|your[-_ ]|xxxx|\*{4}|test|fake|dummy|sample|correct-horse|adminpass|secret-for|0000|1111|aaaa|\.\.\.)")


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo.name}: {result.stderr.strip()[:200]}")
    return result.stdout


def public_ip(text: str) -> bool:
    try:
        address = ipaddress.ip_address(text)
    except ValueError:
        return False
    return address.is_global and not address.is_multicast and not text.startswith(("0.", "255."))


def scan_text(name: str, where: str, text: str, findings: list[Finding], *, document: bool = False, fixture: bool = False) -> None:
    """Scan the lines of one text.

    `document` is true for Markdown and plain-text files (where a date is a finding). `fixture` is true for test
    and conformance files, where a key header or an address is data made up for the test: it is then only a
    thing to review, never a block.
    """
    kind_of_fixture = "REVIEW" if fixture else "BLOCK"
    suffix = " (in a test fixture)" if fixture else ""
    for number, line in enumerate(text.splitlines(), 1):
        if len(line) > 2000:
            continue
        ref = f"{where}:{number}"
        if PRIVATE_KEY.search(line):
            findings.append((kind_of_fixture, name, ref, "private key" + suffix))
        for match in EMAIL.finditer(line):
            if match.group(0).lower() not in PUBLIC_EMAILS:
                findings.append(("BLOCK", name, ref, f"personal e-mail {match.group(0)[:4]}..."))
        for match in IPV4.finditer(line):
            candidate = match.group(1)
            around = line[max(0, match.start() - 12):match.end() + 1]
            if (
                all(0 <= int(part) <= 255 for part in candidate.split("."))
                and candidate not in BENIGN_IPS
                and public_ip(candidate)
                and not re.search(r"(?i)version|v\d+\.\d+\.\d+\.\d+|\d+\.\d+\.\d+\.\d+-", around)
            ):
                octets = [int(part) for part in candidate.split(".")]
                looks_like_a_version = octets[0] <= 9 and max(octets[1:]) <= 99
                if looks_like_a_version:
                    findings.append(("REVIEW", name, ref, "four numbers that may be a version or an address"))
                else:
                    findings.append((kind_of_fixture, name, ref, f"public IP address {candidate.split('.')[0]}.x.x.x" + suffix))
        for match in LITERAL.finditer(line):
            value = match.group(2)
            if not HARMLESS.search(value) and not HARMLESS.search(line) and len(set(value)) > 3:
                findings.append(("REVIEW", name, ref, f"literal {match.group(1).lower()} {value[:3]}..."))
        for marker in PRIVATE_MARKERS:
            if marker in line:
                findings.append(("BLOCK", name, ref, "the name of a private document"))
        lowered = line.lower()
        for phrase in PRIVATE_PHRASES:
            if phrase in lowered:
                findings.append(("BLOCK", name, ref, "a reference to private planning material"))
        if TRACKING_CODE.search(line):
            findings.append(("BLOCK", name, ref, "an internal tracking code"))
        if any(ai in lowered for ai in AI_NAMES):
            findings.append(("REVIEW", name, ref, "mentions an AI tool"))
        if REVIEW_ROUND.search(line):
            findings.append(("REVIEW", name, ref, "mentions an internal review round"))
        if document and ISO_DATE.search(line):
            findings.append(("REVIEW", name, ref, "a calendar date in a document"))


def check_commits(repo: Path, ref: str | None, findings: list[Finding]) -> None:
    log = git(repo, "log", ref or "--all", "--format=%H%x1f%an <%ae>%x1f%cn <%ce>%x1f%B%x1e")
    for record in [r for r in log.split("\x1e") if r.strip()]:
        parts = record.strip("\n").split("\x1f", 3)
        if len(parts) < 4:
            continue
        sha, author, committer, message = parts[0][:10], parts[1], parts[2], parts[3]
        if author not in ALLOWED_AUTHORS or committer not in ALLOWED_AUTHORS:
            findings.append(("BLOCK", repo.name, f"commit {sha}", f"author or committer is not the project's ({author.split('<')[0].strip()})"))
        lowered = message.lower()
        if re.search(r"(?im)^(co-authored-by|generated with|signed-off-by)\b", message) or AI_ASSISTANT in lowered:
            findings.append(("BLOCK", repo.name, f"commit {sha}", "the message has a co-author, AI or sign-off trailer"))
        elif any(ai in lowered for ai in AI_NAMES):
            # the name of an AI provider is often legitimate in a technical message (an environment variable, a client class)
            findings.append(("REVIEW", repo.name, f"commit {sha}", "the message mentions an AI tool"))
        if any(marker in message for marker in PRIVATE_MARKERS):
            findings.append(("BLOCK", repo.name, f"commit {sha}", "the message names a private document"))


def check_history(repo: Path, ref: str | None, findings: list[Finding]) -> None:
    """Paths that were once tracked, and lines that were committed and later removed (they are still public)."""
    name = repo.name
    seen: set[tuple[str, str]] = set()
    for revision in git(repo, "rev-list", ref or "--all").split():
        for path in git(repo, "ls-tree", "-r", "--name-only", revision).splitlines():
            if BAD_PATH.search(path) and ("path", path) not in seen:
                seen.add(("path", path))
                findings.append(("BLOCK", name, f"{path} @ {revision[:10]}", "a secrets, key or environment file was tracked in the history"))
    diff = git(repo, "log", ref or "--all", "-p", "--no-color", "-M", "--diff-filter=MDR", "--unified=0", "--format=commit %h", check=False)
    current = current_path = ""
    for line in diff.splitlines():
        if line.startswith("commit "):
            current = line[7:]
        elif line.startswith("--- "):
            current_path = line[4:].removeprefix("a/")
        elif line.startswith("-") and not line.startswith("---"):
            extra: list[Finding] = []
            scan_text(name, f"history {current}", line[1:], extra)
            for item in extra:
                if item[0] != "BLOCK":
                    continue
                if item[3].startswith("public IP address") and FIXTURE_PATH.search(current_path):
                    continue
                key = (item[2], item[3])
                if key not in seen:
                    seen.add(key)
                    findings.append((item[0], item[1], item[2].rsplit(":", 1)[0] + " (a removed line)", item[3]))


def check_repo(repo: Path, history: bool = False, ref: str | None = None) -> list[Finding]:
    name = repo.name
    findings: list[Finding] = []
    for path in [p for p in git(repo, "ls-files").splitlines() if p]:
        if BAD_PATH.search(path):
            findings.append(("BLOCK", name, path, "a secrets, key or environment file is tracked"))
        suffix = Path(path).suffix.lower()
        if suffix in BINARY_SUFFIXES or path.startswith(("node_modules/", "vendor/")) or path.endswith(("package-lock.json", "LICENSE")):
            continue
        try:
            text = (repo / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        scan_text(name, path, text, findings, document=suffix in {".md", ".txt"}, fixture=bool(FIXTURE_PATH.search(path)))
    check_commits(repo, ref, findings)
    if history:
        check_history(repo, ref, findings)
    return findings


def family_repos(workspace: Path) -> list[Path]:
    return sorted((p for p in workspace.iterdir() if p.is_dir() and is_family_name(p.name) and (p / ".git").exists()), key=lambda p: p.name)


def summarize(findings: list[Finding]) -> tuple[int, int]:
    return sum(1 for f in findings if f[0] == "BLOCK"), sum(1 for f in findings if f[0] == "REVIEW")

# =============================================================================
# URTC-DOCS - src/urtc_docs/count_tests.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Count the tests of every family repository without running them and compare with data/glance.json.

Python suites are COLLECTED (the same tests the runner would run). A suite that needs a toolchain that is not
installed (a C compiler, npm) is reported as ``unknown`` with the reason, never as zero and never as a failure.
Only an exactly counted repository can disagree with the data file.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# repository -> how its documented number is counted. "pytest" runs from the repository root unless a folder is given.
# A string that starts with "unknown:" is the reason why the count cannot be taken here.
PYTEST_FOLDER = {"URTC-VISION-TOOL": "src/vision_companion"}
UNITTEST = {"URTC-DEVTOOLS": "tests"}
UNKNOWN = {
    "URTC": "unknown: the documented number adds host-native C assertions that need a C compiler",
    "URTC-SMART-RACK": "unknown: the documented number adds host-native C assertions that need a C compiler",
    "URTC-WEB-STUDIO": "unknown: the suite is run by npm (vitest) and is not collected here",
}
TIMEOUT_SECONDS = 600
UNITTEST_SNIPPET = (
    "import sys, unittest\n"
    "sys.path.insert(0, '.')\n"
    "suite = unittest.TestLoader().discover(sys.argv[1])\n"
    "def flat(node):\n"
    "    for item in node:\n"
    "        if isinstance(item, unittest.TestSuite):\n"
    "            yield from flat(item)\n"
    "        else:\n"
    "            yield item\n"
    "found = list(flat(suite))\n"
    "print('COUNT=%d FAILED=%d' % (len(found), sum(type(t).__name__ == '_FailedTest' for t in found)))\n"
)
PYTEST_TOTAL = re.compile(r"(\d+) tests? collected")
UNITTEST_TOTAL = re.compile(r"COUNT=(\d+) FAILED=(\d+)")


class CountError(ValueError):
    """The data file is unreadable or a count could not be taken."""


@dataclass(frozen=True)
class Result:
    repo: str
    documented: int | None
    counted: int | None
    note: str = ""

    @property
    def exact(self) -> bool:
        return self.counted is not None

    @property
    def agrees(self) -> bool:
        return self.counted is None or self.documented == self.counted


def parse_pytest(output: str) -> int | None:
    """The number in pytest's 'N tests collected' line, or None when there is none or collection had errors."""
    if re.search(r"\d+ errors? in ", output):
        return None
    match = PYTEST_TOTAL.search(output)
    return int(match.group(1)) if match else None


def parse_unittest(output: str) -> int | None:
    match = UNITTEST_TOTAL.search(output)
    if not match or int(match.group(2)):
        return None
    return int(match.group(1))


def load_documented(path: Path) -> dict[str, int | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        repos = data["repos"]
        return {name: (entry.get("tests") or {}).get("count") for name, entry in repos.items()}
    except (OSError, ValueError, KeyError, AttributeError, TypeError) as error:
        raise CountError(f"cannot read {path}: {error}") from error


def _run(command: list[str], cwd: Path, extra_path: str | None = None) -> str:
    env = dict(os.environ)
    if extra_path:
        env["PYTHONPATH"] = extra_path
    try:
        done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise CountError(f"{' '.join(command[:4])}: {error}") from error
    return (done.stdout or "") + (done.stderr or "")


def count_repo(repo: Path) -> tuple[int | None, str]:
    """(count, note) for one repository; count is None when it cannot be taken exactly."""
    name = repo.name
    if name in UNKNOWN:
        return None, UNKNOWN[name]
    if name in UNITTEST:
        counted = parse_unittest(_run([sys.executable, "-c", UNITTEST_SNIPPET, UNITTEST[name]], repo))
        return (counted, "") if counted is not None else (None, "unknown: unittest discovery failed")
    folder = repo / PYTEST_FOLDER.get(name, ".")
    if not folder.is_dir():
        return None, "unknown: the test folder is missing"
    counted = parse_pytest(_run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"], folder, str(folder)))
    return (counted, "") if counted is not None else (None, "unknown: pytest could not collect (missing dependencies?)")


def compare(workspace: Path, data: Path, names: list[str] | None = None) -> list[Result]:
    documented = load_documented(data)
    results: list[Result] = []
    for name in sorted(names or documented):
        if name not in documented:
            raise CountError(f"{name} is not in {data.name}")
        repo = workspace / name
        if not repo.is_dir():
            results.append(Result(name, documented[name], None, "unknown: the repository is not next to this one"))
            continue
        if documented[name] is None:
            results.append(Result(name, None, None, "no tests documented"))
            continue
        counted, note = count_repo(repo)
        results.append(Result(name, documented[name], counted, note))
    return results


def apply_counts(data: Path, results: list[Result]) -> list[str]:
    """Write the exact counts into the data file (two-space JSON, the same layout); return the names changed."""
    text = data.read_text(encoding="utf-8")
    loaded = json.loads(text)
    changed: list[str] = []
    for result in results:
        if result.exact and result.documented != result.counted:
            loaded["repos"][result.repo]["tests"]["count"] = result.counted
            changed.append(result.repo)
    if changed:
        newline = "\r\n" if "\r\n" in text else "\n"
        data.write_text(json.dumps(loaded, indent=2, ensure_ascii=False).replace("\n", newline) + newline, encoding="utf-8", newline="")
    return changed

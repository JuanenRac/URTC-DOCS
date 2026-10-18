# =============================================================================
# URTC-DOCS - src/urtc_docs/cli.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The command-line entry points behind the scripts of tools/ and behind run.sh / run.bat."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, brand, catalog, family, publication, readmes

REPO = Path(__file__).resolve().parents[2]
CATALOG_FILE = REPO / "docs" / "PROJECT_CATALOG.md"


def _workspace(args: argparse.Namespace) -> Path:
    return Path(args.workspace).resolve() if args.workspace else family.workspace_of(REPO)


def make_catalog(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="make_catalog.py", description="Write docs/PROJECT_CATALOG.md from the manifests of the repositories next to this one.")
    parser.add_argument("--check", action="store_true", help="fail when the table is out of date (versions and maturity included)")
    parser.add_argument("--check-structure", action="store_true", help="fail only when the set of repositories or their kind changed (versions and maturity are ignored)")
    parser.add_argument("--require-siblings", action="store_true", help="fail instead of skipping when no sibling repository is found")
    parser.add_argument("--workspace", help="the folder that holds the repositories (default: the parent of this repository)")
    parser.add_argument("--catalog", default=str(CATALOG_FILE), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    workspace = _workspace(args)
    manifests = [m for m in family.load_manifests(workspace)]
    if len(manifests) < 2:
        message = f"no repository of the ecosystem was found in {workspace}"
        if args.require_siblings:
            print(f"CATALOG=FAIL {message}", file=sys.stderr)
            return 1
        print(f"CATALOG=SKIP {message}")
        return 0
    path = Path(args.catalog)
    problems = catalog.missing_descriptions(manifests)
    if problems:
        print("repositories without a curated description: " + ", ".join(problems), file=sys.stderr)
    if args.check or args.check_structure:
        ok, message = catalog.check_file(path, manifests, structure_only=args.check_structure and not args.check)
        if args.check_structure and problems:
            ok, message = False, message + "; add the missing descriptions to src/urtc_docs/descriptions.py"
        print(f"CATALOG={'PASS' if ok else 'FAIL'} {message} ({len(manifests)} repositories)", file=None if ok else sys.stderr)
        return 0 if ok else 1
    current = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    new = catalog.render(current, manifests)
    if new != current:
        path.write_text(new, encoding="utf-8", newline="\n")
    print(f"CATALOG=WRITTEN {len(manifests)} repositories" if new != current else f"CATALOG=PASS already current ({len(manifests)} repositories)")
    return 0


def make_brand(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="make_brand.py", description="Write the banner, the icon and the map of the families.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    stale = []
    for relative, content in brand.outputs().items():
        target = REPO / relative
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == content:
            continue
        stale.append(relative)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
    if args.check and stale:
        print("BRAND=FAIL out of date: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"BRAND={'PASS' if args.check else 'WRITTEN'} {len(brand.outputs())} files")
    return 0


def make_readmes(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="make_readmes.py", description="Write README.md and its seven translations from tools/readme_src.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    stale = []
    for name, content in readmes.outputs(REPO).items():
        target = REPO / name
        current = target.read_text(encoding="utf-8").replace("\r\n", "\n") if target.is_file() else None
        if current == content:
            continue
        stale.append(name)
        if not args.check:
            target.write_text(content, encoding="utf-8", newline="\n")
    if args.check and stale:
        print("READMES=FAIL out of date: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"READMES={'PASS' if args.check else 'WRITTEN'} {len(readmes.LANGUAGES)} languages")
    return 0


def publication_check(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="publication_check.py", description="Look for anything private in the repositories of the ecosystem before a publication.")
    parser.add_argument("repositories", nargs="*", help="names of the repositories to check (default: every one of the ecosystem next to this one)")
    parser.add_argument("--history", action="store_true", help="also scan every revision for removed lines and once-tracked secret files (slow)")
    parser.add_argument("--no-history", action="store_true", help="accepted for compatibility: the history scan is off unless --history is given")
    parser.add_argument("--ref", help="only the history that this branch reaches")
    parser.add_argument("--workspace", help="the folder that holds the repositories")
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).resolve() if args.workspace else family.workspace_of(REPO)
    repos = [workspace / name for name in args.repositories] if args.repositories else publication.family_repos(workspace)
    if not repos:
        print("PUBLICATION_CHECK=SKIP no repository was found")
        return 0
    blocked = 0
    for repo in repos:
        findings = publication.check_repo(repo, history=args.history and not args.no_history, ref=args.ref)
        block, review = publication.summarize(findings)
        blocked += block
        print(f"{repo.name:34} BLOCK {block:3}  REVIEW {review:3}")
        for kind, _name, where, what in findings[:40]:
            print(f"   {kind:6} {where}  {what}")
        if len(findings) > 40:
            print(f"   ... and {len(findings) - 40} more")
    print("PUBLICATION_CHECK=" + ("FAIL" if blocked else "PASS"))
    return 1 if blocked else 0


def main(argv: list[str] | None = None) -> int:
    """`run.sh` / `run.bat`: without arguments, say what this is; with one, run that tool."""
    commands = {"catalog": make_catalog, "brand": make_brand, "readmes": make_readmes, "publication": publication_check}
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments[0] in {"-h", "--help", "help"}:
        print(f"URTC-DOCS v{__version__}")
        print("Documentation and cross-repository tooling hub of the URTC ecosystem.")
        print("usage: run.sh <catalog|brand|readmes|publication> [options]")
        return 0
    if arguments[0] not in commands:
        print(f"unknown command {arguments[0]!r}; expected one of: {', '.join(commands)}", file=sys.stderr)
        return 2
    return commands[arguments[0]](arguments[1:])


if __name__ == "__main__":
    raise SystemExit(main())

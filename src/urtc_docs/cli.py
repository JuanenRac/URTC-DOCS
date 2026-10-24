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

from . import __version__, brand, catalog, claims, doctor as doctor_module, drift, family, glance, publication, readmes, status

REPO = Path(__file__).resolve().parents[2]
CATALOG_FILE = REPO / "docs" / "PROJECT_CATALOG.md"
GLANCE_FILE = REPO / "data" / "glance.json"
CLAIMS_FILE = REPO / "data" / "claims_reviewed.json"
OWN_NAME = "URTC-DOCS"


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


def make_glance(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="make_glance.py", description="Write or check the 'At a glance' section of the eight READMEs of the repositories next to this one, and check that each has its 'Project status' table.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="insert the section where it is missing and rewrite it where it is stale")
    mode.add_argument("--check", action="store_true", help="fail when a section is missing, misplaced or stale (the default)")
    parser.add_argument("--repo", action="append", metavar="NAME", help="only this repository (repeat the option for several)")
    parser.add_argument("--require-siblings", action="store_true", help="fail instead of skipping a listed repository that is not next to this one")
    parser.add_argument("--workspace", help="the folder that holds the repositories (default: the parent of this repository)")
    parser.add_argument("--data", default=str(GLANCE_FILE), help="the data file (default: data/glance.json)")
    args = parser.parse_args(argv)
    try:
        entries = glance.load_data(Path(args.data))
        workspace = _workspace(args)
        names = args.repo or sorted(entries)
        unknown = [name for name in names if name not in entries]
        if unknown:
            print("GLANCE=FAIL not in the data file: " + ", ".join(unknown), file=sys.stderr)
            return 1
        problems: list[str] = []
        done = skipped = 0
        for name in names:
            repo = workspace / name
            if not repo.is_dir():
                skipped += 1
                if args.require_siblings:
                    problems.append(f"{name}: the repository is not next to this one")
                continue
            if args.apply:
                for changed in glance.apply_repo(repo, entries[name]):
                    print(f"WRITTEN {name}/{changed}")
            problems += glance.check_repo(repo, entries[name]) + status.check_repo(repo)
            done += 1
    except (glance.GlanceError, OSError, ValueError) as error:
        print(f"GLANCE=FAIL {error}", file=sys.stderr)
        return 1
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"GLANCE=FAIL {len(problems)} problem(s) in {done} repositories", file=sys.stderr)
        return 1
    print(f"GLANCE=PASS {done} repositories checked, {skipped} not found next to this one")
    return 0


def check_claims(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_claims.py", description="Fail when a README states a risky capability (E-STOP, interlock, signed, mTLS, ...) without a status marker or a reviewed line.")
    parser.add_argument("--repo", action="append", metavar="NAME", help="only this repository (repeat the option for several)")
    parser.add_argument("--require-siblings", action="store_true", help="fail instead of skipping when no sibling repository is found")
    parser.add_argument("--workspace", help="the folder that holds the repositories (default: the parent of this repository)")
    parser.add_argument("--data", default=str(CLAIMS_FILE), help="the reviewed list (default: data/claims_reviewed.json)")
    parser.add_argument("--update-reviewed", action="store_true", help="rewrite the reviewed list from the READMEs as they are now; read every line it adds first")
    parser.add_argument("--strict-stale", action="store_true", help="also fail when the reviewed list holds a line that no README has any more")
    args = parser.parse_args(argv)
    workspace = _workspace(args)
    repos = claims.repositories(workspace, OWN_NAME)
    if args.repo:
        repos = [repo for repo in repos if repo.name in set(args.repo)]
    if not repos:
        message = f"no repository of the family was found in {workspace}"
        if args.require_siblings:
            print(f"CLAIMS=FAIL {message}", file=sys.stderr)
            return 1
        print(f"CLAIMS=SKIP {message}")
        return 0
    data = Path(args.data)
    if args.update_reviewed:
        reviewed = claims.build_reviewed(workspace, OWN_NAME)
        claims.save_reviewed(data, reviewed)
        total = sum(len(entries) for entries in reviewed.values())
        print(f"CLAIMS=WRITTEN {total} reviewed lines in {data.name}")
        return 0
    reviewed = claims.load_reviewed(data)
    bad_total = risky_total = 0
    stale: list[str] = []
    problems: list[str] = []
    for repo in repos:
        bad, seen, risky = claims.check_repo(repo, reviewed)
        risky_total += risky
        bad_total += len(bad)
        for line, sentence in bad:
            problems.append(f"{repo.name}/README.md:{line}: {sentence[:200]}")
        if not args.repo:
            stale += [f"{repo.name}:{key}" for key in claims.stale_entries(repo.name, reviewed, seen)]
    for problem in problems:
        print(problem, file=sys.stderr)
    if stale:
        print(f"note: {len(stale)} reviewed line(s) no longer match any README (remove them with --update-reviewed)")
    if bad_total or (stale and args.strict_stale):
        print(f"CLAIMS=FAIL {bad_total} sentence(s) with a risk word and no status marker, {len(stale)} stale, in {len(repos)} repositories", file=sys.stderr)
        return 1
    print(f"CLAIMS=PASS {risky_total} sentences with a risk word in {len(repos)} repositories, all marked or reviewed")
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


def check_repo_tools(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_repo_tools.py", description="Fail when a file that every repository carries as the same copy (the documentation-policy and README-parity checks, the manifest version bumper) differs between repositories.")
    parser.add_argument("--require-siblings", action="store_true", help="fail instead of skipping when fewer than two repositories are found")
    parser.add_argument("--workspace", help="the folder that holds the repositories (default: the parent of this repository)")
    args = parser.parse_args(argv)
    workspace = _workspace(args)
    found, count = drift.check_workspace(workspace, template_dir=drift.TEMPLATE_DIR if workspace.resolve() == REPO.resolve().parent else None)
    if count < 2:
        message = f"fewer than two repositories of the ecosystem were found in {workspace}"
        if args.require_siblings:
            print(f"REPO_TOOLS=FAIL {message}", file=sys.stderr)
            return 1
        print(f"REPO_TOOLS=SKIP {message}")
        return 0
    for item in found:
        print(f"{item.repository}/{item.file}: {item.detail}", file=sys.stderr)
    if found:
        print(f"REPO_TOOLS=FAIL {len(found)} copy(ies) differ from the others ({count} repositories, {len(drift.SHARED_FILES)} shared files)", file=sys.stderr)
        return 1
    print(f"REPO_TOOLS=PASS {len(drift.SHARED_FILES)} shared files are the same in {count} repositories")
    return 0


def sync_repo_tools(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sync_repo_tools.py", description="Put the canonical copy of every shared file (template/eh3d-repo-template) into the repositories next to this one. Without --apply it only lists what would change.")
    parser.add_argument("--apply", action="store_true", help="write the files (the line endings of each copy are kept)")
    parser.add_argument("--workspace", help="the folder that holds the repositories (default: the parent of this repository)")
    args = parser.parse_args(argv)
    workspace = _workspace(args)
    items = drift.plan_sync(workspace, template_dir=drift.TEMPLATE_DIR)
    for item in items:
        print(f"{item.repository}/{item.file}: {'written' if args.apply else 'would be written'}")
    if args.apply:
        drift.apply_sync(items)
        print(f"SYNC_REPO_TOOLS=DONE {len(items)} file(s) written")
        return 0
    if items:
        print(f"SYNC_REPO_TOOLS=DIFFERENT {len(items)} file(s) differ from the template (run with --apply)")
        return 1
    print("SYNC_REPO_TOOLS=PASS every shared file is the template")
    return 0


def doctor(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="urtc_doctor.py", description="One report on this machine and on the repositories next to this one: tools, versions, shared copies, bundled firmware and the checks of every repository.")
    parser.add_argument("--workspace", help="the folder that holds the repositories (default: the parent of this repository)")
    parser.add_argument("--fast", action="store_true", help="leave out the checks that start the validation of each repository")
    parser.add_argument("--online", action="store_true", help="also compare the bundled firmware with the newest release on GitHub")
    args = parser.parse_args(argv)
    lines = doctor_module.run_doctor(REPO, _workspace(args), online=args.online, fast=args.fast)
    text, status = doctor_module.render(lines)
    print(text)
    return status


def main(argv: list[str] | None = None) -> int:
    """`run.sh` / `run.bat`: without arguments, say what this is; with one, run that tool."""
    commands = {"catalog": make_catalog, "brand": make_brand, "readmes": make_readmes, "glance": make_glance, "claims": check_claims, "repo-tools": check_repo_tools, "sync-repo-tools": sync_repo_tools, "publication": publication_check, "doctor": doctor}
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments[0] in {"-h", "--help", "help"}:
        print(f"URTC-DOCS v{__version__}")
        print("Documentation and cross-repository tooling hub of the URTC ecosystem.")
        print("usage: run.sh <catalog|brand|readmes|glance|claims|repo-tools|publication|doctor> [options]")
        return 0
    if arguments[0] not in commands:
        print(f"unknown command {arguments[0]!r}; expected one of: {', '.join(commands)}", file=sys.stderr)
        return 2
    return commands[arguments[0]](arguments[1:])


if __name__ == "__main__":
    raise SystemExit(main())

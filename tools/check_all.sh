#!/usr/bin/env bash
# =============================================================================
# URTC-DOCS - tools/check_all.sh
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
# Runs the own CI validation (tools/ci_validate.py) of every repository of the ecosystem that sits next
# to this one, and the checks of this repository, and prints one PASS, FAIL or SKIP line each.
#
#   tools/check_all.sh            # every repository next to this one, then the checks of this one
#   tools/check_all.sh --sync     # also the shared-check sync scripts of HYDRA-UMC-SDK in --check mode, when that repository is next to this one
#
# A check that cannot run here (no python, no tools/ci_validate.py in that repository, no sibling
# repository at all) is reported as SKIP with the reason, never as PASS. The exit status is non-zero
# when any check FAILS, and also when nothing at all could be checked.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SYNC=0
for argument in "$@"; do
  [[ "$argument" == "--sync" ]] && SYNC=1
done

PYTHON="${URTC_PYTHON:-$(command -v python3 || command -v python || true)}"
LOGS="$(mktemp -d)"
trap 'rm -rf -- "$LOGS"' EXIT
FAILED=0
PASSED=0
SKIPPED=0

# report NAME STATUS DETAIL
report() {
  printf '%-34s %-5s %s\n' "$1" "$2" "$3"
  case "$2" in
    FAIL) FAILED=$((FAILED + 1)) ;;
    PASS) PASSED=$((PASSED + 1)) ;;
    SKIP) SKIPPED=$((SKIPPED + 1)) ;;
  esac
  return 0
}

# run NAME DIRECTORY COMMAND... : runs in the directory (a subshell) and captures the output.
run() {
  local name="$1" directory="$2"
  shift 2
  if ( cd "$directory" && "$@" ) >"$LOGS/$name.log" 2>&1; then
    report "$name" PASS "$(grep -E '(CI_VALIDATION=PASS|[0-9]+ passed|CATALOG=PASS|BRAND=PASS|READMES=PASS|GLANCE=PASS|CLAIMS=PASS|PUBLICATION_CHECK=PASS)' "$LOGS/$name.log" | tail -1 | sed 's/^ *//')"
  else
    report "$name" FAIL "see below"
    sed 's/^/    | /' "$LOGS/$name.log" | tail -15
  fi
}

if [[ -z "$PYTHON" ]]; then
  report "everything" SKIP "python is not installed"
  echo
  echo "URTC_CHECK_ALL=FAIL nothing could be checked"
  exit 1
fi

# 1. the repositories of the ecosystem: each one's own CI validation
checked=0
for directory in "$ROOT"/URTC "$ROOT"/URTC-*; do
  [[ -d "$directory" ]] || continue
  name="$(basename "$directory")"
  [[ -f "$directory/urtc.project.json" ]] || continue
  [[ "$name" == "URTC-DOCS" ]] && continue   # the checks of this repository come last
  if [[ ! -f "$directory/tools/ci_validate.py" ]]; then
    report "$name" SKIP "no tools/ci_validate.py"
    continue
  fi
  if [[ ! -d "$directory/.git" ]]; then
    report "$name" SKIP "not a git checkout (the documentation boundary check reads git)"
    continue
  fi
  checked=$((checked + 1))
  run "$name" "$directory" "$PYTHON" tools/ci_validate.py
done
if [[ "$checked" -eq 0 ]]; then
  report "family" SKIP "no repository of the ecosystem was found next to this one"
fi

# 2. this repository: its own validation, the generated documents and the unit tests
run "URTC-DOCS" "$HERE" "$PYTHON" tools/ci_validate.py
run "docs: readmes" "$HERE" "$PYTHON" tools/make_readmes.py --check
run "docs: brand" "$HERE" "$PYTHON" tools/make_brand.py --check
if [[ "$checked" -gt 0 ]]; then
  run "docs: catalogue structure" "$HERE" "$PYTHON" tools/make_catalog.py --check-structure --require-siblings
else
  report "docs: catalogue structure" SKIP "no sibling repositories to read the manifests of"
fi
if [[ "$checked" -gt 0 ]]; then
  run "docs: At a glance tables" "$HERE" "$PYTHON" tools/make_glance.py --check
else
  report "docs: At a glance tables" SKIP "no sibling repositories to read the manifests of"
fi
if [[ "$checked" -gt 0 ]]; then
  run "docs: claim hygiene" "$HERE" "$PYTHON" tools/check_claims.py --require-siblings
else
  report "docs: claim hygiene" SKIP "no sibling repositories to read the READMEs of"
fi
if "$PYTHON" -c "import pytest" >/dev/null 2>&1; then
  run "docs: unit tests" "$HERE" "$PYTHON" -m pytest tests -q
else
  report "docs: unit tests" SKIP "pytest is not installed"
fi

# 3. optional: the sync scripts of HYDRA-UMC-SDK, which keep the shared checks identical everywhere
if [[ "$SYNC" -eq 1 ]]; then
  if [[ -d "$ROOT/HYDRA-UMC-SDK/tools" ]]; then
    for script in sync_doc_policy sync_readme_parity sync_version_tools; do
      run "sdk: $script" "$ROOT/HYDRA-UMC-SDK" "$PYTHON" "tools/$script.py" --check
    done
  else
    report "sdk: sync scripts" SKIP "HYDRA-UMC-SDK is not next to this repository"
  fi
fi

echo
echo "passed $PASSED, failed $FAILED, skipped $SKIPPED"
if [[ "$FAILED" -eq 0 ]]; then
  echo "URTC_CHECK_ALL=PASS"
else
  echo "URTC_CHECK_ALL=FAIL"
  exit 1
fi

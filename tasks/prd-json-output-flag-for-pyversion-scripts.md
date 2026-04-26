[PRD]
# PRD: JSON Output Flag for pyversion Scripts

## Overview

Add a `--json` flag to both `pyversion.py` and `pyversion.sh` so that users can request structured JSON output instead of the default human-readable text. This enables scripting, piping into tools like `jq`, and programmatic consumption by other tools without fragile text parsing.

## Goals

- Add a `--json` flag to `pyversion.py` that emits structured JSON
- Add a `--json` flag to `pyversion.sh` that emits structured JSON
- JSON output includes version string + major/minor/patch as separate fields + OS info
- Default (no flag) behavior remains unchanged

## Quality Gates

These commands must pass for every user story:

- `python -m pytest test_pyversion.py` — existing and new unit tests
- `bash -n pyversion.sh` — shell script syntax check

No browser verification needed (CLI tool only).

## User Stories

### US-001: Add --json flag to pyversion.py

**Description:** As a developer, I want to run `pyversion.py --json` so that I get structured JSON output I can pipe into other tools.

**Acceptance Criteria:**

- [ ] `python pyversion.py --json` exits with code 0
- [ ] Output is valid JSON (parseable by `json.loads`)
- [ ] JSON contains `python_version` (string, e.g. `"3.11.4"`)
- [ ] JSON contains `python_major` (int), `python_minor` (int), `python_patch` (int)
- [ ] JSON contains `os` (string, same value as current `get_os_info()` output)
- [ ] `python pyversion.py` (no flag) still prints the original two-line text output unchanged
- [ ] `python pyversion.py --help` or an unknown flag prints a usage message and exits non-zero
- [ ] `python -m pytest test_pyversion.py` passes

### US-002: Add --json flag to pyversion.sh

**Description:** As a developer, I want to run `pyversion.sh --json` so that I get structured JSON output from the shell script.

**Acceptance Criteria:**

- [ ] `bash pyversion.sh --json` exits with code 0
- [ ] Output is valid JSON (parseable by `python3 -c "import sys,json; json.load(sys.stdin)"`)
- [ ] JSON contains `python_version` (string, e.g. `"3.11.4"`)
- [ ] JSON contains `python_major` (int), `python_minor` (int), `python_patch` (int)
- [ ] JSON contains `os` (string)
- [ ] `bash pyversion.sh` (no flag) still prints the original text output unchanged
- [ ] An unrecognised flag prints an error to stderr and exits with code 1
- [ ] `bash -n pyversion.sh` passes (syntax check)

### US-003: Add unit tests for JSON output in pyversion.py

**Description:** As a developer, I want automated tests for the new `--json` flag so that regressions are caught in CI.

**Acceptance Criteria:**

- [ ] `test_pyversion.py` contains at least one test that calls `main()` (or its helper) with `--json` and asserts the output is valid JSON
- [ ] Test asserts presence of keys: `python_version`, `python_major`, `python_minor`, `python_patch`, `os`
- [ ] Test asserts types of each field (string for version/os, int for major/minor/patch)
- [ ] Existing tests still pass
- [ ] `python -m pytest test_pyversion.py` exits 0

## Functional Requirements

- FR-1: When invoked with `--json`, `pyversion.py` must print a single JSON object to stdout and nothing else.
- FR-2: When invoked with `--json`, `pyversion.sh` must print a single JSON object to stdout and nothing else.
- FR-3: The JSON object must always include the keys: `python_version` (string), `python_major` (int), `python_minor` (int), `python_patch` (int), `os` (string).
- FR-4: Default invocation (no flags) must remain 100% backward-compatible with current output format.
- FR-5: `pyversion.py` must use `argparse` (or equivalent) to parse the `--json` flag — no manual `sys.argv` parsing.
- FR-6: `pyversion.sh` must check `$1` for `--json` and pass it through to a Python one-liner or inline script that emits JSON.
- FR-7: Invalid/unknown flags must produce an error message on stderr and a non-zero exit code.

## Non-Goals

- No YAML, CSV, or other output formats (only `--json` in this iteration)
- No `--output-file` or file redirection flags
- No color/pretty-print option for JSON (compact single-line is fine)
- No changes to the OS detection logic itself
- No new CI pipeline setup (assumes `pytest` already runs in CI)

## Technical Considerations

- `pyversion.py` already imports `platform` and has `get_os_info()` — JSON output can reuse this directly.
- Use `json.dumps` in Python for guaranteed valid JSON serialisation.
- `pyversion.sh` should delegate JSON construction to a Python inline script (`python3 -c "..."`) to avoid fragile bash string quoting — do not hand-build JSON in bash.
- `platform.python_version_tuple()` returns `(major, minor, patch)` as strings — cast to `int` before putting in JSON.
- Keep `argparse` usage minimal in `pyversion.py`; a single optional `--json` flag is sufficient.

## Success Metrics

- `pyversion.py --json | python3 -m json.tool` succeeds on macOS, Linux, and Windows CI runners
- `pyversion.sh --json | python3 -m json.tool` succeeds on macOS and Linux CI runners
- All existing and new tests pass in CI
- No changes to default (non-JSON) output observed in regression tests

## Open Questions

- Should `python_patch` be `0` when `platform.python_version_tuple()` returns a non-numeric patch (e.g. release candidates like `"3.12.0rc1"`)? Recommend: extract leading digits, default to `0` if non-numeric.
- Should `pyversion.sh --json` also work when only `python` (not `python3`) is on PATH? Recommend: yes, reuse the same `python_cmd` detection logic already in the script.
[/PRD]

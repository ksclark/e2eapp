[PRD]
# PRD: CLI Python Version Display Tool

## Overview

A Bash shell script CLI tool that detects and displays the version number of the default Python interpreter (`python` or `python3`) found on the system PATH. Solves the common developer need to quickly check which Python version is active in the current environment.

## Goals

- Display the Python version number from the default `python` / `python3` on PATH
- Output just the clean version string (e.g., `3.11.4`)
- Handle cases where Python is not found gracefully
- Pass `shellcheck` and `bash -n` quality gates

## Quality Gates

These commands must pass for every user story:

- `shellcheck pyversion.sh` — Lint the shell script
- `bash -n pyversion.sh` — Syntax check

## User Stories

### US-001: Detect and display Python version from PATH

**Description:** As a developer, I want to run a shell script that prints the active Python version so that I can quickly confirm which Python is in use.

**Acceptance Criteria:**

- [ ] Script is named `pyversion.sh` and is executable (`chmod +x`)
- [ ] Script tries `python3 --version` first; falls back to `python --version` if `python3` is not found
- [ ] Outputs only the version number (e.g., `3.11.4`) to stdout, with no extra text
- [ ] Running `./pyversion.sh` in a terminal with Python available prints the version and exits 0

### US-002: Handle missing Python gracefully

**Description:** As a developer, I want the script to give a clear error when Python is not found so that I know what to fix.

**Acceptance Criteria:**

- [ ] If neither `python3` nor `python` is found on PATH, the script prints an error message to stderr (e.g., `Error: Python not found on PATH`)
- [ ] Script exits with a non-zero exit code (e.g., `exit 1`) when Python is missing
- [ ] No Python-related error output leaks to stdout

## Functional Requirements

- FR-1: The script MUST check for `python3` before `python` on PATH
- FR-2: The script MUST strip any leading label (e.g., "Python ") and output only the version number (e.g., `3.11.4`)
- FR-3: On success, the script MUST exit with code `0`
- FR-4: On failure (Python not found), the script MUST print to stderr and exit with a non-zero code
- FR-5: The script MUST be valid Bash and pass `shellcheck` without warnings

## Non-Goals

- Detecting all installed Python versions (pyenv, conda, etc.)
- Accepting a custom interpreter path as an argument
- Displaying installation path or build metadata
- Supporting Windows (PowerShell / CMD)
- Package manager installation (Homebrew, apt, etc.)

## Technical Considerations

- Use `command -v python3` or `which python3` to check presence before invoking
- Strip the "Python " prefix using shell parameter expansion or `awk`/`sed`
- Shebang should be `#!/usr/bin/env bash`
- Script file: `pyversion.sh` in the project root

## Success Metrics

- Script outputs a clean version string on a machine with Python installed
- Script exits non-zero with a stderr message on a machine without Python
- `shellcheck pyversion.sh` reports zero issues
- `bash -n pyversion.sh` exits 0

## Open Questions

- Should the script be added to a `bin/` directory or stay in the project root?
- Should it eventually accept an optional `--path` flag to show the interpreter path alongside the version?
[/PRD]

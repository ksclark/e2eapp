[PRD]
# PRD: Python Version Reporter

## Overview

A simple Python script that prints the current Python version and platform/OS information to the console (stdout). The script is run directly via `python main.py` and requires no installation.

## Goals

- Output Python version (e.g. `3.11.2`) to stdout
- Output platform/OS info (e.g. OS name, architecture) to stdout
- Keep the script simple and dependency-free (stdlib only)
- Pass `ruff` linting

## Quality Gates

These commands must pass for every user story:

- `ruff check .` — linting

## User Stories

### US-001: Print Python version to console

**Description:** As a developer, I want to run `python main.py` and see the current Python version printed to stdout so that I can quickly verify which Python is active.

**Acceptance Criteria:**

- [ ] Running `python main.py` prints the Python version string (e.g. `Python version: 3.11.2`)
- [ ] Output goes to stdout
- [ ] Uses `sys.version_info` or `platform.python_version()` from stdlib (no third-party deps)

### US-002: Print platform and OS info to console

**Description:** As a developer, I want the script to also print platform and OS information so that I have full environment context in one command.

**Acceptance Criteria:**

- [ ] Script prints OS name (e.g. `Linux`, `Darwin`, `Windows`)
- [ ] Script prints machine architecture (e.g. `x86_64`, `arm64`)
- [ ] Uses `platform` module from stdlib
- [ ] Output is human-readable and clearly labelled (e.g. `OS: Linux`, `Architecture: x86_64`)

## Functional Requirements

- FR-1: The script must be named `main.py` and runnable via `python main.py`
- FR-2: The script must print Python version to stdout on every run
- FR-3: The script must print OS name to stdout on every run
- FR-4: The script must print machine architecture to stdout on every run
- FR-5: The script must use only Python standard library modules (`sys`, `platform`)
- FR-6: Each piece of info must be on its own labelled line

## Non-Goals

- No file/log output
- No web endpoint or HTTP server
- No CLI argument parsing or flags
- No third-party dependencies
- Not installable as a pip package

## Technical Considerations

- Use `platform.python_version()` for the version string
- Use `platform.system()` for OS name
- Use `platform.machine()` for architecture
- No `requirements.txt` or `pyproject.toml` needed

## Success Metrics

- `python main.py` runs without errors and prints all three fields
- `ruff check .` passes with zero warnings

## Open Questions

- None
[/PRD]

[PRD]
# PRD: Print OS Version in Script

## Overview

Extend the existing Python version detection script to also print the operating system name and version. This gives developers a quick, single-command way to capture both runtime and environment information.

## Goals

- Print the OS name and version (e.g. `macOS 14.4`, `Ubuntu 22.04`) as a new line in the script's output
- Output the OS version **after** the Python version line
- Use only the Python standard library (no new dependencies)

## Quality Gates

These commands must pass for every user story:

- `python -m pytest` — Run the test suite

## User Stories

### US-001: Print OS version after Python version

**Description:** As a developer, I want the script to print the OS name and version on its own line after the Python version, so that I can capture full environment info in one command.

**Acceptance Criteria:**

- [ ] Script prints OS name and version on a new line immediately after the Python version line
- [ ] Output format is human-friendly (e.g. `OS: macOS 14.4` or `OS: Ubuntu 22.04`)
- [ ] Uses `platform` module from the Python standard library
- [ ] Existing Python version output is unchanged
- [ ] `python -m pytest` passes

## Functional Requirements

- FR-1: After printing the Python version, the script must print a line containing the OS name and version in the format `OS: <name> <version>`
- FR-2: The OS detection must use `platform.system()` and `platform.release()` (or `platform.version()` for more detail on Linux/Windows)
- FR-3: No third-party packages may be introduced

## Non-Goals

- Printing raw platform strings (e.g. `Darwin 23.4.0 x86_64`)
- Detecting CPU architecture or hardware info
- Structured/JSON output format
- Changes to any other script

## Technical Considerations

- Use Python's built-in `platform` module
- `platform.system()` returns `Darwin`, `Linux`, or `Windows` — map to friendly names if desired
- `platform.mac_ver()`, `platform.win32_ver()`, and reading `/etc/os-release` can give friendlier version strings per platform

## Success Metrics

- Running the script on macOS, Linux, and Windows each produces a correct, human-readable OS line
- No regressions to existing Python version output
- All tests pass

## Open Questions

- Should `Darwin` be displayed as `macOS` (friendlier) or left as-is?
- Should the OS line label be `OS:` or something else (e.g. `Platform:`)?
[/PRD]

# pyversion

A pair of lightweight tools that detect and display the active Python version and OS information. Both scripts use only the Python standard library and require no additional dependencies.

| Tool | Language | Purpose |
|------|----------|---------|
| `pyversion.py` | Python | Prints Python version + OS name/version; supports `--json` output |
| `pyversion.sh` | Bash | Prints the bare Python version string from the system PATH |

---

## Prerequisites

- **Python 3.6+** — required to run `pyversion.py` and its test suite
- **Bash** — required to run `pyversion.sh`
- **pytest** — required to run the test suite (`pip install pytest`)
- **shellcheck** *(optional)* — to lint `pyversion.sh` (`brew install shellcheck` / `apt install shellcheck`)

---

## Usage

### `pyversion.py` — Python version and OS reporter

```bash
python pyversion.py
```

**Default output** (two lines to stdout):

```
3.11.4
OS: macOS 14.4
```

#### Flags

| Flag | Description |
|------|-------------|
| `--json` | Output all fields as a single-line JSON object |
| `--help` | Show usage information |

#### `--json` output

```bash
python pyversion.py --json
```

```json
{"python_version": "3.11.4", "python_major": 3, "python_minor": 11, "python_patch": 4, "os": "macOS 14.4"}
```

**JSON field reference:**

| Field | Type | Description |
|-------|------|-------------|
| `python_version` | `string` | Full version string (e.g. `"3.11.4"`) |
| `python_major` | `integer` | Major version component |
| `python_minor` | `integer` | Minor version component |
| `python_patch` | `integer` | Patch version component |
| `os` | `string` | Human-friendly OS name and version (e.g. `"macOS 14.4"`, `"Ubuntu 22.04"`) |

#### OS detection behaviour

`pyversion.py` maps raw platform values to human-friendly names:

| Platform | Source | Example output |
|----------|--------|----------------|
| macOS | `platform.mac_ver()[0]`; falls back to `platform.release()` in CI | `macOS 14.4` |
| Windows | `platform.win32_ver()[1]` (trimmed to `major.minor`); falls back to `platform.release()` | `Windows 10.0` |
| Linux | `NAME` and `VERSION_ID` from `/etc/os-release`; falls back to kernel release | `Ubuntu 22.04` |
| Other | Raw `platform.system()` + `platform.release()` | `FreeBSD 13.2` |

---

### `pyversion.sh` — Bash version checker

```bash
bash pyversion.sh
# or, after chmod +x pyversion.sh:
./pyversion.sh
```

**Output** (one line to stdout):

```
3.11.4
```

The script tries `python3` first, then falls back to `python`. If neither is found, it prints an error to stderr and exits with code `1`.

#### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Python found; version printed successfully |
| `1` | Python not found on PATH, or version query failed |

---

## Running the tests

The test suite covers `pyversion.py` (OS detection, JSON output, flag handling, and edge cases):

```bash
python -m pytest test_pyversion.py
```

Run with verbose output:

```bash
python -m pytest test_pyversion.py -v
```

### Shell script quality checks

```bash
bash -n pyversion.sh          # syntax check
shellcheck pyversion.sh       # lint (requires shellcheck)
```

---

## Project structure

```
.
├── pyversion.py          # Python version + OS reporter (with --json support)
├── pyversion.sh          # Bash wrapper — prints bare version string
├── test_pyversion.py     # pytest test suite for pyversion.py
└── tasks/                # Product requirement documents (PRDs)
    ├── prd-cli-python-version-display-tool.md
    └── prd-python-version-reporter.md
```

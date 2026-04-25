"""Tests for pyversion.py OS detection."""
import json
import platform
import sys
from unittest import mock

import pytest

from pyversion import get_os_info, main
import io


def test_get_os_info_returns_string():
    result = get_os_info()
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="Darwin→macOS mapping only relevant on macOS hosts",
)
def test_get_os_info_not_raw_darwin():
    """Should not return raw 'Darwin' — should map to 'macOS' on Darwin systems."""
    result = get_os_info()
    assert not result.startswith("Darwin"), "Expected friendly name, got raw 'Darwin'"


def test_get_os_info_macos(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    result = get_os_info()
    assert result == "macOS 14.4"


def test_get_os_info_macos_empty_ver_fallback(monkeypatch):
    """mac_ver()[0] == '' in CI → falls back to platform.release()."""
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("", ("", "", ""), ""))
    monkeypatch.setattr(platform, "release", lambda: "23.4.0")
    result = get_os_info()
    assert result == "macOS 23.4.0"


def test_get_os_info_windows_empty_ver_fallback(monkeypatch):
    """win32_ver()[1] == '' in CI → falls back to platform.release()."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "win32_ver", lambda: ("10", "", "SP0", ""))
    monkeypatch.setattr(platform, "release", lambda: "10")
    result = get_os_info()
    assert result == "Windows 10"


def test_get_os_info_linux_with_os_release(monkeypatch, tmp_path):
    os_release = tmp_path / "os-release"
    os_release.write_text('NAME="Ubuntu"\nVERSION_ID="22.04"\n')
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    original_open = open

    def mock_open(path, *args, **kwargs):
        if path == "/etc/os-release":
            return original_open(str(os_release), *args, **kwargs)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    result = get_os_info()
    assert result == "Ubuntu 22.04"


def test_get_os_info_linux_escaped_quotes(monkeypatch, tmp_path):
    """os-release values with escaped inner quotes are parsed correctly."""
    os_release = tmp_path / "os-release"
    os_release.write_text('NAME="Ubuntu \\"Focal\\""\nVERSION_ID="20.04"\n')
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    original_open = open

    def mock_open(path, *args, **kwargs):
        if path == "/etc/os-release":
            return original_open(str(os_release), *args, **kwargs)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    result = get_os_info()
    assert result == 'Ubuntu "Focal" 20.04'


def test_get_os_info_linux_no_version_id(monkeypatch, tmp_path):
    """NAME present but VERSION_ID absent (e.g. Arch Linux) → kernel release."""
    os_release = tmp_path / "os-release"
    os_release.write_text('NAME="Arch Linux"\n')
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "release", lambda: "6.8.9-arch1-1")
    original_open = open

    def mock_open(path, *args, **kwargs):
        if path == "/etc/os-release":
            return original_open(str(os_release), *args, **kwargs)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    result = get_os_info()
    assert result == "Arch Linux 6.8.9-arch1-1"


def test_get_os_info_linux_no_os_release(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "release", lambda: "5.15.0")

    def raise_os_error(path, *args, **kwargs):
        raise OSError("not found")

    monkeypatch.setattr("builtins.open", raise_os_error)
    result = get_os_info()
    assert result == "Linux 5.15.0"


def test_get_os_info_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "win32_ver", lambda: ("10", "10.0", "SP0", "Multiprocessor Free"))
    result = get_os_info()
    assert result == "Windows 10.0"


def test_get_os_info_unknown(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "FreeBSD")
    monkeypatch.setattr(platform, "release", lambda: "13.2")
    result = get_os_info()
    assert result == "FreeBSD 13.2"


def test_main_output(monkeypatch, capsys):
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main([])
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert lines[0] == "3.11.4"
    assert lines[1] == "OS: macOS 14.4"


# ---------------------------------------------------------------------------
# --json flag tests
# ---------------------------------------------------------------------------

def test_main_json_output_is_valid_json(monkeypatch, capsys):
    """--json flag produces parseable JSON on stdout."""
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "python_version_tuple", lambda: ("3", "11", "4"))
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main(["--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)  # raises if not valid JSON
    assert data is not None


def test_main_json_required_keys(monkeypatch, capsys):
    """--json output contains all required keys."""
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "python_version_tuple", lambda: ("3", "11", "4"))
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main(["--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    for key in ("python_version", "python_major", "python_minor", "python_patch", "os"):
        assert key in data, f"Missing key: {key}"


def test_main_json_field_types(monkeypatch, capsys):
    """--json output fields have the correct types."""
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "python_version_tuple", lambda: ("3", "11", "4"))
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main(["--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data["python_version"], str)
    assert isinstance(data["python_major"], int)
    assert isinstance(data["python_minor"], int)
    assert isinstance(data["python_patch"], int)
    assert isinstance(data["os"], str)


def test_main_json_field_values(monkeypatch, capsys):
    """--json output contains the expected field values."""
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "python_version_tuple", lambda: ("3", "11", "4"))
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main(["--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["python_version"] == "3.11.4"
    assert data["python_major"] == 3
    assert data["python_minor"] == 11
    assert data["python_patch"] == 4
    assert data["os"] == "macOS 14.4"


def test_main_json_no_text_output(monkeypatch, capsys):
    """--json flag does NOT produce the plain-text lines."""
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "python_version_tuple", lambda: ("3", "11", "4"))
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main(["--json"])
    captured = capsys.readouterr()
    assert "OS:" not in captured.out
    # Output should be a single line of JSON
    lines = captured.out.strip().splitlines()
    assert len(lines) == 1


def test_main_no_json_flag_unchanged(monkeypatch, capsys):
    """Default (no --json) behavior is unchanged."""
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.4", ("", "", ""), ""))
    main([])
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert lines[0] == "3.11.4"
    assert lines[1] == "OS: macOS 14.4"


def test_main_unknown_flag_exits_nonzero():
    """Unknown/invalid flags must exit non-zero."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--invalid-flag-xyz"])
    assert exc_info.value.code != 0

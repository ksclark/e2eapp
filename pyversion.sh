#!/usr/bin/env bash
# pyversion.sh — print the installed Python version number (e.g. 3.11.4)
set -euo pipefail

if command -v python3 > /dev/null 2>&1; then
    python_cmd="python3"
elif command -v python > /dev/null 2>&1; then
    python_cmd="python"
else
    echo "Error: neither python3 nor python found in PATH" >&2
    exit 1
fi

flag="${1:-}"

if [ "$#" -gt 1 ]; then
    echo "Error: unexpected arguments" >&2
    exit 1
fi

if [ "$flag" = "--json" ]; then
    "$python_cmd" -c "import platform,json; v=platform.python_version_tuple(); s=platform.system(); r=(platform.mac_ver()[0] or platform.release()) if s=='Darwin' else (platform.win32_ver()[1] or platform.release()) if s=='Windows' else platform.release(); n='macOS' if s=='Darwin' else ('Windows' if s=='Windows' else s); print(json.dumps({'python_version':platform.python_version(),'python_major':int(v[0]),'python_minor':int(v[1]),'python_patch':int(v[2]),'os':n+' '+r}))"
elif [ -n "$flag" ]; then
    echo "Error: unknown flag: $flag" >&2
    exit 1
else
    version=$("$python_cmd" --version 2>&1) || {
        echo "Error: failed to get version from $python_cmd" >&2
        exit 1
    }
    printf '%s\n' "${version#Python }"
fi

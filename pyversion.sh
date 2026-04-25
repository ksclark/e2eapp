#!/usr/bin/env bash
# pyversion.sh — print the installed Python version number (e.g. 3.11.4)

if command -v python3 > /dev/null 2>&1; then
    python_cmd="python3"
elif command -v python > /dev/null 2>&1; then
    python_cmd="python"
else
    echo "Error: neither python3 nor python found in PATH" >&2
    exit 1
fi

version=$("$python_cmd" --version 2>&1)
echo "${version#Python }"

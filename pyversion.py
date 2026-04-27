"""Print Python version and OS name/version."""
import argparse
import json
import platform
import shlex


def get_os_info():
    """Return a human-friendly OS name and version string."""
    system = platform.system()
    if system == "Darwin":
        os_name = "macOS"
        # mac_ver()[0] can return "" in some CI/virtualized environments
        version = platform.mac_ver()[0] or platform.release()
    elif system == "Windows":
        os_name = "Windows"
        # win32_ver()[1] can return "" in some CI/virtualized environments
        version = platform.win32_ver()[1] or platform.release()
        # Trim to major.minor if it's long
        parts = version.split(".")
        version = ".".join(parts[:2]) if len(parts) >= 2 else version
    elif system == "Linux":
        os_name = "Linux"
        # Try to get a friendly distro name from /etc/os-release
        try:
            with open("/etc/os-release") as f:
                info = {}
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        k, _, v = line.partition("=")
                        # Use shlex to correctly handle shell-quoted values
                        # (e.g. escaped inner quotes: NAME="Ubuntu \"Focal\"")
                        try:
                            parsed = shlex.split(v)[0]
                        except (ValueError, IndexError):
                            # ValueError: malformed shell quoting
                            # IndexError: empty value (e.g. NAME=)
                            parsed = v.strip('"')
                        if parsed:  # skip empty values
                            info[k] = parsed
            os_name = info.get("NAME", "Linux")
            version = info.get("VERSION_ID", platform.release())
        except OSError:
            version = platform.release()
    else:
        os_name = system
        version = platform.release()

    return f"{os_name} {version}".strip()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print Python version and OS information."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output version and OS info as a JSON object.",
    )
    parser.add_argument(
        "--hello",
        action="store_true",
        help="Print Hello, World! to stdout.",
    )
    args = parser.parse_args(argv)

    if args.hello:
        print("Hello, World!")
    elif args.json:
        major, minor, patch = platform.python_version_tuple()
        data = {
            "python_version": platform.python_version(),
            "python_major": int(major),
            "python_minor": int(minor),
            "python_patch": int(patch),
            "os": get_os_info(),
        }
        print(json.dumps(data, ensure_ascii=False))
    else:
        print(platform.python_version())
        print(f"OS: {get_os_info()}")


if __name__ == "__main__":
    main()

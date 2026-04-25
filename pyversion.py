"""Print Python version and OS name/version."""
import platform
import sys


def get_os_info():
    """Return a human-friendly OS name and version string."""
    system = platform.system()
    if system == "Darwin":
        os_name = "macOS"
        version = platform.mac_ver()[0]  # e.g. '14.4'
    elif system == "Windows":
        os_name = "Windows"
        version = platform.win32_ver()[1]  # e.g. '10.0.19041'
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
                        info[k] = v.strip('"')
            os_name = info.get("NAME", "Linux")
            version = info.get("VERSION_ID", platform.release())
        except OSError:
            version = platform.release()
    else:
        os_name = system
        version = platform.release()

    return f"{os_name} {version}".strip()


def main():
    print(platform.python_version())
    print(f"OS: {get_os_info()}")


if __name__ == "__main__":
    main()

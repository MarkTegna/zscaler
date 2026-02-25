"""
Version management utility for ZScaler
Handles version increments according to version management standards
"""

import re
import sys
from datetime import datetime


def get_current_version():
    """Read current version from zscaler.py"""
    with open('zscaler.py', 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "0.0.1"


def parse_version(version_str):
    """Parse version string into components"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)([a-z]?)$', version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")

    major, minor, patch, letter = match.groups()
    return int(major), int(minor), int(patch), letter


def format_version(major, minor, patch, letter=''):
    """Format version components into string"""
    version = f"{major}.{minor}.{patch}"
    if letter:
        version += letter
    return version


def increment_letter(letter):
    """Increment letter suffix, return (new_letter, overflow)"""
    if not letter:
        return 'a', False
    if letter == 'z':
        return '', True  # Overflow
    return chr(ord(letter) + 1), False


def update_version_in_file(new_version):
    """Update version in zscaler.py"""
    with open('zscaler.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update version
    content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )

    # Update compile date
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r'__compile_date__\s*=\s*["\'][^"\']+["\']',
        f'__compile_date__ = "{today}"',
        content
    )

    with open('zscaler.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Version updated to: {new_version}")


def automatic_build():
    """Handle automatic build version increment (letter only)"""
    current = get_current_version()
    major, minor, patch, letter = parse_version(current)

    new_letter, overflow = increment_letter(letter)

    if overflow:
        # Letter overflow - increment patch internally but don't create artifacts
        patch += 1
        new_letter = 'a'
        print(f"Letter overflow detected - internal PATCH increment to {patch}")

    new_version = format_version(major, minor, patch, new_letter)
    update_version_in_file(new_version)
    print("Automatic build - no artifacts created")


def user_build():
    """Handle user-requested build (remove letter, increment patch)"""
    current = get_current_version()
    major, minor, patch, _ = parse_version(current)

    # Remove letter suffix and increment patch
    patch += 1
    new_version = format_version(major, minor, patch, '')

    update_version_in_file(new_version)
    print(f"User build - version updated to {new_version}")
    print("Ready to create distribution artifacts")


def increment_minor():
    """Increment minor version (for GitHub pushes)"""
    current = get_current_version()
    major, minor, _, _ = parse_version(current)

    minor += 1
    patch = 0
    new_version = format_version(major, minor, patch, '')

    update_version_in_file(new_version)
    print(f"Minor version incremented to {new_version}")


def increment_major():
    """Increment major version"""
    current = get_current_version()
    major, _, _, _ = parse_version(current)

    major += 1
    minor = 0
    patch = 0
    new_version = format_version(major, minor, patch, '')

    update_version_in_file(new_version)
    print(f"Major version incremented to {new_version}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python update_version.py [auto|user|minor|major]")
        print(f"Current version: {get_current_version()}")
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == 'auto':
            automatic_build()
        elif command == 'user':
            user_build()
        elif command == 'minor':
            increment_minor()
        elif command == 'major':
            increment_major()
        else:
            print(f"Unknown command: {command}")
            print("Valid commands: auto, user, minor, major")
            sys.exit(1)
    except (ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

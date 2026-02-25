"""
Build script for ZScaler program
Creates Windows executable and distribution zip
"""

import os
import sys
import zipfile
import subprocess
from datetime import datetime


def get_version():
    """Extract version from zscaler.py"""
    with open('zscaler.py', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return "0.0.1"


def update_compile_date():
    """Update compile date in zscaler.py"""
    with open('zscaler.py', 'r', encoding='utf-8') as f:
        content = f.read()

    today = datetime.now().strftime("%Y-%m-%d")
    content = content.replace(
        '__compile_date__ = datetime.now().strftime("%Y-%m-%d")',
        f'__compile_date__ = "{today}"'
    )

    with open('zscaler.py', 'w', encoding='utf-8') as f:
        f.write(content)


def build_executable():
    """Build Windows executable using PyInstaller"""
    print("Building executable...")

    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--onefile',
        '--console',
        '--name', 'zscaler',
        '--clean',
        'zscaler.py'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return False

    print("Executable built successfully")
    return True


def create_distribution():
    """Create distribution zip file"""
    version = get_version()
    zip_filename = f"zscaler_v{version}.zip"
    zip_path = os.path.join('dist', zip_filename)

    print(f"Creating distribution: {zip_filename}")

    # Ensure dist directory exists
    os.makedirs('dist', exist_ok=True)

    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add executable
        exe_path = os.path.join('dist', 'zscaler.exe')
        if os.path.exists(exe_path):
            zipf.write(exe_path, 'zscaler.exe')

        # Add config file
        if os.path.exists('zscaler.ini'):
            zipf.write('zscaler.ini', 'zscaler.ini')

        # Add README if exists
        if os.path.exists('README.md'):
            zipf.write('README.md', 'README.md')

        # Add CHANGELOG if exists
        if os.path.exists('CHANGELOG.md'):
            zipf.write('CHANGELOG.md', 'CHANGELOG.md')

    print(f"Distribution created: {zip_path}")
    return True


def main():
    """Main build process"""
    print("=" * 50)
    print("ZScaler Build Process")
    print("=" * 50)

    # Update compile date
    update_compile_date()

    # Build executable
    if not build_executable():
        sys.exit(1)

    # Create distribution
    if not create_distribution():
        sys.exit(1)

    version = get_version()
    print("=" * 50)
    print(f"Build completed successfully - Version {version}")
    print("=" * 50)


if __name__ == "__main__":
    main()

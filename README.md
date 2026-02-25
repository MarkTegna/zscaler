# ZScaler Display Program

A simple Windows program that displays "ZScaler" to the screen and waits 10 seconds before exiting.

## Author
Mark Oldham

## Version
0.0.1

## Compile Date
2026-02-25

## Requirements
- Python 3.7 or higher
- PyInstaller (for building executable)

## Installation

### From Source
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the program:
```bash
python zscaler.py
```

### From Executable
Simply run `zscaler.exe` from the distribution package.

## Configuration

The program uses `zscaler.ini` for configuration:

```ini
[Display]
# Message to display on screen
message = ZScaler

# Number of seconds to wait before exiting
wait_seconds = 10
```

## Building

To build the Windows executable and distribution package:

```bash
python build.py
```

This will create:
- `dist/zscaler.exe` - Windows executable
- `dist/zscaler_v0.0.1.zip` - Distribution package

## Usage

Run the program:
```bash
zscaler.exe
```

The program will:
1. Display "ZScaler" to the console
2. Wait 10 seconds
3. Exit automatically

## License

Copyright (c) 2026 Mark Oldham

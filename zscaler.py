"""
ZScaler Display Program
A simple Windows program that displays "ZScaler" and waits 10 seconds before exiting.
"""

import time
import configparser
import os

__version__ = "0.2.0"
__author__ = "Mark Oldham"
__compile_date__ = "2026-02-25"


def load_config():
    """Load configuration from zscaler.ini"""
    config = configparser.ConfigParser()
    config_file = 'zscaler.ini'

    if os.path.exists(config_file):
        config.read(config_file)
    else:
        # Create default config
        config['Display'] = {
            'message': 'ZScaler',
            'wait_seconds': '10'
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)

    return config


def main():
    """Main program entry point"""
    config = load_config()

    # Get configuration values
    message = config.get('Display', 'message', fallback='ZScaler')
    wait_seconds = config.getint('Display', 'wait_seconds', fallback=10)

    # Display the message
    print(message)

    # Wait for specified seconds
    time.sleep(wait_seconds)


if __name__ == "__main__":
    main()

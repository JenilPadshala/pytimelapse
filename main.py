"""
PyTimeLapse
A cross-platform timelapse camera application for MacOS and Raspberry Pi OS.
"""

import sys
import platform
import argparse
import os

def get_operating_system():
    """Detect the underlying operating system."""
    
    os_name = sys.platform
    if os_name == "darwin":
        return "macos"
    elif os_name.startswith("linux"):
        return "linux"
    else:
        return "unsupported"

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="PyTimeLapse - Capture timelapse sequences.")
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default =  10.0,
        help = "Time interval between captures in seconds (default: 10.0)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default = "timelapse_output",
        help = "Directory to save captured images (default: 'timelapse_output')"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default = 0,
        help = "Maximum number of images to capture (default: 0 for unlimited)"
    )
    args = parser.parse_args()
    return args


def main():
    print("Starting PyTimeLapse application...")
    # --- Placeholder for future logic ---
    # 1. Parse arguments
    args = parse_arguments()
    print(f"Configuration:")
    print(f" Interval: {args.interval} seconds")
    print(f" Output Directory: {args.output}")
    print(f" Image Limit: {'No limit' if args.limit == 0 else args.limit}")

    # 2. Detect platform
    current_os = get_operating_system()
    print(f"Detected operating system: {current_os}")
    
    if current_os == "unsupported":
        print(f"Error: Unsupported operating system '{sys.platform}'. Exiting.")
        sys.exit(1)
    
    if current_os == "linux":
        print("Linux platform detected. RPI - spcific implementation will be added later.")

    # 3. Initialize camera based on platform
    # 4. Start timelapse loop
    # 5. Cleanup
    # --- End Placeholder ---
    print("PyTimelapse finished (Placeholder).")

if __name__ == "__main__":

    main()

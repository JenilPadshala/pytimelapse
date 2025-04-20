"""
PyTimeLapse
A cross-platform timelapse camera application for MacOS and Raspberry Pi OS.
"""

import sys
import platform

def get_operating_system():
    """Detect the underlying operating system."""
    
    os_name = sys.platform
    if os_name == "darwin":
        return "macos"
    elif os_name.startswith("linux"):
        return "linux"
    else:
        return "unsupported"

def main():
    print("Starting PyTimeLapse application...")
    # --- Placeholder for future logic ---
    # 1. Parse arguments
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

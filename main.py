"""
PyTimeLapse
A cross-platform timelapse camera application for MacOS and Raspberry Pi OS.
"""

import sys
import platform
import argparse
import os
import time

# Import camera classes and factory function
from camera import MacCamera, PiCamera, CameraError, get_camera


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
    # 3. Initialize camera based on platform
    camera = None
    try:
        camera_config = {}
        camera = get_camera(os_type=current_os, config=camera_config)

        with camera:
            print("Camera initialized successfully. (Placeholder)")
            # 4. Start timelapse loop
            print("Starting capture loop (Placeholder - 1 capture)")
            try:
                os.makedirs(args.output, exist_ok=True)
                print(f"Output directory '{args.output}' ensured.")
            except OSError as e:
                print(f"Error creating output directory '{args.output}': {e}")
                raise CameraError(f"Cannot create output directory: {e}") from e
            filename = os.path.join(args.output, "placeholder_capture_00001.jpg")
            camera.capture_image(filename)
            time.sleep(1)
    
    except CameraError as e:
        print(f"Camera error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if camera:
            camera.shutdown()
        sys.exit(1)
    finally:
        print("Camera shutdown sequence completed.")

    # 5. Cleanup
    # --- End Placeholder ---
    print("PyTimelapse finished (Placeholder).")

if __name__ == "__main__":

    main()

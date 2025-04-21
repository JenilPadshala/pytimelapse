"""
PyTimeLapse
A cross-platform timelapse camera application for MacOS and Raspberry Pi OS.
"""

import sys
import platform
import argparse
import os
import time
import datetime

# Import camera classes and factory function
from camera import MacCamera, PiCamera, CameraError, get_camera

# Import video compilation util
from video_utils import compile_video_ffmpeg

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
    # video compilation arguments
    parser.add_argument(
        "--compile-video",
        action="store_true", # makes it a flag, True if present
        help="Compile captured images into a video after capture finishes (requires ffmpeg)."
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="Framerate(frames per second) for the compiled video (default: 24)."
    )
    parser.add_argument(
        "--video-filename",
        type=str,
        default="timelapse.mp4",
        help="Filename for the compiled video (default: timeplapse.mp4)."
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

    # validate interval
    if args.interval <= 0:
        print("Error: Interval must be positive.")
        sys.exit(1)
    
    # 2. Detect platform
    current_os = get_operating_system()
    print(f"Detected operating system: {current_os}")
    
    if current_os == "unsupported":
        print(f"Error: Unsupported operating system '{sys.platform}'. Exiting.")
        sys.exit(1)
    # 3. Initialize camera based on platform
    camera = None
    images_captured = 0
    start_time = time.monotonic() 
    try:
        # Ensuring output directory exists
        try: 
            print(f"Ensuring output directory '{args.output}' exists...")
            os.makedirs(args.output, exist_ok=True)
        except OSError as e:
            print(f"Error creating output directory '{args.output}': {e}")
            sys.exit(1)
        
        # Initialize camera
        print("Initializing camera...")
        camera_config = {}
        camera = get_camera(os_type=current_os, config=camera_config)

        # use context manager for automatic setup/teardown
        with camera:
            print("Camera initialized successfully. Starting timelapse capture...")
            print(f"Press Ctrl+C to stop the capture early.")

            # Start timelapse loop
            capture_count = 0
            while True:
                if args.limit > 0 and capture_count >= args.limit:
                    print(f"\nReached image limit ({args.limit}). Stopping capture.")
                    break

                image_number = capture_count + 1
                filename = f"image_{image_number:05d}.jpg"
                filepath = os.path.join(args.output, filename)

                # capture the image
                try:
                    print(f"Capturing image {image_number}{f'/{args.limit}' if args.limit > 0 else ''} to {filepath}...")
                    success = camera.capture_image(filepath)
                    if success:
                        capture_count +=1
                        images_captured += 1
                    else:
                        print(f"Warning: Capture attempt for {filepath} reported failure but didn't raise error.")
                except CameraError as e:
                    print(f"\nError during capture for {filepath}: {e}")
                    print("Attempting to continue capture...")
                    time.sleep(args.interval)
                    continue

                # Wait for the next interval
                if args.limit > 0 and capture_count >= args.limit:
                    print(f"\nReached image limit ({args.limit}). Stopping capture.")
                    break

                print(f"Waiting for {args.interval} seconds before next capture...")
                try:
                    time.sleep(args.interval)
                except KeyboardInterrupt:
                    print("\nStopping loop due to Ctrl+C.")
                    break
    
    except CameraError as e:
        print(f"\nCritical Camera Error during setup or loop: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCapture interrupted by user (Ctrl+C).")
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {type(e).__name__}: {e}")
    finally:
        end_time = time.monotonic()
        duration = end_time - start_time
        print("-" * 30)
        print("PyTimelapse finished.")
        print(f"Total images captured: {images_captured}")
        print(f"Total duration: {datetime.timedelta(seconds=duration)}")
        print("-" * 30)
        
        # --- Call video compilation if requested ---
        if args.compile_video and images_captured > 0:
            print("\nVideo compilation requested.")
            # Define the image pattern based on how files were saved
            image_pattern = "image_%05d.jpg" # Matches f"image_{image_number:05d}.jpg"
            # Construct the full output video path (can be relative or absolute)
            video_output_path = os.path.join(args.output, args.video_filename)

            compile_video_ffmpeg(
                image_folder=args.output,
                image_pattern=image_pattern,
                output_filename=video_output_path,
                fps=args.fps
            )
        elif args.compile_video and images_captured == 0:
             print("\nVideo compilation skipped: No images were captured.")

if __name__ == "__main__":
    main()

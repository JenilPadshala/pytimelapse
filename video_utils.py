import subprocess
import shutil
import os


def check_ffmpeg():
    """Checks if ffmpeg command exists in the system PATH."""
    return shutil.which("ffmpeg") is not None


def compile_video_ffmpeg(image_folder, image_pattern, output_filename, fps):
    """
    Compiles images into a video using ffmpeg.

    Args:
        image_folder (str) : Path to the folder containing images.
        image_pattern (str) : Filename pattern (e.g., 'image_%05d.jpg').
        output_filename (str) : Path for the output video file.
        fpg (int) : Framerate for the output video.

    Returns:
        bool: True if compilation succeeded, False otherwise.
    """

    if not check_ffmpeg():
        print("Error: ffmpeg command not found. Cannot compile video.")
        print(
            "Please install ffmpeg (e.g., 'brew install ffmpeg' or 'sudo apt install ffmpeg')."
        )
        return False

    print("\nAttempting to compile video using ffmpeg...")
    print(f"  Image Source: {os.path.join(image_folder, image_pattern)}")
    print(f"  Output Video: {output_filename}")
    print(f"  Framerate: {fps}")

    # Ensure output directory exists for the video file
    video_output_dir = os.path.dirname(output_filename)
    if video_output_dir and not os.path.exists(video_output_dir):
        try:
            os.makedirs(video_output_dir)
            print(f"Created directory for video output: {video_output_dir}")
        except OSError as e:
            print(
                f"Error creating directory for video output '{video_output_dir}': {e}"
            )
            return False

    command = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        os.path.join(image_folder, image_pattern),  # Input pattern
        "-c:v",
        "libx264",  # Video codec H.264 (widely compatible)
        "-pix_fmt",
        "yuv420p",  # Pixel format for compatibility
        "-crf",
        "23",  # Constant Rate Factor (lower means better quality, 18-28 is common range)
        "-preset",
        "medium",  # Encoding speed vs compression (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
        output_filename,  # Output file path
    ]

    print(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        # Print ffmpeg output (stderr often contains progress/info)
        if result.stdout:
            print("\n--- ffmpeg stdout ---")
            print(result.stdout)
        if result.stderr:
            print("\n--- ffmpeg stderr ---")
            print(result.stderr)  # Print errors or progress info

        if result.returncode != 0:
            print(
                f"\nError: ffmpeg compilation failed with return code {result.returncode}."
            )
            return False
        else:
            print(f"\nVideo compilation successful: {output_filename}")
            return True

    except FileNotFoundError:
        # This should theoretically be caught by check_ffmpeg, but as fallback
        print("Error: ffmpeg command not found. Cannot compile video.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during ffmpeg execution: {e}")
        return False

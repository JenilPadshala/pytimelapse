# PyTimelapse

PyTimelapse is a powerful, user-friendly Python application for creating high-quality timelapses with minimal setup. This tool allows you to capture image sequences at configurable intervals on macOS (with full support for built-in and USB webcams) and has planned support for Raspberry Pi cameras. 

Featuring a clean command-line interface with intuitive parameters, PyTimelapse makes it easy to customize your capture process. When your timelapse sequence is complete, PyTimelapse can automatically compile the images into a polished video using ffmpeg. The project leverages modern Python tooling with `uv` package manager support for simple installation and dependency management.

A cross-platform Python script for capturing timelapse image sequences on macOS and (planned) Raspberry Pi, with an option to compile the sequence into a video using ffmpeg.

## Features

- **Timelapse Capture:** Captures images at regular, user-defined intervals.
- **Cross-Platform (WIP):**
  - **macOS:** Fully supported using built-in or USB webcams via OpenCV. Includes camera warm-up logic to improve initial exposure.
  - **Raspberry Pi:** Structure in place, but implementation using `picamera2` is planned for the future.
- **Configurable:**
  - Set time interval between captures (`--interval`).
  - Specify output directory for images (`--output`).
  - Set a maximum number of images to capture (`--limit`, 0 for unlimited).
- **Sequential Naming:** Saves images with zero-padded sequential filenames (e.g., `image_00001.jpg`, `image_00002.jpg`).
- **Video Compilation (Optional):**
  - Compile the captured image sequence into a video file (e.g., MP4).
  - Requires external `ffmpeg` tool to be installed.
  - Enable with `--compile-video` flag.
  - Configure framerate (`--fps`) and output video filename (`--video-filename`).
- **Graceful Stop:** Press `Ctrl+C` to stop the capture process cleanly.

## Requirements

- **Python:** Version 3.8 or higher recommended.
- **`uv` Package Manager:** Recommended for easy setup and dependency management ([Install uv](https://github.com/astral-sh/uv#installation)).
- **Python Libraries:**
  - `opencv-python`: For camera access on macOS (installed via `uv`).
- **External Tools:**
  - `ffmpeg`: **Required only if using the `--compile-video` feature.**
    - **macOS:** Install using Homebrew: `brew install ffmpeg`
    - **Debian/Ubuntu/Raspberry Pi OS:** Install using apt: `sudo apt update && sudo apt install ffmpeg`

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone <your-repository-url>
    cd pytimelapse
    ```

2.  **Install `uv` (if you haven't already):**
    Follow instructions at [https://github.com/astral-sh/uv#installation](https://github.com/astral-sh/uv#installation).

3.  **Create Virtual Environment:**

    ```bash
    uv venv
    ```

4.  **Activate Environment:**

    ```bash
    # macOS / Linux
    source .venv/bin/activate
    # Windows (check uv docs for specific shell)
    ```

5.  **Install Dependencies:**

    ```bash
    uv pip sync --all-extras
    ```

    _(This installs core dependencies like `opencv-python` and development dependencies like `pytest`)_

6.  **macOS Camera Permissions:**
    The first time you run the script on macOS, the operating system should prompt you to grant camera access to your terminal or IDE (e.g., Terminal, VS Code, PyCharm). You **must allow** this for the script to work. If you accidentally deny it, go to `System Settings > Privacy & Security > Camera` to enable access.

7.  **(Planned) Raspberry Pi Setup:**
    - When Raspberry Pi support is implemented, you will need to enable the camera interface using `sudo raspi-config` under `Interface Options`.
    - The `picamera2` library and its dependencies will also need to be installed (instructions will be added later).

## Usage

Run the script from the project's root directory using `python main.py`.

**Basic Example (Capture 50 images, 5 seconds apart):**

```bash
python main.py -l 50 -i 5 -o my_timelapse_pics
```

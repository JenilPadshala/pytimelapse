"""
Camera Abstraction Layer for PyTimeLapse.

Defines a base structure and placeholder implementations for different camera systems.
"""

import os
import cv2
import time

class CameraError(Exception):
    """Custom exception for camera-related errors."""
    pass

class CameraBase:
    """Base class for camera implementations."""
    def __init__(self, config=None):
        """Initialize with optional configuration."""
        self.config = config if config else {}
        print(f"{self.__class__.__name__}: Base init")
    
    def initialize(self):
        """Set up the camera hardware/connection."""
        print(f"{self.__class__.__name__}: Base initialize (Not implemented)")
    
    def capture_image(self, filepath):
        """Capture a single image and save it to the specified path."""
        print(f"{self.__class__.__name__}: Base capture_image to {filepath} (Not implemented)")
    
    def shutdown(self):
        """Release camera resources cleanly."""
        print(f"{self.__class__.__name__}: Base shutdown (Not implemented)")
    
    def __enter__(self):
        """Context manager entry: initialize the camera."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit: shutdown the camera."""
        self.shutdown()

class MacCamera(CameraBase):
    """Placeholder implementation for macOS camera (using OpenCV later)."""
    def __init__(self, config=None):
        super().__init__(config)
        self.camera_index = self.config.get('camera_index', 0)
        self.resolution = self.config.get('resolution', None)
        self.capture = None
        print(f"MacCamera: Configured for index {self.camera_index}, resolution {self.resolution or 'default'}")
    
    def initialize(self):
        print("MacCamera: Initializing cv2.VideoCapture({self.camera_index})")
        try:
            self.capture = cv2.VideoCapture(self.camera_index)
            if not self.capture.isOpened():
                time.sleep(0.5)
                self.capture.release()
                self.capture = cv2.VideoCapture(self.camera_index)
                if not self.capture.isOpened():
                    raise CameraError(f"Cannot open camera at index {self.camera_index}")
            
            #set resolution if specified
            if self.resolution and len(self.resolution) == 2:
                width, height = self.resolution
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                # verify if resolution was set
                actual_width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
                actual_height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print(f"MacCamera: Requested resolution {width}x{height}, Actual: {int(actual_width)}x{int(actual_height)}")
            
            # --- Add warm-up delay and frame discard ---
            print("MacCamera: Warming up camera (allowing time for auto-exposure)...")
            warm_up_time = 2.0
            discard_frames = 5
            start_time = time.time()
            frame_count = 0
            while time.time() - start_time < warm_up_time:
                ret, _ = self.capture.read()
                frame_count += 1
                if not ret:
                    print("MacCamera: Warning - Frame drop during warm-up.")
                time.sleep(0.01)
            print(f"MacCamera: Warm-up complete. Read {frame_count} frames in {time.time() - start_time:.2f} seconds.")
            # --- End warm-up delay ---    
            print(f"MacCamera: Camera {self.camera_index} initialized successfully.")

        except Exception as e:
            # clean up if initialization fails
            if self.capture:
                self.capture.release()
            self.capture = None
            raise CameraError(f"Failed during MacCamera initialization: {e}") from e
        
    
    def capture_image(self, filepath):
        if not self.capture or not self.capture.isOpened():
            raise CameraError("MacCamera is not initialized or has been shut down.")
        print(f"MacCamera: Reading frame from camera {self.camera_index}...")

        ret, frame = self.capture.read()
        if not ret or frame is None:
            raise CameraError("Failed to capture image from camera {self.camera_index}.")
        
        print(f"MacCamera: Saving frame to {filepath}...")
        try:
            output_dir = os.path.dirname(filepath)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            success = cv2.imwrite(filepath, frame)
            if not success:
                raise CameraError(f"Failed to save image to {filepath} (cv2.imwrite returned false).")
            print(f"MacCamera: Image saved successfully to {filepath}.")
            return True
        except Exception as e:
            raise CameraError(f"Error saving image to {filepath}: {e}") from e
        
    def shutdown(self):
        if self.capture and self.capture.isOpened():
            print(f"MacCamera: Releasing camera {self.camera_index}...")
            self.capture.release()
            print(f"MacCamera: Camera {self.camera_index} released.")
        else:
            print(f"MacCamera: Shutdown called, but camera {self.camera_index} was not active.")
        self.capture = None

class PiCamera(CameraBase):
    """Placeholder implementation for Raspberry Pi camera."""
    def __init__(self, config=None):
        super().__init__(config)
        print("PiCamera: Initialized (Placeholder)")
    
    def initialize(self):
        print("PiCamera: Setting up Raspberry Pi camera... (Placeholder)")
        return True
    
    def capture_image(self, filepath):
        print(f"PiCamera: Capturing image to {filepath}... (Placeholder)")
        # Placeholder for actual image capture logic
        return True
    
    def shutdown(self):
        print("PiCamera: Shutting down Raspberry Pi camera... (Placeholder)")


def get_camera(os_type="auto", config=None):
    """Factory function to get the appropriate camera class based on the OS."""
    if os_type == "auto":
        import sys
        platform = sys.platform
        if platform == "darwin":
            os_type = "macos"
        elif platform.startswith("linux"):
            os_type = "linux"
        else:
            raise CameraError(f"Unsupported OS for camera detection: {platform}")
    
    if os_type == "macos":
        print("Selecting MacCamera implementation.")
        return MacCamera(config)
    elif os_type == "linux":
        print("Selecting PiCamera implementation.")
        return PiCamera(config)
    else:
        raise ValueError(f"Invalid os_type specified: {os_type}. Supported types are 'macos' and 'linux'.")

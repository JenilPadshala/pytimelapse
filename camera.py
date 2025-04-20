"""
Camera Abstraction Layer for PyTimeLapse.

Defines a base structure and placeholder implementations for different camera systems.
"""

import os

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
        print("MacCamera: Initialized (Placeholder)")
    
    def initialize(self):
        print("MacCamera: Setting up webcam... (Placeholder)")
        return True
    
    def capture_image(self, filepath):
        print(f"MacCamera: Capturing image to {filepath}... (Placeholder)")
        return True
        
    def shutdown(self):
        print("MacCamera: Shutting down webcam... (Placeholder)")

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

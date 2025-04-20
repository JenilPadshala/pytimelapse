import sys
import pytest
from unittest import mock

import os

from main import get_operating_system, parse_arguments

@pytest.mark.parametrize(
    "platform_string, expected_os",
    [
        ("darwin", "macos"),
        ("linux", "linux"),
        ("win32", "unsupported"),
        ("linux2", "linux"),
        ("cygwin", "unsupported"),
        ("freebsd11", "unsupported"),
    ],
)
def test_get_operating_system(platform_string, expected_os):
    """Test the get_operating_system function with different platform strings."""

    with mock.patch.object(sys, "platform", platform_string):
        assert get_operating_system() == expected_os


# --- Test parse_arguments function ---

# Test default arguments
def test_parse_arguments_defaults(monkeypatch):
    """ Test if default arguments are parsed correctly. """
    monkeypatch.setattr(sys, "argv", ["main.py"])
    args = parse_arguments()
    assert args.interval == 10.0
    assert args.output == "timelapse_output"
    assert args.limit == 0

# Test custom arguments
def test_parse_arguments_custom(monkeypatch):
    """ Test if custom arguments are parsed correctly. """
    test_argv = [
        'main.py',
        '--interval', '5.5',
        '--output', 'my_images',
        '--limit', '100'
    ]
    monkeypatch.setattr(sys, "argv", test_argv)
    args = parse_arguments()
    assert args.interval == 5.5
    assert args.output == "my_images"
    assert args.limit == 100

# Test short options
def test_parse_arguments_short(monkeypatch):
    """ Test if short options are parsed correctly. """

    test_argv = [
        'main.py',
        '-i', '2.5',
        '-o', 'short_output',
        '-l', '50'
    ]
    monkeypatch.setattr(sys, "argv", test_argv)
    args = parse_arguments()
    assert args.interval == 2.5
    assert args.output == "short_output"
    assert args.limit == 50

# Test invalid arguments
def test_parse_arguments_invalid_type(monkeypatch):
    """ Test if invalid arguments raise an error. """
    test_argv = ['main.py', '--interval', 'not_a_number']
    monkeypatch.setattr(sys, "argv", test_argv)
    with pytest.raises(SystemExit):
        parse_arguments()


# --- Tests for camera selection ---

from unittest.mock import patch, MagicMock
from camera import get_camera, MacCamera, PiCamera, CameraError

@patch('main.get_operating_system', return_value='macos')
@patch('main.get_camera') # Mock the factory function *where it's used* in main
def test_main_uses_correct_camera_on_macos(mock_get_camera, mock_get_os, monkeypatch):
    """Test if main gets and uses the correct camera instance on macOS."""
    monkeypatch.setattr(sys, 'argv', ['main.py', '-l', '1'])

    # Create a mock camera instance that get_camera will return
    mock_camera_instance = MagicMock(spec=MacCamera) # Use spec for better mocking

    # Configure get_camera mock to return our instance
    mock_get_camera.return_value = mock_camera_instance

    # Configure the __enter__ on our instance to return itself
    mock_camera_instance.__enter__.return_value = mock_camera_instance

    with patch('os.makedirs', return_value=None), \
         patch('time.sleep', return_value=None):
        # No reload should be needed if we import main late or patch correctly
        from main import main
        main()

    # Assertions
    mock_get_os.assert_called_once() # Was OS checked?
    # Was get_camera called with the correct OS type?
    mock_get_camera.assert_called_once_with(os_type='macos', config={})
    # Was the context manager used on our instance?
    mock_camera_instance.__enter__.assert_called_once()
    # Was capture called on our instance?
    mock_camera_instance.capture_image.assert_called_once()
    # Was the context manager exited (implying shutdown would be called in real code)?
    mock_camera_instance.__exit__.assert_called_once()


@patch('main.get_operating_system', return_value='linux')
@patch('main.get_camera') # Mock the factory function in main
def test_main_uses_correct_camera_on_linux(mock_get_camera, mock_get_os, monkeypatch):
    """Test if main gets and uses the correct camera instance on Linux."""
    monkeypatch.setattr(sys, 'argv', ['main.py', '-l', '1'])

    # Create a mock camera instance get_camera will return
    mock_camera_instance = MagicMock(spec=PiCamera) # Use spec for better mocking

    # Configure get_camera mock
    mock_get_camera.return_value = mock_camera_instance

    # Configure __enter__ on our instance
    mock_camera_instance.__enter__.return_value = mock_camera_instance

    with patch('os.makedirs', return_value=None), \
         patch('time.sleep', return_value=None):
        from main import main
        main()

    # Assertions
    mock_get_os.assert_called_once()
    # Was get_camera called correctly?
    mock_get_camera.assert_called_once_with(os_type='linux', config={})
    # Check context manager and capture call
    mock_camera_instance.__enter__.assert_called_once()
    mock_camera_instance.capture_image.assert_called_once()
    mock_camera_instance.__exit__.assert_called_once()


# Test for unsupported OS (this one should be mostly correct already)
@patch('main.get_operating_system', return_value='unsupported')
@patch('main.get_camera') # Also mock get_camera here
def test_main_exits_on_unsupported_os(mock_get_camera, mock_get_os, monkeypatch):
    """Test if main exits cleanly on unsupported OS."""
    monkeypatch.setattr(sys, 'argv', ['main.py'])

    with pytest.raises(SystemExit) as e:
         # Import late to ensure mocks are active
         from main import main
         main()

    assert e.value.code == 1 # Check exit code
    mock_get_os.assert_called_once() # OS check should still happen
    mock_get_camera.assert_not_called() # Ensure we didn't try to get a camera

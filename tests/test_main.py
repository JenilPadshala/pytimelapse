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


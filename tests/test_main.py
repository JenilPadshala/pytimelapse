import sys
import pytest
from unittest import mock

import os

from main import get_operating_system

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
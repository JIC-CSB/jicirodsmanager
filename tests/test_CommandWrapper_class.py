"""Test the CommandWrapper class."""

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import pytest


def test_initialisation():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper([])
    assert callable(cmd)


def test_cmd_when_successful():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper(["ls"])

    # Mock stuff.
    cmd.success = MagicMock(return_value=True)

    # Run stuff.
    cmd()

    # Assert stuff.
    cmd.success.assert_called_once_with()


def test_cmd_when_not_successful():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper(["ls"])

    # Mock stuff.
    cmd.success = MagicMock(return_value=False)

    # Run stuff. Here we need to catch and ignore the RuntimeError
    # generated as a consequence of cmd.success() returning False.
    with pytest.raises(RuntimeError):
        cmd()


def test_cmd_raises_when_invoked_with_command_not_in_path():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper(["rubbish"])

    # Run stuff.
    with pytest.raises(RuntimeError):
        cmd()

"""Test the CommandWrapper class."""

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import pytest


def test_initialisation():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper()
    assert callable(cmd)


def test_cmd_when_successful():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper()

    # Mock stuff.
    cmd.success = MagicMock(return_value=True)
    cmd.process_stdout = MagicMock()
    cmd.process_stderr = MagicMock()

    # Run stuff.
    cmd(["ls"])

    # Assert stuff.
    cmd.success.assert_called_once_with()
    cmd.process_stdout.assert_called_once_with()
    cmd.process_stderr.assert_not_called()


def test_cmd_when_not_successful():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper()

    # Mock stuff.
    cmd.success = MagicMock(return_value=False)
    cmd.process_stdout = MagicMock()
    cmd.process_stderr = MagicMock()

    # Run stuff. Here we need to catch and ignore the RuntimeError
    # generated as a consequence of cmd.success() returning False.
    try:
        cmd(["ls"])
    except RuntimeError:
        pass

    # Assert stuff.
    cmd.success.assert_called_once_with()
    cmd.process_stdout.assert_not_called()
    cmd.process_stderr.assert_called_once_with()


def test_cmd_raises_when_invoked_with_command_not_in_path():
    from jicirodsmanager import CommandWrapper
    cmd = CommandWrapper()

    # Run stuff.
    with pytest.raises(RuntimeError):
        cmd(["rubbish"])

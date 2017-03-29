"""Test the wrapping of iRODS commnads."""

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_group_exists():
    from jicirodsmanager.irods import GroupExists
    group_exists = GroupExists()

    # Mock stuff.
    group_exists._call_cmd_line = MagicMock()
    group_exists.stdout = MagicMock(return_value="public\nrodsadmin\n")
    group_exists.stderr = MagicMock(return_value="")
    group_exists.returncode = MagicMock(return_value=0)

    assert group_exists("rodsadmin")
    assert not group_exists("rg-matthew-hartley")

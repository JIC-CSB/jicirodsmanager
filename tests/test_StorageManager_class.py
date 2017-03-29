"""Test the storage manager class."""

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_initialisation():

    from jicirodsmanager import StorageManager
    storage_manager = StorageManager()

    # These are the public methods.
    assert callable(storage_manager.group_exists)
    assert callable(storage_manager.add_user)
    assert callable(storage_manager.add_group)


def test_add_user():
    from jicirodsmanager import StorageManager
    storage_manager = StorageManager()

    # Mock stuff.
    storage_manager.group_exists = MagicMock(return_value=True)
    storage_manager.create_user = MagicMock(return_value=True)
    storage_manager.add_user_to_group = MagicMock()

    # Run command.
    storage_manager.add_user("olssont", "rg-matthew-hartley")

    # Assert stuff.
    storage_manager.group_exists.assert_called_once_with("rg-matthew-hartley")
    storage_manager.create_user.assert_called_once_with("olssont")
    storage_manager.add_user_to_group.assert_called_once_with(
        "olssont", "rg-matthew-hartley")


def test_add_user_when_group_does_not_exist():
    from jicirodsmanager import StorageManager
    storage_manager = StorageManager()

    # Mock stuff.
    storage_manager.group_exists = MagicMock(return_value=False)
    storage_manager.create_user = MagicMock(return_value=True)
    storage_manager.add_user_to_group = MagicMock()

    # Run command.
    storage_manager.add_user("olssont", "rg-matthew-hartley")

    # Assert stuff.
    storage_manager.group_exists.assert_called_once_with("rg-matthew-hartley")
    storage_manager.create_user.assert_not_called()
    storage_manager.add_user_to_group.assert_not_called()


def test_only_try_to_add_user_to_group_if_user_creation_was_successful():
    from jicirodsmanager import StorageManager
    storage_manager = StorageManager()

    # Mock stuff.
    storage_manager.group_exists = MagicMock(return_value=True)
    storage_manager.create_user = MagicMock(return_value=False)
    storage_manager.add_user_to_group = MagicMock()

    # Run command.
    storage_manager.add_user("olssont", "rg-matthew-hartley")

    # Assert stuff.
    storage_manager.group_exists.assert_called_once_with("rg-matthew-hartley")
    storage_manager.create_user.assert_called_once_with("olssont")
    storage_manager.add_user_to_group.assert_not_called()


def test_add_group_no_quota():
    from jicirodsmanager import StorageManager
    storage_manager = StorageManager()

    # Mock stuff.
    storage_manager.create_group_with_quota = MagicMock()
    storage_manager.create_group_without_quota = MagicMock()

    # Run command.
    storage_manager.add_group("rg-matthew-hartley")

    # Assert stuff.
    storage_manager.create_group_without_quota.assert_called_once_with(
        "rg-matthew-hartley")
    storage_manager.create_group_with_quota.assert_not_called()


def test_add_group_with_quota():
    from jicirodsmanager import StorageManager
    storage_manager = StorageManager()

    # Mock stuff.
    storage_manager.create_group_with_quota = MagicMock()
    storage_manager.create_group_without_quota = MagicMock()

    # Run command.
    storage_manager.add_group("rg-matthew-hartley", 500)

    # Assert stuff.
    storage_manager.create_group_without_quota.assert_not_called()
    storage_manager.create_group_with_quota.assert_called_once_with(
        "rg-matthew-hartley", 500)

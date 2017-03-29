"""Module for storing irods specific code."""

import logging

from jicirodsmanager import StorageManager, CommandWrapper

logger = logging.getLogger(__name__)


def string_to_list(s):
    """Return a list of items.

    :param s: string with white space separated items
    :returns: list of items
    """
    return s.strip().split()


def nbi_zone_user_name(user_name):
    "Return nbi zone user name."""
    return "{}#nbi".format(user_name)


class IrodsStorageManager(StorageManager):
    """Class for adding users/groups/namespaces to an irods storage system."""

    command_prefix = "irods"

    def group_exists(self, group_name):
        """Return true if the group exists."""
        logger.info("Calling group exists")
        lg = CommandWrapper(["iadmin", "lg"])
        groups = string_to_list(lg())
        return group_name in groups

    def create_group_without_quota(self, group_name):
        """Add the group without setting a quota."""
        logger.info("Calling create_group_without_quota")
        mkgroup = CommandWrapper(["iadmin", "mkgroup", group_name])
        mkgroup()
        if mkgroup.returncode == 0:
            collection = "/{}".format(group_name)
            imkdir = CommandWrapper(
                ["imkdir", collection])
            imkdir()
            if imkdir.returncode == 0:
                ichmod_own = CommandWrapper(
                    ["ichmod", "own", group_name, collection])
                ichmod_own()
                ichmod_inherit = CommandWrapper(
                    ["ichmod", "inherit", collection])
                ichmod_inherit()
        return mkgroup.returncode == 0

    def create_group_with_quota(self, group_name, quota):
        """Add the group and set quota."""
        logger.info("Calling create_group_with_quota")
        created = self.create_group_without_quota(group_name)
        if created:
            sgq = CommandWrapper(
                ["iadmin", "sgq, group_name", "total", quota])
            sgq()

    def create_user(self, user_name):
        """Create the user and return True if successful."""
        logger.info("Calling create_user")
        mkuser = CommandWrapper(
            ["iadmin", "mkuser", nbi_zone_user_name(user_name)])
        mkuser()
        return mkuser.returncode == 0

    def add_user_to_group(self, user_name, group_name):
        """Add the user to the group."""
        logger.info("Calling add_user_to_group")
        atg = CommandWrapper(
            ["iadmin", "atg", group_name, nbi_zone_user_name(user_name)])
        atg()

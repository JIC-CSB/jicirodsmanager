"""Module for storing irods specific code."""

import os
import sys
import json
import base64
import logging
import requests

from jicirodsmanager import StorageManager, CommandWrapper

logger = logging.getLogger(__name__)


def string_to_list(s):
    """Return a list of items.

    :param s: string with white space separated items
    :returns: list of items
    """
    return s.strip().split()


def get_research_groups():

    consul_url = "http://consul.scicomp.jic.ac.uk/v1/kv/research-groups"

    response = requests.get(consul_url)

    encoded_group_string = json.loads(response.content)[0]['Value']

    group_list_string = base64.b64decode(encoded_group_string)

    group_list = json.loads(group_list_string)

    return [s.lower() for s in group_list]


def is_valid_research_group(group_name):

    return group_name in get_research_groups()


def irods_zone_collection_name(group_name):
    """Return iRODS collection name derived from group_name including working
    out the iRODS zone."""

    irods_envfile = os.path.expanduser('~/.irods/irods_environment.json')
    irods_zone_name = json.load(open(irods_envfile))['irods_zone_name']

    return "/{}/{}".format(irods_zone_name, group_name)


def nbi_zone_user_name(user_name):
    """Return nbi zone user name."""
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

        if not is_valid_research_group(group_name):
            err = "Group {} does not exist in consul.".format(group_name)
            logger.warning(err)
            sys.stderr.write(err + '\n')
            sys.exit(2)

        mkgroup = CommandWrapper(["iadmin", "mkgroup", group_name])
        mkgroup()
        if mkgroup.returncode == 0:
            collection = irods_zone_collection_name(group_name)
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
        return mkgroup.success()

    def create_group_with_quota(self, group_name, quota):
        """Add the group and set quota."""
        logger.info("Calling create_group_with_quota")
        created = self.create_group_without_quota(group_name)
        if created:
            sgq = CommandWrapper(
                ["iadmin", "sgq", group_name, "total", quota])
            sgq()

    def create_user(self, user_name):
        """Create the user. Do not exit if command fails."""
        logger.info("Calling create_user")
        mkuser = CommandWrapper(
            ["iadmin", "mkuser", nbi_zone_user_name(user_name), "rodsuser"])
        mkuser(exit_on_failure=False)

    def add_user_to_group(self, user_name, group_name):
        """Add the user to the group."""
        logger.info("Calling add_user_to_group")
        atg = CommandWrapper(
            ["iadmin", "atg", group_name, nbi_zone_user_name(user_name)])
        atg()

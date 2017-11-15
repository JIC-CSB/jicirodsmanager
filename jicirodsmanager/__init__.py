"""jicirodsmanager package."""

import logging
import sys
from subprocess import Popen, PIPE

__version__ = "1.0.0"

logger = logging.getLogger(__name__)


class CommandWrapper(object):
    """Class for creating API calls from command line tools."""

    def __init__(self, args):
        self.args = args

    def success(self):
        """Return True if the command line tool was run successfully."""
        return self.returncode == 0

# Useful helper functions

    def _call_cmd_line(self):
        """Run the command line tool."""
        try:
            logging.info("Calling Popen with: {}".format(self.args))
            p = Popen(self.args, stdout=PIPE, stderr=PIPE)
        except OSError:
            raise(RuntimeError("No such command found in PATH"))

        self.stdout, self.stderr = p.communicate()
        self.stdout = self.stdout.decode("utf-8")
        self.stderr = self.stderr.decode("utf-8")
        self.returncode = p.returncode

# Interface API.

    def __call__(self, exit_on_failure=True):
        """Return wrapped stdout or raise if stderr is not empty."""
        self._call_cmd_line()
        if self.success():
            return self.stdout
        else:
            logger.warning("Command failed: {}".format(self.args))
            logger.warning(self.stderr)
            sys.stderr.write(self.stderr)

            if exit_on_failure:
                sys.exit(self.returncode)


class StorageManager(object):
    """Class for adding users/groups/namespaces/quotas to a storage system."""

# Class variable and methods that need to be overridden by subclasses.

    command_prefix = "default"

    def group_exists(self, group_name):
        """Return true if the group exists."""

    def create_group_without_quota(self, group_name):
        """Add the group without setting a quota."""

    def create_group_with_quota(self, group_name, quota):
        """Add the group and set quota."""

    def create_project_without_quota(self, project_name):
        """Add the project without setting a quota."""

    def create_project_with_quota(self, project_name, quota):
        """Add the project and set quota."""

    def create_user(self, user_name):
        """Create the user."""

    def add_user_to_group(self, user_name, group_name):
        """Create the user."""


# Command line interface API.

    def add_user(self, user_name, group_name):
        """Add the user to the storage system."""
        if not self.group_exists(group_name):
            print("The group {} does not exist.".format(group_name))
            print("Please create it using the {}-groupadd command.".format(
                self.command_prefix))
            return

        # At this point the group should exist.
        self.create_user(user_name)
        # The previous command might have failed if the user exists
        # We'll try adding them anyway
        self.add_user_to_group(user_name, group_name)

    def add_group(self, group_name, quota=None):
        """Add the group to the storage system."""
        if quota is None:
            return self.create_group_without_quota(group_name)
        return self.create_group_with_quota(group_name, quota)

    def add_project(self, project_name, quota=None):
        """Add the project to the storage system."""
        if quota is None:
            return self.create_project_without_quota(project_name)
        return self.create_project_with_quota(project_name, quota)

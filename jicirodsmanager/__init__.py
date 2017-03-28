"""jicirodsmanager package."""

from subprocess import Popen, PIPE

__version__ = "0.1.0"


class CommandWrapper(object):
    """Class for creating API calls from command line tools."""

# Class variable and methods that need to be overridden by subclasses.

    def process_stdout(self):
        """Return the desired output of the wrapped command line tool."""
        return self.stdout

    def process_stderr(self):
        """Return a useful error message."""
        return self.stderr

    def success(self):
        """Return True if the command line tool was run successfully."""
        if self.returncode == 0:
            return True
        else:
            return False

# Useful helper functions

    def _call_cmd_line(self, args):
        """Run the command line tool."""
        try:
            p = Popen(args, stdout=PIPE, stderr=PIPE)
        except OSError:
            raise(RuntimeError("No such command found in PATH"))

        self.stdout, self.stderr = p.communicate()
        self.returncode = p.returncode

# Interface API.

    def __call__(self, args):
        """Return wrapped stdout or raise if stderr is not empty."""
        self._call_cmd_line(args)
        if self.success():
            return self.process_stdout()
        else:
            raise(RuntimeError(self.process_stderr()))


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

    def create_user(self, user_name):
        """Create the user and return True if successful."""

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
        # If we manage to create the user we add it to the group.
        if self.create_user(user_name):
            self.add_user_to_group(user_name, group_name)

    def add_group(self, group_name, quota=None):
        """Add the group to the storage system."""
        if quota is None:
            return self.create_group_without_quota(group_name)
        return self.create_group_with_quota(group_name, quota)

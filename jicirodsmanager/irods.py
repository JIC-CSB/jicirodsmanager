"""Module for storing irods specific code."""

from jicirodsmanager import CommandWrapper


class GroupExists(CommandWrapper):
    """Callable class to find out if a group exists in current irods zone."""

    cmd = ["iadmin", "lg"]

    def process_stdout(self, *args, **kwargs):
        try:
            group_name = kwargs["group_name"]
        except KeyError:
            group_name = args[0]
        groups = self.stdout().strip().split()
        return group_name in groups


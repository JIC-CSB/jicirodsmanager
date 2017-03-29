"""Manger iRODS storage."""

import argparse
import logging

from jicirodsmanager.irods import IrodsStorageManager

root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

root.addHandler(handler)


def adduser(args):
    root.info("Calling adduser")
    storage_manager = IrodsStorageManager()
    storage_manager.add_user(args.user_name, args.group_name)

def addgroup(args):
    root.info("Calling addgroup")
    storage_manager = IrodsStorageManager()
    storage_manager.add_group(args.group_name, args.quota)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers()

    user = subparsers.add_parser("adduser")
    user.add_argument("user_name")
    user.add_argument("group_name")
    user.set_defaults(func=adduser)

    group = subparsers.add_parser("addgroup")
    group.add_argument("group_name")
    group.add_argument("-q", "--quota", type=int, default=None)
    group.set_defaults(func=addgroup)

    args = parser.parse_args()

    # Run it!
    args.func(args)

if __name__ == "__main__":
    main()

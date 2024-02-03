#! /usr/bin/python3

import importlib

from argparse import ArgumentParser
from os import path


ROOT_DIR = path.dirname(__file__)


def set_subapp_command(parser: ArgumentParser):
    parser.add_argument(
        "name",
        type=str,
        help="name of the subapp"
    )
    parser.add_argument(
        "-m", "--main-subapp",
        type=str,
        default="site",
        help="name of the main subapp, used for importing stuffs under it"
    )
    parser.add_argument(
        "--route",
        type=str,
        help="route of the subapp"
    )


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
    )
    set_subapp_command(subparsers.add_parser(
        name="subapp",
        help="create a new subapp",
    ))
    subparsers.add_parser(
        name="rm-cache",
        help="remove cache files",
    )

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    command = args.command.replace("-", "_")
    command_args = args.__dict__
    del command_args["command"]

    module = importlib.import_module(f"app.manager")
    if hasattr(module, command) and callable(getattr(module, command)):
        getattr(module, command)(**command_args, root_dir=ROOT_DIR)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

#! /usr/bin/python3

from os import path, environ

from main import autoloader


# Set the NO_LOAD_SUBAPPS environment variable to 1 to prevent subapps
# from being loaded.
environ.setdefault("AUTOLOADER_MANAGER_MODE", "1")


ROOT_DIR = path.dirname(__file__)


def main():
    parser, action_dict = autoloader.get_parser()

    args = parser.parse_args()

    if not hasattr(args, "command") or getattr(args, "command") is None:
        parser.print_help()
        return

    command = args.command
    command_args = args.__dict__
    del command_args["command"]
    action_dict[command](**command_args, root_dir=ROOT_DIR)

if __name__ == "__main__":
    main()

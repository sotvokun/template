import os
import importlib
import logging

from argparse import ArgumentParser
from enum import Enum
from types import ModuleType
from typing import Callable, Optional, TypedDict, Unpack, Any
from fastapi import FastAPI, APIRouter

from app.manager import APIManager, Command


ENV_AUTOLOADER_MANAGER_MODE = "AUTOLOADER_MANAGER_MODE"


_autoloader_instance: Optional["Autoloader"] = None


class AutoloaderOptions(TypedDict):
    main_subapp: str


class Autoloader:

    class Module(Enum):
        route = "route"
        event = "event"
        command = "command"

    class _LoggerFormatter(logging.Formatter):
        _format = "%(levelname)s: [%(name)s] %(message)s"
        _reset = "\x1b[0m"
        _red = "\x1b[31m"
        _green = "\x1b[32m"
        _yellow = "\x1b[33m"
        _grey = "\x1b[90m"
        _bold_red = "\x1b[1;31m"
        _light_gray = "\x1b[37m"
        _format = "[%(name)s] %(levelname)-17s %(message)s"

        COLORS = {
            logging.DEBUG: _grey,
            logging.INFO: _green,
            logging.WARNING: _yellow,
            logging.ERROR: _red,
            logging.CRITICAL: _bold_red,
        }

        def format(self, record: logging.LogRecord) -> str:
            color = self.COLORS.get(record.levelno, self._reset)
            record.levelname = f"{color}{record.levelname}{self._reset}" + ":"
            record.name = f"{self._light_gray}{record.name}{self._reset}"
            formatter = logging.Formatter(self._format)
            return formatter.format(record)

    options: AutoloaderOptions = {
        "main_subapp": "site"
    }

    load_modules: list[Module] = [
        Module.route,
        Module.event
    ]

    @staticmethod
    def module_name(subapp: str, module: Optional[str]) -> str:
        """
        Returns the module (Python package) name of a subapp.
        """
        return f"app.{subapp}" + (f".{module}" if module else "")

    def import_module(self, subapp: str, module: str) -> ModuleType:
        """
        Imports a subapp module (Python package).
        """
        return importlib.import_module(self.module_name(subapp, module))

    def config(self, name: str, default: Any = None):
        """
        Returns a config value from the main subapp.
        """
        main_subapp = self.options["main_subapp"]
        try:
            config_module = self.import_module(main_subapp, "config")
            return getattr(config_module, name, default)
        except ModuleNotFoundError:
            raise RuntimeError(
                f"No `config.py` found in the main subapp: {main_subapp}")

    def _initialize_logger(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(Autoloader._LoggerFormatter())
        self.logger = logging.getLogger("Autoload")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)

    def __init__(self, main: FastAPI, /, **options: Unpack[AutoloaderOptions]):
        global _autoloader_instance

        self._initialize_logger()

        self.manager_mode = os.environ.get(ENV_AUTOLOADER_MANAGER_MODE, 0)
        self.loaded_managers = []
        self.main = main
        self.options.update(options)

        _autoloader_instance = self

        load_modules = [
            Autoloader.Module.route,
            Autoloader.Module.event
        ] if self.manager_mode else [
            Autoloader.Module.command
        ]

        self.load_subapp(self.options["main_subapp"], load_modules)

        installed_subapps = self.config("INSTALLED_SUBAPPS", [])
        for subapp in installed_subapps:
            if subapp == self.options["main_subapp"]:
                continue
            self.load_subapp(subapp, load_modules)

    def load_subapp(self, subapp: str, modules: list[Module] = []):
        """
        Loads a subapp.
        """
        if self.manager_mode and self.loaded_managers is None:
            self.loaded_managers = []
        for module in modules:
            match module:
                case Autoloader.Module.route:
                    self.load_subapp_route(subapp)
                case Autoloader.Module.event:
                    self.load_subapp_event(subapp)
                case Autoloader.Module.command:
                    manager = self.load_subapp_command(subapp)
                    if manager:
                        self.loaded_managers.append(manager)

    def load_subapp_route(self, subapp: str):
        """
        Loads a subapp route.
        """
        module = Autoloader.Module.route.value
        module_name = self.module_name(subapp, module)
        try:
            route_module = self.import_module(subapp, module)
        except ModuleNotFoundError:
            self.logger.info(
                f"SKIPPING. Module '{module_name}' not found in subapp: {subapp}.")
            return

        entry_point = "router"
        if not hasattr(route_module, entry_point):
            self.logger.error(f"Module '{module_name}' in subapp '{
                              subapp}' has no {entry_point}")
            return

        router = getattr(route_module, entry_point)
        if not isinstance(router, APIRouter):
            self.logger.error(
                f"'{module_name}.{entry_point}' in subapp '{subapp}' expect: 'fastapi.APIRouter', got: {type(router)}")
            return

        self.main.include_router(route_module.router)

    def load_subapp_event(self, subapp: str):
        """
        Loads and registers a subapp event.
        """
        module = Autoloader.Module.event.value
        module_name = self.module_name(subapp, module)
        try:
            event_module = self.import_module(subapp, module)
        except ModuleNotFoundError:
            self.logger.info(
                f"SKIPPING. Module '{module_name}' not found in subapp: {subapp}.")
            return

        ON_INSTALL = "on_install"
        if hasattr(event_module, ON_INSTALL) and callable(
                getattr(event_module, ON_INSTALL)):
            event_module.on_install(self.main)

        ON_STARTUP = "on_startup"
        if hasattr(event_module, ON_STARTUP) and callable(
                getattr(event_module, ON_STARTUP)):
            self.main.router.on_startup.append(event_module.on_startup)

        ON_SHUTDOWN = "on_shutdown"
        if hasattr(event_module, ON_SHUTDOWN) and callable(
                getattr(event_module, ON_SHUTDOWN)):
            self.main.router.on_shutdown.append(event_module.on_shutdown)

    def load_subapp_command(self, subapp: str):
        """
        Loads the subapp commands into the manager
        """
        module = Autoloader.Module.command.value
        module_name = self.module_name(subapp, module)
        try:
            command_module = self.import_module(subapp, module)
        except ModuleNotFoundError:
            # NOTE silently ignore if a command module is not found
            return None

        entry_point = "manager"
        if not hasattr(command_module, entry_point):
            # NOTE silently ignore if a manager is not found
            return None

        manager = getattr(command_module, entry_point)
        if not isinstance(manager, APIManager):
            self.logger.error(
                f"'{module_name}.{entry_point}' in subapp '{subapp}' expect: 'app.manager.APIManager', got: {type(manager)}")
            return None

        if getattr(manager, "title") is None:
            manager.title = subapp
        return manager

    def get_parser(self) -> tuple[ArgumentParser, dict[str, Callable]]:
        """
        Parses the command line arguments with loaded subapps commands.
        """
        action_dict = {}

        def create_subparser(subparsers, command: Command):
            subparser = subparsers.add_parser(
                command["name"],
                help=command.get("help", None)
            )
            for arg in command["arguments"]:
                subparser.add_argument(
                    *arg.get("name_or_flags", []),
                    type=arg.get("type", str),
                    help=arg.get("help", None),
                    default=arg.get("default", None),
                )
            action_dict[command["name"]] = command["action"]
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(
            title="commands",
            dest="command"
        )
        for manager in self.loaded_managers:
            if len(manager.commands) == 0:
                continue
            for command in manager.commands:
                create_subparser(subparsers, command)
        return parser, action_dict


def get_config(name: str, default: Any = None):
    """
    Returns a config value from the main subapp.
    """
    global _autoloader_instance
    if _autoloader_instance is None:
        raise RuntimeError("Autoloader not initialized")
    return _autoloader_instance.config(name, default)


def import_module(subapp: str, module: str) -> ModuleType:
    """
    Imports a subapp module (Python package).
    """
    global _autoloader_instance
    if _autoloader_instance is None:
        raise RuntimeError("Autoloader not initialized")
    return _autoloader_instance.import_module(subapp, module)


def import_main_module(module: str) -> ModuleType:
    """
    Imports a module from the main subapp.
    """
    return import_module(get_config("main_subapp"), module)

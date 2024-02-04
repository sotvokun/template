import importlib
import logging

from enum import Enum
from types import ModuleType
from typing import Optional, TypedDict, Unpack, Any
from fastapi import FastAPI, APIRouter


class AutoloaderLoggerFormatter(logging.Formatter):
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


class AutoloaderOptions(TypedDict):
    main_subapp: str


class AutoloadModule(Enum):
    route = "route"
    event = "event"


_autoloader_instance: Optional["Autoloader"] = None

class Autoloader:

    options: AutoloaderOptions = {
        "main_subapp": "site"
    }

    load_modules: list[AutoloadModule] = [
        AutoloadModule.route,
        AutoloadModule.event
    ]


    @staticmethod
    def module_name(subapp: str, module: Optional[str]) -> str:
        """
        Returns the module (Python package) name of a subapp.
        """
        return f"app.{subapp}" + (f".{module}" if module else "")


    @staticmethod
    def get_config(name: str, default: Any = None):
        """
        Returns a config value from the main subapp.
        """
        global _autoloader_instance
        if _autoloader_instance is None:
            raise RuntimeError("Autoloader not initialized")
        return _autoloader_instance.config(name, default)


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
            raise RuntimeError(f"No `config.py` found in the main subapp: {main_subapp}")


    def _initialize_logger(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(AutoloaderLoggerFormatter())
        self.logger = logging.getLogger("Autoload")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)


    def __init__(self, main: FastAPI, /, **options: Unpack[AutoloaderOptions]):
        global _autoloader_instance

        self._initialize_logger()

        self.main = main
        self.options.update(options)
        self.load_subapp(self.options["main_subapp"], self.load_modules)

        _autoloader_instance = self

        installed_subapps = self.config("INSTALLED_SUBAPPS", [])
        for subapp in installed_subapps:
            if subapp == self.options["main_subapp"]:
                continue
            self.load_subapp(subapp, self.load_modules)


    def load_subapp(self, subapp: str, modules: list[AutoloadModule] = []):
        """
        Loads a subapp.
        """
        for module in modules:
            match module:
                case AutoloadModule.route:
                    self.load_subapp_route(subapp)
                case AutoloadModule.event:
                    self.load_subapp_event(subapp)


    def load_subapp_route(self, subapp: str):
        """
        Loads a subapp route.
        """
        module_name = self.module_name(subapp, "route")
        try:
            route_module = self.import_module(subapp, "route")
        except ModuleNotFoundError:
            self.logger.info(f"SKIPPING. Module '{module_name}' not found in subapp: {subapp}.")
            return

        if not hasattr(route_module, "router"):
            self.logger.error(f"Module '{module_name}' in subapp '{subapp}' has no router")
            return

        router = getattr(route_module, "router")
        if not isinstance(router, APIRouter):
            self.logger.error(
                f"'{module_name}.router' in subapp '{subapp}' expect: 'fastapi.APIRouter', got: {type(router)}")
            return

        self.main.include_router(route_module.router)


    def load_subapp_event(self, subapp: str):
        """
        Loads and registers a subapp event.
        """
        module_name = self.module_name(subapp, "event")
        try:
            event_module = self.import_module(subapp, "event")
        except ModuleNotFoundError:
            self.logger.info(f"SKIPPING. Module '{module_name}' not found in subapp: {subapp}.")
            return

        ON_INSTALL = "on_install"
        if hasattr(event_module, ON_INSTALL) and callable(getattr(event_module, ON_INSTALL)):
            event_module.on_install(self.main)

        ON_STARTUP = "on_startup"
        if hasattr(event_module, ON_STARTUP) and callable(getattr(event_module, ON_STARTUP)):
            self.main.router.on_startup.append(event_module.on_startup)

        ON_SHUTDOWN = "on_shutdown"
        if hasattr(event_module, ON_SHUTDOWN) and callable(getattr(event_module, ON_SHUTDOWN)):
            self.main.router.on_shutdown.append(event_module.on_shutdown)

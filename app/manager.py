from functools import wraps
from typing import Any, Callable, NotRequired, Optional, TypeAlias, TypedDict


class _Argument(TypedDict):
    name_or_flags: NotRequired[list[str]]
    type: NotRequired[type]
    default: NotRequired[Any]
    help: NotRequired[str]
    required: NotRequired[bool]


Arg: TypeAlias = _Argument


class Command(TypedDict):
    name: str
    help: NotRequired[Optional[str]]
    action: Callable
    arguments: list[_Argument]


class APIManager:
    title: Optional[str]
    help: Optional[str]
    commands: list[Command]

    def __init__(
        self,
        title: Optional[str] = None,
        help: Optional[str] = None
    ):
        self.title = title
        self.help = help
        self.commands = []

    def add_command(
        self,
        name: str,
        help: Optional[str],
        action: Callable,
        arguments: list[_Argument]
    ):
        self.commands.append(
            Command(
                name=name,
                help=help,
                action=action,
                arguments=arguments
            )
        )

    def command(self, **kwargs: Any):
        def decorator(func: Callable):
            @wraps
            def wrapper():
                pass
            self.commands.append(
                Command(
                    name=kwargs.get("_name", func.__name__).replace("_", "-"),
                    help=(kwargs.get("_help", func.__doc__) or "").strip(),
                    action=func,
                    arguments=[
                        Arg(
                            **{
                                **value,
                                "name_or_flags": value.get("name_or_flags", [key])
                            },
                        ) for key, value in dict(
                            filter(
                                lambda pair: not pair[0].startswith("_"),
                                kwargs.items()
                            )
                        ).items()
                    ]
                )
            )
            return wrapper
        return decorator

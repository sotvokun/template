from os import PathLike
from typing import Any, Callable, Optional, Sequence
from fastapi import Request
from fastapi.templating import Jinja2Templates


_templates: Optional[Jinja2Templates] = None


def initialize(
    directory: str | PathLike | Sequence[str | PathLike],
    *,
    context_processors: Optional[list[Callable[[
        Request], dict[str, Any]]]] = None,
    **env_options: Any,
):
    global _templates
    if _templates is not None:
        return
    _templates = Jinja2Templates(
        directory=directory,
        context_processors=context_processors,
        **env_options,
    )


def inject() -> Jinja2Templates:
    global _templates
    if _templates is None:
        raise RuntimeError("Templates not initialized")
    return _templates

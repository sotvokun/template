import os
import shutil

from typing import Optional
from pathlib import Path


def subapp(root_dir: str, name: str, main_subapp: str, route: Optional[str] = None):
    target_path = os.path.join(root_dir, "app", name)
    if os.path.exists(target_path):
        print(f"Subapp '{name}' already exists.")
        return

    def create_file(name: str, content: str|list[str] = ""):
        file_path = os.path.join(target_path, name)
        with open(file_path, "w", encoding="utf-8", newline=os.linesep) as f:
            if isinstance(content, list):
                f.write(os.linesep.join(content))
            else:
                f.write(content)

    os.mkdir(target_path)
    create_file("__init__.py")
    create_file("schema.py", [
        f"from app.{main_subapp}.schema import DataSchema, PaginatedSchema"
    ])
    create_file("model.py", [
        f"from app.{main_subapp}.model import BaseModel"
    ])
    create_file("route.py", [
        f"from fastapi import APIRouter",
        "",
        "",
        (f"router = APIRouter(prefix=\"{route}\")" if route else "router = APIRouter()"),
    ])
    create_file("event.py", [
        "from fastapi import FastAPI",
        "",
        "",
        "def on_startup() -> None:",
        "\tpass",
        "",
        "",
        "def on_shutdown() -> None:",
        "\tpass",
        "",
        "",
        "def on_hook(app: FastAPI) -> None:",
        "\tpass",
        "",
        "",
    ])


def rm_cache(root_dir: str):
    for p in Path(root_dir).rglob("__pycache__"):
        shutil.rmtree(p)

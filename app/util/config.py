from dotenv import load_dotenv
from typing import Optional
from importlib import reload

import app.config


_loaded_dotenv: bool = False


def get(key: str, default: Optional[str] = None) -> Optional[str]:
    global _loaded_dotenv
    if not _loaded_dotenv:
        load_dotenv()
        reload(app.config)
        _loaded_dotenv = True

    parts = key.split('.')
    counter = 0
    obj = None
    for part in parts:
        if counter == 0:
            obj = getattr(app.config, part, None)
        elif type(obj) == dict:
            obj = obj.get(part, None)
        else:
            obj = getattr(obj, part, None)

        if obj is None:
            return default
        counter += 1

    return obj

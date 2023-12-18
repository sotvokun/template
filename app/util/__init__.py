from typing import Any, Optional

import app.config

def config(key: str, default: Optional[str] = None) -> Any:
    parts = key.split(".")
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
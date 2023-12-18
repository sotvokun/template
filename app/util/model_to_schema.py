"""
This module contains a function that converts a SQLAlchemy model into a Pydantic
model(schema).

It is used to fasten the development process by avoiding the need to write
Pydantic models for each SQLAlchemy model.

The code is taken from the following repository:
https://github.com/wezhai/sqlalchemy-to-pydantic
"""

from typing import Container, Optional, Type
from pydantic import BaseModel, ConfigDict, create_model


orm_config = ConfigDict(from_attributes=True)

def model_to_schema(
    db_model: Type,
    *,
    config: Type = orm_config,
    exclude: Container[str] = None,
) -> Type[BaseModel]:
    table = db_model.metadata.tables[db_model.__tablename__]
    fields = {}
    for column in table.columns:
        name = column.name
        if exclude and name in exclude:
            continue
        python_type: Optional[type] = None
        if hasattr(column.type, "impl"):
            if hasattr(column.type.impl, "python_type"):
                python_type = column.type.impl.python_type
        elif hasattr(column.type, "python_type"):
            python_type = column.type.python_type
        else:
            raise TypeError(f"Could not infer python_type for {column}")

        if not column.nullable:
            fields[name] = (python_type, ...)
        else:
            fields[name] = (Optional[python_type], None)

    return create_model(
        db_model.__name__,
        __config__=config,
        **fields,
    )
from pydantic import BaseModel, ConfigDict, Field


schema_config: ConfigDict = {
    "from_attributes": True
}


class BaseSchema(BaseModel):
    __config__ = schema_config


class DataSchema[T](BaseSchema):
    data: T


class PaginatedSchema[T](BaseSchema):
    data: T
    count: int = Field(..., description="Total number of items")
    total: int = Field(..., description="Total number of pages")
    current: int = Field(..., description="Current page number")

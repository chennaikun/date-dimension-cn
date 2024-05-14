from pydantic import BaseModel, Field


class Holiday(BaseModel):
    name: str = Field(...)
    date: str = Field(...)
    is_offday: bool = Field(alias="isOffDay")

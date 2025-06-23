from pydantic import BaseModel, Field


class UserName(BaseModel):
    value: str = Field(min_length=1)

from pydantic import BaseModel, Field


class _Command(BaseModel):
    message: list[str | None]


class _User(BaseModel):
    name: str = Field(..., alias="@name")
    command: _Command


class _SecurityResult(BaseModel):
    user: _User


class _Response(BaseModel):
    security_result: _SecurityResult = Field(..., alias="securityresult")

from typing import Optional

from pydantic import BaseModel, Field


class _Command(BaseModel):
    messages: list[Optional[str]] = Field(..., alias="message")


class _User(BaseModel):
    name: str = Field(..., alias="@name")
    command: _Command


class _SecurityResult(BaseModel):
    user: _User


class _Response(BaseModel):
    security_result: _SecurityResult = Field(..., alias="securityresult")

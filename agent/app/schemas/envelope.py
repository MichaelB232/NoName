"""Standard response envelope (.agents/AGENTS.md §2.A), mirrored from the backend."""

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessEnvelope(BaseModel, Generic[T]):
    success: Literal[True] = True
    data: T
    message: str = "OK"


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[object] = Field(default_factory=list)


class ErrorEnvelope(BaseModel):
    success: Literal[False] = False
    error: ErrorBody

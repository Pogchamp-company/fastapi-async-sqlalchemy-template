from fastapi import status
from pydantic import BaseModel


class BaseActionResponse(BaseModel):
    ok: bool


class ActionResponseWithDetails(BaseActionResponse):
    detail: str


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


base_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": HTTPError,
        "description": "When Authorization is incorrect",
    },
    status.HTTP_403_FORBIDDEN: {
        "model": HTTPError,
        "description": "When user has no required role",
    }
}

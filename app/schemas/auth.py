from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["andersen"])
    password: str = Field(..., min_length=6)

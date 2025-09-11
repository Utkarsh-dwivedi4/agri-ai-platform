from pydantic import BaseModel

class SignupIn(BaseModel):
    name: str | None
    phone: str
    language: str | None = "en"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

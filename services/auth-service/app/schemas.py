from pydantic import BaseModel, constr


class SignupIn(BaseModel):
    name: str | None
    phone: constr(regex=r'^\+?\d{10,15}$')  # Validate phone number format
    language: str | None = "en"


class LoginOTPRequest(BaseModel):
    phone: constr(regex=r'^\+?\d{10,15}$')


class OTPVerifyRequest(BaseModel):
    phone: constr(regex=r'^\+?\d{10,15}$')
    otp: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

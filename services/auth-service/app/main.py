from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import Farmer
from .schemas import SignupIn, Token, LoginOTPRequest, OTPVerifyRequest
from .utils import create_access_token
from .otp_utils import generate_otp, verify_otp
import uvicorn


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/v1/auth/request-otp", status_code=status.HTTP_200_OK)
def request_otp(payload: LoginOTPRequest):
    generate_otp(payload.phone)
    return {"message": "OTP sent (check your phone or logs)"}


@app.post("/v1/auth/verify-otp", response_model=Token)
def verify_otp_and_login(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    if not verify_otp(payload.phone, payload.otp):
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    farmer = db.query(Farmer).filter(Farmer.phone == payload.phone).first()
    if not farmer:
        # Auto-register on first OTP verification
        farmer = Farmer(name=None, phone=payload.phone, language="en")
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
    token = create_access_token({"sub": str(farmer.id), "roles": ["farmer"]})
    return {"access_token": token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

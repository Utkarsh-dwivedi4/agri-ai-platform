from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import Farmer
from .schemas import SignupIn, Token
from .utils import create_access_token
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/v1/auth/signup", response_model=Token)
def signup(payload: SignupIn, db: Session = Depends(get_db)):
    # simple signup, no password (phone-based registration)
    existing = db.query(Farmer).filter(Farmer.phone == payload.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered")
    farmer = Farmer(name=payload.name, phone=payload.phone, language=payload.language or "en")
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    token = create_access_token({"sub": str(farmer.id), "roles": ["farmer"]})
    return {"access_token": token}

@app.post("/v1/auth/login", response_model=Token)
def login(payload: SignupIn, db: Session = Depends(get_db)):
    # For prototype: login by phone (no password). In prod, add OTP.
    farmer = db.query(Farmer).filter(Farmer.phone == payload.phone).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Not found")
    token = create_access_token({"sub": str(farmer.id), "roles": ["farmer"]})
    return {"access_token": token}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import Farmer, Farm
from .schemas import FarmIn, FarmOut
import uvicorn

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Farmer Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# simple auth dependency that reads Authorization header and decodes in production
def get_current_user(authorization: str | None = Header(None)):
    # In this prototype we accept token and treat sub as farmer_id
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth")
    token = authorization.replace("Bearer ", "")
    # naive decode: in production, use jose and verify signature
    # here we just return token for demo
    return token

@app.post("/v1/farms", response_model=FarmOut)
def add_farm(payload: FarmIn, user=Depends(get_current_user), db: Session = Depends(get_db)):
    farmer_id = payload.farmer_id
    farm = Farm(farmer_id=farmer_id, name=payload.name, polygon_json=payload.polygon_json, area_ha=payload.area_ha)
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

@app.get("/v1/farms/{farm_id}")
def get_farm(farm_id: str, db: Session = Depends(get_db)):
    f = db.query(Farm).filter(Farm.id == farm_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Not found")
    return f

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

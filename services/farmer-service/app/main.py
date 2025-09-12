from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import tensorflow as tf
import numpy as np
from PIL import Image

from . import models, schemas
from .db import SessionLocal, engine

app = FastAPI()

# Create database tables (run once)
models.Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load your trained TensorFlow model
model = tf.keras.models.load_model("models/crop_disease_model.h5")

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/inference/upload")
async def predict_crop_disease(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    processed = preprocess_image(image)
    prediction = model.predict(processed)
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = float(np.max(prediction))
    labels = ["Healthy", "Blight", "Rust", "Leaf Spot"]
    result = labels[predicted_class]
    return {"disease": result, "confidence": confidence}

# Soil data endpoint
@app.post("/soil-data/", response_model=schemas.SoilDataOut)
def add_soil_data(data: schemas.SoilDataIn, db: Session = Depends(get_db)):
    db_data = models.SoilData(**data.dict(), recorded_at=datetime.utcnow())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get("/soil-data/{farm_id}", response_model=List[schemas.SoilDataOut])
def get_soil_data(farm_id: str, db: Session = Depends(get_db)):
    return db.query(models.SoilData).filter(models.SoilData.farm_id == farm_id).all()

# Weather forecast endpoint
@app.post("/weather-forecast/", response_model=schemas.WeatherForecastOut)
def add_weather_forecast(data: schemas.WeatherForecastIn, db: Session = Depends(get_db)):
    db_data = models.WeatherForecast(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Market price endpoint
@app.post("/market-price/", response_model=schemas.MarketPriceOut)
def add_market_price(data: schemas.MarketPriceIn, db: Session = Depends(get_db)):
    db_data = models.MarketPrice(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Crop recommendation endpoint (example stub; replace with real ML logic)
@app.post("/crop-recommendation/", response_model=schemas.CropRecommendationOut)
def add_crop_recommendation(data: schemas.CropRecommendationIn, db: Session = Depends(get_db)):
    db_data = models.CropRecommendation(**data.dict(), created_at=datetime.utcnow())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get("/crop-recommendation/{farm_id}", response_model=List[schemas.CropRecommendationOut])
def get_crop_recommendations(farm_id: str, db: Session = Depends(get_db)):
    return db.query(models.CropRecommendation).filter(models.CropRecommendation.farm_id == farm_id).all()

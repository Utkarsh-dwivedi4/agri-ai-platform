from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class FarmIn(BaseModel):
    farmer_id: str
    name: str
    polygon_json: Any
    area_ha: float

class FarmOut(FarmIn):
    id: str

class SoilDataIn(BaseModel):
    farm_id: str
    ph: float
    moisture: float
    nutrient_content: Any  # JSON object

class SoilDataOut(SoilDataIn):
    id: str
    recorded_at: datetime

class WeatherForecastIn(BaseModel):
    farm_id: str
    temperature: float
    rainfall: float
    humidity: float
    forecast_date: datetime

class WeatherForecastOut(WeatherForecastIn):
    id: str

class CropRotationIn(BaseModel):
    farm_id: str
    crop_name: str
    planting_date: datetime
    harvest_date: datetime

class CropRotationOut(CropRotationIn):
    id: str

class MarketPriceIn(BaseModel):
    crop_name: str
    price: float
    date: datetime
    market_location: str

class MarketPriceOut(MarketPriceIn):
    id: str

class CropRecommendationIn(BaseModel):
    farm_id: str
    recommended_crop: str
    predicted_yield: float
    profit_margin: float
    sustainability_score: float

class CropRecommendationOut(CropRecommendationIn):
    id: str
    created_at: datetime

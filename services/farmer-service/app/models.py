from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from .db import Base

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=False)
    language = Column(String, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Farm(Base):
    __tablename__ = "farms"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey('farmers.id'))
    name = Column(String)
    polygon_json = Column(JSON)
    area_ha = Column(Numeric)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SoilData(Base):
    __tablename__ = "soil_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey('farms.id'))
    ph = Column(Numeric)
    moisture = Column(Numeric)
    nutrient_content = Column(JSON)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey('farms.id'))
    temperature = Column(Numeric)
    rainfall = Column(Numeric)
    humidity = Column(Numeric)
    forecast_date = Column(DateTime(timezone=True))

class CropRotation(Base):
    __tablename__ = "crop_rotations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey('farms.id'))
    crop_name = Column(String)
    planting_date = Column(DateTime(timezone=True))
    harvest_date = Column(DateTime(timezone=True))

class MarketPrice(Base):
    __tablename__ = "market_prices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_name = Column(String)
    price = Column(Numeric)
    date = Column(DateTime(timezone=True))
    market_location = Column(String)

class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey('farms.id'))
    recommended_crop = Column(String)
    predicted_yield = Column(Numeric)
    profit_margin = Column(Numeric)
    sustainability_score = Column(Numeric)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

from pydantic import BaseModel
from typing import Any


class FarmIn(BaseModel):
farmer_id: str
name: str
polygon_json: Any
area_ha: float


class FarmOut(FarmIn):
id: str
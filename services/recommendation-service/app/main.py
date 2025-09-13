from fastapi import FastAPI, Request
import os
import requests

app = FastAPI(title="Recommendation Service")

# Simple rule-based prototype crop list
CROPS = [
    {"crop": "maize", "min_ph": 5.5, "max_ph": 7.5, "water_need": "medium"},
    {"crop": "rice", "min_ph": 5.0, "max_ph": 7.0, "water_need": "high"},
    {"crop": "groundnut", "min_ph": 6.0, "max_ph": 7.8, "water_need": "low"},
]

# Environment variables for APIs
BHUWAN_API_ENDPOINT = os.getenv("BHUVAN_API_ENDPOINT", "https://bhuvan.nrsc.gov.in/api/some_endpoint")
BHUWAN_API_KEY = os.getenv("BHUVAN_API_KEY", "")

FARMONAUT_API_ENDPOINT = os.getenv("FARMONAUT_API_ENDPOINT", "https://api.farmonaut.com/ai/agri/health")
FARMONAUT_API_KEY = os.getenv("FARMONAUT_API_KEY", "")

def get_bhuvan_agri_data(lat: float, lon: float):
    if lat is None or lon is None:
        return None
    try:
        params = {"lat": lat, "lon": lon, "apikey": BHUWAN_API_KEY}
        r = requests.get(BHUWAN_API_ENDPOINT, params=params)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Bhuvan API error: {e}")
    return None

def get_farmonaut_data(lat: float, lon: float):
    if lat is None or lon is None:
        return None
    try:
        headers = {"Authorization": f"Bearer {FARMONAUT_API_KEY}"}
        params = {"lat": lat, "lng": lon}
        r = requests.get(FARMONAUT_API_ENDPOINT, headers=headers, params=params)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Farmonaut API error: {e}")
    return None

@app.post("/v1/recommendation/crop")
async def recommend(request: Request):
    payload = await request.json()

    lat = payload.get("lat")
    lon = payload.get("lon")

    # Fetch external data from APIs
    bhuvan_data = get_bhuvan_agri_data(lat, lon)
    farmonaut_data = get_farmonaut_data(lat, lon)

    # Extract soil info from Bhuvan or use payload fallback
    soil = payload.get("soil", {"ph": 6.3})
    if bhuvan_data and "soil_ph" in bhuvan_data:
        soil["ph"] = bhuvan_data["soil_ph"]

    water_constraint = payload.get("constraints", {}).get("water_limit_l", None)

    recommendations = []
    for c in CROPS:
        if soil["ph"] >= c["min_ph"] and soil["ph"] <= c["max_ph"]:
            score = 0.8
            # Penalize high water need crops if water is limited
            if water_constraint and c["water_need"] == "high":
                score -= 0.3
            
            # Adjust score downward if Farmonaut pest alert is high for crop
            pest_alert_level = farmonaut_data.get("pest_alert_level", 0) if farmonaut_data else 0
            if pest_alert_level > 5 and c["crop"] in (farmonaut_data.get("affected_crops", [])):
                score -= 0.2

            recommendations.append({
                "crop": c["crop"],
                "suitability_score": round(max(score, 0), 2),
                "expected_yield_qtl": 3.0,  # Placeholder, can be adjusted
                "expected_profit_inr": 10000,
                "sustainability_score": 0.7
            })

    return {
        "recommended_crops": recommendations,
        "bhuvan_data": bhuvan_data,
        "farmonaut_data": farmonaut_data,
        "model_version": "enhanced-ai-v0.1"
    }

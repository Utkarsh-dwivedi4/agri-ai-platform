from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Recommendation Service")

# Very simple rule-based engine for prototype
CROPS = [
    {"crop": "maize", "min_ph": 5.5, "max_ph": 7.5, "water_need": "medium"},
    {"crop": "rice", "min_ph": 5.0, "max_ph": 7.0, "water_need": "high"},
    {"crop": "groundnut", "min_ph": 6.0, "max_ph": 7.8, "water_need": "low"},
]

@app.post("/v1/recommendation/crop")
def recommend(payload: dict):
    # payload may include farm_id, soil_estimate, water_limit_l, market_prices etc.
    soil = payload.get("soil", {"ph": 6.3})
    water_constraint = payload.get("constraints", {}).get("water_limit_l", None)
    res = []
    for c in CROPS:
        if soil["ph"] >= c["min_ph"] and soil["ph"] <= c["max_ph"]:
            score = 0.8
            # simple water calculation:
            if water_constraint and c["water_need"] == "high":
                score -= 0.3
            res.append({
                "crop": c["crop"],
                "suitability_score": round(score,2),
                "expected_yield_qtl": 3.0,
                "expected_profit_inr": 10000,
                "sustainability_score": 0.7
            })
    return {"recommended_crops": res, "model_version": "rule-v0.1"}

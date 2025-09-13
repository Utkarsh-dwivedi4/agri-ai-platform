from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from .s3client import upload_fileobj
from .dummy_model import predict_image_and_saliency
import uuid
import json
import os
import requests
from sqlalchemy.orm import Session
from .config import DATABASE_URL

app = FastAPI(title="Image Inference")

# Bhuvan API endpoint and API key from environment variables
Bhuvan_API_ENDPOINT = os.getenv("BHUVAN_API_ENDPOINT", "https://bhuvan.nrsc.gov.in/api/some_endpoint")
BHUVAAN_API_KEY = os.getenv("BHUVAN_API_KEY", "")

def get_bhuvan_agri_data(lat: float, lon: float):
    if lat is None or lon is None:
        return None
    params = {
        "lat": lat,
        "lon": lon,
        "apikey": BHUVAAN_API_KEY
    }
    try:
        response = requests.get(Bhuvan_API_ENDPOINT, params=params)
        if response.status_code == 200:
            return response.json()  # Adjust depending on actual API response structure
        else:
            return None
    except Exception as e:
        print(f"Bhuvan API error: {e}")
        return None

@app.post("/v1/inference/image")
async def infer_image(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    farm_id: str = Form(...),
    farmer_id: str = Form(...),
    lat: float | None = Form(None),
    lon: float | None = Form(None),
):
    img_id = str(uuid.uuid4())
    object_name = f"images/raw/{farm_id}/{img_id}.jpg"
    # Upload original image to MinIO
    url = upload_fileobj(image.file, object_name)

    # Run dummy model prediction synchronously and upload saliency map
    res = predict_image_and_saliency(None)
    saliency_obj = f"images/inference/{farm_id}/{img_id}_saliency.png"
    upload_fileobj(res["saliency_bytes"], saliency_obj)
    saliency_url = f"http://{os.getenv('MINIO_ENDPOINT','minio:9000')}/{os.getenv('MINIO_BUCKET','agri-images')}/{saliency_obj}"

    # Fetch Bhuvan agri data based on lat/lon if provided
    bhuvan_data = get_bhuvan_agri_data(lat, lon)

    response = {
        "image_id": img_id,
        "s3_path": url,
        "label": res["label"],
        "confidence": res["confidence"],
        "saliency_url": saliency_url,
        "bhuvan_data": bhuvan_data,
        "model_version": "dummy-v0.1"
    }
    return response

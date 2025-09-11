from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from .s3client import upload_fileobj
from .dummy_model import predict_image_and_saliency
import uuid
import json
from sqlalchemy.orm import Session
from .config import DATABASE_URL
# Minimal DB usage omitted; we'll only save image meta to DB via simple psycopg2 or SQLAlchemy if needed

app = FastAPI(title="Image Inference")

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
    # upload original image to MinIO
    url = upload_fileobj(image.file, object_name)

    # run dummy model synchronously and upload saliency
    res = predict_image_and_saliency(None)
    saliency_obj = f"images/inference/{farm_id}/{img_id}_saliency.png"
    upload_fileobj(res["saliency_bytes"], saliency_obj)
    saliency_url = f"http://{os.getenv('MINIO_ENDPOINT','minio:9000')}/{os.getenv('MINIO_BUCKET','agri-images')}/{saliency_obj}"

    response = {
        "image_id": img_id,
        "s3_path": url,
        "label": res["label"],
        "confidence": res["confidence"],
        "saliency_url": saliency_url,
        "model_version": "dummy-v0.1"
    }
    return response

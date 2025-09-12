from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image

app = FastAPI()

# ✅ Load your trained TensorFlow model
model = tf.keras.models.load_model("models/crop_disease_model.h5")

# Preprocessing helper
def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))   # adjust to model input size
    img_array = np.array(image) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/inference/upload")
async def predict(file: UploadFile = File(...)):
    # Open uploaded image
    image = Image.open(file.file).convert("RGB")
    processed = preprocess_image(image)
    
    # Model prediction
    prediction = model.predict(processed)
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = float(np.max(prediction))

    # Example class labels
    labels = ["Healthy", "Blight", "Rust", "Leaf Spot"]
    result = labels[predicted_class]

    return {"disease": result, "confidence": confidence}

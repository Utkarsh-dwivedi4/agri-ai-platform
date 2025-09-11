import random
from PIL import Image, ImageDraw

def predict_image_and_saliency(image_path_or_stream):
    # Dummy prediction
    labels = ["healthy", "leaf_rust", "brown_spot", "blight"]
    label = random.choice(labels)
    confidence = round(random.uniform(0.7, 0.99), 2)

    # create a small saliency image to store
    im = Image.new("RGB", (256, 256), color=(255,255,255))
    d = ImageDraw.Draw(im)
    d.rectangle([50, 50, 200, 200], outline=(255,0,0))
    saliency_bytes = None
    from io import BytesIO
    buf = BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    return {"label": label, "confidence": confidence, "saliency_bytes": buf}

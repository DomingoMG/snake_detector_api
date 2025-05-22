from fastapi import UploadFile, File
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
from PIL import Image
import io


class SnakeClassifier:
    def __init__(self, model_path: str, input_size: tuple, threshold: float):
        self.model = load_model(model_path)
        self.input_size = input_size
        self.threshold = threshold

    def center_crop(self, image: Image.Image) -> Image.Image:
        width, height = image.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        return image.crop((left, top, right, bottom))

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        cropped = self.center_crop(img)
        resized = cropped.resize(self.input_size)
        array = image.img_to_array(resized)
        array = np.expand_dims(array, axis=0)
        return array / 255.0  # Normalización

    def predict(self, image_bytes: bytes) -> dict:
        input_tensor = self.preprocess_image(image_bytes)
        prediction = self.model.predict(input_tensor)[0][0]
        return {
            "class": "snake" if prediction > self.threshold else "no_snake",
            "confidence": float(prediction)
        }
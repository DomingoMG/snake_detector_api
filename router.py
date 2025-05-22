from fastapi import APIRouter, UploadFile, File, HTTPException
from model.snake_classifier import SnakeClassifier

router = APIRouter()
snake_classifier = SnakeClassifier(
    model_path="model/snake_classifier_mobilenet.h5",
    input_size=(224, 224),
    threshold=0.76
)

@router.post("/snake-detector/detect")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = snake_classifier.predict(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

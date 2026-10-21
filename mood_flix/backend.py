from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deepface import DeepFace
import cv2
import numpy as np
import base64
import uvicorn

app = FastAPI(title="MoodFlix AI Engine")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image_base64: str

# Emotion to Movie Genre Mapping
MOVIE_DB = {
    "happy": ["The Grand Budapest Hotel (Comedy)", "La La Land (Musical)", "Paddington 2 (Adventure)"],
    "sad": ["Inside Out (Animation)", "The Pursuit of Happyness (Drama)", "Good Will Hunting (Drama)"],
    "angry": ["John Wick (Action)", "Mad Max: Fury Road (Action)", "Fight Club (Thriller)"],
    "fear": ["A Quiet Place (Horror)", "Get Out (Thriller)", "Alien (Sci-Fi)"],
    "surprise": ["Inception (Sci-Fi)", "The Prestige (Mystery)", "Knives Out (Mystery)"],
    "neutral": ["The Secret Life of Walter Mitty (Adventure)", "The Truman Show (Drama)", "Interstellar (Sci-Fi)"],
    "disgust": ["Shaun of the Dead (Horror-Comedy)", "Zombieland (Action-Comedy)"]
}

@app.post("/api/analyze")
async def analyze_emotion(data: ImageData):
    try:
        # Strip the base64 header if present (data:image/jpeg;base64,...)
        img_data = data.image_base64
        if "," in img_data:
            img_data = img_data.split(",")[1]
        
        # Decode base64 to an OpenCV image array
        nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Analyze emotion using DeepFace
        # enforce_detection=False prevents crashes if no face is perfectly aligned
        analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        
        # DeepFace returns a list of dictionaries if multiple faces are found; we take the first
        dominant_emotion = analysis[0]['dominant_emotion']
        
        # Fetch recommendations
        recommendations = MOVIE_DB.get(dominant_emotion, MOVIE_DB["neutral"])

        return {
            "status": "success",
            "emotion": dominant_emotion,
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting MoodFlix AI Backend on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

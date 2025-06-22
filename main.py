from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import cv2
from utils import extract_frames, compute_feature_vector
from qdrant_setup import upload_to_qdrant, search_similar_frames
from fastapi.responses import HTMLResponse


app = FastAPI()

FRAME_DIR = "frames"
QUERY_DIR = "query_images"

os.makedirs(FRAME_DIR, exist_ok=True)
os.makedirs(QUERY_DIR, exist_ok=True)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 videos supported.")
    
    video_path = f"temp_{uuid.uuid4()}.mp4"
    with open(video_path, "wb") as f:
        f.write(await file.read())
    
    frame_paths = extract_frames(video_path, FRAME_DIR, interval=1)
    vectors = []

    for path in frame_paths:
        vec = compute_feature_vector(path)
        vectors.append((os.path.basename(path), vec))
    
    upload_to_qdrant(vectors)
    os.remove(video_path)

    return {"message": "Frames extracted and feature vectors stored.", "frames": frame_paths}

@app.post("/query/")
async def query_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".png", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only image files supported.")
    
    query_path = os.path.join(QUERY_DIR, f"{uuid.uuid4()}.jpg")
    with open(query_path, "wb") as f:
        f.write(await file.read())
    
    query_vec = compute_feature_vector(query_path)
    results = search_similar_frames(query_vec)

    return JSONResponse(content=results)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>🎥 Welcome to the Video Feature API</h2>
    <p>Use <a href="/docs">/docs</a> to access the Swagger UI and test the API endpoints.</p>
    """


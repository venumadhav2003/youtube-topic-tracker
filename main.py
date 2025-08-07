from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from video_fetcher import fetch_youtube_videos
from db import init_db, save_videos, get_all_videos
from typing import List
from models import Video
import os

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/videos", response_model=List[Video])
def get_videos(q: str = Query(..., description="Search term")):
    videos = fetch_youtube_videos(q)
    save_videos(videos)
    return videos

@app.get("/videos/stored", response_model=List[Video])
def list_stored():
    return get_all_videos()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join("static", "index.html"))

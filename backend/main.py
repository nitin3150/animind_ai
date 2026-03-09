from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.generate import router
from utils.save_code import get_tmp_dir
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,prefix="/generate",tags=["generate"])

# Ensure the media directory exists before mounting
media_dir = os.path.join(get_tmp_dir(), "code", "media")
os.makedirs(media_dir, exist_ok=True)
app.mount("/media", StaticFiles(directory=media_dir), name="media")

@app.get("/")
async def root():
    return {"message": "App is running!!"}
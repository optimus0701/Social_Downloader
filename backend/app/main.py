from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.routers import info, download
from app.services.download_manager import manager

# Tạo thư mục download nếu chưa có
os.makedirs(settings.download_dir, exist_ok=True)

app = FastAPI(
    title="Social Media Downloader API",
    description="API for downloading videos, audio and images from social platforms",
    version="1.0.0"
)

# CORS middleware
# Cấu hình production có thể thắt chặt origin hơn
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_domains],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(info.router)
app.include_router(download.router)

@app.on_event("startup")
async def startup_event():
    manager.start_cleanup_task()

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "ipv6_rotation": settings.ipv6_enabled}

# Endpoint để frontend serve (nếu dùng chung 1 container)
# Trong môi trường dev ta sẽ comment cái này để tránh conflict với vite dev server proxy, hoặc tạo file rỗng trước
try:
    if os.path.exists("../frontend/dist"):
        app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
except:
    pass

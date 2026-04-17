from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import HttpUrl
import os

from app.models.schemas import DownloadRequest, DownloadJobResponse
from app.services.download_manager import manager
from app.config import settings

router = APIRouter(prefix="/api/download", tags=["Download"])

@router.post("", response_model=DownloadJobResponse)
async def start_download(request: DownloadRequest):
    url_str = str(request.url)
    try:
        job_id = await manager.start_download(url_str, request.format, request.quality)
        return manager.get_job(job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}/status", response_model=DownloadJobResponse)
async def get_download_status(job_id: str):
    job = manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/{job_id}/file")
async def get_downloaded_file(job_id: str):
    job = manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="File is not ready yet")
        
    if not job.filename or not os.path.exists(job.filename):
        raise HTTPException(status_code=404, detail="File no longer exists on server")
        
    filename = os.path.basename(job.filename)
    return FileResponse(
        path=job.filename,
        filename=filename,
        media_type="application/octet-stream"
    )

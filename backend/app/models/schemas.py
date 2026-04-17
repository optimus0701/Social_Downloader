from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Any

class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str = "best" # "best", "audio", "images"
    quality: str = "highest"

class FormatInfo(BaseModel):
    format_id: str
    ext: str
    resolution: Optional[str] = None
    filesize: Optional[int] = None
    note: Optional[str] = None

class MediaInfo(BaseModel):
    title: str
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    platform: str
    is_slideshow: bool = False
    formats: List[FormatInfo] = []

class InfoRequest(BaseModel):
    url: HttpUrl

class DownloadJobResponse(BaseModel):
    job_id: str
    status: str # "pending", "downloading", "completed", "error"
    progress: float = 0.0
    filename: Optional[str] = None
    error: Optional[str] = None

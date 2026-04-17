from fastapi import APIRouter, HTTPException
from urllib.parse import urlparse
from app.models.schemas import InfoRequest, MediaInfo
from app.services import ytdlp_service, gallery_service

router = APIRouter(prefix="/api/info", tags=["Info"])

def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

@router.post("", response_model=MediaInfo)
async def get_media_info(request: InfoRequest):
    url_str = str(request.url)
    if not validate_url(url_str):
        raise HTTPException(status_code=400, detail="Invalid URL")
        
    try:
        # Check nếu là ảnh/gallery bằng gallery-dl trước (hữu ích cho TikTok, Instagram)
        is_gallery = False
        if "tiktok.com" in url_str or "instagram.com" in url_str:
             is_gallery = gallery_service.extract_gallery_info(url_str)
             
        # Lấy thông tin chung bằng yt-dlp
        info = ytdlp_service.extract_info(url_str)
        info.is_slideshow = is_gallery
        
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

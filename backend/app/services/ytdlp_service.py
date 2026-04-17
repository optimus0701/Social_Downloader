import yt_dlp
import os
import uuid
import logging
from typing import Dict, Any, Callable
from app.config import settings
from app.models.schemas import FormatInfo, MediaInfo
from app.services.ipv6_rotator import ipv6_rotator

logger = logging.getLogger(__name__)

def get_base_ydl_opts() -> Dict[str, Any]:
    opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(settings.download_dir, '%(id)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # Fake user agent
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    
    if settings.cookies_path and os.path.exists(settings.cookies_path):
        opts['cookiefile'] = settings.cookies_path
        
    if ipv6_rotator:
        rotated_ip = ipv6_rotator.next_address()
        if rotated_ip:
            logger.info(f"Using rotated IPv6 source address: {rotated_ip}")
            opts['source_address'] = rotated_ip
            # Option to force IPv6 might be needed depending on the host setup
            # opts['force_ipv6'] = True
            
    return opts

def extract_info(url: str) -> MediaInfo:
    ydl_opts = get_base_ydl_opts()
    # We only want to extract info, not download
    ydl_opts['extract_flat'] = False 
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    # Filter out formats without video or audio to keep it clean
                    if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                        resolution = f"{f.get('width', '')}x{f.get('height', '')}" if f.get('width') else 'audio only'
                        formats.append(FormatInfo(
                            format_id=f.get('format_id', ''),
                            ext=f.get('ext', ''),
                            resolution=resolution,
                            filesize=f.get('filesize') or f.get('filesize_approx'),
                            note=f.get('format_note')
                        ))
            
            return MediaInfo(
                title=info.get('title', 'Unknown Title'),
                thumbnail=info.get('thumbnail'),
                duration=info.get('duration'),
                platform=info.get('extractor_key', 'Unknown'),
                formats=formats
            )
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "HTTP Error 429" in error_msg and ipv6_rotator:
            ipv6_rotator.mark_failed()
        logger.error(f"Error extracting info for {url}: {e}")
        raise e

def download_video(url: str, format_type: str, quality: str, progress_hook: Callable[[Dict[str, Any]], None] = None) -> str:
    """
    Downloads media and returns the path to the downloaded file.
    format_type: 'best', 'audio'
    """
    ydl_opts = get_base_ydl_opts()
    
    # Generate unique filename to avoid overriding
    job_id = str(uuid.uuid4())
    ydl_opts['outtmpl'] = os.path.join(settings.download_dir, f'{job_id}.%(ext)s')
    
    if format_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif format_type == 'best':
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['merge_output_format'] = 'mp4'

    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([url])
            if error_code != 0:
                raise Exception("yt-dlp returned non-zero error code")
            
            # Find the downloaded file since extension might change (e.g. mkv -> mp4, webm -> mp3)
            # The progress hook usually has the final filename, but if not, we can search the dir
            for file in os.listdir(settings.download_dir):
                if file.startswith(job_id):
                    return os.path.join(settings.download_dir, file)
            
            raise FileNotFoundError("Downloaded file could not be located after completion")
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "HTTP Error 429" in error_msg and ipv6_rotator:
            ipv6_rotator.mark_failed()
        logger.error(f"Error downloading {url}: {e}")
        raise e

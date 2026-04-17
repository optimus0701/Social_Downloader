import subprocess
import os
import uuid
import json
import logging
from app.config import settings
from app.services.ipv6_rotator import ipv6_rotator

logger = logging.getLogger(__name__)

def extract_gallery_info(url: str) -> bool:
    """
    Dùng gallery-dl để check xem có phải ảnh/slideshow hay không.
    Trả về True nếu URL có vẻ chứa gallery/ảnh.
    """
    cmd = ["gallery-dl", "--dump-urls", url]
    
    if ipv6_rotator:
        rotated_ip = ipv6_rotator.next_address()
        if rotated_ip:
            # gallery-dl có option --source-address
            cmd.extend(["--source-address", rotated_ip])
            
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        # Nếu ra được mảng các URL ảnh (thường 2+ url cho slideshow)
        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return len(lines) > 0
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        logger.error(f"gallery-dl info error: {e}")
        return False

def download_gallery(url: str) -> str:
    """
    Tải ảnh từ gallery-dl và nén lại thành file zip nếu có nhiều ảnh.
    Trả về path file đã nén hoặc file ảnh.
    """
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(settings.download_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    # Sử dụng cấu hình cơ bản cho gallery-dl
    cmd = [
        "gallery-dl", 
        "--directory", job_dir,
        "--write-metadata",
        url
    ]
    
    if settings.cookies_path and os.path.exists(settings.cookies_path):
        cmd.extend(["--cookies", settings.cookies_path])
        
    if ipv6_rotator:
        rotated_ip = ipv6_rotator.next_address()
        if rotated_ip:
            cmd.extend(["--source-address", rotated_ip])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check HTTP 429 in stderr for IPv6 rotation
        if "HTTP 429" in result.stderr and ipv6_rotator:
            ipv6_rotator.mark_failed()
            
        if result.returncode != 0:
            raise Exception(f"gallery-dl error: {result.stderr}")
            
        # Nén thành file zip vì trả về cục bộ thường là nhiều file ảnh
        zip_path = os.path.join(settings.download_dir, f"{job_id}.zip")
        
        # Archive all files inside job_dir
        import shutil
        shutil.make_archive(os.path.join(settings.download_dir, job_id), 'zip', job_dir)
        
        # Clean up the directory
        shutil.rmtree(job_dir)
        
        return zip_path
        
    except Exception as e:
        logger.error(f"gallery-dl download error: {e}")
        raise e

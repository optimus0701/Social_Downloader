import asyncio
import uuid
import time
import os
import logging
from typing import Dict
from app.models.schemas import DownloadJobResponse
from app.services import ytdlp_service, gallery_service
from app.config import settings

logger = logging.getLogger(__name__)

class DownloadManager:
    def __init__(self):
        self.jobs: Dict[str, DownloadJobResponse] = {}
        self.cleanup_task = None
        
    def start_cleanup_task(self):
        if not self.cleanup_task:
            self.cleanup_task = asyncio.create_task(self._periodic_cleanup())
            
    async def _periodic_cleanup(self):
        """Dọn dẹp các local files và jobs cũ mỗi giờ"""
        while True:
            try:
                now = time.time()
                for job_id, job in list(self.jobs.items()):
                    # Giả sử cần dọn sau N giờ
                    # Thực tế cần 1 timestamp lưu trong job, nhưng for simplicity ta sẽ check file time
                    if job.filename and os.path.exists(job.filename):
                        file_mtime = os.path.getmtime(job.filename)
                        if now - file_mtime > settings.cleanup_hours * 3600:
                            try:
                                os.remove(job.filename)
                                logger.info(f"Cleaned up old file: {job.filename}")
                                del self.jobs[job_id]
                            except Exception as e:
                                logger.error(f"Failed to delete {job.filename}: {e}")
                
            except Exception as e:
                logger.error(f"Cleanup task error: {e}")
                
            await asyncio.sleep(3600) # Chạy mỗi giờ một lần

    def get_job(self, job_id: str) -> DownloadJobResponse:
        return self.jobs.get(job_id)
        
    def get_all_jobs(self) -> list[DownloadJobResponse]:
        return list(self.jobs.values())

    async def start_download(self, url: str, format_type: str, quality: str) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = DownloadJobResponse(job_id=job_id, status="pending")
        
        # Chạy trong background
        asyncio.create_task(self._download_task(job_id, url, format_type, quality))
        return job_id
        
    async def _download_task(self, job_id: str, url: str, format_type: str, quality: str):
        self.jobs[job_id].status = "downloading"
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                # Tính % downloaded
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    downloaded = d.get('downloaded_bytes', 0)
                    self.jobs[job_id].progress = (downloaded / total) * 100
            elif d['status'] == 'finished':
                self.jobs[job_id].progress = 100.0
                # self.jobs[job_id].filename có thể được set ở ytdlp service nếu nó access vào manager

        try:
            # Nếu chạy bằng I/O bound blocking code (yt_dlp/gallery_dl), cần wrap vào to_thread
            if format_type == "images":
                filepath = await asyncio.to_thread(gallery_service.download_gallery, url)
            else:
                filepath = await asyncio.to_thread(
                    ytdlp_service.download_video, url, format_type, quality, progress_hook
                )
                
            self.jobs[job_id].status = "completed"
            self.jobs[job_id].progress = 100.0
            self.jobs[job_id].filename = filepath
            
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            self.jobs[job_id].status = "error"
            self.jobs[job_id].error = str(e)

manager = DownloadManager()

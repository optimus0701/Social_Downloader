from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    api_port: int = 8000
    download_dir: str = "/downloads"
    max_file_size_mb: int = 2048
    cleanup_hours: int = 24
    allowed_domains: str = "*"

    # Bỏ trống nếu không dùng
    cookies_path: Optional[str] = None
    
    # ipv6 settings for oracle cloud
    ipv6_enabled: bool = False
    ipv6_blocks: str = "" # Comma separated blocks e.g. "2001:db8:1::/64,2001:db8:2::/64"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def ipv6_block_list(self) -> List[str]:
        if not self.ipv6_enabled or not self.ipv6_blocks:
            return []
        return [b.strip() for b in self.ipv6_blocks.split(",") if b.strip()]

settings = Settings()

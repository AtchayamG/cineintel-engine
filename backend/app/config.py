import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "CineIntel Engine"
    TRACK: str = "Parallel Web Systems Track"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Runtime Mode: 'live' or 'demo'
    RUNTIME_MODE: str = os.getenv("RUNTIME_MODE", "demo").lower()
    
    # Google Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
    
    # Server
    PORT: int = int(os.getenv("PORT", 8002))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    CORS_ORIGINS: List[str] = ["*"]
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    ENABLE_MOCK_FALLBACK: bool = os.getenv("ENABLE_MOCK_FALLBACK", "false").lower() in ("true", "1", "yes")
    
    # Parallel Web API
    PARALLEL_API_KEY: str = os.getenv("PARALLEL_API_KEY", "")
    PARALLEL_BASE_URL: str = os.getenv("PARALLEL_BASE_URL", "https://api.parallel.ai")

    @property
    def parallel_api_origin(self) -> str:
        return normalize_parallel_api_origin(self.PARALLEL_BASE_URL)

    @property
    def parallel_sdk_base_url(self) -> str:
        return get_parallel_sdk_base_url(self.PARALLEL_BASE_URL)

    @property
    def parallel_rest_search_url(self) -> str:
        return get_parallel_rest_search_url(self.PARALLEL_BASE_URL)

    @property
    def parallel_rest_extract_url(self) -> str:
        return get_parallel_rest_extract_url(self.PARALLEL_BASE_URL)

    @property
    def is_gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY or (self.GOOGLE_CLOUD_PROJECT and self.GOOGLE_CLOUD_LOCATION))

    @property
    def is_parallel_configured(self) -> bool:
        return bool(self.PARALLEL_API_KEY)

def normalize_parallel_api_origin(url: str) -> str:
    url = url.strip().rstrip('/')
    if url.endswith('/v1'):
        url = url[:-3].rstrip('/')
    return url

def get_parallel_sdk_base_url(url: str) -> str:
    return normalize_parallel_api_origin(url)

def get_parallel_rest_search_url(url: str) -> str:
    return f"{normalize_parallel_api_origin(url)}/v1/search"

def get_parallel_rest_extract_url(url: str) -> str:
    return f"{normalize_parallel_api_origin(url)}/v1/extract"

settings = Settings()


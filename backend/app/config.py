import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "CineIntel Engine"
    TRACK: str = "Parallel Web Systems Track"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Runtime Mode: 'live', 'demo', or 'hybrid'
    RUNTIME_MODE: str = os.getenv("RUNTIME_MODE", "demo").lower()
    GEMINI_RUNTIME_MODE: Optional[str] = None
    PARTNER_RUNTIME_MODE: Optional[str] = None
    
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

    def model_post_init(self, __context) -> None:
        self.RUNTIME_MODE = (self.RUNTIME_MODE or "demo").lower()
        if not self.GEMINI_RUNTIME_MODE:
            env_gemini = os.getenv("GEMINI_RUNTIME_MODE")
            if env_gemini:
                self.GEMINI_RUNTIME_MODE = env_gemini.lower()
            elif self.RUNTIME_MODE == "hybrid":
                self.GEMINI_RUNTIME_MODE = "live"
            else:
                self.GEMINI_RUNTIME_MODE = self.RUNTIME_MODE
        else:
            self.GEMINI_RUNTIME_MODE = self.GEMINI_RUNTIME_MODE.lower()

        if not self.PARTNER_RUNTIME_MODE:
            env_partner = os.getenv("PARTNER_RUNTIME_MODE")
            if env_partner:
                self.PARTNER_RUNTIME_MODE = env_partner.lower()
            elif self.RUNTIME_MODE == "hybrid":
                self.PARTNER_RUNTIME_MODE = "demo"
            else:
                self.PARTNER_RUNTIME_MODE = self.RUNTIME_MODE
        else:
            self.PARTNER_RUNTIME_MODE = self.PARTNER_RUNTIME_MODE.lower()

    @property
    def effective_runtime_mode(self) -> str:
        gemini_mode = (self.GEMINI_RUNTIME_MODE or self.RUNTIME_MODE).lower()
        partner_mode = (self.PARTNER_RUNTIME_MODE or self.RUNTIME_MODE).lower()
        if self.RUNTIME_MODE == "hybrid":
            return "hybrid"
        if gemini_mode == partner_mode:
            return gemini_mode
        return "hybrid"

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
        return bool(
            self.GEMINI_API_KEY
            or (self.GOOGLE_CLOUD_PROJECT and self.GOOGLE_CLOUD_LOCATION)
            or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            or os.getenv("K_SERVICE")
        )

    @property
    def gemini_configured_evidence(self) -> str:
        if self.GEMINI_API_KEY:
            return "Gemini Developer API key configured"
        if self.GOOGLE_CLOUD_PROJECT and self.GOOGLE_CLOUD_LOCATION:
            return f"Vertex AI ADC configured (project: {self.GOOGLE_CLOUD_PROJECT}, location: {self.GOOGLE_CLOUD_LOCATION})"
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return "Application Default Credentials file configured (GOOGLE_APPLICATION_CREDENTIALS)"
        if os.getenv("K_SERVICE"):
            return "Cloud Run runtime environment detected (Ambient ADC)"
        return "No Gemini API key or GCP ADC project configured"

    @property
    def is_parallel_configured(self) -> bool:
        return bool(self.PARALLEL_API_KEY)

    @property
    def parallel_configured_evidence(self) -> str:
        if self.PARALLEL_API_KEY:
            return f"Parallel API key configured (origin: {self.parallel_api_origin})"
        return "No PARALLEL_API_KEY configured (using local research fixtures)"

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


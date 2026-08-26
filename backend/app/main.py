import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from app.config import settings
from app.routes.intel_routes import router as intel_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s")
logger = logging.getLogger("cineintel.main")

app = FastAPI(
    title="CineIntel Engine API",
    version="1.0.0",
    description="Open-Web Grounding, Film Trend Research & Grounded Screenplay Doctor powered by Parallel Search API/SDK and Gemini 3.7."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intel_router, prefix=settings.API_PREFIX)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#00f0ff"/><text x="50" y="68" font-size="60" text-anchor="middle" font-family="sans-serif" stroke="none">🌐</text></svg>"""

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=FAVICON_SVG, media_type="image/svg+xml")

@app.get("/")
@app.get("/ui")
async def serve_ui():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "service": settings.PROJECT_NAME,
        "track": settings.TRACK,
        "mode": settings.effective_runtime_mode,
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
async def health_check():
    gemini_mode = settings.GEMINI_RUNTIME_MODE
    partner_mode = settings.PARTNER_RUNTIME_MODE
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "track": settings.TRACK,
        "runtime_mode": settings.effective_runtime_mode,
        "providers": {
            "google_gemini": {
                "mode": gemini_mode,
                "configured": settings.is_gemini_configured,
                "model": settings.GEMINI_MODEL,
                "status": "LIVE_CONFIGURED" if (gemini_mode == "live" and settings.is_gemini_configured) else ("LIVE_MISSING_CONFIG" if gemini_mode == "live" else "DEMO_MODE_ACTIVE"),
                "evidence": settings.gemini_configured_evidence
            },
            "parallel_web": {
                "mode": partner_mode,
                "configured": settings.is_parallel_configured,
                "integration": "Official Parallel Search SDK / API (parallel-web)",
                "status": "LIVE_CONFIGURED" if (partner_mode == "live" and settings.is_parallel_configured) else ("LIVE_MISSING_CONFIG" if partner_mode == "live" else "DEMO_MODE_ACTIVE"),
                "evidence": settings.parallel_configured_evidence
            }
        }
    }

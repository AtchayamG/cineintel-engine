import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.routes.intel_routes import router as intel_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s")
logger = logging.getLogger("cineintel.main")

app = FastAPI(
    title="CineIntel Engine API",
    version="1.0.0",
    description="Open-Web Grounding, Viral Film Trend Forecasting & Grounded Screenplay Doctor powered by Parallel MCP and Gemini 2.0."
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

@app.get("/")
@app.get("/ui")
async def serve_ui():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "service": settings.PROJECT_NAME,
        "track": settings.TRACK,
        "mode": settings.RUNTIME_MODE,
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "track": settings.TRACK,
        "runtime_mode": settings.RUNTIME_MODE,
        "providers": {
            "google_gemini": {
                "configured": settings.is_gemini_configured,
                "model": settings.GEMINI_MODEL
            },
            "parallel_mcp": {
                "configured": settings.is_parallel_configured,
                "server": "mcp-parallel-web",
                "status": "LIVE_CONFIGURED" if settings.is_parallel_configured else "DEMO_MODE_ACTIVE"
            }
        }
    }

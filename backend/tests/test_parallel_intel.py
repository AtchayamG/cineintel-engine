import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings
from app.services.parallel_service import ParallelService, parallel_service
from app.services.gemini_service import GeminiService, gemini_service
from app.agents.grounded_writer_agent import grounded_writer_agent
from app.agents.trend_analyst_agent import trend_analyst_agent
from app.agents.casting_intel_agent import casting_intel_agent
from app.mcp.parallel_mcp_server import parallel_mcp_server

@pytest.mark.asyncio
async def test_parallel_mcp_tools():
    tools = parallel_mcp_server.list_tools()
    assert len(tools) >= 2
    tool_names = [t["name"] for t in tools]
    assert "parallel_search_web" in tool_names
    assert "parallel_extract_url" in tool_names

@pytest.mark.asyncio
async def test_parallel_search_demo_fixtures():
    """Verify demo mode returns local research fixtures with non-clickable fixture IDs."""
    service = ParallelService()
    service.runtime_mode = "demo"
    res = await service.search_open_web("Cyberpunk cinematography tropes")
    assert res["status"] == "success"
    assert res["mode"] == "demo"
    assert "results" in res
    assert len(res["results"]) > 0
    first_result = res["results"][0]
    assert first_result["url"].startswith("fixture:")
    assert first_result["retrieval_status"] == "LOCAL_RESEARCH_FIXTURE"
    assert "snippet" in first_result

@pytest.mark.asyncio
async def test_parallel_search_live_mode_no_silent_fallback():
    """Verify live mode returns live_unavailable/live_error on missing key or failure without fallback to demo."""
    service = ParallelService()
    service.runtime_mode = "live"
    service.api_key = ""  # Missing key
    res = await service.search_open_web("Cyberpunk cinematography tropes")
    assert res["status"] == "error"
    assert res["mode"] == "live_unavailable"
    assert "PARALLEL_API_KEY" in res["error"]

@pytest.mark.asyncio
async def test_gemini_live_mode_no_silent_fallback():
    """Verify Gemini live mode returns live_unavailable on missing client without fallback to demo."""
    service = GeminiService()
    service.runtime_mode = "live"
    service.client = None
    res = service.synthesize_research_and_script("Cyberpunk detective", "Sci-Fi Noir", [])
    assert res["success"] is False
    assert res["mode"] == "live_unavailable"
    assert res["data"] is None

@pytest.mark.asyncio
async def test_gemini_research_synthesis_demo():
    sources = [{
        "title": "Sci-Fi Tropes",
        "url": "fixture:sci-fi-tropes",
        "snippet": "AI consciousness narrative tension"
    }]
    res = gemini_service.synthesize_research_and_script("Cyberpunk detective", "Sci-Fi Noir", sources)
    assert res["success"] is True
    assert "data" in res
    assert "grounded_title" in res["data"]
    assert "viability_critique" in res["data"]
    assert "Sci-Fi Noir" in res["data"]["concept_summary"]

@pytest.mark.asyncio
async def test_route_type_regression_genre_dict():
    """
    Regression Test for UI/Data Bug:
    Ensure POST /api/v1/intel/script/grounded passes genre as string,
    and concept_summary does NOT render a Python dictionary string representation.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/intel/script/grounded", json={
            "premise": "A synthetic investigator in Neo-Tokyo",
            "genre": "Cyberpunk Thriller"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("genre") == "Cyberpunk Thriller"
        syn = data.get("gemini_synthesis")
        assert syn is not None
        concept_summary = syn.get("concept_summary", "")
        # Must contain genre string and MUST NOT contain python dict string representation
        assert "Cyberpunk Thriller" in concept_summary
        assert "{'agent':" not in concept_summary
        assert "{'genre':" not in concept_summary

@pytest.mark.asyncio
async def test_health_readiness_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "providers" in data
        assert "parallel_web" in data["providers"]
        assert "google_gemini" in data["providers"]
        assert data["providers"]["google_gemini"]["model"] == settings.GEMINI_MODEL

@pytest.mark.asyncio
async def test_primary_ui_workflow_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # GET /
        resp_ui = await ac.get("/")
        assert resp_ui.status_code == 200

        # POST /api/v1/intel/analyze/trends
        resp_trends = await ac.post("/api/v1/intel/analyze/trends", json={
            "premise": "Quantum AI grid crash",
            "genre": "Hard Sci-Fi"
        })
        assert resp_trends.status_code == 200
        trends_data = resp_trends.json()
        assert trends_data.get("genre") == "Hard Sci-Fi"
        # Verify 8.8 market score was removed
        assert "8.8" not in str(trends_data)
        assert "market_viability_score" not in trends_data

        # GET /api/v1/intel/casting/affinity
        resp_casting = await ac.get("/api/v1/intel/casting/affinity")
        assert resp_casting.status_code == 200

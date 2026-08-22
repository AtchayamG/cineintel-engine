import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import httpx
from parallel import AsyncParallel
from app.config import (
    settings,
    normalize_parallel_api_origin,
    get_parallel_sdk_base_url,
    get_parallel_rest_search_url,
    get_parallel_rest_extract_url
)
from app.services.parallel_service import ParallelService, parallel_service
from app.services.gemini_service import GeminiService, gemini_service
from app.agents.grounded_writer_agent import grounded_writer_agent
from app.agents.trend_analyst_agent import trend_analyst_agent
from app.agents.casting_intel_agent import casting_intel_agent
from app.mcp.parallel_mcp_server import parallel_mcp_server

@pytest.mark.asyncio
async def test_parallel_url_normalization_helpers():
    test_cases = [
        ("https://api.parallel.ai", "https://api.parallel.ai", "https://api.parallel.ai/v1/search", "https://api.parallel.ai/v1/extract"),
        ("https://api.parallel.ai/", "https://api.parallel.ai", "https://api.parallel.ai/v1/search", "https://api.parallel.ai/v1/extract"),
        ("https://api.parallel.ai/v1", "https://api.parallel.ai", "https://api.parallel.ai/v1/search", "https://api.parallel.ai/v1/extract"),
        ("https://api.parallel.ai/v1/", "https://api.parallel.ai", "https://api.parallel.ai/v1/search", "https://api.parallel.ai/v1/extract"),
        ("https://custom-proxy.internal/v1/", "https://custom-proxy.internal", "https://custom-proxy.internal/v1/search", "https://custom-proxy.internal/v1/extract")
    ]
    for raw_input, expected_sdk_base, expected_rest_search, expected_rest_extract in test_cases:
        assert normalize_parallel_api_origin(raw_input) == expected_sdk_base
        assert get_parallel_sdk_base_url(raw_input) == expected_sdk_base
        assert get_parallel_rest_search_url(raw_input) == expected_rest_search
        assert get_parallel_rest_extract_url(raw_input) == expected_rest_extract

@pytest.mark.asyncio
async def test_sdk_path_endpoint_construction_contract():
    """
    Contract test: Proves that official parallel-web AsyncParallel SDK constructs
    exact endpoint 'https://api.parallel.ai/v1/search' (without '/v1/v1' duplication)
    when passed normalized base URLs.
    """
    inputs = [
        "https://api.parallel.ai",
        "https://api.parallel.ai/",
        "https://api.parallel.ai/v1",
        "https://api.parallel.ai/v1/",
        "https://custom-proxy.internal/v1/"
    ]

    for raw_url in inputs:
        sdk_base_url = get_parallel_sdk_base_url(raw_url)
        intercepted_url = None

        def mock_handler(request: httpx.Request):
            nonlocal intercepted_url
            intercepted_url = str(request.url)
            return httpx.Response(200, json={"results": [], "search_id": "mock_id"})

        transport = httpx.MockTransport(mock_handler)
        mock_http_client = httpx.AsyncClient(transport=transport)
        client = AsyncParallel(api_key="test_key", base_url=sdk_base_url, http_client=mock_http_client)
        
        await client.search(objective="cinematography tropes", search_queries=["cinematography tropes"])
        
        expected_url = f"{sdk_base_url}/v1/search"
        assert intercepted_url == expected_url
        assert "/v1/v1" not in intercepted_url

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
        ui_html = resp_ui.text
        assert "MODE: DEMO FIXTURES" in ui_html
        assert "Run Deterministic Research Fixtures" in ui_html

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

@pytest.mark.asyncio
async def test_xss_prevention_static():
    """
    Verify that index.html employs strict XSS prevention.
    """
    import os
    index_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verify helpers exist
    assert 'function escapeHTML' in content
    assert 'function isValidHttpUrl' in content
    assert "url.protocol === 'http:'" in content
    assert "url.protocol === 'https:'" in content

    # Verify noopener noreferrer target=_blank
    assert 'rel="noopener noreferrer"' in content
    assert 'target="_blank"' in content

    # Verify that dangerous properties are not interpolated directly
    assert '${safeTitle}' in content
    assert '${safeUrl}' in content
    assert '${safeSnippet}' in content
    
    assert '<a href="${s.url}"' not in content
    assert '>${s.title}<' not in content

@pytest.mark.asyncio
async def test_demo_mode_button_reset_regression():
    """
    Regression Test for UI Bug:
    Ensure that after a demo run, the button resets to the exact honest fixture wording,
    including 'local Gemini-shaped synthesis fixture'.
    """
    import os
    index_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The reset label must strictly use this phrasing so it does not regress to 'Gemini 3.7 Synthesis' in demo mode
    expected_reset_code = "btn.innerText = isLive ? '⚡ Run Parallel Search + Gemini 3.7 Grounded Synthesis' : '⚡ Run Deterministic Research Fixtures + local Gemini-shaped synthesis fixture';"
    assert expected_reset_code in content, "The button reset code in finally block must restore the exact demo fixture wording."

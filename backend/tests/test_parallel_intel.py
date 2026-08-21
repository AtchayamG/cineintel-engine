import pytest
from app.services.parallel_service import parallel_service
from app.services.gemini_service import gemini_service
from app.agents.grounded_writer_agent import grounded_writer_agent
from app.mcp.parallel_mcp_server import parallel_mcp_server

@pytest.mark.asyncio
async def test_parallel_mcp_tools():
    tools = parallel_mcp_server.list_tools()
    assert len(tools) >= 2
    tool_names = [t["name"] for t in tools]
    assert "parallel_search_web" in tool_names
    assert "parallel_extract_url" in tool_names

@pytest.mark.asyncio
async def test_parallel_search_demo():
    res = await parallel_service.search_open_web("Cyberpunk cinematography tropes")
    assert res["status"] == "success"
    assert len(res["results"]) > 0
    assert "url" in res["results"][0]

@pytest.mark.asyncio
async def test_gemini_research_synthesis():
    sources = [{"title": "Sci-Fi Tropes", "url": "https://example.com", "snippet": "AI consciousness narrative tension"}]
    res = gemini_service.synthesize_research_and_script("Cyberpunk detective", "Sci-Fi Noir", sources)
    assert res["success"] is True
    assert "data" in res
    assert "grounded_title" in res["data"]
    assert "viability_critique" in res["data"]

@pytest.mark.asyncio
async def test_grounded_writer_end_to_end():
    res = await grounded_writer_agent.generate_grounded_script("A cyber detective investigates a glitch", "Sci-Fi Noir")
    assert "gemini_synthesis" in res
    assert res["parallel_sources_retrieved"] > 0
    assert "measured_latency_ms" in res

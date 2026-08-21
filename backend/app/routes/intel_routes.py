from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.parallel_service import parallel_service
from app.agents.trend_analyst_agent import trend_analyst_agent
from app.agents.grounded_writer_agent import grounded_writer_agent
from app.agents.casting_intel_agent import casting_intel_agent
from app.mcp.parallel_mcp_server import parallel_mcp_server

router = APIRouter(prefix="/intel", tags=["CineIntel Engine API"])

class TrendSearchRequest(BaseModel):
    premise: str = "A rogue synthetic investigator in a cyberpunk city."
    genre: str = "Sci-Fi Noir"

class GroundedScriptRequest(BaseModel):
    premise: str
    genre: str = "Sci-Fi Noir"

@router.post("/analyze/trends")
async def analyze_trends(req: TrendSearchRequest):
    return await trend_analyst_agent.analyze_premise(req.premise, req.genre)

@router.post("/script/grounded")
async def generate_grounded_script(req: GroundedScriptRequest):
    trends = await trend_analyst_agent.analyze_premise(req.premise, req.genre)
    return await grounded_writer_agent.generate_grounded_script(req.premise, trends)

@router.get("/casting/affinity")
async def get_casting_affinity():
    return await casting_intel_agent.evaluate_cast_affinity(["Maya Vance", "Dr. Alistair Chen"])

@router.get("/mcp/tools")
async def get_mcp_tools():
    return {
        "server": "mcp-parallel-web",
        "tools": parallel_mcp_server.list_tools()
    }

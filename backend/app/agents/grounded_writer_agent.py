import logging
import time
from typing import Dict, Any, List
from app.services.parallel_service import parallel_service
from app.services.gemini_service import gemini_service

logger = logging.getLogger("cineintel.grounded_writer")

class GroundedWriterAgent:
    """
    Autonomous Grounded Screenwriter Agent.
    Infuses real-world data, scientific accuracy, and cultural zeitgeist
    into Gemini 2.0 screenplay generation using Parallel Search & Extract MCP.
    """
    def __init__(self):
        self.name = "GroundedWriterAgent"
        self.role = "Fact-Grounded Screenplay Architect"

    async def generate_grounded_script(self, premise: str, genre: str) -> Dict[str, Any]:
        start = time.time()
        
        # Step 1: Query Parallel Search MCP for relevant web context
        search_res = await parallel_service.search_open_web(f"{genre} cinematography tropes {premise[:30]}")
        sources = search_res.get("results", [])

        # Step 2: Call Gemini 2.0 to synthesize sources into grounded concept
        gemini_res = gemini_service.synthesize_research_and_script(premise, genre, sources)

        return {
            "agent": self.name,
            "premise": premise,
            "genre": genre,
            "parallel_sources_retrieved": len(sources),
            "sources": sources,
            "parallel_evidence_source": search_res.get("evidence_source"),
            "gemini_synthesis": gemini_res.get("data"),
            "gemini_evidence_source": gemini_res.get("evidence_source"),
            "measured_latency_ms": round((time.time() - start) * 1000, 2)
        }

grounded_writer_agent = GroundedWriterAgent()

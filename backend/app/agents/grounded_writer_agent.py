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
    into Gemini 3.7 screenplay generation using Parallel Search & Extract.
    """
    def __init__(self):
        self.name = "GroundedWriterAgent"
        self.role = "Fact-Grounded Screenplay Architect"

    async def generate_grounded_script(self, premise: str, genre: str) -> Dict[str, Any]:
        start = time.time()
        genre_str = genre if isinstance(genre, str) else str(genre)
        
        # Step 1: Query Parallel Search for relevant web context
        search_res = await parallel_service.search_open_web(f"{genre_str} cinematography tropes {premise[:30]}")
        sources = search_res.get("results", [])

        # If search failed in live mode, pass through status
        if search_res.get("status") == "error":
            return {
                "agent": self.name,
                "status": search_res.get("status"),
                "mode": search_res.get("mode"),
                "error": search_res.get("error"),
                "premise": premise,
                "genre": genre_str,
                "parallel_sources_retrieved": 0,
                "sources": [],
                "gemini_synthesis": None,
                "measured_latency_ms": round((time.time() - start) * 1000, 2)
            }

        # Step 2: Call Gemini 3.7 to synthesize sources into grounded concept
        gemini_res = gemini_service.synthesize_research_and_script(premise, genre_str, sources)

        return {
            "agent": self.name,
            "status": "success" if gemini_res.get("success") else "error",
            "mode": gemini_res.get("mode", search_res.get("mode")),
            "error": gemini_res.get("error"),
            "premise": premise,
            "genre": genre_str,
            "parallel_sources_retrieved": len(sources),
            "sources": sources,
            "parallel_evidence_source": search_res.get("evidence_source"),
            "gemini_synthesis": gemini_res.get("data"),
            "gemini_evidence_source": gemini_res.get("evidence_source"),
            "measured_latency_ms": round((time.time() - start) * 1000, 2)
        }

grounded_writer_agent = GroundedWriterAgent()

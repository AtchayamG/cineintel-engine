import os
import json
import logging
import time
from typing import Dict, Any, List, Optional
from app.config import settings

logger = logging.getLogger("cineintel.gemini")

class GeminiService:
    """
    Google GenAI SDK & Gemini 2.0 Integration Service for CineIntel Engine.
    Synthesizes open-web research returned from Parallel Search MCP into
    fact-grounded screenplay treatments and uncertainty-bounded market viability critiques.
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.project = settings.GOOGLE_CLOUD_PROJECT
        self.location = settings.GOOGLE_CLOUD_LOCATION
        self.model_name = settings.GEMINI_MODEL
        self.runtime_mode = settings.RUNTIME_MODE
        self.client = None
        self._init_client()

    def _init_client(self):
        if self.api_key or (self.project and self.location):
            try:
                from google import genai
                if self.api_key:
                    self.client = genai.Client(api_key=self.api_key)
                else:
                    self.client = genai.Client(vertexai=True, project=self.project, location=self.location)
                logger.info(f"Initialized Google GenAI Client with model: {self.model_name} (Mode: LIVE)")
            except Exception as e:
                logger.warning(f"Could not initialize google-genai client ({e}). Running in demo mode.")
        else:
            logger.info("No Gemini credentials found. Running in deterministic DEMO fixture mode.")

    def synthesize_research_and_script(self, premise: str, genre: str, search_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calls Gemini 2.0 to ground screenplay development using Parallel Search sources.
        """
        start_time = time.time()
        
        sources_summary = "\n".join([f"- Title: {s.get('title')} | URL: {s.get('url')} | Snippet: {s.get('snippet')}" for s in search_sources])

        prompt = f"""
        You are a seasoned narrative development executive and script doctor.
        Analyze this film premise: '{premise}' in genre '{genre}'.
        
        Use the following real-world web research sources retrieved from Parallel Search:
        {sources_summary}

        Output JSON strictly matching this schema:
        {{
            "grounded_title": "string",
            "concept_summary": "string",
            "viability_critique": "string",
            "uncertainty_rating": "string (Low / Moderate / High)",
            "key_grounded_tropes": ["string", "string"],
            "recommended_scene_beats": ["string", "string"],
            "cinematography_lut_reference": "string"
        }}
        """

        if self.client and self.runtime_mode == "live":
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "system_instruction": "You ground fictional screenplays in real-world cultural data and cinematic benchmarks.",
                        "response_mime_type": "application/json"
                    }
                )
                result = json.loads(response.text.strip())
                latency_ms = int((time.time() - start_time) * 1000)
                return {
                    "success": True,
                    "mode": "live",
                    "evidence_source": "Google GenAI API (Gemini 2.0 Flash Live)",
                    "data": result,
                    "latency_ms": latency_ms
                }
            except Exception as e:
                logger.error(f"Gemini research synthesis failed: {e}")
                if not settings.ENABLE_MOCK_FALLBACK:
                    return {
                        "success": False,
                        "mode": "live_error",
                        "error": str(e),
                        "data": None
                    }

        # Deterministic Demo Mode
        latency_ms = max(int((time.time() - start_time) * 1000), 28)
        demo_synthesis = {
            "grounded_title": "Neon Horizons: Quantum Resonance",
            "concept_summary": f"A grounded investigation into synthetic consciousness ethics against a localized atmospheric grid collapse in {genre}.",
            "viability_critique": "Strong audience alignment when focusing on philosophical conflict over generic spectacle. High indie streaming appeal based on reference tropes.",
            "uncertainty_rating": "Moderate (Requires targeted visual execution to avoid trope saturation)",
            "key_grounded_tropes": [
                "Atmospheric micro-climate failure",
                "Non-linear quantum memory recall logs",
                "35mm blue streak anamorphic lensing"
            ],
            "recommended_scene_beats": [
                "Opening on rain-slicked runway with degraded telemetry readouts",
                "Breach into crystalline memory vault with irregular crimson strobe lighting",
                "Moral confrontation between detective and lead systems architect"
            ],
            "cinematography_lut_reference": "Panavision C-Series Anamorphic with cyan undertones and warm amber highlights"
        }

        return {
            "success": True,
            "mode": "demo",
            "evidence_source": "Deterministic Local Synthesis Dataset (demo fixture)",
            "data": demo_synthesis,
            "latency_ms": latency_ms
        }

gemini_service = GeminiService()

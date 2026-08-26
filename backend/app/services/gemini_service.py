import os
import json
import logging
import time
from typing import Dict, Any, List, Optional
from app.config import settings

logger = logging.getLogger("cineintel.gemini")

class GeminiService:
    """
    Google GenAI SDK & Gemini 3.7 Integration Service for CineIntel Engine.
    Synthesizes open-web research returned from Parallel Search into
    fact-grounded screenplay treatments, scene beats, and uncertainty-bounded viability critiques.
    """
    def __init__(self):
        self._api_key: Optional[str] = None
        self._project: Optional[str] = None
        self._location: Optional[str] = None
        self._model_name: Optional[str] = None
        self._runtime_mode: Optional[str] = None
        self.client = None
        self._init_client()

    @property
    def api_key(self) -> str:
        return self._api_key if self._api_key is not None else settings.GEMINI_API_KEY

    @api_key.setter
    def api_key(self, val: str):
        self._api_key = val

    @property
    def project(self) -> str:
        return self._project if self._project is not None else settings.GOOGLE_CLOUD_PROJECT

    @project.setter
    def project(self, val: str):
        self._project = val

    @property
    def location(self) -> str:
        return self._location if self._location is not None else settings.GOOGLE_CLOUD_LOCATION

    @location.setter
    def location(self, val: str):
        self._location = val

    @property
    def model_name(self) -> str:
        return self._model_name if self._model_name is not None else settings.GEMINI_MODEL

    @model_name.setter
    def model_name(self, val: str):
        self._model_name = val

    @property
    def runtime_mode(self) -> str:
        return self._runtime_mode if self._runtime_mode is not None else settings.GEMINI_RUNTIME_MODE

    @runtime_mode.setter
    def runtime_mode(self, val: str):
        self._runtime_mode = val

    def _init_client(self):
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Initialized Google GenAI Client with model: {self.model_name} (Mode: LIVE API KEY)")
            except Exception as e:
                logger.warning(f"Could not initialize google-genai client with API key ({e}).")
        elif self.project:
            try:
                from google import genai
                self.client = genai.Client(vertexai=True, project=self.project, location=self.location or "global")
                logger.info(f"Initialized Google GenAI Client on Vertex AI (project: {self.project}, location: {self.location}, model: {self.model_name})")
            except Exception as e:
                logger.warning(f"Could not initialize google-genai client on Vertex AI ({e}).")
        elif self.runtime_mode == "live":
            try:
                from google import genai
                self.client = genai.Client(vertexai=True, location=self.location or "global")
                logger.info(f"Initialized Google GenAI Client via Cloud Run ADC (location: {self.location}, model: {self.model_name})")
            except Exception as e:
                logger.warning(f"Could not initialize google-genai client via Cloud Run ADC ({e}).")
        else:
            logger.info("No Gemini credentials found. Running in deterministic DEMO fixture mode.")

    def synthesize_research_and_script(self, premise: str, genre: str, search_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calls Gemini 3.7 Flash to ground screenplay development using Parallel Search sources.
        """
        start_time = time.time()
        
        # Ensure genre is a string
        genre_str = genre if isinstance(genre, str) else str(genre)

        if self.runtime_mode == "live":
            if not self.client:
                return {
                    "success": False,
                    "mode": "live_unavailable",
                    "error": "Gemini API credentials or client not configured in live mode.",
                    "data": None
                }

            sources_summary = "\n".join([
                f"- Title: {s.get('title')} | URL: {s.get('url')} | Snippet: {s.get('snippet')}"
                for s in search_sources
            ])

            prompt = f"""
            You are a seasoned narrative development executive and script doctor.
            Analyze this film premise: '{premise}' in genre '{genre_str}'.
            
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

            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "system_instruction": "You ground fictional screenplays in real-world cultural data, evidence, and cinematic benchmarks. Do not output unsupported ROI or market scores.",
                        "response_mime_type": "application/json"
                    }
                )
                result = json.loads(response.text.strip())
                latency_ms = int((time.time() - start_time) * 1000)
                return {
                    "success": True,
                    "mode": "live",
                    "evidence_source": f"Google GenAI API ({self.model_name} Live)",
                    "data": result,
                    "latency_ms": latency_ms
                }
            except Exception as e:
                logger.error(f"Gemini research synthesis failed: {e}")
                return {
                    "success": False,
                    "mode": "live_error",
                    "error": f"Gemini API error: {str(e)}",
                    "data": None
                }

        # Deterministic Demo Mode
        latency_ms = max(int((time.time() - start_time) * 1000), 28)
        demo_synthesis = {
            "grounded_title": "Neon Horizons: Quantum Resonance",
            "concept_summary": f"A grounded investigation into synthetic consciousness ethics against a localized atmospheric grid collapse in {genre_str}.",
            "viability_critique": "The premise presents strong potential around philosophical human-AI conflict. Development should focus on distinct visual styling and character agency rather than generic sci-fi tropes.",
            "uncertainty_rating": "Moderate (Requires targeted visual execution to avoid audience trope saturation)",
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

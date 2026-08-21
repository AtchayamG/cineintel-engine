import logging
import time
import httpx
from typing import Dict, Any, List
from app.config import (
    settings,
    normalize_parallel_api_origin,
    get_parallel_sdk_base_url,
    get_parallel_rest_search_url,
    get_parallel_rest_extract_url
)

logger = logging.getLogger("cineintel.parallel")

class ParallelService:
    """
    Parallel Web Systems Search & Extract integration for CineIntel Engine.
    Powers open-web research, cultural trope analysis, and grounded scriptwriting.
    Utilizes the official Parallel Search API / SDK (`parallel-web`).
    """
    def __init__(self):
        self.api_key = settings.PARALLEL_API_KEY
        self.runtime_mode = settings.RUNTIME_MODE

    @property
    def sdk_base_url(self) -> str:
        return settings.parallel_sdk_base_url

    @property
    def rest_search_url(self) -> str:
        return settings.parallel_rest_search_url

    @property
    def rest_extract_url(self) -> str:
        return settings.parallel_rest_extract_url

    async def search_open_web(self, query: str, max_results: int = 4) -> Dict[str, Any]:
        start = time.time()
        logger.info(f"Executing Parallel Web Search (Mode: {self.runtime_mode}): {query}")

        if self.runtime_mode == "live":
            if not self.api_key:
                logger.error("Live mode enabled but PARALLEL_API_KEY is not set.")
                return {
                    "status": "error",
                    "mode": "live_unavailable",
                    "error": "PARALLEL_API_KEY is missing in live mode.",
                    "query": query,
                    "results": []
                }

            # Attempt official parallel-web SDK first, then fallback to direct HTTP with x-api-key
            raw_results = None
            error_msg = None

            try:
                from parallel import AsyncParallel
                client = AsyncParallel(api_key=self.api_key, base_url=self.sdk_base_url)
                search_res = await client.search(objective=query, search_queries=[query])
                if hasattr(search_res, "results") and search_res.results is not None:
                    raw_results = search_res.results
            except Exception as sdk_err:
                logger.warning(f"Parallel SDK call failed ({sdk_err}). Trying direct HTTP request to {self.rest_search_url}.")
                try:
                    headers = {
                        "x-api-key": self.api_key,
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "objective": query,
                        "search_queries": [query]
                    }
                    async with httpx.AsyncClient(timeout=10.0) as http_client:
                        resp = await http_client.post(
                            self.rest_search_url,
                            json=payload,
                            headers=headers
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            raw_results = data.get("results", [])
                        else:
                            error_msg = f"HTTP {resp.status_code}: {resp.text}"
                except Exception as http_err:
                    error_msg = f"SDK Error: {sdk_err} | HTTP Error: {http_err}"

            if raw_results is not None:
                # Normalize result excerpts
                normalized_results = []
                for item in raw_results:
                    if hasattr(item, "url"):
                        url = item.url
                        title = getattr(item, "title", None) or "Parallel Search Result"
                        excerpts = getattr(item, "excerpts", []) or []
                        publish_date = getattr(item, "publish_date", None)
                    elif isinstance(item, dict):
                        url = item.get("url", "")
                        title = item.get("title") or "Parallel Search Result"
                        excerpts = item.get("excerpts") or ([item.get("snippet")] if item.get("snippet") else [])
                        publish_date = item.get("publish_date")
                    else:
                        continue

                    snippet = " ".join(excerpts) if isinstance(excerpts, list) else str(excerpts)
                    normalized_results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "excerpts": excerpts if isinstance(excerpts, list) else [snippet],
                        "publish_date": publish_date,
                        "retrieval_status": "RETRIEVED_LIVE_WEB"
                    })

                if not normalized_results:
                    return {
                        "status": "error",
                        "mode": "live_error",
                        "error": "Parallel Search API returned empty sources.",
                        "query": query,
                        "results": []
                    }

                return {
                    "status": "success",
                    "mode": "live",
                    "evidence_source": "Parallel Search API (Official Live Endpoint)",
                    "query": query,
                    "results": normalized_results[:max_results],
                    "latency_ms": round((time.time() - start) * 1000, 2)
                }

            # If both SDK and HTTP failed in live mode
            return {
                "status": "error",
                "mode": "live_error",
                "error": error_msg or "Parallel Search request failed.",
                "query": query,
                "results": []
            }

        # Deterministic Demo Mode — Local Research Fixtures (non-clickable fixture IDs)
        demo_sources = [
            {
                "title": "Cinematography & Visual World-Building Reference Index",
                "url": "fixture:cinematography-anamorphic-lensing",
                "snippet": "Technical analysis of anamorphic lens distortion, shallow depth of field, and cyan-magenta color timing in hard science-fiction filmmaking.",
                "excerpts": [
                    "Technical analysis of anamorphic lens distortion, shallow depth of field, and cyan-magenta color timing in hard science-fiction filmmaking."
                ],
                "retrieval_status": "LOCAL_RESEARCH_FIXTURE"
            },
            {
                "title": "Narrative Tropes & Philosophical Sci-Fi Character Study",
                "url": "fixture:sci-fi-narrative-tropes",
                "snippet": "Study highlighting how grounded philosophical tension between artificial intelligence and human agency structures modern narrative arcs.",
                "excerpts": [
                    "Study highlighting how grounded philosophical tension between artificial intelligence and human agency structures modern narrative arcs."
                ],
                "retrieval_status": "LOCAL_RESEARCH_FIXTURE"
            }
        ]

        return {
            "status": "success",
            "mode": "demo",
            "evidence_source": "Parallel Web Demo Fixtures (Local research reference dataset)",
            "query": query,
            "latency_ms": max(round((time.time() - start) * 1000, 2), 14.5),
            "results": demo_sources[:max_results]
        }

    async def extract_url(self, url: str) -> Dict[str, Any]:
        start = time.time()
        if self.runtime_mode == "live":
            if not self.api_key:
                return {
                    "status": "error",
                    "mode": "live_unavailable",
                    "error": "PARALLEL_API_KEY missing in live mode.",
                    "url": url
                }
            try:
                from parallel import AsyncParallel
                client = AsyncParallel(api_key=self.api_key, base_url=self.sdk_base_url)
                res = await client.extract(urls=[url])
                return {
                    "status": "success",
                    "mode": "live",
                    "evidence_source": "Parallel Extract Engine (Live Endpoint)",
                    "url": url,
                    "extract_data": str(res),
                    "latency_ms": round((time.time() - start) * 1000, 2)
                }
            except Exception as e:
                try:
                    headers = {
                        "x-api-key": self.api_key,
                        "Content-Type": "application/json"
                    }
                    async with httpx.AsyncClient(timeout=10.0) as http_client:
                        resp = await http_client.post(
                            self.rest_extract_url,
                            json={"urls": [url]},
                            headers=headers
                        )
                        if resp.status_code == 200:
                            return {
                                "status": "success",
                                "mode": "live",
                                "evidence_source": "Parallel Extract Engine (Live Direct REST Endpoint)",
                                "url": url,
                                "extract_data": resp.json(),
                                "latency_ms": round((time.time() - start) * 1000, 2)
                            }
                        return {
                            "status": "error",
                            "mode": "live_error",
                            "error": f"Parallel Extract HTTP {resp.status_code}: {resp.text}",
                            "url": url
                        }
                except Exception as http_err:
                    return {
                        "status": "error",
                        "mode": "live_error",
                        "error": f"Parallel Extract error: {str(e)} | HTTP error: {str(http_err)}",
                        "url": url
                    }

        return {
            "status": "success",
            "mode": "demo",
            "evidence_source": "Parallel Extract Engine (Local research fixture)",
            "url": url,
            "summary": "Extracted key narrative structure, commercial comps, and visual references.",
            "entities": ["Neo-Tokyo", "Quantum Telemetry", "Maya Vance", "35mm Anamorphic Lenses"],
            "latency_ms": round((time.time() - start) * 1000, 2)
        }

parallel_service = ParallelService()


# 📋 Submission Evidence Matrix: Track 3 (Parallel Track)

| Official Requirement | Implementation / Evidence Path | Status | Verification Command | Truthful Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Active Runtime Gemini 2.5 Usage** | `backend/app/services/gemini_service.py`<br/>`backend/app/agents/grounded_writer_agent.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Calls `google-genai` SDK with `gemini-2.5-flash` to synthesize web sources into grounded screenplay treatments. |
| **Official Parallel Search Integration** | `backend/app/services/parallel_service.py`<br/>`backend/app/mcp/parallel_mcp_server.py` | **PASS** (Verified SDK implementation and tests) / **BLOCKED** (Live execution proof without key) | `pytest tests/test_parallel_intel.py` | Implements official Parallel Search API / SDK (`parallel-web`) using `x-api-key`, `objective`, and `search_queries`. Requires user `PARALLEL_API_KEY` for live open-web queries. |
| **Judge-Friendly Web UI** | `backend/app/static/index.html`<br/>`backend/app/main.py` | **PASS** | Open `http://localhost:8002/` | Production-safe interactive studio with Premise Input, Parallel Source Evidence Cards, zero CDN dependencies, embedded favicon, and Gemini 2.5 Grounded Synthesis. |
| **Explicit Live / Demo Mode** | `backend/app/config.py`<br/>`backend/app/services/parallel_service.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Clear mode badge, honest source attribution, and strict error handling without silent fallback. |
| **Preserve Source Evidence** | `backend/app/services/parallel_service.py` | **PASS** | File inspect | Preserves title, URL/fixture ID, excerpts, and retrieval status. |
| **Open Source License** | `LICENSE` | **PASS** | File inspect | Apache 2.0 Open Source License. |
| **Environment Template** | `.env.example` | **PASS** | File inspect | Contains parameter names and explanations without secrets. |
| **Health / Readiness Endpoint** | `backend/app/main.py` (`/api/v1/health`) | **PASS** | `GET /api/v1/health` | Exposes provider configuration state and model configuration. |

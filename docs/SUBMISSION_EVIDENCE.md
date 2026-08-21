# 📋 Submission Evidence Matrix: Track 3 (Parallel Track)

| Official Requirement | Implementation / Evidence Path | Status | Verification Command | Truthful Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Active Runtime Gemini 2.0 Usage** | `backend/app/services/gemini_service.py`<br/>`backend/app/agents/grounded_writer_agent.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Calls `google-genai` SDK to synthesize web sources into grounded screenplay treatments. |
| **Official Parallel Search Integration** | `backend/app/services/parallel_service.py`<br/>`backend/app/mcp/parallel_mcp_server.py` | **PASS** (Local Curated Fixtures) / **BLOCKED** (Live Parallel Key) | `pytest tests/test_parallel_intel.py` | Implements Parallel Search HTTP API client. Requires user `PARALLEL_API_KEY` for live open-web queries. |
| **Judge-Friendly Web UI** | `backend/app/static/index.html`<br/>`backend/app/main.py` | **PASS** | Open `http://localhost:8002/` | Interactive web studio with Premise Input, Parallel Source Evidence Cards, and Gemini 2.0 Grounded Synthesis. |
| **Explicit Live / Demo Mode** | `backend/app/config.py`<br/>`backend/app/services/parallel_service.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Clear `MODE: DEMO` badge and honest source attribution. |
| **Preserve Source Evidence** | `backend/app/services/parallel_service.py` | **PASS** | File inspect | Preserves title, URL, snippet, and retrieval status. |
| **Open Source License** | `LICENSE` | **PASS** | File inspect | Apache 2.0 Open Source License. |
| **Environment Template** | `.env.example` | **PASS** | File inspect | Contains parameter names and explanations without secrets. |
| **Health / Readiness Endpoint** | `backend/app/main.py` (`/api/v1/health`) | **PASS** | `GET /api/v1/health` | Exposes provider configuration state. |

# 📋 Submission Evidence Matrix: Track 3 (Parallel Track)

| Official Requirement | Implementation / Evidence Path | Status | Verification Command | Truthful Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini SDK Implementation and Demo Tests** | `backend/app/services/gemini_service.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Calls `google-genai>=2.19.0,<3` with current default `gemini-3.7-flash`; demo fixtures pass. |
| **Authenticated Live Gemini Proof (Historical 2.5)** | `docs/evidence/gemini-usage-proof.png` | **PASS (DATED)** | Image inspect | On 2026-08-21 the service used `gemini-2.5-flash` and returned mode live, success true, expected grounded-treatment fields, and observed latency 13204 ms. It proves the authenticated SDK path, not a Gemini 3.7 call or an end-to-end Parallel-plus-Gemini run. |
| **Parallel Integration Implementation** | `backend/app/services/parallel_service.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Implements official Parallel Search API (`parallel-web`) using `x-api-key`. Verified SDK implementation and demo tests. |
| **Live Parallel Execution Proof** | `docs/PARALLEL_LIVE_PROOF.md`<br/>`backend/app/services/parallel_service.py` | **PASS** | Authenticated live smoke | Official endpoint returned `status=success`, `mode=live`, three URL-bearing results on 2026-08-21. Credential was not stored. |
| **Judge-Friendly Web UI** | `backend/app/static/index.html`<br/>`backend/app/main.py` | **PASS** | Open `http://localhost:8002/` | Judge-friendly interactive studio with Premise Input, zero CDN dependencies, embedded favicon, demonstrating deterministic Parallel-shaped research fixtures and a local Gemini-shaped synthesis fixture. |
| **Explicit Live / Demo Mode** | `backend/app/config.py`<br/>`backend/app/services/parallel_service.py` | **PASS** | `pytest tests/test_parallel_intel.py` | Clear mode badge, honest source attribution, and strict error handling without silent fallback. |
| **Preserve Source Evidence** | `backend/app/services/parallel_service.py` | **PASS** | File inspect | Preserves title, URL/fixture ID, excerpts, and retrieval status. |
| **Open Source License** | `LICENSE` | **PASS** | File inspect | Standard MIT Open Source License. |
| **Environment Template** | `.env.example` | **PASS** | File inspect | Contains parameter names and explanations without secrets. |
| **Health / Readiness Endpoint** | `backend/app/main.py` (`/api/v1/health`) | **PASS** | `GET /api/v1/health` | Exposes provider configuration state and model configuration. |

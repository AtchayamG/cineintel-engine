# 🤖 AntiGravity Handoff: Track 3 (Parallel Track)

> Historical note: this handoff records the earlier Gemini 2.5 hardening pass. The current implementation and judge-facing materials use `gemini-3.7-flash`; see `docs/AGENT_HANDOFF.md` and `docs/SUBMISSION_EVIDENCE.md` for current state.

## Result
CineIntel Engine has been updated to be truthful, submission-ready, and strictly compliant with official Parallel Search API / SDK (`parallel-web>=0.5.0`) specifications and Google Gemini 2.5 Flash (`gemini-2.5-flash`).

Key accomplishments:
1. **Parallel Search API / SDK Implementation**: Updated request construction to use `x-api-key` header with `objective` and `search_queries` payload, preferring the official `parallel-web` SDK (`AsyncParallel`). Excerpts are normalized into clean snippet evidence.
2. **Strict Live Error Handling**: Live mode returns explicit `live_unavailable`/`live_error` when keys are missing or API calls fail, with zero silent fallbacks to demo success.
3. **Honest Demo Fixtures**: Replaced fabricated URLs and fake article snippets with self-contained local research fixtures using non-clickable fixture IDs (`fixture:...`).
4. **UI & Route Contract Bug Fix**: Fixed route regression in `/api/v1/intel/script/grounded` where a dictionary was passed to `grounded_writer_agent` instead of the genre string, eliminating the bug where a Python dictionary string was rendered in the concept summary.
5. **Removed Unsupported Hype Claims**: Eliminated the 8.8/10 market score, "high positive audience interest", ROI/performance guarantees, and viral forecasting certainty. Replaced with evidence summaries, uncertainty factors, and character-driven development recommendations.
6. **Gemini 2.5 Flash Migration**: Updated default model configuration from deprecated `gemini-2.0-flash` to stable `gemini-2.5-flash`.
7. **Clean Local UI**: Replaced external Tailwind CDN with repository-local, self-contained judge CSS and added an embedded favicon endpoint to prevent console errors.
8. **Parallel SDK Base URL & Path Endpoint Normalization**: Added URL normalization helpers in `config.py` and `parallel_service.py` (`normalize_parallel_api_origin`, `get_parallel_sdk_base_url`, `get_parallel_rest_search_url`, `get_parallel_rest_extract_url`) ensuring `AsyncParallel` receives base origin (`https://api.parallel.ai`) without trailing `/v1`, completely eliminating path duplication errors (`/v1/v1/search`).
9. **Automated Test Suite**: Built 10 comprehensive pytest suites covering SDK construction, path normalization contract, demo fixture labeling, live mode error handling, route regression, health readiness, and primary UI workflows.

---

## Files Changed

| File Path | Description of Changes |
| :--- | :--- |
| `backend/requirements.txt` | Added `parallel-web>=0.5.0` dependency. |
| `backend/app/config.py` | Added Parallel API origin normalization helpers (`parallel_sdk_base_url`, `parallel_rest_search_url`, `parallel_rest_extract_url`), updated `GEMINI_MODEL` default to `gemini-2.5-flash` and `ENABLE_MOCK_FALLBACK` default to `False`. |
| `backend/app/services/parallel_service.py` | Implemented official Parallel Search API/SDK integration (`AsyncParallel`), normalized `sdk_base_url` to prevent `/v1/v1` duplication, normalized `excerpts`, strict live mode error return, extract REST fallback, and non-clickable demo fixtures. |
| `backend/app/services/gemini_service.py` | Updated to `gemini-2.5-flash`, enforced live mode error return, handled string genre, and removed hype claims. |
| `backend/app/mcp/parallel_mcp_server.py` | Updated tool descriptions and model references to Gemini 2.5 Flash. |
| `backend/app/agents/grounded_writer_agent.py` | Added type safety, error status passthrough, and Gemini 2.5 references. |
| `backend/app/agents/trend_analyst_agent.py` | Removed 8.8/10 score and hype claims; added evidence summaries and uncertainty factors. |
| `backend/app/agents/casting_intel_agent.py` | Updated with clean type annotations and grounded framing. |
| `backend/app/routes/intel_routes.py` | Fixed bug by passing `req.genre` string instead of `trends` dict to `generate_grounded_script`. |
| `backend/app/main.py` | Added embedded SVG favicon endpoint `/favicon.ico` and updated health readiness endpoint. |
| `backend/app/static/index.html` | Replaced Tailwind CDN with repository-local CSS, added embedded favicon link, safe fixture URL rendering, and Gemini 2.5 labels. |
| `backend/tests/test_parallel_intel.py` | Expanded test suite to 10 tests covering SDK path contract, URL normalization, live errors, demo fixtures, route regression, health, and UI workflow. |
| `.env.example` | Updated default model to `gemini-2.5-flash`. |
| `README.md` | Updated architecture, badges, SDK specs, and Gemini 2.5 model labels. |
| `docs/AGENT_HANDOFF.md` | Updated handoff details, architecture map, and verification steps. |
| `docs/AGY_HANDOFF.md` | Updated AntiGravity handoff document. |
| `docs/ARCHITECTURE.md` | Updated system diagram and execution flow for Parallel SDK and Gemini 2.5. |
| `docs/DEVPOST_SUBMISSION.md` | Updated Devpost pitch and feature descriptions. |
| `docs/SUBMISSION_EVIDENCE.md` | Updated evidence matrix with status notes. |
| `docs/VIDEO_DEMO_SCRIPT.md` | Updated video script timing and technical references. |

---

## Verification

1. **Automated Pytest Suite**:
   ```bash
   cd backend
   python -m pytest -v
   ```
   *Result*: `10 passed in 0.83s`


2. **Secret Leak Audit**:
   ```bash
   gitleaks dir --no-banner --redact .
   ```
   *Result*: No leaks detected.

3. **Browser & Route Smoke Test**:
   - `GET /`: Serves clean index HTML with embedded favicon, local CSS, no console errors.
   - `GET /api/v1/health`: Returns 200 with `status: healthy`, `gemini-2.5-flash`, and Parallel provider info.
   - `POST /api/v1/intel/script/grounded`:
     ```json
     {
       "premise": "A synthetic investigator in Neo-Tokyo",
       "genre": "Cyberpunk Thriller"
     }
     ```
     *Verification*: Returns 200. `concept_summary` contains `"in Cyberpunk Thriller."` and does NOT contain any dictionary string representation like `"{'agent': ..."`.

---

## Remaining Work
- **Live Parallel API Key Verification**: Recording an authenticated live smoke call requires placing a live `PARALLEL_API_KEY` into `.env` and running with `RUNTIME_MODE=live`.

---

## Risks
- **Rate Limits & Credentials**: In live mode, missing or invalid `PARALLEL_API_KEY` or `GEMINI_API_KEY` will return `live_unavailable`/`live_error` as designed. Ensure valid keys are supplied before switching `RUNTIME_MODE=live`.

---

## Notes For Integrator
- All code and documentation changes are completely contained within the permitted worktree (`.worktrees/t3-finalize`).
- No external CDN or font dependencies remain in `index.html`.

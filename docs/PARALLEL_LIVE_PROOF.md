# Authenticated Parallel Search Proof

- Verified: 2026-08-21
- Organization: Atchayam Labs
- Runtime mode: `live`
- Integration: official `parallel-web` SDK with direct official-endpoint fallback
- Query: `current audience trends for grounded science fiction cinema`
- Result: `status=success`, `mode=live`, `result_count=3`
- Evidence source returned by the application: `Parallel Search API (Official Live Endpoint)`
- Source integrity check: all three normalized results included a URL

The credential was supplied only at runtime, was never printed, and is not stored in this repository.

## Reproduction shape

Set `PARALLEL_API_KEY` and `RUNTIME_MODE=live`, then call `ParallelService.search_open_web(...)`. The service returns explicit live status and source metadata and does not silently substitute demo fixtures on failure.

# Track 3 Live Deployment & Hybrid Runtime Guide

## Overview

The **CineIntel Engine** (Track 3: Parallel Web Systems Track) implements an autonomous narrative intelligence architecture combining **Parallel Web Systems** (open-web research, search, entity extraction) and **Google Gemini 3.7** (grounded screenplay synthesis, scene beats, and uncertainty critiques).

To support real-world production setups and hackathon evaluation, the backend architecture decouples the execution mode of each provider. This enables **truthful hybrid execution**:
- **Gemini 3.7** may run **LIVE** in production using Google Cloud Run **Application Default Credentials (ADC)** against Vertex AI without requiring a static API key.
- **Parallel Web Systems** may independently run in **LIVE** mode (with an active `PARALLEL_API_KEY`) or in **DEMO** mode (using local deterministic research fixtures).
- The system reports its execution state truthfully at all times.

---

## Runtime Mode Matrix

The backend provides granular runtime control through three environment variables:

| Variable | Values | Default | Purpose |
|---|---|---|---|
| `RUNTIME_MODE` | `demo`, `live`, `hybrid` | `demo` | Baseline runtime mode |
| `GEMINI_RUNTIME_MODE` | `demo`, `live` | Defaults to `RUNTIME_MODE` | Gemini synthesis engine runtime mode |
| `PARTNER_RUNTIME_MODE` | `demo`, `live` | Defaults to `RUNTIME_MODE` | Parallel Web Systems search & extract mode |

### Effective Runtime Modes & Health Reporting

The `/api/v1/health` endpoint calculates and reports the effective top-level mode and per-provider status:

| `GEMINI_RUNTIME_MODE` | `PARTNER_RUNTIME_MODE` | Top-Level `runtime_mode` | Provider Status |
|---|---|---|---|
| `demo` | `demo` | `demo` | Both providers serve deterministic local fixtures |
| `live` | `live` | `live` | Both providers execute live external API calls |
| `live` | `demo` | `hybrid` | Gemini executes live via ADC; Parallel serves local research fixtures |
| `demo` | `live` | `hybrid` | Parallel executes live web searches; Gemini returns structured local synthesis |

---

## Google Cloud Run & Application Default Credentials (ADC)

### ADC Architecture for Gemini 3.7
On Google Cloud Run, container workloads authenticate with Google APIs without static credentials or API keys by leveraging the instance metadata server (`http://metadata.google.internal/computeMetadata/v1/`).

When `GEMINI_RUNTIME_MODE=live` is configured:
1. The backend initializes `google.genai.Client(vertexai=True, project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)`.
2. The Google GenAI SDK automatically queries the Cloud Run ambient metadata server via `google.auth.default()`.
3. Calls to `models.generate_content` run against the Gemini 3.7 Flash endpoint on Vertex AI.

### Required IAM Configuration
The Cloud Run service account must have the **Vertex AI User** role on the Google Cloud project:
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:cineintel-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Cloud Run Environment Variables for Gemini
```env
RUNTIME_MODE=demo
GEMINI_RUNTIME_MODE=live
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=global
GEMINI_MODEL=gemini-3.7-flash
```

---

## Parallel Web Systems API Configuration

The Parallel Web Systems integration uses the official `parallel-web` Python SDK and direct REST fallback to `https://api.parallel.ai/v1/search` and `https://api.parallel.ai/v1/extract`.

### Credentials
- Live web search requires a valid `PARALLEL_API_KEY` from [Parallel](https://parallel.ai).
- For Cloud Run deployment, store the key in **Google Cloud Secret Manager**:
  ```bash
  gcloud secrets create parallel-api-key --data-file=-
  ```
- Reference the secret in Cloud Run:
  ```bash
  --set-secrets="PARALLEL_API_KEY=parallel-api-key:latest"
  ```
- Set `PARTNER_RUNTIME_MODE=live` to activate live search and extract.

---

## Fail-Closed Reliability Contract

The engine strictly enforces a **fail-closed** policy for live execution:
- If a service is configured in `live` mode but credentials (ADC or API key) are missing, the endpoint returns `status: error` with `mode: live_unavailable`.
- If an upstream API request fails or returns an error, the endpoint returns `status: error` with `mode: live_error`.
- **Under no circumstances does live mode silently fall back to demo fixtures.** This guarantees that all reported live evidence is authentic.

---

## Production Dockerfile & Cloud Run Packaging

A minimal production Dockerfile is provided at `backend/Dockerfile`.

### Container Specifications
- **Base Image:** `python:3.11-slim`
- **Port:** Injected dynamically by Cloud Run via `$PORT` (default `8080`).
- **Entrypoint:** `exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}`

### Building & Testing Locally
```bash
# Build Docker image
docker build -t cineintel-backend backend/

# Run container in hybrid mode
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e RUNTIME_MODE=demo \
  -e GEMINI_RUNTIME_MODE=demo \
  -e PARTNER_RUNTIME_MODE=demo \
  cineintel-backend
```

### Deploying to Google Cloud Run (Reference Commands)
```bash
# 1. Build and push image to Google Artifact Registry / Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/cineintel-backend:latest backend

# 2. Deploy to Cloud Run with Hybrid Execution (Gemini Live ADC + Parallel Demo)
gcloud run deploy cineintel-backend \
  --image gcr.io/PROJECT_ID/cineintel-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account cineintel-sa@PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars "RUNTIME_MODE=demo,GEMINI_RUNTIME_MODE=live,PARTNER_RUNTIME_MODE=demo,GOOGLE_CLOUD_PROJECT=PROJECT_ID,GOOGLE_CLOUD_LOCATION=global"

# 3. Deploy to Cloud Run with Full Live Execution (Both Gemini ADC + Parallel API Key)
gcloud run deploy cineintel-backend \
  --image gcr.io/PROJECT_ID/cineintel-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account cineintel-sa@PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars "RUNTIME_MODE=live,GEMINI_RUNTIME_MODE=live,PARTNER_RUNTIME_MODE=live,GOOGLE_CLOUD_PROJECT=PROJECT_ID,GOOGLE_CLOUD_LOCATION=global" \
  --set-secrets "PARALLEL_API_KEY=parallel-api-key:latest"
```

---

## Verification & Health Check

Query the health endpoint to verify configuration:
```bash
curl https://your-cloud-run-url/api/v1/health
```

Example response in hybrid mode:
```json
{
  "status": "healthy",
  "service": "CineIntel Engine",
  "track": "Parallel Web Systems Track",
  "runtime_mode": "hybrid",
  "providers": {
    "google_gemini": {
      "mode": "live",
      "configured": true,
      "model": "gemini-3.7-flash",
      "status": "LIVE_CONFIGURED",
      "evidence": "Vertex AI ADC configured (project: my-project, location: global)"
    },
    "parallel_web": {
      "mode": "demo",
      "configured": false,
      "integration": "Official Parallel Search SDK / API (parallel-web)",
      "status": "DEMO_MODE_ACTIVE",
      "evidence": "No PARALLEL_API_KEY configured (using local research fixtures)"
    }
  }
}
```

---

## Non-Deployment Disclaimer

> [!IMPORTANT]
> **Deployment Status:** This document describes the deployment architecture, configuration parameters, and container readiness. **No live deployment has occurred.** All artifacts and code changes in this repository establish readiness for deployment without making unauthorized cloud or infrastructure mutations.

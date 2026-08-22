<div align="center">

# 🌐 CineIntel Engine
### Real-Time Web Grounding, Film Trend Research & Autonomous Script Doctor
**Built for the Parallel Track — Google Cloud "Agentic Cinema: The Blockbuster Hackathon"**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Parallel Search](https://img.shields.io/badge/Parallel%20Web-Search%20API-00F0FF)](https://parallel.ai)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-3.7%20Flash-4285F4?logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

## 🌟 Overview
**CineIntel Engine** is an autonomous film intelligence and research platform featuring implemented live integrations of the official **Parallel Search API / SDK (`parallel-web`)** and **Google Gemini 3.7 Flash**. By default, the public app provides deterministic Parallel-shaped research fixtures alongside a local Gemini-shaped synthesis fixture. 

When configured in live mode, autonomous agents query open-web sources and preserve titles, URLs, excerpts, and retrieval status to ground screenplay development in verifiable evidence and explicit uncertainty bounds. Independent authenticated smoke checks now prove both Gemini 3.7 Flash and the official Parallel Search endpoint; the public evaluator remains deterministic demo mode for repeatability.

---

## 🚀 Key Features

1. **🔍 Direct Parallel Web Search Integration**:
   - Implements the official `parallel-web>=0.5.0` Python SDK (`from parallel import AsyncParallel`) and `x-api-key` request structure (`objective` and `search_queries`) to retrieve web research and excerpts in live mode.
2. **✍️ Fact-Grounded Screenplay Architecture**:
   - When configured in live mode, ingests real-world excerpts and visual benchmarks into Gemini 3.7 Flash screenplay treatments.
3. **🎭 Audience Archetype & Casting Intelligence**:
   - Evaluates character archetype resonance against genre benchmarks and voice profile recommendations.
4. **🤖 Specialized Gemini 3.7 Agent Crew**:
   - **TrendAnalystAgent**: Researches open-web narrative tropes and presents evidence with uncertainty factors.
   - **GroundedWriterAgent**: Synthesizes Parallel search excerpts into grounded screenplay treatments and scene beats.
   - **CastingIntelAgent**: Evaluates character archetypes and casting considerations.
5. **🛡️ Honest Evidence & Strict Live Error Handling**:
   - The default public app uses self-contained local research fixtures with non-clickable fixture IDs (`fixture:...`).
   - In configured live mode, failures return explicit `live_unavailable`/`live_error` without silent demo fallback.

---

## ⚡ Quickstart

```bash
cd backend
pip install -r requirements.txt
python run_backend.py
```
*API docs available at `http://localhost:8002/docs` and Web UI at `http://localhost:8002/`.*

---

## 🧪 Testing

```bash
cd backend
python -m pytest -v
```

---

## ☁️ Vercel Deployment

**Live judge demo:** https://cineintel-engine.vercel.app/  
**Public source:** https://github.com/AtchayamG/cineintel-engine

A `vercel.json` configuration is included for reproducible public deployment of the FastAPI backend. Public deployments default to `demo` mode using honest deterministic fixtures.

When deploying to Vercel, ensure you set the **Root Directory** in your Vercel project settings to `backend`.

```bash
# Install the Vercel CLI
npm i -g vercel

# Deploy the project from the root directory
vercel
```
*Note: To run in live mode, ensure you set both `PARALLEL_API_KEY` and `GEMINI_API_KEY` environment variables in your Vercel project settings and change `RUNTIME_MODE` to `live`.*

---

## 📄 License
Licensed under the **[MIT License](LICENSE)**.

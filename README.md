<div align="center">

# 🌐 CineIntel Engine
### Real-Time Web Grounding, Film Trend Research & Autonomous Script Doctor
**Built for the Parallel Track — Google Cloud "Agentic Cinema: The Blockbuster Hackathon"**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Parallel Search](https://img.shields.io/badge/Parallel%20Web-Search%20API-00F0FF)](https://parallel.ai)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

## 🌟 Overview
**CineIntel Engine** is an autonomous film intelligence and research platform powered by the official **Parallel Search API / SDK (`parallel-web`)** and **Google Gemini 2.5 Flash**. Before production greenlights occur, autonomous agents crawl open-web datasets, narrative trope benchmarks, and visual cinematography references to ground screenplay development in verifiable evidence and explicit uncertainty bounds.

---

## 🚀 Key Features

1. **🔍 Direct Parallel Web Search Integration**:
   - Uses the official `parallel-web>=0.5.0` Python SDK (`from parallel import AsyncParallel`) and `x-api-key` request structure (`objective` and `search_queries`) to retrieve web research and excerpts.
2. **✍️ Fact-Grounded Screenplay Architecture**:
   - Ingests real-world excerpts and visual benchmarks into Gemini 2.5 Flash screenplay treatments.
3. **🎭 Audience Archetype & Casting Intelligence**:
   - Evaluates character archetype resonance against genre benchmarks and voice profile recommendations.
4. **🤖 Specialized Gemini 2.5 Agent Crew**:
   - **TrendAnalystAgent**: Researches open-web narrative tropes and presents evidence with uncertainty factors.
   - **GroundedWriterAgent**: Synthesizes Parallel search excerpts into grounded screenplay treatments and scene beats.
   - **CastingIntelAgent**: Evaluates character archetypes and casting considerations.
5. **🛡️ Honest Evidence & Strict Live Error Handling**:
   - In demo mode, uses self-contained local research fixtures with non-clickable fixture IDs (`fixture:...`).
   - In live mode, failures return explicit `live_unavailable`/`live_error` without silent demo fallback.

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

## 📄 License
Licensed under the **[Apache License 2.0](LICENSE)**.
